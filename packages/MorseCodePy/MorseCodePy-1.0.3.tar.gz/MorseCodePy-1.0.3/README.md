
# MorseCodePy 1.0.2
## Introduction
MorseCodePy is a module that simplifies the process of translating normal text into **Morse code**. This versatile module supports various languages, including **English**, **Russian**, **Spanish**, **numbers**, **symbols** and **other**.

## Installation

Installing project using pip:

`pip install MorseCodePy` or `pip3 install MorseCodePy`
    
## How to use
`encode(string, dit, dash)` returns string with translated into Morse code. `string` is your text, that you want to translate. Also, you can customise `dit` and `dash`.

`codes` is a dictionary with letters, numbers & symbols and their Morse code translations. **Warning**: translations use 1's and 0's.

`chart(dit, dash)` writes entire dictionary of letters and their Morse codes.

Examples:

```
import MorseCodePy as mcp

string = "SOS"
encode_string = mcp.encode(string)

print(encoded_string)
# Output: ··· --- ···
```

```
import MorseCodePy as mcp

string = "Bye!"
print(mcp.encode(string, dit='0', dash='1'))
# Output: 1000 1011 0 101011
```

```
from MorseCodePy import codes

print(codes['a'])
# Output: 01
```

```
import MorseCodePy as mcp

mcp.chart()
# Output: a: 01 b: 1110 ...
```

## Contact
**GitHub**: https://github.com/CrazyFlyKite

**Email**: karpenkoartem2846@gmail.com

**Discord**: CrazyFlyKite
