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

	integer_sum = int(operand1, 2) + int(operand, 2) 
	binary_sum = format(integer_sum, '017b')
	result= int(binary_sum[1:17],2)

	if binary_sum[0]==1:
		flags['CF']=1
	else:
		flags['CF']=0

	if result=0:
		flags['ZF']=1
	else: 
		flags['ZF']=0

	if binary_sum[1]==1:
		flags['SF']=1
	else:
		flags['SF']=0

	return binary_sum[1:17]

def NOT(operand):
				
	if int(~operand, base=2) ==0:
		flags['ZF']=1
	else: 
		flags['ZF']=0

	if ~operand[0]==1:
		flags['SF']=1
	else:
		flags['SF']=0

	return ~operand

def zf_cf_set(result):
	if int(result, base=2) ==0:
		flags['ZF']=1
	else: 
		flags['ZF']=0

	if result[0]==1:
		flags['SF']=1
	else:
		flags['SF']=0

	return result






memory = [None]*(2**16)


register_value_dict = {'PC' :'0000', 'A':'0000', 'B' :'0000', 'C':'0000', 'D':'0000', 'E':'0000', 'S':'0000'}
register_adress_dict = {'0000000000000000': 'PC', '0000000000000001':'A', '0000000000000010':'B', '0000000000000011':'C', '0000000000000100':'D', '0000000000000101':'E','0000000000000110':'S'}

flags= {'ZF':'', 'CF':'', 'SF':''}


