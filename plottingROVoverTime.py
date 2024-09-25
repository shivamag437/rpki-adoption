import datetime
from time import mktime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# plt.style.use('seaborn-paper') #seaborn ggplot

def readFile(fileName):
	'''Returns list of lines in file'''
	with open(fileName,'r') as inputFile:
		lines=inputFile.readlines()
		return lines

def median(values):
	'''Returns the median of a list which types can be added and divided'''
	if len(values) == 1:
		return values[0]
	elif len (values)<1:
		return 0
	sortedList = sorted(values)
	center = len(values)//2
	if len(values) % 2 == 0:
		return float(sortedList[center-1]+sortedList[center])/2
	return sortedList[center]

def quartiles (values):
	'''Returns the 1st, 2nd (median) and 3rd quartile of lsit of values (floats)'''
	if len(values) == 1:
		return values[0], values[0], values[0]
	elif len(values) < 1:
		return 0,0,0
	sortedList = sorted(values)
	center = len(values)//2
	if len(values) % 2 == 0:
		return median(sortedList[:center]),float(sortedList[center-1]+sortedList[center])/2, median(sortedList[center:])
	return median(sortedList[:center]), sortedList[center], median(sortedList[center+1:])

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
	date_list=['20170401', '20170501', '20170601', '20170701', '20170801','20170901', '20171002', '20171101', '20171201', '20180101', '20180201', '20180301', '20180405', '20180501', '20180601', '20180701', '20180801', '20180901', '20181001', '20181101', '20181201', '20190103', '20190201', '20190301', '20190401', '20190501', '20190601', '20190701', '20190803', '20190901', '20191001', '20191030', '20191201', '20200101', '20200122', '20200204', '20200303', '20200401', '20200430', '20200606', '20200702', '20200805', '20200901', '20201001', '20201029', '20201130', '20201230', '20210130', '20210228', '20210330', '20210430', '20210530', '20210630', '20210730','20210901', '20211001', '20211201', '20220101', '20220201', '20220301', '20220401', '20220501', '20220601', '20220701', '20220801', '20220901', '20221001', '20221101', '20221201', '20230101', '20230201', '20230301', '20230401', '20230501', '20230601', '20230701', '20230801', '20230901', '20231001', '20231101', '20231201', '20240101', '20240201', '20240301']
	v4_ROV_count = []
	v6_ROV_count = []
	v4_ROV_set = set()
	v6_ROV_set = set()
	v4_ROV_percent = []
	v6_ROV_percent =[]
	v4_ff_count = []
	v6_ff_count = []
	for date in date_list:
		dataFile = 'DirectPeerData/RPKIvalidity/'+date +'.dp_POrpkicounts_cleaned'
		data_matrix = [line.split('|') for line in readFile(dataFile)[1:]]
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
	print (v4_ROV_count)
	print (v4_ff_count)
	print (v4_ROV_percent)
	print (v6_ROV_count)
	print (v6_ff_count)
	print (v6_ROV_percent)
	print (len(v4_ROV_set))
	print (len(v6_ROV_set))
	ts_list = [datetime.datetime.strptime(date, "%Y%m%d")  for date in date_list]
	# print ts_list

	#Statistics
	names = ['v4_ROV', 'v4_ROV_%','v6_ROV', 'v6_ROV_%']
	samples = [v4_ROV_count,v4_ROV_percent, v6_ROV_count, v6_ROV_percent]
	print ('data|size|min|mean|max|5p|10p|25p|median|75p|90p|95p|99p')
	for name, sample in zip(names, samples):
		t1, t2, t3 = quartiles (sample)
		t10,t05, t90, t95, t99= percentiles(sample, [0.1,0.05, 0.9, 0.95, 0.99])
		if len(sample) > 0:
			print (f'{name}|{len(sample)}' + '| %.4f| %.4f| %.4f| %.4f| %.4f| %.4f| %.4f| %.4f| %.4f| %.4f| %.4f'%(min(sample), float(sum(sample))/float(len(sample)), max(sample),t05, t10, t1,t2,t3, t90, t95, t99))

	# Figure Environment
	# fig =plt.figure(figsize=(8, 4)) 
	# fig =plt.figure(figsize=(6.8,4))
	fig =plt.figure(figsize =(10,3.5), tight_layout=True)#figsize =(5.9,3.6) sq = (4,3.6) hsq = (5,3.5) lar = (3, 2.2) mlar = (3.8,2.8) nar = (2.2,2.4) poster = (7,3) hposter = (10,3.5) hhposter = (15,3.5) 4ppt = (8,4)
	sq = '_thesis'
	ax0 =fig.subplots()
	ax0.spines["top"].set_visible(False)
	ax0.spines["right"].set_visible(False)
	plt.grid(True, linestyle= ':')
	# ax0.set_title ('RPKI enforcement over time', pad =17, fontsize = 10)
	ax0.set_axisbelow(True)


	graph_type = '_plot_marker_'
	graph_name = 'ROVpercentP_overTime_t'+str(invalid_threshold)
	# graph_name = 'v6_RPKIinvalid_POcount'
	ax0.plot(ts_list, np.array(v4_ROV_percent)*100,marker='o', markersize = 4, linewidth = 1, label = 'IPv4') #'ASes filtering RPKI-invalid IPv4 prefixes')
	ax0.plot(ts_list, np.array(v6_ROV_percent)*100, marker='o',markersize = 4, linewidth = 1, label = 'IPv6') #'ASes filtering RPKI-invalid IPv6 prefixes')
	# ax0.set(ylabel = 'Fraction of measured networks', xlabel='Month') #'Fraction of full feeder ASes', xlabel='Month')
	ax0.set(ylabel = '%'+' of full feeder ASes') #, xlabel='Month') #'Fraction of full feeder ASes', xlabel='Month')
	ax0.set_ylim(top = 100)
	# ax0.set_xlim(right=datetime.datetime(2021,3, 2), left=datetime.datetime(2017,03,15))
	ax0.set_xlim(right=datetime.datetime(2025,1, 1), left=datetime.datetime(2017,3,15))
	# ax0.xaxis.set_major_locator(mdates.MonthLocator()) #YearLocator()
	# ax0.xaxis.set_major_formatter(mdates.DateFormatter('%m'))#%Y
	# ax0.xaxis.set_minor_locator(mdates.DayLocator())
	fig.autofmt_xdate()

	# Plotting CDF
	# graph_type = '_CDF'
	# graph_name = 'v4_RPKIinvalid_percent'
	# good = np.arange(1,len(v4_invalid_percent)+1) / np.float(len(v4_invalid_percent))
	# good_sorted = np.sort(v4_invalid_percent)
	# ax0.step(good_sorted, good, linewidth=1)
	# ax0.set(ylabel = 'Fraction of direct peers (full feed)', xlabel='Fraction of v4 invalid announcements')
	# ax0.set_xlim(right = 0.05, left = 0) 
	# ax0.set_ylim(bottom = 0, top = 1)
	# ax0.legend(bbox_to_anchor=(1.,0.5), loc= 'center left')
	ax0.legend(loc= 'lower right')

	plt.savefig('/Users/ceciliatestart/Dropbox (GaTech)/MIT/RA/BGP/RPKI Filtering/Figures/'+graph_name+graph_type+date_list[0]+'_'+date_list[-1]+sq+'.png', dpi=300)
	# plt.savefig('/Users/ctestart/Dropbox (GaTech)/MIT/RA/BGP/RPKI Filtering/Figures/'+graph_name+graph_type+date_list[0]+'_'+date_list[-1]+sq+'.png', dpi=300)
	# plt.savefig('/Users/ctestart/Dropbox (MIT)/RA/BGP/Filtering/Figures/'+graph_name+graph_type+date_list[0]+'_'+date_list[-1]+sq+'.pdf')
	plt.show()


if __name__ == '__main__':
	main()
