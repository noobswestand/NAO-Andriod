import struct

class Buff():
	def __init__(self,client):
		self.Buffer=b''
		self.BufferO=-1
		self.BufferWrite=[]
		self.BufferWriteT=[]
		self.client=client
		self.string_size=0
	def read(self,size,clear=False):
		if clear==True:
			self.Buffer=b''
		while((self.Buffer==b'' or len(self.Buffer)<size) and self.client.connected==True):
			self.Buffer+=self.client.connection.recv(size)

	def clearbuffer(self):
		self.BufferWrite=[]
		self.BufferWriteT=[]
	def writebit(self,b):
		self.BufferWrite.append(bool(b))
		self.BufferWriteT.append("?")
	def writebyte(self,b):
		self.BufferWrite.append(int(b))
		self.BufferWriteT.append("B")
	def writestring(self,s):
		self.BufferWriteT.append("{}s".format(len(s)+1))
		self.BufferWrite.append(s.encode("utf-8")+b"\x00")
	def writeint(self,b):
		self.BufferWrite.append(int(b))
		self.BufferWriteT.append("i")
	def writedouble(self,b):
		self.BufferWrite.append(float(b))
		self.BufferWriteT.append("d")
	def writefloat(self,b):
		self.BufferWrite.append(float(b))
		self.BufferWriteT.append("f")
	def writeshort(self,b):
		self.BufferWrite.append(int(b))
		self.BufferWriteT.append("h")
	def writeushort(self,b):
		self.BufferWrite.append(int(b))
		self.BufferWriteT.append("H")
	def readstring(self):
		c=0
		s=""
		
		while(c<self.string_size):
			self.read(1,True)
			if self.Buffer!=b'\x00':
				p=struct.unpack('!s', self.Buffer)[0].decode("utf-8")
				s+=p
				c+=1
		self.Buffer=b''
		return str(s)
	def readbyte(self):
		self.read(1)
		self.Buffer2=self.Buffer
		self.Buffer=self.Buffer[2:]
		return struct.unpack('!B', self.Buffer2[:1])[0]
	def readshort(self):
		self.read(2)
		self.Buffer2=self.Buffer
		self.Buffer=self.Buffer[2:]
		return struct.unpack('!h', self.Buffer2[:2])[0]
	def readdouble(self):
		self.read(8)
		Buffer2=self.Buffer
		self.Buffer=self.Buffer[8:]
		return struct.unpack('!d', Buffer2[:8])[0]