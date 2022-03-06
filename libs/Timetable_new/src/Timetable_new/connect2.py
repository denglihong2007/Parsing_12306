"""
时刻表连接程序第二代，仅包括链接函数
接受两个列车对象，按上下行进行连接
暂不考虑始发终到问题
要求train1为上行端的，train2为下行端的。如两车次行别不同，打印警告信息，并以车次1的行别为准。
method参数表示连接方式，默认为0，行别不变。
1：down-up型，所有下行在前。
2：up-down型，所有上行在前。
"""
from .direction import judge_order_by_direction,judge_order_by_station
from datetime import datetime
from .utility import stationEqual

def connect(trainraw1,trainraw2,method=-1):
    if trainraw1.down != trainraw2.down and method == 0:
        print("车次两段行别不同！请检查。",trainraw1.checi.full)
    if method >= 0:
        change = judge_order_by_direction(trainraw1,trainraw2,method)
    else:
        change = judge_order_by_station(trainraw1,trainraw2)

    if change:
        train1 = trainraw2
        train2 = trainraw1
    else:
        train1 = trainraw1
        train2 = trainraw2

    #train1 总是靠前的那个
    if not train1.sfz and train2.sfz:
        train1.sfz=train2.sfz
    if not train1.zdz and train2.zdz:
        train1.zdz=train2.zdz
    for i,s in train2.timetable.items():
        if i not in list(train1.timetable.keys()):
            train1.timetable[i] = s
    return train1


#表征连接状态的常量
ASC_ACCEPT = 0
DSC_ACCEPT = 1
REJECT = -1

def connect_db(rawtrains:list):
    """
    只依赖时刻表的重复特性进行拼接，不考虑上下行问题，不转置车次时刻表。
    rawtrains是非空的。它的首个元素将作为返回的信息。
    """
    if(len(rawtrains)==1):
        return rawtrains[0]

    train = rawtrains.pop(0)  # 这个将作为要连接的起始车次
    unmerged = rawtrains.copy()
    toDel_index = []
    flag = True #标志一次循环中完成了判断

    while flag:
        flag=False
        for index,anTrain in enumerate(unmerged):
            judge = judge_connect(train,anTrain)
            if judge == REJECT:
                continue
            elif judge==ASC_ACCEPT:
                flag=True
                train = joint_simply(train,anTrain)
                toDel_index.append(index)
            else:  #DSC_ACCEPT
                flag=True
                train = joint_simply(anTrain,train)
                toDel_index.append(index)
        for i in reversed(toDel_index):
            del unmerged[i]
        toDel_index = []
        if not unmerged:
            break

    # 如果还有没排好的，递归，得到另一连接出来的车次。此操作类似图的连通分支，最后把两个合并起来即可。
    if unmerged:
        anotherTrain = connect_db(unmerged)
        # print(train,anotherTrain)
        judge=judge_connect(train,anotherTrain,enforce=True)
        if judge==ASC_ACCEPT:
            train = joint_simply(train,anotherTrain)
        else:
            train = joint_simply(anotherTrain,train)
    return train

def judge_connect(train1,train2,enforce=False):
    """
    enforce: 强制返回结果。给可能性最大的判断。
    判断两车次是否能连接起来，及连接方向。返回符号常量
    ASC表示train1在前，DSC表示train2在前，REJECT表示这两个对象不能连接
    """
    common = set(train1.timetable.keys()) & set(train2.timetable.keys())
    if common:
        # 两车次经停站有交集，进行重复车站匹配。
        # train1中第一个与train2交叉的站出现的位置，如果在它的开头则判定train2
        lst1 = list(train1.timetable.keys())
        lst2 = list(train2.timetable.keys())
        common_index_1 = list(map(lambda x:lst1.index(x)+1,common))  # 重复站出现的序号
        common_index_2 = list(map(lambda x:lst2.index(x)+1,common))
        if max(common_index_1)/len(lst1) < 0.2 or max(common_index_1) <=2:
            if min(common_index_2)/len(lst2) > 0.8 or min(common_index_2) >= len(common_index_2)-1:
                # 重复站全部分布在1的前部和2的后部
                return DSC_ACCEPT

        if max(common_index_2)/len(lst1) < 0.2 or max(common_index_2) <=2:
            if min(common_index_1)/len(lst2) > 0.8 or min(common_index_1) >= len(common_index_1)-1:
                return ASC_ACCEPT

    # 出入时刻判定，容差是30分钟。
    allow = 30*60
    startEnd1 = tuple(map(lambda x:datetime.strptime(x,'%H:%M:%S'),
                          (list(train1.timetable.values())[0][0], list(train1.timetable.values())[-1][1])))
    startEnd2 = tuple(map(lambda x:datetime.strptime(x,'%H:%M:%S'),
                          (list(train2.timetable.values())[0][0], list(train2.timetable.values())[-1][1])))

    dt12 = startEnd2[0]-startEnd1[1]  #若1放在前面
    dt21 = startEnd1[0]-startEnd2[1]

    dt12_int = abs(min(dt12.seconds,3600*24-dt12.seconds))
    dt21_int = abs(min(dt21.seconds,3600*24-dt21.seconds))
    if  dt12_int < dt21_int and dt12_int<= allow:
        return ASC_ACCEPT
    elif  dt21_int<= allow:
        return DSC_ACCEPT

    if not enforce:
        return REJECT

    if dt12_int < dt21_int:
        return ASC_ACCEPT
    else:
        return DSC_ACCEPT

def joint_simply(train1,train2):
    """
    不加任何判断地将2连在1的后面。原位操作。
    """
    # 如果有包含关系，直接扔掉
    st1 = set(train1.timetable.keys())
    st2 = set(train2.timetable.keys())
    if st1.issubset(st2): # st1 belongs to st2
        return train2
    elif st2.issubset(st1):
        return train1

    for station,time in train2.timetable.items():
        if station not in train1.timetable.keys():
            train1.timetable[station] = time
    if not train1.sfz:
        train1.sfz=train2.sfz
    if not train1.zdz:
        train1.zdz=train2.zdz
    return train1