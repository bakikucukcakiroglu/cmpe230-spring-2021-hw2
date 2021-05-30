import sys


def splitter(programHex):
    int_value = int(programHex, base=16)
    programBin = format(int_value, '024b') 
    opBin=programBin[0:6]
    addrModeBin= programBin[6:8]
    operandBin=programBin[8:24]
    list=[opBin, addrModeBin, operandBin]
    return list

def ADD(operand1, operand2):

    integer_sum = int(operand1, 2) + int(operand2, 2) 
    print('toplanan elemanlar',int(operand1, 2), int(operand2, 2) )
    binary_sum = format(integer_sum, '017b')
    print('addition binary',binary_sum)
    result= int(binary_sum[1:17],2)

    if binary_sum[0]=='1':
        flags['CF']=1
    else:
        flags['CF']=0

    if result==0:
        flags['ZF']=1
    else: 
        flags['ZF']=0

    if binary_sum[1]=='1':
        flags['SF']=1
    else:
        flags['SF']=0

    return binary_sum[1:17]

def NOT(operand):
    print('operand',operand)
    not_operand=''
    for i in range(0,16):
        print(i)
        if operand[i]=='0':
            not_operand=not_operand+'1'
        else:
            not_operand=not_operand+'0'
    print('not_operand',not_operand)
                
    if int(not_operand, base=2) ==0:
        flags['ZF']=1
    else: 
        flags['ZF']=0

    if not_operand[0]=='1':
        flags['SF']=1
    else:
        flags['SF']=0

    return not_operand

def zf_cf_set(result):

    result_bin=format(result,'016b')
    if result ==0:
        flags['ZF']=1
    else: 
        flags['ZF']=0

    if result_bin[0]=='1':
        flags['SF']=1
    else:
        flags['SF']=0

    return result_bin



memory = ['00000000']*(2**16)
filename = sys.argv[1]
with open(filename, "r") as c_file:
    count=0
    for line in c_file:

        stripped_line=line.strip()
        memory[count]=stripped_line[0:8]
        memory[count+1]=stripped_line[8:16]
        memory[count+2]=stripped_line[16:24]
        count+=3




register_value_dict = {'PC' :'0000000000000000', 'A':'0000000000000000', 'B' :'0000000000000000', 'C':'0000000000000000', 'D':'0000000000000000', 'E':'0000000000000000', 'S':'1111111111111111'}
register_adress_dict = {'0000000000000000': 'PC', '0000000000000001':'A', '0000000000000010':'B', '0000000000000011':'C', '0000000000000100':'D', '0000000000000101':'E','0000000000000110':'S'}

