import datetime
import numpy as np
import os
import csv

# plt.style.use('seaborn-paper') #seaborn ggplot

def readFile(fileName):
	'''Returns list of lines in file'''
	with open(fileName,'r') as inputFile:
		lines=inputFile.readlines()
		return lines

def percentiles (values, percentiles_list):
	''' Returns a list with the percentiles requested rouding to the closest list position'''
	l = len(values)
	if l == 1:
		return [values[0]]*len(percentiles_list)
	elif l < 1:
		return [0]*len(percentiles_list)
	sortedList = sorted(values)
	indexes = [int(round(p*l))-1 for p in percentiles_list]
	p_values = [sortedList[i] for i in indexes]
	return p_values

def cleanOutliers (counts):
	'''Extracts values over 50% 95p in list'''
	p95 = percentiles (counts, [0.95])[0]
	for count in counts:
		if count >p95*1.5:
			counts.remove(count)


def main():
	# Data Files
	# date_list=['20170401', '20170501', '20170601', '20170701', '20170801','20170901', '20171002', '20171101', '20171201', '20180101', '20180201', '20180301', '20180405', '20180501', '20180601', '20180701', '20180801', '20180901', '20181001', '20181101', '20181201', '20190103', '20190201', '20190301', '20190401', '20190501', '20190601', '20190701', '20190803', '20190901', '20191001', '20191030', '20191201', '20200101', '20200122', '20200204', '20200303', '20200401', '20200430', '20200606', '20200702', '20200805', '20200901', '20201001', '20201029', '20201130', '20201230']
	date_list=[]
	for filename in os.listdir('DirectPeerData'):
		if filename.endswith('.dp_POrpkicounts_cleaned'):
			date_list.append(filename.split('.')[0])
	v4_ROV_count = []
	v6_ROV_count = []
	v4_ROV_set = set()
	v6_ROV_set = set()
	v4_ROV_percent = []
	v6_ROV_percent =[]
	v4_ff_count = []
	v6_ff_count = []
	for date in date_list:
		dataFile = 'DirectPeerData/'+date +'.dp_POrpkicounts_cleaned'
		try:
			data_matrix = [line.split('|') for line in readFile(dataFile)[1:]]
		except:
			print ('No data for '+date)
			continue
		dp_asns = [d[0] for d in data_matrix]
		v4_pos = np.array([int(d[2])+int(d[3])+int(d[4])+int(d[1]) for d in data_matrix])
		v4_invalids = [(int(d[3])+int(d[2])) for d in data_matrix ]
		# v4_invalid_percent = [(int(d[3])+int(d[2]))/float(int(d[3])+int(d[2])+int(d[1])) if int(d[1])>0 else 1 for d in data_matrix ]
		v6_pos = np.array([int(d[5])+int(d[6])+int(d[7])+int(d[8]) for d in data_matrix])
		v6_invalids = [(int(d[6])+int(d[7])) for d in data_matrix ]
		# v6_invalid_percent = [(int(d[6])+int(d[7]))/float(int(d[5])+int(d[6])+int(d[7])) if int(d[5])>0 else 1 for d in data_matrix ]
		# v4_full_feeders = [dp_asns[i] for i in range(len(dp_asns)) if v4_pos[i] >= 500000]
		# v6_full_feeders = [dp_asns[i] for i in range(len(dp_asns)) if v6_pos[i] >= 40000]
		# v4_ff_cut = int(percentiles(v4_pos,[0.95])[0]*0.7)
		# v6_ff_cut = int (percentiles(v6_pos,[0.95])[0]*0.7)
		v4_ff_cut = int(max(v4_pos)*0.75)
		v6_ff_cut = int(max(v6_pos)*0.75)
		v4_full_feeders = [dp_asns[i] for i in range(len(dp_asns)) if v4_pos[i] >= v4_ff_cut]
		v6_full_feeders = [dp_asns[i] for i in range(len(dp_asns)) if v6_pos[i] >= v6_ff_cut]
		v4_ff_count.append(len(v4_full_feeders))
		v6_ff_count.append(len(v6_full_feeders))
		v4_ff_invalids = [v4_invalids[i] for i in range(len(dp_asns)) if dp_asns[i] in v4_full_feeders]
		v6_ff_invalids = [v6_invalids[i] for i in range(len(dp_asns)) if dp_asns[i] in v6_full_feeders]
		# v4_ff_invalid_percents = [v4_invalid_percent[i] for i in range(len(dp_asns)) if v4_pos[i]>= v4_ff_cut]
		# v4ROV_cut = percentiles(v4_ff_invalid_percents,[.95])[0]*0.2
		invalid_threshold = 0.2
		cleanOutliers (v4_ff_invalids)
		v4ROV_cut = max(v4_ff_invalids)*invalid_threshold
		# v6_ff_invalid_percents = [v6_invalid_percent[i] for i in range(len(dp_asns)) if v6_pos[i]>= v6_ff_cut]
		# v6ROV_cut = percentiles(v6_ff_invalid_percents,[.95])[0]*0.2
		cleanOutliers(v6_ff_invalids)
		v6ROV_cut = max(v6_ff_invalids)*invalid_threshold
		v4_ROV_asns =[]
		v6_ROV_asns =[]
		for i in range(len(data_matrix)):
			if v4_invalids[i] < v4ROV_cut and v4_pos[i]>=v4_ff_cut:
				v4_ROV_asns.append(dp_asns[i])
			if v6_invalids[i] < v6ROV_cut and v6_pos[i]>=v6_ff_cut:
				v6_ROV_asns.append(dp_asns[i])
		v4_ROV_count.append(len(v4_ROV_asns))
		v6_ROV_count.append(len(v6_ROV_asns))
		v4_ROV_percent.append(float(len(v4_ROV_asns))/len(v4_full_feeders))
		v6_ROV_percent.append(float(len(v6_ROV_asns))/len(v6_full_feeders))
		v4_ROV_set.update(v4_ROV_asns)
		v6_ROV_set.update(v6_ROV_asns)
	# print (v4_ROV_count)
	# print (v4_ff_count)
	# print (v4_ROV_percent)
	# print (v6_ROV_count)
	# print (v6_ff_count)
	# print (v6_ROV_percent)
	# print (len(v4_ROV_set))
	# print (len(v6_ROV_set))
	ts_list = [datetime.datetime.strptime(date, "%Y%m%d")  for date in date_list]
	# print ts_list
	
	combined = zip(ts_list, v4_ROV_percent, v6_ROV_percent, date_list)
	sorted_combined = sorted(combined, key=lambda x: x[0])
	ts_list, v4_ROV_percent, v6_ROV_percent, date_list = zip(*sorted_combined)

	#write to csv
	with open('RPKIFilteringWebpage/ROVoverTime.csv', 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['date', 'ipv4', 'ipv6', 'date_file'])
		for i in range(len(ts_list)):
			writer.writerow([ts_list[i], v4_ROV_percent[i]*100, v6_ROV_percent[i]*100, date_list[i]])

	print ("data written to ROVoverTime.csv")


if __name__ == '__main__':
	main()
