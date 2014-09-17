# coding=utf-8
__author__ = 'chronos'
#!/usr/bin/python

import os
import time
import smbus
import socket
import fcntl
import struct
import oledFunc
import commands
from Buttons import Buttons

# open /dev/i2c-1  
bus = smbus.SMBus(1)

# 导入按键设置
btn = Buttons("radio", "/etc/lirc/irexec.conf")

# RDA REGISTER
RDA_reg_02H = 0xd0
RDA_reg_data = [0x00, 0x00, 0x00, 0x00, 0x40, 0x90, 0x88]
# 定时关机时间及标志位
flag_timing = 10
flag_shutdown = 0
radio_timing = 0
# SET I2C ADDRESS
oledaddress = 0x51
radioaddress = 0x10


# 频道名称汉字
class ChannelWord:
    he = [0x10, 0x60, 0x02, 0x8C, 0x00, 0x04, 0xE4, 0x24, 0x24, 0xE4, 0x04, 0x04, 0xFC, 0x04, 0x04, 0x00,
          0x04, 0x04, 0x7E, 0x01, 0x00, 0x00, 0x0F, 0x04, 0x04, 0x0F, 0x40, 0x80, 0x7F, 0x00, 0x00, 0x00]       # "河"

    bei = [0x00, 0x20, 0x20, 0x20, 0x20, 0xFF, 0x00, 0x00, 0x00, 0xFF, 0x40, 0x20, 0x10, 0x08, 0x00, 0x00,
           0x20, 0x60, 0x20, 0x10, 0x10, 0xFF, 0x00, 0x00, 0x00, 0x3F, 0x40, 0x40, 0x40, 0x40, 0x78, 0x00]      # "北"

    yin = [0x40, 0x40, 0x44, 0x44, 0x54, 0x64, 0x45, 0x46, 0x44, 0x64, 0x54, 0x44, 0x44, 0x40, 0x40, 0x00,
           0x00, 0x00, 0x00, 0xFF, 0x49, 0x49, 0x49, 0x49, 0x49, 0x49, 0x49, 0xFF, 0x00, 0x00, 0x00, 0x00]      # "音"

    yue = [0x00, 0x00, 0xE0, 0x9C, 0x84, 0x84, 0x84, 0xF4, 0x82, 0x82, 0x83, 0x82, 0x80, 0x80, 0x00, 0x00,
           0x00, 0x20, 0x10, 0x08, 0x06, 0x40, 0x80, 0x7F, 0x00, 0x00, 0x02, 0x04, 0x08, 0x30, 0x00, 0x00]      # "乐"

    guang = [0x00, 0x00, 0xF8, 0x08, 0x08, 0x08, 0x08, 0x09, 0x0E, 0x08, 0x08, 0x08, 0x08, 0x08, 0x00, 0x00,
             0x80, 0x60, 0x1F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]    # "广"

    bo = [0x10, 0x10, 0xFF, 0x10, 0x90, 0x82, 0x56, 0x3A, 0x12, 0x7F, 0x11, 0x39, 0x55, 0x90, 0x80, 0x00,
          0x42, 0x82, 0x7F, 0x01, 0x00, 0x00, 0xFF, 0x49, 0x49, 0x7F, 0x49, 0x49, 0xFF, 0x00, 0x00, 0x00]       # "播"

    sheng = [0x80, 0x40, 0x30, 0x1E, 0x10, 0x10, 0x10, 0xFF, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x00, 0x00,
             0x40, 0x40, 0x42, 0x42, 0x42, 0x42, 0x42, 0x7F, 0x42, 0x42, 0x42, 0x42, 0x42, 0x40, 0x40, 0x00]    # "生"

    huo = [0x10, 0x60, 0x02, 0x8C, 0x00, 0x20, 0x24, 0x24, 0x24, 0xFE, 0x22, 0x23, 0x22, 0x20, 0x20, 0x00,
           0x04, 0x04, 0x7E, 0x01, 0x00, 0x00, 0xFE, 0x42, 0x42, 0x43, 0x42, 0x42, 0xFE, 0x00, 0x00, 0x00]      # "活"

    shou = [0x04, 0x04, 0xE4, 0x25, 0x26, 0x34, 0x2C, 0x24, 0x24, 0x24, 0x26, 0x25, 0xE4, 0x04, 0x04, 0x00,
            0x00, 0x00, 0xFF, 0x49, 0x49, 0x49, 0x49, 0x49, 0x49, 0x49, 0x49, 0x49, 0xFF, 0x00, 0x00, 0x00]     # "首"

    du = [0x20, 0x24, 0x24, 0xA4, 0x7F, 0x24, 0x34, 0x28, 0x26, 0x20, 0xFE, 0x02, 0x22, 0xDA, 0x06, 0x00,
          0x04, 0x02, 0xFF, 0x49, 0x49, 0x49, 0x49, 0xFF, 0x00, 0x00, 0xFF, 0x08, 0x10, 0x08, 0x07, 0x00]       # "都"

    tian = [0x40, 0x40, 0x42, 0x42, 0x42, 0x42, 0x42, 0xFE, 0x42, 0x42, 0x42, 0x42, 0x42, 0x40, 0x40, 0x00,
            0x80, 0x80, 0x40, 0x20, 0x10, 0x0C, 0x03, 0x00, 0x03, 0x0C, 0x10, 0x20, 0x40, 0x80, 0x80, 0x00]     # "天"

    jin = [0x10, 0x60, 0x02, 0x0C, 0xC0, 0x10, 0x54, 0x54, 0x54, 0xFF, 0x54, 0x54, 0x7C, 0x10, 0x10, 0x00,
           0x04, 0x04, 0x7C, 0x03, 0x00, 0x10, 0x12, 0x12, 0x12, 0xFF, 0x12, 0x12, 0x12, 0x10, 0x00, 0x00]      # "津"

    tang = [0x00, 0x00, 0xFC, 0x44, 0x54, 0x54, 0x54, 0x55, 0xFE, 0x54, 0x54, 0x54, 0xF4, 0x44, 0x44, 0x00,
            0x40, 0x30, 0x0F, 0x00, 0xFD, 0x45, 0x45, 0x45, 0x47, 0x45, 0x45, 0x45, 0xFD, 0x00, 0x00, 0x00]     # "唐"

    shan = [0x00, 0x00, 0xF0, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0x00, 0xF0, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x3F, 0x20, 0x20, 0x20, 0x20, 0x3F, 0x20, 0x20, 0x20, 0x20, 0x7F, 0x00, 0x00, 0x00]     # "山"

    xin = [0x40, 0x44, 0x54, 0x65, 0xC6, 0x64, 0x54, 0x44, 0x00, 0xFC, 0x44, 0x44, 0xC4, 0x42, 0x40, 0x00,
           0x20, 0x12, 0x4A, 0x82, 0x7F, 0x02, 0x0A, 0x92, 0x60, 0x1F, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00]      # "新"

    wen = [0x00, 0xF8, 0x01, 0x12, 0x10, 0xF2, 0x52, 0x52, 0x52, 0xF2, 0x12, 0x12, 0x02, 0xFE, 0x00, 0x00,
           0x00, 0xFF, 0x00, 0x08, 0x08, 0x0F, 0x09, 0x09, 0x09, 0x7F, 0x04, 0x44, 0x80, 0x7F, 0x00, 0x00]      # "闻"

    zong = [0x20, 0x30, 0xAC, 0x63, 0x30, 0x00, 0x0C, 0x24, 0x24, 0x25, 0x26, 0x24, 0x24, 0x24, 0x0C, 0x00,
            0x22, 0x67, 0x22, 0x12, 0x12, 0x20, 0x11, 0x0D, 0x41, 0x81, 0x7F, 0x01, 0x05, 0x09, 0x31, 0x00]     # "综"

    he2 = [0x40, 0x40, 0x20, 0x20, 0x50, 0x48, 0x44, 0x43, 0x44, 0x48, 0x50, 0x20, 0x20, 0x40, 0x40, 0x00,
           0x00, 0x00, 0x00, 0xFE, 0x42, 0x42, 0x42, 0x42, 0x42, 0x42, 0x42, 0xFE, 0x00, 0x00, 0x00, 0x00]      # "合"

    jiao = [0x08, 0x08, 0x88, 0x68, 0x08, 0x08, 0x09, 0x0E, 0x08, 0x08, 0x88, 0x28, 0x48, 0x88, 0x08, 0x00,
            0x80, 0x81, 0x40, 0x40, 0x21, 0x22, 0x14, 0x08, 0x14, 0x22, 0x41, 0x40, 0x80, 0x81, 0x80, 0x00]     # "交"

    tong = [0x40, 0x42, 0xCC, 0x00, 0x00, 0xE2, 0x22, 0x2A, 0x2A, 0xF2, 0x2A, 0x26, 0x22, 0xE0, 0x00, 0x00,
            0x80, 0x40, 0x3F, 0x40, 0x80, 0xFF, 0x89, 0x89, 0x89, 0xBF, 0x89, 0xA9, 0xC9, 0xBF, 0x80, 0x00]     # "通"

    xiang = [0x10, 0x10, 0x10, 0xD0, 0xFF, 0x90, 0x10, 0x00, 0xFE, 0x22, 0x22, 0x22, 0x22, 0xFE, 0x00, 0x00,
             0x08, 0x04, 0x03, 0x00, 0xFF, 0x00, 0x03, 0x00, 0xFF, 0x42, 0x42, 0x42, 0x42, 0xFF, 0x00, 0x00]    # "相"

    sheng2 = [0x04, 0x14, 0xD4, 0x54, 0x54, 0x54, 0x54, 0xDF, 0x54, 0x54, 0x54, 0x54, 0xD4, 0x14, 0x04, 0x00,
             0x80, 0x60, 0x1F, 0x02, 0x02, 0x02, 0x02, 0x03, 0x02, 0x02, 0x02, 0x02, 0x03, 0x00, 0x00, 0x00]    # "声"

    jing = [0x04, 0x04, 0x04, 0xE4, 0x24, 0x24, 0x25, 0x26, 0x24, 0x24, 0x24, 0xE4, 0x04, 0x04, 0x04, 0x00,
            0x00, 0x40, 0x20, 0x1B, 0x02, 0x42, 0x82, 0x7E, 0x02, 0x02, 0x02, 0x0B, 0x10, 0x60, 0x00, 0x00]     # "京"

    null = [0x00]*32


