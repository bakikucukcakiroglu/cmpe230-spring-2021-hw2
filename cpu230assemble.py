import sys


def converter(opCode,adressingMode,Operand):  # converts the given assembly instruction to hex. Takes op_code, adressing_mode and operand, respectively and converts these instructions to hex format memory addresses.

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

# All instructions. 
my_dict = {'HALT': 1, 'LOAD': 2, 'STORE':3, 'ADD':4, 'SUB':5, 'INC':6, 'DEC':7, 'XOR':8, 'AND':9,  
           'OR':10, 'NOT':11, 'SHL': 12, 'SHR':13, 'NOP':14, 'PUSH':15, 'POP':16,'CMP':17,
           'JMP':18,'JZ':19, 'JE':19, 'JNZ':20, 'JNE':20, 'JC':21, 'JNC':22, 'JA':23, 
          'JAE':24, 'JB':25, 'JBE':26, 'READ':27,'PRINT':28}


# All labels and their memory addresses are recorded in label_dict.
label_dict = { }

# All registers and their memory addresses are recorded in register_dict 
register_dict = {'PC' :'0000', 'A':'0001', 'B' :'0002', 'C':'0003', 'D':'0004', 'E':'0005', 'S':'0006'}

# I/O
input_filename = sys.argv[1]
output_filename=sys.argv[2]

upper_list = [] # All lines in input file is recorded in this list.

with open(input_filename, "r") as first_file:  # We put all lines in a list that is named as upper_list.
  for line in first_file:

    stripped_line = line.strip()                           
    if("'" in line ):
      upper_list.append(line[:-3].upper() )
    elif(("[" in stripped_line) and ("]" in stripped_line)):
      index1=line.index("[")
      index2=line.index("]")
      stripped_line[index1:index2+1].replace(' ', '')
      upper_list.append(stripped_line.upper())
    else:
      upper_list.append(stripped_line.upper())






# Finds the labels and their memory addresses then records the values in the label_dict.
count = 0
for line in upper_list:
  stripped_line = line.strip()
  if ':' in  stripped_line: # If a line contains colon then it is a label.
    words=stripped_line.split()
    if(len(words)!=1 or stripped_line.count(":")>1 or stripped_line[-1]!=":" or not stripped_line[:-1].isalnum() ): # syntax check.
      print("Syntax error.")
      exit()
    
    for x in label_dict:
      if(lower(x) == lower(words[:-1])):
        print("Syntax error.")
        exit()

    temp = stripped_line[:-1]  
    print('temp', temp)
    label_dict[temp] = count 
  elif len(stripped_line)==0: # If a line is empty then continue to next iteration.
      continue
  else:
      count+=3 # Every instruction is 3 byte

f = open(output_filename, "w")


