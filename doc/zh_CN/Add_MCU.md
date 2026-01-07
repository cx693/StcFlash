# 如何向 stcgal 添加新的 MCU 芯片支持

## 📌 概述

stcgal 是一个 **STC MCU ISP Flash 编程工具**，支持多种 STC 51/32 系列微控制器。本文档详细说明如何添加新芯片支持。

---

## 🏗️ 项目架构

```
用户命令行 (stcgal -p /dev/ttyUSB0 firmware.hex)
    ↓
frontend.py (前端选择层 - 参数解析)
    ↓
protocols.py (具体协议实现 - 与芯片通信)
    ↓
models.py (芯片数据库 - 芯片规格定义)
    ↓
硬件 (MCU)
```

添加新芯片需要修改的主要文件：
- **models.py** - 芯片型号定义和参数
- **protocols.py** - 协议识别规则
- **options.py** - （可选）芯片特定配置选项

---

## 🔧 添加新芯片的完整步骤

### 第 1 步：在 models.py 中添加芯片模型

**文件位置**：`stcgal/models.py`

**具体位置**：`MCUModelDatabase` 类中的 `models` 元组（大约第34-1175行）

**MCUModel 字段说明**：

```python
MCUModel(
    name='芯片型号名称',           # 例如: 'STC15W104E'
    magic=0xXXXX,                  # 芯片识别码（16进制，从芯片状态包字节20-22获取）
    total=内存总大小,               # 总内存字节数，例如 65536
    code=代码段大小,                # Code Flash 大小（字节）
    eeprom=EEPROM大小,             # EEPROM 大小（字节），0 表示无 EEPROM
    iap=是否支持IAP,                # True/False - 是否支持 IAP 编程
    calibrate=是否支持校准,         # True/False - 是否支持 RC 振荡器校准
    mcs251=是否是MCS251体系,        # True/False - STC32/MCS251 系列用 True
)
```

**重要公式**：
```
total = code + eeprom
```

**添加位置**：将新项添加到 `models` 元组中（在第1175行的闭合括号前）

**示例**：

如果要添加一个新芯片 `STC15F204E`，根据规格书信息：
- Magic: 0xf2d0
- 总内存: 65536 字节
- Code: 61440 字节  
- EEPROM: 4096 字节
- 支持 IAP：是
- 支持校准：是
- MCS251：否

添加代码：
```python
MCUModel(name='STC15F204E', magic=0xf2d0, total=65536, code=61440, eeprom=4096, 
         iap=True, calibrate=True, mcs251=False),
```

**关键点**：
- Magic 值必须唯一（不能与其他芯片重复）
- 可以通过运行 stcgal 连接芯片后，从调试输出获取 magic 值
- 或查看芯片官方规格书/数据表

---

### 第 2 步：确定芯片使用的通信协议

**支持的协议列表**：

| 协议名称 | 适用芯片系列 | 特点说明 |
|--------|----------|---------|
| `stc89` | STC89/90 | 8位校验和，无校偶位 |
| `stc89a` | STC89/90 (BSL 7.2.5C) | 16位校验和，更新的 BSL 版本 |
| `stc12` | STC10/11/12 | 16位校验和，偶校偶位 |
| `stc12a` | STC12x052 | 特殊处理 |
| `stc12b` | STC12x52/56 | 特殊处理 |
| `stc15a` | STC15x104E | 特殊协议 |
| `stc15` | 大多数 STC15 系列 | 支持 RC 校准、较新芯片 |
| `stc8` | STC8A8K64S4A12 等 | 新一代芯片 |
| `stc8d` | 所有 STC8 和 STC32 系列 | 最新芯片 |
| `stc8g` | STC8G1, STC8H1 | 特定型号 |

**如何判断芯片协议**：
1. 查看芯片型号命名规则
2. 参考现有相似芯片（在 models.py 中搜索相同型号前缀）
3. 查看芯片官方规格书中的 BSL 版本信息

**示例**：
- `STC15W104` → 使用 `stc15` 协议
- `STC8H8K16U` → 使用 `stc8d` 协议  
- `STC89C52RC` → 使用 `stc89` 或 `stc89a` 协议

---

### 第 3 步：在协议自动检测中添加规则

**文件位置**：`stcgal/protocols.py`

**具体位置**：第 71-91 行 `StcAutoProtocol` 类的 `initialize_model()` 方法

