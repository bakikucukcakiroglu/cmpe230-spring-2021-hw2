import sys


def converter(opCode,adressingMode,Operand): #a,b,c hex verilmeli  0x i verme

  opcode   = int(opCode,16) 
  addrmode = int(adressingMode,16) 
  operand  = int(Operand,16) 

  bopcode = format(opcode, '06b') 
  baddrmode = format(addrmode, '02b') 
  boperand = format(operand, '016b') 
  bin = '0b' + bopcode + baddrmode + boperand 
  ibin = int(bin[2:],2) ; 
  instr = format(ibin, '06x')
  instr= instr.upper() 
  return instr


#yardımcı kodlar
# hex(my_dict['HALT'])
# print(hex(my_dict['HALT'])[2:]) #hexe çevirip baştaki 0x i siler
#print(stripped_line.split())  split kullan


# get vs [] for retrieving elements
my_dict = {'HALT': 1, 'LOAD': 2, 'STORE':3, 'ADD':4, 'SUB':5, 'INC':6, 'DEC':7, 'XOR':8, 'AND':9, 
           'OR':10, 'NOT':11, 'SHL': 12, 'SHR':13, 'NOP':14, 'PUSH':15, 'POP':16,'CMP':17,
           'JMP':18,'JZ':19, 'JE':19, 'JNZ':20, 'JNE':20, 'JC':21, 'JNC':22, 'JA':23, 
          'JAE':24, 'JB':25, 'JBE':26, 'READ':27,'PRINT':28}

label_dict = { }

register_dict = {'PC' :'0000', 'A':'0001', 'B' :'0002', 'C':'0003', 'D':'0004', 'E':'0005', 'S':'0006'}

with open("prog.asm.txt", "r") as a_file:


#doğru syntax için label bulur ve string olarak adresini dicte ekler 
  count = 0
  for line in a_file:
    stripped_line = line.strip()
    if ':' in  stripped_line:
        temp = stripped_line[:-1]
        label_dict[temp] = count 
    else:
        count+=3

  f = open("prog.txt", "w")

