"""
A星算法是一种启发式搜索算法，启发式搜索就是在状态空间中的搜索，对每一个搜索的位置进行评估，得到最好的位置
再从这个位置进行搜索，直到找到目标。这样可以省略大量无畏的搜索路径，提高效率

A星算法核心公式： F = G + H
F: 方块移动的总代价，
G: 开始点到当前方块的移动代价  (G = 父节点的G值 + 父节点到当前点的移动代价)
H: 当前方块到结束点的预估移动代价 (当前点到结束点的曼哈顿距离)
拓展： G = 移动代价 * 代价因子(不同地形代价因子不同)

H值如何预测估算出来
在只知道当前点，结束点，而不知道两者的路径情况下，我们无法精确地确定H值大小，所以只能进行预估
很多方法可以预估H值，比如曼哈顿距离，欧式距离，对角线估价，最常用最简单的方法就是使用曼哈顿距离进行预估:
H = 当前方块到结束点的水平距离 + 当前方块到结束点的垂直距离

PS： A星算法之所以被认为是具有启发策略的算法，在于其可通过预估H值，降低走弯路的可能性，更容易找到一条更短的路径。
其他不具有启发策略的算法，没有做预估处理，只是穷举出所有可通行路径，然后从中挑选一条最短的路径。这也是A星算法效率更高的原因。

实现过程:
1. 把起始点添加到 open list， 然后重复下面工作
2. 遍历 open list，查找F值最小的节点，把它作为当前要处理的节点(作为当前节点)，把这个节点移到 close list

3. 判断当前方格的每个相邻方格，如果它是不可抵达，或者它在 close list 中则忽略它
   如果它不在 open list，把它加入 open list，并且把当前方格设置为它的父节点，记录该方格的F,G和H值
   如果它已经在 open list 中，检查这条路径(即经过当前方格到达它那里)是否更好，用G值作为参考，更小的G值表示这是更好的路径
   如果路径更好，则将它的父节点设置为当方格，然后重新计算它的 G 和 F, 如果你的open list 按照F值排序，改变后可能需要重新排序

4. 停止: 终点加入到 open list中，说明终点已经找到，路径确认。或者 open list 为空，查找终点失败
5. 保存路径，从终点开始，每个方格沿着父节点移动到起点
"""


