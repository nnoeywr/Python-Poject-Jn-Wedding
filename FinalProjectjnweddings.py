import sqlite3
from tkinter import *
from PIL import Image, ImageTk
from tkcalendar import Calendar
import requests
import cv2
import numpy as np
from io import BytesIO
import re
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import yagmail
from yagmail.error import YagConnectionClosed
conn = sqlite3.connect('registers.db')
c = conn.cursor()
try:
        c.execute('''CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,--
                name VARCHAR(30) NOT NULL,
                lastname VARCHAR(30) NOT NULL,
                tel VARCHAR(10) NOT NULL,
                email VARCHAR(30) NOT NULL,
                password VARCHAR(30) NOT NULL)''')
        c.execute('''CREATE TABLE booking (id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR(50) NOT NULL,
                package VARCHAR(30) NOT NULL,
                booking_date VARCHAR(30) NOT NULL,
                day VARCHAR(10) NOT NULL,
                month VARCHAR(10) NOT NULL,
                year VARCHAR(10) NOT NULL,
                address VARCHAR(30) NOT NULL,
                status VARCHAR(30) NOT NULL)''')
        c.execute('''CREATE TABLE data (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) NOT NULL,
                booking_date VARCHAR(30) NOT NULL,
                address VARCHAR(30) NOT NULL,
                status VARCHAR(30) NOT NULL,
                email VARCHAR(50) NOT NULL)''')
        conn.commit ()
except:
    pass
def Register():
        Regiswindow = Toplevel(root)
        Regiswindow.title("Member")
        registration_complete = False  
        Regiswindow.geometry('600x400+480+170')
        Regiswindow.resizable(False,False)
        bg_image_register = Image.open(r"D:\python\register_bg.png")
        bg_photo_register = ImageTk.PhotoImage(bg_image_register)
        bg_label_register = Label(Regiswindow,image=bg_photo_register)
        bg_label_register.photo = bg_photo_register # เก็บ reference รูปภาพ
        bg_label_register.pack(fill="both", expand=True)
        def newmember():
                nonlocal registration_complete
                name = name_entry.get()
                lastname = lastname_entry.get()
                tel = tel_entry.get()
                email = email_entry.get()
                password = password_entry.get()
                if not name and not lastname and not tel and not email and not password:##เช็คว่ากรอกข้อมูลครบหรือไม่
                        result_label.config(text="กรุณากรอกข้อมูลให้ครบถ้วน")    
                else:
                        if not tel.isdigit() or len(tel) != 10:##เช็คเบอร์
                               result_label.config(text="กรุณากรอกหมายเลขโทรศัพท์ให้ถูกต้อง")
                        else :
                                try:       
                                        if len(password)>=6 and re.match(r'^[A-Z]', password):##check password
                                                conn = sqlite3.connect('registers.db')
                                                c = conn.cursor()
                                                c.execute("SELECT email FROM users WHERE email=?", (email,))
                                                check_email = c.fetchone()
                                                if check_email:##check email
                                                        result_label.config(text="มีอีเมลล์นี้อยู่แล้ว กรุณาใช้อีเมลล์อื่น")
                                                elif not re.match("^[a-zA-Z0-9 @ . .]+$", email)or not email.endswith('.com'):
                                                        result_label.config(text="กรุณาตรวจสอบอีเมลล์ให้ถูกต้อง")
                                                else:          
                                                        sql = '''INSERT INTO users (name, lastname, tel, email, password) VALUES (?, ?, ?, ?, ?)'''
                                                        data = (name, lastname, tel, email, password)
                                                        c.execute(sql, data)
                                                        
                                                        conn.commit()
                                                        messagebox.showinfo("result", "ลงทะเบียนสำเร็จ:)")                                                        
                                                        registration_complete = True
                                                        delay_ms = 500
                                                        Regiswindow.after(delay_ms, Regiswindow.destroy())  
                                        else:
                                                result_label.config(text="รหัสผ่านควรขึ้นต้นด้วยตัวอักษรพิมพ์ใหญ่\nและต้องมีอย่างน้อย 6 ตัวขึ้นไป")
                                except:
                                        ()
        name_entry = Entry(Regiswindow,font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,cursor='hand2')
        name_entry.place(x=90,y=93)

        lastname_entry = Entry(Regiswindow,font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,cursor='hand2')
        lastname_entry.place(x=408,y=93)

        email_entry = Entry(Regiswindow,font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,cursor='hand2')
        email_entry.place(x=98,y=145)

        tel_entry = Entry(Regiswindow,width=13,font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,cursor='hand2')
        tel_entry.place(x=160,y=198)

        password_entry = Entry(Regiswindow,show='*',font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,cursor='hand2')
        password_entry.place(x=405,y=145)
        #ปุ่มลงทะเบียน
        reg_image = Image.open(r"D:\python\regist_bt.png")
        reg_image = reg_image.resize((110, 40))  # ปรับขนาดปุ่ม
        reg_photo = ImageTk.PhotoImage(reg_image)
        reg_But= Button(Regiswindow,image=reg_photo,bg='#fcd9e2',fg='black',command=newmember,cursor="hand2", font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,activebackground='#fcd9e2')
        reg_But.photo = reg_photo
        reg_But.place(x=320,y=185)  
        #ปุ่มกลับ
        back1_image = Image.open(r"D:\python\back4_bt (1).png")
        back1_image = back1_image.resize((110, 40))  # ปรับขนาดปุ่ม
        back1_photo = ImageTk.PhotoImage(back1_image)
        back1_But= Button(Regiswindow,image=back1_photo,bg='#fcd9e2',fg='black',command=lambda:(Regiswindow.destroy()),cursor="hand2", font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,activebackground='#fcd9e2')
        back1_But.photo = back1_photo
        back1_But.place(x=435,y=185)  
        
        
        result_label = Label(Regiswindow, text="",bg='#fcdde2',fg='black',font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0)
        result_label.place(x=320,y=170) 
