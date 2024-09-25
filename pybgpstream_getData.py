import time
import datetime
import gzip
import sys
from dateutil import parser
from subprocess import Popen, PIPE

import pybgpstream

collector_list=['route-views2', 'route-views3', 'route-views4', 'route-views6', 'route-views.eqix', 'route-views.isc', 'route-views.kixp', 'route-views.jinx', 'route-views.linx', 'route-views.telxatl', 'route-views.wide', 'route-views.sydney', 'route-views.saopaulo', 'route-views.nwax', 'route-views.perth', 'route-views.sg', 'route-views.sfmix', 'route-views.soxrs', 'route-views.chicago', 'route-views.napafrica', 'route-views.flix', 'route-views.chile', 'route-views.amsix', 'route-views.bdix', 'route-views.bknix', 'route-views.fortaleza', 'route-views.gixa', 'route-views.gorex', 'route-views.ny', 'route-views.peru', 'route-views.phoix', 'route-views.rio', 'route-views.uaeix', 'route-views5', 'route-views2.saopaulo', 'route-views.siex', 'route-views.mwix', 'rrc00', 'rrc01','rrc02','rrc03','rrc04','rrc05','rrc06','rrc07','rrc08','rrc09','rrc10','rrc11','rrc12','rrc13','rrc14', 'rrc15','rrc16','rrc18','rrc19','rrc20','rrc21', 'rrc22', 'rrc23', 'rrc24', 'rrc25', 'rrc26']
# new_collectors = ['route-views.bdix', 'route-views.bknix', 'route-views.fortaleza', 'route-views.gixa', 'route-views.gorex', 'route-views.ny', 'route-views.peru', 'route-views.phoix', 'route-views.rio', 'route-views.uaeix', 'route-views5', 'route-views2.saopaulo', 'route-views.siex', 'route-views.mwix']
# ripe_collectors = ['rrc00', 'rrc01','rrc03','rrc04','rrc05','rrc06','rrc07','rrc08','rrc09','rrc10','rrc11','rrc12','rrc13','rrc14', 'rrc15','rrc16','rrc18','rrc19','rrc20','rrc21', 'rrc22', 'rrc23', 'rrc24']


def getBGPStream(collector_name, startTS, endTS, recordType='rib'):
	'''Returns the started BGPStream and the BGPRecord of recordType('rib' or 'update') created filtering by collector_name and TS (timestamp) interval'''
	stream = pybgpstream.BGPStream(
		from_time=startTS, until_time=endTS,
		collectors=[collector_name],
		record_type="ribs",
    )
	return stream

def readGzipFile(FileName):
	'''Returns list of lines from gzip file'''
	commandstring = "gzip -dc " + FileName
	input = Popen(['sh','-c',commandstring], stdout=PIPE,bufsize = 10485760)
	lines = input.stdout.readlines()
	input.stdout.close()
	return lines

def writeGzipFile(file):
   output = Popen("gzip -c > " + file, shell=True, stdin=PIPE)
   return output.stdin

def saveData( file_name, collector_name, startTS, endTS, recordType='ribs', verbose=False):
	'''Writes elements data from BGPstrean in file_name in csv format'''
	f = writeGzipFile(file_name)#open(file_name, 'w')
	#Getting stream and record
	stream = getBGPStream(collector_name, startTS, endTS, recordType)
	#Initializing variables
	counter=0
	# Get records
	for rec in stream.records():
		# print ("There is a record")
		# Getting all elements of the record
		for elem in rec:
			#Get the type, time the element represents, of the BGPElem
			tp = elem.type
			tm = elem.time
			# utc_time = datetime.datetime.utcfromtimestamp(int(elem.time)).strftime('%Y-%m-%d %H:%M:%S')
			peer_address = elem.peer_address
			peer_asn = elem.peer_asn
			# collector_name = elem.collector
			pfx = ''
			as_path = ''
			next_hop = ''
			communities= ''
			if tp in 'RAW': #Rib Announcement Withdrawal
				# Get the prefix
				pfx = elem.fields["prefix"]
				if tp in 'RA':
					# Get the list of ASes in the AS path
					as_path = elem.fields['as-path']
					next_hop = elem.fields['next-hop']
					communities = ' '.join(elem.fields['communities'])
			# print((collector_name +'|'+ str(tm) +'|'+ tp +'|'+ peer_address +'|'+ str(peer_asn) +'|'+ pfx +'|'+ as_path +'|'+ next_hop +'|'+ communities +'\n'))
			f.write (str.encode(collector_name +'|'+ str(tm) +'|'+ tp +'|'+ peer_address +'|'+ str(peer_asn) +'|'+ pfx +'|'+ as_path +'|'+ next_hop +'|'+ communities +'\n'))
			counter +=1
			if verbose:
				if counter %1000000 == 0:
					print ('record %d' %counter)
	f.close()
	return counter

def main():
	start_time = time.time() 	
	# Initialization
	gt_file_path = '/home/ctestart8/'
	date = '20230601'
	rib_time = '1200' # 1600 GMT, BOSTON time = UTC - 4 
	if len(sys.argv) >1:
		date = sys.argv[1]
		if len(sys.argv) >2:
			rib_time = sys.argv[2]
	file_path =  gt_file_path + 'data/BGPstream/'+ date+'/'
	Popen("mkdir " +file_path, shell=True, stdin=PIPE)
	rib_date=date +' '+ rib_time 
	ribTS= int (time.mktime(datetime.datetime.strptime(rib_date, '%Y%m%d %H%M%S').timetuple()))
	print (ribTS)
	totalRecords = 0
	time.sleep(1)
	for collector in collector_list:
		print (collector)
		recordType = 'ribs'
		file_name = file_path+collector+ '_' + date + '_' + recordType +'_'+str(ribTS)+ '.gz'
		counter = saveData (file_name, collector,ribTS-100, ribTS+100, recordType, True)
		print ('Total records saved: '+str(counter))
		totalRecords += counter
	print ('All collectors Total: ' + str(totalRecords))
	print ("--- %s seconds ---" % (time.time() - start_time))

if __name__=='__main__':
    main()