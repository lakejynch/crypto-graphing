import plotly.express as px
import pandas as pd
import json


def testDepth(x):
	if type(x) is dict and x:
		return 1 + max(testDepth(x[a]) for a in x)
	if type(x) is list and x:
		return 1 + max(testDepth(a) for a in x)
	return 0

# load data
with open("info.json", "r") as jf:
	data = json.load(jf)

# get depth of json
depth = testDepth(data)


# name columns (relating to depth)
columns = []
base = "category-"
while len(columns) < depth:
	rebase = base + str(len(columns))
	columns.append(rebase)

# normalize json to csv
df = pd.json_normalize(data)
df = list(df.columns)

# flatten data
flat_data = []
for item in df:
	flattened = item.split(".")
	while len(flattened) < depth:
		flattened += [None]
	flat_data.append(flattened)

df = pd.DataFrame(columns = columns, data = flat_data)

# add values to DF for sizing
val = []
for index, row in df.iterrows():
	val.append(len(df["category-0"].loc[df["category-0"] == row["category-0"]]) / len(df))
df["value"] = val

# plot
fig = px.sunburst(df, path = ["category-0","category-1","category-2"], values = "value",
					width = 2500, height = 2500)

# export
fig.write_html("output.html")
#fig.write_image("output.png")
print("done")
