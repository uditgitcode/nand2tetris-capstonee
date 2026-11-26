(MAIN_LOOP)
    @KBD
    D=M
    @SET_WHITE
    D;JEQ

    @color
    M=-1
    @START_DRAW
    0;JMP

(SET_WHITE)
    @color
    M=0

(START_DRAW)
    @18656
    D=A
    @rowPtr
    M=D

    @20
    D=A
    @rowsLeft
    M=D

(ROW_LOOP)
    @rowsLeft
    D=M
    @MAIN_LOOP
    D;JEQ

    @rowPtr
    D=M
    @wordPtr
    M=D

    @4
    D=A
    @colsLeft
    M=D

(COL_LOOP)
    @colsLeft
    D=M
    @NEXT_ROW
    D;JEQ

    @color
    D=M
    @wordPtr
    A=M
    M=D

    @wordPtr
    M=M+1
    @colsLeft
    M=M-1

    @COL_LOOP
    0;JMP

(NEXT_ROW)
    @32
    D=A
    @rowPtr
    M=D+M
    @rowsLeft
    M=M-1

    @ROW_LOOP
    0;JMP
