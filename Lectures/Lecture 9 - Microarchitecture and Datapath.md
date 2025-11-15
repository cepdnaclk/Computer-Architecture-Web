# Lecture 9: Microarchitecture and Datapath

## Introduction

This lecture transitions from instruction set architecture (ISA) to microarchitecture—the hardware implementation of the ISA. We explore how to build a processor that executes MIPS instructions, covering instruction formats, digital logic fundamentals, datapath construction, and single-cycle processor design. Understanding microarchitecture reveals how software instructions translate to hardware operations and provides the foundation for studying advanced processor designs including pipelining and superscalar execution.

---

## 1. Course Context and MIPS ISA

### 1.1 Transition to Hardware Implementation

**Previous Focus**: ARM ISA

- Instruction set
- Assembly programming
- Software perspective

**Current Focus**: MIPS Microarchitecture

- Hardware implementation
- Processor design
- Hardware perspective

**Why MIPS for Hardware Study?**

- Simpler than ARM (educational clarity)
- Clean RISC design
- Well-documented architecture
- Concepts apply to all processors

### 1.2 MIPS Instruction Categories

**Three Instruction Types** (based on encoding)

**I-Type (Immediate)**

- Contains one immediate operand
- Covers data processing, data transfer, control flow
- Examples: ADDI, LW, SW, BEQ
- Most common type

**R-Type (Register)**

- All operands are registers
- Primarily arithmetic and logic
- Examples: ADD, SUB, AND, OR
- Opcode always 0, funct field specifies operation

**J-Type (Jump)**

- Jump instructions
- Examples: J, JAL
- 26-bit address field

**Contrast with ARM**

- ARM: Data processing, data transfer, flow control
- MIPS: I-type, R-type, J-type
- Different classification philosophy

### 1.3 MIPS Instruction Encoding

**Fixed 32-Bit Length**

- Every instruction exactly 32 bits
- Simplifies fetch and decode
- Enables efficient pipelining

**R-Type Format**

```
[Opcode][RS][RT][RD][SHAMT][Funct]
 6 bits  5   5   5    5      6 bits
```

Fields:

- **Opcode**: Always 0 for R-type
- **RS**: Source register 1 (5 bits for 32 registers)
- **RT**: Source register 2
- **RD**: Destination register
- **SHAMT**: Shift amount (for shift instructions)
- **Funct**: Function code (actual operation)

**I-Type Format**

```
[Opcode][RS][RT][Immediate]
 6 bits  5   5   16 bits
```

Fields:

- **Opcode**: Varies by instruction
- **RS**: Source/base register
- **RT**: Source/destination register
- **Immediate**: 16-bit immediate value or offset

**J-Type Format**

```
[Opcode][Address]
 6 bits  26 bits
```

Fields:

- **Opcode**: 2 for J, 3 for JAL
- **Address**: 26-bit jump target (word address)

## 2. Digital Logic Review

### 2.1 Information Encoding

**Binary Representation**

- Low voltage = Logic 0
- High voltage = Logic 1
- Digital signals immune to analog noise

**Multi-Bit Signals**

- One wire per bit
- 32-bit instruction needs 32 wires
- Parallel transmission within CPU

### 2.2 Combinational Elements

**Definition**

- Output is function of inputs ONLY
- No internal state or memory
- Purely functional relationship

**Examples**

- AND, OR, NOT gates
- Multiplexers: `Y = (S == 0) ? I0 : I1`
- Adders: `Y = A + B`
- ALU: `Y = function(A, B, operation)`

**Characteristics**

- Output changes immediately with input (plus propagation delay)
- Can draw complete truth table
- Asynchronous operation (no clock needed)

### 2.3 Sequential Elements (State Elements)

**Definition**

- Output is function of inputs AND internal state
- Has memory—stores information over time
- State persists between clock cycles

**Examples**

- Registers
- Flip-flops
- Register files
- Memory units

**Characteristics**

- Store information
- Synchronized to clock signal
- Output depends on history

### 2.4 Clocking and Timing

**Clock Signal**

- Periodic alternating signal: Low → High → Low → High...
- Synchronizes all sequential operations

**Edge-Triggered**

- Rising edge: Transition 0 → 1
- Falling edge: Transition 1 → 0
- Most processors use rising edge

**Clock Period and Frequency**

```
Clock Period (T): Duration of one cycle
Clock Rate (f): Cycles per second

Relationship: f = 1/T

Example:
T = 250 ps = 0.25 ns
f = 1/(250 × 10^-12) = 4 GHz
```

### 2.5 Register Operations

**Basic Register**

- Stores multi-bit value (e.g., 32 bits)
- Updates on clock edge: D (input) → Q (output state)

**Register with Write Control**

- Additional Write Enable signal
- Updates ONLY when clock edge AND Write Enable = 1
- Otherwise holds previous value

