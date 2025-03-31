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

###############################
#      file input


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


#################################################
#        instructions

# def slicing(s):
#     op=s[-1:-7:-1]
#     if op=="0110011":
#         #rtype ka return kar rs2,rs1,rd
#     elif op=="0000011":
#         #lw
#     elif op=="0010011":
#         #addi
#     elif op=="1100111":
#         #jalr
#     elif op=="0100011":
#         #sw
#     elif op=="1100011":
#         #beq,bne
#     elif op=="1101111":
#         #jal
#     #return the components that each one has like registers and immediate

def sw(imm,rs1,rs2):
    global pc
    ram_dict[decimal_to_hex(rs1+imm)]=rs2
    pc+=4
    printer()

def btype(rs1,rs2,imm,c):
     global pc
    if c==1: #bne
        if arr[rs1] != arr[rs2]:
            pc += imm
        else:
            pc += 4
        printer()
    elif c==2: #beq
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

def rtype(rs1,rs2,rd,c):
    global pc
    if c==1: #add
        arr[rd]=arr[rs1]+arr[rs2]
        pc +=4
    elif c==2: #sub
        arr[rd]=arr[rs1]-arr[rs2]
        pc+=4
    elif c==3: #or
        arr[rd]=arr[rs1] | arr[rs2]
        pc+=4
        printer()
    elif c==4: #and
        arr[rd]=arr[rs1] & arr[rs2]
        pc+=4
        printer()
    elif c==5: #slt
        if arr[rs1]<arr[rs2] :     
            r=1
            arr[rd]=r
        pc+=4
        printer()
    elif c==6: #srl     
        r = arr[rs1]>>(arr[rs2]%32)
        arr[rd]=r
        pc+=4
        printer()

def addi (imm,rs,rd):
    global pc
    arr[rd]=arr[rs]+imm
    pc+=4
    printer()

#################################
#      main

print("\npc", end=" ")
for i in range(32):
    if i < 10:
        print(" x", end="0" + str(i))
    else:
        print(" x", end=str(i))
print()

# Test cases
btype(0, 1, 12,1)
btype(0, 1, 12,2)
jal(30, -12)
sw(600,65000,20)

#ram output
f=""
with open(output, 'a') as file:
    for key, value in ram_dict.items():
        f=str(key)+":"+str(value)+"\n"
        file.write(f)
        print(f,end="")
