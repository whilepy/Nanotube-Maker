import numpy as np
import math
import datetime
import os


def main():
    while True:
        print('输入指令进行下一步操作[1.快速生成模式 2.文件转化模式 其他.退出]:')
        cmd = input()
        if cmd == '1':
            m, n = map(int, input('请输入m n:').split(' '))
            print(m,n)
            if createPipe(m, n):
                print('文件{}_{}_output.pdb已经生成至当前目录'.format(m, n))
        elif cmd == '2':
            filename = input('请输入文件名:')
            if transFile(filename):
                print('文件' + filename[:-4] + '_output.pdb已经生成至当前目录')
        else:
            break


def transFile(filename, dir_a=0, dir_b=1, dir_c=2):
    filename_input = filename
    filename_output = filename_input[:-4] + '_output.pdb'
    extension_direction_plane = dir_a  # 默认平面的延展方向为x
    axial_direction_pipe = dir_b  # 默认管的轴线方向为y
    vertical_direction_plane = dir_c  # 垂直平面的坐标轴方向Z
    if not os.path.exists(filename_input):
        print('指定文件不存在!')
        return False
    with open(filename_input, 'r') as f:
        list_content = f.readlines()

    if len(list_content) == 0:
        print('该文件为空!')
        return False
    elif 'REMARK   Materials Studio PDB file' not in list_content[0]:
        print('此文件不是本程序可以识别的pdb文件!')
        return False
    else:
        list_line = ' '.join(list_content[2].split()).split(' ')
        list_CRYST_float = list(map(float, list_line[1:7]))  # 读取晶格信息
        perimeter = list_CRYST_float[0]
        list_XYZ_float = []
        list_tensile_ratio = []
        list_atom_index = []
        index = -1
        radius = perimeter / 2 / math.pi
        for i in list_content:
            list_line = ' '.join(i.split()).split(' ')
            if list_line[0] == 'ATOM':
                list_cell_float = list(map(float, list_line[5:8]))  # 读取原子坐标信息
                tensile_ratio = list_cell_float[vertical_direction_plane] / radius
                list_XYZ_float.append(list_cell_float)
                if tensile_ratio not in list_tensile_ratio:
                    list_tensile_ratio.append(tensile_ratio)
                    index += 1
                list_atom_index.append(index)

        if index > 2:
            print("坐标轴设置错误,请重新设置!")
            return False

        array_XYZ_float = np.array(list_XYZ_float)
        # print(list_CRYST_float)
        # print(list_tensile_ratio)
        for i, j in enumerate(array_XYZ_float):
            j[extension_direction_plane] = j[extension_direction_plane] * list_tensile_ratio[list_atom_index[i]]
            theta = j[extension_direction_plane] / j[vertical_direction_plane]
            j[extension_direction_plane] = j[vertical_direction_plane] * math.sin(theta)
            j[vertical_direction_plane] = j[vertical_direction_plane] * math.cos(theta)
        array_XYZ_pipe = np.around(array_XYZ_float, 3)
        f = open(filename_output, 'w')
        index = 0
        for i, j in enumerate(list_content):
            list_line = ' '.join(j.split()).split(' ')
            if list_line[0] == 'ATOM':
                line_content = 'ATOM{:>7}  {}  {}     {}      {:.3f}  {:.3f}  {:.3f}  {}  {}           {}    \n' \
                    .format(list_line[1], list_line[2], list_line[3], list_line[4],
                            array_XYZ_pipe[index][0], array_XYZ_pipe[index][1], array_XYZ_pipe[index][2],
                            list_line[8], list_line[9], list_line[10])
                # line_content = 'ATOM\t{}\t{}\t{}\t\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'\
                #               .format(list_line[1], list_line[2], list_line[3], list_line[4],
                #                       array_XYZ_pipe[index][0], array_XYZ_pipe[index][1], array_XYZ_pipe[index][2],
                #                       list_line[8], list_line[9], list_line[10])
                # line_content = 'ATOM\t{}\t{}\t{}\t\t{}\t{}\t{}\t{}\t{}\t{}{:>11}\n'\
                #               .format(list_line[1], list_line[2], list_line[3], list_line[4],
                #                       array_XYZ_pipe[index][0], array_XYZ_pipe[index][1], array_XYZ_pipe[index][2],
                #                       list_line[8], list_line[9], list_line[10])
                f.write(line_content)
                index += 1
            elif i == 1:
                now_time = datetime.datetime.now()
                f.write('REMARK   Created:  ' + now_time.strftime('%a %b %d %H:%M:%S +0800 %Y\n'))
            else:
                f.write(j)
        f.close()
        return True


