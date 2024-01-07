from tkinter import *
from tkinter import filedialog
import random
import string


bracket = ','

def generate_random_key():
    length = 12
    characters = string.ascii_letters
    key = ''.join(random.choice(characters) for _ in range(length))
    key_entry.delete(0, END)
    key_entry.config(foreground=text_color)
    key_entry.insert(0, key)


def browse_file():
    file_path = filedialog.askopenfilename()
    file_content = ""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
    except FileNotFoundError:
        file_content = f"{file_path} adında bir dosya bulunamadı."
    except Exception as e:
        file_content = f"Dosya okuma hatası: {e}"
    file_entry.delete('1.0', 'end')
    file_entry.insert('1.0', file_content)


def reverse(text):
    lines = text.splitlines()
    revers_text = ""
    for line in lines:
        revers_text += ''.join(line[i] for i in range(len(line))[::-1])
        revers_text += '\n'
    return revers_text


def transpose(text):
    lines = text.splitlines()
    max_line_length = max(len(line) for line in lines)
    transposed = ""
    for i in range(max_line_length):
        transposed += ''.join(line[i] if i < len(line) else ' ' for line in lines)
        transposed += '\n'
    return transposed


def encryption():
    if (key_entry.get() != '') and (file_entry.get("1.0", "end-1c") != ''):
        reverse_text = reverse(file_entry.get("1.0", "end-1c"))
        transpose_text = transpose(reverse_text)
        revers_key = reverse(key_entry.get())
        encrypted_text = ""
        for i, char in enumerate(transpose_text):
            encrypted_text += str(ord(char) + ord(revers_key[i % len(revers_key)]))
            encrypted_text += bracket
        file_entry.delete('1.0', 'end')
        file_entry.insert('1.0', encrypted_text)


def decryption():
    if (key_entry.get() != '') and (file_entry.get("1.0", "end-1c") != ''):
        text = file_entry.get("1.0", "end-1c")
        revers_key = reverse(key_entry.get())
        chars = text.split(bracket)
        decrypted_text = ""
        for i, char in enumerate(chars):
            try:
                decrypted_text += chr(int(char) - ord(revers_key[i % len(revers_key)]))
            except ValueError:
                decrypted_text += char
        decrypted_text = reverse(transpose(decrypted_text))
        trim = ""
        for line in decrypted_text.splitlines():
            trim += line.strip(" ")
            trim += '\n'
        decrypted_text = trim
        file_entry.delete('1.0', 'end')
        file_entry.insert('1.0', decrypted_text)


def on_key_press(event):
    if event.keysym == "Return":
        encryption()
    elif event.keysym == "Escape":
        decryption()


primary_color = '#2D4A53'
secondary_color = '#161B22'
text_color = '#AFB3B7'
background_color = '#5A636A'

windows = Tk(className=" Encryption Application")
windows.resizable(False, False)
windows.iconbitmap(default='encryption.ico')

size = Canvas(windows, height=400, width=600, background=primary_color, highlightbackground=primary_color)
size.pack()

key_label = Label(size, text="KEY", background=primary_color, foreground=text_color)
key_label.place(x=30, y=30)
key_entry = Entry(windows, background=background_color, foreground=text_color)
key_entry.place(x=80, y=30)
key_entry.focus_set()
key_button = Button(windows, text="Random Key", background=secondary_color, foreground=text_color, activebackground=background_color, command=generate_random_key)
key_button.place(x=210, y=28)

text_label = Label(windows, text="TEXT", background=primary_color, foreground=text_color)
text_label.place(x=30, y=65)
file_button = Button(windows, text="SELECT FOLDER", background=secondary_color, foreground=text_color, activebackground=background_color, command=browse_file)
file_button.place(x=80, y=65)
file_entry = Text(windows, width=67, height=14, background=background_color, foreground=text_color)
file_entry.place(x=30, y=100)

encrypt_button = Button(windows, text="Encryption", width=10, height=2, background=secondary_color, foreground=text_color, activebackground=background_color, command=encryption)
encrypt_button.place(x=490, y=340)

decrypt_button = Button(windows, text="Decryption", width=10, height=2, background=secondary_color, foreground=text_color, activebackground=background_color, command=decryption)
decrypt_button.place(x=400, y=340)

windows.bind("<Key>", on_key_press)

windows.mainloop()
