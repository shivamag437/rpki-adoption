import sys
from subprocess import Popen, PIPE

def readGzipFile(FileName):
	'''Returns list of lines from gzip file'''
	commandstring = "gzip -dc " + FileName
	input = Popen(['sh','-c',commandstring], stdout=PIPE,bufsize = 10485760)
	lines = input.stdout.readlines()
	input.stdout.close()
	return lines

def readFile(fileName):
	'''Returns list of lines in file'''
	with open(fileName,'r') as inputFile:
		lines=inputFile.readlines()
		return lines

def main():
	# Initialization
	gt_file_path = '/home/ctestart8/'
	date = '20190816'
	ta='' #placeholder for selective trust anchor inclusion analysis
	if len(sys.argv) >1:
		date = sys.argv[1]
		if len(sys.argv) >2:
			ta = '-'+sys.argv[2]
	bogons = [line.strip('\n') for line in readFile( gt_file_path + 'code/rpki_adopt/iana-bogons.txt')]
	file_path =  gt_file_path + 'code/rpki_adopt/PO_peercounts/'+date+ '/'
	file_name = file_path+date+'.prefix-origin-peercount-dplist-rpki'+ta+'.gz'
	lines = readGzipFile(file_name)
	print ('Initial POs: %d'%(len(lines)-1))

	# output_file = file_path+date+'.prefix-origin-peercount-dplist_full_feeders-rpki_cleaned'
	output_file = file_path+date+'.prefix-origin-peercount-dplist-rpki'+ta+'_cleaned'
	v4_count = 0
	v6_count = 0
	with open (output_file, 'wb') as fout:
		fout.write(lines[0])
		for i, line in enumerate(lines[1:]):
			# Cleaning bogons
			pfx = line.decode('UTF-8').split('|')[0]
			if pfx not in bogons:
				# Cleaning long prefixes (/25-/32 for IPv4, /64-/128 for IPv6)
				pfxlen = int(pfx.split('/')[1])
				if ':' not in pfx:
					#IPv4 prefix
					if 8 <= pfxlen <= 24:
						fout.write(line)
						v4_count += 1
				else:
					#IPv6 prefix
					if 8 <= pfxlen <= 64:
						fout.write(line)
						v6_count += 1
			if i%100000==0:
				print (i)
	print ('v4 POs: %d, v6 POs: %d' %(v4_count, v6_count))
	print ('Wrote '+output_file)
	comp = Popen(['gzip', output_file],stdin=PIPE, stdout=PIPE, stderr=PIPE)
	print ('Compressed ' + output_file)
	

if __name__ == '__main__':
	main()