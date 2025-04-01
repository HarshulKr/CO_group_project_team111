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

def slicing(s):
    op=s[-1:-8:-1]
    if op=="0110011":
        rd = int(s[-8:-13:-1], 2)
        func3 = s[-13:-16:-1]
        rs1 = int(s[-16:-21:-1], 2)
        rs2 = int(s[-21:-27:-1], 2)
        func7 = s[-27:-33:-1]

        if(func3=="000"):
            if(func7=="0000000"):#add
                rtype(rs1,rs2,rd,1)
            elif(func7=="0100000"):#sub
                rtype(rs1,rs2,rd,2)
        elif(func3=="010"):#slt
                rtype(rs1,rs2,rd,5)
        elif(func3=="101"):#srl
                rtype(rs1,rs2,rd,6)
        elif(func3=="110"):#or
                rtype(rs1,rs2,rd,3)
        elif(func3=="111"):#and
                rtype(rs1,rs2,rd,4)
        
        #rtype ka return kar rs2,rs1,rd
    elif op=="0000011":
        #lw
        rd = int(s[-8:-13:-1], 2)
        func3 = s[-13:-16:-1]
        rs1 = int(s[-16:-21:-1], 2)
        imm = int(s[-21:-33:-1], 2)
        lw(rs1,rd,imm)
        
    elif op=="0010011":
        rd = int(s[-8:-13:-1], 2)
        func3 = s[-13:-16:-1]
        rs1 = int(s[-16:-21:-1], 2)
        imm = int(s[-21:-33:-1], 2)
        addi(imm,rs1,rd)



        #addi
    elif op=="1100111":
        rd = int(s[-8:-13:-1], 2)
        func3 = s[-13:-16:-1]
        rs1 = int(s[-16:-21:-1], 2)
        imm = int(s[-21:-33:-1], 2)
        
        jalr(rd,imm)
        #jalr
    elif op=="0100011":
        imm1 = int(s[-8:-13:-1], 2)
        func3 = s[-13:-16:-1]
        rs1 = int(s[-16:-21:-1], 2)
        rs2 = int(s[-21:-27:-1], 2)
        imm2 = int(s[-27:-33:-1], 2)
        final = (imm2 << 5) | imm1
        sw(final,rs1,rs2)

        #sw
    elif op == "1100011":
        imm1 = s[-8:-13:-1]
        func3 = s[-13:-16:-1]
        rs1 = s[-16:-21:-1]
        rs2 = s[-21:-27:-1]
        imm2 = s[-27:-33:-1]

        imm = imm2[0] + imm1[-1] + imm2[1:] + imm1[:-1] + "0"
        final_imm = int(imm, 2)

        if func3 == "000":
            btype(rs1, rs2, final_imm)
        else:
            btype(rs1, rs2, final_imm)


    elif op=="1101111":
        rd = int(s[-8:-13:-1], 2)
        imm=int(s[-13:-33:-1],2)

        jal(rd,imm)
        #jal
    #return the components that each one has like registers and immediate


def sw(rs2, rs1, imm):
    global pc
    address=arr[rs1] + imm  
    ram_dict[decimal_to_hex(address)]=arr[rs2]  
    pc += 4  
    printer()


def lw(rd, rs1, imm):
    global pc
    address=arr[rs1]+imm 
    arr[rd]=ram_dict.get(decimal_to_hex(address), 0)  # Load the word
    pc+=4  
    printer()

def jalr(rd, rs1, imm):
    global pc
    temp=pc+4
    pc=(arr[rs1]+imm) & ~1
    arr[rd]=temp
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
    arr[rd]=pc + 4
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
        r=arr[rs1]>>(arr[rs2]%32)
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
