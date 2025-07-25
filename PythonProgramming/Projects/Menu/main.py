
# Project created by Supriya Nithin & Mohammed Hesham Ahmed
# TITLE: RESTAURANT MANAGEMENT SYSTEM
# Final class on 15-05-2019 Found.Software Dev-Python SEIS 603-04 prof: Eric Level


from tkinter import *
import random
import time
from tkinter import messagebox, ttk

root = Tk()

root.geometry("1366x768+0+0")                #
root.title("E.LEVEL RESTAURANT")

Tops = Frame(root, width=1550, height=80, bd=12, relief="raise")
Tops.pack(side=TOP)
lblTitle = Label(Tops, font=("times new roman", 50, 'bold'), text="             E.LEVEL RESTAURANT          ")
lblTitle.grid(row=0, column=0)

localtime = time.asctime(time.localtime(time.time()))
lblInfo = Label(Tops, font=('calibri', 20, 'bold'), text=localtime, bd=10, anchor='w')
lblInfo.grid(row=1, column=0)


BottomMainFrame = Frame(root, width=1550, height=770, bd=12, relief="raise")
BottomMainFrame.pack(side=BOTTOM)

f1 = Frame(BottomMainFrame, width=500, height=770, bd=12, relief=SUNKEN)
f1.pack(side=LEFT)

f1top = Frame(f1, width=500, height=570, bd=12, relief="raise")
f1top.pack(side=TOP)
f1bottom = Frame(f1, width=500, height=200, bd=12, relief="raise")
f1bottom.pack(side=BOTTOM)

f2 = Frame(BottomMainFrame, width=400, height=770, bd=12, relief=SUNKEN)
f2.pack(side=LEFT)
f2Top = Frame(f2, width=400, height=350, bd=4, relief="raise")
f2Top.pack(side=TOP)
f2Bottom = Frame(f2, width=400, height=450, bd=4, relief="raise")
f2Bottom.pack(side=BOTTOM)

f3 = Frame(BottomMainFrame, width=400, height=770, bd=12, relief=SUNKEN)
f3.pack(side=RIGHT)

f3top = Frame(f3, width=400, height=770, bd=12, relief="raise")
f3top.pack(side=TOP)
f3bottom = Frame(f3, width=400, height=100, bd=12, relief="raise")
f3bottom.pack(side=BOTTOM)

Receipt_Ref = StringVar()
DateofOrder = StringVar()
DateofOrder.set(time.strftime("%d/%m/%y"))

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()
var5 = IntVar()
var6 = IntVar()
var7 = IntVar()
var8 = IntVar()
var9 = IntVar()
var10 = IntVar()
var11 = IntVar()
var12 = IntVar()
var13 = IntVar()
var14 = IntVar()
var15 = IntVar()
var16 = IntVar()
var17 = IntVar()
var18 = IntVar()
var19 = IntVar()
var20 = IntVar()
var21 = IntVar()
var100 = IntVar()

var1.set(0)
var2.set(0)
var3.set(0)
var4.set(0)
var5.set(0)
var6.set(0)
var7.set(0)
var8.set(0)
var9.set(0)
var10.set(0)
var11.set(0)
var12.set(0)
var13.set(0)
var14.set(0)
var15.set(0)
var16.set(0)
var17.set(0)
var18.set(0)
var19.set(0)
var20.set(0)
var21.set(0)
var100.set(0)

varThali = StringVar()
varSalad = StringVar()
varBiryani = StringVar()
varLittiChokha = StringVar()
varChickenCurry = StringVar()
varPaneerTikka = StringVar()
varChickenTikka = StringVar()
varFishTikka = StringVar()

varThali.set(0)
varSalad.set(0)
varBiryani.set(0)
varLittiChokha.set(0)
varChickenCurry.set(0)
varPaneerTikka.set(0)
varChickenTikka.set(0)
varFishTikka.set(0)

varChocoBrownie = StringVar()
varGulabJamun = StringVar()
varPaan = StringVar()
varRasmalai = StringVar()
varJalebi = StringVar()

varChocoBrownie.set(0)
varGulabJamun.set(0)
varPaan.set(0)
varRasmalai.set(0)
varJalebi.set(0)

