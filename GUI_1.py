from tkinter import *
import qrcode
import mysql.connector
from PIL import Image,ImageTk

class generator:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1930x1080")
        self.root.title("QR Code Generator")
        #self.root.resizable(False,False)

        title=Label(self.root,text="QR Code Generator",font=("times new roman",40),fg="white",bg='#053246').place(x=0,y=0,relwidth=1)
        
        qr_frame=Frame(self.root,relief=RIDGE,bg="white",border=5)
        qr_frame.place(x=60,y=90,width=700,height=650)

        qr_frame_title=Label(qr_frame,text="Product Details",bg='#053246',font=("times new roman",30),fg="white")
        qr_frame_title.place(x=0,y=0,relwidth=1)
        
        #---------variables-----------
        self.Id=StringVar()
        self.Cost=StringVar()
        self.Units=StringVar()
        self.Expiry=StringVar()
        self.msg=""
        self.count=1
        
        
        #-----------details------------

        lbl_prod_id=Label(qr_frame,text="Product ID",font=("times new roman",20,'bold'),fg="black",bg="white")
        lbl_prod_id.place(x=50,y=100,width=200)
        self.txt_prod_id=Entry(qr_frame,font=("times new roman",20),bg="yellow",fg="black",textvariable=self.Id)
        self.txt_prod_id.place(x=300,y=100,width=300)

        lbl_cost=Label(qr_frame,text="Product Cost",font=("times new roman",20,'bold'),fg="black",bg="white")
        lbl_cost.place(x=50,y=200,width=200)
        self.txt_cost=Entry(qr_frame,font=("times new roman",20),bg="yellow",fg="black",textvariable=self.Cost)
        self.txt_cost.place(x=300,y=200,width=300)

        lbl_units=Label(qr_frame,text="Units",font=("times new roman",20,'bold'),fg="black",bg="white")
        lbl_units.place(x=50,y=300,width=200)
        self.txt_units=Entry(qr_frame,font=("times new roman",20),bg="yellow",fg="black",textvariable=self.Units)
        self.txt_units.place(x=300,y=300,width=300)

        lbl_expiry=Label(qr_frame,text="Expiry Month",font=("times new roman",20,'bold'),fg="black",bg="white")
        lbl_expiry.place(x=50,y=400,width=200)
        self.txt_expiry=Entry(qr_frame,font=("times new roman",20),bg="yellow",fg="black",textvariable=self.Expiry)
        self.txt_expiry.place(x=300,y=400,width=300)

        generate=Button(qr_frame,text="Generate & Save",command=self.generate,font=("times new roman",21,'bold'),fg="white",bg='#123456')
        generate.place(x=100,y=500,width=220)

        clear=Button(qr_frame,text="Clear",command=self.clear,font=("times new roman",21,'bold'),fg="white",bg='#123456')
        clear.place(x=350,y=500,width=200)
        
        self.message_=Label(qr_frame,text=self.msg,font=("times new roman",25,'bold'),fg="green",bg="white")
        self.message_.place(x=0,y=580,relwidth=1)

        qr_code=Frame(self.root,relief=RIDGE,bg="white",border=5)
        qr_code.place(x=860,y=90,width=600,height=650)

        lbl_right_title=Label(qr_code,text="Product QR Code",bg='#053246',font=("times new roman",30),fg="white")
        lbl_right_title.place(x=0,y=0,relwidth=1)

        self.qr_img=Label(qr_code,text="Not Available",font=("times new roman",18),bg="black",fg="white")
        self.qr_img.place(x=100,y=100,width=400,height=400)
        
    # generate button function
    def generate(self):
        if self.Id.get()=='' or self.Cost.get()=='' or self.Units.get()=='' or self.Expiry.get()=='':
            self.msg="All fields are required"
            self.message_.config(text=self.msg,fg="red")
            self.qr_img.config(text="Not Available",font=("times new roman",18),bg="black",fg="white")
        else:
            print(self.Id.get(),self.Cost.get(),self.Units.get(),self.Expiry.get())
            self.msg="QR Code Generated Sucessfully!!!"
            self.message_.config(text=self.msg,fg="green")
            #data set
            # qr_data=(f"{self.Id.get()}\n{self.Cost.get()}\n{self.Units.get()}\n{self.Expiry.get()}")  
            # qr=qrcode.make(qr_data)
            x=int(self.Units.get())
            #  qr.png('code.png',scale=10)
            # self.count+=1
            a=self.Id.get()
            b=self.Cost.get()
            c=self.Units.get()
            d=self.Expiry.get()
            e=1
            
            if x==1:
                # qr_data=(f"{a}\n{b}\n{x}\n{d}")  
                qr_data=(f"{a}\n{b}\n{x}\n{d}\n{e}")
                qr=qrcode.make(qr_data)
                x=int(self.Units.get())
                self.img=ImageTk.PhotoImage(qr)
                print(qr)
                self.qr_img.config(image=self.img)
                qr.save("D:\Desktop\qr folder\QR_project\_"+str(self.Id.get())+str(x)+".png")
                # con=mysql.connector.connect(host="localhost",user="root",password="chetan",database="products")
                # print(con)
                # con=mysql.connector.connect(host="",user="root",password="chetan",database="products")
                # print(con)
                con=mysql.connector.connect(host="localhost",user="root",password="chetan",database="products")
                print(con)
                mycursor=con.cursor()
                s='insert into item values(%s,%s,%s,%s)'
                t=(self.Id.get(),self.Cost.get(),self.Units.get(),self.Expiry.get())
                mycursor.execute(s,t)
                mycursor.execute("select * from item")
                for i in mycursor:
                    print(i)
                con.commit()
            if x>1:
                for i in range(1,x+1):
                    qr_data=(f"{a}\n{b}\n{i}\n{d}\n")  
                    qr=qrcode.make(qr_data)
                    x=int(self.Units.get())
                    self.img=ImageTk.PhotoImage(qr)
                    print(qr)
                    self.qr_img.config(image=self.img)
                    qr.save("D:\Desktop\qr folder\QR_project\_"+str(self.Id.get())+str(i)+".png")
                    con=mysql.connector.connect(host="localhost",user="root",password="chetan",database="products")
                    print(con)
                    mycursor=con.cursor()
                    s='insert into item values(%s,%s,%s,%s)'
                    t=(self.Id.get(),self.Cost.get(),i,self.Expiry.get())
                    # mycursor.execute(s,t)
                    mycursor.execute("select * from item")
                    for i in mycursor:
                        print(i)
                    con.commit()
                    
    def clear(self):
        self.msg=""
        self.message.config(text=self.msg,fg="green")
        self.txt_prod_id.delete(0,END)
        self.txt_expiry.delete(0,END)
        self.txt_cost.delete(0,END)
        self.txt_units.delete(0,END)
        
        
root=Tk()
obj=generator(root)
root.mainloop()