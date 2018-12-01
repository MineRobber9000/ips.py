import ips,ips.patch,io,linebuffer
from colorama import init, deinit, Fore
from sys import exit

TEST_COUNT = 18
TEST_NUM = 0
PASSED = 0

lb = linebuffer.LineBuffer("Testing [0/13]"+("."*20))

init()

def testcond(name,value,expected,errormsg="Value different than expected ({!s})"):
	global TEST_NUM,PASSED
	TEST_NUM+=1
	lb.set(linebuffer.pad("[{:>2}/{!s}] {}".format(TEST_NUM,TEST_COUNT,name),50,"."))
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
	PASSED+=1
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
	testcond("RLE dissolves to ips.patch.RLEModify",type(d.records[0]),ips.patch.RLEModify,"Record did not dissolve correctly. ({!s})")
	r = d.records[0]
	testcond("Offset parsed",r.offset,0xFFDDBB,"Offset parsed incorrectly ({:03X})")
	testcond("Size parsed",r.size,0xFFFF,"Size parsed incorrectly ({:02X})")
	testcond("Data parsed",len(r.data),0xFFFF,"Data parsed incorrectly ({:02X})")
	testcond("All data == 0",all(x==0 for x in r.data),True,"Data set incorrectly")

# Applying a patch
f = io.BytesIO()
f.write(bytearray(b"PATCH"))
f.write(bytearray([0x00,0x00,0x00,0x00,0x01,0xFF]))
f.write(bytearray(b"EOF"))
f.seek(0)
d = ips.PatchFile.fromPatchFile(f)
testcond("Record parsed",len(d.records),1)
r = d.records[0]
testcond("Offset parsed",r.offset,0)
testcond("Size parsed",r.size,1)
testcond("Data parsed",r.data,[0xFF])
testcond("Applies correctly",d.apply([0x00,0xc3,0x50,0x01]),[0xff,0xc3,0x50,0x01])

print("{:.0%} of {!s} tests passed.".format(PASSED/TEST_COUNT,TEST_COUNT))
if PASSED<TEST_COUNT:
	exit(1)
exit(0)
