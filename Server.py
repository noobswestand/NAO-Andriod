import socket,sys,Client,time,select
from threading import Thread,Lock

class Server:
	def __init__(self,port):
		self.running = True
		self.max_clients=5
		self.clients=[]
		self.clientpid=0
		self.port=port
		
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		try:
			self.socket.bind(("", self.port))
			self.socket.listen(5)
		except socket.error as err:
			self.running = False
			print("Failed to bind socket: [{0}] {1}".format(err[0], err[1]))
			sys.exit()



	def inputs(self):
		while self.running:
			x=str(input("Server>"))
			if "exit" in x:
				for c in self.clients:
					c.connected=False
				self.running=False

	def start(self):
		#Inputs
		self.input_thread = Thread(target = self.inputs)
		self.input_thread.setDaemon(True)
		self.input_thread.start()

		read_list = [self.socket]
		while self.running:
			time.sleep(1/1000)
			readable, writable, errored = select.select(read_list, [], [],1)
			for s in readable:
				if s is self.socket:
					connection, address = self.socket.accept()
					read_list.append(connection)
					print("Connected to {0}:{1}".format(address[0], address[1]))
					client = Client.Client(connection, address, self, self.clientpid,address[0])
					client.start()
					self.clients.append(client)
					self.clientpid+=1

			#self.socket.listen(self.max_clients)
			#connection, address = self.socket.accept()
			


server=Server(5000)
#server=Thread(target = Server,args=(5000,))
#server.setDaemon(True)
server.start()
