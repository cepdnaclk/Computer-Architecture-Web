# Lecture 6: Branching and Control Flow

*By Dr. Kisaru Liyanage*

## 6.1 Introduction

Control flow is what distinguishes computers from simple calculators—the ability to make decisions and alter execution based on conditions. This lecture explores conditional operations and branching in ARM assembly, covering comparison instructions, conditional branches, loop implementation, and PC-relative addressing. Understanding these mechanisms is essential for translating high-level control structures (if statements, loops) into assembly code and for comprehending how processors implement dynamic program behavior.


## 6.2 Fundamentals of Conditional Execution

### 6.2.1 Decision-Making in Computers

**What Makes Computers Powerful**

- Ability to make decisions based on data
- Execute different instructions depending on conditions
- Implement if statements, loops, and function calls
- Respond dynamically to input and computed values

**Control Flow Concepts**

- **Sequential execution**: Default behavior (PC += 4)
- **Conditional branching**: Jump if condition is true
- **Unconditional branching**: Always jump
- **Function calls**: Branch with return address saving

### 6.2.2 Program Status Register (PSR)

**Status Flags**

- **N (Negative)**: Set if result is negative (bit 31 = 1)
- **Z (Zero)**: Set if result is zero
- **C (Carry)**: Set if unsigned overflow occurred
- **V (oVerflow)**: Set if signed overflow occurred

**How Flags Are Set**

- Comparison instructions (CMP, CMN, TST, TEQ)
- Arithmetic/logic instructions with S suffix (ADDS, SUBS)
- Flags reflect the result of the operation
- Used by subsequent conditional branches

**Example**

```assembly
CMP R1, R2           ; Compare R1 and R2 (computes R1 - R2)
                      ; Sets flags based on result
```

If R1 = 5, R2 = 3:

- Result of R1 - R2 = 2 (positive, non-zero)
- N = 0 (not negative)
- Z = 0 (not zero)
- C = 1 (no borrow needed)
- V = 0 (no overflow)

## 6.3 Comparison Instructions

### 6.3.1 Compare (CMP)

**Syntax**

```assembly
CMP Rn, Rm           ; Compare Rn with Rm
CMP Rn, #imm         ; Compare Rn with immediate
```

**Operation**

- Performs Rn - Rm (subtraction)
- Updates PSR flags based on result
- Does NOT store the result
- Does NOT modify any register

**Example Usage**

```assembly
MOV R1, #10
MOV R2, #5
CMP R1, R2           ; Compares 10 with 5
                      ; Result: 10 - 5 = 5 (positive, non-zero)
                      ; Z = 0, N = 0
```

### 6.3.2 Compare Negative (CMN)

**Syntax**

```assembly
CMN Rn, Rm           ; Compare Negative
CMN Rn, #imm
```

**Operation**

- Performs Rn + Rm (addition)
- Updates PSR flags
- Equivalent to CMP Rn, -Rm
- Useful for checking if sum equals zero

### 6.3.3 Test (TST)

**Syntax**

```assembly
TST Rn, Rm           ; Test bits
TST Rn, #imm
```

**Operation**

- Performs Rn AND Rm (bitwise AND)
- Updates PSR flags
- Result not stored
- Used to test if specific bits are set

**Example: Check if bit 5 is set**

```assembly
TST R1, #0x20        ; Test bit 5
BEQ bit_clear        ; Branch if bit was clear (Z=1)
```

### 6.3.4 Test Equivalence (TEQ)

**Syntax**

```assembly
TEQ Rn, Rm           ; Test Equivalence
TEQ Rn, #imm
```

**Operation**

- Performs Rn XOR Rm (exclusive OR)
- Updates PSR flags
- Z=1 if values are equal
- Used to compare values without affecting C or V flags

## 6.4 Conditional Branch Instructions

### 6.4.1 Branch if Equal (BEQ)

**Syntax**

```assembly
BEQ label            ; Branch if equal (Z=1)
```

**Condition**

- Branches if Zero flag is set (Z = 1)
- Typically used after CMP to check equality

**Example**

```assembly
CMP R1, R2           ; Compare R1 and R2
BEQ equal_label      ; Jump to equal_label if R1 == R2
; Code if not equal
equal_label:
; Code if equal
```

### 6.4.2 Branch if Not Equal (BNE)

**Syntax**

```assembly
BNE label            ; Branch if not equal (Z=0)
```

**Condition**

- Branches if Zero flag is clear (Z = 0)
- Opposite of BEQ

**Example**

```assembly
CMP R3, #0
BNE not_zero         ; Jump if R3 != 0
; Code if R3 is zero
not_zero:
; Code if R3 is non-zero
```

### 6.4.3 Signed Comparison Branches

**Branch if Greater or Equal (BGE)**

