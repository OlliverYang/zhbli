from tkinter import *
# import win32api,win32con
import time
# print(win32api.GetSystemMetrics(win32con.SM_CXSCREEN))
# print(win32api.GetSystemMetrics(win32con.SM_CYSCREEN))
i=0
top=Tk()
lab=Label(top,text='欢迎使用！', font=('Times','15'), fg='white', bg='black')
lab.master.overrideredirect(True)
lab.master.geometry("+1000+1024")  # 左右、上下
lab.pack()
words = ['不要猜测','自由','循序渐进', '对自己诚实', '不同的人有不同的感受', '睡觉时主动、自动想事情是生理疾病，但可以通过意识治标。']
length = len(words)
def show(event):
    global i
    while True:
        print(i)
        time.sleep(2)
        lab.config(text=words[i%length])
        lab.update()
        i+=1

lab.bind('<Enter>',show)
mainloop()