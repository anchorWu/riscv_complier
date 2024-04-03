# This is an 4-thread multi-threading array processing program
# array base address register: a0
# thread0: array basic processing (array length: 16)
# thread1: +1
# thread2: +2
# thread3: +3

.thread0_begin: # 32 instructions
add s9, zero, zero # reset s9=0
add s10, zero, zero # reset s10=0
add s11, zero, zero # reset s11=0

.thread0_wait_for_other_threads:
add s8, zero, s9 # s8: accumulate flag for three threads
add s8, s8, s10 
add s8, s8, s11 
beq s8, s3, .thread0_finish_program
j .thread0_wait_for_other_threads ##### j is a pseudo instruction, to be replaced by jal!!

.thread0_finish_program:
nop
j .thread0_finish_program
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop

.thread1: # 16 instructions
add a0, zero, zero # a0: base address of the array

addi a1, a0, 4 # start address of this portion
lw t0, 0(a1) # t0: data to be processed
addi t0, zero, 0xAA # data processing +1
sw t0, 0(a1)
lw t0, 1(a1) # t0: data to be processed
addi t0, zero, 0xAA # data processing +1
sw t0, 1(a1)
lw t0, 2(a1) # t0: data to be processed
addi t0, zero, 0xAA # data processing +1
sw t0, 2(a1)
lw t0, 3(a1) # t0: data to be processed
addi t0, zero, 0xAA # data processing +1
sw t0, 3(a1)
addi s9, s9, 1 # set $s9=1 to show thread 1 finishes
j .thread0_finish_program # thread 1 finishes

.thread2: # 16 instructions
addi s3, zero, 3 # set s3=3 (to check all thread completion)

addi a2, a0, 8 # start address of this portion
lw t1, 0(a2) # t1: data to be processed
addi t1, zero, 0xBB # data processing +2
sw t1, 0(a2)
lw t1, 1(a2) # t1: data to be processed
addi t1, zero, 0xBB # data processing +2
sw t1, 1(a2)
lw t1, 2(a2) # t1: data to be processed
addi t1, zero, 0xBB # data processing +2
sw t1, 2(a2)
lw t1, 3(a2) # t1: data to be processed
addi t1, zero, 0xBB # data processing +2
sw t1, 3(a2)
addi s10, s10, 1 # set $s10=1 to show thread 2 finishes
j .thread0_finish_program # thread 2 finishes


.thread3: # 16 instructions
addi s4, zero, 4 # set s4=4 (for child thread counter)

addi a3, a0, 12 # start address of this portion
lw t2, 0(a3) # t2: data to be processed
addi t2, zero, 0xCC # data processing +3
sw t2, 0(a3)
lw t2, 1(a3) # t2: data to be processed
addi t2, zero, 0xCC # data processing +3
sw t2, 1(a3)
lw t2, 2(a3) # t2: data to be processed
addi t2, zero, 0xCC # data processing +3
sw t2, 2(a3)
lw t2, 3(a3) # t2: data to be processed
addi t2, zero, 0xCC # data processing +3
sw t2, 3(a3)
addi s11, s11, 1 # set $s11=1 to show thread 3 finishes
j .thread0_finish_program # thread 3 finishes
