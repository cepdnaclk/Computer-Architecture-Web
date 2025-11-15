# Lecture 19: Multiprocessors

## Introduction

Multiprocessor systems represent a fundamental paradigm shift in computer architecture, using multiple processors on the same chip to execute multiple programs or threads simultaneously when traditional performance improvement techniques—clock frequency scaling and instruction-level parallelism—reached physical and practical limits. This lecture explores the evolution toward multiprocessor architectures driven by power walls and parallelism walls, examines the critical challenge of cache coherence that arises when multiple processors maintain private caches of shared memory, and analyzes solutions including bus snooping protocols like MESI and scalable directory-based coherence schemes. We compare architectural organizations from uniform memory access (UMA) to non-uniform memory access (NUMA), understanding how different designs balance simplicity, performance, and scalability for systems ranging from dual-core smartphones to thousand-processor supercomputers.

---

## 1. Introduction to Multiprocessors

Multiprocessor systems address performance limitations encountered with single processor systems by employing multiple processors on the same chip to execute multiple programs or threads simultaneously.

---

## 2. Performance Evolution Background

### Historical Performance Improvements

#### Early Methods: Clock Frequency Scaling

**Approach**:

- Increasing clock frequency (reducing clock cycle time)
- Goal: Spend less time per instruction

**Limitations Encountered**:

- Hit barrier at ~4 GHz: Power wall problem
- Excessive power dissipation caused overheating
- Cooling became inadequate
- Could not sustainably increase frequency further

#### Instruction Level Parallelism (ILP)

**Techniques**:

- **Pipelining**: Process multiple instructions simultaneously
- Utilize different hardware components at same time
- Example: Execute one instruction while fetching another
- **Advanced techniques**: Multiple issue, out-of-order execution
- Exploit parallelism inherent in programs

**Limitations Encountered**:

- Programs contain limited inherent parallelism
- Dependencies prevent unlimited parallel execution
- Hit "parallelism wall"
- Can't exploit more parallelism beyond program's inherent limits

### Moore's Law Context

**Observation**:

- Number of transistors doubles every 2 years
- Technology improves, more transistors available

**Question**: How to use abundant transistors?

**Solution**: Multiple processors on same chip

---

## 3. Multiprocessor Approach

### Key Characteristics

- Multiple processor cores on same chip
- Execute multiple instruction streams simultaneously
- Run multiple programs/threads in real time (true parallelism)
- Different from single processor illusion of parallelism

### Terminology

- **Processing Elements (PE)**: Common term for individual processors
- Each PE is a complete CPU with fetch, decode, execute units

### Key Problem: Communication Between Processors

- Multiple processors executing simultaneously
- Programs often need to communicate/share data
- Splitting programs into threads requires coordination
- Communication is central design challenge

---

## 4. Shared Memory Multiprocessors (SMM)

### Most Common Approach

**Architecture**:

- Communication through shared memory
- All processors access same physical address space
- Memory device connected via common bus/interconnect

### Operating System Role

**Responsibilities**:

- OS code stored in shared memory
- OS shared between all processors
- Manages memory access arbitration
- Performs workload balancing
- Ensures processors access only authorized memory portions

### Workload Balancing

**Purpose**:

- OS distributes tasks among processors
- Goal: All processors working in parallel
- Avoid idle processors
- Maximize overall system utilization

---

## 5. Memory Contention Problem

### Inherent Issue

**Challenge**:

- Multiple processors accessing same memory device
- Competition for memory access
- Processors must wait for memory availability
- Synchronization overhead
- Access time increases with contention

### Effect on Performance

**Bottleneck**:

- Memory becomes bottleneck
- Bus connects all processors to memory
- If one processor using memory, others must wait
- Can take hundreds of cycles
- Limits scalability

---

## 6. Uniform Memory Access (UMA)

### Definition

**Characteristics**:

- Each processor sees memory in exact same way
- Same average memory access time for all processors
- Access time independent of which processor is accessing
- By design, no difference in access time (ignoring contention)

### Also Known As

- **Symmetric Multiprocessors (SMP)**
- Both terms used interchangeably

