import random
import copy
import threading
import tkinter as tk
from functools import reduce

ALPHA = 1.0  # 信息启发因子
BETA = 2.0  # 期望启发因子
RHO = 0.5  # 信息素挥发因子
Q = 100.0  # 信息素释放总量

ant_num = 75  # 蚁群数量
city_num = 50  # 城市数量

# 城市坐标
# distance_x = [178, 272, 176, 171, 650, 499, 267, 703, 408, 437,12,67]
# distance_y = [170, 395, 198, 151, 242, 556, 57, 401, 305, 421,765,34]
# 3778
distance_x = [
    178, 272, 176, 171, 650, 499, 267, 703, 408, 437, 491, 74, 532,
    416, 626, 42, 271, 359, 163, 508, 229, 576, 147, 560, 35, 714,
    757, 517, 64, 314, 675, 69, 391, 628, 87, 240, 705, 699, 258,
    428, 614, 36, 360, 482, 666, 597, 209, 201, 492, 294]
distance_y = [
    170, 395, 198, 151, 242, 556, 57, 401, 305, 421, 267, 105, 525,
    381, 244, 330, 395, 169, 141, 380, 153, 442, 528, 329, 232, 48,
    498, 265, 343, 120, 165, 50, 433, 63, 491, 275, 348, 222, 288,
    490, 213, 524, 244, 114, 104, 552, 70, 425, 227, 331]
# 城市距离
distance_graph = [[0.0 for i in range(city_num)] for j in range(city_num)]  # 列表解析 初始化城市距离为0

# 信息素
pheromone_graph = [[1.0 for i in range(city_num)] for j in range(city_num)]  # 初始化信息素为1

# 最优路径
best_path = []


# 蚂蚁类
class Ant(object):

    def __init__(self, ID):
        self.ID = ID  # ID
        self.initialization_data()

    # 初始化数据
    def initialization_data(self):
        self.path = []  # 当前蚂蚁的路径
        self.total_distance = 0.0  # 当前路径的总距离
        self.move_count = 0  # 移动次数
        self.current_city = -1  # 当前停留的城市
        self.city_state = [True for i in range(city_num)]  # 城市状态 未去过为True

        city_index = random.randint(0, city_num - 1)  # 随机初始出生点
        self.current_city = city_index  # 出生点记录到当前城市
        self.path.append(city_index)  # 将当前城市添加到路径中
        self.city_state[city_index] = False  # 将该城市状态改为False
        self.move_count = 1

    # 选择城市
    def choice_next_city(self):
        next_city = -1
        select_citys_prob = [0.0 for i in range(city_num)]  # 存储去下个城市的概率 初始值为0
        total_prob = 0.0

        for i in range(city_num):
            if self.city_state[i]:
                select_citys_prob[i] = pow(pheromone_graph[self.current_city][i], ALPHA) * pow(
                    (1.0 / distance_graph[self.current_city][i]), BETA)
                total_prob += select_citys_prob[i]

        # 轮盘选择
        # 产生一个随机概率,范围0.0-total_prob
        if total_prob > 0.0:
            temp_prob = random.uniform(0.0, total_prob)
            for i in range(city_num):
                if self.city_state[i]:
                    temp_prob -= select_citys_prob[i]
                    if temp_prob < 0.0:
                        next_city = i
                        break
        if next_city == -1:
            next_city = random.randint(0, city_num - 1)
            while not (self.city_state[next_city]):  # if==False,说明已经遍历过了
                next_city = random.randint(0, city_num - 1)

        # 返回下一个城市序号
        return next_city

    # 计算路径总距离
    def cal_total_distance(self):
        # 总长度
        temp_distance = 0.0
        # 计算从0到city_num的距离
        for i in range(1, city_num):
            start, end = self.path[i], self.path[i - 1]
            temp_distance += distance_graph[start][end]

        # 加上最后一个到0的距离
        end = self.path[0]
        temp_distance += distance_graph[start][end]
        self.total_distance = temp_distance

    def move(self, next_city):
        self.path.append(next_city)  # 将下一个城市加到路径中
        self.city_state[next_city] = False  # 将该城市状态改为False
        self.total_distance += distance_graph[self.current_city][next_city]  # 城市距离加上到下一个城市的距离
        self.current_city = next_city  # 移动到下一个城市
        self.move_count += 1  # 移动次数加一

    def search_path(self):
        # 初始化
        self.initialization_data()

        # 搜索路径
        while self.move_count < city_num:
            # 移动到下一个城市
            next_city = self.choice_next_city()
            self.move(next_city)
        self.cal_total_distance()


