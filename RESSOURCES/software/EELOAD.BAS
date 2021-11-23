10  '  *******  EELOAD.BAS  20/3/87    Version 1.0 *******'
20 ' Written by R.Soja, Motorola East Kilbride'
30 ' Motorola Copyright 1987'
40 ' This program downloads S record file to the MC68HC11 through special'
50 ' bootstrap program, designed to program either internal or external '
60 ' EEPROM in the 68HC11's memory map'
70 ' The loader can also verify memory against an S record file.'
80 ' Downloaded data is optionally echoed on terminal.'
90 ' ==================================
100 CR$=CHR$(13)
110 MIN$=CHR$(32)
120 MAX$=CHR$(127)
130 ERM$="Can't find "
140 LOADER$="EEPROGIX.BOO"
150 CLRLN$=SPACE$(80)
160 VER$="1.0": 'Version number of EELOAD'
170 ERRTOT%=0:  'Number of errors found by verify operation'
180 CLS
190 PRINT "  <<<<<<<<          EELOAD Version ";VER$;"                     >>>>>>>>"
200 PRINT "  <<<<<<<< 68HC11 Internal/External EEPROM loader/verifier >>>>>>>>"
210 PRINT
220 PRINT "==>  Before continuing, ensure 68HC11 is in bootstrap mode,"
230 PRINT "     RESET is off, and COM1 or COM2 is connected to the SCI"
240 PRINT
250 ' First make sure loader program is available'
260 ON ERROR GOTO 880
270 OPEN LOADER$ FOR INPUT AS #2
280 CLOSE #2
290 ON ERROR GOTO 0
300 CHAN$="0"
310 ROW=CSRLIN: 'Store current line number'
320 WHILE CHAN$<>"1" AND CHAN$<>"2"
330   GOSUB 1070
340   LINE INPUT "Enter COM channel number (1/2):",CHAN$
350 WEND
360 CM$="COM"+CHAN$
370 ' Now set baud rate to 1200 and load EEPROG through boot loader'
380 ' by executing DOS MODE and COPY commands'
390 SHELL "MODE "+CM$+":1200,N,8,1"
400 SHELL "COPY "+LOADER$+" "+CM$
401 GOSUB 1070
402 FOR I%=1 TO 4:PRINT CLRLN$;:NEXT I%:PRINT: 'Clear DOS commands from screen'
410 ECHO$=" "
420 WHILE ECHO$<>"Y" AND ECHO$<>"N"
430   GOSUB 1070
440   LINE INPUT "Do you want echo to screen (Y/N):",ECHO$
450 WEND
470 ROW=CSRLIN: 'Store current line number'
480 EEOPT$=" ": 'Initialise option char'
490 WHILE EEOPT$<>"X" AND EEOPT$<>"I" AND EEOPT$<>"V"
500   GOSUB 1070
510   LINE INPUT "Select Internal,eXternal or Verify EEPROM option (I/X/V):",EEOPT$
520 WEND
530 OPT$="Verify"
540 IF EEOPT$="I" THEN OPT$="Internal"
550 IF EEOPT$="X" THEN OPT$="External"
560 ROW=CSRLIN: 'Store current line position in case of file error'
570 RXERR=0:    'Initialise number of RX errors allowed'
580 ON ERROR GOTO 910
590 GOSUB 1070
600 IF OPT$="Verify" THEN INPUT "Enter filename to verify: ",F$ ELSE INPUT "Enter filename to download:",F$
610 CLOSE
620 OPEN F$ FOR INPUT AS #2
630 ON ERROR GOTO 0
640 'COM1 or 2 connected to SCI on HC11'
650  OPEN CM$+":9600,N,8,1" AS #1
660 'Establish contact with HC11 by sending CR char & waiting for echo'
670 ON ERROR GOTO 860: 'Clear potential RX error'
680 PRINT #1,CR$;
690 GOSUB 990: 'Read char into B$'
700 'Transmit Internal,External or Verify EEPROM option char to 68HC11'
710 PRINT #1,EEOPT$;:GOSUB 990:              'No echo to screen'
720 ON ERROR GOTO 930
730 PRINT "Starting download of <";F$;"> to: ";OPT$;" Eeprom"
732 IF ECHO$="Y" THEN E%=1 ELSE E%=0
734 IF EEOPT$="V" THEN V%=1 ELSE V%=0
740 WHILE NOT EOF(2)
750  INPUT #2,S$
751  L%=LEN(S$)
752  FOR I%=1 TO L%
760      PRINT #1,MID$(S$,I%,1);:GOSUB 990:IF E% THEN PRINT B$;
770      IF V% THEN GOSUB 1030:IF C$<>"" THEN PRINT ":";HEX$(ASC(C$));
785  NEXT I%
787  IF E% THEN PRINT
790 WEND
795 PRINT
800 PRINT "Download Complete"
810 IF V% THEN PRINT ERRTOT%;" error(s) found"
820 CLOSE #2
830 SYSTEM
840 END
850 ' -----------------'
860 IF RXERR>5 THEN 940 ELSE RXERR=RXERR+1:RESUME 610
870 ' -----------------'
880 PRINT:PRINT ERM$;LOADER$:PRINT "Program aborted"
890 GOTO 830
900 ' -----------------'
910 PRINT ERM$;F$;SPACE$(40)
920 RESUME 580
930 '-----------------'
940 PRINT:PRINT "Communication breakdown: Download aborted"
950 GOTO 820
960 '--------------------'
970 '--SUB waits for received character, with time limit'
980 '--    returns with char in B$, or aborts if time limit exceeded'
990 T0%=0:WHILE LOC(1)=0:IF T0%>100 THEN 940 ELSE T0%=T0%+1:WEND
1000 B$=INPUT$(1,#1):RETURN
1010 '--------------------'
1020 '--SUB waits for received character, with time limit'
1025 '--    returns with char in C$, or null in C$ if time limit exceeded'
1030 T0%=0:C$="":WHILE LOC(1)=0 AND T0%<1:T0%=T0%+1:WEND
1040 IF LOC(1)>0 THEN C$=INPUT$(1,#1):ERRTOT%=ERRTOT%+1
1050 RETURN
1060 '--------------------'
1070 '--SUB Clear line '
1080 LOCATE ROW,1,1:PRINT CLRLN$
1090 LOCATE ROW,1,1:RETURN
1100 '--------------------'
CATE ROW,1,1:RETURN
1100 '--------------------'
