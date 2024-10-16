import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv
import os

plt.style.use('seaborn-paper') #seaborn ggplot

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
	date = '20230601' #'20190901' #'20210530' #'20201029'
	date_list=[]
	for filename in os.listdir('DirectPeerData'):
		if filename.endswith('.dp_POrpkicounts_cleaned'):
			date_list.append(filename.split('.')[0])
	ipvs = ['v4', 'v6']
	for ipv in ipvs:
		for date in date_list:
			dataFile = 'DirectPeerData/'+date +'.dp_POrpkicounts_cleaned'
			data_matrix = [line.split('|') for line in readFile(dataFile)[1:]]
			data_matrix.sort(key=lambda d: int(d[0]))
			# data_matrix.sort(key= lambda d: int(d[2])+int(d[3]))
			# collector_list =[d[0] for d in data_matrix]
			dp_asns = [d[0] for d in data_matrix]
			v4_invalidASN = np.array([int(d[3]) for d in data_matrix])
			v4_invalidLength = np.array([int(d[2]) for d in data_matrix])
			v4_valid = np.array([int(d[1]) for d in data_matrix])
			v4_unknown = np.array([int(d[4]) for d in data_matrix])
			v4_pos = np.array([int(d[2])+int(d[3])+int(d[4])+int(d[1]) for d in data_matrix])
			v4_invalid_percent = [(int(d[3])+int(d[2]))/float(int(d[3])+int(d[2])+int(d[1])) if int(d[1])>0 else 1 for d in data_matrix ]
			v6_invalidASN = np.array([int(d[7]) for d in data_matrix])
			v6_invalidLength = np.array([int(d[6]) for d in data_matrix])
			v6_valid = np.array([int(d[5]) for d in data_matrix])
			v6_unknown = np.array([int(d[8]) for d in data_matrix])
			v6_pos = np.array([int(d[5])+int(d[6])+int(d[7])+int(d[8]) for d in data_matrix])
			v6_invalid_percent = [(int(d[6])+int(d[7]))/float(int(d[5])+int(d[6])+int(d[7])) if int(d[5])>0 else 1 for d in data_matrix ]
			v4_dp_asns = [data_matrix[i][0] for i in range(len(data_matrix)) if v4_pos[i]>0]
			v6_dp_asns = [data_matrix[i][0] for i in range(len(data_matrix)) if v6_pos[i]>0]

			#Statistics
			names = ['v4_valid', 'v4_invalidLength', 'v4_invalidASN', 'v4_unknown', 'all_POs', 'v4_invalid', 'v4_invalid_percent','v6_valid', 'v6_invalidLength', 'v6_invalidASN', 'v6_unknown', 'v6_POs', 'v6_invalid', 'v6_invalid_percent']
			samples = [v4_valid, v4_invalidLength, v4_invalidASN, v4_unknown, v4_pos, v4_invalidASN+v4_invalidLength, v4_invalid_percent, v6_valid, v6_invalidLength, v6_invalidASN, v6_unknown, v6_pos, v6_invalidASN+v6_invalidLength, v6_invalid_percent]
			# names = ['v6_valid', 'v6_invalidLength', 'v6_invalidASN', 'v6_unknown', 'v6_POs', 'v6_invalid', 'v6_invalid_percent']
			# samples = [v6_valid, v6_invalidLength, v6_invalidASN, v6_unknown, v6_pos, v6_invalidASN+v6_invalidLength, v6_invalid_percent]
			print (date)
			print ('data|size|min|mean|max|5p|10p|25p|median|75p|90p|95p|99p')
			for name, sample in zip(names, samples):
				t1, t2, t3 = quartiles (sample)
				t10,t05, t90, t95, t99= percentiles(sample, [0.1,0.05, 0.9, 0.95, 0.99])
				if len(sample) > 0:
					print ('%s| %d| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f| %.2f'%(name, len(sample),min(sample), float(sum(sample))/float(len(sample)), max(sample),t05, t10, t1,t2,t3, t90, t95, t99))

			# dp_filtering = [(col, dp, x) for x,dp,col, po in zip(v4_invalid_percent,dp_asns, collector_list, v4_pos) if x<0.03 and po>500000]
			filtering_count = 0
			ROV_asns =[]
			print ('v4 prefixes')
			# v4_ff_cut = int(max(v4_pos,[0.95])[0]*0.7)
			v4_ff_cut = int(max(v4_pos)*0.75)
			print (v4_ff_cut)
			# v4_ff_invalid_percents = [v4_invalid_percent[i] for i in range(len(v4_valid)) if v4_pos[i]>= v4_ff_cut]
			v4_ff_invalids = [v4_invalidLength[i]+v4_invalidASN[i] for i in range(len(v4_valid)) if v4_pos[i]>= v4_ff_cut]
			cleanOutliers(v4_ff_invalids)
			print (len(v4_ff_invalids))
			# v4ROV_cut = max(v4_ff_invalid_percents,[.95])[0]*0.2
			v4ROV_cut = max(v4_ff_invalids)*0.2
			print (v4ROV_cut)
			info_asns = ['1299','2914' '59715', '50300', '34968', '37271', '60501', '328474']
			for i in range(len(data_matrix)):
				if dp_asns[i] in info_asns:
					print ('%s, %.2f, %d/%d, %d'%(dp_asns[i], v4_invalid_percent[i], v4_invalidASN[i]+v4_invalidLength[i], v4_invalidASN[i]+v4_invalidLength[i]+v4_valid[i], v4_pos[i]))
				if v4_invalidLength[i]+v4_invalidASN[i]<= v4ROV_cut and v4_pos[i]>=v4_ff_cut:
					# print data_matrix[i]
					print ('%s, %.2f, %d/%d, %d'%(dp_asns[i], v4_invalid_percent[i], v4_invalidASN[i]+v4_invalidLength[i], v4_invalidASN[i]+v4_invalidLength[i]+v4_valid[i], v4_pos[i]))
					filtering_count +=1
					ROV_asns.append(int(dp_asns[i]))

			print ('Direct peers filtering: %d'%len(set(ROV_asns)))
			print (set(ROV_asns))
			print ('Total Direct peers: %d'%len(set (v4_dp_asns)))
			v4_full_feeders = [int(dp_asns[i]) for i in range(len(dp_asns)) if v4_pos[i] >= v4_ff_cut]
			print ('Total Full Feeders: %d'%len(v4_full_feeders))
			print (v4_full_feeders)

			v6ROV_asns =[]
			print ('v6 prefixes')
			# ff_cut = int (percentiles(v6_pos,[0.95])[0]*0.7)
			v6_ff_cut = int(max(v6_pos)*0.75)
			print (v6_ff_cut)
			v6_ff_invalids = [v6_invalidLength[i]+v6_invalidASN[i] for i in range(len(v6_valid)) if v6_pos[i]>= v6_ff_cut]
			# v6_ff_invalid_percents = [v6_invalid_percent[i] for i in range(len(v6_valid)) if v6_pos[i]>= ff_cut]
			cleanOutliers(v6_ff_invalids)
			print (len(v6_ff_invalids))
			# v6ROV_cut = percentiles(v6_ff_invalid_percents,[.95])[0]*0.2
			v6ROV_cut = max(v6_ff_invalids)*0.2
			print (v6ROV_cut)
			for i in range(len(data_matrix)):
				if v6_invalidLength[i]+v6_invalidASN[i]<= v6ROV_cut and v6_pos[i]>=v6_ff_cut:
					# print data_matrix[i]
					print ('%s, %.2f, %d/%d, %d'%(dp_asns[i], v6_invalid_percent[i], v6_invalidASN[i]+v6_invalidLength[i],v6_invalidASN[i]+v6_invalidLength[i]+v6_valid[i], v6_pos[i] ))
					v6ROV_asns.append(int(dp_asns[i]))

			print ('Direct peers filtering: %d'%len(set(v6ROV_asns)))
			print (set(v6ROV_asns))
			print ('Total Direct peers: %d'%len(set (v6_dp_asns)))
			v6_full_feeders = [int(dp_asns[i]) for i in range(len(dp_asns)) if v6_pos[i] >= v6_ff_cut]
			print ('Total Full Feeders: %d'%len(v6_full_feeders))
			# print v6_full_feeders
			v4_v6_filtering = [x for x in v6ROV_asns if x in ROV_asns]
			print ('IPv4 and PIv6 filtering :%d'%(len(v4_v6_filtering)))

			# Figure Environment
			# fig =plt.figure(figsize=(8, 4)) 
			# fig =plt.figure(figsize=(6.8,4))
			fig =plt.figure(figsize =(5,3.5), tight_layout=True)#figsize =(5.9,3.6) sq = (4,3.6)  lar = (3, 2.2) nar = (2.2,2.4) mlar =(3.8,2.8)
			sq = '_thesis'
			ax0 =fig.subplots()
			ax0.spines["top"].set_visible(False)
			ax0.spines["right"].set_visible(False)
			plt.grid(True, linestyle= ':')
			ax0.set_axisbelow(True)

			# graph_type = '_bar'
			# graph_name = 'v4_RPKIinvalid_perDP'
			# # graph_name = 'v4_invalidASN_perDP'
			# ind = [x for x, _ in enumerate(dp_asns)]
			# # plt.bar(ind, v4_unknown, width=0.8,label="v4_unknown", bottom = v4_valid+v4_invalidASN+v4_invalidLength)
			# plt.bar(ind, v4_invalidASN, width=0.8, label="v4_invalidASN", bottom=v4_invalidLength )
			# plt.bar(ind, v4_invalidLength, width=0.8, label="v4_invalidLength") #bottom=v4_valid
			# # plt.bar(ind, v4_valid, width=0.8, label="v4_valid")
			
			# # rotate axis labels
			# plt.xticks(ind, dp_asns)
			# plt.setp(plt.gca().get_xticklabels(), rotation=90)
			# # ax0.set(ylabel = '# Invalid ASN Prefix Origin pairs', xlabel='RV2 Direct Peer ASN')
			# # ax0.set(ylabel = '# Invalid Length Prefix Origin pairs', xlabel='RV2 Direct Peer ASN')
			# plt.ylabel ( '# Prefix Origin pairs')
			# plt. xlabel('RV2 Direct Peer ASN')
			# plt.legend()
			# axs[1].bar(dp_asns, v4_invalidLength, label="v4_invalidLength")
			# # rotate axis labels
			# plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

			graph_type = '_scat'
			graph_name = ipv+'_RPKIinvalid_POcount'
			rpki_invalids = np.zeros(len(data_matrix))
			pos = np.zeros(len(data_matrix))
			ff_cut = 0
			ROV_cut = 0
			ylim =  1000000
			xlim = 8000
			if ipv == 'v4':
				rpki_invalids = v4_invalidLength+v4_invalidASN
				pos = v4_pos
				ff_cut = v4_ff_cut
				ROV_cut = v4ROV_cut
			else:
				rpki_invalids = v6_invalidLength+v6_invalidASN
				pos = v6_pos
				ff_cut = v6_ff_cut
				ROV_cut = v6ROV_cut
				ylim =  100000
				xlim = 1400

			#write to csv
			filename = "RPKIFilteringWebpage/RPKIinvalidFiles/RPKIinvalid_" + date + "_" + ipv + ".csv"
			with open(filename, 'w') as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow(['RPKI filtering threshold', ROV_cut])
				writer.writerow(['Full feeder threshold', ff_cut])
				writer.writerow(['rpki_invalids', 'pos', 'asn'])
				for i in range(len(rpki_invalids)):
					writer.writerow([rpki_invalids[i], pos[i], dp_asns[i]])

			print ("data written to ROVoverTime.csv")

if __name__ == '__main__':
	main()