def createPipe(m, n, dir_a=0, dir_b=1, dir_c=2):
    const_length = 3.30
    const_vertical = 19.80
    list_thickness = [0.61684874212, 0.61747918542]  # 厚度的二分之一,前者xx0，后者x00
    list_axial = [[0, 1.65, 1.65, 0], [1.905, 4.763, 3.811, 0.953]]  # 中间的分量
    num_atom = m * 4
    now_time = datetime.datetime.now()
    str_time = now_time.strftime('%a %b %d %H:%M:%S +0800 %Y\n')
    res_REMARK = 'REMARK   Materials Studio PDB file\nREMARK   Created:  {}'.format(str_time)
    res_ORIGX = 'ORIGX1      1.000000  0.000000  0.000000        0.00000\n' \
                'ORIGX2      0.000000  1.000000  0.000000        0.00000\n' \
                'ORIGX3      0.000000  0.000000  1.000000        0.00000\n'
    res_TER = 'TER{:>8} \n'.format(num_atom + 1)
    format_CRYST = 'CRYST1{:>9.3f}{:>9.3f}{:>9.3f}  90.00  90.00  90.00 P1\n'
    format_SCALE = 'SCALE1      {:.6f}  0.000000  0.000000        0.00000   \n' \
                   'SCALE2      0.000000  {:.6f}  0.000000        0.00000   \n' \
                   'SCALE3      0.000000  0.000000  {:.6f}        0.00000   \n'
    format_ATOM = 'ATOM{:>7}  P1  MOL     2{:>12.3f}{:>8.3f}{:>8.3f}  1.00  0.00           P    '
    format_CONECT = 'CONECT{:>5}{:>5}{:>5}{:>5}'
    filename_output = '{}_{}_output.pdb'.format(m, n)
    extension_direction_plane = dir_a  # 默认平面的延展方向为x
    axial_direction_pipe = dir_b  # 默认管的轴线方向为y
    vertical_direction_plane = dir_c  # 垂直平面的坐标轴方向Z
    mode = 0  # 卷管模式 0:xx0 1:x00
    list_const_CRYST = [0, 0, 0]  # 晶格常数
    if m == n:
        perimeter = m * const_length * math.sqrt(3)
        mode = 0
        list_const_CRYST[extension_direction_plane] = perimeter
        list_const_CRYST[axial_direction_pipe] = const_length
        list_const_CRYST[vertical_direction_plane] = const_vertical
        thickness = list_thickness[0]
    elif n == 0 and m != 0:
        perimeter = m * const_length
        mode = 1
        list_const_CRYST[extension_direction_plane] = perimeter
        list_const_CRYST[axial_direction_pipe] = const_length * math.sqrt(3)
        list_const_CRYST[vertical_direction_plane] = const_vertical
        thickness = list_thickness[1]
    else:
        print('暂时不支持该模式!')
        return False
    res_CRYST = format_CRYST.format(list_const_CRYST[0], list_const_CRYST[1], list_const_CRYST[2])
    res_SCALE = format_SCALE.format(1 / list_const_CRYST[0], 1 / list_const_CRYST[1], 1 / list_const_CRYST[2])
    # 初始化坐标矩阵
    array_XYZ_init = np.zeros((num_atom, 3))
    array_XYZ_init = array_XYZ_init.astype('float64')
    if mode == 1:
        array_ext_init = np.arange(0, perimeter, const_length / 2).reshape((int(num_atom / 2)))
        array_XYZ_init[:int(num_atom / 2), extension_direction_plane] = array_ext_init
        array_XYZ_init[int(num_atom / 2):, extension_direction_plane] = array_ext_init
    else:
        array_ext_init_1 = np.arange(1.905, perimeter, math.sqrt(3) * const_length / 2).reshape((int(num_atom / 2)))
        array_ext_init_2 = np.arange(0.953, perimeter, math.sqrt(3) * const_length / 2).reshape((int(num_atom / 2)))
        array_XYZ_init[:int(num_atom / 2), extension_direction_plane] = array_ext_init_1
        array_XYZ_init[int(num_atom / 2):, extension_direction_plane] = array_ext_init_2
    list_cell_1 = list_axial[mode][0:2]
    list_cell_2 = list_axial[mode][2:4]
    list_axi_init_1 = list_cell_1 * int(num_atom / 4)
    list_axi_init_2 = list_cell_2 * int(num_atom / 4)
    array_XYZ_init[:int(num_atom / 2), axial_direction_pipe] = np.array(list_axi_init_1).reshape((int(num_atom / 2)))
    array_XYZ_init[int(num_atom / 2):, axial_direction_pipe] = np.array(list_axi_init_2).reshape((int(num_atom / 2)))
    list_vertical_1 = [perimeter / 2 / math.pi - thickness] * int(num_atom / 2)
    list_vertical_2 = [perimeter / 2 / math.pi + thickness] * int(num_atom / 2)
    array_XYZ_init[:int(num_atom / 2), vertical_direction_plane] = np.array(list_vertical_1).reshape(
        (int(num_atom / 2)))
    array_XYZ_init[int(num_atom / 2):, vertical_direction_plane] = np.array(list_vertical_2).reshape(
        (int(num_atom / 2)))
    list_atom_index = [0] * int(num_atom / 2) + [1] * int(num_atom / 2)
    # 进行卷管计算
    radius = perimeter / 2 / math.pi
    list_tensile_ratio = [(radius - thickness) / radius, (radius + thickness) / radius]
    list_str_ATOM = [''] * num_atom
    list_str_CONECT = [''] * num_atom
    for i, j in enumerate(array_XYZ_init):
        j[extension_direction_plane] = j[extension_direction_plane] * list_tensile_ratio[list_atom_index[i]]
        theta = j[extension_direction_plane] / j[vertical_direction_plane]
        j[extension_direction_plane] = j[vertical_direction_plane] * math.sin(theta)
        j[vertical_direction_plane] = j[vertical_direction_plane] * math.cos(theta)
        list_str_ATOM[i] = format_ATOM.format(i + 1, j[0], j[1], j[2])
        if mode == 0:
            offset = int(num_atom / 2)
            if i == 0:
                list_str_CONECT[i] = format_CONECT.format(i + 1, i + offset, i + offset + 1, '').rstrip()
            elif i + 1 == offset:
                list_str_CONECT[i] = format_CONECT.format(i + 1, i + offset + 1, 1, '').rstrip()
            elif i + 1 <= offset:
                list_str_CONECT[i] = format_CONECT.format(i + 1, i + offset + 1, i + offset + 2, '').rstrip()
            elif i + 1 >= offset + 3:
                list_str_CONECT[i] = format_CONECT.format(i + 1, i - offset, i - offset + 1, '').rstrip()
            else:
                list_str_CONECT[i] = format_CONECT.format(i + 1, i + 1 - offset, '', '').rstrip()
        else:
            offset = int(num_atom / 2)
            if i == 0:
                list_str_CONECT[i] = format_CONECT.format(i + 1, offset, '', '').rstrip()
            elif i == 1:
                list_str_CONECT[i] = format_CONECT.format(i + 1, i + offset + 1, i + offset + 2, '').rstrip()
            elif i == offset:
                list_str_CONECT[i] = format_CONECT.format(i + 1, num_atom, '', '').rstrip()
            elif i == offset - 1:
                list_str_CONECT[i] = format_CONECT.format(i + 1, i + 1 + offset, 1, i + offset).rstrip()
            elif i == offset + 1:
                list_str_CONECT[i] = format_CONECT.format(i + 1, i + 1 - offset, i + 2 - offset, '').rstrip()
            elif (i + 1) % 2 == 1:
                if i + 1 < offset:
                    list_str_CONECT[i] = format_CONECT.format(i + 1, i + 2 + offset, i + offset, '').rstrip()
                else:
                    list_str_CONECT[i] = format_CONECT.format(i + 1, i - offset, i + 2 - offset, '').rstrip()
            else:
                if i + 1 < offset:
                    list_str_CONECT[i] = format_CONECT.format(i + 1, i + 1 + offset, i + 2 + offset,
                                                              i + offset).rstrip()
                else:
                    list_str_CONECT[i] = format_CONECT.format(i + 1, i - offset, i + 1 - offset,
                                                              i + 2 - offset).rstrip()
            #   整合数据输出
    f = open(filename_output, 'w')
    f.write(res_REMARK)
    f.write(res_CRYST)
    f.write(res_ORIGX)
    f.write(res_SCALE)
    f.write('\n'.join(list_str_ATOM) + '\n')
    f.write(res_TER)
    f.write('\n'.join(list_str_CONECT) + '\n')
    f.write('END\n')
    f.close()
    return True


main()
