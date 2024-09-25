import pytricia
import json
import gzip
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

def loadGzipJson (fn):
	''' Returns a json element loaded from fn assumed .gz with 1 json element'''
	with gzip.open(fn, 'rb') as f:
		d = json.loads(f.read().decode('ascii'))
	return d

def getCandidateROAs(pyt, pfx):
	'''Returns a list of jsonroas obtained from the pyt tree'''
	candidate_roas = []
	candidate_roas.extend(pyt[pfx])
	search_pfx = pyt.get_key(pfx)
	while(pyt.parent(search_pfx) is not None):
		candidate_roas.extend(pyt[pyt.parent(search_pfx)])
		search_pfx = pyt.parent(search_pfx)
	return candidate_roas

def main():
	# Initialization
	gt_file_path = '/home/ctestart8/'
	date = '20180901'
	# roas_time = '1335'
	ff = '' #'_full_feeders' #
	if len(sys.argv) >1:
		date =  sys.argv[1]
	file_path =  gt_file_path + 'code/rpki_adopt/PO_peercounts/'+date+ '/'
	file_name = file_path+date+'_allcollectors_PO_dps.gz'

	#Loading RPKI validated ROAs
	# json_file = '/mdt/RPKI/rpki-validator/%s.validatedroas.json.gz'%(date)
	json_file =  gt_file_path + 'data/RPKI/%s.validatedroas.json.gz'%(date)
	roas_list = loadGzipJson(json_file)['roas']
	v4roas = [roa for roa in roas_list if ':' not in roa['prefix']]
	v6roas = [roa for roa in roas_list if ':' in roa['prefix']]
	print ('ROAs: %d, (v4: %d, v6:%d)'%(len (roas_list), len(v4roas), len(v6roas)))
	# IPv4 ROAs
	pyt = pytricia.PyTricia()
	for roa in v4roas:
		if pyt.has_key(str(roa['prefix'])):
			pyt[str(roa['prefix'])].append(roa)
		else:
			pyt[str(roa['prefix'])] = [roa]
	# IPv6 ROAs
	pyt6 = pytricia.PyTricia(128)
	for roa in v6roas:
		if pyt6.has_key(str(roa['prefix'])):
			pyt6[str(roa['prefix'])].append(roa)
		else:
			pyt6[str(roa['prefix'])] = [roa]
	print ('v4 Tree length: %d, v6 tree length: %d'%(len(pyt), len(pyt6)))

	# Checking PO RPKI validity
	lines = readGzipFile(file_name)
	print ('POs: %d'%len(lines[1:]))
	rpki_status = {}
	ipv4_count  = 0
	ipv6_count = 0
	# tas_count = 0
	for i,line in enumerate(lines [1:]):
		pfx, origin, peer_count, dplist = line.decode('UTF-8').strip('\n').split('|')
		# pfx, origin, peer_count = line.strip('\n').split('|')
		pfx_len = int(pfx.split('/')[1])
		if ':' not in pfx:
			# IPv4 pfx
			ipv4_count += 1
			if pfx in pyt:
				candidate_roas = getCandidateROAs(pyt,pfx)
				candidate_origins = [int(roa['asn'].split('AS')[1]) for roa in candidate_roas]
				tas = set([roa['ta'] for roa in candidate_roas])
				if int(origin) in candidate_origins:
					# ASN match
					invalid_lenght = True
					for roa in candidate_roas:
						# print ('AS'+str(origin)+', '+str(roa['asn']))
						if 'AS'+str(origin) == str(roa['asn']):
							#selecting ROA with matching ASN
							# print (' AS MATCH')
							if pfx_len <= int(roa['maxLength']):
								# Pfx, ASN and max len match ---> RPKI valid
								rpki_status[line] = 'v4_valid'
								invalid_lenght = False
								# print ('VALID')
					if invalid_lenght :
						# No maxLen match --> RPKI invalid
						rpki_status[line] = 'v4_invalidLength'
				else:
					# NO ASN match --> RPKI invalid ASN
					rpki_status[line] = 'v4_invalidASN'
			else:
				#pfx not in pyt --> RPKI unknown
				rpki_status[line] = 'v4_unknown'
		else:
			# IPv6 pfx
			ipv6_count += 1
			if pfx in pyt6:
				candidate_roas = getCandidateROAs(pyt6,pfx)
				candidate_origins = [int(roa['asn'].split('AS')[1]) for roa in candidate_roas]
				tas = set([roa['ta'] for roa in candidate_roas])
				if int(origin) in candidate_origins:
					# ASN match
					invalid_lenght = True
					for roa in candidate_roas:
						if 'AS'+str(origin) == str(roa['asn']):
							#selecting ROA with matching ASN
							if pfx_len <= int(roa['maxLength']):
								# Pfx, ASN and max len match ---> RPKI valid
								rpki_status[line] = 'v6_valid'
								invalid_lenght = False
					if invalid_lenght :
						# No maxLen match --> RPKI invalid
						rpki_status[line] = 'v6_invalidLength'
				else:
					# NO ASN match --> RPKI invalid ASN
					rpki_status[line] = 'v6_invalidASN'
			else:
				#pfx not in pyt --> RPKI unknown
				rpki_status[line] = 'v6_unknown'
		if i%100000 ==0:
			print (i)
	
	output_file = file_path+date+'.prefix-origin-peercount-dplist'+ff+'-rpki'
	with open(output_file, 'w') as outfile:
		outfile.write('# format: prefix|origin|peer_count|rpki_status|dp_list'+ff+'\n')
		# outfile.write('# format: prefix|origin|peer_count'+ff+'|rpki_status'+'\n')
		for line in rpki_status:
			outfile.write('|'.join(line.decode('UTF-8').split('|')[:3])+'|'+rpki_status[line]+'|'+line.decode('UTF-8').split('|')[-1])
			# outfile.write(line.strip('\n') +'|'+rpki_status[line]+'\n')
	print ('Wrote '+ output_file)
	comp = Popen(['gzip', output_file],stdin=PIPE, stdout=PIPE, stderr=PIPE)
	print ('Compressed ' + output_file)

if __name__ == '__main__':
	main()