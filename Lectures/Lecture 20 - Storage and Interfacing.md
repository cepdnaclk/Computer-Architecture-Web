# Lecture 20: Storage and Input/Output Systems

## Introduction

This lecture completes our exploration of computer architecture by examining storage devices and input/output (I/O) systems that enable computers to interact with external devices and provide persistent data storage beyond volatile main memory. We explore storage technologies from mechanical magnetic disks to solid-state flash memory, understanding their performance characteristics, reliability metrics, and cost tradeoffs. The lecture covers I/O communication methods including polling, interrupts, and direct memory access (DMA), analyzes RAID configurations that improve both performance and dependability, and examines how storage systems connect to processors through memory-mapped I/O or dedicated I/O instructions. Understanding these peripheral systems reveals how complete computer systems integrate computation, memory, and external interaction into cohesive platforms.

---

## 1. Introduction to I/O Devices and Storage

Chapter 6 covers storage devices and input/output systems that enable computers to interact with external devices and persistent storage.

---

## 2. I/O Device Characteristics

I/O devices can be characterized by three fundamental factors:

### 1. Behavior

**Input Devices**:

- Provide data to system
- Examples: keyboards, mice, sensors

**Output Devices**:

- Receive data from system
- Examples: displays, printers, speakers

**Storage Devices**:

- Store and retrieve data
- Examples: disks, flash drives

### 2. Partner

**Human Devices**:

- Communicate with humans
- Examples: keyboards, displays, audio

**Machine Devices**:

- Communicate with other machines
- Examples: networks, controllers

### 3. Data Rate

- Measured in bytes per second or transfers per second
- Wide variation across device types
- Affects system design and communication methods

---

## 3. I/O Bus Connections

### Simplified System Architecture

#### Components

- **Processor (CPU)**
- **Cache**
- **Memory I/O Interconnect (Bus)**
- **Main Memory**
- **Multiple I/O Controllers**
- **Various I/O Devices**

#### Bus Structure

- Processor and cache connected to bus
- Main memory connected to bus
- I/O controllers connected to bus
- Each controller manages specific devices

#### Connections

- Processor receives interrupts from bus/devices
- **I/O Controller 1**: Connected to disk
- **I/O Controller 2**: Connected to graphic output
- **I/O Controller 3**: Connected to network channel

Multiple controllers allow parallel device operation while sharing common interconnect.

---

## 4. Dependability

Critical for I/O systems, especially storage devices.

### Why Dependability Matters

- Storage devices hold data that must be reliable
- Users depend on devices being available
- Data loss is unacceptable
- Systems must continue functioning despite component failures

### Dependability is Particularly Important For

- Storage devices (data integrity)
- Critical systems (servers, embedded systems)
- Systems with high availability requirements

---

## 5. Service States

### Two Primary States

#### 1. Service Accomplishment State

- Device is working correctly
- Providing expected service
- Normal operational state

#### 2. Service Interruption State

- Device has failed
- Not providing service
- Requires repair/restoration

### State Transitions

- **From Service Accomplishment to Service Interruption**: Due to failure
- **From Service Interruption to Service Accomplishment**: After restoration/repair

---

## 6. Fault Terminology

### Fault Definition

**Characteristics**:

- Failure of a component
- May or may not affect the system
- May or may not lead to system failure
- System can continue running with faulty component
- May produce correct or wrong output

### Distinction

- **Component failure ≠ System failure**
- Fault tolerance allows operation despite faults

---

## 7. Dependability Measures

### Key Metrics

#### 1. MTTF (Mean Time To Failure)

**Definition**:

- Reliability measure
- Average time device operates before failing
- Measures how long system stays in Service Accomplishment state
- Higher MTTF = more reliable

#### 2. MTTR (Mean Time To Repair)

**Definition**:

- Service interruption measure
- Average time to restore service after failure
- How long device stays in Service Interruption state
- Lower MTTR = faster recovery

#### 3. MTBF (Mean Time Between Failures)

**Formula**:

```
MTBF = MTTF + MTTR
```

**Definition**:

- Complete cycle: operation + repair
- Time from one failure to next failure
- Includes both operational and repair time

#### 4. Availability

**Formula**:

```
Availability = MTTF / (MTTF + MTTR)
```

**Definition**:

- Proportion of time machine is available
- Ratio of operational time to total time
- Expressed as percentage or decimal

---

## 8. Improving Availability

### Two Approaches

---

## 9. 1. Increase MTTF (Mean Time To Failure)

#### a) Fault Avoidance

**Methods**:

- Prevent faults before they occur
- Better design and manufacturing
- Quality components
- Proper operating conditions

