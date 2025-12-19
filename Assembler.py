reg={'zero':'x0','ra':'x1','sp':'x2','gp':'x3','tp':'x4','t0':'x5','t1':'x6','t2':'x7','s0':'x8','fp':'x8','s1':'x9','a0':'x10',
'a1':'x11','a2':'x12','a3':'x13','a4':'x14','a5':'x15','a6':'x16','a7':'x17','s2':'x18','s3':'x19','s4':'x20','s5':'x21','s6':'x22','s7':'x23',
's8':'x24','s9':'x25','s10':'x26','s11':'x27','t3':'x28','t4':'x29','t5':'x30','t6':'x31'}

regad={'x0':'00000','x1':'00001','x2':'00010','x3':'00011','x4':'00100','x5':'00101','x6':'00110','x7':'00111','x8':'01000','x9':'01001','x10':'01010',
'x11':'01011','x12':'01100','x13':'01101','x14':'01110','x15':'01111','x16':'10000','x17':'10001','x18':'10010','x19':'10011','x20':'10100','x21':'10101','x22':'10110','x23':'10111',
'x24':'11000','x25':'11001','x26':'11010','x27':'11011','x28':'11100','x29':'11101','x30':'11110','x31':'11111'}
import sys
if len(sys.argv) >= 3:
    filename = sys.argv[1]
    output = sys.argv[2]
else:
    filename="input.txt"
    output="output.txt"
#import sys
#filename = sys.argv[1]
#output = sys.argv[2]

# filename = "testcases.txt"
# output = "text.txt"

arr_labels={}
k=0

def twos_complement2(n: int, bit_length: int = 21) -> str:
    return format((1 << bit_length) + n, f'0{bit_length}b')
def binconv2(n):
        if(n<0):
            return twos_complement2(n)
        return format(n,'021b')
def twos_complement1(n: int, bit_length: int = 13) -> str:
    return format((1 << bit_length) + n, f'0{bit_length}b')
def binconv1(n):
        if(n<0):
            return twos_complement1(n)
        return format(n,'013b')
def twos_complement3(n: int, bit_length: int = 12) -> str:
    return format((1 << bit_length) + n, f'0{bit_length}b')
def binconv3(n):
        if(n<0):
            return twos_complement3(n)
        return format(n,'012b')
def stype(l1,index):
    opcode="0100011"
    f3="010"
    l2=l1[1].split(",")
    rs2=regad[reg[l2[0]]]
    l3=(l2[1]).split("(")
    rs1=regad[reg[l3[1][0:2]]]

    if l1[0]!="sw" or (reg[l2[0]] not in regad) or (reg[l3[1][0:2]] not in regad):
        print("Error on line",+str(index))
        return
    
    imm=binconv3(int(l3[0]))
    f=imm[0:7]+rs2+rs1+f3+imm[7:12]+opcode
    return f

def rtype(l1,rtypeins,index):
    ins=l1[0]
    l2=l1[1].split(",")
    if len(l2)!=3:
        print("Error on line"+str(index))
        return
    rs2=reg[l2[2]]
    rs1=reg[l2[1]]
    rd=reg[l2[0]]
    if (ins not in  rtypeins) or (rs1 not in regad) or (rs2 not in regad) or (rd not in regad):
        print("Error on line"+str(index))
        return
    
    funct3='000'
    funct7='0000000'

    if ins == 'add':
        funct3 = '000'
        funct7 = '0000000' 
    elif ins == 'sub':
        funct3 = '000'
        funct7 = '0100000' 
    elif ins == 'slt':
        funct3 = '010'
        funct7 = '0000000'  
    elif ins == 'srl':
        funct3 = '101'
        funct7 = '0000000'  
    elif ins == 'or':
        funct3 = '110'
        funct7 = '0000000'  
    elif ins == 'and':
        funct3 = '111'
        funct7 = '0000000' 
   
    opcode = '0110011'  
    bi = funct7 + regad[rs2] + regad[rs1] + funct3 + regad[rd] + opcode
    
    return bi

def itype(l1, index):
    func = l1[0]
    temp = l1[1].split(",")
    
    opcode = {"lw": "0000011", "addi": "0010011", "jalr": "1100111"}
    funct3 = {"lw": "010", "addi": "000", "jalr": "000"}
    
    if func == "lw":
        if len(temp) != 2:
            print("Error on line", index)
            return None
            
        load = temp[0]
        offset, r1 = temp[1].split("(")
        r1 = r1.replace(")", "")

        if load in reg:
            load = reg[load]
        if r1 in reg:
            r1 = reg[r1]

        if load not in regad or r1 not in regad:
            print("Error on line", index)
            return None

        imm_bin = binconv3(int(offset))
        rd_bin = regad[load]
        rs1_bin = regad[r1]
        func3_bin = funct3["lw"]
        opcode_bin = opcode["lw"]
        f = imm_bin + rs1_bin + func3_bin + rd_bin + opcode_bin
        return f

    elif func == "addi":
        if len(temp) != 3:
            print("Error on line", index)
            return None

        rd, rs1, imm = temp

        if rd in reg:
            rd = reg[rd]
        if rs1 in reg:
            rs1 = reg[rs1]

        if rd not in regad or rs1 not in regad:
            print("Error on line", index)
            return None

        imm_bin = binconv3(int(imm))
        rd_bin = regad[rd]
        rs1_bin = regad[rs1]
        func3_bin = funct3["addi"]
        opcode_bin = opcode["addi"]

        f = imm_bin + rs1_bin + func3_bin + rd_bin + opcode_bin
        return f

    elif func == "jalr":
        if len(temp) != 3:
            print("Error on line", index)
            return None

        rd, rs1, imm = temp

        if rd in reg:
            rd = reg[rd]
        if rs1 in reg:
            rs1 = reg[rs1]

        if rd not in regad or rs1 not in regad:
            print("Error on line", index)
            return None

        imm_bin = binconv3(int(imm))
        rd_bin = regad[rd]
        rs1_bin = regad[rs1]
        func3_bin = funct3["jalr"]
        opcode_bin = opcode["jalr"]

        f = imm_bin + rs1_bin + func3_bin + rd_bin + opcode_bin
        return f