### Key Properties

- Shared address space
- Uniform view of memory by all processors
- All processors experience same average latency

---

## 7. Solution to Contention: Caches

### Using Local Caches

**Approach**:

- Each processor has private cache
- Based on locality principles (temporal and spatial)
- Most memory accesses served at cache level
- Only small percentage (misses) go to main memory
- Reduces bus/memory contention significantly

### Benefits

- Exploits locality in programs
- Minimizes memory accesses
- Reduces bottleneck effect
- Allows better scalability

### New Problem: Cache Coherence

- Shared data blocks can be in multiple caches
- Updates in one cache not automatically reflected in others
- Need mechanism to maintain consistency

---

## 8. Cache Coherence Problem

### The Issue

**Scenario**:

- Multiple caches have copies of same data block
- One processor writes to that block
- Other caches have stale (old) data
- Processors see different values for same address
- Data becomes incoherent

### Example Sequence

1. **PE1 reads X (value = 1)** → Cached in PE1
2. **PE2 reads X (value = 1)** → Cached in PE2
3. **PE1 writes X = 0** → PE1 cache updated
4. Memory may or may not be updated (depends on write policy)
5. PE2 still sees X = 1 (stale data)
6. **Inconsistency**: Same address, different values

### With Write-Through Policy

- PE1 writes X = 0 → Cache and memory updated
- Memory has correct value
- But PE2 cache still has old value (X = 1)
- Coherence still lost

### With Write-Back Policy

- PE1 writes X = 0 → Only cache updated
- Memory still has old value (X = 1)
- PE2 cache still has old value (X = 1)
- Both memory and PE2 incoherent with PE1

### Requirement

- Cache coherence MUST be maintained
- Otherwise parallel programs execute incorrectly
- Get wrong results
- Latest updates must be visible to all processors

---

## 9. Bus Snooping

Common technique for cache coherence in SMP systems.

### What is Bus Snooping?

**Mechanism**:

- Dedicated bus for coherency control: **Snoop bus**
- Sole purpose: Control coherency of cache data
- Separate from memory bus
- Cache controllers communicate through snoop bus

### How It Works

1. Cache controller performs write to address
2. Broadcasts address information on snoop bus
3. All cache controllers listen to snoop bus
4. Controllers check if they have same address cached
5. If yes, take action based on protocol

### Key Feature

- All caches monitor (snoop on) the bus
- Detect writes by other processors
- Take appropriate action to maintain coherence

---

## 10. Write Invalidate Protocol

### Approach

- When write detected, invalidate own copy
- Group of protocols using this approach
- Most common and easiest to implement

### Mechanism

#### On Write by Processor

1. Update own cache
2. Broadcast write address on snoop bus

#### On Receiving Write Broadcast

1. Check if same address in own cache
2. If yes: Mark block as INVALID (clear valid bit)
3. Next access will be miss

### With Write-Through Policy

- Memory always has up-to-date value
- On miss after invalidation: Fetch from memory
- Straightforward implementation

### With Write-Back Policy

**Challenge**:

- Only writing cache has up-to-date value
- Memory has stale value
- On miss after invalidation: Cannot fetch from memory

**Solution: Snoop Read**:

- Cache with invalid block places snoop read request on bus
- Cache controllers listen to snoop read
- Controller with valid up-to-date copy responds
- Supplies data through snoop bus
- More efficient than going to memory
- Avoids slow memory access

### Complexity

**Trade-offs**:

- More complex cache controller
- Snoop bus needs to carry data and addresses
- More hardware required
- Higher power consumption
- But better performance (less memory traffic)

---

## 11. Write Update Protocol

### Alternative Approach

**Concept**:

- Update own copy instead of invalidating
- Also called Write Broadcast
- Different action when write detected

### Mechanism

#### On Write by Processor

1. Update own cache
2. Broadcast BOTH address AND data on snoop bus

#### On Receiving Write Broadcast

1. Check if same address in own cache
2. If yes: Update own copy with new data
3. Keep block VALID

### Benefits