varTotal = StringVar()
varTAX = StringVar()
varServiceCharge = StringVar()
varPay = StringVar()
varPM = StringVar()
varTotal.set(0)
varTAX.set(0)
varServiceCharge.set(0)
varPay.set(0)

varTea = StringVar()
varCola = StringVar()
varCoffee = StringVar()
varOrange = StringVar()
varWater = StringVar()
varFruitCocktail = StringVar()

varTea.set(0)
varCoffee.set(0)
varCola.set(0)
varOrange.set(0)
varWater.set(0)
varFruitCocktail.set(0)

def iExit():
    qExit = messagebox.askyesno("Restraunt Management", "Do you want to quit ?")
    if qExit > 0:
        root.destroy()
        return

def Reset():
    varThali.set(0)
    varSalad.set(0)
    varBiryani.set(0)
    varLittiChokha.set(0)
    varChickenCurry.set(0)
    varPaneerTikka.set(0)
    varChickenTikka.set(0)
    varFishTikka.set(0)
    varChocoBrownie.set(0)
    varGulabJamun.set(0)
    varPaan.set(0)
    varRasmalai.set(0)
    varJalebi.set(0)
    varTotal.set(0)
    varTAX.set(0)
    varServiceCharge.set(0)
    varPay.set(0)
    varTea.set(0)
    varCoffee.set(0)
    varCola.set(0)
    varOrange.set(0)
    varWater.set(0)
    varFruitCocktail.set(0)

    var1.set(0)
    var2.set(0)
    var3.set(0)
    var4.set(0)
    var5.set(0)
    var6.set(0)
    var7.set(0)
    var8.set(0)
    var9.set(0)
    var10.set(0)
    var11.set(0)
    var12.set(0)
    var13.set(0)
    var14.set(0)
    var15.set(0)
    var16.set(0)
    var17.set(0)
    var18.set(0)
    var19.set(0)
    var20.set(0)
    var21.set(0)

    txtThali.configure(state=DISABLED)
    txtSalad.configure(state=DISABLED)
    txtBiryani.configure(state=DISABLED)
    txtLittiChokha.configure(state=DISABLED)
    txtChickenCurry.configure(state=DISABLED)
    txtPaneerTikka.configure(state=DISABLED)
    txtChickenTikka.configure(state=DISABLED)
    txtFishTikka.configure(state=DISABLED)
    txtChocoBrownie.configure(state=DISABLED)
    txtGulabJamun.configure(state=DISABLED)
    txtPaan.configure(state=DISABLED)
    txtRasmalai.configure(state=DISABLED)
    txtJalebi.configure(state=DISABLED)
    txtTotal.configure(state=DISABLED)
    txtTAX.configure(state=DISABLED)
    txtServiceCharge.configure(state=DISABLED)
    txtpay.configure(state=DISABLED)
    txtTea.configure(state=DISABLED)
    txtCoffee.configure(state=DISABLED)
    txtCola.configure(state=DISABLED)
    txtOrange.configure(state=DISABLED)
    txtWater.configure(state=DISABLED)

