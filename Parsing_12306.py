# coding:utf-8
import requests
import json
import os
import csv
import codecs
import re
import datetime
from train_graph import data as ped

graph = ped.Graph()

def Parsing_12306(text: str) -> ped.Train:
    d = json.loads(text)['data']['data']
    train = ped.Train(graph)
    for dct in d:
        if dct['arrive_time'] == '----':
            dct['arrive_time'] = dct['start_time']
        if ('station_name' in dct and dct['station_name'] in station_lists):
            rules_list = rules_lists[station_lists.index(dct['station_name'])]
            if (('station_name' in dct) and rules_list[0] == dct['station_name']):
                dct['station_name'] = rules_list[1]
                if (rules_list[2] != '0'):
                    Time = datetime.datetime.strptime(
                        dct['arrive_time'], "%H:%M")
                    dct['arrive_time'] = (
                        Time + datetime.timedelta(minutes=int(rules_list[2]))).strftime("%H:%M")
                if (rules_list[3] != '0'):
                    Time = datetime.datetime.strptime(
                        dct['start_time'], "%H:%M")
                    dct['start_time'] = (
                        Time + datetime.timedelta(minutes=int(rules_list[3]))).strftime("%H:%M")
                print(dct)
        if ('start_station_name' in dct and dct['start_station_name'] in station_lists):
            rules_list = rules_lists[station_lists.index(
                dct['start_station_name'])]
            if (('start_station_name' in dct) and rules_list[0] == dct['start_station_name']):
                dct['start_station_name'] = rules_list[1]
                if (rules_list[2] != '0'):
                    Time = datetime.datetime.strptime(
                        dct['arrive_time'], "%H:%M")
                    dct['arrive_time'] = (
                        Time + datetime.timedelta(minutes=int(rules_list[2]))).strftime("%H:%M")
                if (rules_list[3] != '0'):
                    Time = datetime.datetime.strptime(
                        dct['start_time'], "%H:%M")
                    dct['start_time'] = (
                        Time + datetime.timedelta(minutes=int(rules_list[3]))).strftime("%H:%M")
                print(dct)
        csv_writer.writerow([train_number,dct['station_name'],dct['arrive_time'],dct['start_time']])
        train.addStation(dct['station_name'], dct['arrive_time'],
                         dct['start_time'], business=True)
        if sfz := dct.get('start_station_name'):
            train.sfz = sfz
        if zdz := dct.get('end_station_name'):
            train.zdz = zdz
    return train


def get_search():
    url = ("https://search.12306.cn/search/v1/train/search?callback=jQuery&keyword={train}&date={date}").format(
        train=train_number, date=date)
    r = requests.get(url, headers=headers)
    with open("search.json", "wb") as code:
        code.write(r.content)
    with open('search.json', encoding='utf-8', errors='ignore') as fp:
        return(fp.read())


print("多规则版，规则文件在“rules.txt”，格式为“原站名 新站名 修改到达分钟 修改出发分钟”，可以用换行来增加规则。本项目使用并遵循GPLv3协议。程序作者：CDK6182CHR、denglihong2007。制作日期：2022.03.11。")
date = str(input("您想爬取的日期是？（一次爬取仅可输入一次，如20220127）"))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edge/97.0.1072.69'}
chinese = "[A-Za-z0-9\!\%\[\]\,\。\"\:\_]"
csv_file = codecs.open('train_number.csv','w',encoding='utf-8-sig')
csv_writer = csv.writer(csv_file)
file = open('rules.txt', encoding='utf-8-sig', errors='ignore')
station_lists = []
rules_lists = []
rule = "0"
while (rule != list([])):
    rule = file.readline().split()
    rules_lists.append(rule)
    if (rule != list([])):
        station_lists.append(rule[0])

with open("libs\\station_name.js", encoding='utf-8', errors='ignore') as fp:
    telecode_list = fp.read()

while True:
    train_number = input("您想爬取的车次是？（输入exit退出）")

    if train_number == "exit":
        graph.save('query_parse.pyetdb')
        csv_file.close()
        os.remove("queryByTrainNo.json")
        os.remove("search.json")
        os._exit(0)

    search = get_search()
    if search == '/**/jQuery({"data":[],"status":true,"errorMsg":""});':
        search = "error"
    if search == '/**/jQuery({"data":null,"status":true,"errorMsg":""});':
        search = "error"

    while search == "error":
        train_number = input("当日未查询到此车次，请重新输入。")
        search = get_search()
        if search == '/**/jQuery({"data":[],"status":true,"errorMsg":""});':
            search = "error"
        if search == '/**/jQuery({"data":null,"status":true,"errorMsg":""});':
            search = "error"
        if train_number == "exit":
            graph.save('query_parse.pyetdb')
            csv_file.close()
            os.remove("queryByTrainNo.json")
            os.remove("search.json")
            os._exit(0)

    train_no = search[33:45]
    search_train = search[38:43].lstrip("0")
    start_station = re.sub(chinese, "", search[105:117])
    to_station = re.sub(chinese, "", search[124:136])
    start_station_code = telecode_list[telecode_list.find(start_station + "|") + len(
        start_station) + 1:telecode_list.find(start_station + "|") + len(start_station) + 4]
    to_station_code = telecode_list[telecode_list.find(to_station + "|") + len(
        to_station) + 1:telecode_list.find(to_station + "|") + len(to_station) + 4]

    year = date[0:4]
    month = date[4:6]
    day = date[6:]

    url = ("https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no={train_no}&from_station_telecode={start_station_code}&to_station_telecode={to_station_code}&depart_date={year}-{month}-{day}").format(
        train_no=train_no, start_station_code=start_station_code, to_station_code=to_station_code, year=year, month=month, day=day)

    print("查询到" + search_train + "的代码为" + train_no + "，起点站为" + start_station + "，终点站为" +
          to_station + "，起点电报码为" + start_station_code + "，终点电报码为" + to_station_code + "。")

    r = requests.get(url)
    with open("queryByTrainNo.json", "wb") as code:
        code.write(r.content)
    if __name__ == '__main__':
        with open('queryByTrainNo.json', encoding='utf-8', errors='ignore') as fp:
            text = fp.read()
        train = Parsing_12306(text)
        train.setFullCheci(search_train)
        graph.addTrain(train)