- No miss on next access to same address
- Data already updated in all caches
- Don't need extra read operation
- Simpler cache controller (no snoop read needed)

### Costs

- Snoop bus must carry data (wider bus)
- More hardware on snoop bus
- Higher power consumption
- More bus traffic

### Comparison

- Simpler than write invalidate with write-back
- Fewer cache misses
- Higher bus bandwidth requirement

---

## 12. Real Protocol Implementations

### Historical Protocols

#### Write Once Protocol

- **Type**: Write invalidate
- **Write policy**: Write-through on first write, write-back after
- One of first bus snooping protocols

#### Synapse N+1 Protocol

- **Type**: Write invalidate
- **Write policy**: Write-back
- Early implementation

#### Berkeley Protocol

- **Type**: Write invalidate
- **Write policy**: Write-back
- Used in Berkeley SPUR processor

#### Illinois Protocol (MESI)

- **Type**: Write invalidate
- **Write policy**: Write-back
- Used in SGI Power and Challenge systems
- Very popular, widely adopted

#### Firefly Protocol

- **Type**: Write update
- **Write policy**: Mixed (write-back for private data, write-through for shared data)
- Used in DEC Firefly and Sun SPARC systems

### Most Common Combination

- Write invalidate protocols
- Write-back policy
- Reduces memory accesses (expensive in terms of time)
- Easier to implement than write update
- Good balance of performance and complexity

---

## 13. MESI Protocol Details

Named after four states: **Modified, Exclusive, Shared, Invalid**

Most popular cache coherency protocol, used in Intel Pentium and IBM PowerPC processors.

### Four Block States (Requires 2 Bits)

#### 1. INVALID (I)

- Data not valid
- Block cannot be used
- Must fetch from elsewhere

#### 2. SHARED (S)

- Multiple caches have copies of this block
- All copies have same value
- Value consistent with memory
- Memory has up-to-date value

#### 3. EXCLUSIVE (E)

- Only cached copy in entire system
- No other cache has this block
- Value consistent with memory
- Memory has up-to-date value

#### 4. MODIFIED (M)

- Only cached copy in system
- Value INCONSISTENT with memory
- This cache has most recent value
- Memory has stale value
- Block is "dirty"

---

## 14. MESI Protocol State Transitions

### Example with PE1, PE2, PE3

**Initial State**: Variable X = 1 in memory, all cache entries invalid

#### Step 1: PE1 Reads X

**Actions**:

- Check other caches (snoop read request)
- No other cache has X
- Fetch from memory
- **State transition**: Invalid → Exclusive

**Result**:

- PE1: X = 1 (Exclusive)

#### Step 2: PE3 Reads X

**Actions**:

- Check other caches (snoop read request)
- PE1 responds (has Exclusive copy)
- PE1 supplies data to PE3

**State transitions**:

- PE1: Exclusive → Shared
- PE3: Invalid → Shared

**Result**:

- Both PE1 and PE3: X = 1 (Shared)
- Consistent with memory

#### Step 3: PE3 Writes X = 0

**Actions**:

- Block in PE3 was Shared
- Update local cache
- Broadcast invalidate on snoop bus
- **State transition**: Shared → Modified

**Result**:

- PE3: X = 0 (Modified)
- PE1 receives invalidate:
  - State transition: Shared → Invalid
  - PE1: X = ? (Invalid)
- Memory still has X = 1 (stale)

#### Step 4: PE1 Reads X

**Actions**:

- Block in PE1 is Invalid (tag matches but invalid)
- Place snoop read request on bus
- PE3 has Modified copy (most up-to-date)
- PE3 responds to snoop read:
  - Supplies data to PE1 through snoop bus
  - Writes back to memory
  - State transition: Modified → Shared
- PE1 receives data:
  - State transition: Invalid → Shared

**Result**:

- PE1: X = 0 (Shared)
- PE3: X = 0 (Shared)
- Memory: X = 0 (updated)
- All consistent

### Key Points

- Coherency maintained throughout
- Invalidations prevent stale data reads
- Modified state identifies most recent value
- Snoop reads fetch from other caches efficiently
- Write-backs occur when transitioning from Modified to Shared