def btype(st1,st2,st3,labels,index):
    if(st1=='beq'):
        if(labels.isdigit() or "-" in labels):
            n=binconv1(int(labels))
            imm=str(n)
            imm1=imm[0]+imm[2:8]
            imm2=imm[8:12]+imm[1]
            if (reg[st2] not in regad) or (reg[st3] not in regad):
                print("Error on line"+str(index))
                return
            rs1=regad[reg[st2]]
            rs2=regad[reg[st3]]
            ansB=imm1+rs2+rs1+"000"+imm2+"1100011"
            return(ansB)
        elif(labels in arr_labels):
            n=binconv1(int((arr_labels[labels])-k)*4)
            imm=str(n)
            imm1=imm[0]+imm[2:8]
            imm2=imm[8:12]+imm[1]
            if (reg[st2] not in regad) or (reg[st3] not in regad):
                print("Error on line"+str(index))
                return
            rs1=regad[reg[st2]]
            rs2=regad[reg[st3]]
            ansB=imm1+rs2+rs1+"000"+imm2+"1100011"
            return(ansB)
    elif(st1=='bne'):
         if(labels.isdigit() or "-" in labels):
            n=binconv1(int(labels))
            imm=str(n)
            imm1=imm[0]+imm[2:8]
            imm2=imm[8:12]+imm[1]
            if (reg[st2] not in regad) or (reg[st3] not in regad):
                print("Error on line"+str(index))
                return
            rs1=regad[reg[st2]]
            rs2=regad[reg[st3]]
            ansB=imm1+rs2+rs1+"001"+imm2+"1100011"
            return(ansB)
         elif(labels in arr_labels):
            n=binconv1((arr_labels[labels]-k)*4)
            imm=str(n)
            imm1=imm[0]+imm[2:8]
            imm2=imm[8:12]+imm[1]
            if (reg[st2] not in regad) or (reg[st3] not in regad):
                print("Error on line"+str(index))
                return
            rs1=regad[reg[st2]]
            rs2=regad[reg[st3]]
            ansB=imm1+rs2+rs1+"001"+imm2+"1100011"
            return(ansB)


def jtype(st1,labels,index):
     rd=regad[reg[st1]]
     if (reg[st1] not in regad):
        print("Error on line"+str(index))
        return
     if(labels.isdigit() or "-" in labels):
            n=binconv2(int(labels))
            imm=str(n)
            ansJ=imm[0]+imm[10:20]+imm[9]+imm[1:9]
            return(ansJ+""+rd+""+"1101111")
     elif(labels in arr_labels):
        n=binconv2((arr_labels[labels]-k)*4)
        imm=str(n)
        ansJ=imm[0]+imm[10:20]+imm[9]+imm[1:9]
        return (ansJ+""+rd+""+"1101111")

def read_assembly_file(filename):
    instructions = []
    
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                instructions.append(line)
    
    return instructions
instruction_array = read_assembly_file(filename)

j=1
jjj=0
for i in instruction_array:
    for lop in range(0,len(i)):
        if(i[lop]==':' and i[lop+1]!=" "):
            instruction_array[jjj]=i[0:lop+1]+" "+i[lop+1:len(i)]
            i=i[0:lop+1]+" "+i[lop+1:len(i)]
    parts = i.replace(',', ' ').split()
    if(':' in parts[0]):
         parts0=parts[0]
         arr_labels[parts0[:-1]]=j
    j+=1
    jjj+=1
k=1
with open(output, 'w') as file:
    for i in instruction_array:
        parts = i.replace(',', ' ').split()
        rtypeins=['add','sub','slt','srl','or','and']
        itypeins=['lw','addi','jalr']
        stypeins=['sw']
        btype_ins=['beq','bne']
        jtype_ins=['jal']
        l1=i.split()
        f=""
        if(parts[0] in btype_ins):
            f=btype(parts[0],parts[1],parts[2],parts[3],k)
        elif(parts[0] in jtype_ins):
            f=jtype(parts[1],parts[2],k)
        elif (parts[0] in rtypeins):
            f=rtype(l1,rtypeins,k)
        elif (parts[0] in itypeins):
            f=itype(l1,k)
        elif (parts[0] in stypeins):
            f=stype(l1,k)
        elif(':' in parts[0]):
            if(parts[1] in btype_ins):
                f=btype(parts[1],parts[2],parts[3],parts[4],k)
            elif(parts[1] in jtype_ins):
                f=jtype(parts[2],parts[3],k)
            elif (parts[1] in rtypeins):
                l1=l1[1:3]
                f=rtype(l1,rtypeins,k)
            elif (parts[1] in stypeins):
                l1=l1[1:3]
                f=stype(l1,k)
            elif (parts[1] in itypeins):
                l1=l1[1:3]
                f=itype(l1,k)
        else:
            print("The instruction name is not correct")   
        if f is not None:
                file.write(f+"\n")
        k+=1

