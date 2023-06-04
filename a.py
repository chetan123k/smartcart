from tkinter import *
from tkinter import ttk
from turtle import width
import cv2
import pyzbar.pyzbar as pyzbar
from PIL import Image, ImageTk
import mysql.connector
import winsound
import time
from playsound import playsound
import numpy as np
from fpdf import FPDF
from pdf_mail import sendpdf


def add_item():
   dict["flag"]=0
   time.sleep(0.1)
   msg.config(text="Scan the product to add to cart",bg="#053246",fg="yellow")
   
def remove_item():
   dict["flag"]=1
   print(dict["flag"])
   time.sleep(0.1)
   msg.config(text="Scan the product to remove from cart",bg="#053246",fg="yellow")
   
def end_shopping():
   total=0
   t_len=len(item_list)
   for i in range(0,t_len):
      cost=item_list[i][1]*item_list[i][4]
      total=total+cost
      con=mysql.connector.connect(host="localhost",user="root",password="chetan",database="products")
      print(con)
      mycursor=con.cursor()
      name=item_list[i][0]
      id=item_list[i][2]
      t=[name,id]
      s="delete from item where name=%s and unit_no=%s"
      # mycursor.execute("SELECT * FROM item WHERE name=;" % D[0])
      mycursor.execute(s,t)
      mycursor.execute("select * from item")
      for i in mycursor:
         print(i)
      con.commit()
   print("total bill :")
   print(total)
   bill.insert(END,"\n==================================================")
   bill.insert(END,f"\nTotal\t\t\t\t\t{total}\n")
   text_file = open("F:\\python programs\\myfile.txt", "w")
   text_file.write(bill.get(1.0, END))
   text_file.close()
   
   pdf=FPDF()
   pdf.add_page()
   pdf.set_font("Times",size=30)
   fd=open("F:\\python programs\\myfile.txt","r")
   for i in fd:
      pdf.cell(100,10,txt = i,ln =1, align='C')
   pdf.output("F:\\python programs\\my.pdf")
   print("done")
   
   sender_email_address ="chetankulkarni004@gmail.com" 
   receiver_email_address ="srushtishastrybelagere123@gmail.com"
   sender_email_password ="ndraumwobxpodnav"
   subject_of_email ="SMARTCART"  
   body_of_email ="Dear customer ,Thank for shopping with us.........😊"
   filename ="my"       
   location_of_file ="F:\python programs"
  

   k = sendpdf(sender_email_address, 
            receiver_email_address,
            sender_email_password,
            subject_of_email,
            body_of_email,
            filename,
            location_of_file)
 
   k.email_send()
   
   
root=Tk()
root.title("Billing Software")
# root.attributes('-fullscreen', True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
name=Label(root,text="Billing System",bd=12,font=("Times New Roman",40),pady=2,relief=GROOVE,bg='#053246',justify=CENTER,fg="white")
name.place(x=0,y=0,width="1530",height="100")

F1=LabelFrame(root,text="Customer Details",bd=12,font=("Times New Roman",15),pady=2,relief=GROOVE,bg='#053246',fg="white")
F1.place(x=0,y=105,relwidth=1,height="80")

cn1=Label(F1,text="Customer Name",font=("times new roman",15,"bold"),fg="gold",bg='#053246').grid(row=0,column=0,padx=20,pady=5)
cn2=Entry(F1,font=("times new roman",15,"bold"),fg="Black").grid(row=0,column=1,padx=20,pady=5)

m1=Label(F1,text="Contact Number",font=("times new roman",15,"bold"),fg="gold",bg='#053246').grid(row=0,column=7,padx=20,pady=5)
m2=Entry(F1,font=("times new roman",15,"bold"),fg="Black").grid(row=0,column=8,padx=20,pady=5)

F4=Frame(root,bg='#053246',pady=2,relief=GROOVE)
F4.place(x=1290,y=190,width=300,height=550)

add=Button(F4,text="Add",command=add_item,font=("Times New Roman",20),pady=2,relief=GROOVE,bg='yellow',fg="black")
add.place(x=35,y=5,width=190,height=80)

rem=Button(F4,text="Remove",command=remove_item,font=("Times New Roman",20),pady=2,relief=GROOVE,bg='yellow',fg="black")
rem.place(x=35,y=95,width=190,height=80)

rem=Button(F4,text="End Shopping",command=end_shopping,font=("Times New Roman",20),pady=2,relief=GROOVE,bg='Green',fg="black")
rem.place(x=35,y=185,width=190,height=80)

rem=Button(F4,text="Cancel",font=("Times New Roman",20),pady=2,relief=GROOVE,bg='Red',fg="black")
rem.place(x=35,y=275,width=190,height=80)

F3=LabelFrame(root,bd=12,font=("Times New Roman",15),pady=2,relief=GROOVE,bg='#053246',fg="white")
F3.place(x=610,y=190,width=680,height=550)

msg=Label(root,text="Scan the product to add",font=("Times New Roman",40),fg='yellow',bg='#053246')
msg.place(x=0,y=740,width=1550,height=50)
label =Label(F3)
label.place(x=10,y=10)

cap= cv2.VideoCapture(0)#enables the cam useage
D=[]            #list to store scanned qr data
dict={'flag':0} #to decide the add or remove operation
item_list=[]  #ontains the product list till end 
R=[] 
new_list=[]

