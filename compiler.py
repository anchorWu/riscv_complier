# @Author   : Pyrrho
# @Date     : 27/03/2024
from table import inst_dict, reg_name


class BasicInstruction:
    def __init__(self, opcode):
        self.opcode = opcode

    @staticmethod
    def bin_bits(num, n) -> list: 
        """
        list的第i个元素, 就是imm[i]对应的位置
        """
        bin_bit = 1
        bin_ext = []
        for i in range(n):
            bin_ext.append('1' if num & bin_bit else '0')  # 从右边最低位向左边最高位依次逐位AND，这样把二进制数倒过来（变成LSB在最左边的一个数组）
            bin_bit <<= 1
        return bin_ext

    @staticmethod
    def bin_cut(bin_bits: list, left, right) -> str:
        if right != 0:
            return ''.join(bin_bits[left:right-1:-1]) #左闭右开区间，步长-1代表从右向左！
        else:
            return ''.join(bin_bits[left::-1]) #从left开始取到最左边

    def parse_bin(self) -> str:
        pass

    def parse_hex(self):
        return hex(int(self.parse_bin(), 2))[2:].zfill(8)

    def __str__(self):
        return self.parse_hex()


class RTypeInstruction(BasicInstruction):
    def __init__(self, rd, rs1, rs2, opcode, funct3, funct7):
        super().__init__(opcode)
        self.funct3 = funct3
        self.funct7 = funct7
        self.rd = rd
        self.rs1 = rs1
        self.rs2 = rs2

    def parse_bin(self):
        # 构建每一部分
        return self.funct7 \
            + reg_name(self.rs2) \
            + reg_name(self.rs1) \
            + self.funct3 \
            + reg_name(self.rd) \
            + self.opcode  # 32位二进制


class ITypeInstruction(BasicInstruction):
    def __init__(self, rd, rs1, imm, opcode, funct3):
        super().__init__(opcode)
        self.rd = rd
        self.rs1 = rs1
        self.imm = self.bin_bits(int(imm), 12)
        self.funct3 = funct3

    def parse_bin(self):
        # 构建每一部分
        return self.bin_cut(self.imm, 11, 0) \
            + reg_name(self.rs1) \
            + self.funct3 \
            + reg_name(self.rd) \
            + self.opcode  # 32位二进制


class STypeInstruction(BasicInstruction):
    def __init__(self, rs1, rs2, imm, opcode, funct3):
        super().__init__(opcode)
        self.rs1 = rs1
        self.rs2 = rs2
        self.imm = self.bin_bits(int(imm), 12)
        self.funct3 = funct3

    def parse_bin(self):
        # 处理参数
        return self.bin_cut(self.imm, 11, 5) \
            + reg_name(self.rs2) \
            + reg_name(self.rs1) \
            + self.funct3 \
            + self.bin_cut(self.imm, 4, 0) \
            + self.opcode   # 32位二进制


class SBTypeInstruction(BasicInstruction):
    def __init__(self, opcode, funct3):
        super().__init__(opcode)
        self.funct3 = funct3

    def parse(self):
        # 处理参数
        code = 0
        return f'{code:x}'  # 32位二进制


class UTypeInstruction(BasicInstruction):
    def __init__(self, opcode):
        super().__init__(opcode)

    def parse(self):
        # 处理参数
        code = 0
        return f'{code:x}'  # 32位二进制


class UJTypeInstruction(BasicInstruction):
    def __init__(self, opcode):
        super().__init__(opcode)

    def parse(self):
        # 处理参数
        code = 0
        return f'{code:x}'  # 32位二进制


parsers = {
    'R': RTypeInstruction,
    'I': ITypeInstruction,
    'S': STypeInstruction,
    'SB': SBTypeInstruction,
    'U': UTypeInstruction,
    'UJ': UJTypeInstruction,
}


class BasicInstructionParser:
    def __init__(self, inst, *args):
        self.inst = inst  # 指令名
        self.paras = args  # 参数
        self.para_num = len(args)  # 参数个数


def parse_single_instruction(inst, *args):  # *意为不定数量
    """
    解析单个指令
    返回一行机器指令
    """

    # 根据 inst 确定：类型、opcode、funct3、funct7
    d = inst_dict(inst)  # 获取指令的类型说明
    fmt = d.pop('fmt')
    parser_cls = parsers[fmt]

    red = {key: value for key, value in d.items() if value}  # 去除无效键
    del red['mnemonic']  # 不需要
    return parser_cls(*args, **red)  # *args：把数组拆开成几个元素, **red：把字典拆开，按照键名对应进行传参


class OriginalInstructionParser:
    pass


if __name__ == '__main__':
    # 逐个指令解析
    # with open('file', 'r', encoding='UTF8') as rf:
    #     for line in rf.readlines():
    #         line = line[:line.index('#')]  # 切除注释
    #         args = line.split(',')

    # parse_result = parse_single_instruction('addi', 'a1', 'a0', '4')
    # parse_result = parse_single_instruction('add', 's8', 'zero', 's9')
    # parse_result = parse_single_instruction('lw', 't0', 'a1', '0')
    parse_result = parse_single_instruction('sw', 'a1', 't0', '1')
    print(parse_result)