---

## 15. Scalability of UMA Systems

### Limitation

**Challenges**:

- Bus snooping doesn't scale well
- Bus contention increases with more processors
- Snoop bus becomes bottleneck
- Memory bus also becomes bottleneck

### Practical Limit

- Up to ~32 processing elements with bus-based design
- Not a hard threshold but approximate practical limit
- Beyond this, contention significantly degrades performance

### Alternative Interconnects

#### Crossbar Switches

- Alternative to bus-based architecture
- Allows multiple simultaneous connections
- Better than simple bus

#### Multi-Stage Crossbar Switch Network

- Multiple crossbar switches in network topology
- Increased parallelism in interconnect
- Can connect multiple memory banks simultaneously
- Increases scalability

### Improved Scalability

- With crossbar networks: Up to ~256 processing elements
- Still limited but much better than bus-based
- Trade-off: More complex hardware

---

## 16. Non-Uniform Memory Access (NUMA)

### Designed for Even Higher Scalability

**Goals**:

- Target: Thousands of processing elements
- Beyond limits of UMA systems
- Still uses shared memory model
- Communication through shared address space

### Key Difference from UMA

**Non-Uniform Access Times**:

- Memory access time DEPENDS on which processor is accessing
- Different processors experience different latencies
- Memory perspective is non-uniform

### Architecture

**Structure**:

- Each processor has local memory
- Faster to access local memory
- Slower to access remote memory (other processors' local memory)
- But all memory accessible by all processors (shared address space)

### Access Time Difference

- Remote memory access: 4-5 times more cycles than local
- Significant performance impact
- Programming must consider locality

### Operating System Role

**Optimization Responsibilities**:

- Must use special algorithms for memory optimization
- Workload distribution affects performance
- Should relocate memory blocks for optimization
- Goal: Maximize local accesses, minimize remote accesses
- Global optimization problem

---

## 17. Two Types of NUMA

### 1. NC-NUMA (Non-Cached NUMA)

**Characteristics**:

- No caches shown in architecture
- Processors directly access memory
- Simpler but slower

### 2. CC-NUMA (Cache-Coherent NUMA)

**Characteristics**:

- Includes caches at each node
- Must maintain cache coherence
- More complex but better performance
- Cannot use bus snooping (not scalable enough)
- Solution: Directory-based coherence

---

## 18. Directory-Based Cache Coherence

Used in CC-NUMA systems for scalable cache coherence.

### What is Directory?

**Definition**:

- Data structure tracking cache contents
- Distributed across system
- Stores information about which blocks are cached where
- Can be in memory or separate hardware

### Purpose

**Functionality**:

- Cache controllers check directory to find block locations
- Determines if other caches have copies of block
- Enables coherence without bus snooping
- Scalable to thousands of processors

### Organization

**Distributed Structure**:

- Directory can be distributed
- Each node has local directory
- Local directory tracks blocks from local memory address range
- Information about which caches have those blocks
- Blocks from other address ranges tracked in other directories

### Operation

**Access Process**:

- Cache controller accesses appropriate directory
- Local directory if accessing local address range
- Remote directory if accessing remote address range
- Directory provides information about block locations
- Can then send invalidations or updates as needed

### Write Policy

- Typically use write-through policy

---

## Key Takeaways

1. Multiprocessors overcome single-processor performance limitations
2. Shared memory provides communication mechanism between processors
3. Cache coherence is essential for correct parallel program execution
4. Bus snooping works well for small-scale systems (up to ~32 processors)
5. MESI protocol is widely adopted for cache coherence
6. UMA systems provide uniform access but limited scalability
7. NUMA systems enable thousands of processors with non-uniform access
8. Directory-based coherence enables scalable cache coherence
9. Operating system plays crucial role in workload balancing and optimization
10. Trade-offs exist between simplicity, performance, and scalability

---

## Summary

Multiprocessor systems have become the standard in modern computing, from smartphones to supercomputers, enabling the parallel processing power required for contemporary applications while managing the complex interactions between multiple processors sharing memory resources.
