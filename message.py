from tkinter import *
from bot import Chatbot
class FirstGUI:
    def __init__(self,master):
        self.master=master
        master.title("Messenger")
        master.geometry("1000x1000")
        master.configure(background="blue")
        #OUTPUT   
        self.label=Label(master, text="Output",width=100,font="ComicSans 15 bold",bg="blue",fg="gold")
        self.label.pack()
 
        #Message Box
        self.frame=Frame(master,bg="black",bd=4,highlightbackground="black",width=1000,height=500, relief=SUNKEN)  
        self.frame.pack(expand=False)
        self.frame.grid_columnconfigure(0,minsize=990)
        
        #Variable for every last message arrival 
        self.p=0
        
        #Initial Value to print on message box
        StringArray=["Hey! What can I do for you"]
        Array=[0]
        for i in range(10):
              StringArray.append("")
              Array.append(0)
        
        #Variable for every messages in current screen
        self.message=[]
        for i in range(11):
             self.frame.grid_rowconfigure(i,minsize=80)
             Typing=StringArray[i]
             #No text in message to show clear
             if Typing=="" or Typing==" ":
                 colr="black"
                 jst="left"
                 r=FLAT
             #For message from application
             elif Array[i]==0:
                 d=NW
                 colr="yellow"
                 jst="left"
                 r=RAISED
             #For message from User
             elif Array[i]==1:
                 d=NE
                 colr="lawn green"
                 jst="right"
                 r=RAISED
             self.message.append(Message(self.frame, text=Typing, bg=colr,width="600",justify=jst,font="ComicSans 10 bold",relief=r))
             self.message[i].grid(row=i,column=0,sticky=d,pady=10)
        
        #INPUT
        self.label2=Label(master, text="INPUT",width=100,font="ComicSans 15 bold",bg="blue",fg="gold")
        self.label2.pack()
      
        #Varialble used to clear the screen
        self.k=0
        
        #For Textbox
        self.text = Text(root,font="ComicSans 15",width="65",height="2",wrap=WORD)
        self.text.pack(side="left")
        
        #Variable used to define whole screen has maximum no. of messages
        self.m=0
        
        #Button for clearing
        self.B1 = Button(root, text ="Clear",command=lambda: self.clear(master,StringArray,Array),fg="white",bg="black",activeforeground="yellow",activebackground="gray37",font="Times 15 bold",padx=10,pady=10)
        self.B1.pack(side="right")
        
        #Button for sending
        self.B = Button(root, text ="Send",command=lambda: self.Send(master,StringArray,Array),fg="white",bg="black",activeforeground="yellow",activebackground="gray37",font="Times 15 bold",padx=10,pady=10)
        self.B.pack(side="right")   
            
    #Function for clearing
    def clear(self,master,StringArray,Array):
        for i in range(11):
            StringArray[i]=""
            Array[i]=0
        StringArray[0]="Hey! What can I do for you"    
        self.k=1
        self.Send(master,StringArray,Array)       
    
    #Function for sending   
    def Send(self,master,StringArray,Array):
        p=self.p
        m=self.m
        #To check screen is full
        if p==10:
           m=1            
        #To check function is call directly without calling clear
        if self.k==0:   
           Typing=self.text.get("1.0","1.220")
           #To delete text of send box
           self.text.delete("1.0",END)
           if Typing!="":
             p=(p+1)%11
             StringArray[p]=Typing
             Array[p]=1
             p=(p+1)%11
             reply=CB.inference(Typing,1)
             StringArray[p]=' '.join(reply)
             Array[p]=0
           if m==1:
               j=(p+2)%11
           else:
               j=0
        #To check function is call indirectly with calling clear
        else:
           j=0
           p=0
           self.k=0
           m=0              
        #To print new screen contents
        for i in range(11):
             self.frame.grid_rowconfigure(i,minsize=80)
             Typing=StringArray[j]
             if Typing=="" or Typing==" ":
                    d=NW
                    colr="black"
                    jst="left"
                    r=FLAT
             elif Array[j]==0:
                     d=NW
                     colr="yellow"
                     jst="left"
                     r=RAISED
             elif Array[j]==1:
                     d=NE
                     colr="lawn green"
                     r=RAISED
                     jst="right"
             self.message[i].grid_remove()
             self.message[i]=Message(self.frame, text=Typing, bg=colr,width="600",justify=jst,font="ComicSans 10 bold",relief=r)
             self.message[i].grid(row=i,column=0,sticky=d)                    
             j=(j+1)%11
        self.p=p 
        self.m=m

if __name__== '__main__':
      root=Tk()
      CB=Chatbot()
      #To make the GUI
      my_gui=FirstGUI(root)
      root.mainloop()
