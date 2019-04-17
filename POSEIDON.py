import sys
import re
filename = sys.argv[1]
contents = ""
with open(filename,'r' ) as handle:
    contents = handle.read()

contents = """
Disassembly of section .plt:

00000390 <.plt>:
 390:   ff b3 04 00 00 00       pushl  0x4(%ebx)
 396:   ff a3 08 00 00 00       jmp    *0x8(%ebx)
 39c:   00 00                   add    %al,(%eax)
"""

"""
00000360 <_init>:
 360:	53                   	push   %ebx
 361:	83 ec 08             	sub    $0x8,%esp
 364:	e8 97 00 00 00       	call   400 <__x86.get_pc_thunk.bx>
 369:	81 c3 73 1c 00 00    	add    $0x1c73,%ebx
 36f:	8b 83 18 00 00 00    	mov    0x18(%ebx),%eax
 375:	85 c0                	test   %eax,%eax
 377:	74 05                	je     37e <_init+0x1e>
 379:	e8 3a 00 00 00       	call   3b8 <__gmon_start__@plt>
 37e:	83 c4 08             	add    $0x8,%esp
 381:	5b                   	pop    %ebx
 382:	c3                   	ret
Disassembly of section .plt:

00000390 <.plt>:
 390:   ff b3 04 00 00 00       pushl  0x4(%ebx)
 396:   ff a3 08 00 00 00       jmp    *0x8(%ebx)
 39c:   00 00                   add    %al,(%eax)
        ...

000003a0 <__libc_start_main@plt>:
 3a0:   ff a3 0c 00 00 00       jmp    *0xc(%ebx)
 3a6:   68 00 00 00 00          push   $0x0
 3ab:   e9 e0 ff ff ff          jmp    390 <.plt>

Disassembly of section .plt.got:

000003b0 <__cxa_finalize@plt>:
 3b0:   ff a3 14 00 00 00       jmp    *0x14(%ebx)

"""
class DisasDataLine:
    def __init__(self,line=""):
        self.addr = 0
        self.code_in_bytes = [0]*12
        self.command = "nop"
        self.command_data = "0x0"
        print("line:"+"'"+line+"'")
        self.decode(line)   
    def decode(self, line):
        if line == "":
            return None
        addr = line[:line.find(':')].rsplit()
        self.addr = addr
        symb_len = {':':line.find(':')}
        code_in_bytes = line[symb_len[':']:symb_len[':']+12+4]
        self.code_in_bytes = code_in_bytes
    def print(self):
        pass
        #print("addr:"+str(self.addr))
        # print("code_in_bytes"+self.code_in_bytes)
        # print("command:"+self.command)
        # print("command_data:"+self.command_data)
class DisasFunction:
    def __init__(self,text):
        self.function_name = ""
        self.address_start = 0
        self.disas_data_lines = []
        self.decode(text)
    def setFunctionName(self,name):
        self.function_name = name
    def setAddressStart(self,start):
        self.address_start = start
    def decode(self,text):
        # print(text)
        text_in_lines = text.split('\n')
        # self.address_start = text_in_lines[0][:8]
        # print("self.address_start"+"'"+self.address_start+"'")
        print("text in DisasFunction:'"+text+"'") 
        for line in text_in_lines[1:]:
            # continue
            # sys.exit()
            decoded_line = DisasDataLine(line)
            if decoded_line == None:
                pass
            else:
                self.disas_data_lines.append(decoded_line)
    def print(self):
        print("function_name:"+self.function_name)
        print("address_start:"+str(self.address_start))
        print("disas_data_lines:")
        for line in self.disas_data_lines:
            line.print()