def login(): 
        login_window = Toplevel(root)
        login_window.title("Login")
        login_window.geometry('600x400+480+170')
        login_window.resizable(False,False)
        bg_image_login = Image.open(r"D:\python\login_bg.png")
        bg_photo_login = ImageTk.PhotoImage(bg_image_login)
        bg_label_login = Label(login_window, image=bg_photo_login)
        bg_label_login.photo = bg_photo_login  # เก็บ reference รูปภาพ
        bg_label_login.pack(fill="both", expand=True)
        logged_in_name = ""
        logged_in_lastname = ""
        show_tel="" 
        show_email=""
        show_status=''
        showpack=''
        sum=''
        name=''
        lname=''
        tel=''
        e=''
        pw=''
        date=''
        def authenticate():##เข้าสู่ระบบเช็ค
                nonlocal logged_in_name #ใช้ประกาศตัวแปรให้ใช้ในฟังก์ชันอื่นภายนอกฟังก์ชันตัวเอง
                nonlocal logged_in_lastname
                nonlocal show_email
                nonlocal show_tel
                email = email_entry.get()
                password = password_entry.get()
                show_email=email
                conn = sqlite3.connect('registers.db')
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
                log = c.fetchone()
                if log :
                        logged_in_name = log[1]  # ชื่ออยู่ในตำแหน่งที่ 1 ของผลลัพธ์ที่คืนมา
                        logged_in_lastname = log[2]
                        show_tel=log[3]
                        result_label.config(text=f'เข้าสู่ระบบสำเร็จ\nชื่อ: {logged_in_name} {logged_in_lastname}')
                        delay_ms = 500
                        login_window.after(delay_ms, packages(), login_window.destroy())
                elif  email=='admin' and password=='123456': 
                        admin()
                        login_window.destroy()                            
                else:
                        result_label.config(text='เข้าสู่ระบบไม่สำเร็จ\nโปรดตรวจสอบอีเมลล์และรหัสผ่านของคุณอีกครั้ง')

        def repass():##func รีเซ็ทรหัส
                login_window.destroy() 
                forgot_passwindow = Toplevel(root)
                forgot_passwindow.title("Forgot Password")
                forgot_passwindow.geometry('500x300+480+170')
                forgot_passwindow.resizable(False,False)
                bg_image_forgot = Image.open(r"D:\python\repassword_bg.png")
                bg_photo_forgot = ImageTk.PhotoImage(bg_image_forgot)
                bg_label_forgot = Label(forgot_passwindow,image=bg_photo_forgot)
                bg_label_forgot.photo = bg_photo_forgot # เก็บ reference รูปภาพ
                bg_label_forgot.pack(fill="both", expand=True)
                def changePassword():
                        email = email_entry.get()
                        new_password = password_entry.get()
                        conn = sqlite3.connect('registers.db')
                        c=conn.cursor()
                        c.execute("SELECT * FROM users WHERE email=?",(email,))
                        user=c.fetchone()
                        if user:
                                if len(new_password)>=6 and re.match(r'^[A-Z]', new_password):
                                        if new_password != user[5]:
                                                c.execute("UPDATE users SET password=? WHERE email=?",(new_password,email))
                                                conn.commit()
                                                result_label.config(text='เปลี่ยนรหัสผ่านสำเร็จค่ะ (✯◡✯)',font=("DB Helvethaica X", 10))    
                                                delay_ms = 500
                                                forgot_passwindow.after(delay_ms,lambda:(forgot_passwindow.destroy(),login()))   
                                        else :
                                                result_label.config(text='รหัสผ่านใหม่ต้องไม่ซ้ำกับรหัสผ่านเดิมค่ะ (πーπ)', font=("DB Helvethaica X", 10))
                                else:
                                        result_label.config(text='รหัสผ่านควรขึ้นต้นด้วยตัวอักษรพิมพ์ใหญ่\nและต้องมีอย่างน้อย 6 ตัวขึ้นไป (πーπ)', font=("DB Helvethaica X", 10))
                        else:
                                result_label.config(text='Not found (πーπ)',font=("DB Helvethaica X", 10),)

                email_entry = Entry(forgot_passwindow,width=25,font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,cursor="hand2")
                email_entry.place(x=175,y=70)
                password_entry = Entry(forgot_passwindow,show='*',width=25,font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,cursor="hand2")
                password_entry.place(x=175,y=170)
                result_label = Label(forgot_passwindow, text="",bg='#fcdbe2',fg='black',font=("DB Helvethaica X", 10))
                result_label.place(x=195,y=202)
                
                #ปุ่ม_repassword
                resetpass_image = Image.open(r"D:\python\resetpass_bt (1).png")
                resetpass_image = resetpass_image.resize((110, 40))  # ปรับขนาดปุ่ม
                resetpass_photo = ImageTk.PhotoImage(resetpass_image)
                resetpass_But= Button(forgot_passwindow,image=resetpass_photo,bg='#fcd9e2',fg='black',command=changePassword,cursor="hand2", font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,activebackground='#fcd9e2')
                resetpass_But.photo = resetpass_photo
                resetpass_But.place(x=150,y=240)
                
                #ปุ่มย้อนกลับหน้า_repassword
                back2_image = Image.open(r"D:\python\back4_bt (1).png")
                back2_image = back2_image.resize((110, 40))  # ปรับขนาดปุ่ม
                back2_photo = ImageTk.PhotoImage(back2_image)
                back2_But= Button(forgot_passwindow,image=back2_photo,bg='#fcd9e2',fg='black',command=lambda:(forgot_passwindow.destroy(),login()),cursor="hand2", font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,activebackground='#fcd9e2')
                back2_But.photo = back2_photo
                back2_But.place(x=280,y=240)  

        def packages():
                packwindow=Toplevel(root)
                packwindow.title("เลือกแพคเกจ")
                packwindow.geometry('1000x650+275+60')  
                packwindow.resizable(False,False)
                bg_image_pack = Image.open(r"D:\python\menu_bg.png")
                bg_photo_pack = ImageTk.PhotoImage(bg_image_pack)
                bg_label_pack = Label(packwindow,image=bg_photo_pack)
                bg_label_pack.photo = bg_photo_pack # เก็บ reference รูปภาพ
                bg_label_pack.pack(fill="both", expand=True) 
                name_label = Label(packwindow, text=f'ชื่อ: {logged_in_name} {logged_in_lastname} ',bg='white',font=("DB Helvethaica X", 15) )
                name_label.place(x=90,y=490)
                def Tabletime(): #ตารางคิวงาน
                        packwindow.destroy()
                        timetable_window = Toplevel(root)
                        timetable_window.title("ตารางเวลา")
                        timetable_window.geometry('1000x650+275+60')
                        timetable_window.resizable(False,False)

                        canvas = Canvas(timetable_window, width=1000, height=650)
                        canvas.pack()

                        # Load and display the background image on the canvas
                        bg_image = Image.open(r"D:\python\bookingtable_bg (1).png")
                        bg_photo = ImageTk.PhotoImage(bg_image)
                        canvas.create_image(0, 0, anchor=NW, image=bg_photo)
                        canvas.image = bg_photo

                        tree_label = tk.Label(timetable_window, text="ตารางงาน", font=("DB Helvethaica X", 14))
                        tree_label.pack(pady=20)

                        frame = Frame(canvas)  # Create a frame as a child of the canvas
                        canvas.create_window((200,150), window=frame, anchor=NW)  # Place the frame on the canvas

                        # ดึงข้อมูลจากฐานข้อมูล
                        c = conn.cursor()
                        c.execute("SELECT * FROM data ")
                        result = c.fetchall()

                        # เรียงลำดับข้อมูลตามคอลัมน์ 'วันที่'
                        sorted_result = sorted(result, key=lambda x: datetime.strptime(x[2], '%Y-%m-%d'))
                        def on_vertical_scroll(*args):
                                tree.yview(*args) 
                        tree = ttk.Treeview(frame, columns=("name", "booking_date", "address"))
                        tree.heading("name", text="ขื่อ-สกุล")
                        tree.heading("booking_date", text="วันที่จอง")
                        tree.heading("address", text="สถานที่จัดงาน")
                        tree.column("name", anchor="center", width=300)
                        tree.column("booking_date", anchor="center", width=100)
                        tree.column("address", anchor="center", width=150)
                        tree.column("#0", width=0, stretch=NO)
                        style = ttk.Style()
                        style.configure("Treeview.Heading", font=("DB Helvethaica X", 12))
                        style.configure("Treeview", font=("DB Helvethaica X", 12))
                        for x in sorted_result:
                                tree.insert("", "end", values=x[1:])
                        vscrollbar = ttk.Scrollbar(frame, orient="vertical",command=on_vertical_scroll)
                        vscrollbar.pack(side="right", fill="y")
                        tree.config(yscrollcommand=vscrollbar.set)
                        tree.pack(fill="both", expand=True)
                        back_image = Image.open(r"D:\python\back-icon.png")
                        back_image = back_image.resize((50, 40))  # ปรับขนาดปุ่ม
                        back_photo = ImageTk.PhotoImage(back_image)
                        back_But= Button(timetable_window,image=back_photo, text="ย้อนกลับ",bg='#e171ac',command=lambda: (packages(), timetable_window.destroy()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#e171ac')
                        back_But.photo = back_photo
                        back_But.place(x=940, y=7) 
                def check_email_booking(email): #
                        conn = sqlite3.connect('registers.db')
                        c = conn.cursor()
                        # ตรวจสอบว่ามีการจองโดยใช้อีเมลล์นี้'
                        c.execute("SELECT COUNT(*) FROM booking WHERE email = ?  ", (email,))
                        booking_count = c.fetchone()[0]  # ดึงจำนวนการจองของอีเมลล์นี
                        conn.close()
                        return booking_count > 0
                def cf(logged_in_name, logged_in_lastname, show_email,show_tel):
                        cf_details = Toplevel(root)
                        cf_details.title(f"ยืนยันการจอง")
                        cf_details.geometry('1000x650+275+60')
                        cf_details.resizable(False,False)
                        booked_image = Image.open(r"D:\python\booking_bg.png")
                        booked_photo = ImageTk.PhotoImage(booked_image)
                        booked_label = Label(cf_details,image=booked_photo)
                        booked_label.photo = booked_photo # เก็บ reference รูปภาพ
                        booked_label.pack(fill="both", expand=True) 
                        def confirm_booking():
                                address = address_entry.get()
                                selected_date = cal.get_date()
                                selected_package = package_var.get()  # รับแพ็คเกจที่ผู้ใช้เลือก
                                nonlocal sum
                                nonlocal show_status
                                nonlocal showpack
                                year, month, day = map(int, selected_date.split('-'))

                                if not address or not selected_date or not selected_package:
                                        result_label.config(text="กรุณากรอกข้อมูลให้ครบถ้วน")
                                else:
                                        if check_email_booking(show_email):  # เรียกใช้ฟังก์ชันเพื่อตรวจสอบการจองเดิมๆ
                                                result_label.config(text="คุณมีการจองอยู่แล้ว\nหากต้องการแก้ไขกรุณาติดต่อAdmin",font=("DB Helvethaica X", 13))
                                        else:
                                                # ตรวจสอบว่าวันที่ที่ผู้ใช้เลือกไม่ซ้ำกับวันที่อื่นที่มีอยู่ในระบบ
                                                conn = sqlite3.connect('registers.db')
                                                c = conn.cursor()
                                                c.execute("SELECT COUNT(*) FROM booking WHERE booking_date = ?", (selected_date,))
                                                booking_count = c.fetchone()[0]  # ดึงจำนวนแถวที่มีวันที่ซ้ำกัน
                                                conn.close()
                                                if   selected_date < current_date:
                                                        result_label.config(text="กรุณาเลือกวันที่ให้ถูกต้อง\nถึงคุณจะเลือกวันที่ในอดีตได้ แต่คุณเลือกให้เขากลับมารักเหมือนในอดีตไม่ได้หรอกค่ะT-T ")
                                                elif booking_count > 0:
                                                        result_label.config(text="วันที่นี้ถูกจองแล้ว")
                                                else :
                                                        pay = Toplevel(root)
                                                        pay.title(f"จ่ายตัง")
                                                        pay.geometry('1000x650+275+60')
                                                        pp_image = Image.open(r"D:\python\payment_bg (1).png")
                                                        pay.resizable(False,False)
                                                        pp_photo = ImageTk.PhotoImage(pp_image)
                                                        pp_label = Label(pay,image=pp_photo)
                                                        pp_label.photo = pp_photo # เก็บ reference รูปภาพ
                                                        pp_label.pack(fill="both", expand=True)        
                                              
                                                        def finished():
                                                                response = messagebox.askyesno("การจอง", "คุณชำระเงินแล้วใช่หรือไม่?")
                                                                if response>0:
                                                                        conn = sqlite3.connect('registers.db')
                                                                        c = conn.cursor()
                                                                        sql1 = '''INSERT INTO booking (email,package, booking_date,day,month,year, address,status) VALUES (?,?,?, ?,?,?,?, ?)'''
                                                                        booked = (show_email,selected_package, selected_date,day,month,year, address,"รอดำเนินการ")
                                                                        c.execute(sql1, booked)
                                                                        c.execute("INSERT INTO data (name, booking_date, address,status,email) VALUES (?,?, ?, ?,?)",(logged_in_name +" "+ logged_in_lastname,  selected_date, address,"รอดำเนินการ",show_email))
                                                                        conn.commit()
                                                                        conn.close()
                                                                        messagebox.showinfo("Result", "การจองสำเร็จ :D")
                                                                        email = show_email
                                                                        try:
                                                                                email_sender = "jnweddingphotograp@gmail.com"
                                                                                app_password = "dqkk gcop cuwp npxg"  

                                                                                recipients = [email]
                                                                              
                                                                                text=f"BookingComplete  \n"
                                                                                text +=F"------------------------------------------------ \n"
                                                                                text +=F"รายละเอียดการจองของคุณคือ \n"
                                                                                text +=F"ชื่อ-สกุล:{logged_in_name}  {logged_in_lastname} \n"
                                                                                text +=F"แพ็คเกตที่จอง:{selected_package} \n"
                                                                                text +=F"วันที่จอง:{selected_date} \n"
                                                                                text +=F"สถานที่:{address} \n"
                                                                                text +=F"------------------------------------------------ \n"
                                                                                text +=F"ขอบคุณที่ใช้บริการ Jn Weddingphotography  \n"
                                                                                yag = yagmail.SMTP(email_sender, app_password)
                                                                                yag.send(
                                                                                        to=recipients,
                                                                                        subject="recipe", 
                                                                                        contents=text 
                                                                                )
                                                                                yag.close()
                                                                        except YagConnectionClosed:
                                                                                messagebox.showerror("Error", "Connection to email server failed. Please check your credentials and internet connection.")
                                                                        except Exception as e:
                                                                                messagebox.showerror("Error", f"An error occurred while sending the email: {str(e)}")
                                                                else:
                                                                        messagebox.showinfo("Result", "กรุณาทำรายการใหม่อีกครั้งค่ะT-T")
                                                                        confirm_booking()               
                                                        info_label =Label(pay, text=f"{logged_in_name} {logged_in_lastname} ",bg='#ffffff',font=("DB Helvethaica X", 15))
                                                        info_label.place(x=160,y=110)
                                                        info_label1 =Label(pay, text=f"{show_tel} ",bg='#ffffff',font=("DB Helvethaica X", 15))
                                                        info_label1.place(x=270,y=185)
                                                        info_label2 =Label(pay, text=f"{selected_package} ",bg='#ffffff',font=("DB Helvethaica X", 15))
                                                        info_label2.place(x=217,y=255)
                                                        info_label2 =Label(pay, text=f"{address} ",bg='#ffffff',font=("DB Helvethaica X", 15))
                                                        info_label2.place(x=270,y=325)
                                                        info_label2 =Label(pay, text=f"{selected_date} ",bg='#ffffff',font=("DB Helvethaica X", 15))
                                                        info_label2.place(x=220,y=397)
                                                        package_prices = {"Package 1": 4000,"Package 2": 9000,"Package 3": 18000}
                                                                        # คำนวณราคารวมจากแพ็คเกจที่ผู้ใช้เลือก
                                                        sum = package_prices.get(selected_package, 0)
                                                        package_url = f"https://promptpay.io/0981965003/{sum}.png"
                                                                        # ตัด URL ราคาเดิมทิ้งแล้วแทนที่ด้วย URL ใหม่ที่มีราคา
                                                        package_url = package_url
                                                                        # ตรวจสอบความถูกต้องของ URL และดาวน์โหลด QR Code
                                                        response = requests.get(package_url)
                                                        if response.status_code == 200:# ดาวน์โหลด QR Code และแสดงผล
                                                                image = Image.open(BytesIO(response.content))
                                                                if image.mode != 'L':
                                                                        image = image.convert('L')
                                                                img_np = np.array(image)
                                                                qr_decoder = cv2.QRCodeDetector()
                                                                val, pts, qr_code = qr_decoder.detectAndDecode(img_np)
                                                                print("Decoded value from the QR code:", val)
                                                                image = image.resize((int(image.width * 0.75), int(image.height * 0.75)))
                                                                img_tk = ImageTk.PhotoImage(image)
                                                                label = Label(pay, image=img_tk)
                                                                label.image = img_tk
                                                                label.place(x=730,y=150)
                                                                
                                                                pay_image = Image.open(r"D:\python\sed_bt.png") #ปุ่มเสร็จสิ้น
                                                                pay_image = pay_image.resize((110, 50))  
                                                                pay_photo = ImageTk.PhotoImage(pay_image)
                                                                pay_But= Button(pay,image=pay_photo, text="สรุป",bg='#fcdbe2', command=finished,cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdbe2')
                                                                pay_But.photo = pay_photo
                                                                pay_But.place(x=600, y=385)

                                                                back_image = Image.open(r"D:\python\back01_bt.png") #ปุ่มย้อนกลับ
                                                                back_image = back_image.resize((100, 60))  
                                                                back_photo = ImageTk.PhotoImage(back_image)
                                                                back_But= Button(pay,image=back_photo, text="ย้อนกลับ",bg='#fcdbe2',command=lambda:(pay.destroy()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdbe2')
                                                                back_But.photo = back_photo
                                                                back_But.place(x=500, y=380)            
                                                        else:
                                                                print("Failed to download the image. HTTP status code:", response.status_code)
                                                                    
                        name_label = Label(cf_details, text=f'{logged_in_name} {logged_in_lastname}',bg='#ffffff',font=("DB Helvethaica X", 15))
                        name_label.place(x=70,y=98)
                        
                        address_entry = Entry(cf_details,width=20,font=("DB Helvethaica X", 10),cursor="hand2",borderwidth=0, highlightthickness=0)
                        address_entry.place(x=350, y=275)

                        current_date = datetime.now().strftime('%Y-%m-%d')
                        cal = Calendar(cf_details, selectmode="day", date_pattern='yyyy-mm-dd', date=current_date)
                        cal.place(x=245, y=335)
                        
                        package_options = ["Package 1", "Package 2", "Package 3"]
                        package_var = StringVar()
                        package_var.set(package_options[0])
                        package_menu = OptionMenu(cf_details, package_var, *package_options)
                        package_menu.place(x=280, y=200)
                                
                        #ปุ่มบันทึก
                        confirm_image = Image.open(r"D:\python\save_1_bt.png")
                        confirm_image = confirm_image.resize((100, 60))  # ปรับขนาดปุ่ม
                        confirm_photo = ImageTk.PhotoImage(confirm_image)
                        confirm_But= Button(cf_details,image=confirm_photo,bg='#fcdce2',fg='black',command=lambda:(confirm_booking()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdce2')
                        confirm_But.photo = confirm_photo
                        confirm_But.place(x=600, y=400)
                        
                        
                        #ปุ่มย้อนกลับ
                        back_image = Image.open(r"D:\python\back01_bt.png")
                        back_image = back_image.resize((100, 60))  # ปรับขนาดปุ่ม
                        back_photo = ImageTk.PhotoImage(back_image)
                        back_But= Button(cf_details,image=back_photo,bg='#fcdce2',fg='black',command=lambda:(cf_details.destroy(),packages()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdce2')
                        back_But.photo = back_photo
                        back_But.place(x=510, y=400)
                        
                        #text
                        result_label = Label(cf_details, text="",bg='#e171ac',font=("DB Helvethaica X", 10),fg='white')
                        result_label.place(x=520,y=460) 
                                        
                #ปุ่มดำเนินการจอง
                package1_image = Image.open(r"D:\python\book_bt.png")
                package1_image = package1_image.resize((100, 60))  # ปรับขนาดปุ่ม
                package1_photo = ImageTk.PhotoImage(package1_image)
                package1_But= Button(packwindow,image=package1_photo,bg='#fcdbe2',fg='black',command=lambda:(packwindow.destroy(),cf(logged_in_name, logged_in_lastname, show_email,show_tel)),cursor="hand2", borderwidth=0, highlightthickness=0,activebackground='#fcdbe2')
                package1_But.photo = package1_photo
                package1_But.place(x=265,y=473)
                
                #ปุ่มเช็คตาราง
                check_image = Image.open(r"D:\python\checktable_bt.png")
                check_image = check_image.resize((110, 60))  # ปรับขนาดปุ่ม
                check_photo = ImageTk.PhotoImage(check_image)
                check_But= Button(packwindow,image=check_photo,bg='#fcdbe2',fg='black',command=Tabletime,cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdbe2')
                check_But.photo = check_photo
                check_But.place(x=75,y=545)
                
                #ปุ่มกลับ
                back_image = Image.open(r"D:\python\back-icon.png")
                back_image = back_image.resize((50, 40))  # ปรับขนาดปุ่ม
                back_photo = ImageTk.PhotoImage(back_image)
                back_But= Button(packwindow,image=back_photo, text="ย้อนกลับ",bg='#e171ac',fg='black',command=lambda:(packwindow.destroy(),login()),cursor="hand2", font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,activebackground='#e171ac')
                back_But.photo = back_photo
                back_But.place(x=15, y=610)           
        
                
        def admin():
                admin_window = Toplevel(root)
                admin_window.title("Admin")
                admin_window.geometry('1000x650+275+60')
                admin_window.resizable(False,False)
                
                def on_vertical_scroll(*args):
                        tree.yview(*args)
                tree_label = tk.Label(admin_window, text="ข้อมูล users ทั้งหมด", font=("DB Helvethaica X", 14))
                tree_label.pack()
                frame = ttk.Frame(admin_window)
                frame.pack()
                tree = ttk.Treeview(frame,columns=("id","name","lastname","tel","email","password"))
                tree.heading("id",text="id")
                tree.heading("name",text="ชื่อ")
                tree.heading("lastname",text="นามสกุล")
                tree.heading("tel",text="เบอร์")
                tree.heading("email",text="อีเมล")
                tree.heading("password",text="รหัส")
                tree.column("id",anchor="center",width=60)
                tree.column("name",anchor="center",width=125)
                tree.column("lastname",anchor="center",width=125)
                tree.column("tel",anchor="center",width=110)
                tree.column("email",anchor="center",width=150)
                tree.column("password",anchor="center",width=100)
                tree.column("#0",width=0,stretch=NO)
                style = ttk.Style()
                style.configure("Treeview.Heading",font = ("DB Helvethaica X",12))
                style.configure("Treeview", font=("DB Helvethaica X", 12))
                conn = sqlite3.connect("registers.db")
                c = conn.cursor()
                c.execute("SELECT * FROM users ")
                result = c.fetchall()
                for x in result :
                        tree.insert("","end",values=x)
                vscrollbar = ttk.Scrollbar(frame, orient="vertical", command=on_vertical_scroll)
                vscrollbar.pack(side="right", fill="y")
                tree.config(yscrollcommand=vscrollbar.set)
                tree.pack(fill="both", expand=True)
                def on_vertical_scroll(*args):
                        tree.yview(*args) 
                tree_label = tk.Label(admin_window, text="ข้อมูลการจอง", font=("DB Helvethaica X", 14))
                tree_label.pack()
                frame1 = ttk.Frame(admin_window)
                frame1.pack()
                tree = ttk.Treeview(frame1,columns=("id","email","package","booking_date","address","status"))
                tree.heading("id",text="")
                tree.heading("email",text="อีเมลล์")
                tree.heading("package",text="แพ็คเกต")
                tree.heading("booking_date",text="วันที่จอง")
                tree.heading("address",text="สถานที่จัดงาน")
                tree.heading("status",text="สถานะ")
                tree.column("id",anchor="center",width=60)
                tree.column("email",anchor="center",width=150)
                tree.column("package",anchor="center",width=100)
                tree.column("booking_date",anchor="center",width=100)
                tree.column("address",anchor="center",width=150)
                tree.column("status",anchor="center",width=130)
                tree.column("#0",width=0,stretch=NO)
                
                style = ttk.Style()
                style.configure("Treeview.Heading",font = ("DB Helvethaica X", 12))
                style.configure("Treeview", font=("DB Helvethaica X", 12))
                conn = sqlite3.connect("registers.db")
                c = conn.cursor()
                c.execute("SELECT * FROM booking ")
                result = c.fetchall()
                for x in result :
                        tree.insert("", "end", values=(x[0],x[1], x[2], x[3], x[7], x[8]))
                vscrollbar = ttk.Scrollbar(frame1, orient="vertical", command=on_vertical_scroll)
                vscrollbar.pack(side="right", fill="y")
                tree.config(yscrollcommand=vscrollbar.set)
                tree.pack(fill="both", expand=True)
                def delete_booking() :
                        conn = sqlite3.connect('registers.db')
                        c = conn.cursor()
                        c.execute("DELETE FROM data WHERE status = 'เสร็จสิ้น'")
                        conn.commit()
                        conn.close()
                edit_image = Image.open(r"D:\python\redata_bt.png")
                edit_image = edit_image.resize((110, 40))  # ปรับขนาดปุ่ม
                edit_photo = ImageTk.PhotoImage(edit_image)
                edit_But= Button(admin_window,image=edit_photo,bg='#e171ac',command=lambda:(update(),admin_window.destroy()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#e171ac')
                edit_But.photo = edit_photo
                edit_But.place(x=400,y=550) 
        
                clear_image = Image.open(r"D:\python\delete_bt.png")
                clear_image = clear_image.resize((110, 40))  # ปรับขนาดปุ่ม
                clear_photo = ImageTk.PhotoImage(clear_image)
                clear_But= Button(admin_window,image=clear_photo, bg='#e171ac',command=lambda: (delete_booking()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#e171ac')
                clear_But.photo = clear_photo
                clear_But.place(x=500,y=550) 
                
                 
                sum_image = Image.open(r"D:\python\conclude_bt.png")
                sum_image = sum_image.resize((110, 40))  # ปรับขนาดปุ่ม
                sum_photo = ImageTk.PhotoImage(sum_image)
                sum_But= Button(admin_window,image=sum_photo,bg='#e171ac',command=lambda:(admin_window.destroy(),show_sum()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#e171ac')
                sum_But.photo = sum_photo
                sum_But.place(x=600, y=550)

                back_image = Image.open(r"D:\python\back2_bt.png")
                back_image = back_image.resize((110, 40))  # ปรับขนาดปุ่ม
                back_photo = ImageTk.PhotoImage(back_image)
                back_But= Button(admin_window,image=back_photo, text="ย้อนกลับ",bg='#e171ac',command=lambda:(admin_window.destroy(),login()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#e171ac')
                back_But.photo = back_photo
                back_But.place(x=300,y=550) 
        def update():
                admin_win= Toplevel(root)
                admin_win.title("Admin Update")
                admin_win.geometry('1000x650+275+60')
                admin_win.resizable(False,False)
                bg_image_admin = Image.open(r"D:\python\admin_user (1).png")
                bg_photo_admin = ImageTk.PhotoImage(bg_image_admin)
                bg_label_admin = Label(admin_win,image=bg_photo_admin)
                bg_label_admin.photo = bg_photo_admin # เก็บ reference รูปภาพ
                bg_label_admin.pack(fill="both", expand=True)
                def edit():
                        email = email_entry.get()    
                        conn = sqlite3.connect('registers.db')
                        c = conn.cursor() 
                        c.execute("SELECT name FROM users WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                nentry=Entry(admin_win,textvariable=name,width = 13,borderwidth=0,font=("DB Helvethaica X", 10))
                                nentry.insert(0,x)
                                nentry.place(x=137 ,y=238)
                        c.execute("SELECT lastname FROM users WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                lnameentry=Entry(admin_win,textvariable=lname,width = 13,borderwidth=0,font=("DB Helvethaica X", 10))
                                lnameentry.insert(0,x)
                                lnameentry.place(x=513 ,y=238)
                        c.execute("SELECT tel FROM users WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                telentry=Entry(admin_win,textvariable=tel,width = 13,borderwidth=0,font=("DB Helvethaica X", 10))
                                telentry.insert(0,x)
                                telentry.place(x=545 ,y=290)
                        c.execute("SELECT email FROM users WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                eentry=Entry(admin_win,textvariable=e,width = 25,borderwidth=0,font=("DB Helvethaica X", 10))
                                eentry.insert(0,x)
                                eentry.place(x=171 ,y=290)
                        c.execute("SELECT password FROM users WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                pwentry=Entry(admin_win,textvariable=pw,width = 13,borderwidth=0,font=("DB Helvethaica X", 10))
                                pwentry.insert(0,x)
                                pwentry.place(x=190 ,y=342) 
                        c.execute("SELECT email FROM booking WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                eentry=Entry(admin_win,textvariable=e,width = 25,borderwidth=0,font=("DB Helvethaica X", 10))
                                eentry.insert(0,x)
                                eentry.place(x=171 ,y=290)
                        c.execute("SELECT package FROM booking WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                package = x[0]  
                                packentry = Entry(admin_win, width=13, borderwidth=0, font=("DB Helvethaica X", 10))
                                packentry.insert(0, package)
                                packentry.place(x=185,y=475)
                        c.execute("SELECT booking_date FROM booking WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                dateentry=Entry(admin_win,textvariable=date,width = 13,borderwidth=0,font=("DB Helvethaica X", 10))
                                dateentry.insert(0,x)
                                dateentry.place(x=515,y=477) 
                        c.execute("SELECT address FROM booking WHERE email=?", (email,))
                        booked = c.fetchall()
                        for x in booked :
                                addressentry = Entry(admin_win, width=13, borderwidth=0, font=("DB Helvethaica X", 11))
                                addressentry.insert(0, x)
                                addressentry.place(x=220,y=530)
                        c.execute("SELECT status FROM booking WHERE email=?", (email,))
                        booked = c.fetchall()
                        status_var = StringVar()
                        status_options = ["การจองสำเร็จ", "เสร็จสิ้น"]
                        status_var.set("ระบุสถานะ")
                        status_menu = OptionMenu(admin_win, status_var, *status_options)
                        status_menu.place(x=505, y=525)
                        def saveedit():
                                n1 = nentry.get()
                                lname = lnameentry.get()
                                tel = telentry.get()
                                e = eentry.get()
                                pw = pwentry.get()
                                email = email_entry.get()
                                conn = sqlite3.connect('registers.db')
                                c = conn.cursor()
                                data=(n1,lname,tel,e,pw,email)
                                c.execute('''UPDATE users SET name=?,lastname=?,tel=?,email=?,password=?  WHERE email=?''',data)
                                conn.commit()
                                conn.close()
                        def savestatusedit():
                                e=eentry.get()
                                pack = packentry.get()
                                address = addressentry.get()        
                                date =dateentry.get()
                                email = email_entry.get()
                                conn = sqlite3.connect('registers.db')
                                c = conn.cursor()
                                data1=(e,pack,address,date,email)
                                c.execute('''UPDATE booking SET email=?, package=?, address=?, booking_date=? WHERE email=?''', data1)
                                conn.commit()
                                conn.close()
                        def statusup():
                                status=status_var.get()
                                conn = sqlite3.connect('registers.db')
                                c = conn.cursor()
                                c.execute('''UPDATE booking SET status=? WHERE email=?''', (status, email))
                                c.execute('''UPDATE data SET status=? WHERE email=?''', (status, email))
                                conn.commit()
                                conn.close()
                        def clear_booking():
                                conn = sqlite3.connect('registers.db')
                                c = conn.cursor()
                                c.execute("DELETE FROM booking WHERE email=? ",(email,))
                                conn.commit()
                                conn.close()
                        del_image = Image.open(r"D:\python\cleardata_bt.png")
                        del_image = del_image.resize((110, 40))  # ปรับขนาดปุ่ม
                        del_photo = ImageTk.PhotoImage(del_image)
                        del_But= Button(admin_win,image=del_photo,bg='#e171ac',fg='black', command=lambda: (clear_booking(),admin_win.destroy(),admin()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#e171ac')
                        del_But.photo = del_photo
                        del_But.place(x=750, y=495)

                        save_image = Image.open(r"D:\python\save_bt.png")
                        save_image = save_image.resize((110, 40))  # ปรับขนาดปุ่ม
                        save_photo = ImageTk.PhotoImage(save_image)
                        save_But= Button(admin_win,image=save_photo, bg='#e171ac',fg='black',command=lambda: (saveedit(),savestatusedit(),admin_win.destroy(),admin()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#e171ac')
                        save_But.photo = save_photo
                        save_But.place(x=750, y=455)

                        save_But= Button(admin_win,text='บันทึกสถานะ',bg='#e171ac',fg='black',command=lambda: (statusup()),cursor="hand2",activebackground='#e171ac')
                        save_But.place(x=650, y=527)
        

                email_entry = Entry(admin_win,width=25, font=("DB Helvethaica X", 12),borderwidth=0, highlightthickness=0)
                email_entry.place(x=110, y=95)

                serch_image = Image.open(r"D:\python\serch-icon.png")
                serch_image = serch_image.resize((50, 50))  
                serch_photo = ImageTk.PhotoImage(serch_image)
                serch_But = Button(admin_win,image=serch_photo, bg='#fcd3e2', command=edit, font=("DB Helvethaica X", 10),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcd3e2')
                serch_But.photo = serch_photo
                serch_But.place(x=375, y=80)

                back_image = Image.open(r"D:\python\back-icon.png")
                back_image = back_image.resize((50, 40))  # ปรับขนาดปุ่ม
                back_photo = ImageTk.PhotoImage(back_image)
                back_But= Button(admin_win,image=back_photo,bg='#e171ac',fg='black',command=lambda:(admin_win.destroy(),admin()),cursor="hand2", font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,activebackground='#e171ac')
                back_But.photo = back_photo
                back_But.place(x=920, y=10)
        def summary():
                conn = sqlite3.connect('registers.db')
                c = conn.cursor()
                c.execute("SELECT booking_date, package FROM booking")
                bookings = c.fetchall()
                amount = {} # สร้างพจนานุกรมเพื่อเก็บยอดเงินรายเดือน
                # นับยอดเงินในแต่ละเดือน
                for booking in bookings:
                        booking_date = booking[0]#ดึงวันที่จองจาก tuple ใน bookings
                        year, month, _ = map(int, booking_date.split('-'))
                        package = booking[1]
                        package_prices = {"Package 1": 4000, "Package 2": 9000, "Package 3": 18000}
                        income = package_prices.get(package)##ดึงราคาของแพ็คเกจที่ถูกจองและเก็บไว้ในตัวแปร 
                        # เพิ่มยอดเงินในแต่ละเดือน##ตรวจสอบว่าข้อมูลรายได้สำหรับเดือนและปีที่กำลังพิจารณาอยู่ในamount
                        if (year, month) in amount:
                                amount[(year, month)] += income
                        else:
                                amount[(year, month)] = income
                conn.close()
                return amount

        def show_sum():
                result_window = Toplevel(root)
                result_window.title("สรุปยอดเงินรายเดือน")
                result_window.geometry('1000x650+275+60')
                result_window.resizable(False,False)

                canvas = Canvas(result_window, width=1000, height=650)
                canvas.pack()
                bg_image = Image.open(r"D:\python\Sarub_bg (1).png")
                bg_photo = ImageTk.PhotoImage(bg_image)
                canvas.create_image(0, 0, anchor=NW, image=bg_photo)
                canvas.image = bg_photo

                frame = Frame(canvas)  # Create a frame as a child of the canvas
                canvas.create_window((200,170), window=frame, anchor=NW)  # Place the frame on the canvas
                tree = ttk.Treeview(frame, columns=("package", "booking_date", "address", "status"))
                tree.heading("package", text="แพ็คเกต")
                tree.heading("booking_date", text="วันที่จอง")
                tree.heading("address", text="สถานที่จัดงาน")
                tree.heading("status", text="สถานะ")
                tree.column("package", anchor="center", width=100)
                tree.column("booking_date", anchor="center", width=100)
                tree.column("address", anchor="center", width=150)
                tree.column("status", anchor="center", width=130)
                tree.column("#0", width=0, stretch=NO)
                style = ttk.Style()
                style.configure("Treeview.Heading", font=("DB Helvethaica X", 12))
                style.configure("Treeview", font=("DB Helvethaica X", 12))         
                tree.pack(pady=10)                                      
                def select_show():
                        selected_month = month_var.get()
                        selected_year = year_var.get()
                        if selected_month != "เดือน" and selected_year != "ปี":
                                selected_month = int(selected_month)
                                selected_year = int(selected_year)

                        if selected_month != "เดือน" and selected_year != "ปี":
                                month_total = summary()
                                result_label.config(text="สรุปยอดเงินรายเดือน")
                                
                                for item in tree.get_children():
                                        tree.delete(item)

                                conn = sqlite3.connect("registers.db")
                                c = conn.cursor()
                                c.execute("SELECT * FROM booking WHERE month=? AND year=?", (selected_month, selected_year))
                                result = c.fetchall()
                                
                                for x in result:
                                        tree.insert("", "end", values=(x[2], x[3], x[7], x[8]))

                                label_text = f"รวม : {month_total.get((selected_year, selected_month), 0)} บาท"
                                result_label.config(text=label_text)
                        else:
                                result_label.config(text="กรุณาเลือกเดือนและปี")

                month_var = StringVar()                        
                year_var = StringVar()
                month_options = ["01", "02","03","04","05","06","07","08","09","10","11","12"]
                month_var.set("ระบุเดือน")
                month_menu = OptionMenu(result_window, month_var, *month_options)
                month_menu.place(x=750,y=180)
               
                
                year_options = ["2023","2024","2025","2026","2027","2028","2029","2030","2031","2032","2033"]
                year_var.set("ระบุปี")
                year_menu = OptionMenu(result_window, year_var, *year_options)
                year_menu.place(x=750,y=210)
                

                # เพิ่มปุ่ม "ดูรายการสรุปยอด"
                show_image = Image.open(r"D:\python\Total-summary_bt.png")
                show_image = show_image.resize((120, 60))  # ปรับขนาดปุ่ม
                show_photo = ImageTk.PhotoImage(show_image)
                show_But= Button(result_window,image=show_photo, bg='#fcdbe2',command=lambda:(select_show()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdbe2')
                show_But.photo = show_photo
                show_But.place(x=750, y=260)  

                result_label = Label(result_window, text="", font=("DB Helvethaica X", 15),bg='#fcdbe2',fg='black')
                result_label.place(x=750, y=390)
                
                back_image = Image.open(r"D:\python\back01_bt.png")
                back_image = back_image.resize((110, 60))  # ปรับขนาดปุ่ม
                back_photo = ImageTk.PhotoImage(back_image)
                back_But= Button(result_window,image=back_photo, text="ย้อนกลับ",bg='#fcdbe2',command=lambda:(result_window.destroy(),admin()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#fcdbe2')
                back_But.photo = back_photo
                back_But.place(x=750, y=310)  
        
        email_entry = Entry(login_window,width=20,font=("DB Helvethaica X", 10),borderwidth=0, highlightthickness=0,cursor="hand2")
        email_entry.place(x=400,y=173)
        password_entry = Entry(login_window, show="*",font=("DB Helvethaica X", 10),width=18,borderwidth=0, highlightthickness=0,cursor="hand2")
        password_entry.place(x=428,y=213)

        login_image = Image.open(r"D:\python\login_bt.png")
        login_image = login_image.resize((95, 37))  # ปรับขนาดปุ่ม
        login_photo = ImageTk.PhotoImage(login_image)
        login_But = Button(login_window,image=login_photo, text="ค้นหา",bg="#ffffff", command=authenticate,cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#ffffff')
        login_But.photo = login_photo
        login_But.place(x=350, y=250)

        forget_image = Image.open(r"D:\python\resetpass_bt.png")
        forget_image = forget_image.resize((95, 36))  # ปรับขนาดปุ่ม
        forget_photo = ImageTk.PhotoImage(forget_image)
        forget_But = Button( login_window,image=forget_photo ,text="ลืมรหัสผ่าน",bg="#ffffff",command=repass,cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#ffffff')
        forget_But.photo = forget_photo
        forget_But.place(x=460,y=250)

        back_image = Image.open(r"D:\python\back-icon.png")
        back_image = back_image.resize((50, 40))  # ปรับขนาดปุ่ม
        back_photo = ImageTk.PhotoImage(back_image)
        back_But= Button(login_window,image=back_photo, text="ย้อนกลับ",bg='#ffffff',command=lambda:(login_window.destroy()),cursor="hand2", borderwidth=0, highlightthickness=0,activebackground='#ffffff')
        back_But.photo = back_photo
        back_But.place(x=0,y=0)
        result_label = Label(login_window, text="",bg='#ffffff',fg='black',font=("DB Helvethaica X", 10))
        result_label.place(x=350,y=290)

def contact():
        contact_window = Toplevel(root)
        contact_window.title("Login")
        contact_window.geometry('1000x650+275+60')
        contact_window.resizable(False,False)
        bg_image_ct = Image.open(r"D:\python\contact_bg.png")
        bg_photo_ct = ImageTk.PhotoImage(bg_image_ct)
        bg_label_ct = Label(contact_window, image=bg_photo_ct)
        bg_label_ct.photo = bg_photo_ct  # เก็บ reference รูปภาพ
        bg_label_ct.pack(fill="both", expand=True)
        back_image = Image.open(r"D:\python\back-icon.png")
        back_image = back_image.resize((50, 40))  # ปรับขนาดปุ่ม
        back_photo = ImageTk.PhotoImage(back_image)
        back_But= Button(contact_window,image=back_photo, text="ย้อนกลับ",bg='#e171ac',command=lambda:(contact_window.destroy()),cursor="hand2",borderwidth=0, highlightthickness=0,activebackground='#e171ac')
        back_But.photo = back_photo
        back_But.place(x=15, y=610)
   
   
root = Tk()
root.title('Photo Booking')
bg_image = Image.open(r"D:\python\main_bg.png")
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = Label(image=bg_photo)
bg_label.photo = bg_photo  # เก็บ reference รูปภาพ
bg_label.pack(fill="both", expand=True)
register_button = Button(root, text='Sign Up',bg='#e171ac',fg='white', command=Register,borderwidth=0, highlightthickness=0,cursor="hand2",activebackground='#e171ac')
register_button.config(font=("DB Helvethaica X", 12,'bold'))
register_button.place(x=775,y=14)
login_button = Button(root, text='Login', bg='#e171ac',fg='white', font=45, command=login,borderwidth=0, highlightthickness=0,cursor="hand2",activebackground='#e171ac')
login_button.config(font=("DB Helvethaica X", 12,'bold'))
login_button.place(x=715,y=15)
contact_button = Button(root, text='Contact Us', bg='#e171ac',fg='white', font=45,command=contact,borderwidth=0, highlightthickness=0,cursor="hand2",activebackground='#e171ac')
contact_button.config(font=("DB Helvethaica X", 12,'bold'))
contact_button.place(x=855,y=15)
close_image = Image.open(r"D:\python\rootQ.png")
close_image = close_image.resize((40, 40))  # ปรับขนาดปุ่ม
close_photo = ImageTk.PhotoImage(close_image)
close_button = Button(root, image=close_photo, bg='#e171ac', command=root.quit,borderwidth=0, highlightthickness=0,cursor="hand2",activebackground='#e171ac')
close_button.photo = close_photo
close_button.place(x=950, y=7)
root.geometry('1000x650+275+60')
root.resizable(False,False)
root.mainloop()