```assembly
BGE label            ; Branch if Rn >= Rm (signed)
                      ; Condition: N == V
```

**Branch if Less Than (BLT)**

```assembly
BLT label            ; Branch if Rn < Rm (signed)
                      ; Condition: N != V
```

**Branch if Greater Than (BGT)**

```assembly
BGT label            ; Branch if Rn > Rm (signed)
                      ; Condition: Z==0 AND N==V
```

**Branch if Less or Equal (BLE)**

```assembly
BLE label            ; Branch if Rn <= Rm (signed)
                      ; Condition: Z==1 OR N!=V
```

**Example**

```assembly
CMP R1, R2
BGE greater_equal    ; Branch if R1 >= R2 (signed)
; Code if R1 < R2
greater_equal:
; Code if R1 >= R2
```

### 6.4.4 Unsigned Comparison Branches

**Branch if Higher or Same (BHS)** (also called BCS - Branch if Carry Set)

```assembly
BHS label            ; Branch if Rn >= Rm (unsigned)
                      ; Condition: C == 1
```

**Branch if Lower (BLO)** (also called BCC - Branch if Carry Clear)

```assembly
BLO label            ; Branch if Rn < Rm (unsigned)
                      ; Condition: C == 0
```

**Branch if Higher (BHI)**

```assembly
BHI label            ; Branch if Rn > Rm (unsigned)
                      ; Condition: C==1 AND Z==0
```

**Branch if Lower or Same (BLS)**

```assembly
BLS label            ; Branch if Rn <= Rm (unsigned)
                      ; Condition: C==0 OR Z==1
```

### 6.4.5 Signed vs. Unsigned Example

**Key Difference**

```assembly
MOV R0, #0xFFFFFFFF  ; R0 = -1 (signed) or 4,294,967,295 (unsigned)
MOV R1, #1           ; R1 = 1
CMP R0, R1

BLO lower_unsigned   ; BRANCH NOT TAKEN
                      ; Unsigned: 4,294,967,295 > 1

BLT less_signed      ; BRANCH TAKEN
                      ; Signed: -1 < 1
```

**When to Use Each**

- **Signed**: Comparing integers that can be negative (temperatures, offsets, differences)
- **Unsigned**: Comparing addresses, array indices, sizes, counts

### 6.4.6 Unconditional Branch

**Syntax**

```assembly
B label              ; Branch always
```

**Purpose**

- Jump without checking any condition
- Skip code sections
- Implement infinite loops
- Return to loop start

**Example**

```assembly
B end                ; Skip this section
; Code to skip
end:
; Continue execution here
```

## 6.5 Labels in Assembly

### 6.5.1 Label Definition

**Purpose**

- Mark specific instruction locations
- Provide symbolic names for addresses
- Enable branches and data references

**Syntax**

```assembly
label:               ; Label definition (note colon)
    MOV R0, #1      ; Instruction at this label
```

**Naming Rules**

- Can be almost any identifier
- Common conventions: loop, exit, done, L1, L2
- Cannot conflict with instruction mnemonics
- Case-sensitive

**Example**

```assembly
start:
    MOV R0, #0
loop:
    ADD R0, R0, #1
    CMP R0, #10
    BLT loop         ; Branch to loop label
    B start          ; Branch to start label
```

### 6.5.2 Label Resolution

**Assembly Process**

1. First pass: Record label addresses
2. Second pass: Replace labels with addresses
3. Calculate offsets for PC-relative branches

**Virtual Addresses**

- Assembler assigns virtual addresses from 0
- First instruction: address 0
- Second instruction: address 4
- Third instruction: address 8
- Physical addresses determined at load time

## 6.6 Implementing Control Structures

### 6.6.1 If Statement

**C Code**

```c
if (i == j)
    f = g + h;
else
    f = g - h;
```

**ARM Assembly (Method 1: Branch on False)**

```assembly
    CMP R3, R4       ; Compare i (R3) and j (R4)
    BNE else         ; Branch to else if not equal
    ADD R0, R1, R2   ; f = g + h (then clause)
    B exit           ; Skip else clause

else:
    SUB R0, R1, R2   ; f = g - h (else clause)
exit:
    ; Continue...
```

**ARM Assembly (Method 2: Conditional Execution)**

```assembly
    CMP R3, R4       ; Compare i and j
    ADDEQ R0, R1, R2 ; f = g + h (executed only if equal)
    SUBNE R0, R1, R2 ; f = g - h (executed only if not equal)
```


### 6.6.2 If-Else Ladder

**C Code**

```c
if (x < 0)
    result = -1;
else if (x == 0)
    result = 0;
else
    result = 1;
```

**ARM Assembly**

```assembly
    CMP R1, #0       ; Compare x with 0
    BLT negative     ; Branch if x < 0
    BEQ zero         ; Branch if x == 0
    ; x > 0
    MOV R0, #1
    B done

negative:
    MOV R0, #-1
    B done
zero:
    MOV R0, #0
done:
    ; Continue...
```

