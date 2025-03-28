pc = 0
arr = [0] * 32

def printer():
    print(pc, end=" ")
    for i in range(32):
        print(" ", arr[i], end=" ")
    print()

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
    if(i<10):
        print(" x",end="0"+str(i))
    else:
        print(" x",end=str(i))
print()


#checks for harshul
# arr[0]=12
# bne(0,1,12)
#beq(0, 1, 12)
#jal(30,-12)