def Receipt():
    roor = Tk()
    roor.geometry("600x700+0+0")

    f1 = Frame(roor, width=1600, height=700, bd=12, relief="raise")
    f1.pack()
    lblReceipt = Label(f1, font=('calibri', 12, 'bold'), text="Receipt", bd=2, anchor='w')
    lblReceipt.grid(row=0, column=0, sticky=W)
    txtReceipt = Text(f1, width=64, height=35, bg="white", bd=8, font=('calibri', 11, 'bold'))
    txtReceipt.grid(row=1, column=0)
    txtReceipt.delete("1.0", END)
    x = random.randint(1000, 500890)
    randomRef = str(x)
    Receipt_Ref.set("BILL" + randomRef)

    txtReceipt.insert(END, 'Receipt Ref:\t\t\t' + Receipt_Ref.get() + '\t\t\t' + DateofOrder.get() + "\n")
    txtReceipt.insert(END, 'Items\t\t\t\t' + "No. of Items \n\n")
    txtReceipt.insert(END, 'Thali:\t\t\t\t\t' + varThali.get() + "\n")
    txtReceipt.insert(END, 'Salad: \t\t\t\t\t' + varSalad.get() + "\n")
    txtReceipt.insert(END, 'Biryani: \t\t\t\t\t' + varBiryani.get() + "\n")
    txtReceipt.insert(END, 'Litti-Chokha: \t\t\t\t\t' + varLittiChokha.get() + "\n")
    txtReceipt.insert(END, 'Chicken Curry: \t\t\t\t\t' + varChickenCurry.get() + "\n")
    txtReceipt.insert(END, 'Paneer Tikka: \t\t\t\t\t' + varPaneerTikka.get() + "\n")
    txtReceipt.insert(END, 'Chicken Tikka: \t\t\t\t\t' + varChickenTikka.get() + "\n")
    txtReceipt.insert(END, 'Fish Tikka: \t\t\t\t\t' + varFishTikka.get() + "\n")
    txtReceipt.insert(END, 'Choco Brownie: \t\t\t\t\t' + varChocoBrownie.get() + "\n")
    txtReceipt.insert(END, 'Gulab Jamun: \t\t\t\t\t' + varGulabJamun.get() + "\n")
    txtReceipt.insert(END, 'Paan: \t\t\t\t\t' + varPaan.get() + "\n")
    txtReceipt.insert(END, 'RasMalai: \t\t\t\t\t' + varRasmalai.get() + "\n")
    txtReceipt.insert(END, 'Jalebi: \t\t\t\t\t' + varJalebi.get() + "\n")
    txtReceipt.insert(END, 'Tea: \t\t\t\t\t' + varTea.get() + "\n")
    txtReceipt.insert(END, 'Coffee: \t\t\t\t\t' + varCoffee.get() + "\n")
    txtReceipt.insert(END, 'Cola: \t\t\t\t\t' + varCola.get() + "\n")
    txtReceipt.insert(END, 'Orange Juice: \t\t\t\t\t' + varOrange.get() + "\n")
    txtReceipt.insert(END, 'Water: \t\t\t\t\t' + varWater.get() + "\n")
    txtReceipt.insert(END, '\nTotal Cost of Food: \t\t' + varTotal.get() + "\nTAX:\t\t" + varTAX.get() + "\nService Charge:\t\t" + varServiceCharge.get() + "\nTotal Payble amount:\t\t" + varPay.get())
    root.mainloop()