**Timing Example**

```
Clock: __|‾|__|‾|__|‾|__
Write:  ‾‾‾‾|___|‾‾‾‾‾
Data:   [A][B][C][D][E]
State:  [A][A][A][D][D]
```

### 2.6 Critical Path and Clock Period

**Combinational Logic Delay**

- All combinational elements have propagation delay
- Different elements, different delays

**Clock Period Constraint**

```
Clock Period ≥ Longest Path Delay

Path: Register → Combinational Logic → Register

Must allow time for:
1. Register output stabilization
2. Combinational logic computation
3. Result reaching next register input
4. Setup time before next clock edge
```

**Critical Path**

- Longest delay path from register to register
- Determines minimum clock period
- Limits maximum clock frequency

**Single-Cycle Constraint**

- Complete one instruction per clock cycle
- Clock period must accommodate slowest instruction
- All instructions take same time (inefficient!)

## 3. CPU Execution Stages

### 3.1 Instruction Fetch (IF)

**Purpose**: Retrieve next instruction from memory

**Steps**:

1. Use Program Counter (PC) for instruction address
2. Access Instruction Memory with PC
3. Retrieve 32-bit instruction word
4. Instruction now in CPU for processing

**Hardware**:

- Program Counter (32-bit register)
- Instruction Memory (read-only during execution)
- Address bus from PC to memory
- Data bus from memory to CPU

### 3.2 Instruction Decode (ID)

**Purpose**: Interpret instruction and extract fields

**Decode Operations**:

1. **Examine Opcode** (bits 26-31):

   - If opcode = 0: R-type
   - If opcode = 2 or 3: J-type
   - Otherwise: I-type

2. **Extract Register Numbers**:

   - R-type: RS, RT, RD (three 5-bit fields)
   - I-type: RS, RT (two 5-bit fields)
   - J-type: No registers

3. **Extract Immediate/Address**:

   - I-type: 16-bit immediate
   - J-type: 26-bit address

4. **Extract Function/Shift** (R-type only):
   - Funct: bits 0-5 (ALU operation)
   - SHAMT: bits 6-10 (shift amount)

**Control Unit Role**:

- Decodes opcode
- Generates control signals
- Determines datapath activation

### 3.3 Execute (EX)

**Purpose**: Perform operation or calculate address

**Operations by Type**:

**Arithmetic/Logic (R-type, I-type arithmetic)**:

- Send operands to ALU
- ALU performs operation
- Operation from funct field (R-type) or opcode (I-type)

**Memory Access (Load/Store)**:

- ALU calculates address: Base + Offset
- Always performs addition
- Result is memory address

**Branch**:

- ALU compares registers: RS - RT
- Zero flag indicates equality
- Result determines branch decision

### 3.4 Memory Access (MEM)

**Purpose**: Read or write data memory

**Applies To**:

- Load instructions: Read from memory
- Store instructions: Write to memory
- NOT arithmetic/logic (skip this stage)

**Load Operation**:

1. Use address from ALU
2. Read data from memory
3. Data will be written to register

**Store Operation**:

1. Use address from ALU
2. Get data from RT register
3. Write data to memory

### 3.5 Register Write-Back (WB)

**Purpose**: Write result to destination register

**Applies To**:

- Arithmetic/Logic: Write ALU result
- Load: Write memory data
- NOT store or branch

**Source Selection**:

- Arithmetic/Logic: Data from ALU
- Load: Data from memory
- Multiplexer selects appropriate source

### 3.6 PC Update

**Purpose**: Determine next instruction address

**Default**: PC = PC + 4 (sequential)

**Branch/Jump**: PC = calculated target address

**Control Flow**:

- Multiplexer selects next PC value
- Sequential or branch/jump target
- Update happens at clock edge

## 4. R-Type Instruction Datapath

### 4.1 Register File

**Structure**:

- 32 registers (R0-R31), 32 bits each
- Three ports: 2 read, 1 write

**Read Ports**:

- Read Address 1: RS (5 bits)
- Read Address 2: RT (5 bits)
- Read Data 1: 32-bit output
- Read Data 2: 32-bit output
- Combinational (no clock)

**Write Port**:

- Write Address: RD (5 bits)
- Write Data: 32-bit input
- Write Enable: Control signal
- Synchronized (clock edge)

### 4.2 R-Type Execution Flow

**Instruction**: `ADD $t0, $t1, $t2` (R0 = R1 + R2)

**Step 1: Register Read**

- Extract RS (R1) and RT (R2) fields
- Register file outputs two 32-bit values

**Step 2: ALU Operation**

- Inputs: Two register values
- Funct field (6 bits) → ALU control (4 bits)
- ALU performs specified operation
- Examples: ADD, SUB, AND, OR, SLT

