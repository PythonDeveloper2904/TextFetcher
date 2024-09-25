#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import webbrowser


def search_manga(keyword):
    # Open the browser with the specified search URL
    webbrowser.open(r"https://manga.bilibili.com/search?from=manga_homepage&keyword="+keyword)


def open_manga():
    webbrowser.open(  # 打开特定的漫画


def main():
    keyword = input("请输入关键词: ")
    if keyword == "":
        print("关键词不能为空!")
    search_manga(keyword)
    print  # 输出前10个漫画的信息以及链接
    comic = int(input  # 询问用户要打开第几个漫画
    open_manga(comic)


if __name__ == "__main__":
    main()