def price_list():
    roo = Tk()
    roo.geometry("600x700+0+0")
    roo.title("MENU")

    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="ITEM", fg="black", bd=5)
    lblinfo.grid(row=0, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="_____________", fg="white", anchor=W)
    lblinfo.grid(row=0, column=2)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="PRICE in $", fg="black", anchor=W)
    lblinfo.grid(row=0, column=3)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Thali (470 Cal.)", fg="steel blue", anchor=W)
    lblinfo.grid(row=1, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="9", fg="steel blue", anchor=W)
    lblinfo.grid(row=1, column=3)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Salad (253 Cal.)", fg="steel blue", anchor=W)
    lblinfo.grid(row=2, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="4", fg="steel blue", anchor=W)
    lblinfo.grid(row=2, column=3)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Biryani (348 Cal.)", fg="steel blue", anchor=W)
    lblinfo.grid(row=3, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="19", fg="steel blue", anchor=W)
    lblinfo.grid(row=3, column=3)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Litti-Chokha (285 Cal.)", fg="steel blue", anchor=W)
    lblinfo.grid(row=4, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="3", fg="steel blue", anchor=W)
    lblinfo.grid(row=4, column=3)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Chicken Curry (296 Cal.)", fg="steel blue", anchor=W)
    lblinfo.grid(row=5, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="10", fg="steel blue", anchor=W)
    lblinfo.grid(row=5, column=3)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Paneer Tikka (272.2 Cal.)", fg="steel blue", anchor=W)
    lblinfo.grid(row=6, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="7", fg="steel blue", anchor=W)
    lblinfo.grid(row=6, column=3)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Chicken Tikka (148 Cal.)", fg="steel blue", anchor=W)
    lblinfo.grid(row=7, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="10", fg="steel blue", anchor=W)
    lblinfo.grid(row=7, column=3)

    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Fish Tikka (218 Cal.)", fg="steel blue", anchor=W)
    lblinfo.grid(row=8, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="10", fg="steel blue", anchor=W)
    lblinfo.grid(row=8, column=3)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Chocolate Brownie (132 Cal.)", fg="steel blue", anchor=W)
    lblinfo.grid(row=9, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="4", fg="steel blue", anchor=W)
    lblinfo.grid(row=9, column=3)

    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Hot Gulab Jamun with Icecream (160 Cal.)", fg="steel blue", anchor=W)
    lblinfo.grid(row=10, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="5", fg="steel blue", anchor=W)
    lblinfo.grid(row=10, column=3)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Paan (75 Cal.)", fg="steel blue", anchor=W)
    lblinfo.grid(row=11, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="3", fg="steel blue", anchor=W)
    lblinfo.grid(row=11, column=3)

    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Rasmalai (150 Cal.)", fg="steel blue", anchor=W)
    lblinfo.grid(row=12, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="5", fg="steel blue", anchor=W)
    lblinfo.grid(row=12, column=3)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Jalebi (123 Cal.)", fg="steel blue", anchor=W)
    lblinfo.grid(row=13, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="3", fg="steel blue", anchor=W)
    lblinfo.grid(row=13, column=3)

    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Tea", fg="steel blue", anchor=W)
    lblinfo.grid(row=14, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="2", fg="steel blue", anchor=W)
    lblinfo.grid(row=14, column=3)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Coffee", fg="steel blue", anchor=W)
    lblinfo.grid(row=15, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="2", fg="steel blue", anchor=W)
    lblinfo.grid(row=15, column=3)

    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Cola", fg="steel blue", anchor=W)
    lblinfo.grid(row=16, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="3", fg="steel blue", anchor=W)
    lblinfo.grid(row=16, column=3)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Orange Juice", fg="steel blue", anchor=W)
    lblinfo.grid(row=17, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="3", fg="steel blue", anchor=W)
    lblinfo.grid(row=17, column=3)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="Mineral Water", fg="steel blue", anchor=W)
    lblinfo.grid(row=18, column=0)
    lblinfo = Label(roo, font=('calibri', 15, 'bold'), text="2", fg="steel blue", anchor=W)
    lblinfo.grid(row=18, column=3)
    roo.mainloop()

def TotalCost():
    m1 = float(varThali.get())
    m2 = float(varSalad.get())
    m3 = float(varBiryani.get())
    m4 = float(varLittiChokha.get())
    m5 = float(varChickenCurry.get())
    m6 = float(varPaneerTikka.get())
    m7 = float(varChickenTikka.get())
    m8 = float(varFishTikka.get())
    m9 = float(varChocoBrownie.get())
    m10 = float(varGulabJamun.get())
    m11 = float(varPaan.get())
    m12 = float(varRasmalai.get())
    m13 = float(varJalebi.get())
    m14 = float(varTea.get())
    m15 = float(varCola.get())
    m16 = float(varCoffee.get())
    m17 = float(varOrange.get())
    m18 = float(varWater.get())

    iTotal = ( m1 * 9 + m2 * 4 + m3 * 19 + m4 * 3 + m5 * 10 + m6 * 7 + m7 * 10 + m8 * 10 + m9 * 4 + m10 * 5 + m11 * 3 + m12 * 5 + m13 * 3 + m14 * 2 + m15 * 2 + m16 * 3 +
                m17 * 2 + m18 * 2 )

    striTotal = '$', str(iTotal)
    varTotal.set(striTotal)

    TAX = (9 / 100) * iTotal
    strTAX = '$', str('%.2f' % TAX)
    varTAX.set(strTAX)


    service_charge = 0.1 * iTotal
    strService_charge = "$", str(service_charge)
    varServiceCharge.set(strService_charge)

    strPay = '$', str('%.2f' % (iTotal + TAX + service_charge))
    varPay.set(strPay)

