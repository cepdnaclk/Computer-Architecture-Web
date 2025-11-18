# Lecture 7: Function Call and Return

## Introduction

Function calling is a fundamental mechanism that enables modular programming and code reuse. This lecture explores how ARM assembly implements function calls, covering parameter passing, return value handling, the call stack, register preservation conventions, and recursion. Understanding these mechanisms is essential for translating high-level function-based programs into assembly and for comprehending how processors manage execution context across function boundaries.


## 1. Function Calling Fundamentals

### 1.1 Function Calling Steps

**Complete Call Sequence**

1. **Place parameters** in argument registers (R0-R3)
2. **Transfer control** to callee function using BL
3. **Acquire stack storage** for temporary values
4. **Back up registers** that need preservation (R4-R11)
5. **Perform function operations** (the actual work)
6. **Place result** in return register (R0)
7. **Restore backed-up registers** from stack
8. **Return to caller** using MOV PC, LR

**Why This Complexity?**

- Enables nested and recursive function calls
- Protects caller's data in registers
- Provides local storage for function variables
- Supports arbitrary call depth

### 1.2 Why Use Functions?

**Benefits**

- **Code reuse**: Write once, call many times
- **Modularity**: Break complex problems into manageable pieces
- **Abstraction**: Hide implementation details
- **Maintainability**: Easier to debug and modify

**Example**

```c
int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(5, 3);  // Function call
}
```

## 2. ARM Register Conventions

### 2.1 Register Usage Rules

**Register Classification**

```
R0-R1:   Arguments and return results
         - Caller does NOT expect these preserved
         - Scratch registers

R2-R3:   Additional arguments
         - Also scratch registers
         - Caller does NOT expect preservation

R4-R11:  Local variables
         - MUST be preserved across function calls
         - Callee saves if it uses these registers

R12:     Intra-procedure-call scratch register
         - Can be corrupted by function calls
         - Not preserved

R13 (SP): Stack Pointer
         - Points to top of stack
         - MUST always be valid

R14 (LR): Link Register
         - Stores return address
         - Set by BL instruction

R15 (PC): Program Counter
         - Next instruction address
         - Modified to return from function
```


### 2.2 Shared Register File

**Key Concept**

- ALL functions share the SAME 16 registers
- No separate register sets per function
- Registers are a shared resource requiring careful management

**Implications**

- Functions must coordinate register usage
- Conventions prevent conflicts
- Callee must preserve certain registers (R4-R11)
- Caller can assume R4-R11 unchanged after call

**Example Scenario**

```assembly
main:
    MOV R4, #10      ; main uses R4
    MOV R0, #5       ; Pass argument
    BL function      ; Call function
    ; R4 still contains 10 (guaranteed)
    ADD R5, R4, R0   ; Use preserved R4 and return value

function:
    ; Must preserve R4 if we use it
    ; Can freely modify R0-R3, R12
    MOV R0, #20      ; Return value
    MOV PC, LR       ; Return
```

## 3. Function Call Instructions

### 3.1 Branch and Link (BL)

**Syntax**

```assembly
BL function_label    ; Branch and Link
```


**Operation**

1. **Save return address**: LR = address of next instruction
2. **Jump to function**: PC = function_label address

**Example**

```assembly
    MOV R0, #10      ; Address: 0x1000
    BL fun           ; Address: 0x1004
    ADD R1, R0, #5   ; Address: 0x1008 (return point)


fun:
    ; LR contains 0x1008 (address after BL)
    ; Function code here
    MOV PC, LR       ; Return to 0x1008
```

**Why "Link"?**

- Creates a "link" back to caller
- LR provides the connection
- Enables function to return

### 3.2 Return from Function

**Basic Return**

```assembly
MOV PC, LR           ; Copy LR to PC
```

**Operation**

- PC = LR (jump to return address)
- Execution continues at instruction after BL
- Simple and fast

**Alternative (older ARM)**

```assembly
BX LR                ; Branch and Exchange
```

## 4. Parameter Passing

### 4.1 Using R0-R3

**Convention**

- First 4 arguments in R0-R3
- Arguments loaded before BL instruction
- Callee reads R0-R3 to get parameters

**Example: Two Parameters**

```c
int multiply(int a, int b) {
    return a * b;
}

int result = multiply(6, 7);
```

**ARM Assembly**

