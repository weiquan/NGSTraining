import itertools

MAX_INT = 100000
table_leftNt = {'A':'$', 'C':'A', 'G':'C', 'T':'G'}
table_rightNt = {'A':'C', 'C':'G', 'G':'T', '$':'A'}
class FMIdx():
	def __init__(self, string=''):
		self.string = string
		self.sa = None
		self.bwt = None
		self.occ = None
		self.count = None
	def buildIdx(self):
		self.buildSA()
		self.buildBwt()
		self.buildAux()
	def buildSA(self):
		self.sa = [i for i in xrange(len(self.string))]
		self.sa.sort(key=lambda x:self.string[x:])
	def buildBwt(self):
		if self.sa == None: self.buildSA()
		bwt = [self.string[i-1] for i in self.sa]
		self.bwt = ''.join(bwt)
	def buildAux(self):
		self.occ = FMIdx.buildOcc(self.bwt)#occ[i][c] denotes number of c in bwt[:i] 
		self.count = FMIdx.buildCount(self.bwt)
		self.primary = FMIdx.getPrimary(self.bwt) 
	def backward_search(self, p):
		#print self.count
		i = len(p)-1
		l = 0
		r = len(self.bwt)
		while l < r and i >=0:
			c = p[i]
			l = self.count[c] + self.occ[l][c]
			r = self.count[c] + self.occ[r][c]
			i -= 1
		return l, r
	def forward_search(self, p):
		#print self.count
		i = 0
		l = 0
		r = len(self.bwt)
		while l < r and i < len(p):
			c = p[i]
			l = self.count[c] + self.occ[l][c]
			r = self.count[c] + self.occ[r][c]
			i += 1
		return l, r
	def repeat_max_len(self, p):
		#print self.count
		i = 0
		l = 0
		r = len(self.bwt)
		while r-l >=2 and i < len(p):
			c = p[i]
			l = self.count[c] + self.occ[l][c]
			r = self.count[c] + self.occ[r][c]
			i += 1
		return i-1
	def printIdx(self):
		for i in xrange(len(self.bwt)):
			print self.bwt[i], self.occ[i], self.sa[i]
	@staticmethod
	def getPrimary(bwt):
		return bwt.find('$')
	@staticmethod
 	def buildOcc(bwt):
		occ=[ {'A':0, 'C':0, 'G':0, 'T':0, '$':0} for i in xrange(len(bwt)+1)]
		for dic, c in itertools.izip(occ, bwt):
			dic[c] =1

		for i in xrange(1, len(occ)):
			for c in ['A', 'C', 'G', 'T', '$']:
				occ[i][c] += occ[i-1][c]
		for i in xrange(len(occ)-1, 0, -1):
			occ[i] = occ[i-1]
		occ[0] = {'A':0, 'C':0, 'G':0, 'T':0, '$':0}
		return occ
	@staticmethod
	def buildCount(bwt):
		count = {}
		ntList = ['$', 'A', 'C', 'G', 'T']
		for c in ntList:
			count[c] = bwt.count(c)
		for i, c in enumerate(ntList[1:]):
			count[ntList[i+1]] += count[ntList[i+1-1]] 

		for i in xrange(len(ntList)-1, 0, -1):
			count[ntList[i]] = count[ntList[i-1]]
		count['$'] = 0
		#print count
		return count 	
	@staticmethod
	def inverseBwt(bwt):
		i = FMIdx.getPrimary(bwt)
		C = FMIdx.buildCount(bwt)
		Occ = FMIdx.buildOcc(bwt)
		string = ''
		while len(string) != len(bwt):
			#print i, bwt[i]
			c = bwt[i]
			string += c
			i = C[c] + Occ[i][c]
		return string[::-1] 

def test_bw_search():
	seq = 'ACAGGATAGATCCAT$'
	pattern = 'AT'
	ans = set([5, 9, 13])
	

	idx = FMIdx(seq)
	idx.buildIdx()
	l, r = idx.backward_search(pattern)
	
	result = set([idx.sa[x] for x in xrange(l, r)])
	#print ans, result
	if ans == result:
		print 'pass test_bw_search'
	return
def test_fw_search():
	seq = 'ACAGGATAGATCCAT$'
	pattern = 'AT'
	ans = set([5, 9, 13])
	

	idx = FMIdx(seq[::-1])
	idx.buildIdx()
	l, r = idx.forward_search(pattern)
	
	result = set([len(seq)-idx.sa[x]-len(pattern) for x in xrange(l, r)])
	print ans, result
	if ans == result:
		print 'pass test_fw_search'
	return
def test_repeat_max_len ():
	seq = 'ACAGGATAGATCCAT$'
	pattern = 'ACAG'
	

	idx = FMIdx(seq[::-1])
	idx.buildIdx()
#	l, r = idx.forward_search(pattern)
#	result = set([len(seq)-idx.sa[x]-len(pattern) for x in xrange(l, r)])
#	print result

	l = idx.repeat_max_len(pattern)
	print l		
	return


def main():
	fp = open('rosalind_mrep.txt','r')
	seq = fp.readline().strip()
	#string = FMIdx.inverseBwt(bwt)
	#print string
	seq += '$'
	idx = FMIdx(seq[::-1])
	idx.buildIdx()
	#idx.printIdx()
	repeatLen = 20
	#print idx.match_len('AA')
	for i in xrange(len(seq)):
		l = idx.repeat_max_len(seq[i:-1])
		#print l
		if l >= repeatLen:
			#print l 
			print seq[i:i+l]

		#print l, seq1[i:]
	fp.close()
if __name__ == '__main__':
	main()
	#test_bw_search()
	#test_fw_search()
	#test_repeat_max_len()