def a():
    if var1.get() == 1:
        txtThali.configure(state=NORMAL)
        varThali.set("")
    elif var1.get() == 0:
        txtThali.configure(state=DISABLED)
        varThali.set("0")


def b():
    if var2.get() == 1:
        txtSalad.configure(state=NORMAL)
        varSalad.set("")
    elif var2.get() == 0:
        txtSalad.configure(state=DISABLED)
        varSalad.set("0")


def c():
    if var3.get() == 1:
        txtBiryani.configure(state=NORMAL)
        varBiryani.set("")
    elif var3.get() == 0:
        txtBiryani.configure(state=DISABLED)
        varBiryani.set("0")


def d():
    if var4.get() == 1:
        txtLittiChokha.configure(state=NORMAL)
        varLittiChokha.set("")
    elif var4.get() == 0:
        txtLittiChokha.configure(state=DISABLED)
        varLittiChokha.set("0")


def e():
    if var5.get() == 1:
        txtChickenCurry.configure(state=NORMAL)
        varChickenCurry.set("")
    elif var5.get() == 0:
        txtChickenCurry.configure(state=DISABLED)
        varChickenCurry.set("0")


def f():
    if var6.get() == 1:
        txtPaneerTikka.configure(state=NORMAL)
        varPaneerTikka.set("")
    elif var6.get() == 0:
        txtPaneerTikka.configure(state=DISABLED)
        varPaneerTikka.set("0")


def g():
    if var7.get() == 1:
        txtChickenTikka.configure(state=NORMAL)
        varChickenTikka.set("")
    elif var7.get() == 0:
        txtChickenTikka.configure(state=DISABLED)
        varChickenTikka.set("0")


def h():
    if var8.get() == 1:
        txtFishTikka.configure(state=NORMAL)
        varFishTikka.set("")
    elif var8.get() == 0:
        txtFishTikka.configure(state=DISABLED)
        varFishTikka.set("0")


def i():
    if var9.get() == 1:
        txtChocoBrownie.configure(state=NORMAL)
        varChocoBrownie.set("")
    elif var9.get() == 0:
        txtChocoBrownie.configure(state=DISABLED)
        varChocoBrownie.set("0")


def j():
    if var10.get() == 1:
        txtGulabJamun.configure(state=NORMAL)
        varGulabJamun.set("")
    elif var10.get() == 0:
        txtGulabJamun.configure(state=DISABLED)
        varGulabJamun.set("0")


def k():
    if var11.get() == 1:
        txtPaan.configure(state=NORMAL)
        varPaan.set("")
    elif var11.get() == 0:
        txtPaan.configure(state=DISABLED)
        varPaan.set("0")


def l():
    if var12.get() == 1:
        txtRasmalai.configure(state=NORMAL)
        varRasmalai.set("")
    elif var12.get() == 0:
        txtRasmalai.configure(state=DISABLED)
        varRasmalai.set("0")


def m():
    if var13.get() == 1:
        txtJalebi.configure(state=NORMAL)
        varJalebi.set("")
    elif var13.get() == 0:
        txtJalebi.configure(state=DISABLED)
        varJalebi.set("0")


def n():
    if var14.get() == 1:
        txtTea.configure(state=NORMAL)
        varTea.set("")
    elif var14.get() == 0:
        txtTea.configure(state=DISABLED)
        varTea.set("0")


def o():
    if var15.get() == 1:
        txtCola.configure(state=NORMAL)
        varCola.set("")
    elif var15.get() == 0:
        txtCola.configure(state=DISABLED)
        varCola.set("0")


def p():
    if var16.get() == 1:
        txtCoffee.configure(state=NORMAL)
        varCoffee.set("")
    elif var16.get() == 0:
        txtCoffee.configure(state=DISABLED)
        varCoffee.set("0")


def q():
    if var17.get() == 1:
        txtOrange.configure(state=NORMAL)
        varOrange.set("")
    elif var17.get() == 0:
        txtOrange.configure(state=DISABLED)
        varOrange.set("0")


def r():
    if var18.get() == 1:
        txtWater.configure(state=NORMAL)
        varWater.set("")
    elif var18.get() == 0:
        txtWater.configure(state=DISABLED)
        varWater.set("0")

