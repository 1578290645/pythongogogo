from tkinter import *
import tkinter.messagebox
game_over=0
color_number = 1
code = ""
size = 16
chess_num=0
global is_chess
chess_color = 0
xxx = 1
yyy = 1
is_chess=0
# 保存棋盘
chess = [[0 for i in range(size+1)] for i in range(size+1)]
# 给每一种可能的情况设置权值来实现ai，可以通过调整权值改变难度（越聪明的ai这个表越长）
chess_Value = [[0 for i in range(size+1)] for i in range(size+1)]
dic = {"0": 0, "1": 8, "2": 10, "11": 50, "22": 1000, "111": 2500, "222": 3000, "1111": 5000, "2222": 40000,
       "21": 4, "12": 2, "211": 25, "122": 20, "11112": 4000, "112": 30, "1112": 2800, "221": 500, "2221": 2000,
       "22221": 20000}

#  使棋落在棋盘点上
def paint(event):
    #  使棋落在棋盘点上
    global color_number
    global is_chess
    global chess_num
    #事件
    if event.x % 30 > 15 :
        event.x = event.x//30 + 1
    else:
        event.x = event.x // 30
    if event.y % 30 > 15:
        event.y = event.y // 30 + 1
    else:
        event.y = event.y//30
    if event.x > size:
        event.x = size
    if event.y > size:
        event.y = size
    if event.x < 1:
        event.x = 1
    if event.y < 1:
        event.y = 1

    # 黑白轮流落子
    x1, y1 = (event.x*30 - 15), (event.y*30 - 15)
    x2, y2 = (event.x*30 + 15), (event.y*30 + 15)
    if chess[event.x][event.y] == 0:
        #绘制棋子
        canvas.create_oval(x1, y1, x2, y2, fill="black")
        chess[event.x][event.y] = 1
        color_number = color_number + 1
        is_chess=0
        chess_num=chess_num+1
        canvas.create_rectangle(490,20,530,50,fill='#6B8E23')
        #记录和刷新的分数
        canvas.create_text(510, 30, fill='white', text='步数:{}'.format(chess_num))
        gameover(event.x, event.y)
        #轮到白棋
        ai()
    color_number += 1   

#  为了玩家的游戏体验并没有使用必胜算法，理论上还可以用不同的权值表调整游戏难度
#  这个ai还是比较傻的。。。
def ai():
    global xxx, yyy
    global code  #获取棋型
    global chess_color #保存颜色
    global is_chess
    global chess_num
    for i in range(1, size+1):
        for j in range(1, size + 1):
            if chess[i][j] == 0:
                code = ""
                chess_color = 0
                #向右 由于判断方式完全一样，其他几种就不注释了
                for x in range(i + 1, size + 1):
                    # 如果向右的第一位置为空就跳出循环
                    if chess[x][j] == 0:
                        break
                    else:
                        if chess_color == 0:  # 这是右边第一颗棋子
                            code += str(chess[x][j])  # 记录它的颜色
                            chess_color = chess[x][j]  # 保存它的颜色
                        else:
                            if chess_color == chess[x][j]:  # 跟第一颗棋子颜色相同
                                code += str(chess[x][j])  # 记录它的颜色
                            else:  # 右边找到一颗不同颜色的棋子
                                code += str(chess[x][j])
                                break
                # 取出对应的权值
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                # 把code，chess_color清空
                code = ""
                chess_color = 0
                # 向左
                for x in range(i - 1, 0, -1):
                    if chess[x][j] == 0:
                        break
                    else:
                        if chess_color == 0:  
                            code += str(chess[x][j])  
                            chess_color = chess[x][j] 
                        else:
                            if chess_color == chess[x][j]:  
                                code += str(chess[x][j]) 
                            else:  
                                code += str(chess[x][j])
                                break
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                code = ""
                chess_color = 0
                #  向上
                for y in range(j - 1, 0, -1):
                    if chess[i][y] == 0:
                        break
                    else:
                        if chess_color == 0:  
                            code += str(chess[i][y])  
                            chess_color = chess[i][y] 
                        else:
                            if chess_color == chess[i][y]:  
                                code += str(chess[i][y])  
                            else:  
                                code += str(chess[i][y])
                                break
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                code = ""
                chess_color = 0
                # 向下
                for y in range(j+1, size+1):
                    if chess[i][y] == 0:
                        break
                    else:
                        if chess_color == 0: 
                            code += str(chess[i][y])  
                            chess_color = chess[i][y] 
                        else:
                            if chess_color == chess[i][y]: 
                                code += str(chess[i][y])  
                            else:  
                                code += str(chess[i][y])
                                break

                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                code = ""
                chess_color = 0
                # 向左下
                for x, y in zip(range(i - 1, 0, -1), range(j + 1, size + 1)):
                    if chess[x][y] == 0:
                        break
                    else:
                        if chess_color == 0:  
                            code += str(chess[x][y])  
                            chess_color = chess[x][y]  
                        else:
                            if chess_color == chess[x][y]:  
                                code += str(chess[x][y])  
                            else:  
                                code += str(chess[x][y])
                                break
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                code = ""
                chess_color = 0
                # 向右上
                for x, y in zip(range(i + 1, size+1), range(j - 1, 0, -1)):
                    if chess[x][y] == 0:
                        break
                    else:
                        if chess_color == 0:  
                            code += str(chess[x][y]) 
                            chess_color = chess[x][y]  
                        else:
                            if chess_color == chess[x][y]:  
                                code += str(chess[x][y])  
                            else:  
                                code += str(chess[x][y])
                                break
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                code = ""
                chess_color = 0
                # 向左上
                for x, y in zip(range(i - 1, 0, -1), range(j - 1, 0, -1)):
                    if chess[x][y] == 0:
                        break
                    else:
                        if chess_color == 0:  
                            code += str(chess[x][y])  
                            chess_color = chess[x][y] 
                        else:
                            if chess_color == chess[x][y]: 
                                code += str(chess[x][y]) 
                            else:  
                                code += str(chess[x][y])
                                break
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                code = ""
                chess_color = 0
                # 向右下
                for x, y in zip(range(i+1, size+1), range(j+1, size+1)):
                    if chess[x][y] == 0:
                        break
                    else:
                        if chess_color == 0:  
                            code += str(chess[x][y])  
                            chess_color = chess[x][y]  
                        else:
                            if chess_color == chess[x][y]:  
                                code += str(chess[x][y])  
                            else:  
                                code += str(chess[x][y])
                                break
                value = dic.get(code)
                if value:
                    chess_Value[i][j] += value
                code = ""
                chess_color = 0
    mymax = 0
    #权值大小代表落子的优先级别高低
    for a in range(1, size+1):
        for b in range(1, size + 1):
            if chess_Value[a][b] > mymax and chess[a][b] == 0:
                mymax = chess_Value[a][b]
                xxx = a
                yyy = b
    chess[xxx][yyy] = 2
    canvas.create_oval(xxx*30-15, yyy*30-15, xxx*30+15, yyy*30+15, fill="white")
    is_chess=1
    chess_num=chess_num+1
    canvas.create_rectangle(490,20,530,50,fill='#6B8E23')
    canvas.create_text(510, 30, fill='white', text='步数:{}'.format(chess_num))
    gameover(xxx, yyy)