```assembly
    MOV R0, #6       ; First argument (a)
    MOV R1, #7       ; Second argument (b)
    BL multiply      ; Call function
    ; R0 now contains result (42)


multiply:
    MUL R0, R0, R1   ; R0 = R0 × R1
    MOV PC, LR       ; Return
```

### 4.2 More Than 4 Arguments

**Solution: Use Stack**

- Arguments 1-4 in R0-R3
- Additional arguments pushed to stack
- Callee reads from stack

**Example: 6 Arguments**

```c
int sum6(int a, int b, int c, int d, int e, int f) {
    return a + b + c + d + e + f;
}
```

**ARM Assembly**

```assembly
    MOV R0, #1       ; arg1
    MOV R1, #2       ; arg2
    MOV R2, #3       ; arg3
    MOV R3, #4       ; arg4
    MOV R4, #5
    MOV R5, #6
    SUB SP, SP, #8   ; Space for 2 more args
    STR R4, [SP, #0] ; arg5 on stack
    STR R5, [SP, #4] ; arg6 on stack
    BL sum6
    ADD SP, SP, #8   ; Clean up stack


sum6:
    ; R0-R3 have first 4 args
    ; Load arg5 and arg6 from stack
    LDR R4, [SP, #0] ; arg5
    LDR R5, [SP, #4] ; arg6
    ADD R0, R0, R1
    ADD R0, R0, R2
    ADD R0, R0, R3
    ADD R0, R0, R4
    ADD R0, R0, R5
    MOV PC, LR
```

## 5. Return Values

### 5.1 Primary Return Register (R0)

**Convention**

- Result placed in R0
- Caller reads R0 after function returns
- Works for 32-bit values

**Example**

```assembly
add:
    ADD R0, R0, R1   ; R0 = R0 + R1
    MOV PC, LR       ; Return with result in R0

main:
    MOV R0, #10
    MOV R1, #20
    BL add           ; Call function
    ; R0 now contains 30
```

### 5.2 64-Bit Return Values

**Convention**

- Lower 32 bits in R0
- Upper 32 bits in R1
- Example: 64-bit integer or two 32-bit values

**Example**

```c
long long multiply64(int a, int b) {
    return (long long)a * b;
}
```

**ARM Assembly**

```assembly
multiply64:
    SMULL R0, R1, R0, R1  ; Signed multiply long
    ; R0 = lower 32 bits
    ; R1 = upper 32 bits
    MOV PC, LR
```


## 6. The Stack

### 6.1 Stack Structure

**Definition**

- Last In, First Out (LIFO) data structure
- Part of main memory
- Used for temporary storage

**Characteristics**

- **Starts at high address**: Top of memory
- **Grows downward**: Toward lower addresses
- **Stack Pointer (SP/R13)**: Points to top of stack
- **Dynamic size**: Grows and shrinks as needed

**Memory Layout**

```
High Address
  ┌─────────┐
  │  Stack  │ ← SP points here
  │   ↓     │   (grows downward)
  │         │
  ├─────────┤
  │  Heap   │
  │   ↑     │   (grows upward)
  ├─────────┤
  │  Data   │   (static variables)
  ├─────────┤
  │  Text   │   (instructions)
  └─────────┘
Low Address
```


### 6.2 Stack Uses

**Primary Purposes**

1. **Saving register values** (preserve R4-R11)
2. **Storing local variables** (arrays, structures)
3. **Preserving return addresses** (nested calls)
4. **Extra function arguments** (beyond R0-R3)
5. **Storing local arrays** that don't fit in registers

## 7. Stack Operations

### 7.1 Allocating Stack Space (Pushing)

**Decrement Stack Pointer**

```assembly
SUB SP, SP, #4       ; Allocate 4 bytes (1 register)
SUB SP, SP, #12      ; Allocate 12 bytes (3 registers)
```


**Why Subtract?**

- Stack grows toward lower addresses
- Allocating space moves SP downward
- Each 32-bit register needs 4 bytes

### 7.2 Storing Values to Stack

**Single Register**

```assembly
SUB SP, SP, #4       ; Allocate space
STR R4, [SP, #0]     ; Store R4 at top of stack
```


**Multiple Registers**

```assembly
SUB SP, SP, #12      ; Space for 3 registers
STR R4, [SP, #0]     ; Store R4
STR R5, [SP, #4]     ; Store R5
STR R6, [SP, #8]     ; Store R6
```

**Push Multiple (Convenient)**

```assembly
PUSH {R4-R6}         ; Allocate and store in one instruction
```


