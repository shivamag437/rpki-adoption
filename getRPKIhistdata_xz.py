import sys
import time
import subprocess
from subprocess import Popen, PIPE

tas = ['arin', 'apnic', 'apnic-iana', 'apnic-ripe', 'apnic-arin', 'apnic-lacnic', 'apnic-afrinic', 'lacnic', 'afrinic', 'ripencc']

def main():
	start_time = time.time() 	
	# Initialization
	gt_file_path = '/home/ctestart8/'
	date = '20190816'
	if len(sys.argv) >1:
		date = sys.argv[1]
	# file_path = '/mdt/RPKI/histdata/'+ date+'/'
	file_path =  gt_file_path +'data/RPKI/'+ date+'/'
	year = date[:4]
	month = date[4:6]
	day = date[6:]
	Popen("mkdir " +file_path, shell=True, stdin=PIPE)
	for ta in tas:
		link = "https://ftp.ripe.net/rpki/"+ta+".tal/"+year+"/"+month+"/"+day+"/roas.csv.xz"
		file_name = file_path+date+'_'+ta+'_roas.csv.xz'
		subprocess.call(["wget","-O", file_name, link])
	print ("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
	main()
