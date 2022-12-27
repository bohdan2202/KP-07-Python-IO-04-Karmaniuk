.386
.model flat, stdcall
option casemap:none

include \masm32\include\masm32rt.inc

.data
;перелік перемінних факторіал
n_factorial dd 0
fact_factorial dd 1
ret_factorial dd 1
;список змінних main
n_main dd 0
ret_main dd 0

O2 dd 0
O3 dd 0
O4 dd 0
O6 dd 0
O1 dd 0
  
.code
start:

main proc
    ;внесення значення в перемінну
    mov eax, 4
    mov n_main, eax
    ;зіставлення двох чисел     
    mov eax, n_main
    mov ebx, 0
    cmp eax, ebx
    jl @LOWER6
    mov eax, 0
    mov O6, eax
    jmp @EXIT_LT6
    @LOWER6: 
    mov eax, 1
    mov O6, eax
    @EXIT_LT6:
    ;if
    mov eax, O6
    mov ebx, 0
    cmp eax, ebx
    jne @TRUE5
    ;false
    ;записувати значення в перемінну
    mov eax, n_main
    mov n_factorial, eax
    call factorial
    ;повернення наслідок функції
    mov eax, ret_factorial
    mov ret_main, eax
    jmp @EXIT_IF5
    @TRUE5: 
    ;true
    ;повернення наслідок функції
    mov eax, 0
    mov ret_main, eax
    @EXIT_IF5:
    fn MessageBox,0,str$(ret_main), "Return", MB_OK
    ret
main endp

factorial proc
    ;зітавлення двох цифр <
    mov eax, n_factorial
    mov ebx, 1
    cmp eax, ebx
    jl @LOWER1
    mov eax, 0
    mov O1, eax
    jmp @EXIT_LT1
    @LOWER1:
    mov eax, 1
    mov O1, eax
    @EXIT_LT1:
    ;if
    mov eax, O1
    mov ebx, 0
    cmp eax, ebx
    jne @TRUE1
    ;false
    ;помножування двох чисел
    mov eax, fact_factorial
    mov ebx, n_factorial
    mul ebx
    mov fact_factorial, eax
    ;віднімання двох чисел
    mov eax, n_factorial
    mov ebx, 1
    sub eax, ebx
    mov n_factorial, eax
    ;повернення наслідку функції
    mov eax, fact_factorial
    mov ret_factorial, eax
    call factorial
    @TRUE1:
    ;true
    ret
factorial endp

invoke main
invoke ExitProcess, 0
END start