lblMeal = Label(f1top, font=("calibri", 25, 'bold'), text="Lunch Meal")
lblMeal.grid(row=0, column=0)

Thali = Checkbutton(f1top, text="Thali", variable=var1, onvalue=1, offvalue=0, font=("calibri", 18, 'bold'), command=a)
Thali.grid(row=1, column=0, sticky=W)
txtThali = Entry(f1top, font=("calibri", 18, 'bold'), bd=8, textvariable=varThali, width=4, justify="right",
                 state=DISABLED)
txtThali.grid(row=1, column=1)

Salad = Checkbutton(f1top, text="Salad", variable=var2, onvalue=1, offvalue=0, font=("calibri", 18, 'bold'), command=b)
Salad.grid(row=2, column=0, sticky=W)
txtSalad = Entry(f1top, font=("calibri", 18, 'bold'), bd=8, textvariable=varSalad, width=4, justify="right",
                 state=DISABLED)
txtSalad.grid(row=2, column=1)

Biryani = Checkbutton(f1top, text="Biryani", variable=var3, onvalue=1, offvalue=0, font=("calibri", 18, 'bold'),
                        command=c)
Biryani.grid(row=3, column=0, sticky=W)
txtBiryani = Entry(f1top, font=("calibri", 18, 'bold'), bd=8, textvariable=varBiryani, width=4, justify="right",
                     state=DISABLED)
txtBiryani.grid(row=3, column=1)

LittiChokha = Checkbutton(f1top, text="Litti Chokha", variable=var4, onvalue=1, offvalue=0, font=("calibri", 18, 'bold'),
                          command=d)
LittiChokha.grid(row=4, column=0, sticky=W)
txtLittiChokha = Entry(f1top, font=("calibri", 18, 'bold'), bd=8, textvariable=varLittiChokha, width=4, justify="right",
                       state=DISABLED)
txtLittiChokha.grid(row=4, column=1)

ChickenCurry = Checkbutton(f1top, text="Chicken Curry", variable=var5, onvalue=1, offvalue=0,
                           font=("calibri", 18, 'bold'), command=e)
ChickenCurry.grid(row=5, column=0, sticky=W)
txtChickenCurry = Entry(f1top, font=("calibri", 18, 'bold'), bd=8, textvariable=varChickenCurry, width=4, justify="right",
                        state=DISABLED)
txtChickenCurry.grid(row=5, column=1)

lblSpace = Label(f1top, text="\n")
lblSpace.grid(row=6, column=0)
lblTikka = Label(f1top, font=("calibri", 25, 'bold'), text="Tikka")
lblTikka.grid(row=7, column=0)

PaneerTikka = Checkbutton(f1top, text="Paneer Tikka", variable=var6, onvalue=1, offvalue=0,
                             font=("calibri", 18, 'bold'), command=f)
PaneerTikka.grid(row=8, column=0, sticky=W)
txtPaneerTikka = Entry(f1top, font=("calibri", 18, 'bold'), bd=8, textvariable=varPaneerTikka, width=4,
                          justify="right", state=DISABLED)
txtPaneerTikka.grid(row=8, column=1)

ChickenTikka = Checkbutton(f1top, text="Chicken Tikka", variable=var7, onvalue=1, offvalue=0,
                              font=("calibri", 18, 'bold'), command=g)
ChickenTikka.grid(row=9, column=0, sticky=W)
txtChickenTikka = Entry(f1top, font=("calibri", 18, 'bold'), bd=8, textvariable=varChickenTikka, width=4,
                           justify="right", state=DISABLED)
txtChickenTikka.grid(row=9, column=1)

FishTikka = Checkbutton(f1top, text="Fish Tikka", variable=var8, onvalue=1, offvalue=0,
                           font=("calibri", 18, 'bold'), command=h)
FishTikka.grid(row=10, column=0, sticky=W)
txtFishTikka = Entry(f1top, font=("calibri", 18, 'bold'), bd=8, textvariable=varFishTikka, width=4, justify="right",
                        state=DISABLED)
txtFishTikka.grid(row=10, column=1)