def gobang():
    global tk
    global chess_num
    #绘制棋盘
    tk = Tk()
    tk.title("五子棋")
    tk.geometry("540x510")
    global canvas
    canvas = Canvas(tk, width=500, height=500,bg='#6B8E23')
    canvas.pack(expand=YES, fill=BOTH)
    #事件
    canvas.bind("<Button-1>", paint)
    for num in range(1, 17):
        canvas.create_line(num*30, 30, num*30, 480,fill="#476042", width=2)
    for num in range(1, 17):
        canvas.create_line(30, num*30, 480, num*30,fill="#476042", width=2)
    canvas.create_rectangle(490,20,530,50,fill='#6B8E23')
    canvas.create_text(510, 30, fill='white', text='步数:{}'.format(chess_num))
    tk.mainloop()

def restart():
    global is_chess
    global chess_num
    #销毁原进程
    tk.destroy()
    #数据复原
    color_number = 1
    is_chess=0
    chess_num=0
    code = ""
    chess_color = 0
    xxx = 1
    yyy = 1
    for i in range(size+1):
        for j in range(size+1):
            chess[i][j]=0
            chess_Value[i][j]=0
    #重启
    gobang()

#   五子棋判断输赢的方法
def  gameover (xx, yy):
    global game_over
    count = 0
    for i in range(xx + 1, 17):
        if chess[i][yy] == chess[xx][yy]:
            count += 1
        else:
            break
    for i in range(xx, 0, -1):
        if chess[i][yy] == chess[xx][yy]:
            count += 1
        else:
            break
    if count >= 5:
        game_over=1

    count = 0

    for i in range(yy + 1, 17):
        if chess[xx][i] == chess[xx][yy]:
            count += 1
        else:
            break
    for i in range(yy, 0, -1):
        if chess[xx][i] == chess[xx][yy]:
            count += 1
        else:
            break
    if count >= 5:
        game_over=1
    count = 0

    for i, j in zip(range(xx+1, 17), range(yy+1, 17)):
        if chess[i][j] == chess[xx][yy]:
            count += 1
        else:
            break
    for i, j in zip(range(xx, 0, -1), range(yy, 0, -1)):
        if chess[i][j] == chess[xx][yy]:
            count += 1
        else:
            break
    if count >= 5:
        game_over=1
    count = 0

    for i, j in zip(range(xx - 1, 0, -1), range(yy + 1, 17)):
        if chess[i][j] == chess[xx][yy]:
            count += 1
        else:
            break
    for i, j in zip(range(xx, 17), range(yy, 0, -1)):
        if chess[i][j] == chess[xx][yy]:
            count += 1
        else:
            break
    if count >= 5:
        game_over=1
    count = 0 
    if game_over == 1:
        if is_chess==0:
            text="黑棋胜利！"
        else:
            text="白棋胜利！"  
        tkinter.messagebox.askokcancel("五子棋",text)
        #游戏结束后退出游戏
        game_over=0
        restart()


gobang()
