import sys
import os
import time
from urllib.request import urlopen 
import json
import streamlit as st
import pandas as pd

st.title("Looping 4 first posts from json file")
st.write("Posts")

num_of_entries = 4
time_int= 5

url = "https://jsonplaceholder.typicode.com/posts"
response = urlopen(url) 
json_posts = json.loads(response.read())

with st.empty():
	while True:
		for i in range(num_of_entries):
			df = pd.DataFrame(json_posts[i].items()).astype("str")
			df
			time.sleep(time_int)
