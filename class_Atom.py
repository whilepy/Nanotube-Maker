class Atom:
    def __init__(self, index, element, xyz, connect):
        self.index = index  # 原子编号
        self.element = element  # 原子元素名字
        self.xyz = xyz  # 原子当前坐标
        self.connect = connect  # 原子连接情况

    def get_index(self):
        return self.index

    def get_element(self):
        return self.element

    def get_xyz(self):
        return self.xyz

    def get_connect(self):
        return self.connect

    def set_index(self, index):
        self.index = index

    def set_element(self, element):
        self.element = element

    def set_xyz(self, xyz):
        self.xyz = xyz

    def set_connect(self, connect):
        self.connect = connect
