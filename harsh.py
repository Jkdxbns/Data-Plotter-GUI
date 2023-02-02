import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation
from adjustText import adjust_text


data = pd.read_csv('E:/College/BARC/BARC/Data-Plotter-GUI/sample files/output_csv_half.csv',names = ["Time","Area1","Area2","Area3","Area4", '6', '7'],index_col = 0)

data1 =(data.Time)
data2 =(data.Area1)
count = 0
A = []
B = []


def draw_graph(i):
    global count
    count = count + 1
    A.append(data["Time"][count])
    B.append(data["Area1"][count])
    x_axis = len(data1)
    plt.cla()
    plt.plot(A, B)
    plt.xticks([x for x in range(1,x_axis,int(x_axis/9))])
    plt.grid()
    

anima = animation.FuncAnimation(plt.gcf(),draw_graph,interval = 0)
plt.show()


