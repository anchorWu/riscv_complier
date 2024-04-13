# @Author   : Pyrrho
# @Date     : 27/03/2024
from table import inst_dict, reg_name
import sys


def pre_compile(read_lines):
    """
    预处理：去除注释和空行
    """
    lines = []
    for line in read_lines:
        if line.count('#'):
            line = line[:line.index('#')]  # 切除注释
        line = line.strip()  # 去掉每一行的前后空白
        if line:
            lines.append(line)

    return lines


# 开始进入 original code 处理程序


class OriginalInstructionParser:
    def __init__(self, lines: list):
        """
        参数接收源码，行的数组
        """
        self.label_index = {}  # 保存标签对应指令的序号

        self.splits = self.to_splits(lines)  # 将每个源码行转为参数列表

    def to_splits(self, codes: list) -> list:
        """
        分割字符串，转为指令+参数的列表
        用字典记录标签对应的指令，不再保留标签
        """
        splits = []
        index = 0
        for line in codes:
            if line == 'nop':
                line = 'addi x0, x0, 0'
            elif line[0:2] == 'j ':
                line = 'jal x0' + line[1:]
            if line[0] != '.':  # 不是标签，添加到列表
                split = split_param(line)
                splits.append(split)
                index += 0
            else:  # 是标签，记录到字典
                label = line[:line.index(':')]
                self.label_index[label] = index  # 字典的键是标签名，值是指令的序号
        return splits

    def parse(self) -> list:
        """
        转为 basic code ：根据字典，替换掉引用了标签的参数
        """
        for split in self.splits:
            for i in range(len(split)):
                param = split[i]
                if param[0] == '.':
                    split[i] = 4 * (self.label_index[param] - i)
                    print(split[i])
        return self.splits


# original code 处理程序结束

# 以下开始为 basic code 处理程序

def split_param(instruction: str) -> list:
    """
    将一条指令字符串，分割为指令名和参数的列表
    """
    splits = []
    for s in instruction.split(','):
        s = s.strip()
        for t in s.split():  # 不传参，用空格分隔
            t = t.strip()
            if t.count('('):
                splits.append(t[t.index('(') + 1:t.index(')')])  # 括号里面的
                splits.append(t[:t.index('(')])  # 括号左边的
            else:
                splits.append(t)

    return splits


class BasicInstruction:
    """
    父类，包含功能性的方法
    """

    def __init__(self, opcode):
        self.opcode = opcode

    @staticmethod
    def to_int(num: str) -> int:
        """
        字符串转数字。能识别 0x 开头
        """
        try:
            return int(num)
        except ValueError:  # 本程序仅出现0x开头的用例
            return int(num, 16)

    @staticmethod
    def bin_bits(num: int, n) -> list:
        """
        list的第i个元素, 就是imm[i]对应的位置
        注意元素类型为str，而不是int
        """
        bin_bit = 1
        bin_ext = []
        for i in range(n):
            # 从右边最低位向左边最高位依次逐位AND，这样把二进制数倒过来（变成LSB在最左边的一个数组）
            bin_ext.append('1' if num & bin_bit else '0')
            bin_bit <<= 1
        return bin_ext

    @staticmethod
    def bin_cut(bin_bits: list, left, right) -> str:
        """
        切割 二进制位组成的数组，获取其中特定的区间
        """
        if right != 0:
            return ''.join(bin_bits[left:right - 1:-1])  # 左闭右开区间，步长-1代表从右向左！
        else:
            return ''.join(bin_bits[left::-1])  # 从left开始取到最左边

    def parse_bin(self) -> str:
        """
        将 basic instruction 转为 32 位二进制
        """
        pass

    def parse_hex(self):
        """
        将 basic instruction 转为 8 位十六进制
        """
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
        self.imm = self.bin_bits(self.to_int(imm), 12)
        self.funct3 = funct3

    def parse_bin(self):
        # 构建每一部分
        return self.bin_cut(self.imm, 11, 0) \
            + reg_name(self.rs1) \
            + self.funct3 \
            + reg_name(self.rd) \
            + self.opcode  # 32位二进制


class STypeInstruction(BasicInstruction):  # 交换rs1和rs2
    def __init__(self, rs1, rs2, imm, opcode, funct3):
        super().__init__(opcode)
        self.rs1 = rs2
        self.rs2 = rs1
        self.imm = self.bin_bits(self.to_int(imm), 12)
        self.funct3 = funct3

    def parse_bin(self):
        # 处理参数
        return self.bin_cut(self.imm, 11, 5) \
            + reg_name(self.rs2) \
            + reg_name(self.rs1) \
            + self.funct3 \
            + self.bin_cut(self.imm, 4, 0) \
            + self.opcode  # 32位二进制


