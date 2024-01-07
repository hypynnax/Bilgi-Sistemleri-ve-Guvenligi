from tkinter import *
from tkinter import messagebox


def adjustment(array, letters_limit):
    for i in range(len(array) - 1, -1, -1):
        if array[i] % letters_limit == 0 and array[i] != 0:
            array[i] = 0
            array[i - 1] += 1


def check_the_ending(array, limit):
    is_the_end = True
    for step in array:
        if step != limit:
            is_the_end = False
            break
    return is_the_end


def exit(array):
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            if array[i] == array[j]:
                return False
    return True


def make_it_unique(array, limit):
    while True:
        if exit(array) or check_the_ending(array, limit):
            return
        array[len(array) - 1] += 1
        adjustment(array, limit + 1)


def produce():
    if (letters_entry.get() != '') and (password_length_entry.get() != ''):
        number = 0
        letters = letters_entry.get().strip(' ').split(',')
        password_length = int(password_length_entry.get())
        step_value = [0] * password_length
        limit = len(letters) - 1
        possibilities_text = ''
        while True:
            if choice_var.get() == 0:
                make_it_unique(step_value, limit)

            password = ""

            for step in step_value[::-1]:
                password = letters[step] + password

            possibilities_text += password
            number += 1

            if check_the_ending(step_value, limit):
                break

            possibilities_text += ','

            step_value[-1] += 1
            adjustment(step_value, limit + 1)

        if choice_var.get() == 0:
            possibilities_text = possibilities_text[:-(password_length + 1)]
            number -= 1

        possibilities_text = possibilities_text.replace(',', ',\n')

        possible_passwords_entry.delete('1.0', END)
        possible_passwords_entry.insert('1.0', possibilities_text)
        possible_passwords_number.config(text='NOPP : ' + str(number))


def search():
    target = search_entry.get()
    text = possible_passwords_entry.get(
        "1.0", "end-1c").replace('\n', '').strip()
    if (target != '') and (text != ''):
        is_there = FALSE
        index = 0
        possible_passwords = text.split(',')
        for password in possible_passwords:
            index += 1
            if password == target:
                is_there = TRUE
                break
        if is_there:
            messagebox.showinfo("Bilgilendirme", "Aranan " + target +
                                " şifresi " + str(index) + ". sırada bulundu.")
        else:
            messagebox.showerror("Uyarı", "Aranan şifre bulunamadı!")


def save():
    text_content = possible_passwords_entry.get("1.0", "end-1c")
    with open("possible passwords.txt", "w") as file:
        file.write(text_content)
    messagebox.showinfo(
        "Bilgilendirme", "İşlem Başarılı, veriler \"possible passwords.txt\" dosyasına kayıt edildi")


def on_key_press(event):
    if event.keysym == "Return":
        produce()
    elif event.state == 4:
        if event.keysym.lower() == 'f':
            search()
        elif event.keysym.lower() == 's':
            save()


primary_color = '#2D4A53'
secondary_color = '#161B22'
text_color = '#AFB3B7'
background_color = '#5A636A'

windows = Tk(className=" Password Probabilities Application")
windows.resizable(False, False)
windows.iconbitmap(default='possibilities.ico')

size = Canvas(windows, height=400, width=675, background=primary_color, highlightbackground=primary_color)
size.pack()

password_length_label = Label(size, text="PASSWORD LENGTH", background=primary_color, foreground=text_color)
password_length_label.place(x=30, y=30)
password_length_entry = Spinbox(from_=0, to=10, width=5, background=background_color, foreground=text_color)
password_length_entry.place(x=150, y=30)

letters_label = Label(size, text="LETTERS", background=primary_color, foreground=text_color)
letters_label.place(x=225, y=30)
letters_entry = Entry(windows, background=background_color, foreground=text_color)
letters_entry.place(x=280, y=30)

letters_label = Label(size, text="IS THERE AGAİN?", background=primary_color, foreground=text_color)
letters_label.place(x=420, y=30)
choice_var = IntVar(value=1)
true_button = Radiobutton(windows, text="TRUE", variable=choice_var, value="1", background=primary_color, foreground=text_color, activebackground=primary_color, activeforeground=text_color)
true_button.place(x=525, y=28)
false_button = Radiobutton(windows, text="FALSE", variable=choice_var, value="0", background=primary_color, foreground=text_color, activebackground=primary_color, activeforeground=text_color)
false_button.place(x=590, y=28)

processing_button = Button(windows, text="PROCESSİNG", width=10, height=1, background=secondary_color, foreground=text_color, activebackground=background_color, command=produce)
processing_button.place(x=570, y=60)

possible_passwords_label = Label(windows, text="POSSİBLE PASSWORDS", background=primary_color, foreground=text_color)
possible_passwords_label.place(x=30, y=65)
possible_passwords_entry = Text(windows, width=77, height=14, background=background_color, foreground=text_color)
possible_passwords_entry.place(x=30, y=100)
possible_passwords_number = Label(windows, text="NOPP : 0", background=primary_color, foreground=text_color)
possible_passwords_number.place(x=30, y=330)

search_entry = Entry(windows, background=background_color, foreground=text_color)
search_entry.place(x=340, y=350)

search_button = Button(windows, text="SEARCH", width=10, height=2, background=secondary_color, foreground=text_color, activebackground=background_color, command=search)
search_button.place(x=480, y=340)

save_button = Button(windows, text="SAVE", width=10, height=2, background=secondary_color, foreground=text_color, activebackground=background_color, command=save)
save_button.place(x=570, y=340)

windows.bind("<Key>", on_key_press)

windows.mainloop()
