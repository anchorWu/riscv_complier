# @Author   : Pyrrho
# @Date     : 27/03/2024

# (MNEMONIC, FMT, OPCODE, FUNCT3, FUNCT7)
base_integer_instruction_table = (
    # ('lb', 'I', '0000011', '000', ''),

    ('lw', 'I', '0000011', '010', ''),  # pass
    ('addi', 'I', '0010011', '000', ''),  # pass
    ('add', 'R', '0110011', '000', '0000000'),  # pass
    ('sw', 'S', '0100011', '010', ''),
)


def inst_dict(inst):
    """
    元组转换为字典形式
    :param inst: 指令名
    :return: 指令的字典
    """
    for t in base_integer_instruction_table:
        if t[0] == inst:
            return {
                'mnemonic': t[0],
                'fmt': t[1],
                'opcode': t[2],
                'funct3': t[3],
                'funct7': t[4],
            }


register_table = (
    ('x0', 'zero'),
    ('x1', 'ra'),
    ('x2', 'sp'),
    ('x3', 'gp'),
    ('x4', 'tp'),
    ('x5', 't0'),
    ('x6', 't1'),
    ('x7', 't2'),
    ('x8', 's0'),
    ('x9', 's1'),
    ('x10', 'a0'),
    ('x11', 'a1'),
    ('x12', 'a2'),
    ('x13', 'a3'),
    ('x14', 'a4'),
    ('x15', 'a5'),
    ('x16', 'a6'),
    ('x17', 'a7'),
    ('x18', 's2'),
    ('x19', 's3'),
    ('x20', 's4'),
    ('x21', 's5'),
    ('x22', 's6'),
    ('x23', 's7'),
    ('x24', 's8'),
    ('x25', 's9'),
    ('x26', 's10'),
    ('x27', 's11'),
    ('x28', 't3'),
    ('x29', 't4'),
    ('x30', 't5'),
    ('x31', 't6'),
)


def reg_name(reg):
    for i in register_table:
        if i[1] == reg:
            return bin(int(i[0][1:]))[2:].zfill(5)