**现有代码 480行附近**：
```python
def initialize_model(self):
    super().initialize_model()

    protocol_database = [("stc89", r"STC(89|90)(C|LE)\d"),
                         ("stc12a", r"STC12(C|LE)\d052"),
                         ("stc12b", r"STC12(C|LE)(52|56)"),
                         ("stc12", r"(STC|IAP)(10|11|12)\D"),
                         ("stc15a", r"(STC|IAP)15[FL][012]0\d(E|EA|)$"),
                         ("stc15", r"(STC|IAP|IRC)15\D"),
                         ("stc8g", r"STC8H1K\d\d$"),
                         ("stc8g", r"STC8G"),
                         ("stc8d", r"STC8H"),
                         ("stc8d", r"STC32"),
                         ("stc8d", r"STC8A8K\d\dD\d"),
                         ("stc8", r"STC8\D")]

    for protocol_name, pattern in protocol_database:
        if re.match(pattern, self.model.name):
            self.protocol_name = protocol_name
            break
    else:
        self.protocol_name = None
```

**添加新规则**（在 `protocol_database` 列表中添加）：

使用正则表达式匹配芯片型号名称：

```python
# 新增规则示例
("stc15", r"STC15F204"),  # 匹配 STC15F204* 系列
("stc8d", r"STC8A8K\d\dD\d"),  # 匹配特定 STC8A 系列
```

**正则表达式说明**：
- `\d` - 匹配任何数字 (0-9)
- `[ABC]` - 匹配 A、B、C 中的任意一个
- `*` - 前面的元素出现 0 次或多次
- `$` - 字符串结束
- `()` - 分组
- `|` - 或操作符

**测试规则**：
```python
import re
pattern = r"STC15F\d+"
re.match(pattern, "STC15F204E")  # True
re.match(pattern, "STC15W104")   # False
```

**规则顺序很重要**：
- 更具体的规则应该放在前面
- 例如：先写 `STC15F\d+` 再写 `STC15\D`

---

### 第 4 步：（可选）添加芯片特定配置选项

**文件位置**：`stcgal/options.py`

只有在芯片有特殊配置选项（如 RC 校准、看门狗、低电压复位等）时才需要此步骤。

**现有选项类**：
- `Stc89Option` - STC89 系列（支持 cpu_6t_enabled 等）
- `Stc12Option` - STC12 系列
- `Stc15Option` - STC15 系列
- `Stc8Option` - STC8 系列

**创建新选项类的模板**：

```python
class YourChipOption(BaseOption):
    """芯片特定选项处理"""

    def __init__(self, msr):
        super().__init__()
        self.msr = bytearray(msr)  # msr 是从状态包中提取的配置字节
        
        self.options = (
            ("option_name1", self.get_option1, self.set_option1),
            ("option_name2", self.get_option2, self.set_option2),
        )

    def get_msr(self):
        """返回配置字节以编程到芯片"""
        return bytes(self.msr)

    def get_option1(self):
        """获取选项1的当前值"""
        return bool(self.msr[0] & 0x01)

    def set_option1(self, val):
        """设置选项1"""
        val = Utils.to_bool(val)
        self.msr[0] &= 0xfe  # 清除第 0 位
        self.msr[0] |= 0x01 if val else 0x00
```

**注意**：
- 大多数新芯片可以使用现有的协议类及其选项
- 只在芯片有独特的配置选项时才需要创建新类

---

### 第 5 步：在前端注册新协议（通常不需要）

**文件位置**：`stcgal/frontend.py`

**位置**：`StcGal` 类的 `initialize_protocol()` 方法（第52-82行）

**现有代码**：
```python
def initialize_protocol(self, opts):
    """Initialize protocol backend"""
    if opts.protocol == "stc89":
        self.protocol = Stc89Protocol(opts.port, opts.handshake, opts.baud)
    elif opts.protocol == "stc89a":
        self.protocol = Stc89AProtocol(opts.port, opts.handshake, opts.baud)
    # ... 更多协议 ...
    else:
        self.protocol = StcAutoProtocol(opts.port, opts.handshake, opts.baud)
```

**说明**：
- 使用自动检测时（`-P auto`），stcgal 会根据 magic 值自动匹配到正确的协议
- 通常不需要修改此处
- 只有创建全新协议类时才需要添加

---

## 🧪 验证步骤

### 1. 检查 Magic 值唯一性

```bash
cd c:\Users\CXi\Desktop\stcgal-master
grep -o "magic=0x[a-fA-F0-9]*" stcgal/models.py | sort | uniq -d
```

