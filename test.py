import ips,ips.patch,io,linebuffer
from colorama import init, deinit, Fore

TEST_COUNT = 13
TEST_NUM = 0

lb = linebuffer.LineBuffer("Testing [0/13]"+("."*20))

init()

def testcond(name,value,expected,errormsg="Value different than expected ({!s})"):
	global TEST_NUM
	TEST_NUM+=1
	lb.set(linebuffer.pad("{} [{!s}/{!s}]".format(name,TEST_NUM,TEST_COUNT),50,"."))
	lb.draw()
	lb.draw()
	try:
		assert value==expected
	except:
		print(Fore.RED+"FAIL"+Fore.RESET)
		print(errormsg.format(value))
		lb.set("")
		lb.pad = 0
		return False
	print(Fore.GREEN+"PASS"+Fore.RESET)
	return True

# create fake data
f = io.BytesIO()
assert f.write(bytearray([0xFF,0xDD,0xBB,0x00,0x00,0xFF,0xFF,0x00,0xFF,0xBB,0xDD,0x00,0x10]+[0x00 for i in range(0x10)]))==(8+5+16),"should write 8 bytes to fake file"
f.seek(0)

# RLE encoded modifiers
r = ips.patch.Modify.fromPatchFile(f)
testcond("Offset of RLE",r.offset,0xFFDDBB,"Offset parsed incorrectly ({:03X})")
testcond("Size of RLE",r.size,0xFFFF,"Size parsed incorrectly ({:02X})")
testcond("RLE parsed correctly (len(data)==size)",len(r.data),0xFFFF,"RLE parsed incorrectly ({:02X})")
testcond("All data == 0",all(x==0 for x in r.data),True,"Some data non-zero")

# Normal modifiers
m = ips.patch.Modify.fromPatchFile(f)
testcond("Offset of manual",m.offset,0xFFBBDD,"Offset parsed incorrectly ({:03X})")
testcond("Size of manual",m.size,0x10,"Size parsed incorrectly ({:02X})")
testcond("Data parsed correctly (len(data)==size)",len(m.data),m.size,"RLE parsed incorrectly ({:02X})")
testcond("All data == 0",all(x==0 for x in m.data),True,"Some data non-zero")

# Reading a file
with open("test.ips","rb") as f:
	d = ips.PatchFile.fromPatchFile(f)
	assert type(d.records[0])==ips.patch.RLEModify,"Record did not dissolve correctly."
	r = d.records[0]
	assert r.offset==0xFFDDBB,"Offset parsed incorrectly ({:03X})".format(r.offset)
	assert r.size==0xFFFF,"Size parsed incorrectly ({:02X})".format(r.size)
	assert len(r.data)==0xFFFF,"Data parsed incorrectly ({:02X})".format(len(r.data))
	assert all(x==0 for x in r.data),"Data set incorrectly"
