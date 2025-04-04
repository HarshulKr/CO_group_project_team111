#conversions
#####################################################################################
def twos_complement1(n: int, bit_length: int = 32) -> str:
    return format((1 << bit_length) + n, f'0{bit_length}b')

def binconv1(n):
    if n<0:
        return twos_complement1(n)
    return format(n, '032b')

def binary_to_decimal(binary: str) -> int:
    length = len(binary)
    is_negative = binary[0] == '1'
    if is_negative:
        inverted = ''.join('0' if bit == '1' else '1' for bit in binary)
        decimal = int(inverted, 2) + 1
        return -decimal
    else:
        return int(binary, 2)

def decimal_to_hex(n):
    result = f'{n:x}'
    result = [i for i in result]
    for i in range(len(result)):
        if result[i].isalpha():
            result[i] = result[i].upper()
    result = ''.join(result)
    l= len(result)
    final=''
    for i in range(0,8-l):
        final= final+'0'
    result='0x'+final+result
    return result
#######################################################################################
#I/O
#######################################################################################
with open(output,'w') as file:
    file.write("")

def read_assembly_file(filename):
    instructions = []
    with open(filename,'r') as file:
        for line in file:
            line=line.strip()
            if line and not line.startswith('#'):
                instructions.append(line)
    return instructions

def printer():
    with open(output, 'a') as file:
        file.write(f"0b{binconv1(pc)} ")
        for i in range(32):
            file.write(f"0b{binconv1(arr[i])} ")  
        file.write("\n")
    # printer2()
##########################################################################################
def end():  
    with open(output, 'a') as file:
        for key, value in ram_dict.items():
            file.write(f"{key}:0b{binconv1(value)}\n")
