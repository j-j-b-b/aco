import copy
from pack.ant import Ant
from pack.queue import Queue
from global_variable import city_num, pheromone_graph, distance_graph, distance_x, distance_y, \
    ant_num, Q, RHO ,weight,loss_value
import json

que = Queue()
shortest_distance = 0
str1 = ''
def new():
    global ants, run, temp_pheromone, best_ant, iter
    # 求城市间的距离
    for i in range(city_num):
        for j in range(city_num):
            temp_distance = pow((distance_x[i] - distance_x[j]), 2) + pow((distance_y[i] - distance_y[j]), 2)
            temp_distance = pow(temp_distance, 0.5)
            distance_graph[i][j] = float(int(temp_distance + 0.5))  # 向下取整；+0.5实现四舍五入
    # 初始化信息素

    for i in range(city_num):
        for j in range(city_num):
            pheromone_graph[i][j] = 1.0

    ants = [Ant(ID) for ID in range(ant_num)]  # 初始蚁群
    best_ant = Ant(-1)  # 记录最优解蚂蚁
    best_ant.total_distance = 99999  # 初始最大距离
    run = True
    iter = 0


# @app.route('/api/json', methods=['GET', 'POST'])
def search_path():
    global ants, run, temp_pheromone, best_ant, iter, best_path, shortest_distance,que,weight,loss_value,str1
    loss_value = 0

    if (iter >= 15):
        que.put(int(best_ant.total_distance))
        for i in range(1 , que.size()):
            loss_value =loss_value + weight*(que.find(i-1) - que.find(i))
        que.get()
        print(loss_value)
        if(loss_value <= 50):
            return str1, shortest_distance
        
    else:
        que.put(int(best_ant.total_distance))

    # 遍历每一只蚂蚁
    for ant in ants:
        # 搜索一条路径
        ant.search_path()
        # 与当前最优蚂蚁比较
        if ant.total_distance < best_ant.total_distance:
            # 更新最优解
            best_ant = copy.deepcopy(ant)
            best_path = best_ant.path
            shortest_distance = int(best_ant.total_distance)

    # 更新信息素
    temp_pheromone = [[0.0 for col in range(city_num)] for raw in range(city_num)]
    for ant in ants:
        for i in range(1, city_num):
            start, end = ant.path[i - 1], ant.path[i]
            # 在路径上的每两个相邻城市间留下信息素，与路径总距离反比，蚁周模型
            temp_pheromone[start][end] += Q / ant.total_distance
            temp_pheromone[end][start] = temp_pheromone[start][end]

    # 更新所有城市之间的信息素，旧信息素衰减加上新迭代信息素
    for i in range(city_num):
        for j in range(city_num):
            pheromone_graph[i][j] = pheromone_graph[i][j] * RHO + temp_pheromone[i][j]
    iter = iter + 1
    print(u"迭代次数：", iter, u"最佳路径总距离：", int(best_ant.total_distance))
    print(best_path)
    
    # socketio.emit('connect', {'data': best_path}, namespace='/test_conn')
    # json(best_path,shortest_distance)
    str1 = processing_data()
    return str1, shortest_distance


    


def processing_data():
    list_json = []
    str1 = ''
    api_json = {"x": 1, "y": 2, "sort": -1}
    for i, j in zip(distance_x, distance_y):
        api_json["x"] = i
        api_json["y"] = j
        list_json.append(copy.deepcopy(api_json))

    for i, j in zip(best_path, range(len(distance_x))):
        list_json[i]["sort"] = j
    for i in list_json:
        str1=str1 + str(i) + '?'
    return str1


