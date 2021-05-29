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
  print('geliyom')

with open("prog.asm.txt", "r") as b_file:
  
  for line in b_file:   
    stripped_line = line.strip()
    words = stripped_line.split(' ') #düzgün syntaxta lineı boşluklardan ayırır ( STORE [ A ]) düşün  LOAD [A]
    print(words)

    if words[0] == 'HALT':
      f.write('040000')
    if words[0] == 'LOAD':
      print ('girdim')
      if words[1] in register_dict:               # register mı?
        register_value= register_dict[words[1]]
        f.write('09'+register_value)
        f.write('\n')
      elif '[' in words[1] and ']' in words[1]: 
        print('memory veya memory register')
        if words[1][1:-1] in register_dict:       # memory register
          register_value= register_dict[words[1][1:-1]]
          f.write('0A'+ register_value)
          f.write('\n')
        else:                                     #memory
          f.write('0B'+words[1][1:-1]) 
          f.write('\n')
      elif ((words[1].isdigit() and len(words[1])==4) or (words[1].count('\'')==2)):   #immediate
        if(words[1].isdigit() and len(words[1])==4):
          f.write('08'+words[1])
          f.write('\n')
        else:
          character = words[1][1:-1]
          print('character', character,hex(ord(character))[2:])

          f.write(converter('2', '0', hex(ord(character))[2:]))
          f.write('\n')
      elif words[1] in label_dict:
          hex(label_dict[words[1]])
          f.write(converter('2', '0', hex(label_dict[words[1]])[2:]))
          f.write('\n')








































