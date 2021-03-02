# Nanotube-Maker/纳米管生成程序
This program is used to quickly generate nanotubes with or without thickness.  
傻瓜式操作,只需要设置原胞预设文件,输入手性指数,就能快速得到你想要的管pdb文件,导入MS直接使用。  
目前仅支持单层或者有厚度的原子面进行卷管  
# 原胞预设文件说明
格式:  
<原子1编号>,<原子元素>,<坐标x>,<坐标y>,<坐标z>,<原胞内键连原子编号>  
<原子2编号>,<原子元素>,<坐标x>,<坐标y>,<坐标z>,<原胞内键连原子编号>  
<晶格常数>  
举例1:  
1,P,1.64999999,0.95262794,0.61699230,2  
2,P,3.29999998,1.90525588,-0.61699230,1  
3.30  
举例2:  
1,Ge,1.74359367,1.00666428,10.66859287,2  
2,S,3.48718734,2.01332855,9.31182288,1  
3.487187  
注意:  
1.单层纳米管,仍然当做两类原子,仿造举例1。  
2.由于只支持一/两种元素构造，所以<原子1编号>、<原子2编号>、<原胞内键连原子编号>参数可以仿造例子不要改变或者直接在文件给定的预设文件中修改即可。  
3.坐标默认z轴为原子平面法线方向。  
# 程序输入参数说明
1.选择模式  
  输入1:指定快速生成模式  
  输入2:根据代码内设定的预设文件列表和指定手性指数范围进行快速大批量生成  
2.输入预设文件名  
  仅在模式1中:输入预设文件名  
  举例: GeS.txt  
  错误程序闪退  
3.输入手性指数n,m  
  仅在模式1中:输入你想要得到的手性指数  
  举例: 0 6 或者 6 0 或者 7 1  
  错误会提示报错  
4.输入高低位编号  
  仅在模式1中:由于在有厚度的原子面中，部分原子可能在管的外层，也可能在管的内层，输入你在预设文件中对应编号就将其设置为外层。  
  举例: 1 或者 2  
  错误会提示报错  
# 关于作者
联系方式: 896180667@qq.com  
有什么不懂可以联系。  
# 效果展示
![image](https://github.com/whilepy/Nanotube-Maker/blob/main/image/1.jpg)  
![image](https://github.com/whilepy/Nanotube-Maker/blob/main/iamge/2.jpg)  
![image](https://github.com/whilepy/Nanotube-Maker/blob/main/iamge/3.jpg)  
![image](https://github.com/whilepy/Nanotube-Maker/blob/main/iamge/4.jpg)  
![image](https://github.com/whilepy/Nanotube-Maker/blob/main/iamge/5.jpg)  
![image](https://github.com/whilepy/Nanotube-Maker/blob/main/iamge/6.jpg)  
![image](https://github.com/whilepy/Nanotube-Maker/blob/main/iamge/7.jpg)  
