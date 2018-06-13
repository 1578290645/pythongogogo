#这是一个贪吃蛇小游戏
#特别说明
#a.小的方形食物吃一个加一分
#b,大的圆形食物吃一个加3分，每获得10分刷新一次(吃到中心才算哦)
#c.撞到墙壁就会挂掉的哟
#希望您玩的愉快
from tkinter import *
import threading
import queue
import time
import random
 
 
class GUI(Tk):
    #这个类创建gui
 
    def __init__(self, queue):
        #构造函数
        Tk.__init__(self)
        self.title("贪吃蛇")
        self.queue = queue
        self.is_game_over = False
        #设置画布和各个画图参量
        self.canvas = Canvas(self, width=495, height=305, bg='#008000')
        self.canvas.pack()
        self.snake = self.canvas.create_line((0,0),(0,0), fill='#FFD700', width=10)
        self.food = self.canvas.create_rectangle(0,0,0,0, fill='#00FF00', outline='#00FF00')
        self.specialfood = self.canvas.create_oval(0,0,0,0, fill='#FF4500', outline='#FF4500')
        self.point_score = self.canvas.create_text(455, 15, fill='white', text='得分:0')
        self.queue_handler()
 
    def restart(self):
        self.destroy()
        main()
        #执行
    def queue_handler(self):
        try:
            while True:
                task = self.queue.get(block=False)
                if task.get('game_over'):
                    self.game_over()
                elif task.get('move'):
                    points = [x for point in task['move'] for x in point]
                    self.canvas.coords(self.snake, *points)
                elif task.get('food'):
                    self.canvas.coords(self.food, *task['food'])
                elif task.get('specialfood'):
                    self.canvas.coords(self.specialfood, *task['specialfood'])
                elif task.get('points_score'):
                    self.canvas.itemconfigure(self.point_score,text='得分:{}'.format(task['points_score']))
                    #之前入队的一个任务已经完成。由队列的消费者线程调用
                    self.queue.task_done()
        except queue.Empty:
            if not self.is_game_over:
                #刷新
                self.canvas.after(100, self.queue_handler)
 
    def game_over(self):
        self.is_game_over = True
        self.canvas.create_text(220, 150, fill='black',text='游戏结束！')
        #设置按钮
        quitbtn = Button(self, text='退出', command=self.destroy)
        retbtn = Button(self, text='重来', command=self.restart)
        self.canvas.create_window(230, 180, anchor=W, window=quitbtn)
        self.canvas.create_window(200, 180, anchor=E, window=retbtn)
 
 
class Food():
    #这个类创建食物
 
    #构造函数
    def __init__(self, queue):
        self.queue = queue
        self.make_food()
 
    def make_food(self):
        #随机生成食物的坐标
        x = random.randrange(5, 480, 10)
        y = random.randrange(5, 295, 10)
        self.position = x,y
        self.exppos = x-5,y-5,x+5,y+5
        #入队
        self.queue.put({'food':self.exppos})


class Special_Food():
    #这两个类实现特殊食物
   
    def __init__(self, queue):
        self.queue = queue
        self.make_specialfood()
        self.clear_specialfood()
 
        
    def make_specialfood(self):
        #随机生成坐标
        x = random.randrange(5, 480, 10)
        y = random.randrange(5, 295, 10)
        self.sposition = x,y
        self.sexppos = x-10,y-10,x+10,y+10
        #入队
        self.queue.put({'specialfood':self.sexppos})
       
    def clear_specialfood(self):
        #在特殊食物不应该出现的时候，相当于隐藏
        self.sposition = 0,0
        self.sexppos = 0,0,0,0
        self.queue.put({'specialfood':self.sexppos})
       
            
            
         
 