with open("prog.txt", "r") as c_file:

	for line in c_file:
		stripped_line=line.strip()
		list=splitter(stripped_line)

		if(list[0]=='000001'):	#1 HALT

			exit()



		if(list[0]=='000010'): 	#2  LOAD
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



		if(list[0]=='000011'):	#3  STORE
			if list[1]=='01':
				register_name=register_adress_dict[list[2]]
				register_value_dict[register_name]=register_value_dict['A']
			if list[1]=='10':
				register_name=register_adress_dict[list[2]]
				register_value= register_value_dict[register_name]
				memory_address_dec= int(register_value, base=2)
				memory[memory_address_dec]= register_value_dict['A'][:8]
				memory[memory_address_dec+1]=register_value_dict['A'][8:16]
			if list[1]=='11':
				memory_address_dec= int(list[2], base=2)
				memory[memory_address_dec]=register_value_dict['A'][0:8]
				memory[memory_address_dec+1]=register_value_dict['A'][8:16]



		if(list[0]=='000100'):	#4  ADD
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



		if(list[0]=='000101'):	#5  SUB
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



		if(list[0]=='000110'):	#6  INC
			increment='0000000000000001'
			if list[1]=='00':								
				operand=list[2]
				ADD(operand, registerA_value)

			if list[1]=='01':
				register_name=register_adress_dict[list[2]]
				operand=register_value_dict[register_name]
				register_value_dict[register_name]=ADD(operand, increment)[1:17]

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


		if(list[0]=='000111'):	#7  DEC
			decrement='1111111111111111'
			if list[1]=='00':								
				operand=list[2]
				ADD(operand, decrement)

			if list[1]=='01':
				register_name=register_adress_dict[list[2]]
				operand=register_value_dict[register_name]
				registerA_value=register_value_dict['A']
				register_value_dict[register_name]=ADD(operand, decrement)[1:17]

			if list[1]=='10':
				register_name=register_adress_dict[list[2]]
				register_value= register_value_dict[register_name]
				memory_address_dec= int(register_value, base=2)
				operand=memory[memory_address_dec]+memory[memory_address_dec+1]
				memory[memory_address_dec]= ADD(operand, decrement)[0:8]
				memory[memory_address_dec+1]=ADD(operand, decrement)[8:16]

			if list[1]=='11':
				memory_address_dec= int(list[2], base=2)
				operand=memory[memory_address_dec]+memory[memory_address_dec+1]
				memory[memory_address_dec]= ADD(operand,increment)[0:8]
				memory[memory_address_dec+1]=ADD(operand, increment)[8:16]


		if(list[0]=='001000'):	#8  XOR
			if list[1]=='00':								
				operand=list[2]
				registerA_value=register_value_dict['A']
				register_value_dict['A']=zf_cf_set(operand ^ registerA_value)

			if list[1]=='01':
				register_name=register_adress_dict[list[2]]
				operand=register_value_dict[register_name]
				registerA_value=register_value_dict['A']
				register_value_dict['A']=zf_cf_set(operand ^ registerA_value)

			if list[1]=='10':
				register_name=register_adress_dict[list[2]]
				register_value= register_value_dict[register_name]
				memory_address_dec= int(register_value, base=2)
				operand=memory[memory_address_dec]+memory[memory_address_dec+1]
				registerA_value=register_value_dict['A']
				register_value_dict['A']=zf_cf_set(operand ^ registerA_value)

			if list[1]=='11':
				memory_address_dec= int(list[2], base=2)
				operand=memory[memory_address_dec]+memory[memory_address_dec+1]
				registerA_value=register_value_dict['A']
				register_value_dict['A']=zf_cf_set(operand ^ registerA_value)



		if(list[0]=='001001'):	#9  AND

			if list[1]=='00':								
				operand=list[2]
				registerA_value=register_value_dict['A']
				register_value_dict['A']=zf_cf_set(operand & registerA_value)

			if list[1]=='01':
				register_name=register_adress_dict[list[2]]
				operand=register_value_dict[register_name]
				registerA_value=register_value_dict['A']
				register_value_dict['A']=zf_cf_set(operand & registerA_value)

			if list[1]=='10':
				register_name=register_adress_dict[list[2]]
				register_value= register_value_dict[register_name]
				memory_address_dec= int(register_value, base=2)
				operand=memory[memory_address_dec]+memory[memory_address_dec+1]
				registerA_value=register_value_dict['A']
				register_value_dict['A']=zf_cf_set(operand & registerA_value)

			if list[1]=='11':
				memory_address_dec= int(list[2], base=2)
				operand=memory[memory_address_dec]+memory[memory_address_dec+1]
				registerA_value=register_value_dict['A']
				register_value_dict['A']=zf_cf_set(operand & registerA_value)



		if(list[0]=='001010'):	#10 OR

			if list[1]=='00':								
				operand=list[2]
				registerA_value=register_value_dict['A']
				register_value_dict['A']=zf_cf_set(operand | registerA_value)

			if list[1]=='01':
				register_name=register_adress_dict[list[2]]
				operand=register_value_dict[register_name]
				registerA_value=register_value_dict['A']
				register_value_dict['A']=zf_cf_set(operand | registerA_value)

			if list[1]=='10':
				register_name=register_adress_dict[list[2]]
				register_value= register_value_dict[register_name]
				memory_address_dec= int(register_value, base=2)
				operand=memory[memory_address_dec]+memory[memory_address_dec+1]
				registerA_value=register_value_dict['A']
				register_value_dict['A']=zf_cf_set(operand | registerA_value)

			if list[1]=='11':
				memory_address_dec= int(list[2], base=2)
				operand=memory[memory_address_dec]+memory[memory_address_dec+1]
				registerA_value=register_value_dict['A']
				register_value_dict['A']=zf_cf_set(operand | registerA_value)



		if(list[0]=='001011'):	#11 NOT

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



		if(list[0]=='001100'):	#12 SHL

			register_name=register_adress_dict[list[2]]
			operand=register_value_dict[register_name]
			shifted_operand=operand+'0'
			shifted_int=int(shifted_operand, base=2)
			register_value_dict[register_name]=shifted_operand[1:17]
			result= int(shifted_operand[1:17], base=2)


			if shifted_operand[0]==1:
				flags['CF']=1
			else:
				flags['CF']=0

			if result=0:
				flags['ZF']=1
			else: 
				flags['ZF']=0

			if shifted_operand[1]==1:
				flags['SF']=1
			else:
				flags['SF']=0



		if(list[0]=='001101'):	#13 SHR
			
			register_name=register_adress_dict[list[2]]
			operand=register_value_dict[register_name]
			shifted_int=int(shifted_operand, base=2)/2 #nasıl bölme int mi double mi
			register_value_dict[register_name]=format(shifted_int, '016b')

			if shifted_int=0:
				flags['ZF']=1
			else: 
				flags['ZF']=0

			flags['SF']=0
	


		if(list[0]=='001110'):	#14 NOP
			
			register_value_dict['PC']+=3



		if(list[0]=='001111'):	#15 PUSH

			register_name=register_adress_dict[list[2]]
			operand=register_value_dict[register_name]
			memory[register_value_dict['S']-1]=operand[0:8]
			memory[register_value_dict['S']]=operand[8:16]

			register_value_dict['S']-=2



		if(list[0]=='010000'):	#16 POP

			register_name=register_adress_dict[list[2]]
			register_value_dict[register_name]=memory[register_value_dict['S']]+memory[register_value_dict['S']+1]
			
			register_value_dict['S']+=2



		if(list[0]=='010001'):	#17 CMP
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
				not_operand=NOT(operand)
				inc_not_operand=ADD(not_operand, increment)
				registerA_value=register_value_dict['A']
				ADD(inc_not_operand, registerA_value)
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



		if(list[0]=='010010'):	#18 JMP

			register_value_dict['PC']=list[2]

		

		if(list[0]=='010011'):	#19 JZ-JE

			if(flags['ZF']==1):
				register_value_dict['PC']=list[2]
			else:
				register_value_dict['PC']+=3



		if(list[0]=='010100'):	#20	JNZ-JNE

			if(flags['ZF']==0):
				register_value_dict['PC']=list[2]
			else:
				register_value_dict['PC']+=3



		if(list[0]=='010101'):	#21 JC

			if(flags['CF']==1):
				register_value_dict['PC']=list[2]
			else:
				register_value_dict['PC']+=3



		if(list[0]=='010110'):	#22 JNC

			if(flags['CF']==0):
				register_value_dict['PC']=list[2]
			else:
				register_value_dict['PC']+=3



		if(list[0]=='010111'):	#23 JA

			if(flags['CF']==0 and flags['ZF']==0):
				register_value_dict['PC']=list[2]
			else:
				register_value_dict['PC']+=3
		


		if(list[0]=='011000'):	#24 JAE

			if((flags['CF']==0 and flags['ZF']==0) or flags['ZF']==1):
				register_value_dict['PC']=list[2]
			else:
				register_value_dict['PC']+=3



		if(list[0]=='011001'):	#25 JB

			if(flags['CF']==1):
				register_value_dict['PC']=list[2]
			else:
				register_value_dict['PC']+=3



		if(list[0]=='011010'):	#26 JBE

			if((flags['CF']==1 or flags['ZF']==1):
				register_value_dict['PC']=list[2]
			else:
				register_value_dict['PC']+=3



		if(list[0]=='011011'):	#27 READ

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



		if(list[0]=='011100'):	#28 PRİNT

			if list[1]=='00':								
				operand=list[2]
				ascii_char=int(operand, base=2)
				print(char(ascii_char))

			if list[1]=='01':
				register_name=register_adress_dict[list[2]]
				operand=register_value_dict[register_name]
				ascii_char=int(operand, base=2)
				print(char(ascii_char))

			if list[1]=='10':
				register_name=register_adress_dict[list[2]]
				register_value= register_value_dict[register_name]
				memory_address_dec= int(register_value, base=2)
				operand=memory[memory_address_dec]+memory[memory_address_dec+1]
				ascii_char=int(operand, base=2)
				print(char(ascii_char))

				
			if list[1]=='11':
				memory_address_dec= int(list[2], base=2)
				operand=memory[memory_address_dec]+memory[memory_address_dec+1]
				ascii_char=int(operand, base=2)
				print(char(ascii_char))









