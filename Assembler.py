reg={'zero':'x0','ra':'x1','sp':'x2','gp':'x3','tp':'x4','t0':'x5','t1':'x6','t2':'x7','s0':'x8','fp':'x8','s1':'x9','a0':'x10',
'a1':'x11','a2':'x12','a3':'x13','a4':'x14','a5':'x15','a6':'x16','a7':'x17','s2':'x18','s3':'x19','s4':'x20','s5':'x21','s6':'x22','s7':'x23',
's8':'x24','s9':'x25','s10':'x26','s11':'x27','t3':'x28','t4':'x29','t5':'x30','t6':'x31'}

regad={'x0':'00000','x1':'00001','x2':'00010','x3':'00011','x4':'00100','x5':'00101','x6':'00110','x7':'00111','x8':'01000','x9':'01001','x10':'01010',
'x11':'01011','x12':'01100','x13':'01101','x14':'01110','x15':'01111','x16':'10000','x17':'10001','x18':'10010','x19':'10011','x20':'10100','x21':'10101','x22':'10110','x23':'10111',
'x24':'11000','x25':'11001','x26':'11010','x27':'11011','x28':'11100','x29':'11101','x30':'11110','x31':'11111'}


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