# commands
# 退出RADIO程序
def doquit():
    # 手动清屏
    oledFunc.oledreset(oledaddress)
    time.sleep(0.1)
    # 确认退出信息
    oledFunc.oledstr(oledaddress, 0, 0, ' QUIT RPi RADIO ')
    oledFunc.oledstr(oledaddress, 3, 0, ' Are you sure ? ')
    oledFunc.oledstr(oledaddress, 6, 0, 'Press PLAY for Y')
    while True:
        irbutton = btn.readbutton()     # 接收按键
        # 向前按钮返回
        if irbutton == 'PREVIOUS':
            # 手动清屏
            oledFunc.oledreset(oledaddress)
            time.sleep(0.1)
            display()   # 显示主屏信息
            break       # 跳出返回主屏
        # 确认按钮退出
        if irbutton == 'PLAY':
            # 手动清屏
            oledFunc.oledreset(oledaddress)
            time.sleep(0.1)
            radioshutdown()     # 关闭RADIO
            quit()              # 退出程序
        time.sleep(0.2)


# RADIO RESET
def radioreset():
    # 发送软件复位指令
    RDA_reg_02H = 0x00
    RDA_reg_data[0] = 0x02
    bus.write_i2c_block_data(radioaddress, RDA_reg_02H, RDA_reg_data)
    time.sleep(0.01)
    # 收音模块默认参数
    RDA_reg_02H = 0xd0
    RDA_reg_data[0] = 0x01
    bus.write_i2c_block_data(radioaddress, RDA_reg_02H, RDA_reg_data)


