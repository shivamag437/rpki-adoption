import datetime
import os

# plt.style.use('seaborn-paper') #seaborn ggplot

def readFile(fileName):
	'''Returns list of lines in file'''
	with open(fileName,'r') as inputFile:
		lines=inputFile.readlines()
	return lines


def main():
	# Data Files
	date_list=[ '20181201','20190103', '20190201', '20190209',   '20190301', '20190330',  '20190406','20190501', '20190601', '20190622', '20190701', '20190803', '20190901', '20191001','20191015', '20191030', '20191201', '20200101', '20200122','20200130' , '20200204', '20200303','20200320' ,'20200327' , '20200401', '20200415', '20200430', '20200606', '20200702', '20200805', '20200901', '20201001', '20201029', '20201130', '20201230', '20210130', '20210228', '20210330', '20210430', '20210530', '20210630', '20210730', '20210901', '20211001', '20211201', '20220101', '20220201', '20220301', '20220401', '20220501', '20220601', '20220701', '20220801', '20220901', '20221001', '20221101', '20221201', '20230101', '20230201', '20230301', '20230401', '20230501', '20230601' , '20230701', '20230801', '20230901', '20231001', '20231101', '20231201', '20240101', '20240201', '20240301'] # '20170401', '20170501', '20170601', '20170701', '20170801','20170901', '20171002', '20171101', '20171201', '20180101', '20180201', '20180301', '20180405', '20180501', '20180601', '20180701', '20180801', '20180901', '20181001', '20181101', '20191004','20191008','20191010', '20191023','20191025','20191027','20191029', '20200122',
	date_list=[]
	for filename in os.listdir('DirectPeerData'):
		if filename.endswith('.dp_POrpkicounts_cleaned'):
			date_list.append(filename.split('.')[0])
	ipvs = ['v4', 'v6']
	for ipv in ipvs:
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
			dataFile = 'DirectPeerData/'+date +'.dp_POrpkicounts_cleaned'
			data_matrix = [line.split('|') for line in readFile(dataFile)[1:]]
			max_pos = max([int(d[iASN])+int(d[iLen])+int(d[iVal])+int(d[iUnk]) for d in data_matrix])
			for d in data_matrix:
				pos = int(d[iASN])+int(d[iLen])+int(d[iVal])+int(d[iUnk])
				if int(d[0]) in asn_invalids and pos >= max_pos*0.75:
					asn_invalids[int(d[0])][date] = int(d[iASN])+int(d[iLen])
					asn_pos[int(d[0])][date] = pos

		ts_list = [datetime.datetime.strptime(date, "%Y%m%d")  for date in date_list]
		#sort ts_list and date_list
		combined = zip(ts_list, date_list)
		sorted_combined = sorted(combined, key=lambda x: x[0])
		ts_list, date_list = zip(*sorted_combined)

		
		# Save data
		# Transpose the file
		file_path = 'RPKIFilteringWebpage/Tier1ASes_IP'+ipv+'_RPKIinvalidsCount_transposed.csv'
		with open(file_path,'w') as fout:
			fout.write('date,'+','.join([str(asn)+'-'+asn_names[i] for i, asn in enumerate(asn_list)])+'\n')
			for date in date_list:
				invalids = [str(asn_invalids[asn][date]) if date in asn_invalids[asn] else 'NA' for asn in asn_list]
				fout.write(str(datetime.datetime.strptime(date, "%Y%m%d"))+','+','.join(invalids)+'\n')

		print ('Data saved in: '+file_path)

if __name__ == '__main__':
	main()