with open("prog.asm.txt", "r") as b_file:
  
  for line in b_file:   
    stripped_line = line.strip()
    words = stripped_line.split() #düzgün syntaxta lineı boşluklardan ayırır ( STORE [ A ]) düşün  LOAD [A]
    print(words)


    if words[0] == 'HALT':
      f.write('040000')
    


    if words[0] == 'LOAD':
      print('buraya')
      print(words[1].count('\''))
      print(words[1][1:-1])
      if words[1] in register_dict:               # register mı?
        f.write(converter('2', '1', register_dict[words[1]]))
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        if words[1][1:-1] in register_dict:       # memory register
          f.write(converter('2', '2', register_dict[words[1][1:-1]]))
          f.write('\n')
        else:                                     #memory
          f.write(converter('2', '3', words[1][1:-1]))
          f.write('\n')
      elif ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        print('girdim')
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('2', '0', words[1]))
          f.write('\n')
        else:
          character = words[1][1:-1]
          f.write(converter('2', '0', hex(ord(character))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('2', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'STORE':
      if words[1] in register_dict:               # register mı?
        f.write(converter('3', '1', register_dict[words[1]]))
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        if words[1][1:-1] in register_dict:       # memory register
          f.write(converter('3', '2', register_dict[words[1][1:-1]]))
          f.write('\n')
        else:                                     #memory
          f.write(converter('3', '3', words[1][1:-1]))
          f.write('\n')



    if words[0] == 'ADD':
      if words[1] in register_dict:               # register mı?  A,B,C
        f.write(converter('4', '1', register_value))
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        if words[1][1:-1] in register_dict:       # memory register [A]
          f.write(converter('4', '2', register_dict[words[1][1:-1]]))
          f.write('\n')
        else:                                     #memory [0010]
          f.write(converter('4', '3', words[1][1:-1]))
          f.write('\n')
      elif ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('4', '0', words[1]))
          f.write('\n')
        else:
          character = words[1][1:-1]
          f.write(converter('4', '0', hex(ord(character))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('4', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'SUB':
      if words[1] in register_dict:               # register mı?
        f.write(converter('5', '1', register_dict[words[1]]))
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        if words[1][1:-1] in register_dict:       # memory register
          f.write(converter('5', '2', register_dict[words[1][1:-1]]))
          f.write('\n')
        else:                                     #memory
          f.write(converter('5', '3', words[1][1:-1]))
          f.write('\n')
      elif ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('5', '0', words[1]))
          f.write('\n')
        else:
          character = words[1][1:-1]
          f.write(converter('5', '0', hex(ord(character))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('5', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'INC':
      if words[1] in register_dict:               # register mı?
        f.write(converter('6', '1', register_dict[words[1]]))
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        if words[1][1:-1] in register_dict:       # memory register
          f.write(converter('6', '2', register_dict[words[1][1:-1]]))
          f.write('\n')
        else:                                     #memory
          f.write(converter('6', '3', words[1][1:-1]))
          f.write('\n')
      elif ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('6', '0', words[1]))
        else:
          f.write(converter('6', '0', hex(ord(words[1][1:-1]))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('6', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'DEC':
      if words[1] in register_dict:               # register mı?
        f.write(converter('7', '1', register_dict[words[1]]))
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        if words[1][1:-1] in register_dict:       # memory register
          f.write(converter('7', '2', register_dict[words[1][1:-1]]))
          f.write('\n')
        else:                                     #memory
          f.write(converter('7', '3', words[1][1:-1]))
          f.write('\n')
      elif ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('7', '0', words[1]))
          f.write('\n')
        else:
          character = words[1][1:-1]
          f.write(converter('7', '0', hex(ord(character))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('7', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'XOR':
      if words[1] in register_dict:               # register mı?
        f.write(converter('8', '1', register_dict[words[1]]))
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        if words[1][1:-1] in register_dict:       # memory register
          f.write(converter('8', '2', register_dict[words[1][1:-1]]))
          f.write('\n')
        else:                                     #memory
          f.write(converter('8', '3', words[1][1:-1]))
          f.write('\n')
      elif ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('8', '0', words[1]))
          f.write('\n')
        else:
          character = words[1][1:-1]
          f.write(converter('8', '0', hex(ord(character))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('8', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'AND':
      if words[1] in register_dict:               # register mı?
        f.write(converter('9', '1', register_dict[words[1]]))
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        if words[1][1:-1] in register_dict:       # memory register
          f.write(converter('9', '2', register_dict[words[1][1:-1]]))
          f.write('\n')
        else:                                     #memory
          f.write(converter('9', '3', words[1][1:-1]))
          f.write('\n')
      elif ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('9', '0', words[1]))
          f.write('\n')
        else:
          f.write(converter('9', '0', hex(ord(words[1][1:-1]))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('9', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'OR':
      if words[1] in register_dict:               # register mı?
        f.write(converter('A', '1', register_dict[words[1]]))
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        if words[1][1:-1] in register_dict:       # memory register
          f.write(converter('A', '2', register_dict[words[1][1:-1]]))
          f.write('\n')
        else:                                     #memory
          f.write(converter('A', '3', words[1][1:-1]))
          f.write('\n')
      elif ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('A', '0', words[1]))
          f.write('\n')
        else:
          f.write(converter('A', '0', hex(ord(words[1][1:-1]))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('A', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'NOT':
      if words[1] in register_dict:               # register mı?
        f.write(converter('B', '1', register_dict[words[1]]))
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        if words[1][1:-1] in register_dict:       # memory register
          f.write(converter('B', '2', register_dict[words[1][1:-1]]))
          f.write('\n')
        else:                                     #memory
          f.write(converter('B', '3', words[1][1:-1]))
          f.write('\n')
      elif ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('B', '0', words[1]))
          f.write('\n')
        else:
          f.write(converter('B', '0', hex(ord(words[1][1:-1]))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('B', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'SHL':
      if words[1] in register_dict:               # register mı?
        f.write(converter('C', '1', register_dict[words[1]]))
        f.write('\n')



    if words[0] == 'SHR':
      if words[1] in register_dict:               # register mı?
        f.write(converter('D', '1', register_dict[words[1]]))
        f.write('\n')



    if words[0] == 'NOP':
      f.write('')



    if words[0] == 'PUSH':
      if words[1] in register_dict:               # register mı?
        f.write(converter('F', '1', register_dict[words[1]]))
        f.write('\n')



    if words[0] == 'POP':
      if words[1] in register_dict:               # register mı?
        f.write(converter('10', '1', register_dict[words[1]]))
        f.write('\n')



    if words[0] == 'CMP':
      if words[1] in register_dict:               # register mı?
        f.write(converter('11', '1', register_dict[words[1]]))
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        if words[1][1:-1] in register_dict:       # memory register
          f.write(converter('11', '2', register_dict[words[1][1:-1]]))
          f.write('\n')
        else:                                     #memory
          f.write(converter('11', '3', words[1][1:-1]))
          f.write('\n')
      elif ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('11', '0', words[1]))
          f.write('\n')
        else:
          f.write(converter('11', '0', hex(ord(words[1][1:-1]))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('11', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'JMP':
      if ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('12', '0', words[1]))
          f.write('\n')
        else:
          f.write(converter('12', '0', hex(ord(words[1][1:-1]))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('12', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'JZ' or words[0] == 'JE' :
      if ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('13', '0', words[1]))
          f.write('\n')
        else:
          f.write(converter('13', '0', hex(ord(words[1][1:-1]))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('13', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'JNZ' or words[0] == 'JNE' :
      if ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('14', '0', words[1]))
          f.write('\n')
        else:
          f.write(converter('14', '0', hex(ord(words[1][1:-1]))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('14', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'JC':
      if ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('15', '0', words[1]))
          f.write('\n')
        else:
          f.write(converter('15', '0', hex(ord(words[1][1:-1]))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('15', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'JNC':
      if ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('16', '0', words[1]))
          f.write('\n')
        else:
          f.write(converter('16', '0', hex(ord(words[1][1:-1]))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('16', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'JA':

      if ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('17', '0', words[1]))
          f.write('\n')
        else:
          character = words[1][1:-1]
          f.write(converter('17', '0', hex(ord(character))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('17', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'JAE':

      if ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('18', '0', words[1]))
          f.write('\n')
        else:
          character = words[1][1:-1]
          f.write(converter('18', '0', hex(ord(character))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('18', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'JB':

      if ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('19', '0', words[1]))
          f.write('\n')
        else:
          character = words[1][1:-1]
          f.write(converter('19', '0', hex(ord(character))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('19', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'JBE':

      if ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('1A', '0', words[1]))
          f.write('\n')
        else:
          character = words[1][1:-1]
          f.write(converter('1A', '0', hex(ord(character))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('1A', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')



    if words[0] == 'READ':
      if words[1] in register_dict:               # register mı?
        f.write(converter('1B', '1', register_dict[words[1]]))
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        if words[1][1:-1] in register_dict:       # memory register
          f.write(converter('1B', '2', register_dict[words[1][1:-1]]))
          f.write('\n')
        else:                                     #memory
          f.write(converter('1B', '3', words[1][1:-1]))
          f.write('\n')



    if words[0] == 'PRINT':
      if words[1] in register_dict:               # register mı?
        f.write(converter('1C', '1', register_dict[words[1]]))
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        if words[1][1:-1] in register_dict:       # memory register
          f.write(converter('1C', '2', register_dict[words[1][1:-1]]))
          f.write('\n')
        else:                                     #memory
          f.write(converter('1C', '3', words[1][1:-1]))
          f.write('\n')
      elif ((words[1].isdigit() and len(words[1])==4) or (words[1][0]=='‘' and words[1][2]=='’')):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write(converter('1C', '0', words[1]))
          f.write('\n')
        else:
          character = words[1][1:-1]
          f.write(converter('1C', '0', hex(ord(character))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          f.write(converter('1C', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')


