# Radio Shutdown
def radioshutdown():
    RDA_reg_data[0] = 0x00      # 关闭RADIO
    bus.write_i2c_block_data(radioaddress, RDA_reg_02H, RDA_reg_data)


# FM自动搜台，参数“reg_02h”为搜台方向
def fmseek(reg_02h):
    reg_data = [0x00, 0x00, 0x00, 0x00]     # 存储channel信息
    reg_02h |= (1 << 0)     # 内部自动寻台使能，SEEK位置1
    RDA_reg_data[2] &= ~(1 << 4)    # 调谐禁用
    bus.write_i2c_block_data(radioaddress, reg_02h, RDA_reg_data)

    while 0 == (reg_data[0] & 0x40):        # 等待STC标志置位
        reg_data = bus.read_i2c_block_data(0x10, 0x0a, 4)   # 读取内部状态
        time.sleep(0.02)

    # 获取当前工作频点
    chan = reg_data[0] & 0x03
    chan = reg_data[1] | (chan << 8)
    chan <<= 6
    # 保存当前工作频点
    RDA_reg_data[1] = (chan >> 8) & 0xff
    RDA_reg_data[2] = (chan & 0xff)


# 音量调大
def vol_up():
    if RDA_reg_data[6] & 0x0f < 0x0f:       # 取音量值
        RDA_reg_02H = 0xd0
        RDA_reg_data[0] = 0x01
        RDA_reg_data[2] &= ~(1 << 4)
        RDA_reg_data[6] += 1
        bus.write_i2c_block_data(radioaddress, RDA_reg_02H, RDA_reg_data)