flags= {'ZF': None, 'CF': None, 'SF': None}
output_file_name=sys.argv[2]
output_file= open(output_file_name, "w")
with open(filename, "r") as d_file:
    counter=0
    while int(register_value_dict['PC'],base=2) <65536:
        counter+=1
        print(counter,'registers ', register_value_dict)
        print('flags', flags)
        print('PC= ', register_value_dict['PC'])
        instruction_line=memory[int(register_value_dict['PC'],base=2)]
        list=splitter(instruction_line)
        print(list)

        if(list[0]=='000001'):    #1 HALT

            print('1')

            exit()



        if(list[0]=='000010'):     #2  LOAD
            print('2')

            if list[1]=='00':                                
                register_value_dict['A']=list[2]
            if list[1]=='01':
                register_name=register_adress_dict[list[2]]
                register_value_dict['A']=register_value_dict[register_name]
            if list[1]=='10':
                register_name=register_adress_dict[list[2]]
                register_value= register_value_dict[register_name]
                memory_address_dec= int(register_value, base=2)
                register_value_dict['A']=memory[memory_address_dec]+memory[memory_address_dec+1]
            if list[1]=='11':
                memory_address_dec= int(list[2], base=2)
                register_value_dict['A']=memory[memory_address_dec]+memory[memory_address_dec+1]
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='000011'):    #3  STORE
            print('3')

            if list[1]=='01':
                register_name=register_adress_dict[list[2]]
                register_value_dict[register_name]=register_value_dict['A']
            if list[1]=='10':
                register_name=register_adress_dict[list[2]]
                register_value= register_value_dict[register_name]
                memory_address_dec= int(register_value, base=2)
                memory[memory_address_dec]= register_value_dict['A'][0:8]
                memory[memory_address_dec+1]=register_value_dict['A'][8:16]
            if list[1]=='11':
                memory_address_dec= int(list[2], base=2)
                memory[memory_address_dec]=register_value_dict['A'][0:8]
                memory[memory_address_dec+1]=register_value_dict['A'][8:16]
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='000100'):    #4  ADD
            print('4')

            if list[1]=='00':                                
                operand=list[2]
                registerA_value=register_value_dict['A']
                register_value_dict['A']=ADD(operand, registerA_value)
            if list[1]=='01':
                register_name=register_adress_dict[list[2]]
                operand=register_value_dict[register_name]
                registerA_value=register_value_dict['A']
                register_value_dict['A']=ADD(operand, registerA_value)
            if list[1]=='10':
                register_name=register_adress_dict[list[2]]
                register_value= register_value_dict[register_name]
                memory_address_dec= int(register_value, base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                registerA_value=register_value_dict['A']
                register_value_dict['A']=ADD(operand, registerA_value)
            if list[1]=='11':
                memory_address_dec= int(list[2], base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                registerA_value=register_value_dict['A']
                register_value_dict['A']=ADD(operand, registerA_value)
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='000101'):    #5  SUB
            print('5')

            increment='0000000000000001'
            if list[1]=='00':                                
                operand=list[2]
                not_operand=NOT(operand)
                inc_not_operand=ADD(not_operand, increment)
                registerA_value=register_value_dict['A']
                register_value_dict['A']=ADD(inc_not_operand, registerA_value)

            if list[1]=='01':
                register_name=register_adress_dict[list[2]]
                operand=register_value_dict[register_name]
                not_operand=NOT(operand)
                inc_not_operand=ADD(not_operand, increment)
                registerA_value=register_value_dict['A']
                register_value_dict['A']=ADD(inc_not_operand, registerA_value)

            if list[1]=='10':
                register_name=register_adress_dict[list[2]]
                register_value= register_value_dict[register_name]
                memory_address_dec= int(register_value, base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                not_operand=NOT(operand)
                inc_not_operand=ADD(not_operand, increment)
                registerA_value=register_value_dict['A']
                register_value_dict['A']=ADD(inc_not_operand, registerA_value)

            if list[1]=='11':
                memory_address_dec= int(list[2], base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                not_operand=NOT(operand)
                inc_not_operand=ADD(not_operand, increment)
                registerA_value=register_value_dict['A']
                register_value_dict['A']=ADD(inc_not_operand, registerA_value)
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='000110'):    #6  INC
            print('6')
            print(int(register_value_dict['PC'],2))

            increment='0000000000000001'
            if list[1]=='00':                                
                operand=list[2]
                ADD(operand, registerA_value)

            if list[1]=='01':
                register_name=register_adress_dict[list[2]]
                operand=register_value_dict[register_name]
                register_value_dict[register_name]=ADD(operand, increment)

            if list[1]=='10':
                register_name=register_adress_dict[list[2]]
                register_value= register_value_dict[register_name]
                memory_address_dec= int(register_value, base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                memory[memory_address_dec]= ADD(operand, increment)[0:8]
                memory[memory_address_dec+1]=ADD(operand, increment)[8:16]

            if list[1]=='11':
                memory_address_dec= int(list[2], base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                memory[memory_address_dec]= ADD(operand,increment)[0:8]
                memory[memory_address_dec+1]=ADD(operand, increment)[8:16]
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='000111'):    #7  DEC
            print('7')

            decrement='1111111111111111'   
            if list[1]=='00':                                
                operand=list[2]
                print('decrementten önce1', operand)
                ADD(operand, decrement)
                print('decrementten sonra1')

            if list[1]=='01':
                register_name=register_adress_dict[list[2]]
                operand=register_value_dict[register_name]
                print('decrementten önce2', operand)
                register_value_dict[register_name]=ADD(operand, decrement)
                print('decrementten sonra2',register_value_dict[register_name])

            if list[1]=='10':
                register_name=register_adress_dict[list[2]]
                register_value= register_value_dict[register_name]
                memory_address_dec= int(register_value, base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                print('decrementten önce3', operand)
                memory[memory_address_dec]= ADD(operand, decrement)[0:8]
                memory[memory_address_dec+1]=ADD(operand, decrement)[8:16]

            if list[1]=='11':
                memory_address_dec= int(list[2], base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                print('decrementten önce4', operand)
                memory[memory_address_dec]= ADD(operand,increment)[0:8]
                memory[memory_address_dec+1]=ADD(operand, increment)[8:16]
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='001000'):    #8  XOR
            print('8')

            if list[1]=='00':                                
                operand=list[2]

                registerA_value=register_value_dict['A']
                print('xor', operand, register_value_dict['A'] )
                operand_dec=int(operand, base=2)
                registerA_value_dec= int(registerA_value, base=2)
                register_value_dict['A']=zf_cf_set(operand_dec ^ registerA_value_dec)
                print('xor result', register_value_dict['A'])

            if list[1]=='01':
                register_name=register_adress_dict[list[2]]
                operand=register_value_dict[register_name]
                registerA_value=register_value_dict['A']
                operand_dec=int(operand, base=2)
                registerA_value_dec= int(registerA_value, base=2)
                register_value_dict['A']=zf_cf_set(operand_dec^ registerA_value_dec)

            if list[1]=='10':
                register_name=register_adress_dict[list[2]]
                register_value= register_value_dict[register_name]
                memory_address_dec= int(register_value, base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                registerA_value=register_value_dict['A']
                operand_dec=int(operand, base=2)
                registerA_value_dec= int(registerA_value, base=2)
                register_value_dict['A']=zf_cf_set(operand_dec ^ registerA_value_dec)

            if list[1]=='11':
                memory_address_dec= int(list[2], base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                registerA_value=register_value_dict['A']
                operand_dec=int(operand, base=2)
                registerA_value_dec= int(registerA_value, base=2)
                register_value_dict['A']=zf_cf_set(operand_dec ^ registerA_value_dec)
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')




        if(list[0]=='001001'):    #9  AND
            print('9')

            if list[1]=='00':                                
                operand=list[2]
                registerA_value=register_value_dict['A']
                operand_dec=int(operand, base=2)
                registerA_value_dec= int(registerA_value, base=2)
                register_value_dict['A']=zf_cf_set(operand_dec & registerA_value_dec)

            if list[1]=='01':
                register_name=register_adress_dict[list[2]]
                operand=register_value_dict[register_name]
                registerA_value=register_value_dict['A']
                operand_dec=int(operand, base=2)
                registerA_value_dec= int(registerA_value, base=2)
                register_value_dict['A']=zf_cf_set(operand_dec & registerA_value_dec)

            if list[1]=='10':
                register_name=register_adress_dict[list[2]]
                register_value= register_value_dict[register_name]
                memory_address_dec= int(register_value, base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                registerA_value=register_value_dict['A']
                operand_dec=int(operand, base=2)
                registerA_value_dec= int(registerA_value, base=2)
                register_value_dict['A']=zf_cf_set(operand_dec& registerA_value_dec)

            if list[1]=='11':
                memory_address_dec= int(list[2], base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                registerA_value=register_value_dict['A']
                operand_dec=int(operand, base=2)
                registerA_value_dec= int(registerA_value, base=2)
                register_value_dict['A']=zf_cf_set(operand_dec& registerA_value_dec)
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='001010'):    #10 OR
            print('10')

            if list[1]=='00':                                
                operand=list[2]
                registerA_value=register_value_dict['A']
                operand_dec=int(operand, base=2)
                registerA_value_dec= int(registerA_value, base=2)
                register_value_dict['A']=zf_cf_set(operand_dec | registerA_value_dec)

            if list[1]=='01':
                register_name=register_adress_dict[list[2]]
                operand=register_value_dict[register_name]
                registerA_value=register_value_dict['A']
                operand_dec=int(operand, base=2)
                registerA_value_dec= int(registerA_value, base=2)
                register_value_dict['A']=zf_cf_set(operand_dec| registerA_value_dec)

            if list[1]=='10':
                register_name=register_adress_dict[list[2]]
                register_value= register_value_dict[register_name]
                memory_address_dec= int(register_value, base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                registerA_value=register_value_dict['A']
                operand_dec=int(operand, base=2)
                registerA_value_dec= int(registerA_value, base=2)
                register_value_dict['A']=zf_cf_set(operand_dec | registerA_value_dec)

            if list[1]=='11':
                memory_address_dec= int(list[2], base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                registerA_value=register_value_dict['A']
                operand_dec=int(operand, base=2)
                registerA_value_dec= int(registerA_value, base=2)
                register_value_dict['A']=zf_cf_set(operand_dec | registerA_value_dec)
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='001011'):    #11 NOT
            print('11')

            if list[1]=='00':                                
                operand=list[2]
                NOT(operand)

            if list[1]=='01':
                register_name=register_adress_dict[list[2]]
                operand=register_value_dict[register_name]
                register_value_dict[register_name]= NOT(operand)

            if list[1]=='10':
                register_name=register_adress_dict[list[2]]
                register_value= register_value_dict[register_name]
                memory_address_dec= int(register_value, base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                memory[memory_address_dec]= NOT(operand)[0:8]
                memory[memory_address_dec+1]=NOT(operand)[8:16]

            if list[1]=='11':
                memory_address_dec= int(list[2], base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                memory[memory_address_dec]= NOT(operand)[0:8]
                memory[memory_address_dec+1]=NOT(operand)[8:16]
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='001100'):    #12 SHL
            print('12')

            register_name=register_adress_dict[list[2]]
            operand=register_value_dict[register_name]
            shifted_operand=operand+'0'
            shifted_int=int(shifted_operand, base=2)
            register_value_dict[register_name]=shifted_operand[1:17]
            print('shl i-o', operand, register_value_dict[register_name])
            result= int(shifted_operand[1:17], base=2)


            if shifted_operand[0]=='1':
                flags['CF']=1
            else:
                flags['CF']=0

            if result==0:
                flags['ZF']=1
            else: 
                flags['ZF']=0

            if shifted_operand[1]=='1':
                flags['SF']=1
            else:
                flags['SF']=0
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='001101'):    #13 SHR
            print('13')

            register_name=register_adress_dict[list[2]]
            operand=register_value_dict[register_name]
            shifted_int=int(operand, base=2)/2 #nasıl bölme int mi double mi
            register_value_dict[register_name]=format(int(shifted_int), '016b')

            if shifted_int==0:
                flags['ZF']=1
            else: 
                flags['ZF']=0

            flags['SF']=0
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')

    

        if(list[0]=='001110'):    #14 NOP
            print('14')
            print('nop öncesi',int(register_value_dict['PC'] ,2))

            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')
            print('nop sonrası',int(register_value_dict['PC'] ,2))




        if(list[0]=='001111'):    #15 PUSH
            print('15')

            register_name=register_adress_dict[list[2]]
            operand=register_value_dict[register_name]
            index= int(register_value_dict['S'],base=2)
            memory[index-1]=operand[0:8]
            memory[index]=operand[8:16]

            register_value_dict['S']=format(index-2, '016b')
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')




        if(list[0]=='010000'):    #16 POP
            print('16')

            register_name=register_adress_dict[list[2]]
            index= int(register_value_dict['S'], base=2)
            print(index)
            if(index<=65534):#!!!!!!!!!!!!
                register_value_dict[register_name]=memory[index+1]+memory[index+2]
                register_value_dict['S']=format(index+2, '016b')
                
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')
        





        if(list[0]=='010001'):    #17 CMP
            print('17')

            increment='0000000000000001'
            if list[1]=='00':                                
                operand=list[2]
                not_operand=NOT(operand)
                inc_not_operand=ADD(not_operand, increment)
                registerA_value=register_value_dict['A']
                ADD(inc_not_operand, registerA_value)

            if list[1]=='01':
                register_name=register_adress_dict[list[2]]
                operand=register_value_dict[register_name]
                print('nota giren operand',operand)
                not_operand=NOT(operand)
                inc_not_operand=ADD(not_operand, increment)
                registerA_value=register_value_dict['A']
                print('regA', register_value_dict['A'], 'operand', operand)
                ADD(inc_not_operand, registerA_value)

                # register_name=register_adress_dict[list[2]]
                # operand=register_value_dict[register_name]
                # not_operand=NOT(operand)
                # inc_not_operand=ADD(not_operand, increment)
                # registerA_value=register_value_dict['A']
                # register_value_dict['A']=ADD(inc_not_operand, registerA_value)
            if list[1]=='10':
                register_name=register_adress_dict[list[2]]
                register_value= register_value_dict[register_name]
                memory_address_dec= int(register_value, base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                not_operand=NOT(operand)
                inc_not_operand=ADD(not_operand, increment)
                registerA_value=register_value_dict['A']
                ADD(inc_not_operand, registerA_value)
            if list[1]=='11':
                memory_address_dec= int(list[2], base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                not_operand=NOT(operand)
                inc_not_operand=ADD(not_operand, increment)
                registerA_value=register_value_dict['A']
                ADD(inc_not_operand, registerA_value)
            
            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='010010'):    #18 JMP
            print('18')

            register_value_dict['PC']=list[2]

        

        if(list[0]=='010011'):    #19 JZ-JE
            print('19')


            if(flags['ZF']==1):
                register_value_dict['PC']=list[2]
            else:
                #print('jz öncesi',int(register_value_dict['PC'] ,2))
                register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')
                #print('jz sonrası', int(register_value_dict['PC'],2))



        if(list[0]=='010100'):    #20    JNZ-JNE
            print('20')

            if(flags['ZF']==0):
                print('pc değişti')
                print(list[2])
                register_value_dict['PC']=list[2]
                print(register_value_dict['PC'])
            else:
                register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='010101'):    #21 JC
            print('21')

            if(flags['CF']==1):
                register_value_dict['PC']=list[2]
            else:
                register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='010110'):    #22 JNC
            print('22')

            if(flags['CF']==0):
                register_value_dict['PC']=list[2]
            else:
                register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='010111'):    #23 JA
            print('23')

            if(flags['SF']==0):
                register_value_dict['PC']=list[2]
            else:
                register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')
        


        if(list[0]=='011000'):    #24 JAE
            print('24')

            if((flags['SF']==0) or flags['ZF']==1):
                register_value_dict['PC']=list[2]
            else:
                register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='011001'):    #25 JB
            print('25')

            if(flags['SF']==1):
                register_value_dict['PC']=list[2]
            else:
                register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='011010'):    #26 JBE
            print('26')

            if(flags['SF']==1 or flags['ZF']==1):
                register_value_dict['PC']=list[2]
            else:
                register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='011011'):    #27 READ
            print('27')

            operand= input('Type a character')
            asci_operand= ord(operand)
            operand_binary=format(asci_operand, '016b')
            
            if list[1]=='01':
                register_name=register_adress_dict[list[2]]
                register_value_dict[register_name]=operand_binary
                
            if list[1]=='10':
                register_name=register_adress_dict[list[2]]
                register_value= register_value_dict[register_name]
                memory_address_dec= int(register_value, base=2)
                memory[memory_address_dec]=operand_binary[0:8]
                memory[memory_address_dec+1]=operand_binary[8:16]

            if list[1]=='11':
                memory_address_dec= int(list[2], base=2)
                memory[memory_address_dec]=operand_binary[0:8]
                memory[memory_address_dec+1]=operand_binary[8:16]

            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')



        if(list[0]=='011100'):    #28 PRİNT
            print('28')

            if list[1]=='00':                                
                operand=list[2]
                ascii_char=int(operand, base=2)
                print(chr(ascii_char))
                output_file.write(chr(ascii_char))

            if list[1]=='01':
                register_name=register_adress_dict[list[2]]
                operand=register_value_dict[register_name]
                ascii_char=int(operand, base=2)
                print(chr(ascii_char))
                output_file.write(chr(ascii_char))

            if list[1]=='10':
                register_name=register_adress_dict[list[2]]
                register_value= register_value_dict[register_name]
                memory_address_dec= int(register_value, base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                ascii_char=int(operand, base=2)
                output_file.write(chr(ascii_char))

                
            if list[1]=='11':
                memory_address_dec= int(list[2], base=2)
                operand=memory[memory_address_dec]+memory[memory_address_dec+1]
                ascii_char=int(operand, base=2)
                output_file.write(chr(ascii_char))

            register_value_dict['PC']=format(int(register_value_dict['PC'],2)+3, '016b')










