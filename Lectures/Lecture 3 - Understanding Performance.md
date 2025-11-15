# Lecture 3: Understanding Performance

## Introduction

Understanding computer performance is fundamental to computer architecture and system design. This lecture explores how performance is measured, the factors that influence it, and the principles that guide performance optimization. We examine the metrics used to evaluate systems, the mathematical relationships between performance factors, and Amdahl's Law—a critical principle for understanding the limits of performance improvements.

---

## 1. Defining and Measuring Performance

### 1.1 Response Time vs. Throughput

**Response Time (Execution Time)**

- Time to complete a single task
- Includes all overhead and waiting time
- User-perceived performance metric
- Example: Time for a program to run from start to finish

**Throughput (Bandwidth)**

- Number of tasks completed per unit time
- Measures system capacity
- Important for servers and data centers
- Example: Number of transactions processed per second

**Relationship Between Metrics**

- Improving response time often improves throughput
- Improving throughput doesn't always improve response time
- Different optimization strategies for each metric
- System design must balance both considerations

### 1.2 Performance Definition

**Mathematical Definition**

```
Performance = 1 / Execution Time
```

**Performance Comparison**

- If System A is faster than System B:
  - Execution Time_A < Execution Time_B
  - Performance_A > Performance_B

**Relative Performance**

```
Performance_A / Performance_B = Execution Time_B / Execution Time_A
```

Example: If System A is 2× faster than System B:

- Performance_A / Performance_B = 2
- Execution Time_B / Execution Time_A = 2
- System A takes half the time of System B

## 2. CPU Time and Performance Factors

### 2.1 Components of Execution Time

**Total Execution Time**

- CPU time: Time CPU spends computing the task
- I/O time: Time waiting for input/output operations
- Other system activities: OS overhead, other programs

**CPU Time Focus**

- Primary metric for processor performance
- Excludes I/O and system effects
- Directly reflects processor and memory system performance
- Most relevant for comparing processor architectures

### 2.2 The CPU Time Equation

**Basic Formula**

```
CPU Time = Clock Cycles × Clock Period
```

Or equivalently:

```
CPU Time = Clock Cycles / Clock Rate
```

**Key Relationships**

- Clock Period = 1 / Clock Rate
- Clock Rate measured in Hz (cycles/second)
- Clock Cycles = total cycles to execute program
- Higher clock rate → shorter clock period → faster execution

**Example Calculation**

```
Program requires 10 billion cycles
Processor runs at 4 GHz (4 × 10^9 Hz)

CPU Time = 10 × 10^9 cycles / (4 × 10^9 cycles/sec)
         = 2.5 seconds
```

### 2.3 Instruction Count and CPI

**Cycles Per Instruction (CPI)**

- Average number of clock cycles per instruction
- Varies by instruction type and implementation
- Key microarchitecture metric

**Extended CPU Time Equation**

```
CPU Time = Instruction Count × CPI × Clock Period
```

Or:

```
CPU Time = (Instruction Count × CPI) / Clock Rate
```

**Three Performance Factors**

1. **Instruction Count**: Number of instructions executed
2. **CPI**: Average cycles per instruction
3. **Clock Rate**: Speed of the processor clock

**Factor Dependencies**

- Instruction Count: Determined by algorithm, compiler, ISA
- CPI: Determined by processor implementation (microarchitecture)
- Clock Rate: Determined by hardware technology and organization

## 3. Understanding CPI in Detail

### 3.1 CPI Variability

**Different Instructions, Different CPIs**

- Simple operations: May complete in 1 cycle (ADD, AND)
- Memory operations: May take multiple cycles (LOAD, STORE)
- Branch instructions: Variable cycles (depends on prediction)
- Multiply/Divide: Often take many cycles

**Calculating Average CPI**

```
Average CPI = Σ (CPI_i × Instruction Count_i) / Total Instruction Count
```

Where:

- CPI_i = cycles per instruction for instruction type i
- Instruction Count_i = number of times instruction i executed

### 3.2 CPI Example Calculation

**Given:**

- Program executes 100,000 instructions
- 50,000 ALU operations (CPI = 1)
- 30,000 load instructions (CPI = 3)
- 20,000 branch instructions (CPI = 2)

**Calculation:**

```
Total Cycles = (50,000 × 1) + (30,000 × 3) + (20,000 × 2)
             = 50,000 + 90,000 + 40,000
             = 180,000 cycles

Average CPI = 180,000 / 100,000 = 1.8
```

### 3.3 Instruction Classes

**Common Instruction Categories**

