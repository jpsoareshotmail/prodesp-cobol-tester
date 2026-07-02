000000* VERSION   1.1  ; SAVED 20181003 16:31:00                    |000|0001.01    
000100$$SET SHARING=SHAREDBYALL                                         |           
000200$$SET TEMPORARY                                                   |           
000300 IDENTIFICATION  DIVISION.                                        |           
000400**************************                                        |           
000500*                                                                 |           
000600*PROGRAM-ID.     PC-GAA-L009.                                     |           
000700 AUTHOR.         SSA.                                             |           
000800 DATE-WRITTEN.   OUTUBRO/2018.                                    |           
000900 SECURITY.                                                        |           
001000*                                                                 |           
001100******************************************************************|           
001200*    OBJETIVO:                                                   *|           
001300*    CONSISTE PLACA DE 3 LETRAS INFORMANDO AO CHAMADOR           *|           
001400*    PLACA MERCOSUL TRANSFORMADA NO FORMATO LLLNNNN              *|           
001500******************************************************************|           
001600*                A   L   T   E   R   A   C   A   O               *|           
001700******************************************************************|           
001800*                                                                *|           
001900*  DATA       AN /PROGR    OBJETIVO                              *|           
002000*  ====       =========    ========                              *|           
002100*                                                                *|           
002200*  --/--/--   ---/---      ------------------------------------  *|           
002300*  --/--/--   ---/---      ------------------------------------  *|           
002400******************************************************************|           
002500*                                                                 |           
002600                                                                  |           
002700                                                                  |           
002800 ENVIRONMENT DIVISION.                                            |           
002900**********************                                            |           
003000*                                                                 |           
003100 CONFIGURATION   SECTION.                                         |           
003200*************************                                         |           
003300*                                                                 |           
003400 OBJECT-COMPUTER.    A15.                                         |           
003500 SPECIAL-NAMES.                                                   |           
003600*                                                                 |           
003700     DECIMAL-POINT                   IS      COMMA.               |           
003800                                                                  |           
003900                                                                  |           
004000/                                                                 |           
004100 DATA        DIVISION.                                            |           
004200                                                                  |           
004300 WORKING-STORAGE SECTION.                                         |           
004400*************************                                         |           
004500*                                                                 |           
004600                                                                  |           
004700*====> Sø PODE VIR:                                               |           
004800****                 LLLNLNN   (3 LETRAS MERCOSUL)                |           
004900*                                                                 |           
005000 01          AX-PARM-PL-MERC   PIC X(010).                        |           
005100                                                                  |           
005200 01          AX-RETORNO.                                          |           
005300     05      AX-RET-PLACA.                                        |           
005400        10   AX-RET-PLACA-NR   PIC X(007).                        |           
005500        10   FILLER            PIC X(003).                        |           
005600                                                                  |           
005700     05      AX-RET-PLACA-R    REDEFINES   AX-RET-PLACA.          |           
005800        10   AX-RET-LET            PIC X(003).                    |           
005900        10   AX-RET-NUM1           PIC 9(001).                    |           
006000        10   AX-RET-NUM2           PIC 9(001).                    |           
006100        10   AX-RET-NUM34          PIC 9(002).                    |           
006200        10   FILLER                PIC X(003).                    |           
006300                                                                  |           
006400                                                                  |           
006500***--------> AREA AUXILIAR PARA A PLACA RECEBIDA                  |           
006600                                                                  |           
006700 01          AX-PLACA.                                            |           
006800     05      AX-PLAC        PIC X(001)   OC  7.                   |           
006900     05      FILLER         PIC X(003).                           |           
007000                                                                  |           
007100 01          AX-PLACA-R1    REDEFINES    AX-PLACA.                |           
007200     05      AX-LET         PIC X(003).                           |           
007300     05      AX-NUM1        PIC 9(001).                           |           
007400     05      AX-NUM2        PIC X(001).                           |           
007500     05      AX-NUM34       PIC 9(002).                           |           
007600     05      FILLER         PIC X(003).                           |           
007700                                                                  |           
007800 01          AX-PLACA-R2    REDEFINES    AX-PLACA.                |           
007900     05      FILLER         PIC X(003).                           |           
008000     05      AX-NUMERO      PIC X(004).                           |           
008100     05      FILLER         PIC X(003).                           |           
008200                                                                  |           
008300                                                                  |           
008400                                                                  |           
008500/                                                                 |           
008600 PROCEDURE   DIVISION                USING   AX-PARM-PL-MERC      |           
008700                                             AX-RETORNO.          |           
008800                                                                  |           
008900*                                                                 |           
009000 010-E-PROCEDURE.                                                 |           
009100*                                                                 |           
009200*                                                                 |           
009300     MOVE    SPACES                  TO      AX-PLACA.            |           
009400     MOVE    SPACES                  TO      AX-RETORNO.          |           
009500     MOVE    SPACES                  TO      AX-RET-PLACA.        |           
009600                                                                  |           
009700     MOVE    AX-PARM-PL-MERC         TO      AX-PLACA.            |           
009800     MOVE    AX-LET                  TO      AX-RET-LET.          |           
009900     MOVE    AX-NUM1                 TO      AX-RET-NUM1.         |           
010000     MOVE    AX-NUM34                TO      AX-RET-NUM34.        |           
010100                                                                  |           
010200                                                                  |           
010300     IF      AX-NUMERO               =       "0A00"               |           
010400             MOVE    SPACES          TO      AX-RETORNO           |           
010500     ELSE                                                         |           
010600     IF      AX-PLAC (05)            =       "A"                  |           
010700             MOVE    "0"             TO      AX-RET-NUM2          |           
010800     ELSE                                                         |           
010900     IF      AX-PLAC (05)            =       "B"                  |           
011000             MOVE    "1"             TO      AX-RET-NUM2          |           
011100     ELSE                                                         |           
011200      IF     AX-PLAC (05)            =       "C"                  |           
011300             MOVE    "2"             TO      AX-RET-NUM2          |           
011400     ELSE                                                         |           
011500     IF      AX-PLAC (05)            =       "D"                  |           
011600             MOVE    "3"             TO      AX-RET-NUM2          |           
011700     ELSE                                                         |           
011800     IF      AX-PLAC (05)            =       "E"                  |           
011900             MOVE    "4"             TO      AX-RET-NUM2          |           
012000     ELSE                                                         |           
012100     IF      AX-PLAC (05)            =       "F"                  |           
012200             MOVE    "5"             TO      AX-RET-NUM2          |           
012300     ELSE                                                         |           
012400     IF      AX-PLAC (05)            =       "G"                  |           
012500             MOVE    "6"             TO      AX-RET-NUM2          |           
012600     ELSE                                                         |           
012700     IF      AX-PLAC (05)            =       "H"                  |           
012800             MOVE    "7"             TO      AX-RET-NUM2          |           
012900     ELSE                                                         |           
013000     IF      AX-PLAC (05)            =       "I"                  |           
013100             MOVE    "8"             TO      AX-RET-NUM2          |           
013200     ELSE                                                         |           
013300     IF      AX-PLAC (05)            =       "J"                  |           
013400             MOVE    "9"             TO      AX-RET-NUM2          |           
013500     ELSE                                                         |           
013600             MOVE    SPACES          TO      AX-RETORNO.          |           
013700                                                                  |           
013800                                                                  |           
013900                                                                  |           
014000                                                                  |           
014100 010-S-PROCEDURE.                                                 |           
014200     EXIT PROGRAM.                                                |           
014300***************************************************************** |           
