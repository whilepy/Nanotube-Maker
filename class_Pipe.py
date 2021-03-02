import class_PrimitiveCell as pc
import numpy as np
import datetime


def get_max_com_divisor(a, b):
    if a < b:
        a, b = b, a  # 保证a大于b
    while a % b != 0:
        a, b = b, a % b
    return b


def create_str_REMARK():
    now_time = datetime.datetime.now()
    str_time = now_time.strftime('%a %b %d %H:%M:%S +0800 %Y\n')
    res_REMARK = 'REMARK   Materials Studio PDB file\nREMARK   Created:  {}'.format(str_time)
    return res_REMARK


def create_str_ORIGX():
    res_ORIGX = 'ORIGX1      1.000000  0.000000  0.000000        0.00000\n' \
                'ORIGX2      0.000000  1.000000  0.000000        0.00000\n' \
                'ORIGX3      0.000000  0.000000  1.000000        0.00000\n'
    return res_ORIGX


class Pipe:
    pri_cell: pc

    def __init__(self, n, m, pri_cell):
        self.m = m
        self.n = n
        self.pri_cell = pri_cell
        self.perimeter = 0
        self.length = 0
        self.radius = 0
        self.thickness = 0
        self.tension_ratio = [0, 0]

    def get_pipe(self, high=2):
        high = high - 1
        #   快速构建一个待卷平面,并作一个简单的核对
        num_atoms = len(self.pri_cell.get_atoms())
        atoms_plane_r, list_index = self.get_planeA()
        num = len(atoms_plane_r)
        n = self.n
        m = self.m
        dR = get_max_com_divisor(2 * m + n, 2 * n + m)
        N = 4 * (m * m + n * n + m * n) / dR
        if int(N) != num:
            return False
        # 先对筛选后的原子进行连接状况更新
        # print(list_index)
        for i, item in enumerate(atoms_plane_r):
            connect = item.get_connect()
            connect_new = []
            for j in connect:
                if j in list_index:
                    connect_new.append(j)
            item.set_connect(connect_new)
        #  此处需要对编号重编
        for i, item in enumerate(atoms_plane_r):
            item.set_index(i + 1)
            connect = item.get_connect()
            connect_new = [0] * len(connect)
            for j, item_ in enumerate(connect):
                index = list_index.index(item_)
                connect_new[j] = index + 1
            item.set_connect(connect_new)
        #   卷管上下层进行拉伸压缩变化,并且对纵坐标进行平移,进行弯曲操作
        # high_element = self.pri_cell.get_atoms()[high].get_element()
        x_list = []
        y_list = []
        z_list = []
        if num_atoms == 2:
            for i, item in enumerate(atoms_plane_r):
                [x, y, z] = item.get_xyz()
                if list_index[i] %2 != high:
                    x = x * self.tension_ratio[1]  # 拉伸
                    z = self.radius + self.thickness / 2
                else:
                    x = x * self.tension_ratio[0]  # 压缩
                    z = self.radius - self.thickness / 2
                beta = x / z
                x = np.sin(beta) * z
                z = np.cos(beta) * z
                x_list.append(x)
                y_list.append(y)
                z_list.append(z)
                # print(x, y, z)
                item.set_xyz([x, y, z])
        return np.array(x_list), np.array(y_list), np.array(z_list), atoms_plane_r

    def outputPipe2pdb(self, atoms_pipe):
        filename = '{}_{}_output.pdb'.format(self.n, self.m)
        # 核心部分输出格式
        format_CRYSTAL = 'CRYST1{:>9.3f}{:>9.3f}{:>9.3f}{:>7.2f}{:>7.2f}{:>7.2f} P1\n'
        format_SCALE = 'SCALE1      {:.6f}  0.000000  0.000000        0.00000   \n' \
                       'SCALE2      0.000000  {:.6f}  0.000000        0.00000   \n' \
                       'SCALE3      0.000000  0.000000  {:.6f}        0.00000   \n'
        format_ATOM = 'ATOM{:>7}{:>4}  MOL     2{:>12.3f}{:>8.3f}{:>8.3f}  1.00  0.00{:>12}    '
        format_TER = 'TER{:>8} \n'
        format_CONECT = 'CONECT{:>5}{:>5}{:>5}{:>5}'
        # 构造常规信息
        str_REMARK = create_str_REMARK()
        str_ORIGX = create_str_ORIGX()
        # 构造出CRYSTAL信息
        str_CRYSTAL = format_CRYSTAL.format(self.perimeter, self.length, 20, 90, 90, 90)
        # 构造出SCALE信息
        str_SCALE = format_SCALE.format(1 / self.perimeter, 1 / self.length, 1 / 20)
        # 构造出ATOM信息和CONNECT信息
        num_atoms = len(atoms_pipe)
        list_str = [' '] * num_atoms
        list_str_ = [' '] * num_atoms
        for i, item in enumerate(atoms_pipe):
            e = item.get_element()
            id_ = self.pri_cell.get_id_by_element(e)
            [x, y, z] = item.get_xyz()
            list_str[i] = format_ATOM.format(item.get_index(), e + str(id_), x, y, z, e)
            # 分界线-----------------------------
            connect = item.get_connect()
            num_connect = len(connect)
            connect_str = [''] * 3
            for j, item_ in enumerate(connect):
                connect_str[j] = str(item_)
            list_str_[i] = format_CONECT.format(item.get_index(), connect_str[0], connect_str[1], connect_str[2])
        str_ATOM = '\n'.join(list_str) + '\n'
        str_CONNECT = '\n'.join(list_str_) + '\n'
        # 构造TER信息和结束标记
        str_TER = format_TER.format(num_atoms + 1)
        str_END = 'END\n'
        # 写到文件
        f = open(filename, 'w')
        f.write(str_REMARK)
        f.write(str_CRYSTAL)
        f.write(str_ORIGX)
        f.write(str_SCALE)
        f.write(str_ATOM)
        f.write(str_TER)
        f.write(str_CONNECT)
        f.write(str_END)
        f.close()

    def get_plane(self, w=20, h=20):  # 通过平移计算出一个理想平面和连接方案,垂直方向必须为z
        num_atoms = self.pri_cell.get_num_atoms() * w * h
        a1, a2 = self.pri_cell.get_a()
        hw = int(w / 2)
        hh = int(h / 2)
        offset_x = hh * a2 * np.cos(self.pri_cell.angel / 180.0 * np.pi) + hw * a1
        offset_y = hh * a2 * np.sin(self.pri_cell.angel / 180.0 * np.pi)
        array_res = np.zeros((w * h, 2, 3))

        index = 0
        for i in range(w):
            for j in range(h):
                for k, item in enumerate(self.pri_cell.get_atoms()):
                    index += 1
                    # i,j为斜坐标系坐标，通过X=(i-j)sina,Y=(i+j)sina
                    x = j * a2 * np.cos(self.pri_cell.angel / 180.0 * np.pi) + i * a1 + item.get_xyz()[0] - offset_x
                    y = j * a2 * np.sin(self.pri_cell.angel / 180.0 * np.pi) + item.get_xyz()[1] - offset_y
                    z = item.get_xyz()[2]
                    at = pc.atom.Atom(index, item.get_element(), [x, y, z], item.get_connect())
                    array_res[i * h + j][k] = np.array([x, y, z])
        return array_res

    def get_planeA(self):  # 通过平移计算出一个理想平面和连接方案,垂直方向必须为z
        # 初始化
        num_atoms = self.pri_cell.get_num_atoms()
        a1, a2 = self.pri_cell.get_a()
        m = self.m
        n = self.n
        angel = self.pri_cell.angel / 180.0 * np.pi
        if num_atoms == 1:
            self.thickness = 0
        elif num_atoms == 2:
            atoms = self.pri_cell.get_atoms()
            self.thickness = abs(atoms[0].get_xyz()[2] - atoms[1].get_xyz()[2])
        # 计算一些参数 theta角,基矢,向量C,T以及两者对角线矢量diagonal,标准周长,标准半径
        theta = np.arccos((2 * n + m) / (2 * np.sqrt(n * n + m * m + m * n)))
        vector_a1 = np.array([a1, 0])
        vector_a2 = np.array([a2 * np.cos(angel), a2 * np.sin(angel)])
        vector_C = n * vector_a1 + m * vector_a2
        dR = get_max_com_divisor(2 * m + n, 2 * n + m)
        t1 = -(2 * m + n) / dR
        t2 = (2 * n + m) / dR
        vector_T = t1 * vector_a1 + t2 * vector_a2
        # vector_diagonal = vector_C + vector_T
        self.perimeter = np.linalg.norm(vector_C)
        self.length = np.linalg.norm(vector_T)
        self.radius = self.perimeter / 2 / np.pi
        self.tension_ratio = [1 - self.thickness / 2 / self.radius, 1 + self.thickness / 2 / self.radius]
        # 计算区域坐标
        # dia1 = t1 + n
        dia2 = t2 + m
        num_x = int(n) - int(t1)
        index = 0
        at = pc.atom.Atom(index, 'C', [0, 0, 0], [0])
        atoms_plane = [at] * (int(dia2) + 1) * (int(n) - int(t1) + 1) * num_atoms
        for j in range(int(dia2) + 1):
            for i in range(int(t1), int(n) + 1):
                v = self.pcv2cbv(i, j)
                for k, item in enumerate(self.pri_cell.get_atoms()):
                    index += 1
                    connect = []
                    x = v[0] + item.get_xyz()[0]
                    y = v[1] + item.get_xyz()[1]
                    z = item.get_xyz()[2]
                    if index % 2 == 1:
                        connect.append(index + 1)
                        if j != 0:
                            connect.append(index - num_atoms * num_x + 1)
                        if i != int(t1):
                            connect.append(index - 1)
                    else:
                        connect.append(index - 1)
                        if j != int(dia2):
                            connect.append(index + num_atoms * num_x - 1)
                        if i != int(n):
                            connect.append(index + 1)

                    at = pc.atom.Atom(index, item.get_element(), [x, y, z], connect)
                    atoms_plane[index - 1] = at
        atoms_plane_r, list_index = self.plane_atom_screening(theta, vector_C, vector_T, atoms_plane)
        return atoms_plane_r, list_index

    def pcv2cbv(self, n, m):  # 原胞基矢向量转直角坐标系向量
        a1, a2 = self.pri_cell.get_a()
        angel = self.pri_cell.angel / 180.0 * np.pi
        vector_a1 = np.array([a1, 0])
        vector_a2 = np.array([a2 * np.cos(angel), a2 * np.sin(angel)])
        return n * vector_a1 + m * vector_a2

    def cbv2pcv(self, vector):  # 直角坐标系向量转原胞基矢向量
        pass

    def plane_atom_screening(self, theta, vector_c, vector_t, atoms_plane):
        n = self.n
        m = self.m
        dR = get_max_com_divisor(2 * m + n, 2 * n + m)
        N = 4 * (m * m + n * n + m * n) / dR
        x = vector_c[0]
        y = vector_c[1]
        x0 = x * np.cos(-theta) - y * np.sin(-theta)
        y0 = x * np.sin(-theta) + y * np.cos(-theta)
        vector_c_r = np.array([x0, y0])
        x = vector_t[0]
        y = vector_t[1]
        x0 = x * np.cos(-theta) - y * np.sin(-theta)
        y0 = x * np.sin(-theta) + y * np.cos(-theta)
        vector_t_r = np.array([x0, y0])
        # x0_list = []
        # y0_list = []
        atoms_list_r = []
        list_index = []
        for i, item in enumerate(atoms_plane):
            [x, y, z] = item.get_xyz()
            x0 = x * np.cos(-theta) - y * np.sin(-theta)
            y0 = x * np.sin(-theta) + y * np.cos(-theta)
            # if i % 2 == 1:
            #     print(x, y, z)
            #     x0_list.append(x)
            #     y0_list.append(y)
            if 0 <= x0 <= vector_c_r[0] and 0 <= y0 <= vector_t_r[1]:
                item.set_xyz([x0, y0, z])
                atoms_list_r.append(item)
                list_index.append(item.get_index())
                # x0_list.append(x0)
                # y0_list.append(y0)

        # return np.array(x0_list), np.array(y0_list)
        return atoms_list_r, list_index
