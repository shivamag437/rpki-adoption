import time
import json
import sys
from os import listdir
from subprocess import Popen, PIPE

def readFile(fileName):
	'''Returns list of lines in file'''
	with open(fileName,'r') as inputFile:
		lines=inputFile.readlines()
		return lines

def main():
	# Initialization
	gt_file_path = '/home/ctestart8/'
	start_time = time.time() 
	date = '20210701'
	if len(sys.argv) >1:
		date = sys.argv[1]
	file_path =  gt_file_path +'data/RPKI/'

	# ROAS info from TAs
	file_list = [f for f in listdir(file_path+date+ '/') if date in f]
	print (f'Files: {len(file_list)}')
	je = {"roas":[]}

	for file in file_list:
		# filename convention: date_ta_roas.csv (eg. 20230501_afrinic_roas.csv)
		trust_anchor = file.split('_')[1]
		lines = readFile(file_path +date+ '/'+file)
		for line in lines[1:]:
			# Expected file format : URI,ASN,IP Prefix,Max Length,Not Before,Not After
			uri,asn,pfx,maxlen,notbefore,notafter = line.split(',')
			if len(maxlen)==0:
				maxlen = pfx.split('/')[1]
			# print line
			try:
				roa_je = {"asn": asn, "prefix": pfx, "maxLength": int(maxlen), "ta": trust_anchor}
			except Exception as e:
				print (maxlen)
				print (e)
			else:
				je["roas"].append(roa_je)
	l = len (je["roas"])
	print (f"ROAs: {l}")
	# print (je["roas"])

	# Saving data in the same format as rpki-validator json file
	dump_file = file_path + date+ '.validatedroas.json'
	with open(dump_file, 'w') as f:
		json.dump(je, f,  indent=4, sort_keys = True)
	print (f"Wrote {dump_file}")
	comp = Popen(['gzip', dump_file],stdin=PIPE, stdout=PIPE, stderr=PIPE)
	print (f'Compressed {dump_file}')
	print (f"--- {(time.time() - start_time)} seconds ---" )


if __name__ == '__main__':
	main()