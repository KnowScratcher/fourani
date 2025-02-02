import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
from scipy.io import wavfile
from tkinter import messagebox
from tkinter import ttk
from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
canvas = None
toolbar = None
file:str = ""
out:str = ""
y = None
rate = None
def openFile():
    global fileName,canvas,toolbar,file,y,rate
    filePath = filedialog.askopenfile(filetypes=(("wav files","*.wav"),("all files","*.*")))
    
    fig = Figure(figsize = (10, 5), 
                 dpi = 100) 
  
    # list of squares 
    w = wavfile.read(filePath.name)
    rate = w[0]
    y = w[1][:,0]
    file = filePath.name
    fileName.config(text=filePath.name.split("/")[-1])
    # print(y)
    # adding the subplot 
    plot1 = fig.add_subplot(111)
  
    # plotting the graph 
    plot1.plot(y) 
    try:
        canvas.get_tk_widget().destroy()
        toolbar.destroy()
    except:
        pass
  
    # creating the Tkinter canvas 
    # containing the Matplotlib figure 
    canvas = FigureCanvasTkAgg(fig, 
                               master = frame)   
    canvas.draw() 
  
    # placing the canvas on the Tkinter app 
    canvas.get_tk_widget().pack()
  
    # creating the Matplotlib toolbar 
    toolbar = NavigationToolbar2Tk(canvas, 
                                   frame) 
    toolbar.update() 
  
    # placing the toolbar on the Tkinter app 
    canvas.get_tk_widget().pack()  
    
def openOutput():
    global out
    out = filedialog.askdirectory()
    toFile.config(text=f"儲存到: {out}")
    toFileButton.config(text="重新指定輸出資料夾")

def quit():
    app.destroy()

def generate():
    global progress
    if "" in [file,out,startValue,endValue]:
        messagebox.showerror("參數不完整","請確定所有參數都設定好了(wav檔、輸出資料夾、開始、結束時間)")
        return
    try:
        print(startValue,endValue)
        start = int(startValue.get())
        end = int(endValue.get())
    except:
        messagebox.showerror("參數錯誤","請確認時間(整數)")
        return
    # datas = [178000,529500,1294000,1652500,1950000,2350000]
    # Number of sample points
    N = 256
    # sample rate
    l_all = y
    T = 1.0 / rate
    fig, (ax,ax2) = plt.subplots(2,1)       # 建立單一圖表
    ax.set_xlim(0,1000)              # x 座標範圍設定 0～20
    ax.set_ylim(0,y.max())          # y 座標範圍設定 -1.5～1.5
    ax2.set_xlim(0,len(l_all)-1)
    ax2.set_ylim(-1*y.max(),y.max())

    n = [i for i in range(start,end,N)] # n = [i for i in range(5,len(l_all)-1,N)]  # 使用串列升成式產生 0～20 共 100 筆資料
    xs, ys = [], []   
    x2s, y2s = [], []               # 設定 x 和 y 變數為空串列
    line, = ax.plot(xs, ys)          # 定義 line 變數為折線圖物件 ( 注意 line 後方有逗號 )
    line2, = ax2.plot(x2s,y2s)
    print("running")
    def run(i):
        # print(f"{i}/{len(l_all)}")
        progress['value'] = ((i-start)/(end-start))*100
        print((i/len(l_all))*100)
        app.update()
        l = l_all[i:(i+N)] if i+N <= len(l_all) else l_all[i:-1]
        y = l #np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
        yf = fft(y)
        xf = fftfreq(N, T)[:N//2]
        xs = xf
        ys = 2.0/N * np.abs(yf[0:N//2])
        line.set_data(xs, ys)        # 重新設定資料點
        ax.legend([f"{i}/{len(l_all)}"])
        x2s = [i for i in range(5,i+N)] if i+N <= len(l_all) else [i for i in range(5,len(l_all))]
        y2s = list(map(int,l_all[5:(i+N)])) if i+N <= len(l_all) else list(map(int,l_all[5:-1]))
        line2.set_data(x2s,y2s)

    # def run2(i):
    #     print(f"{i}/{len(l_all)}")
        

    ani = animation.FuncAnimation(fig, run, frames=n, interval=100,repeat=False)
    print("saving")
    ani.save(f'{out}/{file.split("/")[-1][:-4]}.gif', fps=10)
    # ani.pause()
    messagebox.showinfo("成功",f"已完成{file.split('/')[-1][:-4]}.gif")
    return
    # progress.destroy()
    # app.update()


app = tk.Tk()

width = 900
height = 800
window_width = app.winfo_screenwidth()
window_height = app.winfo_screenheight()
left = int((window_width - width)/2)
top = int((window_height - height)/2)  
app.geometry(f"{width}x{height}+{left}+{top}")
app.resizable(False,False)
app.title("FourAni")
app.iconbitmap('favicon.ico')

title = tk.Label(app,text="FourAni",font=("Arial",20))
title.pack()
fileName = tk.Label(app,text="未選取檔案")
fileName.pack()

openFileButton = tk.Button(app,text="開啟wav",command=openFile)
openFileButton.pack()

toFile = tk.Label(app,text="儲存到: 未知")
toFile.pack()

toFileButton = tk.Button(app,text="開啟輸出資料夾",command=openOutput)
toFileButton.pack()

frame = tk.Frame(app,padx=0)
frame.pack()

frameFunction = tk.Frame(app)
frameFunction.pack()
frameFunction1 = tk.Frame(frameFunction)
frameFunction1.pack()
frameFunction2 = tk.Frame(frameFunction)
frameFunction2.pack()

startLabel = tk.Label(frameFunction1,text="開始時間(x): ")
startLabel.pack(side="left")

startValue = tk.StringVar()
startValueInput = tk.Entry(frameFunction1,textvariable=startValue)
startValueInput.pack(side="left")

endLabel = tk.Label(frameFunction2,text="結束時間(x): ")
endLabel.pack(side="left")

endValue = tk.StringVar()
endValueInput = tk.Entry(frameFunction2,textvariable=endValue)
endValueInput.pack(side="left")

startButton = tk.Button(frameFunction,text="開始產生",command=generate)
startButton.pack()

progress = ttk.Progressbar(app,mode="determinate")
progress.pack()

app.mainloop()