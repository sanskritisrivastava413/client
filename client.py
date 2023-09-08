import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = "127.0.0.1"
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
	def __init__(self):
		
		self.Window = Tk()
		self.Window.withdraw()
		
		self.login = Toplevel()
		self.login.title("Login")
		self.login.resizable(width = False,
							height = False)
		self.login.configure(width = 400,
							height = 300)
		self.pls = Label(self.login,
					text = "Please login to continue",
					justify = CENTER,
					font = "Helvetica 14 bold")
		
		self.pls.place(relheight = 0.15,
					relx = 0.2,
					rely = 0.07)
		self.labelName = Label(self.login,
							text = "Name: ",
							font = "Helvetica 12")
		
		self.labelName.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.2)
		
		self.entryName = Entry(self.login,
							font = "Helvetica 14")
		
		self.entryName.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.2)
		
		self.entryName.focus()

		self.go = Button(self.login,
						text = "CONTINUE",
						font = "Helvetica 14 bold",
						command = lambda: self.goAhead(self.entryName.get()))
		
		self.go.place(relx = 0.4,
					rely = 0.55)
		self.Window.mainloop()

	def goAhead(self, name):
		self.login.destroy()
		self.layout(name)
		rcv = Thread(target=self.receive)
		rcv.start()

	def layout(self,name):
		
		self.name = name
		self.Window.deiconify()
		self.Window.title("CHATROOM")
		self.Window.resizable(width = False,
							height = False)
		self.Window.configure(width = 470,
							height = 550,
							bg = "#17202A")
		self.labelHead = Label(self.Window,
							bg = "#17202A",
							fg = "#EAECEE",
							text = self.name ,
							font = "Helvetica 13 bold",
							pady = 5)
		
		self.labelHead.place(relwidth = 1)
		self.line = Label(self.Window,
						width = 450,
						bg = "#ABB2B9")
		
		self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
		
		self.textCons = Text(self.Window,
							width = 20,
							height = 2,
							bg = "#17202A",
							fg = "#EAECEE",
							font = "Helvetica 14",
							padx = 5,
							pady = 5)
		
		self.textCons.place(relheight = 0.745,
							relwidth = 1,
							rely = 0.08)
		
		self.labelBottom= Label(self.Window, bg = "cyan", height= 70)
        self.labelBottom.place(relwidth= 1, rely= .8)
        
        self.entrymsg = Entry(self.labelBottom, bg = "white", fg= "blue")
        self.entrymsg.place(relwidth= 0.7, relheight=0.06, rely=0.008,relx=0.01)
        self.entrymsg.focus()
        
        self.buttonMsg = Button(self.labelBottom, text="send", width=20, bg="yellow", command=lambda:self.sendButton[self.entrymsg.get()])
        self.buttonMsg.place(relx=0.7,rely=0.008,relheight=0.06, relwidth=0.2)
        
        self.textCons.config(cursor="arrow")
        self.scrollbar = Scrollbar(self.textCons)
        self.scrollbar.place(relheight=1,relx=0.9)
        self.scrollbar.config(command= self.textCons.yview)
        
    def sendButton(self,msg):
        self.textCons.config(state=DISABLED)
		self.msg = msg
		self.entrymsg.delete(0 , END)
        snd = Thread(target= self.write)
        snd.start()
		
    def showMsg(self,msg):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END,msg+"\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)
        
    def write(self):
        self.textCons.config(state=DISABLED)
        while True:
            Message =(f"{self.name}:{self.msg}")
            client.send(Message.encode("utf-8"))
            self.showMsg(Message)
			break


	def receive(self):
		while True:
			try:
				message = client.recv(2048).decode("utf-8")
				if message == "NICKNAME":
					client.send(self.name.encode("utf-8"))
				else:
					self.showMsg(message)
			except:
				print("An error occured!")
				client.close()
				break

	

g = GUI()