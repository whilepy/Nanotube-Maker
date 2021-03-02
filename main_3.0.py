import class_Pipe as p
import class_Atom as a
import class_PrimitiveCell as pc
import shutil


# import matplotlib.pyplot as plt
# import mpl_toolkits.mplot3d
# from matplotlib.pyplot import MultipleLocator

# 体系A SnS
# at1 = a.Atom(1, 'Sn', [1.88207746, 1.08661793, 10.71733142], [2])
# at2 = a.Atom(2, 'S', [3.76415492, 2.17323586, 9.26308433], [1])
# pc1 = pc.PrimitiveCell([at1, at2], 3.764155, 3.764155, 60)

# 体系B P
# at1 = a.Atom(1, 'P', [1.64999999, 0.95262794, 0.61699230], [2])
# at2 = a.Atom(2, 'P', [3.29999998, 1.90525588, -0.61699230], [1])
# pc1 = pc.PrimitiveCell([at1, at2], 3.3, 3.3, 60)


def mkdir(path):
    import os
    path = path.strip()
    path = path.rstrip("\\")
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print (path+' 创建成功')
        return True
    else:
        print (path+' 目录已存在')
        return False
def readfile(filename):
    f = open(filename, 'r')
    at_list = []
    content = f.readlines()
    if len(content) != 3:
        print('预设文件格式有误!请仔细检查后重试')
        return [], -1
    try:
        a0 = -1
        for i, item in enumerate(content):
            if i <= 1:
                msg = item.split(',')
                if len(msg) != 6:
                    print('预设文件格式有误!请仔细检查后重试')
                    return [], -1
                else:
                    at = a.Atom(int(msg[0]), msg[1], [eval(msg[2]), eval(msg[3]), eval(msg[4])], [int(msg[5])])
                    at_list.append(at)
            else:
                a0 = eval(item)
        return at_list, a0
    except Exception as e:
        print('预设文件格式有误!请仔细检查后重试')
        print("出现如下异常%s" % e)
        return [], -1


while True:
    print('输入指令进行下一步操作[1.快速生成模式 2.批量产出模式 其他.退出]:')
    cmd = input()
    if cmd == '1':
        file_name = input("请输入预设文件名:")
        at_list, a0 = readfile(file_name)
        if len(at_list) != 0:
            pc1 = pc.PrimitiveCell(at_list, a0, a0, 60)
            try:
                n, m = map(int, input('请输入n m(空格分隔):').split(' '))
                p1 = p.Pipe(n, m, pc1)
                h = int(input('请输入高位编号(1或2):'))
                x_array, y_array, z_array, r = p1.get_pipe(h)
                # ax = plt.subplot(projection='3d')  # 创建一个三维的绘图工程
                # ax.set_title('3d_image_show')  # 设置本图名称
                # ax.scatter(x_array, y_array, z_array, c='r')  # 绘制数据点 c: 'r'红色，'y'黄色，等颜色
                # ax.set_xlabel('X')  # 设置x坐标轴
                # ax.set_ylabel('Y')  # 设置y坐标轴
                # ax.set_zlabel('Z')  # 设置z坐标轴
                # ax.set_xlim(-20, 20)
                # ax.set_ylim(-20, 20)
                # ax.set_zlim(-20, 20)
                p1.outputPipe2pdb(r)
                print('文件{}_{}_output.pdb已经生成至当前目录\n如果能在论文中答谢将是最大支持(≧▽≦)/！'.format(n, m))
                # plt.show()
            except Exception as e:
                print('生成失败！\n如有问题请联系作者:896180667@qq.com')
                print("出现如下异常%s" % e)
    if cmd == '2':
        deepth = 10
        filelist = ['GeS.txt', 'GeSe.txt', 'SnS.txt', 'SnSe.txt']
        for f in filelist:
            at_list, a0 = readfile(f)
            mkdir(f[:-4])
            if len(at_list) != 0:
                pc1 = pc.PrimitiveCell(at_list, a0, a0, 60)
                for h in range(2):
                    path = '{}\\{}'.format(f[:-4], h + 1)
                    mkdir(path)
                    for i in range(deepth + 1):
                        for j in range(deepth + 1):
                            if i + j < 5:
                                continue
                            try:
                                # n, m = map(int, input('请输入n m(空格分隔):').split(' '))
                                p1 = p.Pipe(i, j, pc1)
                                # h = int(input('请输入高位编号(1或2):'))

                                x_array, y_array, z_array, r = p1.get_pipe(h+1)
                                p1.outputPipe2pdb(r)
                                shutil.move('{}_{}_output.pdb'.format(i, j), path)
                            except Exception as e:
                                print('生成失败！\n如有问题请联系作者:896180667@qq.com')
                                print("出现如下异常%s" % e)
    else:
        break
