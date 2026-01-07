# How to Add Support for New MCU Chips to stcflash

## 📌 Overview

stcflash (The original stcgal) is a **STC MCU ISP Flash Programming Tool** that supports a wide range of STC 51/32 series microcontrollers. This document details how to add support for new chips.

---

## 👍Recommended for use ##
If you can work out the logic of failure, theoretically all MCUs can be supported (not limited to STC, STM, ESP, etc.).

This project welcomes you to submit code to improve it!

File address: https://wwanr.lanzouw.com/b00mq2gzoh

Password: gu10

---

## 🏗️ Project Architecture

```
User Command Line (stcflash -p /dev/ttyUSB0 firmware.hex)
    ↓
frontend.py (Frontend Selection Layer - Argument Parsing)
    ↓
protocols.py (Protocol Implementation - MCU Communication)
    ↓
models.py (Chip Database - MCU Specifications)
    ↓
Hardware (MCU)
```

Main files that need to be modified when adding new chips:
- **models.py** - Chip model definition and parameters
- **protocols.py** - Protocol detection rules
- **options.py** - (Optional) Chip-specific configuration options

---

## 🔧 Complete Steps to Add New Chip Support

### Step 1: Add Chip Model in models.py

**File Location**: `stcflash/models.py`

**Specific Location**: `models` tuple in `MCUModelDatabase` class (around lines 34-1175)

**MCUModel Field Description**:

```python
MCUModel(
    name='Chip Model Name',        # Example: 'STC15W104E'
    magic=0xXXXX,                  # Chip identification code (hexadecimal, obtained from status packet bytes 20-22)
    total=Total Memory Size,        # Total memory bytes, e.g., 65536
    code=Code Flash Size,           # Code Flash size (bytes)
    eeprom=EEPROM Size,            # EEPROM size (bytes), 0 means no EEPROM
    iap=IAP Support,               # True/False - whether IAP programming is supported
    calibrate=RC Calibration,      # True/False - whether RC oscillator calibration is supported
    mcs251=MCS251 Series,          # True/False - use True for STC32/MCS251 series
)
```

**Important Formula**:
```
total = code + eeprom
```

**Adding Location**: Add the new entry to the `models` tuple (before the closing parenthesis at line 1175)

**Example**:

If you want to add a new chip `STC15F204E` with specifications:
- Magic: 0xf2d0
- Total Memory: 65536 bytes
- Code: 61440 bytes
- EEPROM: 4096 bytes
- IAP Support: Yes
- Calibration Support: Yes
- MCS251: No

Add the code:
```python
MCUModel(name='STC15F204E', magic=0xf2d0, total=65536, code=61440, eeprom=4096, 
         iap=True, calibrate=True, mcs251=False),
```

**Key Points**:
- Magic value must be unique (cannot be duplicated with other chips)
- You can obtain the magic value by running stcflash and connecting to the chip, then checking debug output
- Or consult the chip's official datasheet

---

### Step 2: Determine the Communication Protocol for the Chip

**Supported Protocols**:

| Protocol Name | Applicable Chip Series | Features |
|--------------|----------------------|----------|
| `stc89` | STC89/90 | 8-bit checksum, no parity |
| `stc89a` | STC89/90 (BSL 7.2.5C) | 16-bit checksum, newer BSL version |
| `stc12` | STC10/11/12 | 16-bit checksum, even parity |
| `stc12a` | STC12x052 | Special handling |
| `stc12b` | STC12x52/56 | Special handling |
| `stc15a` | STC15x104E | Special protocol |
| `stc15` | Most STC15 series | RC calibration support, newer chips |
| `stc8` | STC8A8K64S4A12 etc. | New generation chips |
| `stc8d` | All STC8 and STC32 series | Latest chips |
| `stc8g` | STC8G1, STC8H1 | Specific models |

**How to Determine the Chip Protocol**:
1. Check the chip model naming convention
2. Refer to existing similar chips (search for same model prefix in models.py)
3. Check BSL version information in the chip's official datasheet