class Snake(threading.Thread):
    #创造和控制贪吃蛇
 
    def __init__(self, gui, queue):
        #构造函数，利用threading控制多线程
        threading.Thread.__init__(self)
        self.gui = gui
        self.queue = queue
        self.daemon = True
        self.points_score = 0
        self.snake_points = [(495,55),(485,55),(475,55),(465,55),(455,55)]
        self.food = Food(queue)
        self.specialfood=Special_Food(queue)
        self.direction = 'Left'
        self.start()
 
    def run(self):
        if self.gui.is_game_over:
            #游戏结束，销毁
            self._delete()
        while not self.gui.is_game_over:
            self.queue.put({'move':self.snake_points})
            #刷新时间
            time.sleep(0.1)
            self.move()
 
    def key_pressed(self,e):
        #从键盘读入指令
        self.direction = e.keysym
 
    def move(self):
        new_snake_point = self.calculate_new_coordinates()
        if self.food.position == new_snake_point:
            #吃到食物了
            if self.points_score%10==9:
                #准备特殊食物
                add_snake_point = self.calculate_new_coordinates()
                #新的坐标进表
                self.snake_points.append(add_snake_point)
                #分数增加
                self.points_score += 1
                self.queue.put({'points_score':self.points_score})
                self.specialfood.make_specialfood()
                self.food.make_food()
            else:
                #不需要准备特殊食物
                add_snake_point = self.calculate_new_coordinates()
                self.snake_points.append(add_snake_point)
                self.points_score += 1
                self.queue.put({'points_score':self.points_score})
                self.food.make_food()
        elif self.specialfood.sposition == new_snake_point and self.points_score!=0 and self.points_score%10==0:
            #特殊食物不应该出现
            add_snake_point = self.calculate_new_coordinates()
            self.snake_points.append(add_snake_point)
            #加3分
            self.points_score += 3
            self.queue.put({'points_score':self.points_score})
            self.specialfood.clear_specialfood()
            
           

        else:
            #不需要加分和伸长，整体坐标平移
            self.snake_points.pop(0)
            self.check_game_over(new_snake_point)
            self.snake_points.append(new_snake_point)
 
    def calculate_new_coordinates(self):
        #读入键盘方向字符，确定direction，而且确定自己不会回头咬死自己
        last_x,last_y = self.snake_points[-1]
        if self.direction == 'Up' :
            if (last_x,last_y-10) !=self.snake_points[-2]:
                new_snake_point = last_x,last_y-10
            else:
                new_snake_point = last_x,last_y+10
        elif self.direction == 'Down' :
            if (last_x,last_y+10) !=self.snake_points[-2]:
                new_snake_point = last_x,last_y+10
            else:
                new_snake_point = last_x,last_y-10
        elif self.direction == 'Left' :
            if (last_x-10,last_y) !=self.snake_points[-2]:
                new_snake_point = last_x-10,last_y
            else:
                new_snake_point = last_x+10,last_y
        elif self.direction == 'Right' :
            if (last_x+10,last_y) !=self.snake_points[-2]:
                new_snake_point = last_x+10,last_y
            else:
                new_snake_point = last_x-10,last_y
        #返回新坐标
        return new_snake_point
 
    def check_game_over(self, snake_point):
        x,y = snake_point[0],snake_point[1]
        if not -5 < x < 505 or not -5 < y < 315 or snake_point in self.snake_points:
            self.queue.put({'game_over':True})
 
 
def main():
    #主函数
    q = queue.Queue()
    gui = GUI(q)
    snake = Snake(gui, q)
    gui.bind('<Key-Left>', snake.key_pressed)
    gui.bind('<Key-Right>', snake.key_pressed)
    gui.bind('<Key-Up>', snake.key_pressed)
    gui.bind('<Key-Down>', snake.key_pressed)
    print("欢迎回到贪吃蛇！"'\n'"说明几个地方："'\n'"a.小的方形食物吃一个加一分"'\n'"b,大的圆形食物吃一个加3分，每获得10分刷新一次(吃到中心才算哦)"'\n'"c.撞到墙壁就会挂掉的哟"'\n')
    gui.mainloop()

 
if __name__ == '__main__':
    main()


 
main()
