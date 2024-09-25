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

def main():
	# Data Files
	date_list=[ '20181201','20190103', '20190201', '20190209',   '20190301', '20190330',  '20190406','20190501', '20190601', '20190622', '20190701', '20190803', '20190901', '20191001','20191015', '20191030', '20191201', '20200101', '20200122','20200130' , '20200204', '20200303','20200320' ,'20200327' , '20200401', '20200415', '20200430', '20200606', '20200702', '20200805', '20200901', '20201001', '20201029', '20201130', '20201230', '20210130', '20210228', '20210330', '20210430', '20210530', '20210630', '20210730', '20210901', '20211001', '20211201', '20220101', '20220201', '20220301', '20220401', '20220501', '20220601', '20220701', '20220801', '20220901', '20221001', '20221101', '20221201', '20230101', '20230201', '20230301', '20230401', '20230501', '20230601' , '20230701', '20230801', '20230901', '20231001', '20231101', '20231201', '20240101', '20240201', '20240301'] # '20170401', '20170501', '20170601', '20170701', '20170801','20170901', '20171002', '20171101', '20171201', '20180101', '20180201', '20180301', '20180405', '20180501', '20180601', '20180701', '20180801', '20180901', '20181001', '20181101', '20191004','20191008','20191010', '20191023','20191025','20191027','20191029', '20200122',
	ipv = 'v4'
	# asn_list = [286, 553, 1103, 1403, 3130, 7018, 7660, 8283, 8455, 12779, 15562, 31019, 34549, 37100, 37271, 37474, 44794, 47147, 47950, 51088, 55222, 57866, 59715, 64463, 196621, 196753, 206499, 209152, 328320, 328474] '_filteringASNs'
	# asn_alltime = {asn:True for asn in asn_list}
	# asn_list = [31019, 8455, 37100, 196621, 37271, 286, 553, 3130, 59715, 1103, 8283, 7018, 12779, 7660, 1403] '_alldatesASNs'
	# asn_list = [286, 7018, 7660, 37100, 37271] _selectedASNs
	# asn_list = [286,  1299, 7018, 37100, 37271, 2914] #_gtASNs 2914 = NTT added later
	# asn_names = ['KPN', 'Telia', 'AT&T', 'Seacom', 'Workonline', 'NTT'] #_gtASNs 2914 = NTT added later
	# asn_list = [286,  1299, 7018, 37100, 37271, 2914, 28329, 61832, 8455, 52873, 6079, 47147 ] #_top500AASN
	# asn_names = ['KPN', 'Telia', 'AT&T', 'Seacom', 'Workonline', 'NTT', 'G8 Net', 'Fortel','Schuberg', 'Softdados', 'RCN', 'Anexia' ] #_top500AASN
	asn_list = [174, 286, 701, 1239,  1299, 2914, 3257, 3491, 3549, 6079, 6453, 6762, 6830, 6939, 7018, 37100, 37271, 28329, 61832, 8455, 52873, 47147 ] #_t1ANDtop500AASN
	asn_names = ['Cogent', 'KPN', 'Verizon', 'Sprint', 'Telia', 'NTT', 'GTT','PCCW', 'Level3', 'RCN', 'Tata','Tel. Italia', 'Liberty Gl.', 'HE','AT&T', 'Seacom', 'Workonline', 'G8 Net', 'Fortel','Schuberg', 'Softdados', 'Anexia' ] #_t1ANDtop500AASN

	# asn_list = [ 174, 701, 1239, 1299, 2914, 3257, 3491, 3549, 6453, 6762, 6830, 6939, 7018] #_tier1
	# asn_names = ['Cogent', 'Verizon', 'Sprint', 'Telia', 'NTT', 'GTT', 'PCCW', 'Level3', 'Tata','Tel. Italia', 'Liberty Gl.', 'HE', 'AT&T'] #_tier1
	# asn_list = [ 174,  1239, 1299, 2914, 3257, 3491,   6939, 7018] #_tier1_select
	# asn_names = ['Cogent', 'Sprint', 'Telia', 'NTT', 'GTT', 'PCCW', 'HE', 'AT&T'] #_tier1_selec
	# asn_list = [ 174, 286, 1239, 1299, 2914, 3257, 3491,   6939, 7018, 37100, 37271, ] #_tier1_gt_select
	# asn_names = ['Cogent', 'KPN',  'Sprint', 'Telia', 'NTT', 'GTT', 'PCCW', 'HE', 'AT&T', 'Seacom', 'Workonline'] #_tier1_gt_selec
	# asn_list = [50304, 1299, 206356, 29467, 49697, 20514, 57381, 34854, 48821, 2613, 15605, 59715, 397143, 43578, 13030, 41327, 26073, 42473] 
	# asn_list = [ 1299, 20514, 57381, 50304, 43578, 13030, 42473] # '_selectedASNs'
	# asn_names = ['Telia', 'QBRANCH', 'FNUTT','BLIX' , 'bitNAP','INIT7', 'ANEXIA' ] #'_selectedASNs'
	# asn_list = [204092, 34019] '_outlierASNs'
	# asn_list = [1299]
	# asn_names =['Telia']
	selected ='_t1ANDtop500ASN'  #  '_gtASNs' # '_Telia' #  '_tier1' # '_tier1_gt_select' # '_selectedASNs' # 
	
	# asn_list.sort()
	asn_invalids = {asn:{} for asn in asn_list}
	asn_pos = {asn:{} for asn in asn_list}
	# v4_ROV_count = []
	# v6_ROV_count = []
	# v4_ROV_set = set()
	# v6_ROV_set = set()
	# v4_ROV_percent = []
	# v6_ROV_percent =[]
	# v4_ff_count = []
	# v6_ff_count = []
	iASN = 3
	iLen = 2
	iVal = 1
	iUnk = 4
	if ipv == 'v6':
		iVal = 5
		iASN = 6
		iLen = 7
		iUnk = 8
	for date in date_list:
		dataFile = 'DirectPeerData/RPKIvalidity/'+date +'.dp_POrpkicounts_cleaned'
		data_matrix = [line.split('|') for line in readFile(dataFile)[1:]]
		max_pos = max([int(d[iASN])+int(d[iLen])+int(d[iVal])+int(d[iUnk]) for d in data_matrix])
		for d in data_matrix:
			pos = int(d[iASN])+int(d[iLen])+int(d[iVal])+int(d[iUnk])
			if int(d[0]) in asn_invalids and pos >= max_pos*0.75:
				asn_invalids[int(d[0])][date] = int(d[iASN])+int(d[iLen])
				asn_pos[int(d[0])][date] = pos

	# Save data
	file_path = 'DirectPeerData/Tier1ASes_IP'+ipv+'_RPKIinvalidsCount.csv'
	with open(file_path,'w') as fout:
		fout.write('asn,'+','.join(date_list)+'\n')
		for asn in asn_list:
			invalids = [str(asn_invalids[asn][date]) if date in asn_invalids[asn] else 'NA' for date in date_list]
			fout.write(str(asn)+','+','.join(invalids)+'\n')
	print ('Wrote '+file_path)


		# dp_asns = [int(d[0]) for d in data_matrix]
		# for asn in asn_list:
		# 	if asn not in dp_asns:
		# 		asn_alltime[asn] = False
	# for asn in asn_alltime:
	# 	if asn_alltime[asn]:
	# 		print asn
	# 	v4_pos = np.array([int(d[2])+int(d[3])+int(d[4])+int(d[1]) for d in data_matrix])
	# 	v4_invalids = [(int(d[3])+int(d[2])) for d in data_matrix ]
	# 	# v4_invalid_percent = [(int(d[3])+int(d[2]))/float(int(d[3])+int(d[2])+int(d[1])) if int(d[1])>0 else 1 for d in data_matrix ]
	# 	v6_pos = np.array([int(d[5])+int(d[6])+int(d[7])+int(d[8]) for d in data_matrix])
	# 	v6_invalids = [(int(d[6])+int(d[7])) for d in data_matrix ]
	# 	# v6_invalid_percent = [(int(d[6])+int(d[7]))/float(int(d[5])+int(d[6])+int(d[7])) if int(d[5])>0 else 1 for d in data_matrix ]
	# 	# v4_full_feeders = [dp_asns[i] for i in range(len(dp_asns)) if v4_pos[i] >= 500000]
	# 	# v6_full_feeders = [dp_asns[i] for i in range(len(dp_asns)) if v6_pos[i] >= 40000]
	# 	# v4_ff_cut = int(percentiles(v4_pos,[0.95])[0]*0.7)
	# 	# v6_ff_cut = int (percentiles(v6_pos,[0.95])[0]*0.7)
	# 	v4_ff_cut = int(max(v4_pos)*0.75)
	# 	v6_ff_cut = int(max(v6_pos)*0.75)
	# 	v4_full_feeders = [dp_asns[i] for i in range(len(dp_asns)) if v4_pos[i] >= v4_ff_cut]
	# 	v6_full_feeders = [dp_asns[i] for i in range(len(dp_asns)) if v6_pos[i] >= v6_ff_cut]
	# 	v4_ff_count.append(len(v4_full_feeders))
	# 	v6_ff_count.append(len(v6_full_feeders))
	# 	# v4_ff_invalid_percents = [v4_invalid_percent[i] for i in range(len(dp_asns)) if v4_pos[i]>= v4_ff_cut]
	# 	# v4ROV_cut = percentiles(v4_ff_invalid_percents,[.95])[0]*0.2
	# 	invalid_threshold = 0.2
	# 	v4ROV_cut = max(v4_invalids)*invalid_threshold
	# 	# v6_ff_invalid_percents = [v6_invalid_percent[i] for i in range(len(dp_asns)) if v6_pos[i]>= v6_ff_cut]
	# 	# v6ROV_cut = percentiles(v6_ff_invalid_percents,[.95])[0]*0.2
	# 	v6ROV_cut = max(v6_invalids)*invalid_threshold
	# 	v4_ROV_asns =[]
	# 	v6_ROV_asns =[]
	# 	for i in range(len(data_matrix)):
	# 		if v4_invalids[i] < v4ROV_cut and v4_pos[i]>=v4_ff_cut:
	# 			v4_ROV_asns.append(dp_asns[i])
	# 		if v6_invalids[i] < v6ROV_cut and v6_pos[i]>=v6_ff_cut:
	# 			v6_ROV_asns.append(dp_asns[i])
	# 	v4_ROV_count.append(len(v4_ROV_asns))
	# 	v6_ROV_count.append(len(v6_ROV_asns))
	# 	v4_ROV_percent.append(float(len(v4_ROV_asns))/len(v4_full_feeders))
	# 	v6_ROV_percent.append(float(len(v6_ROV_asns))/len(v6_full_feeders))
	# 	v4_ROV_set.update(v4_ROV_asns)
	# 	v6_ROV_set.update(v6_ROV_asns)
	# print v4_ROV_count
	# print v4_ff_count
	# print v4_ROV_percent
	# print v6_ROV_count
	# print v6_ff_count
	# print v6_ROV_percent
	# print len(v4_ROV_set)
	# print len(v6_ROV_set)
	# # print ts_list

	#Statistics
	names = [str(asn) for asn in asn_list] + [str(asn) for asn in asn_list]
	samples = [asn_invalids[asn].values() for asn in asn_list]+ [asn_pos[asn].values() for asn in asn_list]
	print (len(names))
	print ('data|size|min|mean|max|5p|10p|25p|median|75p|90p|95p|99p')
	for name, sample in zip(names, samples):
		t1, t2, t3 = quartiles (sample)
		t10,t05, t90, t95, t99= percentiles(sample, [0.1,0.05, 0.9, 0.95, 0.99])
		if len(sample) > 0:
			print (f'{name}|{len(sample)}'+ '| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f'%(min(sample), float(sum(sample))/float(len(sample)), max(sample),t05, t10, t1,t2,t3, t90, t95, t99))

	# Figure Environment
	# fig =plt.figure(figsize=(8, 4)) slar
	# fig =plt.figure(figsize=(6.8,4)) huge = (16,8)
	fig =plt.figure(figsize = (13,4.5), tight_layout=True)#figsize =(5.9,3.6) hposter=(7.5,2.8)  poster = (7,2.8) sq = (4,3.6)  lar = (3, 2.2) mlar = (3.8,2.8) nar = (2.2,2.4) 4ppt = (10,4)
	sq = '_thesis'
	ax0 =fig.subplots()
	ax0.spines["top"].set_visible(False)
	ax0.spines["right"].set_visible(False)
	plt.grid(True, linestyle= ':')
	ax0.set_axisbelow(True)


	graph_type =  '_plot' #  '_plot_annotated' # 
	graph_name = ipv+'Invalids_overTime'+'_'+date_list[0]+'_'+date_list[-1] 
	markers = ['d', 'X', '*', '^', 'P', '>', '<', 'v','.' ]
	# colors = ['C0', 'C1', 'C2', 'C4', 'C3', 'C5', 'C6', 'C7', 'C8', 'C9']
	colors = ['C0', 'C1','C9', 'C4', 'C7', 'C8', 'C6',  'C5', 'C2', 'C3', 'C0']
	linestyles = ['-', '--']
	# graph_name = 'v6_RPKIinvalid_POcount'
	for i in range(len(asn_list)):
		print (i)
		dates = list(asn_invalids[asn_list[i]].keys())
		dates.sort()
		ts_list = [datetime.datetime.strptime(date, "%Y%m%d")  for date in dates]
		sample = [asn_invalids[asn_list[i]][date] for date in dates]
		ax0.plot(ts_list, sample ,marker=markers[i%9], color = colors[i%10], linestyle = linestyles[i%2], markersize = 6, linewidth = 1, label = 'AS'+str(asn_list[i])+' - '+asn_names[i]) #linestyle = linestyles[i//2],
	# for asn in asn_list[10:20]:
	# 	dates = asn_invalids[asn].keys()
	# 	dates.sort()
	# 	ts_list = [datetime.datetime.strptime(date, "%Y%m%d")  for date in dates]
	# 	sample = [asn_invalids[asn][date] for date in dates]
	# 	ax0.plot(ts_list, sample , marker='o', markersize = 4, linewidth = 1, linestyle = '--', label = 'AS'+str(asn))
	# for asn in asn_list[20: 30]:
	# 	dates = asn_invalids[asn].keys()
	# 	dates.sort()
	# 	ts_list = [datetime.datetime.strptime(date, "%Y%m%d")  for date in dates]
	# 	sample = [asn_invalids[asn][date] for date in dates]
	# 	ax0.plot(ts_list, sample ,marker='o', markersize = 4, linewidth = 1, linestyle = ':', label = 'AS'+str(asn))
	# for asn in asn_list[30:]:
	# 	dates = asn_invalids[asn].keys()
	# 	dates.sort()
	# 	ts_list = [datetime.datetime.strptime(date, "%Y%m%d")  for date in dates]
	# 	sample = [asn_invalids[asn][date] for date in dates]
	# 	ax0.plot(ts_list, sample ,marker='o', markersize = 4, linewidth = 1, linestyle = '-.', label = 'AS'+str(asn))
	# ax0.plot(ts_list, v6_ROV_percent, marker='o',markersize = 4, linewidth = 1, label = 'IPv6')
	# ax0.set(ylabel ='# RPKI invalid IP'+ipv+' prefix-origin pairs', xlabel='Month')
	ax0.set(ylabel ='# RPKI-invalid IP'+ipv+' routes', xlabel='Month')
	ax0.set_ylim(top = 6000, bottom = 0)
	# ax0.set_xlim(right=datetime.datetime(2020,3, 1), left=datetime.datetime(2017,03,15))
	# ax0.set_xlim(right=datetime.datetime(2021,8, 9), left=datetime.datetime(2018,11,20))
	ax0.set_xlim(right=datetime.datetime(2025,1, 1), left=datetime.datetime(2018,11,20))
	# ax0.xaxis.set_major_locator(mdates.MonthLocator()) #YearLocator()
	# ax0.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))#%Y
	# ax0.xaxis.set_minor_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
	fig.autofmt_xdate()

	# # Annotations
	# bbox_props = dict(boxstyle="round", fc="w", ec="w", alpha=0.9, pad = 0.15)
	# ax0.axvline(x=datetime.datetime(2019,2, 11) , linewidth = 1, color='C2', linestyle = ":")
	# ax0.annotate("AT&T", xy=(datetime.datetime(2019,2, 13), 5750), color = 'C2', fontsize=8, bbox = bbox_props)
	# ax0.annotate("AS7018", xy=(datetime.datetime(2019,2, 13), 5350), color = 'C2', fontsize=8, bbox = bbox_props)
	# ax0.axvline(x=datetime.datetime(2019,6, 28) , linewidth = 1, color='C1', linestyle = ':')
	# ax0.annotate("KPN", xy=(datetime.datetime(2019,6,30), 5750), color = 'C1', fontsize=8, bbox = bbox_props)
	# ax0.annotate("AS286", xy=(datetime.datetime(2019,6,30), 5350), color = 'C1', fontsize=8, bbox = bbox_props)
	# ax0.axvline(x=datetime.datetime(2019,4, 1) , linewidth = 1, color='C5', linestyle = ':')
	# ax0.annotate("Workonline", xy=(datetime.datetime(2019,4,3), 6000), color = 'C5', fontsize=8, bbox = bbox_props)
	# ax0.annotate("AS37271", xy=(datetime.datetime(2019,4,3), 5600), color = 'C5', fontsize=8, bbox = bbox_props) # set_bbox= (dict(xy=(datetime.datetime(2019,4,3), 5600), height =300, set_background = 'white'))
	# ax0.axvline(x=datetime.datetime(2019,4, 5) , linewidth = 1, color='C3', linestyle = ':')
	# ax0.annotate("Seacom", xy=(datetime.datetime(2019,4,7), 5100), color = 'C3', fontsize=8, bbox = bbox_props)
	# ax0.annotate("AS37100", xy=(datetime.datetime(2019,4,7), 4700), color = 'C3', fontsize=8, bbox = bbox_props)
	# ax0.axvline(x=datetime.datetime(2020,2,4) , linewidth = 1, color='C4', linestyle = ':')
	# ax0.annotate("Telia", xy=(datetime.datetime(2020,2,6), 5750), color = 'C4', fontsize=8, bbox = bbox_props)
	# ax0.annotate("AS1299", xy=(datetime.datetime(2020,2,6), 5350), color = 'C4', fontsize=8, bbox = bbox_props)
	# ax0.axvline(x=datetime.datetime(2020,3,25) , linewidth = 1, color='C7', linestyle = ':')
	# ax0.annotate("NTT", xy=(datetime.datetime(2020,3,27), 5750), color = 'C7', fontsize=8, bbox = bbox_props)
	# ax0.annotate("AS2914", xy=(datetime.datetime(2020,3,27), 5350), color = 'C7', fontsize=8, bbox = bbox_props)
	# ax0.axvline(x=datetime.datetime(2020,5,5) , linewidth = 1, color='C8', linestyle = ':')
	# ax0.annotate("GTT", xy=(datetime.datetime(2020,5,10), 6000), color = 'C8', fontsize=8, bbox = bbox_props)
	# ax0.annotate("AS3257", xy=(datetime.datetime(2020,5,10), 5600), color = 'C8', fontsize=8, bbox = bbox_props)
	# ax0.axvline(x=datetime.datetime(2020,6,29) , linewidth = 1, color='C5', linestyle = ':')
	# ax0.annotate("HE", xy=(datetime.datetime(2020,7,2), 6000), color = 'C5', fontsize=8, bbox = bbox_props)
	# ax0.annotate("AS6939", xy=(datetime.datetime(2020,7,2), 5600), color = 'C5', fontsize=8, bbox = bbox_props)
	# ax0.axvline(x=datetime.datetime(2020,6,5) , linewidth = 1, color='C0', linestyle = ':')
	# ax0.annotate("Cogent", xy=(datetime.datetime(2020,6,7), 5100), color = 'C0', fontsize=8, bbox = bbox_props)
	# ax0.annotate("AS3174", xy=(datetime.datetime(2020,6,7), 4700), color = 'C0', fontsize=8, bbox = bbox_props)
	# ax0.axvline(x=datetime.datetime(2021,2,1) , linewidth = 1, color='C2', linestyle = ':')
	# ax0.annotate("Sprint", xy=(datetime.datetime(2021,2,3), 5100), color = 'C9', fontsize=8, bbox = bbox_props)
	# ax0.annotate("AS1239", xy=(datetime.datetime(2021,2,3), 4700), color = 'C9', fontsize=8, bbox = bbox_props)
	# ax0.axvline(x=datetime.datetime(2021,1,10) , linewidth = 1, color='C6', linestyle = ':')
	# ax0.annotate("PCCW", xy=(datetime.datetime(2021,1,13), 5600), color = 'C6', fontsize=8, bbox = bbox_props)
	# ax0.annotate("AS3491", xy=(datetime.datetime(2021,1,13), 6000), color = 'C6', fontsize=8, bbox = bbox_props)


	fig.autofmt_xdate()

	# # Plotting CDF
	# # graph_type = '_CDF'
	# # graph_name = 'v4_RPKIinvalid_percent'
	# # good = np.arange(1,len(v4_invalid_percent)+1) / np.float(len(v4_invalid_percent))
	# # good_sorted = np.sort(v4_invalid_percent)
	# # ax0.step(good_sorted, good, linewidth=1)
	# # ax0.set(ylabel = 'Fraction of direct peers (full feed)', xlabel='Fraction of v4 invalid announcements')
	# # ax0.set_xlim(right = 0.05, left = 0) 
	# # ax0.set_ylim(bottom = 0, top = 1)
	ax0.legend(bbox_to_anchor=(0.5,1.2), ncol=6, loc= 'center')
	# ax0.legend(bbox_to_anchor=(1.,0.5), loc= 'center left')
	# ax0.legend(loc='center right')

	# plt.savefig('/Users/ctestart/Dropbox (MIT)/RA/BGP/Filtering/Figures/'+graph_name+graph_type+selected+sq+'.pdf')
	# plt.savefig('/Users/ctestart/Dropbox (GaTech)/MIT/RA/BGP/RPKI Filtering/Figures/'+graph_name+graph_type+selected+sq+'.png', dpi=300)
	plt.savefig('/Users/ceciliatestart/Dropbox (GaTech)/MIT/RA/BGP/RPKI Filtering/Figures/'+graph_name+graph_type+selected+sq+'.png', dpi=300)
	plt.show()


if __name__ == '__main__':
	main()
