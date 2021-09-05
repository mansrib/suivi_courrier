import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as msg
from tkinter.ttk import Treeview
from tkcalendar import DateEntry
import time
from datetime import datetime
import pymysql
import os
import cv2
from PIL import Image
from PIL import ImageTk

#--------crer page login----------------

log=Tk()
log.title("منظومة متابعة البريد")
log.geometry("1366x768")
log.resizable(False,False)
log.configure(bg="#BCF7F7")
icon=tkinter.PhotoImage(file="logo-courrier.png")
log.call('wm','iconphoto',log._w,icon)
def make_label(master, x, y, w, h, img, *args, **kwargs):
    f = Frame(master, height = h, width = w)
    f.pack_propagate(0)
    f.place(x = x, y = y)
    labe = Label(f, image = img, *args, **kwargs)
    labe.pack(fill = BOTH, expand = 1)
    return labe
name_user_var=StringVar()
password_var=StringVar()
fram_log=Frame(log, bg="#D090F5")
fram_log.place(x=500, y=100, width=400, height=320)
img = ImageTk.PhotoImage(Image.open('12.png'))
make_label(fram_log, 0, 0, 400, 160, img, bg="#B533FF")
def login_func():
    if name_user_var.get() == "" or password_var.get() == "":
        msg.showerror("خطأ!", "يجب إدخال إسم المستعمل وكلمة المرور", parent=fram_log)
    else:
        try:
            connection = pymysql.connect(host="localhost", user="root", password="", database="courrier")
            cur = connection.cursor()
            cur.execute("select * from users where name=%s and password=%s",
                        (name_user_var.get(), password_var.get()))
            row = cur.fetchone()
            if row == None:
                msg.showerror("خطأ!", "خطأ في إسم المستعمل أو كلمة المرور", parent=fram_log)
            else:
                def aff_dep():
                    # --------crer window----------------
                    root = Tk()
                    root.title("منظومة متابعة البريد")
                    root.geometry("1366x768")
                    root.resizable(False , False)
                    root.configure(bg="#BCF7F7")
                    icon = tkinter.PhotoImage(file="logo-courrier.png")
                    root.call('wm' , 'iconphoto' , root._w , icon)
                    titre_app = Label(root , text=" البريد الوارد" , font=("Arial" , 22 , "bold") , bg="#0A41D4" ,
                                      fg="white")
                    titre_app.pack(fill=X)

                    app_date = datetime.now()
                    x_date = app_date.strftime('%Y-%m-%d')
                    # x_time = app_date.strftime('%H:%M:%S')

                    date_lbl = Label(root , text=x_date , bg="#0A41D4" , fg='#FFC300' , font=('Wide Latin' , 10))
                    date_lbl.place(x=1200 , y=10)

                    def app_time():
                        string = time.strftime('%H:%M:%S %p')
                        time_lbl.config(text=string)
                        time_lbl.after(1000 , app_time)

                    time_lbl = Label(root , bg='#0A41D4' , fg='#FFC300' , font=('Wide Latin' , 10))
                    time_lbl.place(x=70 , y=10)
                    app_time()

                    def fetech_all():
                        conn1 = pymysql.connect(host="localhost" , user="root" , password="" , database="courrier")
                        curr = conn1.cursor()
                        curr.execute(
                            'select image,sujet_doc,date_doc,source_doc,num_doc,clas_doc,type_doc,date_enreg,num_enreg from arrivee')
                        rows = curr.fetchall()
                        if len(rows) != 0:
                            courrier_table.delete(*courrier_table.get_children())
                            for row in rows:
                                courrier_table.insert('' , '0' , values=row)
                            conn1.commit()
                            conn1.close()

                    # --------vider les champs----------------

                    # --------declaration variable----------------
                    sujet_doc_var = StringVar()
                    date_doc_var = StringVar()
                    source_doc_var = StringVar()
                    num_doc_var = StringVar()
                    clas_doc_var = StringVar()
                    type_doc_var = StringVar()
                    date_enreg_var = StringVar()
                    num_enreg_var = StringVar()
                    rech_var = StringVar()
                    sujet_rech_var = StringVar()

                    def incr():
                        conn = pymysql.connect(host="localhost" , user="root" , password="" , database="courrier")
                        curr = conn.cursor()
                        curr.execute("select num_enreg from arrivee")
                        rows = curr.rowcount
                        num_enreg_var.set(rows + 1)
                        conn.close()

                    incr()

                    def recherche():
                        conn = pymysql.connect(host="localhost" , user="root" , password="" , database="courrier")
                        curr = conn.cursor()
                        curr.execute(
                            "select image,sujet_doc,date_doc,source_doc,num_doc,clas_doc,type_doc,date_enreg,num_enreg from arrivee where " +
                            str(rech_var.get()) + " LIKE '%" + str(sujet_rech_var.get()) + "%'")
                        rows = curr.fetchall()
                        if len(rows) != 0:
                            courrier_table.delete(*courrier_table.get_children())
                            for row in rows:
                                courrier_table.insert('' , '0' , values=row)
                            conn.commit()
                            conn.close()

                    # --------selectionee et afficher image----------------
                    img = ''
                    t1 = StringVar()

                    def sel_im():
                        global img
                        fln = filedialog.askopenfilename(initialdir=os.getcwd() , title="مصدر الصور" , filetypes=(
                            ("image jpg" , "*.jpg") , ("image png" , "*.png") , ("tout types" , "*.*")))
                        t1.set(fln)
                        img = cv2.imread(fln , cv2.IMREAD_UNCHANGED)

                    def Aff_im():
                        im = Image.open(t1.get())
                        im.show()
                        # tt=cv2.imread(t1.get(),cv2.IMREAD_UNCHANGED)
                        # cv2.imshow("photo",tt)
                        # cv2.waitkey(0)
                        # cv2.destroyAllwindows()

                    # --------creation des frames----------------
                    fram_manage = Frame(root , bg="white")
                    fram_manage.place(x=1060 , y=40 , width=305 , height=450)

                    fram_boutton = Frame(root , bg="white")
                    fram_boutton.place(x=1060 , y=491 , width=305 , height=253)

                    fram_rech = Frame(root , bg="white")
                    fram_rech.place(x=0 , y=40 , width=1059 , height=50)

                    fram_don = Frame(root , bg="white")
                    fram_don.place(x=0 , y=91 , width=1059 , height=653)

                    # --------conn et ajout----------------
                    def focsel(event):
                        cursor_row = courrier_table.focus()
                        contents = courrier_table.item(cursor_row)
                        row = contents['values']
                        t1.set(row[0])
                        sujet_doc_var.set(row[1])
                        date_doc_var.set(row[2])
                        source_doc_var.set(row[3])
                        num_doc_var.set(row[4])
                        clas_doc_var.set(row[5])
                        type_doc_var.set(row[6])
                        date_enreg_var.set(row[7])
                        num_enreg_var.set(row[8])

                    def Ajout_doc():
                        # -if num_enreg_var== '' or date_enreg_var=="" or type_doc_var=="" or clas_doc_var=="" or num_doc_var=="" or source_doc_var=="" or date_doc_var=="" or sujet_doc_var=="":
                        # -  msg.showwarning('معطيات ناقصة', 'الرجاء تعمير جميع المعطيات')
                        # -else:
                        try:
                            conn = pymysql.connect(host="localhost" , user="root" , password="" , database="courrier")
                            curr = conn.cursor()
                            curr.execute(
                                'insert into arrivee(image,sujet_doc,date_doc,source_doc,num_doc,clas_doc,type_doc,date_enreg,num_enreg) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)' ,
                                (
                                    sujet_doc_var.get() ,
                                    date_doc_var.get() ,
                                    source_doc_var.get() ,
                                    num_doc_var.get() ,
                                    clas_doc_var.get() ,
                                    type_doc_var.get() ,
                                    date_enreg_var.get() ,
                                    num_enreg_var.get() ,
                                    t1.get()
                                ))

                            conn.commit()
                            claer()
                            fetech_all()
                            msg.showinfo("إضافة معطيات" , "تمت إضافة البريد بنجاح")
                            incr()
                            conn.close()

                        except:
                            msg.showerror("خطأ في الإتصال" , "لا يمكن تحقيق الإتصال بقاعدة البيانات")

                    def updattecour():
                        conn = pymysql.connect(host="localhost" , user="root" , password="" , database="courrier")
                        curr = conn.cursor()
                        curr.execute(
                            "update arrivee set image=%s,sujet_doc=%s,date_doc=%s,source_doc=%s,num_doc=%s,clas_doc=%s,type_doc=%s,date_enreg=%s where num_enreg=%s" ,
                            (
                                t1.get() ,
                                sujet_doc_var.get() ,
                                date_doc_var.get() ,
                                source_doc_var.get() ,
                                num_doc_var.get() ,
                                clas_doc_var.get() ,
                                type_doc_var.get() ,
                                date_enreg_var.get() ,
                                num_enreg_var.get()
                            ))

                        conn.commit()
                        claer()
                        fetech_all()
                        msg.showinfo("تحيين معطيات" , "تم تحيين البريد بنجاح")
                        incr()
                        conn.close()

                    def dell():
                        delMessage = msg.askquestion("حذف معطيات" , "هل أنت متأكد من حذف البيانات؟ ")
                        if delMessage == 'yes':
                            conn = pymysql.connect(host="localhost" , user="root" , password="" , database="courrier")
                            curr = conn.cursor()
                            curr.execute(
                                "delete from arrivee where num_enreg=%s" ,
                                (

                                    num_enreg_var.get()
                                ))

                            conn.commit()
                            claer()
                            fetech_all()
                            msg.showinfo("حذف معطيات" , "تم حذف البريد بنجاح")
                            incr()
                            conn.close()

                    def claer():
                        sujet_doc_var.set('')
                        date_doc_var.set('')
                        source_doc_var.set('')
                        num_doc_var.set('')
                        clas_doc_var.set('')
                        type_doc_var.set('')
                        date_enreg_var.set('')
                        num_enreg_var.set('')
                        t1.set('')
                        incr()

                    # --------crer champs de saisie----------------

                    titre_cour = Label(fram_manage , text="معطيات البريد" , font=("Arial" , 16 , "bold") ,
                                       bg="#9814A5" ,
                                       fg="white")
                    titre_cour.place(x=0 , y=1 , width=305 , height=30)

                    Label(fram_manage , text=":رقم التسجيل" , font=("Arial" , 14 , "bold") , bg="white" ,
                          fg="#121483").place(
                        x=180 , y=35 , width=100 , height=30)
                    num_enreg = Entry(fram_manage , stat="readonly" , textvariable=num_enreg_var , bd="2" ,
                                      justify="right").place(x=80 , y=35 , width=100 , height=30)
                    Label(fram_manage , text=":تاريخ التسجيل" , font=("Arial" , 14 , "bold") , bg="white" ,
                          fg="#121483").place(
                        x=190 , y=75 , width=100 , height=30)
                    dat_enreg = DateEntry(fram_manage , stat="readonly" , textvariable=date_enreg_var , bd="2" ,
                                          justify="right" , date_pattern='y/mm/dd').place(x=50 , y=75 , width=130 ,
                                                                                          height=30)

                    Label(fram_manage , text=":نوع الوثيقة" , font=("Arial" , 14 , "bold") , bg="white" ,
                          fg="#121483").place(
                        x=180 , y=115 , width=100 , height=30)
                    typ_enreg = ttk.Combobox(fram_manage , stat="readonly" , textvariable=type_doc_var ,
                                             justify="right")
                    typ_enreg["value"] = (
                    "برقية" , "أمر إداري" , "مراسلة" , "مراسلة سريعة" , "فاكس" , "بطالة إتصال" , "إحالة")
                    typ_enreg.current(0)
                    typ_enreg.place(x=40 , y=115 , width=140 , height=30)
                    Label(fram_manage , text=":رقم الوثيقة" , font=("Arial" , 14 , "bold") , bg="white" ,
                          fg="#121483").place(
                        x=180 , y=155 , width=100 , height=30)
                    numdoc_enreg = Entry(fram_manage , textvariable=num_doc_var , bd="2" , justify="right").place(x=90 ,
                                                                                                                  y=155 ,
                                                                                                                  width=100 ,
                                                                                                                  height=30)

                    Label(fram_manage , text=":تصنيف الوثيقة" , font=("Arial" , 14 , "bold") , bg="white" ,
                          fg="#121483").place(
                        x=180 , y=195 , width=110 , height=30)
                    clasdoc_enreg = ttk.Combobox(fram_manage , stat="readonly" , textvariable=clas_doc_var ,
                                                 justify="right")
                    clasdoc_enreg["value"] = ("عادي" , "سري مكتوم" , "سري مطلق" , "نشرة محدودة" , "سري")
                    clasdoc_enreg.current(0)
                    clasdoc_enreg.place(x=90 , y=195 , width=100 , height=30)
                    Label(fram_manage , text=":مصدر الوثيقة" , font=("Arial" , 14 , "bold") , bg="white" ,
                          fg="#121483").place(
                        x=180 , y=235 , width=110 , height=30)
                    sourcedoc_enreg = Entry(fram_manage , textvariable=source_doc_var , bd="2" , justify="right").place(
                        x=90 ,
                        y=235 ,
                        width=100 ,
                        height=30)
                    Label(fram_manage , text=":تاريخ الوثيقة" , font=("Arial" , 14 , "bold") , bg="white" ,
                          fg="#121483").place(
                        x=180 , y=275 , width=110 , height=30)
                    datdoc_enreg = DateEntry(fram_manage , stat="readonly" , textvariable=date_doc_var , bd="2" ,
                                             justify="right" , date_pattern='y/mm/dd').place(x=50 , y=275 , width=140 ,
                                                                                             height=30)
                    Label(fram_manage , text=":موضوع الوثيقة" , font=("Arial" , 14 , "bold") , bg="white" ,
                          fg="#121483").place(
                        x=185 , y=315 , width=110 , height=30)
                    sujetdoc_enreg = Entry(fram_manage , textvariable=sujet_doc_var , bd="2" , justify="right").place(
                        x=5 ,
                        y=315 ,
                        width=180 ,
                        height=30)
                    Label(fram_manage , text=":صورة الوثيقة" , font=("Arial" , 14 , "bold") , fg="#121483" ,
                          bg="white").place(
                        x=185 , y=360 , width=110 , height=30)
                    image_doc = Entry(fram_manage , textvariable=t1 , bd="2" , justify="right").place(x=5 , y=400 ,
                                                                                                      width=290 ,
                                                                                                      height=30)
                    btn_selim = Button(fram_manage , text="إختيار الصورة" , command=sel_im , bg="white" , fg="#121483" ,
                                       font=("Arial" , 12 , "bold"))
                    btn_selim.place(x=100 , y=360 , width=80 , height=30)
                    btn_affim = Button(fram_manage , text="إظهار الصورة" , command=Aff_im , bg="white" , fg="#121483" ,
                                       font=("Arial" , 12 , "bold"))
                    btn_affim.place(x=10 , y=360 , width=80 , height=30)
                    # Checkbutton(fram_manage, text="حضيرة الأفراد", variable = "s1", onvalue = 1, offvalue = 0,bg="white",font=("Arial", 12, "bold")).place(x=130, y=390, width=180, height=30)
                    # Checkbutton(fram_manage, text="حضيرة الإستعلامات",variable = "s3", onvalue = 1, offvalue = 0,bg="white",font=("Arial", 12, "bold")).place(x=0, y=390, width=125, height=30)
                    # Checkbutton(fram_manage, text="حضيرة التخطيط والعمليات",variable = "s2", onvalue = 1, offvalue = 0,bg="white",font=("Arial", 12, "bold")).place(x=130, y=415, width=180, height=30)
                    # Checkbutton(fram_manage, text="حضيرة اللوجستيك",variable = "s4", onvalue = 1, offvalue = 0,bg="white",font=("Arial", 12, "bold")).place(x=0, y=415, width=125, height=30)
                    # --------crer boutton----------------
                    titre_pc = Label(fram_boutton , text="لوحة التحكم" , font=("Arial" , 16 , "bold") , bg="#9814A5" ,
                                     fg="white")
                    titre_pc.place(x=0 , y=2 , width=305 , height=30)
                    btn_ajout = Button(fram_boutton , text="حفظ" , command=Ajout_doc , bg="white" , fg="#121483" ,
                                       font=("Arial" , 14 , "bold"))
                    btn_ajout.place(x=60 , y=45 , width=200 , height=30)
                    btn_maj = Button(fram_boutton , text="تحيين المعطيات" , bg="white" , fg="#4BEC63" ,
                                     font=("Arial" , 14 , "bold") , command=updattecour)
                    btn_maj.place(x=60 , y=85 , width=200 , height=30)
                    btn_del = Button(fram_boutton , text="حذف المعطيات" , bg="white" , fg="#757876" ,
                                     font=("Arial" , 14 , "bold") , command=dell)
                    btn_del.place(x=60 , y=125 , width=200 , height=30)
                    btn_ann = Button(fram_boutton , text="إلغاء" , bg="white" , fg="#E74BEC" ,
                                     font=("Arial" , 14 , "bold") ,
                                     command=claer)
                    btn_ann.place(x=60 , y=165 , width=200 , height=30)
                    btn_exit = Button(fram_boutton , text="غلق البرنامج" , bg="white" , fg="#FF5733" ,
                                      font=("Arial" , 14 , "bold") , command=root.quit)
                    btn_exit.place(x=60 , y=205 , width=200 , height=30)
                    # --------crer moteur de recherche----------------
                    Label(fram_rech , text=":البحث عن وثيقة حسب" , font=("Arial" , 14 , "bold") , bg="white" ,
                          fg="#121483" ,
                          justify="left").place(x=800 , y=10 , width=150 , height=30)
                    rech = ttk.Combobox(fram_rech , stat="readonly" , textvariable=rech_var , justify="right" ,
                                        font=("Arial" , 14))
                    rech["values"] = (
                        "sujet_doc" , "date_doc" , "source_doc" , "num_doc" , "clas_doc" , "type_doc" , "date_enreg" ,
                        "num_enreg")
                    # def list():
                    # conn = pymysql.connect(host="localhost", user="root", password="", database="courrier")
                    # curr = conn.cursor()
                    # curr.execute("select fieled from arrivee")
                    # res=curr.fetchall()
                    # rech["values"]=(res)
                    #  conn.close()
                    # list()
                    rech.current(0)
                    rech.place(x=650 , y=10 , width=150 , height=30)
                    sujet_rech = Entry(fram_rech , textvariable=sujet_rech_var , bd="2" , justify="right" ,
                                       font=("Arial" , 14)).place(x=450 , y=10 , width=180 , height=30)
                    btn_rech = Button(fram_rech , text="بحث" , bg="white" , fg="#FF5733" ,
                                      font=("Arial" , 14 , "bold") ,
                                      command=recherche)
                    btn_rech.place(x=350 , y=10 , width=80 , height=30)
                    # --------conn et afficher les barre de defillement----------------

                    # Treestyle=ttk.Style()
                    # Treestyle.configure("mystyle.Triview", highlightthicknes=0, bd=0)
                    scrol_x = Scrollbar(fram_don , orient=HORIZONTAL)
                    scrol_y = Scrollbar(fram_don , orient=VERTICAL)
                    courrier_table: Treeview = ttk.Treeview(fram_don ,
                                                            columns=(
                                                                "image" , "sujet_doc" , "date_doc" , "source_doc" ,
                                                                "num_doc" ,
                                                                "clas_doc" , "type_doc" , "date_enreg" , "num_enreg") ,
                                                            xscrollcommand=scrol_x.set ,
                                                            yscrollcommand=scrol_y.set)

                    courrier_table.place(x=18 , y=0 , width=1042 , height=635)
                    scrol_x.pack(side=BOTTOM , fill=X)
                    scrol_y.pack(side=LEFT , fill=Y)

                    scrol_x.config(command=courrier_table.xview)
                    scrol_y.config(command=courrier_table.yview)

                    # --------afficher les donnees----------------
                    courrier_table.heading("image" , text="الصورة")
                    courrier_table.heading("sujet_doc" , text="الموضوع")
                    courrier_table.heading("date_doc" , text="تاريخ الإصدار")
                    courrier_table.heading("source_doc" , text="مصدر الوثيقة")
                    courrier_table.heading("num_doc" , text="رقم الوثيقة")
                    courrier_table.heading("clas_doc" , text="تصنيف الوثيقة")
                    courrier_table.heading("type_doc" , text="نوع الوثيقة")
                    courrier_table.heading("date_enreg" , text="تاريخ الوصول")
                    courrier_table.heading("num_enreg" , text="رقم التسجيل  ")
                    courrier_table.column("image" , anchor="e" , width=160)
                    courrier_table.column("sujet_doc" , anchor="e" , width=160)
                    courrier_table.column("date_doc" , anchor="s" , width=60)
                    courrier_table.column("source_doc" , anchor="e" , width=80)
                    courrier_table.column("num_doc" , anchor="s" , width=40)
                    courrier_table.column("clas_doc" , anchor="e" , width=80)
                    courrier_table.column("type_doc" , anchor="e" , width=80)
                    courrier_table.column("date_enreg" , anchor="s" , width=60)
                    courrier_table.column("num_enreg" , anchor="s" , width=40)
                    courrier_table.bind("<ButtonRelease-1>" , focsel)
                    fetech_all()
                    root.mainloop()
                menu = Tk()
                menu.title("منظومة متابعة البريد")
                menu.geometry("1366x768")
                menu.resizable(False, False)
                menu.configure(bg="#BCF7F7")
                menubarr = Menu(menu)
                menu.config(menu=menubarr)

                file_menu = Menu(menubarr , tearoff=0)
                menubarr.add_cascade(label="الإعدادات" , menu=file_menu)
                file_menu.add_command(label="Light Mode")
                # file_menu.add_separator()
                file_menu.add_command(label="Dark Mode")

                Help_menu = Menu(menubarr , tearoff=0)
                menubarr.add_cascade(label="التحيين" , menu=Help_menu)
                Help_menu.add_command(label="البريد الوارد",command=aff_dep)
                Help_menu.add_command(label="البريد الصادر")
                Help_menu.add_command(label="توزيع البريد ")

                about_menu = Menu(menubarr , tearoff=0)
                menubarr.add_cascade(label="البحث" , menu=about_menu)
                about_menu.add_command(label="About")
                about_menu.add_command(label="Contact")
                menu.mainloop()
                connection.close()

                # Clear all the entries

        except Exception as e:
            msg.showerror("خطأ!", f"Error due to {str(e)}", parent=fram_log)


Label(fram_log, text=":إسم المستعمل", font=("Arial", 14, "bold"), bg="white", fg="#121483").place(x=220,
                                                                                                  y=180,
                                                                                                  width=110,
                                                                                                  height=30)
name_user = Entry(fram_log, textvariable=name_user_var, bd="2", justify="right").place(x=70, y=180,
                                                                                       width=120,
                                                                                       height=30)
Label(fram_log, text=":كلمة المرور", font=("Arial", 14, "bold"), fg="#121483", bg="white").place(x=220,
                                                                                                 y=220,
                                                                                                 width=110,
                                                                                                 height=30)
password = Entry(fram_log, textvariable=password_var, bd="2", justify="right").place(x=70, y=220,
                                                                                     width=120,
                                                                                     height=30)
btn_log = Button(fram_log, command=login_func, text=" دخول", bg="white", fg="#121483",
                 font=("Arial", 12, "bold"))
btn_log.place(x=240, y=280, width=80, height=30)
btn_ann = Button(fram_log, text="إلغاء", bg="white", fg="#121483", font=("Arial", 12, "bold"),
                 command=fram_log.quit)
btn_ann.place(x=100, y=280, width=80, height=30)

log.mainloop()