for line in upper_list:  

  

  if(len(stripped_line)==0): # If line is empty then continue to next iteration.
    continue

  words = stripped_line.split()  # The tokenized version of a list. The list contains strings. For example for LOAD A, words[0]="LOAD" and words[1]="A".
  print(words)

  if words[0] == 'HALT': # If first string of a line is HALT, then write the followings in output file:
    if(len(words)>1): # If there is more than 1 tokens in a line then there is a syntax error.
      print("Syntax error.")
      exit()
    f.write('040000')
    f.write('\n')
    


  elif words[0] == 'LOAD': # If first string of a line is LOAD, then check the second string.

    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error.
      print("Syntax error.")
      exit()
    if words[1] in register_dict: # If second string is one of the register names then write the following in output file:           
      f.write(converter('2', '1', register_dict[words[1]]))  
      f.write('\n')
    elif '[' in words[1] and ']' in words[1]:  # If second string contains [ and ] then that means operand is memory address or operands memory address is given in the register. 
                                                # To decide which one is this check the followings:                                            
      if words[1][1:-1] in register_dict:       # If the word between [ ] is one of the register names then write the following in output file:
        f.write(converter('2', '2', register_dict[words[1][1:-1]]))
        f.write('\n')
      else:                               # If the word between [ ] is a hexadecimal number, then write the following in output file:    
        f.write(converter('2', '3', words[1][1:-1]))
        f.write('\n')
    elif ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):   #If second word is hexadecimal or a char between ' '  then check the followings:
      if(words[1].isalnum() and len(words[1])<6): #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('2', '0', words[1]))
        f.write('\n')
      else:     #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        character = words[1][1:-1]
        f.write(converter('2', '0', hex(ord(character))[2:]))
        f.write('\n')
    elif words[1] in label_dict: #If second string is in label_dict then write the followings in output file.
        f.write(converter('2', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else: # If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()
   



  elif words[0] == 'STORE': # If first string of a line is STORE, then check the second string.

    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error.
      print("Syntax error.")
      exit()
    if words[1] in register_dict: # If second string is one of the register names then write the following in output file:
      f.write(converter('3', '1', register_dict[words[1]]))
      f.write('\n')
    elif '[' in words[1] and ']' in words[1]: # If second string contains [ and ] then that means operand is memory address or operands memory address is given in the register. 
                                                # To decide which one is this check the followings:
      if words[1][1:-1] in register_dict:       # If the word between [ ] is one of the register names then write the following in output file:
        f.write(converter('3', '2', register_dict[words[1][1:-1]]))
        f.write('\n')
      else:                                    # If the word between [ ] is a hexadecimal number, then write the following in output file
        f.write(converter('3', '3', words[1][1:-1]))
        f.write('\n')
    else:  #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'ADD': # If first string of a line is ADD, then check the second string.

    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error.
      print("Syntax error.")
      exit()

    if words[1] in register_dict:               # If second string is one of the register names then write the following in output file:
      f.write(converter('4', '1', register_dict[words[1]]))
      f.write('\n')
    elif '[' in words[1] and ']' in words[1]: # If second string contains [ and ] then that means operand is memory address or operands memory address is given in the register. 
                                                # To decide which one is this check the followings:
      if words[1][1:-1] in register_dict:        # If the word between [ ] is one of the register names then write the following in output file:
        f.write(converter('4', '2', register_dict[words[1][1:-1]]))
        f.write('\n')
      else:                                    # If the word between [ ] is a hexadecimal number, then write the following in output file
        f.write(converter('4', '3', words[1][1:-1]))
        f.write('\n')
    elif ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ): #If second word is hexadecimal or a char between ' '  then check the followings:
      if(words[1].isalnum() and len(words[1])<6): #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('4', '0', words[1]))
        f.write('\n')
      else:  #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        character = words[1][1:-1]
        f.write(converter('4', '0', hex(ord(character))[2:]))
        f.write('\n')
    elif words[1] in label_dict: #If second string is in label_dict then write the followings in output file.
        f.write(converter('4', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else:  #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'SUB': # If first string of a line is SUB, then check the second string.

    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error.
      print("Syntax error.")
      exit()
    if words[1] in register_dict:              # If second string is one of the register names then write the following in output file:
      f.write(converter('5', '1', register_dict[words[1]]))
      f.write('\n')
    elif '[' in words[1] and ']' in words[1]: # If second string contains [ and ] then that means operand is memory address or operands memory address is given in the register. 
                                                # To decide which one is this check the followings:
      if words[1][1:-1] in register_dict:       # If the word between [ ] is one of the register names then write the following in output file:
        f.write(converter('5', '2', register_dict[words[1][1:-1]]))
        f.write('\n')
      else:                                    # If the word between [ ] is a hexadecimal number, then write the following in output file
        f.write(converter('5', '3', words[1][1:-1]))
        f.write('\n')
    elif ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ): #If second word is hexadecimal or a char between ' '  then check the followings: 
      if(words[1].isalnum() and len(words[1])<6): #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('5', '0', words[1]))
        f.write('\n')
      else:  #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        character = words[1][1:-1]
        f.write(converter('5', '0', hex(ord(character))[2:]))
        f.write('\n')
    elif words[1] in label_dict: #If second string is in label_dict then write the followings in output file.
        f.write(converter('5', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'INC':  # If first string of a line is INC, then check the second string.

    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error.
      print("Syntax error.")
      exit()
    if words[1] in register_dict:               # If second string is one of the register names then write the following in output file:
      f.write(converter('6', '1', register_dict[words[1]]))
      f.write('\n')
    elif '[' in words[1] and ']' in words[1]: # If second string contains [ and ] then that means operand is memory address or operands memory address is given in the register. 
                                                # To decide which one is this check the followings:
      if words[1][1:-1] in register_dict:       # If the word between [ ] is one of the register names then write the following in output file:
        f.write(converter('6', '2', register_dict[words[1][1:-1]]))
        f.write('\n')
      else:                                   # If the word between [ ] is a hexadecimal number, then write the following in output file
        f.write(converter('6', '3', words[1][1:-1]))
        f.write('\n')
    elif ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):   #If second word is hexadecimal or a char between ' '  then check the followings: 
      if(words[1].isalnum() and len(words[1])<6): #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('6', '0', words[1]))
      else: #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        f.write(converter('6', '0', hex(ord(words[1][1:-1]))[2:]))
        f.write('\n')
    elif words[1] in label_dict:  #If second string is in label_dict then write the followings in output file.
        f.write(converter('6', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else:  #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'DEC': # If first string of a line is DEC, then check the second string.
    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error.
      print("Syntax error.")
      exit()
    if words[1] in register_dict:              # If second string is one of the register names then write the following in output file:
      f.write(converter('7', '1', register_dict[words[1]]))
      f.write('\n')
    elif '[' in words[1] and ']' in words[1]: # If second string contains [ and ] then that means operand is memory address or operands memory address is given in the register. 
                                                # To decide which one is this check the followings:
      if words[1][1:-1] in register_dict:       # If the word between [ ] is one of the register names then write the following in output file:
        f.write(converter('7', '2', register_dict[words[1][1:-1]]))
        f.write('\n')
      else:                                      # If the word between [ ] is a hexadecimal number, then write the following in output file
        f.write(converter('7', '3', words[1][1:-1]))
        f.write('\n')
    elif ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):   #If second word is hexadecimal or a char between ' '  then check the followings: 
      if(words[1].isalnum() and len(words[1])<6): #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('7', '0', words[1]))
        f.write('\n')
      else: #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        character = words[1][1:-1]
        f.write(converter('7', '0', hex(ord(character))[2:]))
        f.write('\n')
    elif words[1] in label_dict:  #If second string is in label_dict then write the followings in output file.
        f.write(converter('7', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else:  #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'XOR': # If first string of a line is XOR, then check the second string.
    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if words[1] in register_dict:                # If second string is one of the register names then write the following in output file:
      f.write(converter('8', '1', register_dict[words[1]]))
      f.write('\n')
    elif '[' in words[1] and ']' in words[1]: # If second string contains [ and ] then that means operand is memory address or operands memory address is given in the register. 
                                                # To decide which one is this check the followings:
      if words[1][1:-1] in register_dict:       # If the word between [ ] is one of the register names then write the following in output file:
        f.write(converter('8', '2', register_dict[words[1][1:-1]]))
        f.write('\n')
      else:                                      # If the word between [ ] is a hexadecimal number, then write the following in output file
        f.write(converter('8', '3', words[1][1:-1]))
        f.write('\n')
    elif ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):  #If second word is hexadecimal or a char between ' '  then check the followings: 
      if(words[1].isalnum() and len(words[1])<6):  #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('8', '0', words[1]))
        f.write('\n')
      else: #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        character = words[1][1:-1]
        f.write(converter('8', '0', hex(ord(character))[2:]))
        f.write('\n')
    elif words[1] in label_dict: #If second string is in label_dict then write the followings in output file.
        f.write(converter('8', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else:  #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'AND': # If first string of a line is AND, then check the second string.
    if(len(words)>2):  # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if words[1] in register_dict:              # If second string is one of the register names then write the following in output file:
      f.write(converter('9', '1', register_dict[words[1]]))
      f.write('\n')
    elif '[' in words[1] and ']' in words[1]: # If second string contains [ and ] then that means operand is memory address or operands memory address is given in the register. 
                                                # To decide which one is this check the followings:
      if words[1][1:-1] in register_dict:       # If the word between [ ] is one of the register names then write the following in output file:
        f.write(converter('9', '2', register_dict[words[1][1:-1]]))
        f.write('\n')
      else:                                    # If the word between [ ] is a hexadecimal number, then write the following in output file
        f.write(converter('9', '3', words[1][1:-1]))
        f.write('\n')
    elif ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ): #If second word is hexadecimal or a char between ' '  then check the followings: 
      if(words[1].isalnum() and len(words[1])<6):  #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('9', '0', words[1]))
        f.write('\n')
      else: #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        f.write(converter('9', '0', hex(ord(words[1][1:-1]))[2:]))
        f.write('\n')
    elif words[1] in label_dict: #If second string is in label_dict then write the followings in output file.
        f.write(converter('9', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'OR': # If first string of a line is OR, then check the second string.
    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if words[1] in register_dict:               # If second string is one of the register names then write the following in output file:
      f.write(converter('A', '1', register_dict[words[1]]))
      f.write('\n')
    elif '[' in words[1] and ']' in words[1]: # If second string contains [ and ] then that means operand is memory address or operands memory address is given in the register. 
                                                # To decide which one is this check the followings:
      if words[1][1:-1] in register_dict:        # If the word between [ ] is one of the register names then write the following in output file:
        f.write(converter('A', '2', register_dict[words[1][1:-1]]))
        f.write('\n')
      else:                                   # If the word between [ ] is a hexadecimal number, then write the following in output file
        f.write(converter('A', '3', words[1][1:-1]))
        f.write('\n')
    elif ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):    #If second word is hexadecimal or a char between ' '  then check the followings:   
      if(words[1].isalnum() and len(words[1])<6):#If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('A', '0', words[1]))
        f.write('\n')
      else: #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        f.write(converter('A', '0', hex(ord(words[1][1:-1]))[2:]))
        f.write('\n')
    elif words[1] in label_dict:  #If second string is in label_dict then write the followings in output file.
        f.write(converter('A', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()

        
  elif words[0] == 'NOT':  # If first string of a line is NOT, then check the second string.
    if(len(words)>2):  # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if words[1] in register_dict:               # If second string is one of the register names then write the following in output file:
      f.write(converter('B', '1', register_dict[words[1]]))
      f.write('\n')
    elif '[' in words[1] and ']' in words[1]: # If second string contains [ and ] then that means operand is memory address or operands memory address is given in the register. 
                                                # To decide which one is this check the followings:
      if words[1][1:-1] in register_dict:         # If the word between [ ] is one of the register names then write the following in output file:
        f.write(converter('B', '2', register_dict[words[1][1:-1]]))
        f.write('\n')
      else:                                   # If the word between [ ] is a hexadecimal number, then write the following in output file
        f.write(converter('B', '3', words[1][1:-1]))
        f.write('\n')
    elif ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):   #If second word is hexadecimal or a char between ' '  then check the followings:   
      if(words[1].isalnum() and len(words[1])<6):#If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('B', '0', words[1]))
        f.write('\n')
      else:#If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        f.write(converter('B', '0', hex(ord(words[1][1:-1]))[2:]))
        f.write('\n')
    elif words[1] in label_dict:#If second string is in label_dict then write the followings in output file.
        f.write(converter('B', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'SHL': # If first string of a line is SHL, then check the second string.
    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if words[1] in register_dict:               # If second string is one of the register names then write the following in output file:
      f.write(converter('C', '1', register_dict[words[1]]))
      f.write('\n')
    else:                   #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'SHR': # If first string of a line is SHR, then check the second string.
    if(len(words)>2):# If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if words[1] in register_dict:                # If second string is one of the register names then write the following in output file:
      f.write(converter('D', '1', register_dict[words[1]]))
      f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'NOP': # If first string of a line is NOP, then check the second string.
    if(len(words)>1): # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    f.write('380000')
    f.write('\n')



  elif words[0] == 'PUSH': # If first string of a line is PUSH, then check the second string.

    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if words[1] in register_dict:              # If second string is one of the register names then write the following in output file:
      f.write(converter('F', '1', register_dict[words[1]]))
      f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'POP': # If first string of a line is POP, then check the second string.
    if(len(words)>2):  # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if words[1] in register_dict:               # If second string is one of the register names then write the following in output file:
      f.write(converter('10', '1', register_dict[words[1]]))
      f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'CMP': # If first string of a line is CMP, then check the second string.
    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if words[1] in register_dict:               # If second string is one of the register names then write the following in output file:
      f.write(converter('11', '1', register_dict[words[1]]))
      f.write('\n')
    elif '[' in words[1] and ']' in words[1]: # If second string contains [ and ] then that means operand is memory address or operands memory address is given in the register. 
                                                # To decide which one is this check the followings:
      if words[1][1:-1] in register_dict:       # If the word between [ ] is one of the register names then write the following in output file:
        f.write(converter('11', '2', register_dict[words[1][1:-1]]))
        f.write('\n')
      else:                                    # If the word between [ ] is a hexadecimal number, then write the following in output file
        f.write(converter('11', '3', words[1][1:-1]))
        f.write('\n')
    elif ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ): #If second word is hexadecimal or a char between ' '  then check the followings: 
      if(words[1].isalnum() and len(words[1])<6): #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('11', '0', words[1]))
        f.write('\n')
      else: #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        f.write(converter('11', '0', hex(ord(words[1][1:-1]))[2:]))
        f.write('\n')
    elif words[1] in label_dict: #If second string is in label_dict then write the followings in output file.
        f.write(converter('11', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else:  #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'JMP':  # If first string of a line is JMP, then check the second string.
    if(len(words)>2):  # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):    #If second word is hexadecimal or a char between ' '  then check the followings: 
      if(words[1].isalnum() and len(words[1])<6): #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('12', '0', words[1]))
        f.write('\n')
      else: #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        f.write(converter('12', '0', hex(ord(words[1][1:-1]))[2:]))
        f.write('\n')
    elif words[1] in label_dict: #If second string is in label_dict then write the followings in output file.
        print('aaa',words[1][:-1])
        f.write(converter('12', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else:  #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'JZ' or words[0] == 'JE' : # If first string of a line is JZ OR JE, then check the second string.
    if(len(words)>2):  # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):    #If second word is hexadecimal or a char between ' '  then check the followings: 
      if(words[1].isalnum() and len(words[1])<6): #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('13', '0', words[1]))
        f.write('\n')
      else: #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        f.write(converter('13', '0', hex(ord(words[1][1:-1]))[2:]))
        f.write('\n')
    elif words[1] in label_dict: #If second string is in label_dict then write the followings in output file.
        f.write(converter('13', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'JNZ' or words[0] == 'JNE' :  # If first string of a line is JNZ OR JNE, then check the second string.
    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):  #If second word is hexadecimal or a char between ' '  then check the followings: 
      if(words[1].isalnum() and len(words[1])<6): #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('14', '0', words[1]))
        f.write('\n')
      else:  #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        f.write(converter('14', '0', hex(ord(words[1][1:-1]))[2:]))
        f.write('\n')
    elif words[1] in label_dict: #If second string is in label_dict then write the followings in output file.
        f.write(converter('14', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'JC':  # If first string of a line is JC, then check the second string.
    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):   #If second word is hexadecimal or a char between ' '  then check the followings: 
      if(words[1].isalnum() and len(words[1])<6):#If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('15', '0', words[1]))
        f.write('\n')
      else:#If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        f.write(converter('15', '0', hex(ord(words[1][1:-1]))[2:]))
        f.write('\n')
    elif words[1] in label_dict:#If second string is in label_dict then write the followings in output file.
        f.write(converter('15', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else:  #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'JNC': # If first string of a line is JNC then check the second string.
    if(len(words)>2):# If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):   #If second word is hexadecimal or a char between ' '  then check the followings: 
      if(words[1].isalnum() and len(words[1])<6):#If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('16', '0', words[1]))
        f.write('\n')
      else: #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        f.write(converter('16', '0', hex(ord(words[1][1:-1]))[2:]))
        f.write('\n')
    elif words[1] in label_dict:#If second string is in label_dict then write the followings in output file.
        f.write(converter('16', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'JA': # If first string of a line is JA then check the second string.
    if(len(words)>2):# If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()

    if ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):   #If second word is hexadecimal or a char between ' '  then check the followings:
      if(words[1].isalnum() and len(words[1])<6):#If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('17', '0', words[1]))
        f.write('\n')
      else:#If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        character = words[1][1:-1]
        f.write(converter('17', '0', hex(ord(character))[2:]))
        f.write('\n')
    elif words[1] in label_dict:#If second string is in label_dict then write the followings in output file.
        f.write(converter('17', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'JAE': # If first string of a line is JAE then check the second string.
    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()

    if ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):   #If second word is hexadecimal or a char between ' '  then check the followings:
      if(words[1].isalnum() and len(words[1])<6):#If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('18', '0', words[1]))
        f.write('\n')
      else: #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        character = words[1][1:-1]
        f.write(converter('18', '0', hex(ord(character))[2:]))
        f.write('\n')
    elif words[1] in label_dict: #If second string is in label_dict then write the followings in output file.
        f.write(converter('18', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'JB': # If first string of a line is JB then check the second string.
    if(len(words)>2):  # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()

    if ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):   #If second word is hexadecimal or a char between ' '  then check the followings:
      if(words[1].isalnum() and len(words[1])<6): #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('19', '0', words[1]))
        f.write('\n')
      else: #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        character = words[1][1:-1]
        f.write(converter('19', '0', hex(ord(character))[2:]))
        f.write('\n')
    elif words[1] in label_dict:  #If second string is in label_dict then write the followings in output file.
        f.write(converter('19', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'JBE': # If first string of a line is JBE then check the second string.
    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error.
      print("Syntax error.")
      exit()

    if ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):  #If second word is hexadecimal or a char between ' '  then check the followings:
      if(words[1].isalnum() and len(words[1])<6): #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('1A', '0', words[1]))
        f.write('\n')
      else: #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        character = words[1][1:-1]
        f.write(converter('1A', '0', hex(ord(character))[2:]))
        f.write('\n')
    elif words[1] in label_dict:  #If second string is in label_dict then write the followings in output file.
        f.write(converter('1A', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else:  #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'READ': # If first string of a line is READ then check the second string.
    if(len(words)>2): # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if words[1] in register_dict:               # If second string is one of the register names then write the following in output file:
      f.write(converter('1B', '1', register_dict[words[1]]))
      f.write('\n')
    elif '[' in words[1] and ']' in words[1]: # If second string contains [ and ] then that means operand is memory address or operands memory address is given in the register. 
                                                # To decide which one is this check the followings:
      if words[1][1:-1] in register_dict:       # If the word between [ ] is one of the register names then write the following in output file:
        f.write(converter('1B', '2', register_dict[words[1][1:-1]]))
        f.write('\n')
      else:                                      # If the word between [ ] is a hexadecimal number, then write the following in output file  
        f.write(converter('1B', '3', words[1][1:-1]))
        f.write('\n')
    else: #If second word does not meet the above conditions that means there is a syntax error. Because there is nothing left. Exits.
        print("Syntax error.")
        exit()


  elif words[0] == 'PRINT':  # If first string of a line is PRINT, then check the second string.
    if(len(words)>2):  # If there is more than 2 tokens in a line then there is a syntax error
      print("Syntax error.")
      exit()
    if words[1] in register_dict:                # If second string is one of the register names then write the following in output file:
      f.write(converter('1C', '1', register_dict[words[1]]))
      f.write('\n')
    elif '[' in words[1] and ']' in words[1]:   # If second string contains [ and ] then that means operand is memory address or operands memory address is given in the register. 
                                                # To decide which one is this check the followings:
      if words[1][1:-1] in register_dict:       # If the word between [ ] is one of the register names then write the following in output file:
        f.write(converter('1C', '2', register_dict[words[1][1:-1]]))
        f.write('\n')
      else:                                     # If the word between [ ] is a hexadecimal number, then write the following in output file  
        f.write(converter('1C', '3', words[1][1:-1]))
        f.write('\n')
    elif ( ( (words[1].isalnum() and (len(words[1])<6 ) )) or (len(words[1])==3 and words[1][0]=='\'' and words[1][2]=='\'') and (words[1] not in label_dict) ):    #If second word is hexadecimal or a char between ' '  then check the followings:   

      if(words[1].isalnum() and len(words[1])<6): #If second string is 1 2 3 4 5 digit hexadecimal then write the followings in output file:
        f.write(converter('1C', '0', words[1]))
        f.write('\n')
      else: #If it is not a 4 digit hexadecimal then that means it is a char between ' '. Find the ascii code of the char and convert that ascii code to hex. Then put the found value in converter function.
        character = words[1][1:-1]
        f.write(converter('1C', '0', hex(ord(character))[2:]))
        f.write('\n')
    elif words[1] in label_dict: #If second string is in label_dict then write the followings in output file.
        f.write(converter('1C', '0', hex(label_dict[words[1]])[2:]))
        f.write('\n')
    else: #If second string is in label_dict then write the followings in output file.
        print("Syntax error.")
        exit()

  else: 
      print("Syntax error.")
      exit()
