#!/usr/bin/python3.2
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import re

#initialize empty array to hold CSS properties
item_list = []
content = ""

def find(term, text):
    #find all ID's and classes in the document
    matches = re.findall(term + '=".*?"', text)
    return matches
 
def clean(match, tag, qualifier):
    #remove quotation marks
    match = match.replace("\"", "")
 
    #remove 'id=' or 'class='
    match = match.replace(tag + "=", "")

    #prepend the '.' or '#' and add the braces
    #and some newlines
    return qualifier + match + "{\n\n}\n\n"

def choose_src(*args):
    src_file = askopenfilename()
    #open file containing HTML code to be analyzed
    f = open(src_file, "r")
    global content
    content = f.read()
    f.close()
    code_display.insert('1.0', content)

def write_css(*args):
    global item_list
    m = find("id", content)
    for match in m:
        item_list.append(clean(match, 'id', '#'))
 
    #find all classes, assign to variable
    m = find("class", content)
    for match in m:
        item_list.append(clean(match, 'class', '.'))
 
    #remove duplicate items in list
    items = set(item_list)
 
    #open file to write CSS to
    f = open(asksaveasfilename(), "w")
 
    #write tag selectorrs to CSS file
    for tag in tags:
        f.write(tag + "{\n\n}\n\n")

    #for each item in list, print item to CSS file
    for i in items:
        f.write(i)
 
    #close the opened file
    f.close()

def setCheck(name, j):
    states[j] = not states[j]
    if states[j] == 1:
        tags.insert(-1, name)
    else:
        tags.remove(name)

root = Tk()
root.resizable(0,0)
content = ttk.Frame(root)
frame = ttk.Frame(content)
content.grid(column=0, row=0, columnspan=6)
frame.grid(column=0, row=0, columnspan=6, rowspan=3)
button = Button(root, text="QUIT", fg="red", width=10, command=root.quit)
button.grid(column=0, row=0, columnspan=2)
pick_source = Button(root, text="Choose source file", command=choose_src)
pick_source.grid(column=2, row=0, columnspan=2)
write_css = Button(root, text="Process!", width=10, command=write_css)
write_css.grid(column=4, row=0, columnspan=2)
lblTags = Label(root, text="Additional Selectors:")
lblTags.grid(column=0, row=1, columnspan=6)
code_display = Text(root)
s = ttk.Scrollbar(root, orient=VERTICAL, command=code_display.yview)
s.grid(column=5, row=3, sticky=(N,S, E))
code_display.grid(column=0, row=3, columnspan=6)
code_display['yscrollcommand'] = s.set

#Add some padding around all widgets in window
for widget in root.winfo_children():
    widget.grid_configure(padx=5, pady=5)

stateNames = ['a', '*', 'body', 'ul', 'li', 'h3']
tags = []
states = []
col = 0
#Create the checkbuttons
for name in stateNames:
    ttk.Checkbutton(root, text=str(name), command=lambda i=name, j=col: setCheck(i,j)).grid(column=col, row=2)
    states.append(0)
    col = col + 1

root.mainloop()