#### b) Fault Tolerance

**Methods**:

- Design system to withstand faults
- Redundancy (duplicate components)
- Error correction mechanisms
- Graceful degradation

#### c) Fault Forecasting

**Methods**:

- Predict when faults will occur
- Preventive maintenance
- Monitor component health
- Replace before failure

---

## 10. 2. Reduce MTTR (Mean Time To Repair)

### Methods

- Improve tools and processes for diagnosis
- Better diagnostic capabilities
- Easier repair procedures
- Quick replacement mechanisms
- Automated recovery systems
- Skilled maintenance personnel

### Example Problems

- Book provides examples with specific MTTF and MTTR values
- Calculate availability
- Analyze improvement strategies
- Students should practice these calculations

---

## 11. Magnetic Disk Storage

Traditional secondary storage technology using magnetic recording.

### Physical Structure

#### Disk Shape

- Circular/round shape
- Platter rotates on spindle

#### Tracks

- Concentric circles on disk surface
- From periphery (outer edge) to center
- Multiple tracks like ribbons arranged concentrically
- Similar to running tracks in sports (Olympics)

#### Sectors

- Tracks divided by radial lines (from center to periphery)
- Cross-sectional cuts across tracks
- Portion between two separation lines = one sector
- Smallest addressable unit on disk

### Sector Contents

- **Sector ID** (identification)
- **Data** (512 bytes to 4096 bytes typical)
- **Error Correcting Code (ECC)**
  - Hides defects
  - Corrects recording errors
- **Gaps** between sectors (unused spaces)

---

## 12. Disk Access Process

### Access Components and Timing

#### 1. Queuing Delay

- If other accesses are pending
- Wait for previous operations to complete
- Managed by disk controller

#### 2. Seek Time

- Moving head to correct track
- Head positioned on right sector
- Physical movement of read/write head
- Head placed diagonally on disc
- Time to "seek" the target sector
- Typically several milliseconds

#### 3. Rotational Latency

- Rotating disk to position correct sector under head
- Disk spins to align sector with head
- Choose closest direction (shortest rotation)
- Sectors arranged diagonally on disk
- Multiple sectors per track
- Can rotate either direction (clockwise or counterclockwise)

#### 4. Transfer Time

- Actual data read/write
- Depends on sector size and transfer rate
- Usually small compared to seek and rotation

#### 5. Controller Overhead

- Processing by disk controller
- Command interpretation
- Error checking
- Generally small (fraction of millisecond)

### Access Coordination

- Processor initiates access
- Memory Management Unit (MMU) handles translation
- Involves both hardware and operating system
- Reading page from disk to memory: millions of cycles
- Much slower than memory access

---

## 13. Disk Access Example Calculation

### Given Parameters

- **Sector size**: 512 bytes
- **Rotational speed**: 15,000 RPM (rotations per minute)
- **Seek time**: 4 milliseconds
- **Transfer rate**: 100 MB/s
- **Controller overhead**: 0.2 milliseconds
- Assume idle disk (no queuing)

### Average Read Time Calculation

#### 1. Seek Time

4 ms (given)

#### 2. Rotational Latency

- Average = Half rotation time
- Full rotation = 60 seconds / 15,000 RPM = 4 ms
- Average = 4 ms / 2 = **2 ms**
- Why half? Can choose closest direction

#### 3. Transfer Time

- Size / Rate = 512 bytes / 100 MB/s
- = **0.005 ms**

#### 4. Controller Delay

0.2 ms (given)

### Total Average Read Time

```
Total = 4 + 2 + 0.005 + 0.2 = 6.2 milliseconds
```

### Real Case Variation

- Actual average seek time might be 1 ms (not 4 ms)
- Depends on:
  - Which sector being accessed
  - Current head position
  - Distance head must travel
- With 1 ms seek: Total = **3.2 ms**
- Significant variation based on access patterns

### Additional Examples

- Book provides more practice problems
- Students should try different scenarios
- Understand impact of each component on total time

---

## 14. Flash Storage

Modern non-volatile semiconductor storage technology.

### Characteristics

#### Advantages

- Non-volatile (retains data without power)
- 1000x faster than magnetic disk
- Smaller physical size
- Lower power consumption
- More robust (no moving parts)
- Can be carried around easily
- Shock resistant

#### Disadvantages

- More expensive than magnetic disk
- Limited write cycles (wears out over time)
- Technology cost higher

---

## 15. Types of Flash Storage

### 1. NOR Flash

#### Structure

- Bit cell like NOR gate
- Random read/write access
- Can access individual bytes

#### Characteristics

- Byte-level access
- Faster read access
- More expensive