# 音量调小
def vol_down():
    if RDA_reg_data[6] & 0x0f > 0x00:       # 取音量值
        RDA_reg_02H = 0xd0
        RDA_reg_data[0] = 0x01
        RDA_reg_data[2] &= ~(1 << 4)
        RDA_reg_data[6] -= 1
        bus.write_i2c_block_data(radioaddress, RDA_reg_02H, RDA_reg_data)


# 显示音量大小
def show_volume():
    oledFunc.oledstr(oledaddress, 4, 4, 'Volume:')
    vol_l = 0x00    # 音量阶梯低位
    vol_h = 0x00    # 音量阶梯高位
    if RDA_reg_data[6] - 127:       # 减去基础大小
        for i in range(1, RDA_reg_data[6] - 126):
            if i < 9:
                vol_l = (vol_l >> 1) | 0x80
                oledFunc.oledfillarea(oledaddress, 5, 5, 60+i*4, 60+i*4 + 3, vol_l)
            else:
                vol_h = (vol_h >> 1) | 0x80
                oledFunc.oledfillarea(oledaddress, 5, 5, 60+i*4, 60+i*4 + 3, 0xff)
                oledFunc.oledfillarea(oledaddress, 4, 4, 60+i*4, 60+i*4 + 3, vol_h)
        for i in range(RDA_reg_data[6] - 126, 18):
            oledFunc.oledfillarea(oledaddress, 4, 5, 60+i*4, 60+i*4 + 3, 0x00)


# 显示FM频率
def show_frequency():
    # 计算频率
    temp = (RDA_reg_data[1] * 256) + (RDA_reg_data[2] & 0xc0)
    temp >>= 6
    frequency = float(100 * temp + 87000) / 1000
    oledFunc.oledstr(oledaddress, 2, 4, 'FM : ')
    oledFunc.oledstr(oledaddress, 2, 48, str(frequency))
    oledFunc.oledstr(oledaddress, 2, 92, ' MHz')
    channellist(frequency)      # 显示频道


