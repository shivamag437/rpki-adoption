import time
import sys
from collections import defaultdict
from subprocess import Popen, PIPE

def readGzipFile(FileName):
	'''Returns list of lines from gzip file'''
	commandstring = "gzip -dc " + FileName
	input = Popen(['sh','-c',commandstring], stdout=PIPE,bufsize = 10485760)
	lines = input.stdout.readlines()
	input.stdout.close()
	return lines

def main ():
	# Initialization
	start_time = time.time() 
	date = '20190816'
	if len(sys.argv) >1:
		date =  sys.argv[1]
	file_path = '/home/ctestart8/code/rpki_adopt/PO_peercounts/'+date+ '/'
	file_name = file_path+date+'.prefix-origin-peercount-dplist-rpki_cleaned.gz'

	dp_viu = defaultdict(lambda: defaultdict(set))
	lines = readGzipFile(file_name)
	print ('POs: %d'%len(lines[1:]))

	for i,line in enumerate(lines[1:]):
		dl = line.decode('UTF-8')
		po = '|'.join(dl.split('|')[:2])
		rpki_status = dl.split('|')[3]
		dp_list = dl.strip('\n').split('|')[-1].split(',')
		for dp in dp_list:
			dp_viu[dp][rpki_status].add(po)
		if i%100000 ==0:
			print (i)
	print ('Direct peers: %d'%len(dp_viu))
	output_file = '/home/ctestart8/code/rpki_adopt/RPKIvalidity/'+date+'.dp_POrpkicounts_cleaned'
	with open(output_file, 'w') as outfile:
		outfile.write('# format: direct_peer|v4_valid|v4_invalidLength|v4_invalidASN|v4_unknown|v6_valid|v6_invalidLength|v6_invalidASN|v6_unknown\n')
		for dp in dp_viu:
			outfile.write(str(dp)+'|'+str(len(dp_viu[dp]["v4_valid"]))+'|'+str(len(dp_viu[dp]["v4_invalidLength"]))+'|'+str(len(dp_viu[dp]["v4_invalidASN"]))+'|'+str(len(dp_viu[dp]["v4_unknown"]))+'|'+str(len(dp_viu[dp]["v6_valid"]))+'|'+str(len(dp_viu[dp]["v6_invalidLength"]))+'|'+str(len(dp_viu[dp]["v6_invalidASN"]))+'|'+str(len(dp_viu[dp]["v6_unknown"]))+'\n')
	print ('Wrote '+ output_file)
	print ("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
	main()