#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
Location: C:/Users/29042/PycharmProjects/TextFetcher/main.py
Description: 诗词爬虫程序
Created on 2024-9-12
"""

import bs4
import requests as rq
from colorama import Fore, Style, init
from tqdm import tqdm

init()  # 初始化colorama库
url = r"https://www.gushiwen.cn/"  # 目标服务器地址


def get_response(url: str) -> str:
    """
    发送HTTP请求并返回目标URL的响应内容

    :param url: 目标网页的URL地址
    :return: 网页的HTML内容作为字符串返回
    """
    try:
        resp = rq.get(url)
        resp.raise_for_status()  # 检查请求是否成功
        return resp.text
    except rq.exceptions.RequestException as e:
        print(Fore.RED + f"请求失败: {e}" + Style.RESET_ALL)
        return ""


def convert_data(html: str) -> bs4.BeautifulSoup:
    """
    将 HTML 字符串转换为 BeautifulSoup 对象, 用于解析网页内容

    :param html: 网页的 HTML 内容
    :return: 解析后的 BeautifulSoup 对象
    """
    resp = bs4.BeautifulSoup(html, "html.parser")
    return resp


def write(lst: list):
    with open(".\\poems.txt", "w", encoding="utf-8") as f:
        for poem in lst:
            f.write(poem[0] + "\n")  # 标题
            f.write(poem[1] + "\n")  # 朝代
            # 正文
            text = poem[2].replace("。", "。\n")  # 句号后面添加换行符
            f.write(text + "\n")


def find_poem(resp: bs4.BeautifulSoup):
    """
    查找并打印网页中的诗歌内容

    :param resp: 包含HTML文档的BeautifulSoup对象
    """
    poems = resp.findAll("div", class_="contson")
    with open("./poems.txt", "w", encoding="utf-8") as f:
        for poem in poems:
            f.write(poem.text)


def find_by_author(author: str, number) -> list:
    """
    根据作者爬取诗词

    :param author: 目标作者诗词页面的URL
    :param number: 要爬取的诗词数量
    :return: 包含诗词信息的列表
    """
    pages = 1
    poems = 0
    tq = tqdm(total=number, desc="爬取中, 请不要中断. 当前进度为")
    lst = []
    while poems < number:
        # 这个URL中的page参数就是页数, astr参数就是作者的名字
        url = r"https://www.gushiwen.cn/shiwens/default.aspx?page=" + str(pages) + r"&astr=" + author
        resp = get_response(url);
        resp = convert_data(resp)
        father = resp.find("div", id="leftZhankai")
        sons = father.findAll("div", class_="sons")
        if poems + len(sons) > number:
            sons = sons[:number - poems]
            poems = number
        else:
            poems += len(sons)
        for son in sons:
            div2 = son.find("div", class_="cont")
            title = div2.findAll("p")[0].text.strip()
            time = div2.findAll("p")[-1].text.strip()
            content = div2.find("div", class_="contson").text.strip()
            lst.append((title, time, content))
            tq.update(1)
        pages += 1
    return lst


def find_by_dynasty(dynasty: str, number) -> list:
    """
    根据朝代爬取诗词
    :param dynasty: 目标朝代诗词页面的URL
    :param number: 要爬取的诗词数量
    :return: 包含诗词信息的列表
    """
    pages = 1
    poems = 0
    tq = tqdm(total=number, desc="爬取中, 请不要中断. 当前进度为")
    lst = []
    while poems < number:
        # 这个URL中的page参数就是页数, cstr参数就是朝代
        url = r"https://www.gushiwen.cn/shiwens/default.aspx?page=" + str(pages) + r"&cstr=" + dynasty
        resp = get_response(url);
        resp = convert_data(resp)
        father = resp.find("div", id="leftZhankai")
        sons = father.findAll("div", class_="sons")
        if poems + len(sons) > number:
            sons = sons[:number - poems]
            poems = number
        else:
            poems += len(sons)
        for son in sons:
            div2 = son.find("div", class_="cont")
            title = div2.findAll("p")[0].text.strip()
            time = div2.findAll("p")[-1].text.strip()
            content = div2.find("div", class_="contson").text.strip()
            lst.append((title, time, content))
            tq.update(1)
        pages += 1
    return lst


def find_by_poem_type(poem_type: str, number) -> list:
    """
    根据类型爬取诗词
    :param poem_type: 目标类型诗词页面的URL
    :param number: 要爬取的诗词数量
    :return: 包含诗词信息的列表
    """
    pages = 1
    poems = 0
    tq = tqdm(total=number, desc="爬取中, 请不要中断. 当前进度为")
    lst = []
    special_types = {"楚辞": "chuci", "诗经": "shijing", "乐府": "yuefu"}
    if poem_type in special_types:
        urls = []
        pre_addr = r"https://www.gushiwen.cn"
        url = pre_addr + r"/gushi/" + special_types[poem_type] + r".aspx"
        resp = get_response(url)
        resp = convert_data(resp)
        type_conts = resp.findAll("div", class_="typecont")  # 获取所有的组
        for con in type_conts:
            a_lst = con.findAll("a")
            for a in a_lst:
                addr = a["href"]
                urls.append(f"{pre_addr}{addr}")
        for url in urls:
            resp = get_response(url)
            resp = convert_data(resp)
            yuanwen = resp.find(id="sonsyuanwen")
            title = yuanwen.find("h1").text
            time = yuanwen.find("p", class_="source").text.strip()
            content = yuanwen.find("div", class_="conston").text
            lst.append((title, time, content))

        return lst

    while poems < number:
        # 这个URL中的page参数就是页数, tstr参数就是类型
        url = r"https://www.gushiwen.cn/shiwens/default.aspx?page=" + str(pages) + r"&tstr=" + poem_type
        resp = get_response(url)
        resp = convert_data(resp)
        father = resp.find("div", id="leftZhankai")
        sons = father.findAll("div", class_="sons")
        if poems + len(sons) > number:
            sons = sons[:number - poems]
            poems = number
        else:
            poems += len(sons)
        for son in sons:
            div2 = son.find("div", class_="cont")
            title = div2.findAll("p")[0].text.strip()
            time = div2.findAll("p")[-1].text.strip()
            content = div2.find("div", class_="contson").text.strip()
            lst.append((title, time, content))
            tq.update(1)
        pages += 1
    return lst



if __name__ == "__main__":
    types = input(
        Fore.BLUE + "请输入你想要爬取诗文的功能\n[1] 按照作者爬取\n[2] 按照朝代爬取\n[3] 按照类型爬取\n[4] 按照标题爬取\n? " + Style.RESET_ALL).strip()
    if types == '1':  # 按照作者爬取
        author = input(Fore.GREEN + "请输入诗人的名字: " + Style.RESET_ALL).strip()
        number = int(input(Fore.GREEN + "请输入爬取的古诗数量: " + Style.RESET_ALL))
        lst = find_by_author(author, number)
        write(lst)
    elif types == '2':  # 按照朝代爬取
        dynasty = input(Fore.GREEN + "请输入朝代: " + Style.RESET_ALL).strip()
        number = int(input(Fore.GREEN + "请输入爬取的古诗数量: " + Style.RESET_ALL))
        lst = find_by_dynasty(dynasty, number)
        write(lst)
    elif types == '3':  # 按照类型爬取
        poem_type = input(Fore.GREEN + "请输入诗文类型: " + Style.RESET_ALL).strip()
        number = int(input(Fore.GREEN + "请输入爬取的古诗数量: " + Style.RESET_ALL))
        lst = find_by_poem_type(poem_type, number)
        write(lst)
    elif types == '4':  # 按照标题爬取
        pass
    else:
        print(Fore.RED + "选择的模式无效! " + Style.RESET_ALL)
        exit()
