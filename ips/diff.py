import ips.patch
def diff(o,t):
	assert len(o)==len(t)
	for i in range(len(o)):
		if o[i]!=t[i]:
			yield i,t[i]

class BinDiff:
	def __init__(self,f1,f2):
		self.original = f1.read()
		self.modified = f2.read()
		self.differences = dict()
		self.do()

	def do(self):
		for loc,val in diff(self.original,self.modified):
			self.differences[loc]=val

	@property
	def records(self):
		ret = []
		for diff in self.differences:
			n = ips.patch.Modify()
			n.offset = diff
			n.size = 1
			n.data = [self.differences[diff]]
		return ret
