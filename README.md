# RISC-V Core Simulator

## Overview
This project is a software-based simulator for the RISC-V 32-bit Integer (RV32I) instruction set architecture (ISA). Developed in Python, it models the internal workings of a processor, including the datapath, control unit, register file, and memory hierarchy.

The simulator accepts binary machine code as input, executes the instructions by emulating the hardware logic, and generates a detailed trace of the processor's state (Program Counter, Registers, and Data Memory) after every cycle.

## Computer Organization Principles
This project demonstrates a practical application of key Computer Organization and Architecture concepts:

### 1. The Von Neumann Architecture
- **Stored Program Concept**: The simulator treats instructions and data as distinct entities residing in memory (abstracted as input lists and a hash map, respectively), adhering to the principle that programs are stored in memory to be executed.
- **Fetch-Decode-Execute Cycle**: The core loop of the simulator models the fundamental lifecycle of a CPU instruction:
  - **Fetch**: Retrieving the 32-bit binary instruction.
  - **Decode**: Parsing the opcode, function fields (funct3/funct7), and operands.
  - **Execute**: Performing ALU operations or memory access.

### 2. Instruction Set Architecture (ISA) Design
- **RISC Philosophy**: Implements a Reduced Instruction Set Computer (RISC) architecture, focusing on a small set of highly optimized instructions and a Load/Store memory model.
- **Instruction Formats**: The code implements the decoding logic for standard RISC-V formats (**R, I, S, B, J**), demonstrating how binary bit-fields map to hardware control signals.

### 3. Processor Datapath & State Management
- **Register File**: Simulates a bank of 32 general-purpose registers (`x0`-`x31`), enforcing hardware constraints such as `x0` always being zero.
- **ALU Operations**: Software emulation of the Arithmetic Logic Unit, handling bitwise operations (`AND`, `OR`), arithmetic (`ADD`, `SUB`), and comparisons.
- **Program Counter (PC)**: Manages the execution flow, including sequential execution and non-linear control flow (branching and jumping).

### 4. Memory Hierarchy & Addressing
- **Byte-Addressable Memory**: Simulates Data Memory using a dictionary structure to handle sparse addressing, mimicking the behavior of RAM.
- **Endianness & Binary Representation**: Handles 2's complement representation for signed integers and immediate values, ensuring accurate binary arithmetic simulation.

## Technical Implementation

### File Structure
- `simulator.py`: The main processor logic. It contains the instruction decoder (`slicing` function), execution units for each instruction type, and the main execution loop.
- `sim2.py`: An extended version of the simulator with enhanced control flow handling and label management.

### How It Works
1. **Initialization**: The simulator initializes the PC to 0, the Register File (array of 32 integers) to 0, and allocates Data Memory.
2. **Binary Decoding**: Incoming 32-bit binary strings are sliced to extract the **Opcode** (7 bits). Based on the opcode, the decoder identifies the instruction type and extracts relevant fields (`rs1`, `rs2`, `rd`, `immediate`).
3. **Execution Units**:
   - **R-Type**: Performs register-to-register ALU operations.
   - **I-Type**: Handles immediates and loads (`lw`).
   - **S-Type**: Handles stores (`sw`) to the memory dictionary.
   - **B/J-Type**: Calculates target addresses and updates the PC for control flow.
4. **Trace Generation**: After every instruction, the simulator dumps the binary state of the PC and all 32 registers to an output file, allowing for cycle-accurate debugging.

## Installation

```bash
git clone https://github.com/yourusername/riscv-simulator.git
cd riscv-simulator
```

## Usage

### Requirements
- Python 3.6+

### Execution
1. **Prepare Input**: Create a file named `input.txt` containing 32-bit binary instructions (one per line).
2. **Execute**:
   ```bash
   python simulator.py
   ```
   *(Note: Input/Output filenames can be modified in the script variables `filename` and `output`)*
3. **View Results**: Check `output.txt` for the execution trace and memory dump.

### Input Format
Raw 32-bit binary strings. Comments can be added with `#`.
```text
00000000010100000000000010010011  # addi x1, x0, 5
00000000000100001000000010110011  # add x1, x1, x1
```

## Output Format
The output file records the state after each instruction execution.

**Trace Format:**
```text
0b<PC> 0b<x0> 0b<x1> ... 0b<x31>
```

**Memory Dump:**
At the end of execution, the non-zero Data Memory contents are appended:
```text
0x<Address>:0b<Value>
```
