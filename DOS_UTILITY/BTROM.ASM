
        *****************************************************
        * BootLoader To jump in BF00 Progrmer utility       *
        *                                                   *
        * Rev A : B.S. 11/2021                              *
        *****************************************************


PROGRAM		EQU	$BF00	EPROM prog utility in boot ROM
ROM_W_START	EQU	$D410	Start adress to write.

BLPROG	LDAA	#$04	Pattern for DWOM off, no SPI
		STAA	$1028	Turns off DWOM in target MCU
		LDY		#ROM_W_START
* NOTE: Can't use direct addressing in target MCU because
*       regs are located at $1000.
		JMP	PROGRAM	Jumps to EPROM prog routine
ENDBPR	EQU	*


END.
* -------------------------------------------------------------------------
