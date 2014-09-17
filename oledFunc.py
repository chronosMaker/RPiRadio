# coding=utf-8
__author__ = 'chronos'
#!/usr/bin/python

import smbus

# open /dev/i2c-1
bus = smbus.SMBus(1)

# OLED FUNC CMD
WRITE_OCMD = 0x01
WRITE_ODAT = 0x02
OLED_RESET = 0x03

DISP_8X16STR = 0x10
DISP_AREA = 0x11
FILL_AREA = 0x12
SET_SCROHOR = 0x13
SET_SCROVER = 0x14
SET_SCROVERHOR = 0x15

SET_ADDRESS = 0x21

PAGE0 = 0x00
PAGE1 = 0x01
PAGE2 = 0x02
PAGE3 = 0x03
PAGE4 = 0x04
PAGE5 = 0x05
PAGE6 = 0x06
PAGE7 = 0x07

SCROLL_UP = 0x01
SCROLL_DOWN = 0x00
SCROLL_RIGHT = 0x26
SCROLL_LEFT = 0x27
SCROLL_VR = 0x29
SCROLL_VL = 0x2A

FRAMS_2 = 0x07
FRAMS_3 = 0x04
FRAMS_4 = 0x05
FRAMS_5 = 0x00
FRAMS_25 = 0x06
FRAMS_64 = 0x01
FRAMS_128 = 0x02
FRAMS_256 = 0x03


# OLED RESET
# 函数功能 ：模块复位
# 第1个参数：为模块的地址
def oledreset(addr):
    bus.write_byte(addr, OLED_RESET)


# OLED FILLAREA
# 函数功能 ：在指定的范围填充指定的数据
# 第1个参数：为模块的地址
# 第2个参数：所要填充数据的起始页
# 第3个参数：所要填充数据的结束页
# 第4个参数：所要填充数据的起始列
# 第5个参数：所要填充数据的结束列
# 第6个参数：所要填充的数据
def oledfillarea(addr, spage, epage, scolumn, ecolumn, filldata):
    buff = [spage, epage, scolumn, ecolumn, filldata]
    bus.write_i2c_block_data(addr, FILL_AREA, buff)


# OLED DISPLAY STRING
# 函数功能 ：在指定的地方开始显示指定点阵数据图英文字符串
# 第1个参数：为模块的地址
# 第2个参数：所要显示英文字符串的起始页
# 第3个参数：所要显示英文字符串的起始列
# 第4个参数：所要显示的英文字符串
def oledstr(addr, page, column, strs):
    buff = [page, column]
    lstr = map(ord, strs)
    buff.extend(lstr)
    bus.write_i2c_block_data(addr, DISP_8X16STR, buff)


# OLED Scroll Horizontal
# 函数功能 ：指定区域显示的内容向左还是向右翻滚
# 第1个参数：为模块的地址
# 第2个参数：指定向左还是向右翻滚 SCROLL_LEFT SCROLL_RIGHT
# 第3个参数：要翻滚的起始页
# 第4个参数：要翻滚的结束页
# 第3个参数：翻滚帧
def oledscrollhorizontal(addr, lr, spage, epage, frames):
    buff = [lr, spage, epage, frames]
    bus.write_i2c_block_data(addr, SET_SCROHOR, buff)


# OLED Scroll Vertical
# 函数功能 ：指定区域显示的内容向上翻或向下翻
# 第1个参数：为模块的地址
# 第2个参数：指定向上或者向下翻滚 SCROLL_UP SCROLL_DOWN
# 第3个参数：最上方翻滚起始行
# 第4个参数：最下方翻滚结束行
# 第3个参数：翻滚步数大小
# 第4个参数：翻滚快慢延时
def oledscrollvertical(addr, scrollupdown, rowsfixed, rowsscroll, scrollstep, stepdelay):
    buff = [scrollupdown, rowsfixed, rowsscroll, scrollstep, stepdelay]
    bus.write_i2c_block_data(addr, SET_SCROVER, buff)


# OLED Scroll Mixed
def oledscrollmixed(addr, fixedarea, scrollarea, vlr, spage, epage, frames, offset):
    buff = [fixedarea, scrollarea, vlr, spage, epage, frames, offset]
    bus.write_i2c_block_data(addr, SET_SCROVERHOR, buff)


# OLED Deactivate Scroll
# 函数功能 ：显示的内容停止翻滚
# 第1个参数：为模块的地址
def oleddeactivatescroll(addr):
    bus.write_byte_data(addr, WRITE_OCMD, 0x2E)


# OLED Set Location
def oledsetlocation(addr, page, column):
    buff = [0xB0 | page, column % 16, column/16+0x10]
    bus.write_i2c_block_data(addr, WRITE_OCMD, buff)
