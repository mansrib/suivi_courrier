from tkinter import *

root = Tk()
root.title("منظومة متابعة البريد")
root.geometry("400x400")

menubarr = Menu(root)
root.config(menu=menubarr)

file_menu = Menu(menubarr, tearoff = 0)
menubarr.add_cascade(label = "Themes", menu = file_menu)
file_menu.add_command(label = "Light Mode")
#file_menu.add_separator()
file_menu.add_command(label = "Dark Mode")

Help_menu = Menu(menubarr, tearoff = 0)
menubarr.add_cascade(label = "Help", menu = Help_menu)
Help_menu.add_command(label = "Help options")

about_menu = Menu(menubarr, tearoff = 0)
menubarr.add_cascade(label = "About", menu = about_menu)
about_menu.add_command(label = "About")
about_menu.add_command(label = "Contact")

root.mainloop()
