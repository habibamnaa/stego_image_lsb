from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from textwrap import wrap

# Encode stuff

def encodeRequirement(data_cipher_list, image):
    width, height = image.size
    size_limit_algorithm = 16777215  # 24 bit
    size_limit_picture = (width*height*3/8) - (width+(height-1))
    if len(data_cipher_list) <= size_limit_algorithm and len(data_cipher_list) < size_limit_picture :
        return True
    else:
        return False

def genData(data_cipher_list):
    newd = []

    for i in range(len(data_cipher_list)):
        newd.append(format(ord(chr(data_cipher_list[i])), '08b'))
    return "".join(newd)

def encode(data_cipher_list, image):
    width, height = image.size
    iteration_status = True
    iteration = 0
    max_iteration = len(data_cipher_list) * 8
    data_iteration = '{0:024b}'.format(max_iteration) # Converting int to binary 24 bits according to encode requirements
    data_cipher_bin = genData(data_cipher_list)

    # Putting 24 bits value for counting iteration in the first 8 pixel at image
    for y in range(0, 8):
        pixel = list(image.getpixel((0, y)))
        for n in range(0, 3):
            pixel[n] = pixel[n] & ~1 | int(data_iteration[iteration])
            iteration += 1
            image.putpixel((0, y), tuple(pixel))

    # Putting data in image
    x, y = 0, 8
    iteration = 0
    while iteration_status :
        pixel = list(image.getpixel((x, y)))
        for n in range(0, 3):
            if iteration < max_iteration :
                pixel[n] = pixel[n] & ~1 | int(data_cipher_bin[iteration])
                iteration += 1
                image.putpixel((x, y), tuple(pixel))
            else :
                iteration_status = False
                break
        y += 1
        if y >= height :
            y = 0
            x += 1

    image_name = simpledialog.askstring(title="File name", prompt="Type new image file without extension :")
    messagebox.showinfo('Thanks :)', 'The file has been encoded')
    image.save(f"{image_name}.png", "PNG")

# Decode stuff

def decode(image):

    width, height = image.size

    extracted_bin_number = []
    for y in range(0, 8):
        pixel = list(image.getpixel((0, y)))
        for n in range(0, 3):
            extracted_bin_number.append(pixel[n] & 1)

    max_iteration = int("".join([str(x) for x in extracted_bin_number]), 2)

    extracted_bin = []
    x, y = 0, 8
    iteration = 0
    iteration_status = True
    while iteration_status:
        pixel = list(image.getpixel((x, y)))
        for n in range(0, 3):
            if iteration < max_iteration:
                extracted_bin.append(pixel[n] & 1)
                iteration += 1
            else:
                iteration_status = False
                break
        y += 1
        if y >= height:
            y = 0
            x += 1

    return(extracted_bin)



def open_image_encryption():
    global my_image_encrypt, directory_picture_encrypt, my_label_img_encrypt
    root.filename_picture = askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=(("png files", "*.png"), ("all files", "*.*")))
    directory_picture_encrypt = root.filename_picture
    my_label_img_encrypt.configure(text="img dir : " + directory_picture_encrypt)
    temp_canvas_encrypt.destroy()

    left_img = Image.open(directory_picture_encrypt)
    left_img = left_img.resize((300, 200), Image.NEAREST)

    my_image_encrypt = ImageTk.PhotoImage(left_img)

    w1 = Label(root, image=my_image_encrypt, width=300, height=200)
    w1.grid(column=0, row=5, pady=3)

def open_image_decrpytion():
    global my_image_decrypt, directory_picture_decrypt, my_label_img_decrypt
    root.filename_picture = askopenfilename(initialdir="/", title="Select A File",
                                            filetypes=(("png files", "*.png"), ("all files", "*.*")))
    directory_picture_decrypt = root.filename_picture
    my_label_img_decrypt.configure(text="img dir : " + directory_picture_decrypt)
    temp_canvas_decrypt.destroy()

    left_img = Image.open(directory_picture_decrypt)
    left_img = left_img.resize((300, 200), Image.NEAREST)

    my_image_decrypt = ImageTk.PhotoImage(left_img)

    w2 = Label(root, image=my_image_decrypt, width=300, height=200)
    w2.grid(column=0, row=5, pady=3)

