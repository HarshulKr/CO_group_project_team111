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