class DisasSection:
    def __init__(self,text):
        self.section_name = ""
        # self.function_name = ""
        self.address_start = 0
        self.disas_functions = []
        self.decode(text)
        print("text:"+"'"+text+"'")
        # sys.exit()
    def setSectionName(self,name):
        self.section_name = name
    def decode(self,text):
        # print(text)
        text_in_lines = text.split('\n')
        self.address_start = text_in_lines[0][:8]
        print("self.address_start"+"'"+self.address_start+"'")
            
        """
         .init:

00000360 <_init>:
 360:   53                      push   %ebx
 361:   83 ec 08                sub    $0x8,%esp
 364:   e8 97 00 00 00          call   400 <__x86.get_pc_thunk.bx>
 369:   81 c3 73 1c 00 00       add    $0x1c73,%ebx
 36f:   8b 83 18 00 00 00       mov    0x18(%ebx),%eax
 375:   85 c0                   test   %eax,%eax
 377:   74 05                   je     37e <_init+0x1e>
 379:   e8 3a 00 00 00          call   3b8 <__gmon_start__@plt>
 37e:   83 c4 08                add    $0x8,%esp
 381:   5b                      pop    %ebx
 382:   c3                      ret    

'

         r"\s*[\.a-zA-Z]*:\s*(([0-9]*)\s<[._]([a-zA-Z0-9]*)>:)[\s]*"//this gives addr and name function
         "\s*[\.a-zA-Z]*:\s*(([0-9]*)\s<[._]([a-zA-Z0-9]*)>:)([\s\d\w.:%$,<>()+@]*) //this gives all the data after name and addr of function in a group
        """
        print("text:"+"'"+text+"'")
        #regex-scope the header of a function in a section
        func_args = re.match(r"\s*[\.a-zA-Z]*:\s*(([0-9]*)\s<[._]([a-zA-Z0-9]*)>:)([\s\d\w.:%$,<>()+@]*)", text)
        if func_args:
            func_addr = func_args.group(2)
            func_name = func_args.group(3)
            func_code_infos = func_args.group(4)
            print("func_addr:"+func_addr)
            print("func_name:"+func_name)
            print("func_code:'"+func_code_infos+"'")
            disasFunction = DisasFunction(func_code_infos)
            disasFunction.setFunctionName(func_name)
            disasFunction.setAddressStart(func_addr)
            self.disas_functions.append(disasFunction)
    def print(self):
        print("section_name:"+self.section_name)
        # print("function_name:"+self.function_name)
        print("address_start:"+str(self.address_start))
        print("disas_data_lines:")
        # for line in self.disas_data_lines:
        #     line.print()
contents_by_lines = contents.split('\n')
lineNumStart = 0
lineNumEnd = 0
disassembly_of_sections = contents.split("Disassembly of section")
# print(disassembly_of_sections[2])
prev_section = disassembly_of_sections[0]
# print("{")
# print(disassembly_of_sections[0])
# print("}")
# print()
# print("{")
# print(disassembly_of_sections[1])
# print("}")
# print("{")
# print(disassembly_of_sections[2])
# print("}")
lineCount = len(prev_section.split('\n'))
print(lineCount)
for i,section in enumerate(disassembly_of_sections):
    if i == 0:
        continue
    disassembly_of_section_by_lines = section.split('\n')
    for j,line in enumerate(disassembly_of_section_by_lines):
        # if line == "":
        #     continue
        section_name = line
        print(section_name)
        # print(len(prev_section.split('\n')))
        print("Section "+section_name+" starts at line :"+str(lineCount))
        print("Section "+section_name+" ends at line :"+str(lineCount + len(section.split('\n'))-1))
        prev_section = section
        lineCount += len(prev_section.split('\n'))-1
        # print("Section "+section_name+" ends at line :" + str(i))
        # Contruct items of DisasSectiondata
        print(section)

        disasSection = DisasSection(section)
        disasSection.setSectionName(section_name)
        # print(section)
        # disasSection.decode(section)
        disasSection.print()

        continue
        

    # disasSection = DisasSection()
    #     disasSection.decode(contents_by_lines[lineNumStart:lineNumEnd])
    #     disasSection.print()

# sys.exit()
# for i,line in enumerate(contents_by_lines):
#     section_name = ""
#     if "Disassembly of section" in line:
#         section_name = line[len("Disassembly of section"):]
#         print("section name:" + section_name)
#         lineNumStart = i+1
#         for j,templine in enumerate(contents_by_lines[lineNumStart+1:]):
#             if "Disassembly of section" in templine:
#                 lineNumEnd = j+lineNumStart - 1
#         print("Section "+section_name+" starts at line :"+str(lineNumStart))
#         print("Section "+section_name+" ends at line :" + str(lineNumEnd))
#         disasSection = DisasSection()
#         disasSection.decode(contents_by_lines[lineNumStart:lineNumEnd])
#         disasSection.print()