def open_file():
    global directory_file_encrypt, my_label_file
    root.filename_file = askopenfilename(initialdir="/", title="Select A File")
    directory_file_encrypt = root.filename_file
    my_label_file.configure(text="file dir : " + directory_file_encrypt)

def encrypt():
    image_real = Image.open(directory_picture_encrypt, 'r')
    image = image_real.copy()

    data_open = open(directory_file_encrypt, 'rb')
    data = data_open.read()
    data_open.close()
    data_list = list(data)


    data_cipher_list = data_list


    encode(data_cipher_list, image)

def decrypt():
    image = Image.open(directory_picture_decrypt, 'r')

    ciphertext_list = decode(image)

    raw_data = wrap(''.join(str(e) for e in ciphertext_list), 8)  # List of integer to string
    raw_data = [int(i,2) for i in raw_data] # list of string to decimal

    file_name = simpledialog.askstring(title="File name", prompt="Type file name with extension :")
    file_bytes = bytes(raw_data)

    messagebox.showinfo('Thanks :)', 'The file has been decoded')

    with open(file_name, "wb") as file_save:
        file_save.write(file_bytes)

def choose_encrypt():
    global pil, root, key_encrypt, title_encrypt, open_img_encrpytion, my_label_img_encrypt, temp_canvas_encrypt, my_label_file
    pil = 'encode'
    window.destroy()

    root = Tk()
    root.title('Steganography with Least Significant Bits Method')
    directory_picture_encrypt = ''
    directory_file_encrypt = ''

    # Left
    title_encrypt = Label(root, text="Encoding")
    title_encrypt.grid(column=0, row=0, pady=20)

    open_img_encrpytion = Button(root, text="Open Stego Object", command=open_image_encryption).grid(column=0, row=1, pady=1)

    my_label_img_encrypt = Label(root, text="img dir : ")
    my_label_img_encrypt.grid(column=0, row=2, pady=1)
    my_label_img_encrypt.configure(text="img dir : " + directory_picture_encrypt)

    my_btn2 = Button(root, text="Open Image", command=open_file).grid(column=0, row=3, pady=1)
    my_label_file = Label(root, text="file dir : ")
    my_label_file.grid(column=0, row=4, pady=1)
    my_label_file.configure(text="file dir : " + directory_file_encrypt)

    temp_canvas_encrypt = Canvas(root, bg='grey', width=300, height=200)
    temp_canvas_encrypt.grid(column=0, row=5, pady=3)

    encrypt_btn = Button(root, text='Encode', command=encrypt)
    encrypt_btn.grid(column=0, row=6, pady=3)

def choose_decrypt():
    global pil, root, my_label_img_decrypt, temp_canvas_decrypt
    pil = 'decode'
    window.destroy()

    root = Tk()
    root.title('Steganography with Least Significant Bits Method')
    directory_picture_decrypt = ''
    key_encrypt = ''

    # Right

    title_decrypt = Label(root, text="Decoding")
    title_decrypt.grid(column=0, row=0, padx=20)

    open_img_decrpytion = Button(root, text="Open Image", command=open_image_decrpytion).grid(column=0, row=1)

    my_label_img_decrypt = Label(root, text="img dir : ")
    my_label_img_decrypt.grid(column=0, row=2, pady=1)
    my_label_img_decrypt.configure(text="img dir : " + directory_picture_decrypt)

    temp_canvas_decrypt = Canvas(root, bg='grey', width=300, height=200)
    temp_canvas_decrypt.grid(column=0, row=5, pady=3)

    decrypt_btn = Button(root, text='Decode', command=decrypt)
    decrypt_btn.grid(column=0, row=6, pady=3)

    root.mainloop()


pil = ''

window = Tk()
window.title('Steganography Least Significant Bits Method')

title_menu = Label(window, text="<==| CHOOSE ONE |==>")
title_menu.grid(column=1, row=0, pady=20)

encrypt_btn = Button(window, text="Encode", command=choose_encrypt).grid(column=0, row=0, pady=1)
encrypt_btn = Button(window, text="Decode", command=choose_decrypt).grid(column=2, row=0, pady=1)


window.mainloop()