**Step 3: Write-Back**

- ALU result → Register file write data
- RD field specifies destination
- Write Enable = 1
- At clock edge: Result written

### 4.3 ALU Control

**Function Field Encoding**:

```
Funct     | Operation | ALU Control
----------|-----------|-------------
0x20      | ADD       | 0010
0x22      | SUB       | 0110
0x24      | AND       | 0000
0x25      | OR        | 0001
0x2A      | SLT       | 0111
```

**ALU Control Logic**:

- Input: 6-bit funct field
- Output: 4-bit ALU operation
- Combinational logic (lookup table)

## 5. I-Type Instruction Datapath

### 5.1 Differences from R-Type

**Operand Sources**:

- R-type: Both from registers
- I-type: One register, one immediate

**Register Usage**:

- RS: Source register
- RT: Destination register (NOT source!)
- Immediate: 16-bit operand

### 5.2 Sign Extension

**Problem**: 16-bit immediate, 32-bit ALU

**Process**:

1. Take 16-bit immediate
2. Examine bit 15 (sign bit)
3. Replicate sign bit to bits 16-31
4. Result: 32-bit signed value

**Examples**:

```
16-bit: 0x0005 → 32-bit: 0x00000005 (+5)
16-bit: 0xFFFB → 32-bit: 0xFFFFFFFB (-5)
```

**Hardware**: Simple wire replication (fast)

### 5.3 Multiplexer for ALU Input

**ALU Input B Selection**:

- Input 0: Register data (RT) for R-type
- Input 1: Sign-extended immediate for I-type
- Select: ALUSrc control signal

**ALUSrc Signal**:

```
ALUSrc = 0: Use register (R-type, branch)
ALUSrc = 1: Use immediate (I-type)
```

## 6. Load/Store Instruction Datapath

### 6.1 Address Calculation

**Formula**: Address = Base + Offset

**Components**:

- Base: RS register (32-bit pointer)
- Offset: 16-bit signed immediate (sign-extended)
- ALU: Always performs addition

**Examples**:

```
LW $t1, 8($t0)    # Load from $t0 + 8
SW $t2, -4($sp)   # Store to $sp - 4
```

### 6.2 Load Word (LW)

**Instruction Format**:

- RS: Base register
- RT: Destination register
- Immediate: Offset

**Execution**:

1. Read RS (base address)
2. Sign-extend immediate (offset)
3. ALU adds: Address = RS + offset
4. Read data from memory at address
5. Write data to RT register

**Critical Path**: Longest in single-cycle design

- Fetch → Register Read → ALU → Memory → Register Write

### 6.3 Store Word (SW)

**Instruction Format**:

- RS: Base register
- RT: Source register (data to store)
- Immediate: Offset

**Execution**:

1. Read RS (base) and RT (data)
2. ALU calculates address
3. Write RT data to memory at address
4. NO register write-back

**Key Difference**:

- Reads TWO registers (RS and RT)
- Memory write instead of read
- No register write stage

### 6.4 Data Memory

**Interface**:

- Address: From ALU (32 bits)
- Write Data: From RT register
- Read Data: To register file (for loads)

**Control Signals**:

- MemRead: Enable read (LW)
- MemWrite: Enable write (SW)

**Multiplexer for Write-Back**:

- Input 0: ALU result (arithmetic/logic)
- Input 1: Memory data (load)
- Select: MemtoReg signal

## 7. Branch Instruction Datapath

### 7.1 Branch Types

**BEQ (Branch if Equal)**:

- Compare RS and RT
- Branch if RS == RT

**BNE (Branch if Not Equal)**:

- Compare RS and RT
- Branch if RS != RT

### 7.2 Branch Target Calculation

**Components**:

1. PC + 4 (next sequential instruction)
2. Offset from immediate (in instructions)
3. Target = (PC + 4) + (Offset × 4)

**Why PC + 4?**

- Offset relative to NEXT instruction
- PC already incremented

**Word to Byte Conversion**:

- Immediate: Number of instructions
- Multiply by 4: Byte offset
- Shift left 2 (wire routing, no hardware!)

### 7.3 Branch Execution

**Step 1: Register Comparison**

- Read RS and RT
- ALU subtracts: RS - RT
- Generate Zero flag

**Step 2: Zero Flag Evaluation**

- Zero = 1: Values equal
- Zero = 0: Values different

**Step 3: Target Calculation** (parallel)

- Sign-extend immediate
- Shift left 2
- Add to PC + 4

**Step 4: PC Update Decision**

```
BEQ: PCSrc = Branch AND Zero
BNE: PCSrc = Branch AND NOT(Zero)
```

**Multiplexer**:

- Input 0: PC + 4 (sequential)
- Input 1: Branch target
- Select: PCSrc

### 7.4 Sign Extension and Shifting

