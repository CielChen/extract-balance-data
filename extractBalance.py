#################################################  
# Author : CIEL 
# Date   : 2017-09-25
# Function : 提取train.csv中的数据，获得平衡数据集   
#################################################  

#载入需要的库
import numpy as np  #科学计算库
import pandas as pd  #数据分析
import os
from time import time  
import matplotlib.pylab as plt
from pandas import DataFrame
import random
import codecs

# 读取原始数据的csv文件，删除多余的label=0的行，生成平衡数据集
def extract_balance_data(originDataFile, balanceDataFile):
    if os.path.exists(originDataFile):
        # 生成title
        listTitle = []
        #listTitle.append('ID')
        listTitle.append('class')
        for i in range(1, 343):
            listTitle.append('feature' + str(i))
            
        # read the csv file
        # pd.read_csv: 封装在DataFrame数据结构中
        dataMatrix = np.array(pd.read_csv(originDataFile, header=None, skiprows=1, names=listTitle))
        #print(dataMatrix)
        
        # 获取样本总数（rowNum）和每个样本的维度（colNum: 类别+特征，共343维）
        rowNum, colNum = dataMatrix.shape[0], dataMatrix.shape[1]
        print('rowNum:')
        print(rowNum)
        #print(colNum)
        
        print ('统计 label=1 和 label=0 的行数：')
        labelOne = 0   #统计label=1的样本数
        for i in range(0, rowNum):
            if(dataMatrix[i][0] == 1):
                labelOne += 1
        labelZero = rowNum - labelOne
        print('labelOne:')
        print(labelOne)
        print ('labelZero:')
        print(labelZero)
        deleteNum = labelZero - labelOne  #要删除的行数
        
        print ('创建平衡数据集...')
        newDataMatrix = []
        alreadyWrite = 0
        # 写入class=1的行
        for i in range(0, rowNum):
            if(dataMatrix[i][0] == 1):
                newDataMatrix.append(dataMatrix[i, :].tolist())
        # 写入class=0的行
        while(alreadyWrite < labelOne):
            randRow = random.randint(0, rowNum-1)
            if(dataMatrix[randRow][0] == 0):
                for j in range(1, 343):
                    if(dataMatrix[randRow][j] == 0):
                        continue
                newDataMatrix.append(dataMatrix[randRow, :].tolist())
                alreadyWrite += 1
                #print(newDataMatrix)
        
        np.savetxt(balanceDataFile, newDataMatrix, delimiter= ',', newline='\n')

def main():

    # --------------------- step1. 生成训练集的csv文件(train.csv)和验证集的csv文件(validation.csv) ---------------------
    # 原始数据的csv文件
    #originDataFile = 'jupyter-train.csv'  #注意：该csv文件没有'ID'列
    #balanceDataFile = 'balanceTrain.csv'
    originDataFile = '20171114-rawtrain-withoutID.csv'  #注意：该csv文件没有'ID'列
    balanceDataFile = '20171114BalanceTrain.csv'
    extract_balance_data(originDataFile, balanceDataFile)
    
# 在python编译器读取源文件的时候会执行它找到的所有代码，
# 而在执行之前会根据当前运行的模块是否为主程序而定义变量__name__的值为__main__还是模块名。
# 因此，该判断语句为真的时候，说明当前运行的脚本为主程序，而非主程序所引用的一个模块。
# 这在当你想要运行一些只有在将模块当做程序运行时而非当做模块引用时才执行的命令，只要将它们放到if __name__ == "__main__:"判断语句之后就可以了。
if __name__ == '__main__':  
    start = time()
    print('开始修改数据集\n')
    
    main()
    
    print('\n')
    print('修改完毕结束')
    end = time()
    print('用时 %.5f seconds.' % (end-start))




