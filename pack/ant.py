import random
from global_variable import city_num, pheromone_graph, BETA, ALPHA, distance_graph, ant_num


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
