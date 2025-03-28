pc = 0
arr = [0] * 32
ram_dict = {
    addr: 0 for addr in [
        "0x00010000", "0x00010004", "0x00010008", "0x0001000C",
        "0x00010010", "0x00010014", "0x00010018", "0x0001001C",
        "0x00010020", "0x00010024", "0x00010028", "0x0001002C",
        "0x00010030", "0x00010034", "0x00010038", "0x0001003C",
        "0x00010040", "0x00010044", "0x00010048", "0x0001004C",
        "0x00010050", "0x00010054", "0x00010058", "0x0001005C",
        "0x00010060", "0x00010064", "0x00010068", "0x0001006C",
        "0x00010070", "0x00010074", "0x00010078", "0x0001007C"
    ]
}
output = "text.txt"
filename = "testcases.txt"
with open(output, 'w') as file:
    file.write("")
def read_assembly_file(filename):
    instructions = []
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                instructions.append(line)
    
    return instructions
instruction_array = read_assembly_file(filename)
#print(instruction_array)

def decimal_to_hex(decimal_number):
    d2h= f"0x{decimal_number:08X}"
    return d2h
def printer():
    print(pc, end=" ")
    for i in range(32):
        print(" ", arr[i], end=" ")
    print()
    
    with open(output, 'a') as file:
        file.write(str(pc) + " ")
        for i in range(32):
            file.write(" " + str(arr[i]) + " ")
        file.write("\n")

def sw(imm,rs1,rs2):
    global pc
    # print(decimal_to_hex(rs1+imm))
    # print(ram_dict[decimal_to_hex(rs1+imm)])
    ram_dict[decimal_to_hex(rs1+imm)]=rs2
    # print(ram_dict[decimal_to_hex(rs1+imm)])
    pc+=4
    printer()

def bne(rs1, rs2, imm):
    global pc
    if arr[rs1] != arr[rs2]:
        pc += imm
    else:
        pc += 4
    printer()

def beq(rs1, rs2, imm):
    global pc
    if arr[rs1] == arr[rs2]:
        pc += imm
    else:
        pc += 4
    printer()

def jal(rd, imm):
    global pc 
    arr[rd] = pc + 4
    pc += imm
    printer()

def jal(rd, imm):
    global pc 
    arr[rd] = pc + 4
    pc += imm
    printer()

def add(rs1,rs2,rd):
    global pc
    arr[rd]=arr[rs1]+arr[rs2]
    pc +=4

def sub(rs1,rs2,rd):
    global pc
    arr[rd]=arr[rs1]-arr[rs2]
    pc+=4

def or1(rs1,rs2,rd):
    global pc
    r1=ibit(rs1)
    r2=ibit(rs2)
    r=""
    for i in range(0,6):
        if (r1[i]=="0" and r2[i]=="1") or (r1[i]=="1" and r2[i]=="1") or (r1[i]=="1" or r2[i]=="0"):
            r+="1"
        else:
            r+="0"
    arr[rd]=int(r,2)
    pc+=4
    printer()

def and1(rs1,rs2,rd):
    global pc
    r1=ibit(rs1)
    r2=ibit(rs2)
    r=""
    for i in range(0,6):
        if (r1[i]=="0" and r2[i]=="1") or (r1[i]=="0" and r2[i]=="0") or (r1[i]=="1" or r2[i]=="0"):
            r+="0"
        else:
            r+="1"
    arr[rd]=int(r,2)
    pc+=4
    printer()

def addi (imm,rs,rd):
    global pc
    arr[rd]=arr[rs]+imm
    pc+=4
    printer()

print("\npc", end=" ")
for i in range(32):
    if i < 10:
        print(" x", end="0" + str(i))
    else:
        print(" x", end=str(i))
print()

# Test cases
bne(0, 1, 12)
beq(0, 1, 12)
jal(30, -12)
sw(600,65000,20)

#ram output
f=""
with open(output, 'a') as file:
    for key, value in ram_dict.items():
        f=str(key)+":"+str(value)+"\n"
        file.write(f)
        print(f,end="")
