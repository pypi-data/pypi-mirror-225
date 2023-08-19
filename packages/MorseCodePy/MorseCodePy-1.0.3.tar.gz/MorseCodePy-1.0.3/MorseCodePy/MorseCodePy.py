codes = {
    # Latin
    'a': '01', 'b': '1000', 'c': '1010', 'd': '100', 'e': '0', 'f': '0010', 'g': '110', 'h': '0000',
    'i': '00', 'j': '0111', 'k': '101', 'l': '0100', 'm': '11', 'n': '10', 'o': '111', 'p': '0110',
    'q': '1101', 'r': '010', 's': '000', 't': '1', 'u': '001', 'v': '0001', 'w': '011', 'x': '1001',
    'y': '1011', 'z': '1100', 'à': '01101', 'á': '01101', 'â': '01101', 'ç': '10100', 'é': '00100',
    'è': '01001', 'ê': '10010', 'ë': '00100', 'ï': '10011', 'ñ': '11011', 'ó': '1110', 'ü': '0011',
    # Cyrillic
    'а': '01', 'б': '1000', 'в': '011', 'г': '110', 'ґ': '110', 'д': '100', 'е': '0', 'ё': '0', 'є': '00100',
    'ж': '0001', 'з': '1100', 'и': '00', 'і': '00', 'ї': '01110', 'й': '0111', 'к': '101', 'л': '0001',
    'м': '11', 'н': '10', 'о': '111', 'п': '0110', 'р': '010', 'с': '000', 'т': '1', 'у': '001', 'ф': '0010',
    'х': '0000', 'ц': '1010', 'ч': '1110', 'ш': '1111', 'щ': '1101', 'ъ': '11011', 'ы': '1011', 'ь': '1001',
    'э': '00100', 'ю': '0011', 'я': '0101',
    # Numbers
    '0': '11111', '1': '01111', '2': '00111', '3': '00011', '4': '00001', '5': '00000', '6': '10000',
    '7': '11000', '8': '11100', '9': '11110',
    # Symbols
    ' ': ' ', '\n': '\n', '.': '010101', ',': '110011', '!': '101011', '?': '001100', '@': '011010',
    '/': '10010', '\\': '10010', '&': '01000', ';': '101010', ':': '111000', '\'': '011110',
    '\"': '010010', '$': '0001001', '+': '01010', '-': '100001', '=': '10001', '_': '001101'
}


def encode(string: str, dit: str = '·', dash: str = '-', separator: str = '/') -> str:
    """
    This function translates your string into Morse code.
    You can customise dits and dashes
    """

    t_string = str()  # New string that will hold translated text
    string = string.lower()

    char: int = 0
    while char != len(string):
        if string[char] == 'c' and string[char + 1] == 'h':
            t_string += '1111'.replace('1', dash) + ' '
            char += 1
        elif string[char] == ' ':
            t_string += separator + ' '
        else:
            try:
                t_string += codes[string[char]].replace('0', dit).replace('1', dash) + ' '
            except KeyError:
                t_string += '* '  # If character isn't is dictionary "codes"

        char += 1

    return t_string.rstrip()

def chart(dit: str = '·', dash: str = '-') -> None:
    print("Morse Code Chart:")

    for char, morse_code in codes.items():
        print(f"{char}: {morse_code.replace('0', dit).replace('1', dash)}")