#### Applications

- Instruction memory in embedded systems
- Code storage
- Execute-in-place applications

### 2. NAND Flash

#### Structure

- Bit cell like NAND gate
- Block-at-a-time access
- Cannot access individual bytes directly

#### Characteristics

- Denser (more storage per area)
- Block-level access
- Reading and writing done in blocks
- Cheaper per GB

#### Applications

- USB keys/drives
- Media storage (photos, videos)
- Solid-state drives (SSDs)
- Memory cards

**Note**: Values in lecture slides may be outdated as flash storage technology rapidly evolves.

---

## 16. Memory-Mapped I/O

Method of accessing I/O devices using memory addresses.

### Concept

- Reserve some address space for I/O devices
- I/O device registers appear as memory locations
- Same address space as memory
- Address decoder distinguishes between memory and I/O

### Example with 8 Address Lines

- **Total addressable locations**: 256 (2^8)
- **Reserve 128 locations for memory**
- **Reserve 128 locations for I/O devices**
- Same load/store instructions access both

### Access Mechanism

- Use load/store instructions for both memory and I/O
- Operating system controls access
- Uses address translation mechanism
- Can make I/O addresses accessible only to kernel
- Protection mechanism prevents user programs from direct access

### Advantages

- Unified programming model
- Same instructions for memory and I/O
- Simpler instruction set

### Disadvantages

- Reduces available memory address space
- Must reserve addresses for I/O

---

## 17. I/O Instructions

Alternative to memory-mapped I/O: separate I/O instructions.

### Characteristics

- Separate instructions specifically for I/O operations
- Distinct from load/store (memory) instructions
- Can duplicate addresses:
  - Same address can refer to memory location
  - Same address can refer to I/O device
  - Instruction type determines which is accessed

### Access Control

- I/O instructions can only execute in kernel mode
- User programs cannot directly access I/O
- Protection mechanism
- Operating system mediates I/O access

### Example Architecture

- **x86 (Intel/AMD processors)**
- Has special IN and OUT instructions for I/O
- Separate I/O address space

### Advantages

- Full memory address space available
- No address space conflict
- Clear distinction between memory and I/O

### Disadvantages

- More complex instruction set
- Additional instructions needed

---

## 18. Polling

Method for processor to communicate with I/O devices.

### How Polling Works

#### 1. Periodically Check I/O Status Register

- Processor repeatedly reads device status
- Check if device is ready
- Continuous monitoring in loop

#### 2. If Device Ready

- Perform requested operation
- Read data or write data
- Continue with next task

#### 3. If Error Detected

- Take appropriate action
- Error handling
- Retry or report error

### Characteristics

#### When Used

- Small or low-performance systems
- Real-time embedded systems
- Simple applications

#### Advantages

**Predictable Timing**:

- Know exactly when device checked
- Deterministic behavior
- Important for real-time systems

**Low Hardware Cost**:

- Software handles communication
- No additional hardware needed
- Simple implementation

#### Disadvantages

**Wastes CPU Time**:

- CPU continuously loops checking device
- Can't do other work while polling
- Inefficient for high-performance systems

**Not Suitable for Complex Systems**:

- Multiple devices difficult to manage
- CPU time wasted on idle devices

### Programming Model

- Can write program to:
  - Read status bit from device
  - Check if device free
  - Make decisions based on status
- Simple control flow

---

## 19. Interrupts

Alternative to polling: device-initiated communication.

### How Interrupts Work

#### 1. Device Initialization

- Device sends signal/request to processor
- Request for service
- Happens when device ready or error occurs

#### 2. Controller Interrupts CPU

- Device controller signals processor
- Processor stops current work
- Handles interrupt

#### 3. Handler Execution

- Special interrupt handler routine runs
- Services device request
- Returns to original program

### Characteristics

#### Asynchronous

- Not synchronized to instruction execution
- Unlike exceptions (which are synchronous)
- Can occur between any two instructions
- Handler invoked between instructions

#### Fast Identification

- Interrupt often identifies device
- Know which device needs service
- Can be handled quickly

#### Priority System

- Not all devices have same urgency
- Devices categorized by priority levels
- Devices needing urgent attention get higher priority
- High-priority interrupts can preempt low-priority handlers

### Advantages

**Efficient CPU Use**:

- No wasted time polling
- CPU does other work until interrupt

**Good for Multiple Devices**:

- Each device interrupts when ready
- No continuous checking needed

**Responsive**:

- Quick response to device events

### Disadvantages

**More Complex Hardware**:

- Interrupt controller needed
- Priority management

**Context Switching Overhead**:

- Save/restore processor state
- Handler invocation takes time

