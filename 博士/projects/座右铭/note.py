from tkinter import *
# import win32api,win32con
import time
# print(win32api.GetSystemMetrics(win32con.SM_CXSCREEN))
# print(win32api.GetSystemMetrics(win32con.SM_CYSCREEN))
i=0
top=Tk()
lab=Label(top,text='欢迎使用！', font=('Times','8'), fg='white', bg='black')
lab.master.overrideredirect(True)
# lab.master.geometry("+600+1040")  # 笔记本 左右、上下
lab.master.geometry("+900+1055")  # 台式机 左右、上下
lab.pack()
words = ['不要猜测','自由','循序渐进', '对自己诚实', '不同的人有不同的感受',
               '睡觉时主动、自动想事情是生理疾病，但可以通过意识治标',
               '人生余额五十年',
               '如果感到不满意，可以选择立刻采取措施',
               '根据自己的耳鸣/黑眼圈/性能力/睡眠质量可以得出结论，自己的身体状况距正常人有很大差距',
               '美好的事不是轻松实现的，比如演员呈现一台“还可以”的演出要不服很大努力，身体健康也不容易，不然就不会有这么多医院和药物了',
               '不必要说的话不说，不必要做的事不做，不必要想的事不想']
length = len(words)

i = 0
while True:
    print(i)
    time.sleep(5)
    lab.config(text=words[i%length])
    lab.update()
    i += 1

lab.mainloop()