### 7.3 Loading Values from Stack

**Single Register**

```assembly
LDR R4, [SP, #0]     ; Load R4 from stack
ADD SP, SP, #4       ; Release space
```


**Multiple Registers**

```assembly
LDR R4, [SP, #0]     ; Restore R4
LDR R5, [SP, #4]     ; Restore R5
LDR R6, [SP, #8]     ; Restore R6
ADD SP, SP, #12      ; Release space
```

**Pop Multiple**

```assembly
POP {R4-R6}          ; Restore and release in one instruction
```


### 7.4 Stack Space Lifecycle

**Pattern**

1. **Allocate**: SUB SP, SP, #n
2. **Use**: STR/LDR with [SP, offset]
3. **Release**: ADD SP, SP, #n

**Important: Balance**

- Every SUB must have corresponding ADD
- Unbalanced stack causes bugs and crashes
- SP must be restored before return

## 8. Register Preservation

### 8.1 Why Preserve R4-R11?

**Problem**

- All functions share same registers
- Main function may be using R4-R11
- Called function needs registers for its work
- Must not corrupt caller's data

**Solution**

- Callee saves R4-R11 to stack at function start
- Uses registers freely during execution
- Restores R4-R11 from stack before return
- Caller expects R4-R11 unchanged

### 8.2 Preservation Pattern

**Function Template**