# 显示系统信息：（1）CPU温度（2）GPU温度（3）Host Name（4）Host IP（5）Wlan0 IP（6）定时关机（7）固件版本
def showinfo():
    global flag_timing      # 定时关机时间
    global flag_shutdown    # 定时关机标志位
    global radio_timing
    flag = 0        # 菜单入口标志位
    flag_ok = 1     # 选择按钮
    flag_cls = 1    # 清屏标志位
    flag_disp = 1   # 主菜单显示标志位
    # 主菜单LIST
    distemp = ['1.CPU Temp  [  ]', '2.GPU Temp  [  ]', '3.Host Name [  ]', '4.Host IP   [  ]', '5.Wlan0 IP  [  ]',
               '6.Timehalt  [  ]', '7.Firmware  [  ]']
    # 手动清屏
    oledFunc.oledreset(oledaddress)
    time.sleep(0.1)

    while True:
        irbutton = btn.readbutton()     # 按键接收

        # 向前返回
        if irbutton == 'PREVIOUS':
            if flag == 0:               # 当前为主菜单
                # 手动清屏
                oledFunc.oledreset(oledaddress)
                time.sleep(0.1)
                display()   # 显示主屏信息
                break       # 跳出返回主屏
            elif flag != 0:     # 当前非主菜单
                flag = 0        # 返回主菜单
                flag_cls = 1    # 开启清屏
                flag_disp = 1   # 显示主菜单

        # 主菜单信息
        if flag == 0:
            if flag_cls:        # 清屏
                oledFunc.oledreset(oledaddress)
                time.sleep(0.1)
                flag_cls = 0    # 关闭清屏

            if irbutton == 'DOWN' and flag_ok < 7:      # 菜单向下选择
                flag_ok += 1        # 向下移动
                flag_disp = 1       # 开启主菜单更新
            if irbutton == 'UP' and flag_ok > 1:        # 菜单向上选择
                flag_ok -= 1        # 向上移动
                flag_disp = 1       # 开启主菜单更新
            if irbutton == 'PLAY':                      # 选择确认
                flag = flag_ok      # 根据确认位置跳转到对应目录
                flag_cls = 1        # 开启清屏
                #flag_disp = 1       # 开启主菜单更新

            if flag_disp:           # 主菜单信息显示
                flag_disp = 0       # 清标志位，关闭更新
                if flag_ok < 5:     # 前4行
                    oledFunc.oledstr(oledaddress, 0, 0, distemp[0])
                    oledFunc.oledstr(oledaddress, 2, 0, distemp[1])
                    oledFunc.oledstr(oledaddress, 4, 0, distemp[2])
                    oledFunc.oledstr(oledaddress, 6, 0, distemp[3])
                else:               # 后几行上移
                    oledFunc.oledstr(oledaddress, 0, 0, distemp[flag_ok - 4])
                    oledFunc.oledstr(oledaddress, 2, 0, distemp[flag_ok - 3])
                    oledFunc.oledstr(oledaddress, 4, 0, distemp[flag_ok - 2])
                    oledFunc.oledstr(oledaddress, 6, 0, distemp[flag_ok - 1])

                if flag_ok == 1:    # 选择按钮显示及移动
                    oledFunc.oledstr(oledaddress, 0, 104, 'OK')
                    oledFunc.oledstr(oledaddress, 0, 104, 'OK')
                    oledFunc.oledstr(oledaddress, 2, 104, '  ')
                    oledFunc.oledstr(oledaddress, 4, 104, '  ')
                    oledFunc.oledstr(oledaddress, 6, 104, '  ')
                elif flag_ok == 2:
                    oledFunc.oledstr(oledaddress, 0, 104, '  ')
                    oledFunc.oledstr(oledaddress, 2, 104, 'OK')
                    oledFunc.oledstr(oledaddress, 4, 104, '  ')
                    oledFunc.oledstr(oledaddress, 6, 104, '  ')
                elif flag_ok == 3:
                    oledFunc.oledstr(oledaddress, 0, 104, '  ')
                    oledFunc.oledstr(oledaddress, 2, 104, '  ')
                    oledFunc.oledstr(oledaddress, 4, 104, 'OK')
                    oledFunc.oledstr(oledaddress, 6, 104, '  ')
                else:
                    oledFunc.oledstr(oledaddress, 0, 104, '  ')
                    oledFunc.oledstr(oledaddress, 2, 104, '  ')
                    oledFunc.oledstr(oledaddress, 4, 104, '  ')
                    oledFunc.oledstr(oledaddress, 6, 104, 'OK')

        # （1）CPU温度信息
        elif flag == 1:
            # 读取CPU温度信息
            file = open("/sys/class/thermal/thermal_zone0/temp")
            # 读取结果，并转换为浮点数
            cpu_temp = float(file.read()) / 1000
            # 关闭文件
            file.close()
            if flag_cls:    # 清主菜单屏幕
                oledFunc.oledreset(oledaddress)
                time.sleep(0.1)
                flag_cls = 0    # 关闭清屏
            # 显示CPU温度
            oledFunc.oledstr(oledaddress, 1, 0, 'CPU TEMPERATURE:')
            oledFunc.oledstr(oledaddress, 4, 42, str(cpu_temp))
            time.sleep(0.5)

        # （2）GPU温度信息
        elif flag == 2:
            # 读取GPU温度信息
            gpu_temp = commands.getoutput('/opt/vc/bin/vcgencmd measure_temp').replace('temp=', '').replace('\'C', '')
            if flag_cls:        # 清主菜单屏幕
                oledFunc.oledreset(oledaddress)
                time.sleep(0.1)
                flag_cls = 0    # 关闭清屏
            # 显示GPU温度
            oledFunc.oledstr(oledaddress, 1, 0, 'GPU TEMPERATURE:')
            oledFunc.oledstr(oledaddress, 4, 50, str(gpu_temp))
            time.sleep(0.5)

        # （3）Host Name 信息
        elif flag == 3:
            if flag_cls:        # 清主菜单屏幕
                oledFunc.oledreset(oledaddress)
                time.sleep(0.1)
                flag_cls = 0    # 关闭清屏
            oledFunc.oledstr(oledaddress, 1, 0, ' LOCALHOST NAME ')
            oledFunc.oledstr(oledaddress, 4, 20, socket.gethostname())
            time.sleep(0.5)

        # （4）HOST IP 地址
        elif flag == 4:
            if flag_cls:        # 清主菜单屏幕
                oledFunc.oledreset(oledaddress)
                time.sleep(0.1)
                flag_cls = 0    # 关闭清屏
            oledFunc.oledstr(oledaddress, 1, 4, 'HOST IP ADDRESS')
            oledFunc.oledstr(oledaddress, 4, 28, socket.gethostbyname(socket.gethostname()))
            time.sleep(0.5)

        # （5）WLAN0 IP 地址
        elif flag == 5:
            if flag_cls:        # 清主菜单屏幕
                oledFunc.oledreset(oledaddress)
                time.sleep(0.1)
                flag_cls = 0    # 关闭清屏
            # 获取WLAN0 IP 地址
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            oledFunc.oledstr(oledaddress, 1, 0, 'WLAN0 IP ADDRESS')
            oledFunc.oledstr(oledaddress, 4, 12,
                             socket.inet_ntoa(fcntl.ioctl(s.fileno(),
                                                          0x8915, struct.pack('256s', 'wlan0'[:15]))[20:24]))
            time.sleep(0.5)

        # （6）定时关机设置
        elif flag == 6:
            if flag_cls:        # 清主菜单屏幕
                oledFunc.oledreset(oledaddress)
                time.sleep(0.1)
                flag_cls = 0    # 关闭清屏
            oledFunc.oledstr(oledaddress, 0, 0, 'Timing  Shutdown')

            # 设置关机时间
            if irbutton == 'UP' and flag_timing < 120:
                flag_timing += 10
            if irbutton == 'DOWN' and flag_timing > 10:
                flag_timing -= 10
            oledFunc.oledstr(oledaddress, 3, 40, str(flag_timing) + ' min  ')

            # 显示定时关机状态
            if flag_shutdown == 0:
                oledFunc.oledstr(oledaddress, 6, 0, 'Shutdown Not Set')
            if flag_shutdown == 1:
                oledFunc.oledstr(oledaddress, 6, 0, 'Shutdown ' + str(flag_timing) + ' min')

            if irbutton == 'PLAY':      # 确认设置
                # 手动清屏
                oledFunc.oledreset(oledaddress)
                time.sleep(0.1)
                if flag_shutdown == 0:      # 如果还未设置定时关机，进入设置
                    oledFunc.oledstr(oledaddress, 0, 0, ' Shutdown Setup ')
                    oledFunc.oledstr(oledaddress, 3, 0, ' Are you sure ? ')
                    oledFunc.oledstr(oledaddress, 6, 0, 'Press PLAY for Y')
                elif flag_shutdown == 1:    # 如果已经设置定时关机，进入取消
                    oledFunc.oledstr(oledaddress, 0, 0, ' Shutdown Cancel')
                    oledFunc.oledstr(oledaddress, 3, 0, ' Are you sure ? ')
                    oledFunc.oledstr(oledaddress, 6, 0, 'Press PLAY for Y')

                while True:
                    irbutton = btn.readbutton()

                    if flag_shutdown == 0:      # 如果还未设置定时关机，进入设置
                        if irbutton == 'PREVIOUS':      # 返回，不设置
                            # 手动清屏
                            oledFunc.oledreset(oledaddress)
                            time.sleep(0.1)
                            #flag_shutdown = 0
                            break
                        if irbutton == 'PLAY':          # 确认设置
                            os.system("sudo shutdown -h +" + str(flag_timing) + " &")
                            radio_timing = (flag_timing * 60 - 60) * 4      # 定时关闭RADIO
                            # 手动清屏
                            oledFunc.oledreset(oledaddress)
                            time.sleep(0.1)
                            flag_shutdown = 1           # 启动设置状态
                            break

                    if flag_shutdown == 1:      # 如果已经设置定时关机，进入取消
                        if irbutton == 'PREVIOUS':      # 返回，不取消
                            # 手动清屏
                            oledFunc.oledreset(oledaddress)
                            time.sleep(0.1)
                            #flag_shutdown = 1
                            break
                        if irbutton == 'PLAY':          # 确认取消
                            os.system("sudo shutdown -c")
                            # 手动清屏
                            oledFunc.oledreset(oledaddress)
                            time.sleep(0.1)
                            flag_shutdown = 0           # 启动未设置状态
                            break
                    time.sleep(0.2)

        # （7）固件版本信息
        elif flag == 7:
            if flag_cls:        # 清主菜单屏幕
                oledFunc.oledreset(oledaddress)
                time.sleep(0.1)
                flag_cls = 0    # 关闭清屏
            oledFunc.oledstr(oledaddress, 0, 0, 'Firmware Version')
            oledFunc.oledstr(oledaddress, 3, 0, 'RasPi_RADIO_V1.0')
            oledFunc.oledstr(oledaddress, 6, 24, 'BY CHRONOS')
            time.sleep(0.5)