1. **Integer arithmetic**: ADD, SUB, AND, OR
2. **Data transfer**: LOAD, STORE
3. **Control flow**: BRANCH, JUMP, CALL
4. **Floating-point**: FADD, FMUL, FDIV

**CPI Characteristics by Class**

- Integer arithmetic: Usually 1 cycle
- Data transfer: 1-3 cycles (cache hit) or more (cache miss)
- Control flow: 1-2 cycles (correct prediction) or more (misprediction)
- Floating-point: 2-20+ cycles depending on operation

## 4. Performance Optimization Principles

### 4.1 Make the Common Case Fast

**Core Principle**

- Optimize frequent operations rather than rare ones
- Greater impact on overall performance
- Focus resources where they matter most

**Examples**

- Optimize ALU operations (common) over division (rare)
- Fast cache for recent data (commonly accessed)
- Branch prediction for likely paths
- Simple instructions execute quickly

**Application in Design**

- Identify common operations through profiling
- Allocate hardware resources accordingly
- Accept slower performance for rare cases
- Trade-offs guided by usage patterns

### 4.2 Amdahl's Law

**The Fundamental Principle**
The speedup that can be achieved by improving a particular part of a system is limited by the fraction of time that part is used.

**Mathematical Formula**

```
Speedup_overall = 1 / [(1 - P) + (P / S)]
```

Where:

- P = Proportion of execution time that can be improved
- S = Speedup of the improved portion
- (1 - P) = Proportion that cannot be improved

**Alternative Formulation**

```
Execution Time_new = Execution Time_old × [(1 - P) + (P / S)]
```

### 4.3 Amdahl's Law Examples

**Example 1: Multiply Operation Speedup**

Given:

- Multiply operations take 80% of execution time
- New hardware makes multiplies 10× faster

Calculation:

```
P = 0.80 (80% can be improved)
S = 10 (10× speedup)

Speedup_overall = 1 / [(1 - 0.80) + (0.80 / 10)]
                = 1 / [0.20 + 0.08]
                = 1 / 0.28
                = 3.57×
```

**Key Insight:** Despite 10× improvement in multiplies, overall speedup is only 3.57× because 20% of time is unaffected.

**Example 2: Limited Improvement Fraction**

Given:

- Only 30% of execution can be improved
- Improvement is 100× faster

Calculation:

```
P = 0.30
S = 100

Speedup_overall = 1 / [(1 - 0.30) + (0.30 / 100)]
                = 1 / [0.70 + 0.003]
                = 1 / 0.703
                = 1.42×
```

**Key Insight:** Even with 100× improvement, overall speedup is only 1.42× because only 30% of execution benefits.

### 4.4 Implications of Amdahl's Law

**Limitations of Parallelization**

- Serial portions limit parallel speedup
- As parallelism increases, serial portion dominates
- Cannot achieve infinite speedup regardless of cores

**Optimization Strategy**

- Focus on largest contributors to execution time
- Consider what fraction can realistically be improved
- Multiple small improvements may beat one large improvement
- Balance improvements across components

**Example: Multicore Scaling**

```
If 90% of program parallelizes perfectly:
2 cores:  Speedup = 1.82×
4 cores:  Speedup = 3.08×
8 cores:  Speedup = 4.71×
16 cores: Speedup = 6.40×
∞ cores:  Speedup = 10.00× (maximum possible)
```

The 10% serial portion ultimately limits speedup to 10×.

## 5. Complete Performance Analysis

### 5.1 The Complete Performance Equation

**Bringing It All Together**

```
CPU Time = (Instruction Count × CPI × Clock Period)
```

Expanded:

```
CPU Time = (Instructions) × (Cycles/Instruction) × (Seconds/Cycle)
```

**What Affects Each Factor**

**Instruction Count:**

- Algorithm: Efficient algorithms execute fewer instructions
- Programming language: High-level vs low-level
- Compiler: Optimization quality
- ISA: Instruction complexity and capabilities

**CPI:**

- ISA: Instruction complexity
- Microarchitecture: Pipeline depth, branch prediction
- Cache performance: Hit rates affect memory access CPI
- Instruction mix: Distribution of instruction types

**Clock Period (or Clock Rate):**

- Technology: Transistor speed (nm process)
- Organization: Pipeline depth, critical path length
- Power constraints: Higher frequency requires more power
- Cooling limitations: Heat dissipation capacity

### 5.2 Performance Comparison Example

**Scenario:**
Compare two implementations of the same ISA

- System A: Clock Rate = 2 GHz, CPI = 2.0
- System B: Clock Rate = 3 GHz, CPI = 3.0
- Same program with 1 million instructions