如果有输出，说明存在重复的 magic 值，需要修改。

### 2. 检查协议匹配

在 Python 中测试正则表达式：

```python
import re

# 测试新规则
pattern = r"STC15F\d+"
chip_names = ["STC15F204E", "STC15F104W", "STC15W104"]

for name in chip_names:
    if re.match(pattern, name):
        print(f"{name}: 匹配成功")
    else:
        print(f"{name}: 不匹配")
```

### 3. 测试编程

连接新芯片并尝试编程：

```bash
python stcgal.py -p COM3 -P auto firmware.hex
```

观察输出，检查是否：
- 正确识别芯片型号
- 自动检测到正确的协议
- 显示正确的 Flash 大小信息

---

## 📝 完整实例

假设要添加一个新芯片 **XYZ8051-32K**，规格如下：
- 芯片型号名：`XYZ8051-32K`
- Magic 值：`0xabc1`
- 总内存：65536 字节
- Code Flash：32768 字节
- EEPROM：32768 字节
- 支持 IAP：是
- 支持校准：是
- MCS251：否
- 使用协议：stc8d

### 修改步骤

#### 步骤 1：models.py

在 `MCUModelDatabase` 类的 `models` 元组中添加：

```python
MCUModel(name='XYZ8051-32K', magic=0xabc1, total=65536, code=32768, eeprom=32768,
         iap=True, calibrate=True, mcs251=False),
```

#### 步骤 2：protocols.py

在 `StcAutoProtocol.initialize_model()` 的 `protocol_database` 中添加：

```python
protocol_database = [
    # ... 现有规则 ...
    ("stc8d", r"XYZ8051"),  # 新增：匹配 XYZ8051 系列
    # ... 更多规则 ...
]
```

#### 步骤 3：编译并测试

```bash
# 测试正则表达式
python -c "import re; print(bool(re.match(r'XYZ8051', 'XYZ8051-32K')))"  # 输出: True

# 测试编程
python stcgal.py -p COM3 test.hex
```

---

## ⚠️ 重要注意事项

### 必须遵守的规则

1. **Magic 值唯一性**
   - 每个芯片的 magic 值必须唯一
   - 不能与 models.py 中现有的 magic 值重复
   - Magic 值必须从硬件获取或官方规格书获取

2. **存储分配**
   ```
   total = code + eeprom
   code ≥ 0
   eeprom ≥ 0
   ```

3. **协议选择正确**
   - 错误的协议会导致编程失败
   - 选择的协议类必须已在 protocols.py 中实现
   - 使用自动检测时，规则必须准确匹配

4. **正则表达式规则**
   - 避免过于宽泛的规则与现有芯片冲突
   - 特殊规则放在前面，通用规则放在后面
   - 测试规则确保不会误匹配其他芯片

### 常见错误

| 错误 | 症状 | 解决方案 |
|------|------|--------|
| Magic 值重复 | 芯片被识别为另一个型号 | 检查 models.py 中的所有 magic 值 |
| 协议不匹配 | 编程失败，通信错误 | 验证芯片型号对应的协议 |
| 正则表达式过宽 | 多个芯片匹配同一规则 | 使规则更具体 |
| 存储分配错误 | 编程时数据溢出 | 确保 `code + eeprom = total` |

---

## 📚 参考资源

- **STC 官方**：http://stcmcu.com/
- **项目主页**：https://github.com/grigorig/stcgal
- **协议文档**：查看 `doc/reverse-engineering/` 目录中的协议说明文件
- **现有芯片**：models.py 中有 150+ 种芯片定义，可作为参考

---

## 🎯 快速检查清单

在提交新芯片前，检查以下项目：

- [ ] MCUModel 已添加到 models.py 的 models 元组
- [ ] Magic 值唯一（没有重复）
- [ ] code + eeprom = total
- [ ] 选择的协议在 protocols.py 中存在
- [ ] 协议识别规则已添加到 StcAutoProtocol
- [ ] 正则表达式规则经过测试
- [ ] 没有与现有芯片冲突的规则
- [ ] （如需要）创建了特定的选项类

---

## 🚀 后续步骤

1. 连接新芯片到编程器
2. 运行 stcgal 的自动检测模式
3. 验证芯片被正确识别
4. 尝试编程一个测试固件
5. 验证编程成功

成功！现在你的新芯片已支持 stcgal。