btnReceipt = Button(f1bottom, padx=20, pady=2, bd=14, fg="black", font=('calibri', 16, 'bold'), width=16,
                    text="GENERATE RECEIPT", command=Receipt)
btnReceipt.grid(row=0, column=0)

lblMeal = Label(f2Top, font=("calibri", 25, 'bold'), text="Desserts")
lblMeal.grid(row=0, column=0)

ChocoBrownie = Checkbutton(f2Top, text="Chocolate Brownie", variable=var9, onvalue=1, offvalue=0,
                           font=("calibri", 18, 'bold'), command=i)
ChocoBrownie.grid(row=1, column=0, sticky=W)
txtChocoBrownie = Entry(f2Top, font=("calibri", 18, 'bold'), bd=8, textvariable=varChocoBrownie, width=4, justify="right",
                        state=DISABLED)
txtChocoBrownie.grid(row=1, column=1)

GulabJamun = Checkbutton(f2Top, text="Hot Gulab Jamun with Icecream", variable=var10, onvalue=1, offvalue=0,
                         font=("calibri", 18, 'bold'), command=j)
GulabJamun.grid(row=2, column=0, sticky=W)
txtGulabJamun = Entry(f2Top, font=("calibri", 18, 'bold'), bd=8, textvariable=varGulabJamun, width=4, justify="right",
                      state=DISABLED)
txtGulabJamun.grid(row=2, column=1)

Paan = Checkbutton(f2Top, text="Paan", variable=var11, onvalue=1, offvalue=0, font=("calibri", 18, 'bold'), command=k)
Paan.grid(row=3, column=0, sticky=W)
txtPaan = Entry(f2Top, font=("calibri", 18, 'bold'), bd=8, textvariable=varPaan, width=4, justify="right", state=DISABLED)
txtPaan.grid(row=3, column=1)

Rasmalai = Checkbutton(f2Top, text="Rasmalai", variable=var12, onvalue=1, offvalue=0, font=("calibri", 18, 'bold'),
                       command=l)
Rasmalai.grid(row=4, column=0, sticky=W)
txtRasmalai = Entry(f2Top, font=("calibri", 18, 'bold'), bd=8, textvariable=varRasmalai, width=4, justify="right",
                    state=DISABLED)
txtRasmalai.grid(row=4, column=1)

Jalebi = Checkbutton(f2Top, text="Jalebi", variable=var13, onvalue=1, offvalue=0, font=("calibri", 18, 'bold'), command=m)
Jalebi.grid(row=5, column=0, sticky=W)
txtJalebi = Entry(f2Top, font=("calibri", 18, 'bold'), bd=8, textvariable=varJalebi, width=4, justify="right",
                  state=DISABLED)
txtJalebi.grid(row=5, column=1)

lblPaymentMethod = Label(f2Bottom, font=("calibri", 18, 'bold'), text="Payment Method", bd=10, width=16, anchor='w')
lblPaymentMethod.grid(row=0, column=0)

cmbPaymentMethod = ttk.Combobox(f2Bottom, textvariable=varPM, state="readonly", font=("calibri", 10, 'bold'), width=20)
cmbPaymentMethod['value'] = ('Cash', 'Master Card', 'Visa Card', 'Debit Card')
cmbPaymentMethod.current(0)
cmbPaymentMethod.grid(row=0, column=1)

lblTotal = Label(f2Bottom, font=("calibri", 18, 'bold'), text="Total:", bd=10, width=16, anchor='e')
lblTotal.grid(row=2, column=1)
txtTotal = Entry(f2Bottom, font=("calibri", 18, 'bold'), bd=8, textvariable=varTotal, width=10, justify="right",
                 state=DISABLED)
txtTotal.grid(row=2, column=2)


lblTAX = Label(f2Bottom, font=("calibri", 18, 'bold'), text="Tax:", bd=10, width=16, anchor='e')
lblTAX.grid(row=3, column=1)
txtTAX = Entry(f2Bottom, font=("calibri", 18, 'bold'), bd=8, textvariable=varTAX, width=10, justify="right",
                state=DISABLED)
txtTAX.grid(row=3, column=2)

