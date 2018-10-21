def pad(s,l,c=" "):
	return (s+(c*l))[:l]

class LineBuffer:
	def __init__(self,s,l=None):
		if l is None:
			l = len(s)
		self.s = s
		self.l = l
		self.pad = 0
		self.draw()

	def set(self,s):
		self.s = s
		if len(self.s)>self.l:
			self.l = len(self.s)
		elif len(self.s)<self.l:
			self.pad = self.l-len(self.s)
			self.l = len(self.s)

	def get(self):
		return self.s

	def draw(self):
		end = ""
		if self.pad>0:
			end = pad(end,self.pad)
			self.pad = 0
		print("\r{}".format(self.s),end=end)