# 显示当前系统时间
def showtime():
    oledFunc.oledstr(oledaddress, 6, 0, time.strftime("%y-%m%d %X"))


# 显示主屏信息
def display():
    show_frequency()        # 显示FM频率
    show_volume()           # 显示音量大小
    showtime()              # 显示当前系统时间


# 显示频道名称
def show_channel(val1, val2, val3, val4, val5, val6, val7, val8):
    global chan_temp
    for k in range(0, 8):
        if k == 0:
            chan_temp = val1
        elif k == 1:
            chan_temp = val2
        elif k == 2:
            chan_temp = val3
        elif k == 3:
            chan_temp = val4
        elif k == 4:
            chan_temp = val5
        elif k == 5:
            chan_temp = val6
        elif k == 6:
            chan_temp = val7
        elif k == 7:
            chan_temp = val8
        for j in range(0, 2):
            for i in range(0, 16):
                oledFunc.oledfillarea(oledaddress, j, 1, i + k * 16, (i+1) + k * 16, chan_temp[i + j * 16])


# 频道列表
def channellist(chan):
    if 88.7 <= chan <= 88.9:        # 88.8河北生活广播
        show_channel(ChannelWord.he, ChannelWord.bei, ChannelWord.sheng, ChannelWord.huo,
                     ChannelWord.guang, ChannelWord.bo, ChannelWord.null, ChannelWord.null)
    elif 89.0 <= chan <= 89.2:        # 89.1首都生活广播
        show_channel(ChannelWord.shou, ChannelWord.du, ChannelWord.sheng, ChannelWord.huo,
                     ChannelWord.guang, ChannelWord.bo, ChannelWord.null, ChannelWord.null)
    elif 89.4 <= chan <= 89.6:        # 89.5河北音乐广播
        show_channel(ChannelWord.he, ChannelWord.bei, ChannelWord.yin, ChannelWord.yue,
                     ChannelWord.guang, ChannelWord.bo, ChannelWord.null, ChannelWord.null)
    elif 91.0 <= chan <= 91.4:        # 91.1天津生活广播
        show_channel(ChannelWord.tian, ChannelWord.jin, ChannelWord.sheng, ChannelWord.huo,
                     ChannelWord.guang, ChannelWord.bo, ChannelWord.null, ChannelWord.null)
    elif 91.5 <= chan <= 91.8:        # 91.7唐山新闻综合广播
        show_channel(ChannelWord.tang, ChannelWord.shan, ChannelWord.xin, ChannelWord.wen,
                     ChannelWord.zong, ChannelWord.he2, ChannelWord.guang, ChannelWord.bo)
    elif 91.8 <= chan <= 92.0:        # 91.9河北交通广播
        show_channel(ChannelWord.he, ChannelWord.bei, ChannelWord.jiao, ChannelWord.tong,
                     ChannelWord.guang, ChannelWord.bo, ChannelWord.null, ChannelWord.null)
    elif 92.0 <= chan <= 92.2:        # 92.1天津相声广播
        show_channel(ChannelWord.tian, ChannelWord.jin, ChannelWord.xiang, ChannelWord.sheng2,
                     ChannelWord.guang, ChannelWord.bo, ChannelWord.null, ChannelWord.null)
    elif 94.9 <= chan <= 95.1:        # 95河北新闻广播
        show_channel(ChannelWord.he, ChannelWord.bei, ChannelWord.xin, ChannelWord.wen,
                     ChannelWord.guang, ChannelWord.bo, ChannelWord.null, ChannelWord.null)
    elif 96.7 <= chan <= 96.9:        # 96.8唐山交通广播
        show_channel(ChannelWord.tang, ChannelWord.shan, ChannelWord.jiao, ChannelWord.tong,
                     ChannelWord.guang, ChannelWord.bo, ChannelWord.null, ChannelWord.null)
    elif 97.1 <= chan <= 97.3:        # 97.2天津新闻广播
        show_channel(ChannelWord.tian, ChannelWord.jin, ChannelWord.xin, ChannelWord.wen,
                     ChannelWord.guang, ChannelWord.bo, ChannelWord.null, ChannelWord.null)
    elif 97.3 <= chan <= 97.5:        # 97.4北京音乐广播
        show_channel(ChannelWord.bei, ChannelWord.jing, ChannelWord.yin, ChannelWord.yue,
                     ChannelWord.guang, ChannelWord.bo, ChannelWord.null, ChannelWord.null)
    elif 106.7 <= chan <= 106.9:        # 106.8天津交通广播
        show_channel(ChannelWord.tian, ChannelWord.jin, ChannelWord.jiao, ChannelWord.tong,
                     ChannelWord.guang, ChannelWord.bo, ChannelWord.null, ChannelWord.null)
    else:
        oledFunc.oledstr(oledaddress, 0, 0, 'Chronos RPiRadio')     # 显示标题

