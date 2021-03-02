import numpy as np
import datetime
import traceback


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


class CellStruct:
    def __init__(self, elements, const_length, const_thickness, m, n, const_vertical=20):
        self.elements = elements  # 元素字典{'Sn':1,'Se':2} 从1开始，数值越大，vertical分量越大
        self.const_length = const_length  # 暂时为原胞a的值，后期可以改为键长
        self.const_thickness = const_thickness  # vertical分量上下两层的差值的一半，厚度的一半
        # self.const_axial = const_axial  # 为一个四元素列表，表示axial分量的四个值
        self.const_vertical = const_vertical  # crystal晶格参数第三个分量
        # self.const_extent_init = const_extent_init  # 为一个二元素列表，表示ext方向的初始值
        self.m = m
        self.n = n
        self.mode = 0  # mode = 0 :xx0;# mode = 1 :x00
        self.perimeter = 0  # 周长
        self.num_atom = m * 4  # 原子个数
        p1 = self.const_length * 0.577272727
        p2 = self.const_length * 1.443333333
        p3 = self.const_length * 1.154848484
        p4 = self.const_length * 0.288787878
        p1_ = self.const_length * 0.5
        if m == n:
            self.mode = 0
            self.perimeter = m * np.sqrt(3) * self.const_length
            self.const_axial = []
            self.const_extent_init = [p1, p1 / 2]
            self.const_axial = [0, p1_, p1_, 0]
        elif n == 0:
            self.mode = 1
            self.perimeter = m * self.const_length
            self.const_extent_init = [0, 0]
            self.const_axial = [p1, p2, p3, p4]
        else:
            pass
        self.radius = self.perimeter / 2 / np.pi
        self.tensile_ratio = [(self.radius - self.const_thickness) / self.radius,
                              (self.radius + self.const_thickness) / self.radius]

    def get_perimeter(self):
        return self.perimeter

    def get_radius(self):
        return self.radius

    def get_mode(self):
        return self.mode

    def get_tension_ratio(self):
        return self.tensile_ratio

    def get_array_crystal(self):
        if self.mode == 0:
            return np.array([self.perimeter, np.sqrt(3) * self.const_length, self.const_vertical, 90, 90, 90])
        elif self.mode == 1:
            return np.array([self.perimeter, self.const_length, self.const_vertical, 90, 90, 90])
        else:
            pass

    def get_array_scale(self):
        a = self.get_array_crystal()[0:3]
        b = np.ones(3) / a
        return b

    def get_array_xyz_crystal(self):
        array_xyz_init = np.zeros((self.num_atom, 3))
        array_xyz_init = array_xyz_init.astype('float64')
        # 对第1列初始化
        if self.mode == 1:
            array_ext_init = np.arange(0, self.perimeter, self.const_length / 2).reshape((int(self.num_atom / 2)))
            array_xyz_init[:int(self.num_atom / 2), 0] = array_ext_init
            array_xyz_init[int(self.num_atom / 2):, 0] = array_ext_init
        elif self.mode == 0:
            array_ext_init_1 = np.arange(self.const_extent_init[0], self.perimeter,
                                         np.sqrt(3) * self.const_length / 2).reshape((int(self.num_atom / 2)))
            array_ext_init_2 = np.arange(self.const_extent_init[1], self.perimeter,
                                         np.sqrt(3) * self.const_length / 2).reshape((int(self.num_atom / 2)))
            array_xyz_init[:int(self.num_atom / 2), 0] = array_ext_init_1
            array_xyz_init[int(self.num_atom / 2):, 0] = array_ext_init_2
        else:
            pass
        # 对第2列初始化
        list_cell_1 = self.const_axial[0:2]
        list_cell_2 = self.const_axial[2:4]
        list_axi_init_1 = list_cell_1 * int(self.num_atom / 4)
        list_axi_init_2 = list_cell_2 * int(self.num_atom / 4)
        array_xyz_init[:int(self.num_atom / 2), 1] = np.array(list_axi_init_1).reshape((int(self.num_atom / 2)))
        array_xyz_init[int(self.num_atom / 2):, 1] = np.array(list_axi_init_2).reshape((int(self.num_atom / 2)))
        list_vertical_1 = [self.perimeter / 2 / np.pi - self.const_thickness] * int(self.num_atom / 2)
        list_vertical_2 = [self.perimeter / 2 / np.pi + self.const_thickness] * int(self.num_atom / 2)
        # 对第3列初始化
        array_xyz_init[:int(self.num_atom / 2), 2] = np.array(list_vertical_1).reshape((int(self.num_atom / 2)))
        array_xyz_init[int(self.num_atom / 2):, 2] = np.array(list_vertical_2).reshape((int(self.num_atom / 2)))

        return array_xyz_init

    def get_array_xyz_pipe(self):
        a = self.get_array_xyz_crystal()
        # 进行卷管计算

        # 以下是老方法
        # list_atom_index = [0] * int(self.num_atom / 2) + [1] * int(self.num_atom / 2)
        # for i, j in enumerate(a):
        #     j[0] = j[0] * self.tensile_ratio[list_atom_index[i]]
        #     theta = j[0] / j[2]
        #     j[0] = j[2] * np.sin(theta)
        #     j[2] = j[2] * np.cos(theta)
        # return a

        # 以下是新方法
        array_tension_ratio = np.array([self.tensile_ratio[0]] * int(self.num_atom / 2) +
                                       [self.tensile_ratio[1]] * int(self.num_atom / 2)).reshape(self.num_atom)
        a[:, 0] = a[:, 0] * array_tension_ratio
        array_theta = a[:, 0] / a[:, 2]
        a[:, 0] = a[:, 2] * np.sin(array_theta)
        a[:, 2] = a[:, 2] * np.cos(array_theta)
        return a

    def create_str_CRYSTAL(self, dir_e=0, dir_a=1, dir_v=2):
        format_CRYSTAL = 'CRYST1{:>9.3f}{:>9.3f}{:>9.3f}{:>7.2f}{:>7.2f}{:>7.2f} P1\n'
        a = self.get_array_crystal()
        res_CRYSTAL = format_CRYSTAL.format(a[dir_e], a[dir_a], a[dir_v], a[3], a[4], a[5])
        return res_CRYSTAL

    def create_str_SCALE(self, dir_e=0, dir_a=1, dir_v=2):
        a = self.get_array_crystal()
        format_SCALE = 'SCALE1      {:.6f}  0.000000  0.000000        0.00000   \n' \
                       'SCALE2      0.000000  {:.6f}  0.000000        0.00000   \n' \
                       'SCALE3      0.000000  0.000000  {:.6f}        0.00000   \n'
        res_SCALE = format_SCALE.format(1 / a[dir_e], 1 / a[dir_a], 1 / a[dir_v])
        return res_SCALE

    def create_str_ATOM(self, dir_e=0, dir_a=1, dir_v=2):
        a = self.get_array_xyz_pipe()
        format_ATOM = 'ATOM{:>7}{:>4}  MOL     2{:>12.3f}{:>8.3f}{:>8.3f}  1.00  0.00{:>12}    '
        list_str_ATOM = [''] * self.num_atom

        list_elements = sorted(self.elements.items(), key=lambda kv: (kv[1], kv[0]))
        num_elements = len(list_elements)

        if num_elements == 1:
            list_index_elements = [0] * self.num_atom
        elif num_elements == 2:
            list_index_elements = [0] * int(self.num_atom / 2) + [1] * int(self.num_atom / 2)
        else:
            return 'error\n'

        for i in range(self.num_atom):
            e = list_elements[list_index_elements[i]]
            list_str_ATOM[i] = format_ATOM.format(i + 1, e[0] + str(e[1] + 1), a[i][dir_e], a[i][dir_a], a[i][dir_v],
                                                  e[0])
        return '\n'.join(list_str_ATOM) + '\n'

    def create_str_TER(self):
        return 'TER{:>8} \n'.format(self.num_atom + 1)

    def create_str_CONECT(self):
        format_CONECT = 'CONECT{:>5}{:>5}{:>5}{:>5}'
        list_str_CONECT = [''] * self.num_atom
        for i in range(self.num_atom):
            res = self.calculate_CONECT(i + 1)
            list_str_CONECT[i] = format_CONECT.format(res[0], res[1], res[2], res[3]).rstrip()
        return '\n'.join(list_str_CONECT) + '\n'

    def calculate_CONECT(self, i):
        # 该函数用于计算原子连接方式,输入原子编号即可求出对应连接原子编号
        res = [i, '', '', '']  # 此处i为1,2,3,4.....等真实编号
        if self.mode == 0:
            offset = int(self.num_atom / 2)
            if i == 1:
                res[1] = i + offset - 1
                res[2] = i + offset
            elif i == offset:
                res[1] = i + offset
                res[2] = 1
            elif i < offset:
                res[1] = i + offset + 1
                res[2] = i + offset
            elif i >= offset + 3:
                res[1] = i - offset - 1
                res[2] = i - offset
            else:
                res[1] = i - offset
        elif self.mode == 1:
            offset = int(self.num_atom / 2)
            if i == 1:
                res[1] = offset
            elif i == 2:
                res[1] = i + offset
                res[2] = i + offset + 1
            elif i == offset + 1:
                res[1] = self.num_atom
            elif i == offset:
                res[1] = i + offset
                res[2] = 1
                res[3] = i + offset - 1
            elif i == offset + 2:
                res[1] = i - offset
                res[2] = i - offset + 1
            elif i % 2 == 1:
                if i < offset:
                    res[1] = i + offset + 1
                    res[2] = i + offset - 1
                else:
                    res[1] = i - offset - 1
                    res[2] = i - offset + 1
            else:
                if i < offset:
                    res[1] = i + offset
                    res[2] = i + offset + 1
                    res[3] = i + offset - 1
                else:
                    res[1] = i - offset - 1
                    res[2] = i - offset
                    res[3] = i - offset + 1
        else:
            pass
        return res

    def output2file(self, filename, dir_e=0, dir_a=1, dir_v=2):
        try:
            f = open(filename, 'w')
            res_REMARK = create_str_REMARK()
            res_CRYSTAL = self.create_str_CRYSTAL(dir_e, dir_a, dir_v)
            res_ORIGX = create_str_ORIGX()
            res_SCALE = self.create_str_SCALE(dir_e, dir_a, dir_v)
            res_ATOM = self.create_str_ATOM(dir_e, dir_a, dir_v)
            res_TER = self.create_str_TER()
            res_CONECT = self.create_str_CONECT()
            res_END = 'END\n'
            f.write(res_REMARK)
            f.write(res_CRYSTAL)
            f.write(res_ORIGX)
            f.write(res_SCALE)
            f.write(res_ATOM)
            f.write(res_TER)
            f.write(res_CONECT)
            f.write(res_END)
            f.close()
            return True
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            print('traceback.print_exc():')
            traceback.print_exc()
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            return False
