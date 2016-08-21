# coding:utf-8
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *
from threading import Timer
import os
import sys
import hashlib

reload(sys)
sys.setdefaultencoding('utf8')

filename = ''


def author():
    showinfo('作者信息', '本软件由Delav完成')


def about():
    showinfo('版权信息', '本软件版权归属Delav')


def openfile():
    global filename
    filename = askopenfilename(defaultextension='.txt')
    if filename == '':
        filename = None
    else:
        root.title('FileName'+os.path.basename(filename))
        textPad.delete(1.0, END)
        f = open(filename, 'r')
        textPad.insert(1.0, f.read())
        f.close()


def new():
    global filename
    root.title('未命名文件')
    filename = None
    textPad.delete(1.0, END)


# def save():
#     value = textPad.get().strip()
#     if value:
#         f = open(value, 'w')
#         f.write(textPad.get('1.0', END).strip() + '\n')
#         f.close()
#     else:
#         save_as()


def save():
    global filename
    if filename:
        f = open(filename, 'w')
        msg = textPad.get(1.0, END)
        f.write(msg)
        f.close()
    else:
        save_as()


def _save():
    global filename
    f = open(filename, 'w')
    msg = textPad.get(1.0, END)
    f.write(msg)
    f.close()
    root.destroy()


def save_as():
    f = asksaveasfilename(initialfile='未命名.txt', defaultextension='.txt')
    global filename
    filename = f
    fh = open(f, 'w')
    msg = textPad.get(1.0, END)
    fh.write(msg)
    fh.close()
    root.title(os.path.basename(f))


def cut():
    textPad.event_generate('<<Cut>>')


def copy():
    textPad.event_generate('<<Copy>>')


def paste():
    textPad.event_generate('<<Paste>>')


def undo():
    textPad.event_generate('<<Undo>>')


def redo():
    textPad.event_generate('<<Redo>>')


def seleteAll():
    textPad.tag_add('sel', '1.0', END)


def search():
    topsearch = Toplevel(root)
    topsearch.geometry('300x30+200+250')
    label = Label(topsearch, text='Find')
    label.grid(row=0, column=0, padx=5)
    entry = Entry(topsearch, width=20)
    entry.grid(row=0, column=1, padx=5)
    button1 = Button(topsearch, text='查找')
    button1.grid(row=0, column=2)


def bg_color():
    textPad.config(bg='#66CCFF')


def fn_color():
    textPad.config(fg='#FFFFFF')


def ex_quit():
    root.destroy()

root = Tk()
root.title('Delav note')
root.geometry('800x500+100+100')  # 首大小为800x500，位置100*100

# Menu

menubar = Menu(root)
root.config(menu=menubar)

filemenu = Menu(menubar)
menubar.add_cascade(label='文件', menu=filemenu)
filemenu.add_command(label='新建', accelerator='Ctrl+N', command=new)
filemenu.add_command(label='打开', accelerator='Ctrl+O', command=openfile)
filemenu.add_command(label='保存', accelerator='Ctrl+S', command=save)
filemenu.add_command(label='另存为', accelerator='Ctrl+Shift+S', command=save_as)


editmenu = Menu(menubar)
menubar.add_cascade(label='编辑', menu=editmenu)
editmenu.add_command(label='撤销', accelerator='Ctrl+Z', command=undo)
editmenu.add_command(label='重做', accelerator='Ctrl+Y', command=redo)
editmenu.add_separator()
editmenu.add_command(label='剪切', accelerator='Ctrl+X', command=cut)
editmenu.add_command(label='复制', accelerator='Ctrl+C', command=copy)
editmenu.add_command(label='粘贴', accelerator='Ctrl+V', command=paste)
editmenu.add_separator()
editmenu.add_command(label='查找', accelerator='Ctrl+F', command=search)
editmenu.add_command(label='全选', accelerator='Ctrl+A', command=seleteAll)

fontmenu = Menu(root)
menubar.add_cascade(label='字体', menu=fontmenu)
fontmenu.add_command(label='样式')
fontmenu.add_command(label='大小')
fontmenu.add_command(label='颜色', command=fn_color)
fontmenu.add_separator()
fontmenu.add_command(label='背景颜色', command=bg_color)

aboutmenu = Menu(root)
menubar.add_cascade(label='关于', menu=aboutmenu)
aboutmenu.add_command(label='作者', command=author)
aboutmenu.add_command(label='版权', command=about)

# Toolbar
toolbar = Frame(root, height=10, bg='light sea green')
shortButton = Button(toolbar, text='打开', padx=5, pady=1, command=openfile)
shortButton.pack(side=LEFT, padx=5, pady=2)

shortButton = Button(toolbar, text='保存', padx=5, pady=1, command=save)
shortButton.pack(side=LEFT)
toolbar.pack(expand=NO, fill=X)

# text
textPad = Text(root, undo=True)
textPad.pack(expand=YES, fill=BOTH)

scroll = Scrollbar(textPad)
textPad.config(yscrollcommand=scroll.set, bg='#B0E0E6', fg="#FFFFFF", font=18)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT, fill=Y)

contents = textPad.get('1.0', END)


def getSig(contents):
    m = hashlib.md5(contents.encode())
    return m.digest()
sig = getSig(contents)


def show_toplevel():
    contents = textPad.get('1.0', END)
    if sig == getSig(contents):
        ex_quit()
    else:
        top = Toplevel()
        top.title('退出')
        top.geometry('200x100+350+300')
        top.resizable(False, False)
        Label(top, text='内容发生改变，是否保存更改？').pack()
        tcButton = Button(top, text='保存', padx=10, pady=2, command=_save)
        tcButton.pack(side=LEFT, padx=25)

        tcButton = Button(top, text='不保存', padx=10, pady=2, command=ex_quit)
        tcButton.pack(side=RIGHT, padx=25)

filemenu.add_command(label='退出', accelerator='Ctrl+F4', command=show_toplevel)


def get_line():
    global t
    row, col = textPad.index(INSERT).split('.')
    line_num = 'Ln:  ' + row + '   ' + 'Col:  ' + col
    var.set(line_num)

    t = Timer(1, get_line)
    t.start()

t = Timer(1, get_line)
t.start()

# Status Bar
var = StringVar()
status = Label(root, anchor=E, text='Ln', textvariable=var, padx=1)
status.pack(side=BOTTOM, fill=X)

root.mainloop()
