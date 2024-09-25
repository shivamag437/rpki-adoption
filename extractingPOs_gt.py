import sys
import gzip
import time
from os import listdir
from bitsets import bitset
from collections import defaultdict
from subprocess import Popen, PIPE

#bitset configs:
MAX_DIRECT_PEERS = 3000

highest_peer_id_used = 0
peer_to_id = {}
id_to_peer = {}

peer_id_list = range(MAX_DIRECT_PEERS) ###change number to MAXIMUM number of expected direct peers with some additional leeway.

direct_peer_set = bitset("peers",tuple(peer_id_list))

class DirectPeerSet:

	def __init__(self):
		self.peer_bitset = direct_peer_set()

	def addPeer(self, peer_string):
		global highest_peer_id_used
		global peer_to_id
		global id_to_peer
		global direct_peer_set
		try:
			new_peer_id = peer_to_id[peer_string]
		except:
			if highest_peer_id_used >= MAX_DIRECT_PEERS:
				print ("increase max direct peers")
				raise

			peer_to_id[peer_string] = highest_peer_id_used
			id_to_peer[highest_peer_id_used] = peer_string
			new_peer_id = peer_to_id[peer_string]
			highest_peer_id_used += 1

		self.peer_bitset = self.peer_bitset.union(direct_peer_set((new_peer_id,)))

	def getPeers(self):
		peer_ids = list(self.peer_bitset)
		#print (str(sys.getsizeof(self.peer_bitset)))
		return [id_to_peer[x] for x in peer_ids] #map(id_to_peer,peer_ids)

def openGzipFile(FileName):
	'''Returns input.stdout from  gzip file'''
	commandstring = "gzip -dc " + FileName
	input = Popen(['sh','-c',commandstring], stdout=PIPE,bufsize = 10485760)
	return input.stdout

def extractPath (BGPline):
	''' Returns the AS path of an announcement from a line of a RIB bgp dump in ascii'''
	try:
		pathstr = BGPline.split('|')[6]
	except IndexError as ie:
		print (BGPline)
	else:
		if len(pathstr) == 0:
			print ('Bad BGP record')
			print (BGPline)
		elif '{' not in pathstr:
			return [int(x) for x in pathstr.split(' ')]
	return []

def extractPfx (BGPline):
	'''Returns the prefix of an announcement from a line of a RIB bgp dump in ascii'''
	return BGPline.split('|')[5]

def extractDP (BGPline):
	'''Returns the direct peer (DP) of an announcement from a line of a RIB bgp dump in ascii'''
	return BGPline.split('|')[4]


def main ():
	# Initialization
	start_time = time.time() 
	date = '20190816'
	# rib_time = '2000'
	# collector = 'rv2'
	if len(sys.argv) >1:
		date = sys.argv[1]

	#Loading BGP data
	gt_file_path = '/home/ctestart8/'
	bgp_files_path = gt_file_path +'data/BGPstream/'+ date +'/'
	bgp_files = [f for f in listdir(bgp_files_path) if '_ribs_' in f ]
	print ('BGP files: %d'%len(bgp_files))
	# bgp_files.sort()
	# print (bgp_files)
	file_path =  gt_file_path + 'code/rpki_adopt/PO_peercounts/'+date+ '/'
	Popen("mkdir " +file_path, shell=True, stdin=PIPE)
	time.sleep(1)
	# file_path = file_path +'collector_data/'
	# Popen("mkdir " +file_path, shell=True, stdin=PIPE)
	print (file_path)
	po_dp = defaultdict(DirectPeerSet)
	set_count = 0
	for bgpFile in bgp_files:
		collector = bgpFile.split('_')[0]
		print (collector +' '+ date)
		of = openGzipFile(bgp_files_path+bgpFile)
		# ipv4_count  = 0
		# ipv6_count = 0
		for line in of:
			path = extractPath (line.decode('utf8'))
			if len(path) > 0:
				# No set in the path
				dp = extractDP(line.decode('utf8'))
				dp_key = dp +':'+collector
				origin = path[-1]
				pfx = extractPfx(line.decode('utf8'))
				po_key = pfx+'|'+str(origin)
				po_dp [po_key].addPeer(dp_key)
			else:
				#set in path
				set_count += 1
	print ('Set count %d, PO count %d'%(set_count, len(po_dp)))
	# output_file = file_path +collector+'_'+date+'_PO_dps'
	output_file = file_path +date+'_allcollectors_PO_dps'
	with open(output_file, 'w') as outfile:
		outfile.write('# format: prefix|origin|dp_count|dp_list\n')
		# outfile.write('# format: prefix|origin|dp_count\n')
		for po in po_dp:
			dps = [dp_col.split(':')[0] for dp_col in po_dp[po].getPeers()]
			outfile.write(po+'|'+str(len(dps))+'|'+','.join(set(dps))+'\n')
			# outfile.write(po+'|'+str(len(po_dp[po]))+'\n')
	print ('Wrote '+ output_file)
	comp = Popen(['gzip', output_file],stdin=PIPE, stdout=PIPE, stderr=PIPE)
	print ('Compressed ' + output_file)
	print ("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
	main()
