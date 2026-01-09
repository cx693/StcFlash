# stcflash

---
If you want to join my project!/如果你想加入我的项目！
Please submit your application and then send me an email at the following address: pycx0@qq.com
请提交申请后，给我发邮箱📮：pycx0@qq.com
---
## 理论支持所有的 STC! 验证支持 Ai8051U 等。
## Theory supports all STCS! Verify support for Ai8051U, etc.

### stcflash 是基于 stcgal 的二次开发！
### stcflash is a secondary development based on stcgal!

Stcgal 原始项目地址：https://github.com/grigorig/stcgal

---

Stcgal original project address: https://github.com/grigorig/stcgal

## 硬件连接 / Hardware Connection

```
CH340 <-> MCU
3.3V  -- VIN/VCC
TXD   -- RXD
RXD   -- TXD
GND   -- GND
```

## 关于失败逻辑 / About Failure Logic

如果你们可以研究出来失败的逻辑，理论上支持所有的MCU（不限于STC、STM、ESP等等）。
If you can work out the logic of failure, theoretically all MCUs can be supported (not limited to STC, STM, ESP, etc.).

本项目支持你们提交代码修改完善这个项目！
This project welcomes you to submit code to improve it!

文件地址：https://wwanr.lanzouw.com/b00mq2gzoh
File address: https://wwanr.lanzouw.com/b00mq2gzoh

密码：gu10
Password: gu10

## 简介 / Introduction

stcflash 是一个用于 [STC MCU Ltd](http://stcmcu.com/) 的命令行 Flash 编程工具，支持 8051 兼容的微控制器。
stcflash is a command line flash programming tool for [STC MCU Ltd](http://stcmcu.com/) 8051 compatible microcontrollers.

STC 微控制器具有基于 UART/USB 的引导程序加载器 (BSL)。它使用基于数据包的协议通过串行链接对代码内存和 IAP 内存进行编程。这被称为在线系统编程 (ISP)。
STC microcontrollers have an UART/USB based bootstrap loader (BSL). It utilizes a packet-based protocol to flash the code memory and IAP memory over a serial link. This is referred to as in-system programming (ISP).

BSL 还用于配置各种（类似保险丝的）设备选项。遗憾的是，该协议未公开，STC 仅提供了一个（粗糙的）Windows GUI 应用程序用于编程。
The BSL is also used to configure various (fuse-like) device options. Unfortunately, this protocol is not publicly documented and STC only provides a (crude) Windows GUI application for programming.

stcflash 是 STC Windows 软件的全功能开源替代品。
stcflash is a full-featured open source replacement for STC's Windows software.

它支持范围广泛的 MCU，具有很强的便携性，适合自动化使用。
It supports a wide range of MCUs, is very portable and suitable for automation.

## 功能特性 / Features

* 支持 STC 89/90/10/11/12/15/8/32 系列
  Support for STC 89/90/10/11/12/15/8/32 series

* UART 和 USB BSL 支持
  UART and USB BSL support

* 显示芯片信息
  Display chip information

* 确定运行频率
  Determine operating frequency

* 编程 Flash 内存
  Program flash memory

* 编程 IAP/EEPROM
  Program IAP/EEPROM

* 设置设备选项
  Set device options

* 读取唯一设备 ID（STC 10/11/12/15/8）
  Read unique device ID (STC 10/11/12/15/8)

* 调整 RC 振荡器频率（STC 15/8）
  Trim RC oscillator frequency (STC 15/8)

* 通过 DTR 切换或自定义 Shell 命令自动电源循环
  Automatic power-cycling with DTR toggle or a custom shell command

* 自动 UART 协议检测
  Automatic UART protocol detection

## 快速开始 / Quickstart

### 源码安装 / Source Code Installation

```bash
pip install .
```

### 使用 pip 安装 / Install with pip

安装 stcflash（可能需要 root/管理员权限）：
Install stcflash (might need root/administrator privileges):

```bash
pip3 install stcflash
```

### 查看帮助 / Show Help

调用 stcflash 并显示使用帮助：
Call stcflash and show usage:

```bash
stcflash -h
```

## 更多信息 / Further Information

* [添加新的 MCU 型号](doc/zh_CN/Add_MCU.md) / [Adding new MCU models](doc/Add_MCU.md)

* [如何使用 stcflash](doc/zh_CN/USAGE.md) / [How to use stcflash](doc/USAGE.md)

* [常见问题](doc/zh_CN/FAQ.md) / [Frequently Asked Questions](doc/FAQ.md)

* [测试过的 MCU 型号列表](doc/zh_CN/MODELS.md) / [List of tested MCU models](doc/MODELS.md)

## 许可证 / License

stcflash 根据 MIT 许可证发布。
stcflash is published under the MIT license.