assembly
function:
    ; Prologue: Save registers
    SUB SP, SP, #12      ; Allocate space
    STR R4, [SP, #0]     ; Save R4
    STR R5, [SP, #4]     ; Save R5
    STR R6, [SP, #8]     ; Save R6

    ; Function body: Use R4-R6 freely
    ; ...

    ; Epilogue: Restore registers
    LDR R4, [SP, #0]     ; Restore R4
    LDR R5, [SP, #4]     ; Restore R5
    LDR R6, [SP, #8]     ; Restore R6
    ADD SP, SP, #12      ; Release space
    MOV PC, LR           ; Return


**Optimization**

- Only preserve registers actually used
- If function doesn't use R5, don't save/restore it
- Saves stack space and execution time

## 9. Nested Function Calls (Non-Leaf Functions)

### 9.1 The Problem

**Leaf Function**

- Doesn't call other functions
- LR preserved automatically (not overwritten)
- Simple return: MOV PC, LR

**Non-Leaf Function**

- Calls other functions
- BL overwrites LR with new return address
- Original LR lost!
- Cannot return to original caller

**Example Problem**

```assembly
main:
    BL funcA         ; LR = address after this BL

funcA:
    ; LR contains return address to main
    BL funcB         ; LR OVERWRITTEN with return to funcA!
    MOV PC, LR       ; Returns to funcA, not main (WRONG!)

funcB:
    MOV PC, LR       ; Correctly returns to funcA
```


### 9.2 Solution: Save LR to Stack

**Pattern**

assembly
function:
    ; Save LR first!
    SUB SP, SP, #4
    STR LR, [SP, #0]

    ; Now safe to call other functions
    BL other_function

    ; Restore LR before return
    LDR LR, [SP, #0]
    ADD SP, SP, #4
    MOV PC, LR


**Complete Example**

assembly
main:
    MOV R0, #5
    BL outer         ; LR = return_to_main
    ; Execution returns here

outer:
    SUB SP, SP, #4
    STR LR, [SP, #0] ; Save LR (return_to_main)

    MOV R1, R0
    ADD R0, R0, #10
    BL inner         ; LR = return_to_outer (overwrites!)

    ADD R0, R0, R1
    LDR LR, [SP, #0] ; Restore LR (return_to_main)
    ADD SP, SP, #4
    MOV PC, LR       ; Returns to main

inner:
    MUL R0, R0, R0
    MOV PC, LR       ; Returns to outer


## 10. Recursion Example: Factorial

### 10.1 Factorial Function

**C Code**

```c
int fact(int n) {
    if (n <= 1)
        return 1;
    else
        return n * fact(n-1);
}
```


**Key Points**

- Base case: n ≤ 1, return 1
- Recursive case: return n × fact(n-1)
- Each call creates new stack frame
- Stack unwinds as recursion returns

### 10.2 ARM Assembly Implementation

assembly
fact:
    ; Save LR and n
    SUB SP, SP, #8
    STR LR, [SP, #4]     ; Save return address
    STR R0, [SP, #0]     ; Save n

    ; Base case: if (n <= 1) return 1
    CMP R0, #1
    BGT recursive
    MOV R0, #1           ; Return 1
    B fact_end

recursive:
    ; Recursive case: n * fact(n-1)
    SUB R0, R0, #1       ; n-1
    BL fact              ; fact(n-1)
    LDR R1, [SP, #0]     ; Restore original n
    MUL R0, R0, R1       ; n * fact(n-1)

fact_end:
    ; Restore and return
    LDR LR, [SP, #4]
    ADD SP, SP, #8
    MOV PC, LR


### 10.3 Stack Growth During Recursion

**Call: fact(3)**

```
Initial: SP = 0x1000

fact(3) call:
  SP = 0x0FF8: [LR_main, 3]

fact(2) call:
  SP = 0x0FF0: [LR_fact3, 2]

fact(1) call:
  SP = 0x0FE8: [LR_fact2, 1]

Base case returns 1
Unwinds to fact(2): returns 1*2 = 2
Unwinds to fact(3): returns 2*3 = 6
Returns to main with result 6

Final: SP = 0x1000 (restored)
```


**Stack Space Per Call**

- 8 bytes (LR + n)
- fact(5) needs 5 × 8 = 40 bytes
- fact(10) needs 80 bytes
- Deep recursion can overflow stack!

## 11. Memory Layout and Stack vs. Heap

### 11.1 Complete Memory Layout

```
High Address (0xFFFFFFFF)
  ┌──────────────┐
  │   Reserved   │ OS and system
  ├──────────────┤
  │    Stack     │ ← SP (grows down)
  │      ↓       │   Automatic storage
  │              │   Function call data
  │              │   Local variables
  │              │
  │   (unused)   │
  │              │
  │      ↑       │
  │    Heap      │   Dynamic allocation
  │              │   malloc/free, new/delete
  ├──────────────┤
  │ Static Data  │   Global variables
  │              │   String constants
  ├──────────────┤
  │    Text      │   Program instructions
  │ (Code)       │   Read-only
  └──────────────┘
Low Address (0x00000000)
```


### 11.2 Stack Characteristics

**Automatic Storage**

- Allocated when function called
- Released when function returns
- Managed automatically by compiler/runtime

**Fast Access**

- Fixed addressing pattern
- SP always points to top
- Simple offset calculations

**Limited Size**

- Typically 1-8 MB
- Stack overflow if exceeded
- Recursion depth limited

**Scope**

- Local to function
- Not accessible after return
- Perfect for temporary data

### 11.3 Heap Characteristics

**Dynamic Allocation**

- malloc/free in C
- new/delete in C++
- Programmer controls lifetime

**Flexible Size**

- Can grow large (limited by available memory)
- Variable-sized allocations

**Manual Management**

- Must explicitly free memory
- Memory leaks if not freed
- Fragmentation possible

**Global Scope**

- Persists until explicitly freed
- Can pass pointers across functions
- Suitable for data structures

## Key Takeaways

1. **Function calling requires** parameter passing, return value handling, and register preservation.

2. **R0-R3 for arguments and returns** - caller doesn't expect preservation.

3. **R4-R11 must be preserved** by callee if used, protecting caller's data.

4. **BL instruction** saves return address in LR and jumps to function.

5. **Return via MOV PC, LR** copies link register to program counter.

6. **Stack is LIFO structure** growing downward from high addresses, pointed to by SP.

7. **Stack usage** includes saving registers, local variables, return addresses, and extra arguments.

8. **Allocate with SUB SP, release with ADD SP** - must balance allocations and releases.

9. **Non-leaf functions** must save LR to stack before making nested calls.

10. **Recursion** creates multiple stack frames, one per call, unwinding as calls return.

11. **Stack vs. Heap** - stack is automatic/local/fast/limited, heap is manual/global/flexible/larger.

12. **Register conventions** enable modularity and prevent conflicts in shared register file.

## Summary

Function calling mechanisms enable modular programming by providing structured ways to pass control, data, and return values between code sections. ARM's register conventions balance efficiency (passing arguments in registers) with safety (preserving callee-saved registers). The stack provides essential temporary storage for register preservation, local variables, and handling nested calls including recursion. Understanding these mechanisms is crucial for translating high-level function-based code to assembly, optimizing performance, and debugging stack-related issues. The interplay between registers, stack, and calling conventions forms the foundation for understanding how real programs execute, preparing us for more advanced topics like exception handling, operating systems, and compiler optimization.