lblServiceCharge = Label(f2Bottom, font=("calibri", 18, 'bold'), text="Service Charge:", bd=10, width=16, anchor='e')
lblServiceCharge.grid(row=4, column=1)
txtServiceCharge = Entry(f2Bottom, font=("calibri", 18, 'bold'), bd=8, textvariable=varServiceCharge, width=10,
                         justify="right", state=DISABLED)
txtServiceCharge.grid(row=4, column=2)

btnprice = Button(f2Bottom, padx=20, pady=1, bd=14, fg="black", font=('calibri', 16, 'bold'), width=5, text="MENU",
                  command=price_list)
btnprice.grid(row=2, column=0)

btnTotal = Button(f2Bottom, padx=20, pady=1, bd=14, fg="black", font=("calibri", 16, 'bold'), width=5,
                  text="TOTAL", command=TotalCost).grid(row=3, column=0)

btnReset = Button(f2Bottom, padx=20, pady=1, bd=14, fg="black", font=('calibri', 16, 'bold'), width=5, text="RESET",
                  command=Reset)
btnReset.grid(row=4, column=0)

btnExit = Button(f2Bottom, padx=20, pady=1, bd=14, fg="black", font=('calibri', 16, 'bold'), width=5, text="EXIT",
                 command=iExit)
btnExit.grid(row=5, column=0)

lblDrinks = Label(f3top, font=("calibri", 25, 'bold'), text="Drinks")
lblDrinks.grid(row=0, column=0)

Tea = Checkbutton(f3top, text="Tea", variable=var14, onvalue=1, offvalue=0, font=("calibri", 18, 'bold'), command=n)
Tea.grid(row=1, column=0, sticky=W)
txtTea = Entry(f3top, font=("calibri", 18, 'bold'), bd=8, textvariable=varTea, width=4, justify="right", state=DISABLED)
txtTea.grid(row=1, column=1)

Cola = Checkbutton(f3top, text="Cola", variable=var15, onvalue=1, offvalue=0, font=("calibri", 18, 'bold'), command=o)
Cola.grid(row=2, column=0, sticky=W)
txtCola = Entry(f3top, font=("calibri", 18, 'bold'), bd=8, textvariable=varCola, width=4, justify="right", state=DISABLED)
txtCola.grid(row=2, column=1)

Coffee = Checkbutton(f3top, text="Coffee", variable=var16, onvalue=1, offvalue=0, font=("calibri", 18, 'bold'), command=p)
Coffee.grid(row=3, column=0, sticky=W)
txtCoffee = Entry(f3top, font=("calibri", 18, 'bold'), bd=8, textvariable=varCoffee, width=4, justify="right",
                  state=DISABLED)
txtCoffee.grid(row=3, column=1)

Orange = Checkbutton(f3top, text="Orange Juice", variable=var17, onvalue=1, offvalue=0, font=("calibri", 18, 'bold'),
                     command=q)
Orange.grid(row=4, column=0, sticky=W)
txtOrange = Entry(f3top, font=("calibri", 18, 'bold'), bd=8, textvariable=varOrange, width=4, justify="right",
                  state=DISABLED)
txtOrange.grid(row=4, column=1)

Water = Checkbutton(f3top, text="Mineral Water", variable=var18, onvalue=1, offvalue=0, font=("calibri", 18, 'bold'),
                    command=r)
Water.grid(row=5, column=0, sticky=W)
txtWater = Entry(f3top, font=("calibri", 18, 'bold'), bd=8, textvariable=varWater, width=4, justify="right",
                 state=DISABLED)
txtWater.grid(row=5, column=1)
lblSpace = Label(f3top, text="\n\n")
lblSpace.grid(row=6, column=0)


lblpay = Label(f3bottom, font=("calibri", 18, 'bold'), text="Total Payable Amount", fg="red", bd=10, width=16, anchor='e')
lblpay.grid(row=0, column=0)
txtpay = Entry(f3bottom, font=("calibri", 18, 'bold'), bd=8, textvariable=varPay, width=10, justify="right",
               state=DISABLED)
txtpay.grid(row=0, column=1)

root.mainloop()
