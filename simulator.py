import sys
filename = sys.argv[1]
output = sys.argv[2]
pc=0
arr=[0]*32
arr[2]=380
ram_dict = {f"0x{addr:08X}": 0 for addr in range(0x00010000, 0x00010080, 4)}

###############################
#      File Input

def twos_complement1(n: int, bit_length: int = 32) -> str:
    return format((1 << bit_length) + n, f'0{bit_length}b')

def binconv1(n):
    if n<0:
        return twos_complement1(n)
    return format(n, '032b')

# filename = "testcases.txt" 
# output = "text.txt"

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

def decimal_to_hex(decimal_number):
    return f"0x{decimal_number:08X}"

def printer():
    with open(output, 'a') as file:
        file.write(f"0b{binconv1(pc)} ")
        for i in range(32):
            file.write(f"0b{binconv1(arr[i])} ")  
        file.write("\n")

#################################################
#        Instruction Processing

def slicing(s):
    op=s[-7:]
    try:
        if op == "0110011":  # R-type
            rd=int(s[-12:-7], 2)
            func3=s[-15:-12]
            rs1=int(s[-20:-15], 2)
            rs2=int(s[-25:-20], 2)
            func7=s[:7]

            if func3 == "000":
                if func7 == "0000000":
                    rtype(rs1, rs2, rd, 1)  # ADD
                elif func7 == "0100000":
                    rtype(rs1, rs2, rd, 2)  # SUB
            elif func3 =="010":
                rtype(rs1, rs2, rd, 5)  # SLT
            elif func3 == "101":
                rtype(rs1, rs2, rd, 6)  # SRL
            elif func3 == "110":
                rtype(rs1, rs2, rd, 3)  # OR
            elif func3 == "111":
                rtype(rs1, rs2, rd, 4)  # AND
        
        elif op == "0000011":  # LW
            rd = int(s[-12:-7], 2)
            rs1 = int(s[-20:-15], 2)
            imm = int(s[:12], 2)
            lw(rd, rs1, imm)
        
        elif op == "0010011":  # ADDI
            rd = int(s[-12:-7], 2)
            rs1 = int(s[-20:-15], 2)
            imm = int(s[:12], 2)
            addi(imm, rs1, rd)
        
        elif op=="1100111":
            rd = int(s[-8:-13:-1], 2)
            func3 = s[-13:-16:-1]
            rs1 = int(s[-16:-21:-1], 2)
            imm = int(s[-21:-33:-1], 2)
            
            jalr(rd,rs1,imm)
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
            rs1 = int(s[-16:-21:-1],2)
            rs2 = int(s[-21:-27:-1],2)
            imm2 = s[-27:-33:-1]

            imm = imm2[0] + imm1[-1] + imm2[1:] + imm1[:-1] + "0"
            final_imm = int(imm, 2)

            if func3 == "000":
                btype(rs1, rs2, final_imm,2)
            else:
                btype(rs1, rs2, final_imm,1)
        
        elif op=="1101111":
            rd = int(s[-8:-13:-1], 2)
            imm=int(s[-13:-33:-1],2)
            jal(rd,imm)
            #jal
    except Exception as e:
        print(f"Error processing instruction: {s}, Error: {e}")

# Instruction Implementations

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
#      Main Execution

ins = read_assembly_file(filename)
for i in ins:
    slicing(i)

# RAM Output
with open(output, 'a') as file:
    for key, value in ram_dict.items():
        file.write(f"{key}:0b{binconv1(value)}\n")
