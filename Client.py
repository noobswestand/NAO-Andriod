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
		self.robotPort=60856
		self.buffer=Network.Buff(self)

		self.msg_id=-1


	def sendmessage(self):
		types = ''.join(self.buffer.BufferWriteT)
		self.connection.send(struct.pack("="+types,*self.buffer.BufferWrite))

	def case_message_connect(self):
		self.buffer.string_size=self.buffer.readshort()
		ip=self.buffer.readstring()
		#self.robotIP=self.buffer.readstring()
		self.buffer.string_size=self.buffer.readshort()
		port=int(self.buffer.readstring())
		#self.robotPort=int(self.buffer.readstring())
		print("Trying to connect to",self.robotIP,self.robotPort)
		try:
			tts=naoqi.ALProxy("ALTextToSpeech",self.robotIP,self.robotPort)
			self.buffer.clearbuffer()
			self.buffer.writebyte(1)
			self.sendmessage()
			print("Sucessfully connected to",self.robotIP,self.robotPort)
		except:
			self.buffer.clearbuffer()
			self.buffer.writebyte(0)
			self.sendmessage()
			print("Failed to connect to",self.robotIP,self.robotPort)

	def case_message_tts(self):
		self.buffer.string_size=self.buffer.readshort()
		line=self.buffer.readstring()
		speed=self.buffer.readbyte()
		pitch=self.buffer.readbyte()
		try:
			tts=naoqi.ALProxy("ALTextToSpeech",self.robotIP,self.robotPort)
			tts.setParameter("speed", int(float(speed)+50))
			tts.setParameter("pitchShift", float(pitch+50)/100.0)
			tts.say(line)
			self.buffer.clearbuffer()
			self.buffer.writebyte(1)
			self.sendmessage()
		except:
			self.buffer.clearbuffer()
			self.buffer.writebyte(0)
			self.sendmessage()
	def case_message_battery(self):
		try:
			bat = naoqi.ALProxy("ALBattery",self.robotIP,self.robotPort)
			self.buffer.clearbuffer()
			self.buffer.writebyte(bat.getBatteryCharge())
			self.sendmessage()
		except:
			self.buffer.clearbuffer()
			self.buffer.writebyte(255)
			self.sendmessage()
	def case_message_volume(self):
		vol=self.buffer.readbyte()
		try:
			aud = ALProxy("ALAudioDevice", self.robotIP,self.robotPort)
			realvol=aud.getOutputVolume()
			if vol!=255:
				aud.setOutputVolume(vol)
			self.buffer.clearbuffer()
			self.buffer.writebyte(realvol)
			self.sendmessage()
		except:
			self.buffer.clearbuffer()
			self.buffer.writebyte(255)
			self.sendmessage()
	def case_message_posture(self):
		self.buffer.string_size=self.buffer.readshort()
		posture=self.buffer.readstring()
		speed=float(self.buffer.readbyte())/100.0

		print(posture,speed)
		try:
			pp=naoqi.ALProxy("ALRobotPosture",self.robotIP,self.robotPort)
			pp.goToPosture(posture,speed)
			self.buffer.clearbuffer()
			self.buffer.writebyte(1)
			self.sendmessage()
		except:
			self.buffer.clearbuffer()
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
				if self.msg_id==3:
					self.case_message_battery()
				if self.msg_id==4:
					self.case_message_volume()

				if self.msg_id==5:
					self.case_message_posture()

				#self.connected=False


			time.sleep(1.0/60.0)


		self.connection.close()
		print("Disconnected")

				
