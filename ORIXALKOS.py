import sys
import re
from sty import fg, bg, ef, rs, RgbFg
# filename = sys.argv[1]
# contents = ""
# with open(filename,'r' ) as handle:
#     contents = handle.read()

contents = """
Disassembly of section .plt:

00000390 <.plt>:
 390:   ff b3 04 00 00 00       pushl  0x4(%ebx)
 396:   ff a3 08 00 00 00       jmp    *0x8(%ebx)
 39c:   00 00                   add    %al,(%eax)
"""
#											^
#Take this to parse line by line this pawn--|
# [\s]*([\d\w]+):\s*(.{17})[\s]*([\w]*)[\s]*(.*$)

def ERRORLOG(text):
	print(bg.red+fg.white+text+fg.rs+bg.rs)

def WORKLOG(text):
	print(bg(0,0,200)+fg.white+text+fg.rs+bg.rs)

class DisasDataLine:
	def __init__(self,line=""):
		
		self.addr = 0
		self.lenof_code_in_bytes=len("ff b3 04 00 00 00")
		self.code_in_bytes = [0]*self.lenof_code_in_bytes
		self.command = "nop"
		self.command_data = "0x0"
		print("line:"+"'"+line+"'")
		if line == "" or line == " ":
			# ERRORLOG("Object shoulld be None")			
			raise ValueError('Empty line cant be decoded')
		WORKLOG("decoding...")
		self.decode(line)
	def decode(self, line):
		matcher = re.match(r"[\s]*([\d\w]+):\s*(.{17})[\s]*([\w]*)[\s]*(.*$)",line)
		if matcher:
			self.addr = matcher.group(1)
			self.code_in_bytes = matcher.group(2)
			self.command = matcher.group(3)
			self.command_data = matcher.group(4)
		else:
			#print(bg.red+fg.white+"Learn Regexpressions NOOB"+fg.rs+bg.rs)
			ERRORLOG("Learn Regexpressions NOOB")
	def print(self):
		# pass
		print("addr:"+str(self.addr))
		print("code_in_bytes:",end="")
		print(self.code_in_bytes)
		print("command:"+self.command)
		print("command_data:"+self.command_data)
	def prettyprint(self):
		print(str(self.addr)+"\t",end="")
		# print("code_in_bytes:",end="")
		print(self.code_in_bytes+"\t",end="")
		print(self.command+"\t",end="")
		print(self.command_data,end="")
		print()
class DisasFunction:
	def __init__(self,text):
		self.function_name = ""
		self.address_start = 0
		self.disas_data_lines = []
		self.decode(text)
	def decode(self,text):
		print("text:"+"'"+text+"'")
		matcher = re.match(r"[\s]*([\d\w]{8})\s<(.*?)>:([.\n\r\s\S]{0,})",text)
		if matcher:
			self.address_start = matcher.group(1)
			self.function_name = matcher.group(2)
			function_code_infos = matcher.group(3)
			for info in function_code_infos.split('\n'):
				# print("'"+info+"'")
				try:
					disasDataLine=DisasDataLine(info)
					disasDataLine.prettyprint()
					self.disas_data_lines.append(disasDataLine)
				except ValueError:
					continue
			
		else:
			ERRORLOG("Learn to regexp NOOB")
	def print(self):
		print("function_name:"+self.function_name)
		print("address_start:"+str(self.address_start))
		print("disas_data_lines:")
		for line in self.disas_data_lines:
			line.print()
	def prettyprint(self):
		
		print(bg.green+fg.black+"this is what i came up to\n"+str(self.address_start)+"\t",end="")
		print(bg.green+fg.black+self.function_name+":\n")

		for line in self.disas_data_lines:
			line.prettyprint()
		print(fg.rs+bg.rs)
class DisasSection:
	def __init__(self,sections):
		self.section_start_line = 0
		self.section_name = ""
		self.disas_functions = []
		self.decode(sections)
		# print("text:"+"'"+text+"'")
		# sys.exit()
	def decode(self,sections):
		for section in sections:
			print("Section:"+"'"+section+"'")
			disasFunction = DisasFunction(section)
			disasFunction.prettyprint()
			# TODO
			# Add it to disas_functions
			self.disas_functions.append(disasFunction)
	def print(self):
		print("section_name:"+self.section_name)
		# print("function_name:"+self.function_name)
		print("section_start_line:"+str(self.section_start_line))
		print("disas_functions:")
		for function in self.disas_functions:
			function.prettyprint()

if sys.argv[1] == '-test-line':
	for i in contents.split('\n')[4:]:
		try:
			dataLine = DisasDataLine(i)
			dataLine.print()
		except ValueError:
			pass
elif sys.argv[1] == '-test-function':
	contents = """000003b0 <__cxa_finalize@plt>:
3b0:	ff a3 14 00 00 00    	jmp    *0x14(%ebx)
3b6:	66 90                	xchg   %ax,%ax"""
#[\s]*([\d\w]{8})\s<(.*?)>:([.\n\r\s\S]{0,})
	disasFunction = DisasFunction(contents)
	disasFunction.prettyprint()
elif sys.argv[1] == '-test-section':
	contents = """
	Disassembly of section .plt.got:

000003b0 <__cxa_finalize@plt>:
 3b0:	ff a3 14 00 00 00    	jmp    *0x14(%ebx)
 3b6:	66 90                	xchg   %ax,%ax

000003b8 <__gmon_start__@plt>:
 3b8:	ff a3 18 00 00 00    	jmp    *0x18(%ebx)
 3be:	66 90                	xchg   %ax,%ax
 """
	# [\s]*([\d\w]{8})\s<(.*?)>:([.\n\r\s\S^[.{8}]]{0,})
	# ([\s]*[\d\w]{8}\s<.*?>:)
	matcher=re.split(r"([\s]*[\d\w]{8}\s<.*?>:)",contents)
	if matcher:
		sections = []
		# print(matcher[1]+matcher[2])
		# print(matcher[3]+matcher[4])
		index = 1
		while index <= len(matcher):
			if index+1 <= len(matcher):
				section = matcher[index]+matcher[index+1]
				sections.append(section)
				disasSection = DisasSection(sections)
				index+=1
			index+=1
else:
	ERRORLOG("Give an argument.(e.g -test-function -test-section -test-line")