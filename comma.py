# @Author   : Pyrrho
# @Date     : 23/03/2024
import sys

# 前两行添加
line1 = 'memory_initialization_radix=16;'
line2 = 'memory_initialization_vector='

file_name = sys.argv[1]

with open(file_name, 'r', encoding='UTF8') as f:
    lines = f.readlines()

lines = [line.strip() for line in lines]  # 去掉每一行的前后空白

# 每行末尾加逗号
for i in range(len(lines)):
    if i + 1 == len(lines) or lines[i + 1] == '':
        # 最后一行末尾加分号
        lines[i] += ';'
        break
    else:
        lines[i] += ','

# 将修改后的内容写回文件
with open(file_name.split('.')[0] + '.coe', 'w', encoding='UTF8') as f:
    f.write(line1 + '\n')
    f.write(line2 + '\n')
    f.writelines('\n'.join(lines))
