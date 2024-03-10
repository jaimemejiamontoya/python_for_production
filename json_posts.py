import sys
import os
import time
import json
import streamlit as st
import pandas as pd

st.title("Looping 4 first posts from json file")
st.write("Posts")

json_file = "posts.json"

num_of_entries = 4
time_interval = 5

with open(json_file, "r") as file:
	posts = json.load(file)

with st.empty():

	while True:
		for i in range(num_of_entries):
			df = pd.DataFrame(posts[i].items()).astype("str")
			df
			time.sleep(time_interval)
