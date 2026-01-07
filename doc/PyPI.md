stcflash - STC MCU ISP flash tool
===============================

stcflash is a command line flash programming tool for [STC MCU Ltd](http://stcmcu.com/).
8051 compatible microcontrollers.

STC microcontrollers have an UART/USB based boot strap loader (BSL). It
utilizes a packet-based protocol to flash the code memory and IAP
memory over a serial link. This is referred to as in-system programming
(ISP).  The BSL is also used to configure various (fuse-like) device
options. Unfortunately, this protocol is not publicly documented and
STC only provide a (crude) Windows GUI application for programming.

stcflash is a full-featured Open Source replacement for STC's Windows
software; it supports a wide range of MCUs, it is very portable and
suitable for automation.