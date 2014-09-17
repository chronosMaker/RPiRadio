#!/usr/bin/env python
# coding=utf-8
import pylirc


class Buttons:

    # 初始化，这里的app需要和调用它的文件名称一致，conf需要和之前实验中irexec地址一致，"/etc/lirc/irexec.conf"
    def __init__(self, app, conf):
        if not pylirc.init(app, conf, 1):
            raise Exception("Unable to init pylirc")
        # 阻塞模式关闭
        pylirc.blocking(0)

    def readbutton(self):
        # 按下按键传递对应的config值，如果没有匹配的key则为None
        btn = pylirc.nextcode()
        if btn:
            return btn[0]
        else:
            return None
