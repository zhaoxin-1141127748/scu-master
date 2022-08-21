# -*- coding: utf8 -*-
"""
author: Les1ie, HyperMn, syaoranwe
mail: me@les1ie.com
license: CC BY-NC-SA 3.0
"""

import pytz
import requests
from datetime import datetime


s = requests.Session()

user = "USERNAME"    # 账号
passwd = "PASSWORD"   # 密码
api_key = ""  # server酱的api，填了可以微信通知打卡结果，不填没影响


def login(s: requests.Session, username, password):
    # r = s.get(
    #     "https://app.ucas.ac.cn/uc/wap/login?redirect=https%3A%2F%2Fapp.ucas.ac.cn%2Fsite%2FapplicationSquare%2Findex%3Fsid%3D2")
    # print(r.text)
    payload = {
        "username": username,
        "password": password
    }
    r = s.post("https://wfw.scu.edu.cn/a_scu/api/sso/check", data=payload)

    # print(r.text)
    if r.json().get('m') != "操作成功":
        print(r.text)
        print("登录失败")
        exit(1)
    else:
        print("登录成功")


def get_daily(s: requests.Session):
    daily = s.get("https://wfw.scu.edu.cn/ncov/api/default/daily?xgh=0&app_id=scu")
    # info = s.get("https://app.ucas.ac.cn/ncov/api/default/index?xgh=0&app_id=ucas")
    j = daily.json()
    d = j.get('d', None)
    if d:
        return daily.json()['d']
    else:
        print("获取昨日信息失败")
        exit(1)


def submit(s: requests.Session, old: dict):
    new_daily = {
        'realname': old['realname'],    #姓名
        'number': old['number'],        #学工号
        'sfzx': old['sfzx'],            #是否在校
        # 'ismoved': old['ismoved'],      #是否和前一天同城
        'ismoved': 0,  # 如果前一天位置变化这个值会为1，第二天仍然获取到昨天的1，而事实上位置是没变化的，所以置0
        'tw': old['tw'],                #体温
        'sfcxtz': old['sfcxtz'],        #是否出现体征？
        'sfyyjc':old['sfyyjc'],        #是否到医院检查
        'jcjgqr':old['jcjgqr'],        #检查结果属于以下哪种情况
        'jcjg':old['jcjg'],        #观察或诊疗情况&检查结果
        'sfcyglq':old['sfcyglq'],        #是否处于观察期
        'gllx':old['gllx'],        #观察场所 即隔离类型
        'glksrq':old['glksrq'],        #观察（隔离）开始时间
        'jcbhlx':old['jcbhlx'],        #接触（病患）人群类型
        'jcbhrq':old['jcbhrq'],        #接触（病患）日期
        'fxyy':old['fxyy'],        #返校原因
        # 'bztcyy':old['bztcyy'],        #不和前一天同城原因，由于脚本沿用旧数据，并不会造成位置变化，所以不提交此字段
        'szgj':old['szgj'],        #所在国家
        'szcs':old['szcs'],        #所在城市
        'sfjcbh': old['sfjcbh'],        #是否接触无症状感染/疑似/确诊人群（病患）
        'sfcyglq': old['sfcyglq'],      #是否处于隔离/观察期？
        'sfjxhsjc': old['sfjxhsjc'],    #4月8号以后是否进行核酸检测
        'hsjcrq':old['hsjcrq'],        #核酸检测日期
        'hsjcdd':old['hsjcdd'],        #核酸检测地点
        'hsjcjg':old['hsjcjg'],        #核酸检测结果
        'zgfxdq':old['zgfxdq'],        #今日是否在中高风险地区
        'mjry':old['mjry'],        #今日是否接触密接人员
        'csmjry':old['csmjry'],        #近14日内本人/共同居住者是否去过疫情发生场所（市场、单位、小区等）或与场所人员有过密切接触
        'sfcxzysx': old['sfcxzysx'],    #是否出现值得注意的情况？
        'qksm':old['qksm'],        #情况说明（值得注意的情况）
        'remark':old['remark'],        #其他信息（最底端文字）
        'old_szdd': old['old_szdd'],        #昨天所在地点
        'geo_api_info': old['old_city'],    #行政区域api结果,采用昨天的数据中的“历史所在城市”
        'old_city': old['old_city'],        #历史所在城市，沿用
        'old_sfzx':old['old_sfzx'],        #昨天是否在校，沿用
        'old_szgj':old['old_szgj'],        #昨天所在国家，沿用
        'jcjgt':old['jcjgt'],        #昨天的观察或诊疗情况&检查结果
        'geo_api_infot': old['geo_api_infot'],     #历史行政区域api结果，沿用
        'date': datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d"),    #打卡日期
        'app_id': 'scu'}

    r = s.post("https://wfw.scu.edu.cn/ncov/api/default/save", data=new_daily)
    print("提交信息:", new_daily)
    # print(r.text)
    result = r.json()
    if result.get('m') == "操作成功":
        print("打卡成功")
        if api_key:
            message(api_key, result.get('m'), new_daily)
    else:
        print("打卡失败，错误信息: ", r.json().get("m"))
        if api_key:
            message(api_key, result.get('m'), new_daily)


def message(key, title, body):
    """
    微信通知打卡结果
    """
    msg_url = "https://sc.ftqq.com/{}.send?text={}&desp={}".format(key, title, body)
    requests.get(msg_url)

def main_handler(event, context):
    """
    腾讯云云函数入口
    """
    print(datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S %Z"))
    login(s, user, passwd)
    yesterday = get_daily(s)
    submit(s, yesterday)

