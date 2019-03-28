import struct

class Buff():
	def __init__(self,client):
		self.Buffer=b''
		self.BufferO=-1
		self.BufferWrite=[]
		self.BufferWriteT=[]
		self.client=client
		self.string_size=0
	def read(self,size):
		self.Buffer=b''
		while(self.Buffer==b'' and len(self.Buffer)<size and self.client.connected==True):
			self.Buffer+=self.client.connection.recv(size)

	def clearbuffer(self):
		self.BufferWrite.clear()
		self.BufferWriteT.clear()
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
			self.read(1)
			if self.Buffer!=b'\x00':
				p=struct.unpack('!s', self.Buffer)[0].decode("utf-8")
				s+=p
				c+=1
		return str(s)
	def readbyte(self):
		self.read(1)
		Buffer2=self.Buffer
		self.Buffer=self.Buffer[1:]
		return struct.unpack('!B', Buffer2[:1])[0]
	def readbit(self):
		Buffer2=self.Buffer
		self.Buffer=self.Buffer[1:]
		return struct.unpack('?', Buffer2[:1])[0]
	def readshort(self):
		self.read(2)
		return struct.unpack('!h', self.Buffer)[0]
	def readushort(self):
		self.read(2)
		return struct.unpack('!H', Buffer[:2])[0]
	def readint(self):
		Buffer2=self.Buffer
		self.Buffer=self.Buffer[4:]
		return struct.unpack('!i', Buffer2[:4])[0]
	def readdouble(self):
		Buffer2=self.Buffer
		self.Buffer=self.Buffer[8:]
		return struct.unpack('!d', Buffer2[:8])[0]
	def readfloat(self):
		Buffer2=self.Buffer
		self.Buffer=self.Buffer[4:]
		return struct.unpack('!f', Buffer2[:4])[0]
