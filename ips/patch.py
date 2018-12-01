def combine(l,r=0,s=8):
	r = r<<s
	r += l.pop(0)
	if len(l)==0:
		return r
	else:
		return combine(l,r,s)

class Modify:
	def __init__(self,offset=0,size=0,data=[]):
		self.offset = offset
		self.size = size
		self.data = data

	@classmethod
	def fromPatchFile(cls,f):
		t = f.read(3)
		if t==b'EOF':
			return False
		o = cls(0,0,[]) # supplying the default values fixed an error
		d = bytearray(t+f.read(2))
		o.offset = combine(d[:3])
		o.size = combine(d[3:5])
		if o.size==0:
			r = RLEModify()
			d += f.read(3)
			return r.use(d)
		for i in range(o.size):
			o.data.append(f.read(1)[0])
		return o

class RLEModify(Modify):
	def __init__(self,offset=0,size=0,data=[]):
		super(RLEModify,self).__init__(offset,size,data)

	def use(self,d):
		self.offset = combine(d[:3])
		self.size = combine(d[5:7])
		self.data = [d[7]]*self.size
		return self

class PatchFile:
	def __init__(self):
		self.records = []
	@classmethod
	def fromPatchFile(cls,f):
		assert f.read(5)==b'PATCH',"Header must be 5 bytes reading 'PATCH' (no terminator)"
		self = cls()
		o = Modify.fromPatchFile(f)
		while o:
			self.records.append(o)
			o = Modify.fromPatchFile(f)
		return self
	def apply(self,data):
		for record in self.records:
			data[record.offset:record.offset+record.size]=record.data
		return data
