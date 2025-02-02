from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading

# datas = [178000,529500,1294000,1652500,1950000,2350000]
# Number of sample points
N = 512
# sample rate
# T = 1.0 / 16000

def do(FN):
    with open(FN+".txt") as f:
        l_all = f.read().split("\n")
    T = 1.0 / int(l_all[3][12:])
    fig, (ax,ax2) = plt.subplots(2,1)       # 建立單一圖表
    ax.set_xlim(0,1000)              # x 座標範圍設定 0～20
    ax.set_ylim(0,2000)          # y 座標範圍設定 -1.5～1.5
    ax2.set_xlim(0,len(l_all)-5)
    ax2.set_ylim(-4000,4000)

    n = [i for i in range(5,len(l_all)-1,N)]  # 使用串列升成式產生 0～20 共 100 筆資料
    xs, ys = [], []   
    x2s, y2s = [], []               # 設定 x 和 y 變數為空串列
    line, = ax.plot(xs, ys)          # 定義 line 變數為折線圖物件 ( 注意 line 後方有逗號 )
    line2, = ax2.plot(x2s,y2s)
    print("running")
    def run(i):
        print(f"{FN}: {i}/{len(l_all)}")
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

    ani = animation.FuncAnimation(fig, run, frames=n, interval=100)
    #ani2 = animation.FuncAnimation(fig2,run2,frames=n,interval=100)
    print("saving")
    ani.save(f'{FN}.gif', fps=10)
    #ani2.save("wave.gif",fps=10)
    plt.show()

threading.Thread(target=do,args=("al05(+10)-hand",)).start()
threading.Thread(target=do,args=("al05(+20)-hand",)).start()
threading.Thread(target=do,args=("al05(+30)-hand",)).start()
threading.Thread(target=do,args=("al05(+40)-hand",)).start()
threading.Thread(target=do,args=("al05(+50)-hand",)).start()
threading.Thread(target=do,args=("al05(+60)-hand",)).start()