### 6.6.3 While Loop

**C Code**

```c
while (i < n) {
    sum += i;
    i++;
}
```

**ARM Assembly**

```assembly
loop:
    CMP R1, R2       ; Compare i (R1) with n (R2)
    BGE end_loop     ; Exit if i >= n
    ADD R0, R0, R1   ; sum = sum + i
    ADD R1, R1, #1   ; i++
    B loop           ; Branch back to loop start
end_loop:
    ; Continue...
```

### 6.6.4 For Loop

**C Code**

```c
for (i = 0; i < 10; i++) {
    sum += i;
}
```

**ARM Assembly**

```assembly
    MOV R1, #0       ; i = 0 (initialization)

for_loop:
    CMP R1, #10      ; Compare i with 10
    BGE end_for      ; Exit if i >= 10
    ADD R0, R0, R1   ; sum = sum + i (loop body)
    ADD R1, R1, #1   ; i++ (increment)
    B for_loop       ; Branch back to loop start
end_for:
    ; Continue...
```

### 6.6.5 Do-While Loop

**C Code**

```c
do {
    sum += i;
    i++;
} while (i < n);
```

**ARM Assembly**

```assembly
do_loop:
    ADD R0, R0, R1   ; sum = sum + i (loop body first)
    ADD R1, R1, #1   ; i++
    CMP R1, R2       ; Compare i with n
    BLT do_loop      ; Branch back if i < n
    ; Continue...
```

**Key Difference from While**

- Body executes at least once
- Condition checked at end, not beginning

## 6.7 Array Access in Loops

### 6.7.1 Static Array Indexing

**C Code**

```c
while (save[i] == k)
    i++;
```

**ARM Assembly**

```assembly
    ; R6 = base address of save array
    ; R3 = i (index)
    ; R5 = k (comparison value)

loop:
    ADD R12, R6, R3, LSL #2  ; address = base + (i * 4)
    LDR R0, [R12, #0]        ; R0 = save[i]
    CMP R0, R5               ; Compare save[i] with k
    BNE exit                 ; Exit if not equal
    ADD R3, R3, #1           ; i++
    B loop                   ; Continue loop
exit:
    ; Continue...
```

**Dynamic Offset Calculation**

- `R3, LSL #2` means R3 × 4 (shift left 2 = multiply by 4)
- Words are 4 bytes, so array element i is at base + (i × 4)
- Efficient: shift is faster than multiplication

### 6.7.2 Array Traversal

**C Code**

```c
int sum = 0;
for (int i = 0; i < 10; i++) {
    sum += arr[i];
}
```

**ARM Assembly**

```assembly
    LDR R6, =arr     ; R6 = base address of array
    MOV R0, #0       ; sum = 0
    MOV R1, #0       ; i = 0

loop:
    CMP R1, #10
    BGE done
    ADD R12, R6, R1, LSL #2  ; address = base + i*4
    LDR R2, [R12]            ; R2 = arr[i]
    ADD R0, R0, R2           ; sum += arr[i]
    ADD R1, R1, #1           ; i++
    B loop
done:
    ; R0 contains sum
```

## 6.8 PC-Relative Addressing

### 6.8.1 Branch Instruction Encoding

**32-Bit Format**


[Cond][1010][Offset]
 4-bit 4-bit 24-bit


**Fields**

- **Cond**: Condition code (EQ, NE, LT, etc.)
- **1010**: Fixed format field for branch
- **Offset**: 24-bit signed offset

### 6.8.2 Address Calculation

**Problem with Absolute Addressing**

- 24 bits can address 2²⁴ = 16 MB
- Limits program size to 16 MB
- Fixed addresses complicate relocation

**PC-Relative Solution**

- Store offset from current PC, not absolute address
- Target = PC + offset
- Can branch ±16 MB from current instruction
- Total program can exceed 16 MB

**Offset Calculation**


Offset = (Target Address - PC) / 4


**Why Divide by 4?**

- All instructions are 4-byte aligned
- Least significant 2 bits always 00
- Omit these bits in encoding
- Effective range: ±64 MB (24-bit offset × 4)

**Example**


Current PC: 0x1000
Target: 0x1020
Offset = (0x1020 - 0x1000) / 4 = 0x20 / 4 = 8 instructions

Encoded offset in branch instruction: 8
At execution: PC = 0x1000 + (8 × 4) = 0x1020


### 6.8.3 Advantages of PC-Relative

**Position-Independent Code**

- Code can load at any address
- Branches remain correct regardless of location
- Essential for libraries and shared code

**Simplified Linking**

- Linker doesn't need to patch all branches
- Only external function calls need adjustment

**Branch Locality**

