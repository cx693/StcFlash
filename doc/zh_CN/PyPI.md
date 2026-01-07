stcflash - 用于STC MCU的ISP闪存工具
===============================

stcflash是用于[STC MCU Ltd](http://stcmcu.com/)的命令行闪存编程工具。 兼容8051微控制器。

STC微控制器具有基于UART / USB的引导加载程序（BSL）。 
它采用系统内编程，即基于数据包的协议通过串行链路刷新代码存储器和IAP存储器。 
BSL还用于配置各种设备选项。 不幸的是，该协议没有公开记录，STC仅提供（粗略的）Windows GUI应用程序进行编程

stcflash是STC的Windows软件的功能全面的开源替代品。 它支持多种MCU，非常便携，适合自动下载。