**Sign Extension**: Preserves signed offset

- Forward branch: Positive offset
- Backward branch: Negative offset

**Shift Left 2**: Wire routing trick

- Take bits 0-29 of sign-extended value
- Connect to bits 2-31 of result
- Append two zero wires at bits 0-1
- NO actual shifter hardware!

## 8. Complete Single-Cycle Datapath

### 8.1 Integrated Components

**Instruction Fetch**:

- PC register
- Instruction memory
- PC + 4 adder

**Register File**:

- 32 registers with 3 ports
- Two read, one write

**ALU**:

- Two 32-bit inputs
- Operation control
- Result output
- Zero flag

**Data Memory**:

- Address from ALU
- Write data from register
- Read data to register

**Sign Extender**:

- 16-bit input
- 32-bit output

**Branch Logic**:

- Target adder
- PC multiplexer

**Multiplexers**:

- ALU input B (register vs immediate)
- Register write data (ALU vs memory)
- Next PC (PC+4 vs branch target)

### 8.2 Control Signals

**Generated by Control Unit**:

1. RegDst: Register destination select
2. Branch: Branch instruction indicator
3. MemRead: Memory read enable
4. MemtoReg: Memory to register select
5. MemWrite: Memory write enable
6. ALUSrc: ALU source select
7. RegWrite: Register write enable
8. ALUOp: ALU operation type

### 8.3 Parallel Operations

**Key Insight**: Hardware operates in PARALLEL

- All datapath elements active simultaneously
- Some produce meaningless results
- Control signals select valid paths

**Example**: R-type instruction

- Sign extender operates on bits 0-15
- Produces meaningless output (no immediate in R-type)
- Multiplexer doesn't select it (ALUSrc = 0)

### 8.4 Critical Path Analysis

**Path for Load Word** (longest):

```
1. Instruction fetch:     200 ps
2. Register read:         150 ps
3. Sign extend:           50 ps
4. Multiplexer:           25 ps
5. ALU address calc:      200 ps
6. Data memory access:    200 ps
7. Multiplexer:           25 ps
8. Register write setup:  100 ps
Total:                    950 ps
```

**Clock Period**: Must be ≥ 950 ps
**Max Frequency**: 1/950 ps ≈ 1.05 GHz

**Inefficiency**:

- ALL instructions take 950 ps
- Fast R-type (650 ps) waits
- Wasted time per fast instruction

### 8.5 Single-Cycle Disadvantages

**Inefficiency**:

- Fast instructions wait for slow ones
- Clock period by worst case
- Cannot optimize common case

**Hardware Duplication**:

- Separate instruction/data memories
- Multiple adders
- Cannot reuse hardware in same cycle

**No Parallelism**:

- One instruction at a time
- Hardware mostly idle
- Poor resource utilization

**Advantages**:

- Simple design
- Simple control
- One instruction per cycle (conceptually)
- Good for learning

## Key Takeaways

1. **Microarchitecture is hardware implementation of ISA** - translating instruction semantics to hardware operations.

2. **MIPS uses three instruction types**: R-type (registers), I-type (immediate), J-type (jump).

3. **Fixed 32-bit instructions** simplify fetch/decode and enable efficient pipelining.

4. **Combinational elements** have output as function of inputs only; sequential elements have state.

5. **Clock period must exceed longest combinational path** between sequential elements.

6. **Six execution stages**: Fetch, Decode, Execute, Memory, Write-back, PC Update.

7. **Register file has three ports**: two read (combinational), one write (clocked).

8. **Sign extension** converts 16-bit immediate to 32-bit preserving signed value.

9. **Multiplexers select between data sources** based on control signals.

10. **ALU operations vary by instruction**: addition (load/store), subtraction (branch), varies (R-type).

11. **Critical path determines clock period** - load word is longest in single-cycle design.

12. **Single-cycle processor completes one instruction per cycle** but inefficiently (all take same time).

13. **Separate instruction and data memories** required for single-cycle (both accessed same cycle).

14. **Control signals orchestrate datapath** - generated by control unit from opcode.

15. **All hardware operates in parallel** - control signals select valid results, ignore others.

## Summary

Microarchitecture bridges the gap between software instructions and hardware implementation, revealing how processors execute programs. Building a single-cycle MIPS processor requires understanding digital logic fundamentals, datapath component design, and control signal generation. While conceptually simple (one instruction per cycle), the single-cycle design is inefficient because all instructions must complete within the time required by the slowest instruction. The critical path—typically the load word instruction—determines the maximum clock frequency. Understanding this foundation prepares us for more sophisticated designs including multi-cycle processors (which break execution into multiple stages) and pipelined processors (which overlap instruction execution for higher throughput). These microarchitecture concepts apply broadly across processor design, from embedded systems to high-performance superscalar processors.
