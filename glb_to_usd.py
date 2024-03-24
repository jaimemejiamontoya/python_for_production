import os
import hou

class USDmigrationUtils:
    def __init__(self):
        self.asset_name = None

    def createMainTemplate(self, dir_path):
        print("Executing template structure...")

        obj_file = [file for file in os.listdir(dir_path) if file.endswith(".glb")][0]

        self.asset_name = obj_file[:-4]

        # create glt network
        glt_net = hou.node("/obj").createNode("gltf_hierarchy", "glb_file")
        glt_net.parm("filename").set(dir_path + "/" + obj_file)       
        glt_net.parm("assetfolder").set(dir_path) 
        glt_net.parm("flattenhierarchy").set(True) 
        glt_net.parm("importcustomattributes").set(False)
        glt_net.parm("buildscene").pressButton()


        #sopcreate lop
        root_path = "/stage"
        sopcreate_lop = hou.node(root_path).createNode("sopcreate", self.asset_name)
        sopcreate_lop.parm("enable_partitionattribs").set(0)

        # merge  gltf file
        gltf_file =  hou.node(sopcreate_lop.path() + "/sopnet/create").createNode("object_merge")
        gltf_file.parm("objpath1").set(glt_net.path() + "/geo1/gltf1")

        #for loop
        for_each_begin = gltf_file.createOutputNode("block_begin", "foreach_begin1")
        for_each_begin.parm("method").set(1)
        for_each_begin.parm("blockpath").set("../foreach_end1")
        for_each_begin.parm("createmetablock").pressButton()
        meta_node = hou.node(for_each_begin.parent().path() + "/foreach_begin1_metadata1")
        meta_node.parm("blockpath").set("../foreach_end1")

        #attribute wrangle
        attr_wrangle = for_each_begin.createOutputNode("attribwrangle")
        attr_wrangle.setInput(1,meta_node)
        attr_wrangle.parm("class").set(1)
        attr_wrangle.parm("snippet").set('string raw_path[]  = split(@name, "_",1);\nif (len(raw_path) > 1) {\ns@path = "/" + split(@name, "_",1)[1];\n}else {s@path = "/" + split(@name, "_",1)[0];}\nif(split(s@shop_materialpath, "_")[-1] == "Eye") s@path = "/Eye";')


        #end loop
        for_each_end = attr_wrangle.createOutputNode("block_end","foreach_end1")
        for_each_end.parm("itermethod").set(1)
        for_each_end.parm("method").set(1)
        for_each_end.parm("class").set(0)
        for_each_end.parm("useattrib").set(1)
        for_each_end.parm("attrib").set("shop_materialpath")
        for_each_end.parm("blockpath").set("../foreach_begin1")
        for_each_end.parm("templatepath").set("../foreach_begin1")

        #attrib delete
        att_delete = for_each_end.createOutputNode("attribdelete")
        att_delete.parm("ptdel").set("*")
        att_delete.parm("vtxdel").set("* ^N ^uv")
        att_delete.parm("primdel").set("name shop_materialpath" )
        att_delete.parm("dtldel").set("*")

        output_sop = att_delete.createOutputNode("output")

        #create primitive lop
        primitive_lop = hou.node(root_path).createNode("primitive")
        primitive_lop.parm("primpath").set(self.asset_name)
        primitive_lop.parm("primkind").set("component")

        #graft stages
        graft_stages_lop = primitive_lop.createOutputNode("graftstages")
        graft_stages_lop.setNextInput(sopcreate_lop)
        graft_stages_lop.parm("primkind").set("subcomponent")

        #material lop
        materials_net = hou.node(glt_net.path() + "/materials")
        materials = materials_net.children()
        materiallib_lop = graft_stages_lop.createOutputNode("materiallibrary")
        materiallib_lop.parm("materials").set(len(materials))


        for i, material in enumerate(materials):
            material_name = str(material).split("_",1)[1]

            # rename Skin to Head
            if material_name == "Skin":
                   material_name = "Head"

            # rename material subnetwork      
            hou.node(material.path()).setName(material_name)

            materiallib_lop.parm(f"matnode{i+1}").set(str(material))
            materiallib_lop.parm(f"matpath{i+1}").set(f"/{self.asset_name}/materials/{material}_mat")
            materiallib_lop.parm(f"assign{i+1}").set(1)
            materiallib_lop.parm(f"geopath{i+1}").set(f"/{self.asset_name}/{self.asset_name}/{material_name}")

            #set mat network inside
            mat_subnetwork = hou.node(materiallib_lop.path()).createNode("subnet",str(material))

            #texture maps and nodes

            # get color map from imported materials
            base_color_path = hou.node(material.path()).parm("basecolor_texture").eval()

            # create nodes and connections inside material subnetwork

            mtlx_image = hou.node(mat_subnetwork.path()).createNode("mtlximage")
            mtlx_image.parm("file").set(base_color_path)
            mtlsurface = hou.node(mat_subnetwork.path()).createNode("mtlxstandard_surface")

            output_ref = hou.node(mat_subnetwork.path() + "/suboutput1")

            mtlx_image_output = mtlx_image.outputIndex("out")
            mtlsurface_input = mtlsurface.inputIndex("base_color")
            mtlsurface_output = mtlsurface.outputIndex("out")

            mtlsurface.setInput(mtlsurface_input, mtlx_image, mtlx_image_output)
            output_ref.setNextInput(mtlsurface, mtlsurface_output)

            mat_subnetwork.setMaterialFlag(True)

            materiallib_lop.layoutChildren()
            mat_subnetwork.layoutChildren()



        #usd rop export
        usd_rop_export = materiallib_lop.createOutputNode("usd_rop")
        usd_rop_export.parm("lopoutput").set(dir_path + "/usd_export/" + self.asset_name + ".usd")