class Point:
    """描叙AStar算法的节点数据"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Node:
    """节点"""
    def __init__(self, point, g=0, h=0):
        # 当前节点坐标，父节点，G值，H值
        self.point = point
        self.parent = None
        self.g = g
        self.h = h

    # 估价公式：曼哈顿距离
    def manhattan(self, end_node):
        # 终点坐标 减 当前节点坐标，abs是取绝对值
        self.h = (abs(end_node.point.x - self.point.x) + abs(end_node.point.y - self.point.y)) * 10

    def set_g(self, g):
        self.g = g


class AStar:
    """A* 算法"""
    def __init__(self, map2d, start_node, end_node):
        """
        :param map2d: 寻路数组，也就是地图
        :param start_node: 寻路开始节点
        :param end_node: 寻路的终点
        """
        self.open_list = []
        self.close_list = []
        self.map2d = map2d
        self.start_node = start_node
        self.end_node = end_node
        # 当前处理的节点，初始化当前节点为开始节点
        self.current_node = start_node
        # 最后生成的最短路径
        self.path_list = []

    def get_min_node(self):
        """
        :return: 获取open list 中F值最小的节点
        """
        node_temp = self.open_list[0]
        for node in self.open_list:
            if node.g + node.h < node_temp.g + node_temp.h:
                node_temp = node
        return node_temp

    def node_in_open(self, node):
        """
        :param node: 寻找到的node
        :return: 判断当前节点是否在 open list 中
        """
        for n in self.open_list:
            if n.point.x == node.point.x and n.point.y == node.point.y:
                return True
        return False

    def node_in_close(self, node):
        """
        :param node: 寻找到的node
        :return: 判断当前节点是否在 close list 中
        """
        for n in self.close_list:
            if n.point.x == node.point.x and n.point.y == node.point.y:
                return True
        return False

    def end_in_open(self):
        """
        :return: 判断终点是否在 open list 中
        """
        for n in self.open_list:
            if n.point.x == self.end_node.point.x and n.point.y == self.end_node.point.y:
                return True
        return False

    def get_node(self, node):
        """ 从open list 中获取节点 ?"""
        for node_temp in self.open_list:
            if node_temp.point.x == node.point.x and node_temp.point.y == node.point.y:
                return node_temp

    def search_node(self, node):
        """
        :param node:
        :return:
        """
        # 忽略地图障碍和封闭列表
        if not self.map2d.is_pass(node.point):
            return False
        if self.node_in_close(node):
            return False
        # G值计算
        if abs(node.point.x - self.current_node.point.x) == 1 and abs(node.point.y - self.current_node.point.y) == 1:
            g_temp = 14
        else:
            g_temp = 10

        # 节点不在open list中，则加入 open list
        if not self.node_in_open(node):
            node.set_g(g_temp + self.current_node.g)
            # 计算H值
            node.manhattan(self.end_node)
            self.open_list.append(node)
            node.parent = self.current_node
        else:
            # 如果节点在open list中，判断 current_node 到当前点的G值是否要小些, 如果要小些，则重新计算g值，并且改变父节点
            node_temp = self.get_node(node)
            if self.current_node.g + g_temp < node_temp.g:
                node_temp.g = self.current_node.g + g_temp
                node_temp.parent = self.current_node

    def find_near(self):
        """
        :return: 搜索节点周围的点，拐角处无法直接到达
        (x-1, y-1) (x-1, y) (x-1, y+1)
        (x  , y-1) (x  , y) (x  , y+1)
        (x+1, y-1) (x+1, y) (x-1, y+1)
        """
        x = self.current_node.point.x
        y = self.current_node.point.y

        # 查找上下左右
        self.search_node(Node(Point(x - 1, y)))
        self.search_node(Node(Point(x + 1, y)))
        self.search_node(Node(Point(x, y - 1)))
        self.search_node(Node(Point(x, y + 1)))

        # 判断上边和左边是否有效
        if self.map2d.is_pass(Point(x - 1, y)) and self.map2d.is_pass(Point(x, y - 1)):
            self.search_node(Node(Point(x - 1, y - 1)))

        # 判断上边和右边是否有效
        if self.map2d.is_pass(Point(x - 1, y)) and self.map2d.is_pass(Point(x, y + 1)):
            self.search_node(Node(Point(x - 1, y + 1)))

        # 判断左边和下边是否有效
        if self.map2d.is_pass(Point(x, y - 1)) and self.map2d.is_pass(Point(x + 1, y)):
            self.search_node(Node(Point(x + 1, y - 1)))

        # 判断下边和右边有效
        if self.map2d.is_pass(Point(x + 1, y)) and self.map2d.is_pass(Point(x, y + 1)):
            self.search_node(Node(Point(x + 1, y + 1)))

    def start(self):
        # 将初始节点加入开放列表
        self.start_node.manhattan(self.end_node)
        self.start_node.set_g(0)
        self.open_list.append(self.start_node)

        while True:
            # 获取当前开放列表里F值最小的节点
            # 并把它添加到封闭列表，从开发列表删除它
            self.current_node = self.get_min_node()
            self.close_list.append(self.current_node)
            self.open_list.remove(self.current_node)

            self.find_near()

            # 检验是否结束
            if self.end_in_open():
                node_temp = self.get_node(self.end_node)
                while True:
                    self.path_list.append(node_temp)
                    if node_temp.parent:
                        node_temp = node_temp.parent
                    else:
                        return True
            elif len(self.open_list) == 0:
                return False

    def set_result_path(self):
        """设置结束路径"""
        for node in self.path_list:
            self.map2d.set_map(node.point)


class Map2d:
    """地图数据"""
    def __init__(self):
        self.data = [
            list("########################################"),
            list("#**************************************#"),
            list("#******#######################*#########"),
            list("#******#*********#*********************#"),
            list("#******#*****#***#***#########*#########"),
            list("#******#*****#***#***#*******#*********#"),
            list("#************#***#***#*******#*********#"),
            list("#******#*****#***#***#*******#*********#"),
            list("#******#*****#*******#*******#*********#"),
            list("########################################"),
        ]

        # 地图的宽, 高, 可以通过的标志, 已经最后生成路径用的标志
        self.width = 40
        self.high = 10
        self.pass_tag = '*'
        self.path_tag = 'o'

    def show_map(self):
        """
        :return: 显示地图
        """
        for x in range(self.high):
            for y in range(self.width):
                print(self.data[x][y], end="")
            print(" ")

    def set_map(self, point):
        """
        :param point: 节点
        :return: 设置最后生成的路径
        """
        self.data[point.x][point.y] = self.path_tag

    def is_pass(self, point):
        """
        :param point: 坐标
        :return: 判断节点是否有效
        """
        if (point.x < 0 or point.x > self.high - 1) or (point.y < 0 or point.y > self.width - 1):
            return False

        # 判断对应坐标是否可以通行
        if self.data[point.x][point.y] == self.pass_tag:
            return True


if __name__ == '__main__':
    map_test = Map2d()
    map_test.show_map()

    start = Node(Point(1, 1))
    end = Node(Point(8, 38))
    a_star = AStar(map_test, start, end)
    print("A* 开始:")

    if a_star.start():
        a_star.set_result_path()
        map_test.show_map()
        print(len(a_star.path_list))
    else:
        print("没有找到路径")


