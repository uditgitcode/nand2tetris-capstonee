// Simplified Pong paddle loop for assembler verification
@24000
D=A
@paddleAddr
M=D
(PONG_LOOP)
@KBD
D=M
@MOVE_LEFT
D;JGT
@PONG_LOOP
0;JMP
(MOVE_LEFT)
@paddleAddr
A=M
M=-1
@PONG_LOOP
0;JMP
