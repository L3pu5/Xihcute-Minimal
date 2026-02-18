from enum import Enum, auto
import string

class InstructionType(Enum):
    MULTIPLY = auto()
    ADD = auto()
    DP_POP = auto()
    DP_READ = auto()
    SP_STDOUT = auto()
    DUP = auto()
    LOGICAL_INEQUALITY = auto()
    JUMP_CONDITIONAL = auto()
    SIGNED_NEGATE = auto()
    POP = auto()
    END = auto()

InstructionMapping: dict[str, InstructionType] = {
    "*": InstructionType.MULTIPLY,
    "+": InstructionType.ADD,
    "y": InstructionType.DP_POP,
    "t": InstructionType.DP_READ,
    "o": InstructionType.SP_STDOUT,
    "m": InstructionType.DUP,
    "!": InstructionType.LOGICAL_INEQUALITY,
    "b": InstructionType.JUMP_CONDITIONAL,
    "~": InstructionType.SIGNED_NEGATE,
    "l": InstructionType.POP,
    "e": InstructionType.END
}

InstructionCodes = InstructionMapping.keys()

class VirtualMachine():
    stack: list[int] = None
    source: str = None
    instructionPointer: int  = 0
    dataPointer: int  = 0
    codeMapping: dict[InstructionType, any] = {}
    stepCounter = 0

    def __init__(self):
        self.stack = []
        self.source = ""
        self.instructionPointer = 0
        self.dataPointer = 0
        self.codeMapping = {
            InstructionType.MULTIPLY: self.mul,
            InstructionType.ADD: self.add,
            InstructionType.DP_POP: self.pop_dp,
            InstructionType.DP_READ: self.read_dp,
            InstructionType.SP_STDOUT: self.print_stack,
            InstructionType.DUP: self.dup, 
            InstructionType.LOGICAL_INEQUALITY: self.logical_not,
            InstructionType.JUMP_CONDITIONAL: self.conditional_jump,
            InstructionType.SIGNED_NEGATE: self.neg,
            InstructionType.POP: self.pop,
            InstructionType.END: self.end
        }
    
    def sauce(self, sauce: str):
        self.source = sauce
        self.instructionPointer = 0
        self.dataPointer = 0

    def run(self, debug: bool = True):
        while self.instructionPointer < len(self.source):
            self.step(debug)

    def end(self):
        return 
    
    def step(self, debug=True):
        cursor = self.source[self.instructionPointer]
        if debug == True:
            print("-------------------")
            print(f"IP: {self.instructionPointer} '{cursor}'")
            print(f"DP: {self.dataPointer}")
            print(f"Stacktop: {self.stack[-1] if len(self.stack) > 0 else 'nil'}")
            print(f"Step: {self.stepCounter}")
            print("-------------------")
        if cursor in InstructionCodes:
             operation = InstructionMapping[cursor]
             self.codeMapping[operation]()
        else:
            self.push(cursor)

        self.stepCounter += 1
        self.instructionPointer += 1

    def push_IP(self):
        self.stack.append(self.source[self.instructionPointer])
    
    def pop(self):
        if len(self.stack) == 0:
            exit(1)
            
        return int(self.stack.pop())
    
    def push(self, value):
        if isinstance(value, str):
            if value in string.digits:
                self.stack.append(int(value))
            else:
                self.stack.append(ord(value))
        else:
            self.stack.append(value)

    def neg(self):
        value = self.pop()
        value *= -1
        self.push(value)

    def add(self):
        self.push(self.pop() + self.pop())
    
    def mul(self):
        self.push(self.pop() * self.pop())
    
    def dup(self):
        value = self.pop()
        self.push(value)
        self.push(value)

    def read_dp(self):
        value = self.source[self.dataPointer]
        self.dataPointer += 1
        self.push(value)
    
    def pop_dp(self):
        self.dataPointer = self.pop()

    def conditional_jump(self):
        relativeOffset = self.pop()
        value = self.pop()
        if value != 0:
            self.instructionPointer += relativeOffset
    
    def print_stack(self):
        value = self.pop()
        print(chr(value), end = '')

    def logical_not(self):
        v1 = self.pop()
        v2 = self.pop()
        if v1 != v2:
            self.push(1)
        else:
            self.push(0)

code = "92*1+ytotm0!52*~bleHello, World!\0"
vm: VirtualMachine = VirtualMachine()
vm.sauce(code)
vm.run(debug=False)