- Most branches are to nearby instructions
- PC-relative naturally handles this case
- Absolute addressing wastes bits for nearby targets

## 6.9 Conditional Execution (Alternative to Branching)

### 6.9.1 Conditional Instruction Suffixes

**Concept**

- Add condition code to instruction mnemonic
- Instruction executes only if condition is true
- Otherwise, instruction is skipped (NOP)

**Available Suffixes**

- EQ (equal), NE (not equal)
- GT, LT, GE, LE (signed comparisons)
- HI, LO, HS, LS (unsigned comparisons)
- Many others (see ARM documentation)

**Examples**

```assembly
CMP R1, R2
ADDEQ R0, R3, R4     ; Execute ADD only if R1 == R2
SUBNE R0, R3, R4     ; Execute SUB only if R1 != R2
MOVGT R5, #10        ; Execute MOV only if R1 > R2
```

### 6.9.2 Conditional Execution Example

**C Code**

```c
if (a == b)
    max = a;
else
    max = b;
```

**Method 1: Branching**

```assembly
    CMP R1, R2       ; Compare a and b
    BNE else
    MOV R0, R1       ; max = a
    B done

else:
    MOV R0, R2       ; max = b
done:
```

**Method 2: Conditional Execution**

```assembly
    CMP R1, R2       ; Compare a and b
    MOVEQ R0, R1     ; max = a (if equal)
    MOVNE R0, R2     ; max = b (if not equal)
```


### 6.9.3 Advantages and Limitations

**Advantages**

- More compact code (fewer instructions)
- No branch misprediction penalty
- Faster for simple conditions
- Clearer intent in some cases

**Limitations**

- Only works for simple, short sequences
- Cannot conditionally execute blocks of code
- All conditional instructions must fit in pipeline
- May execute both paths (but discard one result)

**When to Use**

- Simple assignments
- Min/max operations
- Short computations with single result
- Performance-critical paths where branches hurt

## 6.10 Basic Blocks

### 6.10.1 Definition

**Basic Block Characteristics**

- Sequence of instructions with:
  - No embedded branches (except possibly at end)
  - No branch targets (except possibly at beginning)
- Executed atomically: all or nothing
- Single entry point, single exit point

**Example**

```assembly
; Basic Block 1 (entry point)
    MOV R0, #0
    MOV R1, #10
    CMP R1, #10
    BNE block2       ; Exit point of block 1

; Basic Block 2 (entry and exit point)
block2:
    ADD R0, R0, #1
    CMP R0, R1
    BLT block2       ; Exit point of block 2
```

### 6.10.2 Importance in Compilation

**Compiler Optimizations**

- Identify basic blocks for analysis
- Optimize within blocks (register allocation, scheduling)
- Build control flow graph from blocks
- Apply inter-block optimizations

**Processor Optimizations**

- Predict block execution
- Prefetch instructions in block
- Schedule instructions more aggressively
- Reduce branch overhead

## Key Takeaways

1. **Conditional execution** distinguishes computers from calculators, enabling decision-making and dynamic behavior.

2. **CMP instruction** sets PSR flags by performing subtraction without storing the result.

3. **Conditional branches** (BEQ, BNE, BGE, BLT, etc.) check PSR flags to decide whether to jump.

4. **Signed vs. unsigned branches** interpret the same bit patterns differently based on context.

5. **Labels** provide symbolic names for addresses, enabling readable branch targets.

6. **If statements** translate to compare + conditional branch + unconditional branch to skip alternate path.

7. **Loops** use compare + conditional branch (to exit) + unconditional branch (to continue).

8. **Array access** in loops uses dynamic offset calculation with shifts (LSL #2 for word arrays).

9. **PC-relative addressing** stores branch offset from current PC, enabling position-independent code and large programs.

10. **Word-based offsets** effectively quadruple branch range by encoding instruction count instead of byte offset.

11. **Conditional execution** provides alternative to branching for simple cases, improving performance and code density.

12. **Basic blocks** are atomic instruction sequences used by compilers and processors for optimization.

13. **Branch locality** means most branches target nearby instructions, making PC-relative addressing natural and efficient.

## Summary

Branching and conditional execution form the foundation of program control flow, translating high-level constructs like if statements and loops into machine instructions. The ARM architecture provides a rich set of conditional branches for both signed and unsigned comparisons, enabling efficient implementation of diverse control structures. Understanding the distinction between comparison (which sets flags) and branching (which checks flags) is essential for correct assembly programming. PC-relative addressing solves program size limitations while enabling position-independent code, and conditional execution offers a performant alternative to branching for simple cases. Mastering these concepts is crucial for translating algorithms into assembly code, optimizing performance-critical sections, and understanding how processors implement dynamic program behavior. These fundamentals prepare us for more advanced topics including function calls, stack management, and processor pipelining.
