import glob
import json
import os
import matplotlib.pyplot as plt
plt.rcParams["figure.dpi"] = 100
plt.rcParams['savefig.dpi'] = 300

def dictNestedIndexing(dict,path):
	indices = path.split("/")
	for index in indices:
		dict = dict[index]
	return dict

folder_list = []

folder_list += glob.glob("saves/lambda-*-*")

output_dict = {}

for folder_name in folder_list:
	print("processing folder '{}'".format(folder_name))
	lambda_val = float(folder_name.split("-")[1].replace("min","-"))

	try:
		output_dict[lambda_val]["raw"]
	except KeyError:
		output_dict[lambda_val] = {}
		output_dict[lambda_val]["raw"] = []
			
	file_list = os.listdir(folder_name)
	temp_dict = {"t_list":[]}
	for filename in file_list:
		if filename.endswith(".json") == False:
			continue
		
		num = int(filename.split(".")[0])

		temp_dict["t_list"].append(num)
		with open("{}/{}".format(folder_name,filename)) as file:
			file_dict = json.load(file)
		
		temp_dict[num] = file_dict["statistics"]["food_stats"]["nest_amount"]

	temp_dict["t_list"].sort()
	temp_dict["y_list"] = []
	for t in temp_dict["t_list"]:
		temp_dict["y_list"].append(temp_dict[t])

	output_dict[lambda_val]["raw"].append({"t_list":temp_dict["t_list"],"y_list":temp_dict["y_list"]})


lambda_values = list(output_dict.keys())
lambda_values.sort()
print(lambda_values)

for lambda_val in lambda_values:
	trial_list = output_dict[lambda_val]["raw"]

	t_list = []
	worst = (0,0)
	best = (0,99999999)
	avg_finish=0
	
	for i,trial in enumerate(trial_list):
		avg_finish += len(trial["t_list"])

		if len(trial["t_list"]) > worst[1]:
			worst = (i,len(trial["t_list"]))

		if len(trial["t_list"]) < best[1]:
			best = (i,len(trial["t_list"]))

	t_list = trial_list[worst[0]]["t_list"]
	avg_finish /= len(trial_list)

	avg_sq_dist = 0
	for trial in trial_list:
		avg_sq_dist += ((len(trial["t_list"]) - avg_finish) ** 2)

	avg_sq_dist /= len(trial_list)
	avg_sq_dist **= 0.5

	output_dict[lambda_val]["best_finish_time"] = best[1]
	output_dict[lambda_val]["avg_finish_time"] = avg_finish
	output_dict[lambda_val]["std_dev_finish_time"] = avg_sq_dist
	output_dict[lambda_val]["worst_finish_time"] = worst[1]

	
	avg_y_list = []
	best_y_list = []
	worst_y_list = []
	for t in t_list:
		count = 0
		for trial in trial_list:
			try:
				count += trial["y_list"][t]
			except IndexError:
				count += trial["y_list"][-1]
		
		count /= len(trial_list)
		avg_y_list.append(count)

		worst_y_list.append(trial_list[worst[0]]["y_list"][t])
		try:
			best_y_list.append(trial_list[best[0]]["y_list"][t])
		except IndexError:
			best_y_list.append(trial_list[best[0]]["y_list"][-1])


	output_dict[lambda_val]["t_list"] = t_list
	output_dict[lambda_val]["avg_y_list"] = avg_y_list
	output_dict[lambda_val]["worst_y_list"] = worst_y_list
	output_dict[lambda_val]["best_y_list"] = best_y_list
	
fig1, ax1 = plt.subplots()


fig_list = []
best_list = []
avg_list = []
worst_list = []
std_dev_list = []

for lambda_val in lambda_values:
	ax1.plot(output_dict[lambda_val]["t_list"],output_dict[lambda_val]["avg_y_list"],label="$\lambda$ = {}".format(lambda_val))

	temp_fig, temp_ax = plt.subplots()
	fig_list.append((temp_fig,temp_ax))
	temp_ax.plot(output_dict[lambda_val]["t_list"],output_dict[lambda_val]["best_y_list"],label="best performance")
	temp_ax.plot(output_dict[lambda_val]["t_list"],output_dict[lambda_val]["avg_y_list"],label="avg. performance")
	temp_ax.plot(output_dict[lambda_val]["t_list"],output_dict[lambda_val]["worst_y_list"],label="worst performance")
	temp_ax.set(xlabel="t",ylabel="Units of Resource",title="$\lambda$ = {}".format(lambda_val))
	temp_ax.legend()

	best_list.append(output_dict[lambda_val]["best_finish_time"])
	avg_list.append(output_dict[lambda_val]["avg_finish_time"])
	worst_list.append(output_dict[lambda_val]["worst_finish_time"])
	std_dev_list.append(output_dict[lambda_val]["std_dev_finish_time"])

ax1.set(xlabel="t",ylabel="Units of Resource")
ax1.legend()



fig2, ax2 = plt.subplots()

ax2.plot(lambda_values,best_list,label="best finish time",linestyle="dashed")
ax2.plot(lambda_values,avg_list,label="avg. finish time")
ax2.plot(lambda_values,worst_list,label="worst finish time",linestyle="dashed")

ax2.set(xlabel="$\lambda$",ylabel="Duration, t")
ax2.legend()

fig3, ax3 = plt.subplots()

ax3.plot(lambda_values,avg_list,label="avg. finish time")
ax3.errorbar(lambda_values,avg_list,yerr=std_dev_list,fmt ="x",label="std. dev.")
ax3.legend()

ax3.set(xlabel="$\lambda$",ylabel="Avg. Completion Time, t")

for lambda_val in lambda_values:
	del output_dict[lambda_val]["raw"]
	del output_dict[lambda_val]["t_list"]
	del output_dict[lambda_val]["avg_y_list"]
	del output_dict[lambda_val]["best_y_list"]
	del output_dict[lambda_val]["worst_y_list"]

with open("temp.json","w") as file:
	json.dump(output_dict,file,indent=4)


plt.show()