name="chetan"
bill_no="12452"
pnum="8095082268"
F3=LabelFrame(root,text="BILL",pady=2,relief=GROOVE,bd=12,font=("times new roman",15),fg="gold",bg='#053246').place(x=0,y=190,width=600,height=550)
bill=Text(F3,font=("times new roman",15,"bold"))
bill.place(x=20,y=220,width=560,height=500)
text_scroll=ttk.Scrollbar(bill,orient="vertical")
text_scroll.pack(side=RIGHT)

# Define function to show frame
def show_frames():
   # Get the latest frame and convert into Image
   cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
   decodedObjects = pyzbar.decode(cv2image)
   for obj in decodedObjects:
            D=obj.data.decode("utf-8")
            D=D.splitlines()
            # print(D)
            D[1]=int(D[1])
            D[4]=int(D[4])
            # print(D)
            l=len(D)
            # for each in range(l):
            #     print(D[each])
            if decodedObjects:
               if dict["flag"]==0:
                  done=0
                  winsound.Beep(3000,500)
                  time.sleep(1)
                  leng=len(item_list)
                  for each in range(0,leng):
                     print(each)
                     a=item_list[each]
                     b=item_list[each]
                     if D==a:
                        if D==b: 
                           done=1
                           break
                  if done==0:
                     item_list.append(D)
                     new_list.append(D)
                     item_list.sort()
                     print(item_list)
                     quantity=[]

                     for i in range(0,len(new_list)-1,1):
                        quantity.append(1)
                        count=0
                        for j in range(i+1,len(new_list),1):
                           if new_list[i][0]==new_list[j][0]:
                                 count+=1
                                 new_list[i][4]+=new_list[j][4]
                                 quantity[i]+=1
                                 new_list.pop(i + 1)
                           else:
                                 i=j
                                 break

                     print(quantity)
                     print(item_list)
                     print("new list :")
                     print(new_list)
                     playsound(r'C:\Users\chetan kulkarni\Downloads\project_voice.mp3')
                  elif done==1:
                     playsound(r'C:\Users\chetan kulkarni\Downloads\already_present.mp3')
                     
                  bill.delete('1.0',END)
                  bill.insert(END,"\t\tSmart Cart for Easy Shopping\n")
                  bill.insert(END,"``````````````````````````````````````````````````````````````````````````````")
                  bill.insert(END,f"\nBill No. : {str(bill_no)}")
                  bill.insert(END,f"\nCustomer Name : {str(name)}")
                  bill.insert(END,f"\nPhone No. : {str(pnum)}")
                  bill.insert(END,"\n==================================================")
                  bill.insert(END,"\nProduct\t\t\tQty\t\tPrice")
                  bill.insert(END,"\n==================================================\n")
                  
                  l=len(new_list)
                  for i in range(0,l):
                     info=(f"{new_list[i][0]}\t\t\t{new_list[i][4]}\t\t{new_list[i][1]*new_list[i][4]}\n")
                     bill.insert(END,info)
                        
               elif dict["flag"]==1:
                  done=0  #to add voice msg
                  leng=len(item_list)
                  print(leng)
                  for each in range(0,leng):
                     print(each)
                     a=item_list[each]
                     b=item_list[each]
                     if D==a:
                        if D==b: 
                           done=1
                           item_list.pop(each)
                           for i in range(0,len(new_list)):
                              if new_list[i][0]==D[0] and len(new_list)>0:
                                 print("yes")
                                 if new_list[i][4]==1:
                                    new_list.pop(i)
                                 else:
                                    new_list[i][4]=new_list[i][4]-1
                           break
                  winsound.Beep(3500,1000)
                  time.sleep(1)
                  D.clear()
                  dict["flag"]==0 
                  print(item_list)   
                  bill.delete('1.0',END)
                  bill.insert(END,"\t\tSmart Cart for Easy Shopping\n")
                  bill.insert(END,"``````````````````````````````````````````````````````````````````````````````")
                  bill.insert(END,f"\nBill No. : {str(bill_no)}")
                  bill.insert(END,f"\nCustomer Name : {str(name)}")
                  bill.insert(END,f"\nPhone No. : {str(pnum)}")
                  bill.insert(END,"\n==================================================")
                  bill.insert(END,"\nProduct\t\t\tQty\t\tPrice")
                  bill.insert(END,"\n==================================================\n")
                  file1 = open("myfile.txt", "w")
                  L = ["\t\tSmart Cart for Easy Shopping\n``````````````````````````````````````````````````````````````````````````````",f"\nBill No. : {str(bill_no)}",
                       f"\nCustomer Name : {str(name)}",f"\nPhone No. : {str(pnum)}","\n==================================================",
                       "\nProduct\t\t\tQty\t\tPrice","\n=================================================="]
                  file1.writelines(L)
                  file1.close()
                  l=len(new_list)
                  # if done==1:
                  #    playsound(r'C:\Users\chetan kulkarni\Downloads\remove_voice.mp3')
                  #    print("removed")
                  # elif done==0:
                  #    playsound(r'C:\Users\chetan kulkarni\Downloads\remove_not_present.mp3')
                     
                  for i in range(0,l):
                     info=(f"{new_list[i][0]}\t\t\t{new_list[i][4]}\t\t{new_list[i][1]}\n")
                     bill.insert(END,info)     
   img = Image.fromarray(cv2image)
   # Convert image to PhotoImage
   imgtk = ImageTk.PhotoImage(image = img)
   label.imgtk = imgtk
   label.configure(image=imgtk)
   # Repeat after an interval to capture continiously
   label.after(20, show_frames)
   
show_frames()
   
root.mainloop() 