### Execution Model

- Main program running
- Instruction completes
- Interrupt checked
- If interrupt pending:
  - Current state saved
  - Interrupt handler runs
  - State restored
  - Resume main program at next instruction

---

## 20. I/O Data Transfer Methods

Three approaches for transferring data between memory and I/O:

---

## 21. 1. Polling-Driven I/O

### Process

- CPU polls device repeatedly
- When ready, CPU transfers data
- CPU moves data between memory and I/O registers

### Issues

- Time consuming
- CPU fully involved in transfer
- Inefficient for high-speed devices
- Wastes CPU cycles

---

## 22. 2. Interrupt-Driven I/O

### Process

- Device interrupts when ready
- CPU services interrupt
- CPU transfers data between memory and I/O registers

### Issues

- Still CPU-intensive for data transfer
- CPU must move every byte
- Better than polling but still inefficient for bulk transfers

---

## 23. 3. Direct Memory Access (DMA)

### Process

**Setup**:

- DMA controller handles transfer
- Removes CPU from data movement
- Processor hands off transfer job to DMA controller
- DMA controller transfers data autonomously

### DMA Operation

**CPU Provides**:

- Starting address in memory
- Transfer size
- Direction (memory→device or device→memory)

**DMA Controller**:

- Transfers data independently
- Operates in parallel with CPU
- No CPU intervention during transfer

**Controller Interrupts CPU On**:

- Completion of transfer
- Error occurrence

### Advantages

- CPU free to do other work
- Efficient bulk data transfers
- Essential for high-speed devices
- Reduces CPU overhead significantly

### When Used

- High-speed devices (disks, network)
- Large data transfers
- When CPU time is valuable

### Comparison

- **Polling**: Simple, predictable, inefficient
- **Interrupts**: Responsive, better than polling, CPU still involved in transfer
- **DMA**: Most efficient, essential for high-performance I/O

---

## 24. RAID (Redundant Array of Independent Disks)

Technology to improve storage performance and dependability.

### Purpose

- Improve performance through parallelism
- Improve dependability through redundancy
- Use multiple disks together as single logical unit

### Benefits

#### Performance Improvement

- Parallel access to multiple disks
- Higher throughput
- Faster data access

#### Dependability Improvement

- Redundancy protects against disk failure
- Data not lost if one disk fails
- Improved reliability

**Note**: Lecture mentions RAID but doesn't go into detailed levels or configurations. This is a complex topic covered more thoroughly in other courses.

---

## 25. Conclusion and Summary

### I/O System Performance Measures

- **Throughput**: Amount of data transferred per unit time
- **Response time**: Time from request to completion
- **Dependability**: Reliability and availability
- **Cost**: Important consideration in system design

---

## 26. Key Points

### System Architecture

- Buses connect CPU, memory, and I/O controllers
- Multiple controllers manage different device types
- Shared interconnect with arbitration

### Communication Mechanisms

- **Polling**: Simple, predictable, inefficient
- **Interrupts**: Responsive, efficient CPU use
- **DMA**: Most efficient for bulk transfers

### Dependability

- Critical for storage systems
- Measured by MTTF, MTTR, MTBF, availability
- Improved through fault tolerance and faster repair

### Storage Technologies

- **Magnetic disk**: Traditional, slower, cheaper per GB, mechanical
- **Flash storage**: Modern, faster, more expensive, no moving parts

### Access Methods

- **Memory-mapped I/O**: I/O uses memory address space
- **I/O instructions**: Separate instruction set for I/O

### Performance Optimization

- **RAID**: Improve performance and dependability
- **DMA**: Reduce CPU overhead
- **Interrupts**: Improve responsiveness

### Exercises

- Book contains practice problems
- Calculate dependability metrics
- Analyze disk access times
- Compare different I/O mechanisms

---

## Key Takeaways

1. I/O systems connect computers to external devices and storage
2. Dependability is critical for storage systems
3. MTTF, MTTR, and availability are key metrics
4. Magnetic disks use mechanical components with millisecond access times
5. Flash storage is faster but more expensive than magnetic storage
6. Memory-mapped I/O and separate I/O instructions are two access methods
7. Polling is simple but inefficient
8. Interrupts improve CPU efficiency
9. DMA is essential for high-speed bulk data transfers
10. RAID improves both performance and reliability

---

## Summary

This concludes the processor and memory sections of the course, covering the complete spectrum from CPU design through memory hierarchy to I/O systems. We have explored how computers are designed from the ground up, from basic arithmetic operations through pipelined execution, memory hierarchies, multiprocessor systems, and finally to storage and I/O mechanisms that enable computers to interact with the external world.