class SBTypeInstruction(BasicInstruction):
    def __init__(self, rs1, rs2, imm, opcode, funct3):
        super().__init__(opcode)
        self.rs1 = rs1
        self.rs2 = rs2
        self.imm = self.bin_bits(self.to_int(imm), 13)
        self.funct3 = funct3

    def parse_bin(self):
        # 处理参数
        return self.imm[12] \
            + self.bin_cut(self.imm, 10, 5) \
            + reg_name(self.rs2) \
            + reg_name(self.rs1) \
            + self.funct3 \
            + self.bin_cut(self.imm, 4, 1) \
            + self.imm[11] \
            + self.opcode  # 32位二进制


class UTypeInstruction(BasicInstruction):
    def __init__(self, rd, imm, opcode):
        super().__init__(opcode)

    def parse_bin(self):
        # 暂未实现
        pass


class UJTypeInstruction(BasicInstruction):
    def __init__(self, rd, imm, opcode):
        super().__init__(opcode)
        self.rd = rd
        self.imm = self.bin_bits(self.to_int(imm), 21)

    def parse_bin(self):
        return self.imm[20] \
            + self.bin_cut(self.imm, 10, 1) \
            + self.imm[11] \
            + self.bin_cut(self.imm, 19, 12) \
            + reg_name(self.rd) \
            + self.opcode  # 32位二进制


basic_parsers = {
    'R': RTypeInstruction,
    'I': ITypeInstruction,
    'S': STypeInstruction,
    'SB': SBTypeInstruction,
    'U': UTypeInstruction,
    'UJ': UJTypeInstruction,
}


def parse_single_basic(inst, *args):  # *意为不定数量参数
    """
    解析单个指令
    返回一行机器指令
    """

    # 根据 inst 确定：类型、opcode、funct3、funct7
    d = inst_dict(inst)  # 获取指令的类型说明
    fmt = d.pop('fmt')
    parser_cls = basic_parsers[fmt]

    red = {key: value for key, value in d.items() if value}  # 去除不需要的 key
    del red['mnemonic']  # 也不需要

    return parser_cls(*args, **red)  # *args：把数组拆开成几个元素, **red：把字典拆开，按照键名对应进行传参


# original code 处理程序结束

def comma(lines):
    # 每行末尾加逗号
    for i in range(len(lines)):
        if i + 1 == len(lines) or lines[i + 1] == '':
            # 最后一行末尾加分号
            lines[i] += ';'
            break
        else:
            lines[i] += ','


# 以下均为测试程序


def test_single_basic():
    """
    测试单个 basic instruction
    """
    bas = 'beq x24 x19 8'
    splits = split_param(bas)
    parse_result = parse_single_basic(*splits)
    print(parse_result)

    bas = 'beq x24 x19 8'
    # bas = 'sw t0, 2(a1)'

    # parse_result = parse_single_instruction('addi', 'a1', 'a0', '4')
    # splits = split_param(bas)

    # parse_result = parse_single_instruction(*splits)
    # parse_result = parse_single_instruction('sw', 'a1', 't0', '1')


def test_original_file(file_name):
    """
    总体测试
    """
    with open(file_name, 'r', encoding='UTF8') as rf:
        read_lines = rf.readlines()

    original_lines = pre_compile(read_lines)
    # 转化为 basic code
    basic_list = OriginalInstructionParser(original_lines).parse()

    # 逐个指令解析
    result_list = []
    for basic in basic_list:
        basic_instruction = parse_single_basic(*basic)
        result_list.append(basic_instruction.__str__())

    comma(result_list)

    # 打印到输出文件
    # 前两行添加
    line1 = 'memory_initialization_radix=16;'
    line2 = 'memory_initialization_vector='

    # 将修改后的内容写回文件
    with open(file_name.split('.')[0] + '.coe', 'w', encoding='UTF8') as f:
        f.write(line1 + '\n')
        f.write(line2 + '\n')
        f.writelines('\n'.join(result_list))


if __name__ == '__main__':
    # 测试单条指令
    # test_single_basic()

    # 测试文件编译
    test_original_file(sys.argv[1])
