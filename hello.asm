;nasm -f elf -l hello.lst hello.asm
;gcc -o hello hello.o

msg:	db "Hello World", 10;10 = carriage return
len:	equ $-msg	;EQU directive eliminates hardcoding:

			;    NUM_OF_STUDENTS  EQU   90
  			;	..
			;    mov ecx, NUM_OF_STUDENTS
			;$ means here, so len is address of here
 
	SECTION .text
	global main	;make label available to linker
main:
	mov edx,len
	mov ecx,msg
	mov ebx,1	;where to write,screen
	mov eax,4	;sys out command
	int 0x80	;interrupt,call kernel to print

	mov ebx,0	;;return 0
	mov eax,1	;exit command to kernel
	int 0x80	;interrupt.Probalby interupt looks at eax for args 