class TSP(object):
    def __init__(self, window, width=800, height=600, n=city_num):
        self.window = window
        self.width = width
        self.height = height
        # 城市数目初始化为city_num
        self.n = n
        # tkinter.Canvas
        self.canvas = tk.Canvas(
            window,
            width=self.width,
            height=self.height,
            bg="white",  # 背景白色
            xscrollincrement=1,
            yscrollincrement=1
        )
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
        self.window.title("蚁群算法(e:开始搜索)")
        self.r = 5
        self.__lock = threading.RLock()  # 线程锁

        self.button()
        self.new()
        for i in range(city_num):
            for j in range(city_num):
                temp_distance = pow((distance_x[i] - distance_x[j]), 2) + pow((distance_y[i] - distance_y[j]), 2)
                temp_distance = pow(temp_distance, 0.5)
                distance_graph[i][j] = float(int(temp_distance + 0.5))  # 向下取整；+0.5实现四舍五入

    def button(self):
        # self.window.bind("n", self.new)  # 初始化
        self.window.bind("e", self.search_path)

    def new(self, evt=None):

        self.run = False

        self.clear()  # 清除信息
        self.citys = []  # 节点坐标
        self.city_node = []  # 节点对象

        for i in range(len(distance_x)):
            # 在画布上随机初始坐标
            x = distance_x[i]
            y = distance_y[i]
            self.citys.append((x, y))
            # 生成节点椭圆，半径为self.r
            node = self.canvas.create_oval(x - self.r,
                                           y - self.r, x + self.r, y + self.r,
                                           fill="#6495ED",  # 填充红色
                                           outline="#000000",
                                           tags="node",
                                           )
            self.city_node.append(node)
            # 显示坐标
            self.canvas.create_text(x, y - 10, text='(' + str(x) + ',' + str(y) + ')', fill='black')

        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = 1.0
        self.ants = [Ant(ID) for ID in range(ant_num)]  # 初始蚁群
        self.best_ant = Ant(-1)  # 记录最优解蚂蚁
        self.best_ant.total_distance = 99999  # 初始最大距离 1 << 31
        self.iter = 1  # 初始化迭代次数

    def line(self, order):
        self.canvas.delete("line")

        def line2(i1, i2):
            p1, p2 = self.citys[i1], self.citys[i2]
            self.canvas.create_line(p1, p2, fill="#000000", tags="line")
            return i2

        reduce(line2, order, order[-1])

    def clear(self):
        for item in self.canvas.find_all():
            self.canvas.delete(item)

    def search_path(self, evt=None):
        global best_path, count

        self.run = True

        count = 0
        while self.run:
            # 遍历每一只蚂蚁
            for ant in self.ants:
                # 搜索一条路径
                ant.search_path()
                # 与当前最优蚂蚁比较
                if ant.total_distance < self.best_ant.total_distance:
                    # 更新最优解
                    self.best_ant = copy.deepcopy(ant)
                    best_path = self.best_ant.path
                    shortest_distance = int(self.best_ant.total_distance)
            # 更新信息素
            self.update_pheromone()
            print(u"迭代次数：", self.iter, u"最佳路径总距离：", int(self.best_ant.total_distance))
            self.line(self.best_ant.path)
            self.window.title("蚁群算法(e:开始搜索) 迭代次数: %d" % self.iter)
            self.canvas.update()
            self.iter = self.iter + 1
            if self.iter > 400 or int(self.best_ant.total_distance) < 3800:
                self.run = False
                print(best_path)
                copyright()
        return best_path, shortest_distance



    # 更新信息素
    def update_pheromone(self):
        global count
        # 获取每只蚂蚁在其路径上留下的信息素
        temp_pheromone = [[0.0 for col in range(city_num)] for raw in range(city_num)]
        for ant in self.ants:
            for i in range(1, city_num):
                start, end = ant.path[i - 1], ant.path[i]
                # 在路径上的每两个相邻城市间留下信息素，与路径总距离反比，蚁周模型
                temp_pheromone[start][end] += Q / ant.total_distance
                temp_pheromone[end][start] = temp_pheromone[start][end]

        # 更新所有城市之间的信息素，旧信息素衰减加上新迭代信息素
        for i in range(city_num):
            for j in range(city_num):
                pheromone_graph[i][j] = pheromone_graph[i][j] * RHO + temp_pheromone[i][j]

    def mainloop(self):
        self.window.mainloop()


def copyright():
    print(u"""
        作者：朱晨霄
        日期：2021-12-06
        """)


if __name__ == '__main__':
    TSP(tk.Tk()).mainloop()
