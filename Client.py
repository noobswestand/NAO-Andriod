import threading,naoqi,select,Network,struct,time

class Client(threading.Thread):
	def __init__(self,connection,address,server,pid,ip):
		threading.Thread.__init__(self)
		self.connection = connection                        # Connection Information
		self.address = address                              # Client Address Properties
		self.server = server                                # Reference to main server
		self.connected = True                               # Connection status
		self.ip=ip
		self.pid=pid
		self.robotIP="127.0.0.1"#"192.168.43.214"
		self.robotPort=9559
		self.buffer=Network.Buff(self)

		self.msg_id=-1


	def sendmessage(self):
		types = ''.join(self.buffer.BufferWriteT)
		self.connection.send(struct.pack("="+types,*self.buffer.BufferWrite))

	def case_message_connect(self):
		self.buffer.string_size=self.buffer.readshort()
		ip=self.buffer.readstring()#self.robotIP=self.buffer.readstring()
		self.buffer.string_size=self.buffer.readshort()
		port=int(self.buffer.readstring())#self.robotPort=int(self.buffer.readstring())
		print("Trying to connect to",self.robotIP,self.robotPort)
		try:
			tts=naoqi.ALProxy("ALTextToSpeech",self.robotIP,self.robotPort)
			self.buffer.writebyte(1)
			self.sendmessage()
			print("Sucessfully connected to",self.robotIP,self.robotPort)
		except:
			self.buffer.writebyte(0)
			self.sendmessage()
			print("Failed to connect to",self.robotIP,self.robotPort)

	def case_message_tts(self):
		self.buffer.string_size=self.buffer.readshort()
		line=self.buffer.readstring()
		try:
			tts=naoqi.ALProxy("ALTextToSpeech",self.robotIP,self.robotPort)
			tts.say(line)
			self.buffer.writebyte(1)
			self.sendmessage()
		except:
			self.buffer.writebyte(0)
			self.sendmessage()

	def run(self):
		while self.connected:
			data=self.connection.recv(1)
			if data!=b'':
				self.msg_id=struct.unpack('!B',data)[0]

				if self.msg_id==1:
					self.case_message_connect()
				if self.msg_id==2:
					self.case_message_tts()

				#self.connected=False


			time.sleep(1.0/60.0)


		self.connection.close()
		print("Disconnected")

				
