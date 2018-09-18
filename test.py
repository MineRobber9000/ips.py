import ips,ips.patch,io

# create fake data
f = io.BytesIO()
assert f.write(bytearray([0xFF,0xDD,0xBB,0x00,0x00,0xFF,0xFF,0x00,0xFF,0xBB,0xDD,0x00,0x10]+[0x00 for i in range(0x10)]))==(8+5+16),"should write 8 bytes to fake file"
f.seek(0)

# RLE encoded modifiers
r = ips.patch.Modify.fromPatchFile(f)
assert r.offset==0xFFDDBB,"Offset parsed incorrectly ({:03X})".format(r.offset)
assert r.size==0xFFFF,"Size parsed incorrectly ({:02X})".format(r.size)
assert len(r.data)==0xFFFF,"Data parsed incorrectly ({:02X})".format(len(r.data))
assert all(x==0 for x in r.data),"Data set incorrectly"

# Normal modifiers
m = ips.patch.Modify.fromPatchFile(f)
assert m.offset==0xFFBBDD,"Offset parsed incorrectly ({:03X})".format(m.offset)
assert m.size==0x10,"Size parsed incorrectly ({:02X})".format(m.size)
assert len(m.data)==0x10,"Data parsed incorrectly ({:02X})".format(len(m.data))
assert all(x==0 for x in m.data),"Data set incorrectly"

# Reading a file
with open("test.ips","rb") as f:
	d = ips.PatchFile.fromPatchFile(f)
	assert type(d.records[0])==ips.patch.RLEModify,"Record did not dissolve correctly."
	r = d.records[0]
	assert r.offset==0xFFDDBB,"Offset parsed incorrectly ({:03X})".format(r.offset)
	assert r.size==0xFFFF,"Size parsed incorrectly ({:02X})".format(r.size)
	assert len(r.data)==0xFFFF,"Data parsed incorrectly ({:02X})".format(len(r.data))
	assert all(x==0 for x in r.data),"Data set incorrectly"