# OLED RESET
oledFunc.oledreset(oledaddress)
time.sleep(1)
# 启动屏显
oledFunc.oledstr(oledaddress, 3, 0, ' CHRONOS  RADIO ')
time.sleep(2)
# OLED RESET
oledFunc.oledreset(oledaddress)
time.sleep(0.5)

# RADIO RESET
radioreset()

# 显示主屏信息
display()
oledFunc.oledstr(oledaddress, 0, 0, 'Chronos RPiRadio')     # 显示标题
time.sleep(0.5)

while True:
    irbutton = btn.readbutton()     # 按键接收
    if not irbutton:                # 没有按键
        showtime()                  # 更新系统时间
        if flag_shutdown == 1 and radio_timing > 0:
            radio_timing -= 1       # 定时关闭RADIO
        elif flag_shutdown == 1 and radio_timing == 0:    # 关闭RADIO
            # 手动清屏
            oledFunc.oledreset(oledaddress)
            time.sleep(0.1)
            # 启动屏显
            oledFunc.oledstr(oledaddress, 3, 0, ' RADIO SHUTDOWN ')
            time.sleep(2)
            oledFunc.oledreset(oledaddress)
            time.sleep(0.1)
            radioshutdown()     # 关闭RADIO
            quit()              # 退出程序
        time.sleep(0.25)        # 每秒更新4次
        continue

    if irbutton == 'NEXT':          # 向后搜台
        RDA_reg_02H |= (1 << 1)
        oledFunc.oledstr(oledaddress, 0, 0, '  FM SEEK ....  ')
        fmseek(RDA_reg_02H)
        show_frequency()            # 更新当前频率
        radio_timing = 50

    elif irbutton == 'PREVIOUS':      # 向前搜台
        RDA_reg_02H &= ~(1 << 1)
        oledFunc.oledstr(oledaddress, 0, 0, '  FM SEEK ....  ')
        fmseek(RDA_reg_02H)
        show_frequency()            # 更新当前频率

    elif irbutton == 'VOL+':          # 调大音量
        vol_up()
        show_volume()               # 更新音量大小

    elif irbutton == 'VOL-':          # 调小音量
        vol_down()
        show_volume()               # 更新音量大小

    elif irbutton == 'UP':            # 打开主菜单
        showinfo()

    elif irbutton == 'DOWN':          # 退出程序
        doquit()
