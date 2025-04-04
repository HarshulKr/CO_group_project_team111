import sys
filename = sys.argv[1]
output = sys.argv[2]

# filename = "testcases.txt" 
# output = "text.txt"

pc=0
arr=[0]*32
arr[2]=380
label_flag=True
stack_dict = {f"0x{addr:08X}": 0 for addr in range(0x00000100, 0x00000180, 4)}
ram_dict = {f"0x{addr:08X}": 0 for addr in range(0x00010000, 0x00010080, 4)}


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
##########################################################################################
def end():  
    with open(output, 'a') as file:
        for key, value in ram_dict.items():
            file.write(f"{key}:0b{binconv1(value)}\n")
###MAIN####

ins = read_assembly_file(filename)
i=0
while(i<len(ins)):
        i=pc//4
        s=ins[i]
        op=s[-7:]
        if(op=="0110011"):
            rd=int(s[-12:-7],2)
            func3=s[-15:-12]
            rs1=int(s[-20:-15], 2)
            rs2=int(s[-25:-20], 2)
            func7=s[:7]

            if func3 == "000":
                if func7 == "0000000":
                    arr[rd]=arr[rs1]+arr[rs2]
                    pc+=4
                    printer()

                elif func7 == "0100000":
                    arr[rd]=arr[rs1]-arr[rs2]
                    pc+=4
                    printer()
            elif func3 =="110":
                arr[rd]=arr[rs1] | arr[rs2]
                pc+=4
                printer()
            elif func3 == "111":
                arr[rd]=arr[rs1] & arr[rs2]
                pc+=4
                printer()
            elif func3 == "010":
                if arr[rs1]<arr[rs2] :     
                    r=1
                    arr[rd]=r
                pc+=4
                printer()
            elif func3 == "101":
                r=arr[rs1]>>(arr[rs2]%32)
                arr[rd]=r
                pc+=4
                printer()
        
        elif(op=="0000011"):
            imm = binary_to_decimal(s[:12])
            rd = int(s[20:25], 2)
            rs1 = int(s[12:17], 2)
            address=arr[rs1]+imm 
            if(decimal_to_hex(address) in ram_dict):
                arr[rd]=ram_dict.get(decimal_to_hex(address), 0)
            else:
                arr[rd]=stack_dict.get(decimal_to_hex(address), 0)  
            pc+=4 
            printer()
            
        elif(op=="0010011"):
            imm = binary_to_decimal(s[:12])
            rd = int(s[-12:-7], 2)
            rs1 = int(s[-20:-15], 2)
            arr[rd]=arr[rs1]+imm
            pc+=4
            printer()

        elif(op=="1100111"):
            rd = int(s[20:25], 2)
            func3 = s[17:20]
            rs1 = int(s[12:17], 2)
            imm = binary_to_decimal(s[:12])
            if (rd==0):
                temp =pc 
                pc= (arr[rs1]+ (imm))
                printer()
                
            else:
                temp =pc 
                pc= (arr[rs1]+ (imm))
                i=(pc//4)-1
                arr[rd]= temp+4
                printer()
                
        elif (op=="0000001"):
            func7=s[0:7]
            if func7=="0000000":
                for j in range(0,32): #rst
                    arr[j]=0
                arr[2]=380
                pc += 4
                printer()
            
            elif func7=="1000000": #halt
                printer()
                end()
                exit(1)
            
            elif func7=="1111111":
                func3=s[17:20]
                if func3=="000":
                    rs1=int(s[12:17],2)
                    rs2=int(s[7:12],2)
                    rd=int(s[20:25],2)
                    arr[rd]=arr[rs1]*arr[rs2]
                    pc+=4
                    printer()
                else:
                    rs1=int(s[12:17],2)
                    rd=int(s[20:25],2)
                    s=binconv1(arr[rs1])
                    s1=s[::-1]
                    arr[rd]=binary_to_decimal(s1)
                    pc+=4
                    printer()
        
        elif(op=="0100011"):
            #SW
            imm1 = s[:7]            
            imm2 = (s[20:25])
            imm=imm1+imm2
            imm=binary_to_decimal(imm)
            rs2=int(s[7:12],2)
            rs1=int(s[12:17],2)
            address = arr[rs1] + imm
            if(decimal_to_hex(address) in ram_dict):
                ram_dict[decimal_to_hex(address)] = arr[rs2]  
            else:
                stack_dict[decimal_to_hex(address)] = arr[rs2]  
            pc += 4  
            printer()


        elif(op=="1100011"):
            imm1=s[20:25]
            imm2=s[0:7]
            imm12=imm2[0]
            imm5_10=imm2[6:0:-1]
            imm11=imm1[4]
            imm1_4=imm1[3:0:-1]+imm1[0]
            imm="0"+imm1_4+imm5_10+imm11+imm12
            imm=imm[::-1]
            imm = binary_to_decimal(imm)
            func3 = s[17:20]
            rs1=int(s[12:17],2)
            rs2=int(s[7:12],2)
            if(rs1==0 and rs2==0 and imm==0):
                printer()
                end()
                exit(1)
            if func3 == "000":
                if arr[rs1] == arr[rs2]:
                    pc += imm
                else:
                    pc += 4
                printer()
                if(rs1==rs2 and imm==0):
                    printer()
                    break

            elif func3=="001":
                if arr[rs1] != arr[rs2]:
                    pc += imm
                else:
                    pc += 4
                printer()

        elif(op=="1101111"):
            rd = int(s[20:25], 2)
            imm=s[0]+s[12:20]+s[11]+s[1:11]+"0"
            imm=binary_to_decimal(imm)
            arr[rd]=pc + 4
            pc=pc+imm
            printer()
            
