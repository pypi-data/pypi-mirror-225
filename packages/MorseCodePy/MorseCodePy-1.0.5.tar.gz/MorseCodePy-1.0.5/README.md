
# MorseCodePy v1.0.5

## Introduction
MorseCodePy is a module that simplifies the process of translating normal text into **Morse code**. This versatile module supports various languages, including **English**, **Russian**, **Spanish**, **numbers**, **symbols** and **other**.

## Installation

Installing module using pip:

`pip install MorseCodePy` or `pip3 install MorseCodePy`
    
## How to use
`encode(string, dit, dash)` returns string with translated into Morse code. `string` is your text, that you want to translate. Also, you can customise `dit` and `dash`.

`chart(dit, dash)` writes entire dictionary of letters and their Morse codes.

`codes` is a dictionary with letters, numbers & symbols and their Morse code translations. **Warning**: translations use **1**'s and **0**'s.

Code examples:

```
import MorseCodePy as mc

string = "SOS"
encode_string = mc.encode(string)

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
import MorseCodePy as mc

mc.chart()
# Output: a: ·- b: ---· ...
```

## Contact
- Discord: CrazyFlyKite

- Email: karpenkoartem2846@gmail.com

- [GitHub](https://github.com/CrazyFlyKite)