**System A:**

```
CPU Time_A = (1 × 10^6 instructions) × (2.0 cycles/instruction) / (2 × 10^9 cycles/sec)
           = 2 × 10^6 cycles / (2 × 10^9 cycles/sec)
           = 0.001 seconds = 1 millisecond
```

**System B:**

```
CPU Time_B = (1 × 10^6 instructions) × (3.0 cycles/instruction) / (3 × 10^9 cycles/sec)
           = 3 × 10^6 cycles / (3 × 10^9 cycles/sec)
           = 0.001 seconds = 1 millisecond
```

**Result:** Both systems have identical performance despite different clock rates and CPIs.

### 5.3 Trade-offs in Design

**Clock Rate vs. CPI Trade-off**

- Higher clock rate may require deeper pipeline
- Deeper pipeline often increases CPI (more stalls)
- Must balance frequency gains against CPI losses

**Instruction Count vs. CPI Trade-off**

- Complex instructions reduce instruction count
- But complex instructions may increase CPI
- CISC vs RISC architecture debate

**Power vs. Performance**

- Higher clock rate increases power consumption
- Power = Capacitance × Voltage² × Frequency
- Mobile systems prioritize power over peak performance

## 6. Practical Performance Considerations

### 6.1 Benchmarking

**Purpose of Benchmarks**

- Measure real-world performance
- Compare different systems objectively
- Standard workloads for reproducibility

**Types of Benchmarks**

- Synthetic: Artificial programs (e.g., Dhrystone, Whetstone)
- Application: Real programs (e.g., SPEC CPU, databases)
- Workload: Representative task mixes

**Benchmark Pitfalls**

- May not represent your workload
- Can be optimized for unfairly
- Need multiple benchmarks for complete picture

### 6.2 Performance Metrics in Practice

**MIPS (Million Instructions Per Second)**

```
MIPS = Instruction Count / (Execution Time × 10^6)
     = Clock Rate / (CPI × 10^6)
```

**Limitations of MIPS:**

- Doesn't account for instruction complexity
- Different ISAs have different instruction capabilities
- Higher MIPS doesn't guarantee better performance
- "Meaningless Indication of Processor Speed"

**Better Metrics:**

- Execution time for specific workloads
- Throughput for server applications
- Energy efficiency (performance per watt)
- Performance per dollar

### 6.3 Power and Energy Considerations

**Power Wall**

- Cannot increase clock rate indefinitely
- Power consumption limits frequency scaling
- Led to multi-core era

**Dynamic Power Equation**

```
Power = Capacitance × Voltage² × Frequency
```

**Energy Equation**

```
Energy = Power × Time
```

**Implications:**

- Lowering voltage reduces power dramatically (squared effect)
- Higher frequency increases power linearly
- Faster execution may save energy overall (less time)
- Energy efficiency increasingly important metric

## Key Takeaways

1. **Performance is the inverse of execution time** - faster systems have shorter execution times and higher performance values.

2. **Three key factors determine CPU performance:**

   - Instruction Count (algorithm, compiler, ISA)
   - CPI (microarchitecture, instruction mix)
   - Clock Rate (technology, organization)

3. **Amdahl's Law limits speedup** - the potential speedup from improving any part of a system is limited by how much time that part is used.

4. **"Make the common case fast"** - optimize frequently executed operations for maximum impact on overall performance.

5. **CPI varies by instruction type** - average CPI depends on the mix of instructions and their individual costs.

6. **Trade-offs are fundamental** - improvements in one area (e.g., clock rate) may harm another (e.g., CPI or power consumption).

7. **Benchmarking is essential** - real workloads provide the most meaningful performance measurements.

8. **Power is a critical constraint** - modern performance optimization must consider power and energy efficiency, not just speed.

9. **Multiple factors must be optimized together** - focusing on only one aspect (like clock rate) can be counterproductive.

10. **Understanding performance equations** enables rational design decisions and accurate performance predictions.

## Summary

Performance analysis is central to computer architecture, providing the foundation for making informed design decisions. By understanding the relationship between instruction count, CPI, and clock rate, architects can identify optimization opportunities and predict the impact of changes. Amdahl's Law reminds us that the benefit of any improvement is constrained by what fraction of execution time it affects, emphasizing the importance of focusing on the common case. As we design systems, we must balance competing factors—clock rate, CPI, power consumption, and cost—to achieve the best overall performance for target applications. The principles covered in this lecture provide the analytical framework for evaluating processor designs and optimization strategies throughout the study of computer architecture.
