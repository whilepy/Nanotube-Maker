from class_cell_struct import CellStruct as cs


# bSnSe_700 = cs({'Sn': 0, 'Se': 1}, 3.9347967142857, 0.77402643, 7, 0)
# bSnSe_770 = cs({'Sn': 0, 'Se': 1}, 3.9347967142857, 0.77402643, 7, 7)
# bGeSe_700 = cs({'Se': 0, 'Ge': 1}, 3.674415, 0.721522865, 7, 0)
# bGeSe_770 = cs({'Se': 0, 'Ge': 1}, 3.674415, 0.721522865, 7, 7)
# bSnS_700 = cs({'S': 0, 'Sn': 1}, 3.764155, 0.727123545, 7, 0)
# bSnS_770 = cs({'S': 0, 'Sn': 1}, 3.764155, 0.727123545, 7, 7)
# bGeS_700 = cs({'S': 0, 'Ge': 1}, 3.487187, 0.678384995, 7, 0)
# bGeS_770 = cs({'S': 0, 'Ge': 1}, 3.487187, 0.678384995, 7, 7)
# bP_700 = cs({'P': 0}, 3.3, 0.61684874212, 7, 0)
# bP_770 = cs({'P': 0}, 3.3, 0.61747918542, 7, 7)
# bSnSe_770.output2file('res.pdb', 1, 0, 2)
while True:
    print('输入指令进行下一步操作[1.快速生成模式 其他.退出]:')
    cmd = input()
    if cmd == '1':
        e = {}
        e_name = input("请输入元素名称(空格分隔):").split(' ')
        e_index = list(map(int, input('请输入元素高低位序号(从0开始,空格分隔):').split(' ')))

        if len(e_name) != len(e_index):
            print('元素与序号不对应!')
            break
        else:
            for i, item in enumerate(e_name):
                e[item] = e_index[i]
        length, thickness = map(float, input('请输入原胞长度与半厚度(空格分开):').split(' '))
        m, n = map(int, input('请输入m n:').split(' '))
        ob = cs(e, length, thickness, m, n)
        if ob.output2file('{}_{}_output.pdb'.format(m, n)):
            print('文件{}_{}_output.pdb已经生成至当前目录'.format(m, n))
    else:
        break
