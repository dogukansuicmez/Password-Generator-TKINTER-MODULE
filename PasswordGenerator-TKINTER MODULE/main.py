import json
from tkinter import *
from tkinter import messagebox
import pyperclip
import random
import smtplib


my_email = "mynewforpython@gmail.com"
my_password = "12312361"






# ---------------------------- SEARCH BUTTON ------------------------------- #
def ara():
    ws = web_entry.get()
    try:
        with open("sifre-email-site.json","r") as file:
            data = json.load(file)
            if ws in data:
                messagebox.showinfo(title=ws,message=f"Your email corresponding to this site is: {data[ws]['email']}\nand password is: {data[ws]['password']}")
            else:
                messagebox.showwarning(title="No search matched",message="sorry no such entry is avaliable")
    except FileNotFoundError:
        messagebox.showwarning(title="Uyarı",message="No Data File Found")






# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def parola_olustur():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    nr_letters = random.randint(8,10)
    nr_symbols = random.randint(2,4)
    nr_numbers = random.randint(2,4)

    parola = []
    for sayi in range(nr_letters):
        parola.append(random.choice(letters))
    for sayi in range(nr_symbols):
        parola.append(random.choice(symbols))
    for sayi in range(nr_numbers):
        parola.append(random.choice(numbers))
    random.shuffle(parola)
    son_parola = "".join(parola)
    #print(son_parola)
    password_entry.delete(0,len(son_parola)) # bunu da ekledim ki bir daha BUTON'a basarsa son_parola'ya kadar kısım silinsin
    password_entry.insert(0,son_parola)
    pyperclip.copy(son_parola) # direk kopyalama tuşuna atar yani direk ctrl + v yaptığında şifre gelir




# ---------------------------- SAVE PASSWORD ------------------------------- #
def add():
    web = web_entry.get()
    eu = eu_entry.get()
    pas = password_entry.get()
    new_data = {
        web: {
            "email": eu,
            "password": pas,
        }
    }
    if web == "" or eu == "" or pas == "":
        messagebox.showwarning(title="UYARI",message="Boşlukları doldurmadın geri git doldur hemen") # boşlukları kontrol eder
    else:
        with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:  # location for gmail in smtp
            connection.starttls()  # birileri hacklemeye çalışırsa bizim gönderdiğimiz maili okuyamaz çunku encrypted yapar bu
            connection.login(user=my_email, password=my_password)

            try:
                with open("sifre-email-site.json","r",encoding="UTF-8") as file:
                    data = json.load(file)

                    data.update(new_data)
            except FileNotFoundError:
                with open("sifre-email-site.json", "w", encoding="UTF-8") as file:
                    json.dump(new_data, file, indent=4)
                web_entry.delete(0, END)  # siler entry'nin içini
                eu_entry.delete(0, END)  # siler entry'nin içini
                password_entry.delete(0, END)  # siler entry'nin içini
            else:
                with open("sifre-email-site.json","w",encoding="UTF-8") as file:
                    # saving update data
                    json.dump(data,file,indent=4)

            finally:
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs="forpythonmynew@yahoo.com",
                    msg=f"Subject:Secret Details\n\nHello, this is a test message {new_data}")
                web_entry.delete(0,END) # siler entry'nin içini
                eu_entry.delete(0,END) # siler entry'nin içini
                password_entry.delete(0,END) # siler entry'nin içini

# ---------------------------- UI SETUP ------------------------------- #

#creating windowm

window = Tk()
window.title("Şifre Yöneticisi")
window.config(padx=20,pady=20,bg="black")

#creating canvas
canvas = Canvas(width=250,height=250,bg="black",highlightthickness=0)
password_symbol = PhotoImage(file="password.png") # bunlar resim eklemek için
canvas.create_image(125,125,image=password_symbol) # bunlar resim eklemek için

canvas.grid(column=1,row=0)

#creating buttons
generate_password = Button(text="Şifre Oluştur",font=("Courier",10,"bold"),bg="black",fg="white",highlightthickness=0,command=parola_olustur)
generate_password.grid(column=2,row=3)
add = Button(text="Ekle",font=("Courier",10,"bold"),bg="black",fg="white",highlightthickness=0,command=add)
add.config(width=44,height=1)
add.grid(column=1,row=4,columnspan=2)
search = Button(text="Ara",font=("Courier",10,"bold"),bg="black",fg="white",highlightthickness=0,command=ara)
search.config(width=13)
search.grid(column=2,row=1,columnspan=2)

#creating labels
website = Label(text="Website adı <==>",bg="black",fg="white")
website.grid(column=0,row=1)
e_u = Label(text="Email/Kullanıcı adı <==>",bg="black",fg="white")
e_u.grid(column=0,row=2)
password = Label(text="Şifre <==>",bg="black",fg="white")
password.grid(column=0,row=3)
anne = Label(text="Şifreniz\nburada güvenli",bg="black",fg="red",font=("Courier",13,"bold"))
ben_haric = Label(text="Kimse\nçalamaz!",bg="black",fg="red",font=("Courier",13,"bold"))
ben_haric.grid(column=2,row=0)
anne.grid(column=0,row=0)

#creating entries
web_entry = Entry()
web_entry.config(width=40,highlightthickness=0)
web_entry.focus() # cursor direk website entry'sinde olur
web_entry.grid(column=1,row=1)
eu_entry = Entry()
#eu_entry.insert(0,"z.......z@gmail.com") # bu şekilde email direk yazılı olur bu entry içinde
eu_entry.config(width=60,highlightthickness=0)
eu_entry.grid(column=1,row=2,columnspan=2)
password_entry = Entry()
password_entry.config(width=40,highlightthickness=0)
password_entry.grid(column=1,row=3)








window.mainloop()