**Examples**:
- `STC15W104` → Use `stc15` protocol
- `STC8H8K16U` → Use `stc8d` protocol
- `STC89C52RC` → Use `stc89` or `stc89a` protocol

---

### Step 3: Add Rule in Protocol Auto-detection

**File Location**: `stcflash/protocols.py`

**Specific Location**: Lines 71-91 in `StcAutoProtocol` class's `initialize_model()` method

**Current Code Around Line 480**:
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

**Adding New Rules** (in the `protocol_database` list):

Use regular expressions to match chip model names:

```python
# New rule examples
("stc15", r"STC15F204"),  # Match STC15F204* series
("stc8d", r"STC8A8K\d\dD\d"),  # Match specific STC8A series
```

**Regular Expression Explanation**:
- `\d` - Match any digit (0-9)
- `[ABC]` - Match any one of A, B, C
- `*` - Previous element appears 0 or more times
- `$` - End of string
- `()` - Grouping
- `|` - OR operator

**Testing Rules**:
```python
import re
pattern = r"STC15F\d+"
re.match(pattern, "STC15F204E")  # True
re.match(pattern, "STC15W104")   # False
```

**Rule Order is Important**:
- More specific rules should be placed first
- Example: Write `STC15F\d+` before `STC15\D`

---

### Step 4: (Optional) Add Chip-specific Configuration Options

**File Location**: `stcflash/options.py`

This step is only needed if the chip has special configuration options (such as RC calibration, watchdog, low voltage reset, etc.).

**Existing Option Classes**:
- `Stc89Option` - STC89 series (supports cpu_6t_enabled, etc.)
- `Stc12Option` - STC12 series
- `Stc15Option` - STC15 series
- `Stc8Option` - STC8 series

**Template for Creating New Option Class**:

```python
class YourChipOption(BaseOption):
    """Chip-specific option handling"""

    def __init__(self, msr):
        super().__init__()
        self.msr = bytearray(msr)  # msr is configuration bytes extracted from status packet
        
        self.options = (
            ("option_name1", self.get_option1, self.set_option1),
            ("option_name2", self.get_option2, self.set_option2),
        )

    def get_msr(self):
        """Return configuration bytes for programming to chip"""
        return bytes(self.msr)

    def get_option1(self):
        """Get current value of option 1"""
        return bool(self.msr[0] & 0x01)

    def set_option1(self, val):
        """Set option 1"""
        val = Utils.to_bool(val)
        self.msr[0] &= 0xfe  # Clear bit 0
        self.msr[0] |= 0x01 if val else 0x00
```

**Note**:
- Most new chips can use existing protocol classes and their options
- Only create new classes if the chip has unique configuration options

---

### Step 5: Register New Protocol in Frontend (Usually Not Needed)

**File Location**: `stcflash/frontend.py`

**Location**: `initialize_protocol()` method of `stcflash` class (lines 52-82)

**Current Code**:
```python
def initialize_protocol(self, opts):
    """Initialize protocol backend"""
    if opts.protocol == "stc89":
        self.protocol = Stc89Protocol(opts.port, opts.handshake, opts.baud)
    elif opts.protocol == "stc89a":
        self.protocol = Stc89AProtocol(opts.port, opts.handshake, opts.baud)
    # ... more protocols ...
    else:
        self.protocol = StcAutoProtocol(opts.port, opts.handshake, opts.baud)
```

**Explanation**:
- When using auto-detection mode (`-P auto`), stcflash automatically matches the correct protocol based on magic value
- Usually no need to modify this
- Only add when creating entirely new protocol classes

---

## 🧪 Verification Steps

### 1. Check Magic Value Uniqueness

```bash
cd c:\Users\CXi\Desktop\stcflash-master
grep -o "magic=0x[a-fA-F0-9]*" stcflash/models.py | sort | uniq -d
```

If there is output, it means there are duplicate magic values that need to be modified.

### 2. Check Protocol Matching

Test regular expressions in Python:

```python
import re

# Test new rule
pattern = r"STC15F\d+"
chip_names = ["STC15F204E", "STC15F104W", "STC15W104"]

for name in chip_names:
    if re.match(pattern, name):
        print(f"{name}: Match successful")
    else:
        print(f"{name}: No match")
```

### 3. Test Programming

Connect the new chip and try programming:

```bash
python stcflash.py -p COM3 -P auto firmware.hex
```

Observe the output to check if:
- The chip model is correctly identified
- The correct protocol is auto-detected
- Flash size information is displayed correctly

---

## 📝 Complete Example

Suppose you want to add a new chip **XYZ8051-32K** with the following specifications:
- Chip Model Name: `XYZ8051-32K`
- Magic Value: `0xabc1`
- Total Memory: 65536 bytes
- Code Flash: 32768 bytes
- EEPROM: 32768 bytes
- IAP Support: Yes
- Calibration Support: Yes
- MCS251: No
- Protocol: stc8d

### Modification Steps

#### Step 1: models.py

Add to the `models` tuple in `MCUModelDatabase` class:

```python
MCUModel(name='XYZ8051-32K', magic=0xabc1, total=65536, code=32768, eeprom=32768,
         iap=True, calibrate=True, mcs251=False),
```

#### Step 2: protocols.py

Add to `protocol_database` in `StcAutoProtocol.initialize_model()`:

```python
protocol_database = [
    # ... existing rules ...
    ("stc8d", r"XYZ8051"),  # New: Match XYZ8051 series
    # ... more rules ...
]
```

#### Step 3: Compile and Test

```bash
# Test regular expression
python -c "import re; print(bool(re.match(r'XYZ8051', 'XYZ8051-32K')))"  # Output: True

# Test programming
python stcflash.py -p COM3 test.hex
```

---

## ⚠️ Important Considerations

### Rules That Must Be Followed

1. **Magic Value Uniqueness**
   - Each chip's magic value must be unique
   - Cannot be duplicated with existing magic values in models.py
   - Magic value must be obtained from hardware or official datasheet

2. **Memory Allocation**
   ```
   total = code + eeprom
   code ≥ 0
   eeprom ≥ 0
   ```

3. **Correct Protocol Selection**
   - Incorrect protocol will cause programming failure
   - Selected protocol must already be implemented in protocols.py
   - When using auto-detection, rules must match accurately

4. **Regular Expression Rules**
   - Avoid overly broad rules that conflict with existing chips
   - Place specific rules before generic rules
   - Test rules to ensure no false matches with other chips

### Common Errors

| Error | Symptom | Solution |
|-------|---------|----------|
| Duplicate Magic Value | Chip identified as another model | Check all magic values in models.py |
| Protocol Mismatch | Programming failure, communication errors | Verify chip model's corresponding protocol |
| Regex Too Broad | Multiple chips match same rule | Make rule more specific |
| Memory Allocation Error | Data overflow during programming | Ensure `code + eeprom = total` |

---

## 📚 Reference Resources

- **STC Official**: http://stcmcu.com/
- **Project Homepage**: https://github.com/grigorig/stcflash
- **Protocol Documentation**: See protocol description files in `doc/reverse-engineering/` directory
- **Existing Chips**: models.py contains 150+ chip definitions that can serve as reference

---

## 🎯 Quick Verification Checklist

Before submitting a new chip, verify the following:

- [ ] MCUModel added to models tuple in models.py
- [ ] Magic value is unique (no duplicates)
- [ ] code + eeprom = total
- [ ] Selected protocol exists in protocols.py
- [ ] Protocol detection rule added to StcAutoProtocol
- [ ] Regular expression rule tested
- [ ] No conflicts with existing chip rules
- [ ] (If needed) Created chip-specific option class

---

## 🚀 Next Steps

1. Connect new chip to programmer
2. Run stcflash in auto-detection mode
3. Verify chip is correctly identified
4. Try programming a test firmware
5. Verify programming is successful

Success! Your new chip is now supported by stcflash.
