# @Author   : Pyrrho
# @Date     : 27/03/2024
from table import inst_dict, reg_name
import sys

class BasicInstruction:
    def __init__(self, opcode):
        self.opcode = opcode

    @staticmethod
    def to_int(num) -> int:
        try:
            return int(num)
        except ValueError:
            return int(num, 16)

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
            return ''.join(bin_bits[left:right - 1:-1])  # 左闭右开区间，步长-1代表从右向左！
        else:
            return ''.join(bin_bits[left::-1])  # 从left开始取到最左边

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
        self.imm = self.bin_bits(self.to_int(imm), 12)
        self.funct3 = funct3

    def parse_bin(self):
        # 构建每一部分
        return self.bin_cut(self.imm, 11, 0) \
            + reg_name(self.rs1) \
            + self.funct3 \
            + reg_name(self.rd) \
            + self.opcode  # 32位二进制


class STypeInstruction(BasicInstruction): #交换rs1和rs2
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

    def parse(self):
        # 处理参数
        code = 0
        return f'{code:x}'  # 32位二进制


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


def split_param(basic) -> list:
    if basic.count('#'):
        basic = basic[:basic.index('#')]  # 切除注释

    splits = []
    for s in basic.split(','):
        s = s.strip()
        for t in s.split(): #不传参，用空格分隔
            t = t.strip()
            if t.count('('):
                splits.append(t[t.index('(') + 1:t.index(')')])  # 括号里面的
                splits.append(t[:t.index('(')])  # 括号左边的
            else:
                splits.append(t)

    return splits


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

def test_single_basic():
    bas = 'beq x24 x19 8'
    splits = split_param(bas)
    parse_result = parse_single_instruction(*splits)
    print(parse_result)

if __name__ == '__main__':
    # test_single_basic()

    file_name = sys.argv[1]
    # 逐个指令解析
    result_list = []
    with open(file_name, 'r', encoding='UTF8') as rf:
        lines = rf.readlines()   

    lines = [line.strip() for line in lines] #去掉每一行的前后空白

    for line in lines:
        if line == '' or line[0] == '.' or line[0] == '#': #去掉空行和标签
            continue
        splits = split_param(line)
        # print(line)
        line_result = parse_single_instruction(*splits)
        result_list.append(line_result.__str__())

    bas = 'beq x24 x19 8'
    # bas = 'sw t0, 2(a1)'

    # parse_result = parse_single_instruction('addi', 'a1', 'a0', '4')
    # splits = split_param(bas)

    # parse_result = parse_single_instruction(*splits)
    # parse_result = parse_single_instruction('sw', 'a1', 't0', '1')
    
    #打印到输出文件
    # 前两行添加
    line1 = 'memory_initialization_radix=16;'
    line2 = 'memory_initialization_vector='
    
    # 每行末尾加逗号
    for i in range(len(result_list)):
        if i+1 == len(result_list) or result_list[i+1] == '':
            # 最后一行末尾加分号
            result_list[i] += ';'
            break
        else:
            result_list[i] += ','

    # 将修改后的内容写回文件
    with open(file_name.split('.')[0]+'.coe', 'w', encoding='UTF8') as f:
        f.write(line1 + '\n')
        f.write(line2 + '\n')
        f.writelines('\n'.join(result_list))
