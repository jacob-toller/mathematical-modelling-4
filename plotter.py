import json

import matplotlib.pyplot as plt

import os

saved_as = "example_save"

dict = {
	"t_list" : []
}

file_list = os.listdir("saves/{}".format(saved_as))
plot_items = [("statistics/food_stats/nest_amount","Quantity at base"),
	      ("statistics/food_stats/walker_total_amount","Currently in transit"),
	      ("statistics/food_stats/food_pile_total_amount","Remaining in piles")
  ]

def dictNestedIndexing(dict,path):
	indices = path.split("/")
	for index in indices:
		dict = dict[index]
	return dict


for filename in file_list:
	if filename.endswith(".json") == False:
		continue
	
	temp_dict = {}
	num = int(filename.split(".")[0])

	dict["t_list"].append(num)

	with open("saves/{}/{}".format(saved_as,filename)) as file:
		file_dict = json.load(file)
	
	for item in plot_items:
		path = item[0]
		label = item[1]
		temp_dict[label] = dictNestedIndexing(file_dict,path)

	dict[num] = temp_dict



fig1, ax1 = plt.subplots()	

dict["t_list"].sort()

for item in plot_items:
	label = item[1]
	dict[label] = []
	for t in dict["t_list"]:
		dict[label].append(dict[t][label])

	ax1.plot(dict["t_list"],dict[label],label=label)

ax1.set(xlabel="t",ylabel="Units of Resource")
ax1.legend()
plt.show()