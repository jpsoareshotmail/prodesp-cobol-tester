000000* VERSION   1.1  ; SAVED 20180712 16:36:53                    |000|0001.01    
000100$$SET SHARING=SHAREDBYALL                                         |           
000200$$SET TEMPORARY                                                   |           
000300 IDENTIFICATION  DIVISION.                                        |           
000400**************************                                        |           
000500*                                                                 |           
000600*PROGRAM-ID.     PC-GAA-L008.                                     |           
000700 AUTHOR.         SSA.                                             |           
000800 DATE-WRITTEN.   jULHO/2018.                                      |           
000900 SECURITY.                                                        |           
001000*                                                                 |           
001100******************************************************************|           
001200*    OBJETIVO:                                                   *|           
001300*    CONSISTE PLACA DE 3 LETRAS INFORMANDO AO CHAMADOR           *|           
001400*    PLACA TRANSFORMADA EM MERCOSUL NO FORMATO LLLNLNN           *|           
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
004800****                 LLLNNNN     (3 LETRAS NORMAL)                |           
004900*                                                                 |           
005000 01          AX-PARM-PLACA       PIC X(007).                      |           
005100*                                                                 |           
005200*====> AX-RET-TIPO =  0 : PLACA INVALIDA                          |           
005300*                     1 : PLACA TRANSFORMADA EM MERCOSUL          |           
005400                                                                  |           
005500*  TIPO RET/ PLACA ACESSO NOVO TAM.10                             |           
005600                                                                  |           
005700 01          AX-RETORNO.                                          |           
005800     05      AX-RET-TIPO       PIC 9(001).                        |           
005900                                                                  |           
006000     05      AX-RET-PLACA-MERC.                                   |           
006100        10   AX-RET-PLACAM     PIC X(007).                        |           
006200        10   FILLER            PIC X(003).                        |           
006300                                                                  |           
006400     05      AX-RET-PLACAM-MERC-R  REDEFINES   AX-RET-PLACA-MERC. |           
006500        10   AX-RET-LET            PIC X(003).                    |           
006600        10   AX-RET-NUM1           PIC 9(001).                    |           
006700        10   AX-RET-NUM2           PIC X(001).                    |           
006800        10   AX-RET-NUM34          PIC 9(002).                    |           
006900        10   FILLER                PIC X(003).                    |           
007000                                                                  |           
007100                                                                  |           
007200***--------> AREA AUXILIAR PARA A PLACA RECEBIDA                  |           
007300                                                                  |           
007400 01          AX-PLACA.                                            |           
007500     05      AX-PLAC        PIC X(001)   OC  7.                   |           
007600                                                                  |           
007700 01          AX-PLACA-R1    REDEFINES    AX-PLACA.                |           
007800     05      AX-LET         PIC X(003).                           |           
007900     05      AX-NUM1        PIC 9(001).                           |           
008000     05      AX-NUM2        PIC X(001).                           |           
008100     05      AX-NUM34       PIC 9(002).                           |           
008200                                                                  |           
008300                                                                  |           
008400                                                                  |           
008500/                                                                 |           
008600 PROCEDURE   DIVISION                USING   AX-PARM-PLACA        |           
008700                                             AX-RETORNO.          |           
008800                                                                  |           
008900*                                                                 |           
009000 010-E-PROCEDURE.                                                 |           
009100*                                                                 |           
009200*                                                                 |           
009300     MOVE    SPACES                  TO      AX-PLACA.            |           
009400     MOVE    LOW-VALUES              TO      AX-RETORNO.          |           
009500     MOVE    SPACES                  TO      AX-RET-PLACA-MERC.   |           
009600                                                                  |           
009700     MOVE    AX-PARM-PLACA           TO      AX-PLACA.            |           
009800                                                                  |           
009900                                                                  |           
010000     IF     (AX-PLAC (01)            NOT     ALPHABETIC OR        |           
010100             AX-PLAC (01)            =       SPACES     OR        |           
010200                                             LOW-VALUES)     OR   |           
010300            (AX-PLAC (02)            NOT     ALPHABETIC OR        |           
010400             AX-PLAC (02)            =       SPACES     OR        |           
010500                                             LOW-VALUES)     OR   |           
010600            (AX-PLAC (03)            NOT     ALPHABETIC OR        |           
010700             AX-PLAC (03)            =       SPACES     OR        |           
010800                                             LOW-VALUES)          |           
010900             MOVE    0               TO      AX-RET-TIPO          |           
011000             GO                      TO      010-S-PROCEDURE.     |           
011100                                                                  |           
011200                                                                  |           
011300                                                                  |           
011400     IF     (AX-PLAC (04)            NOT     NUMERIC OR           |           
011500             AX-PLAC (04)            =       SPACES  OR           |           
011600                                             LOW-VALUES)     OR   |           
011700            (AX-PLAC (05)            NOT     NUMERIC OR           |           
011800             AX-PLAC (05)            =       SPACES  OR           |           
011900                                             LOW-VALUES)     OR   |           
012000            (AX-PLAC (06)            NOT     NUMERIC OR           |           
012100             AX-PLAC (06)            =       SPACES  OR           |           
012200                                             LOW-VALUES)     OR   |           
012300            (AX-PLAC (07)            NOT     NUMERIC OR           |           
012400             AX-PLAC (07)            =       SPACES  OR           |           
012500                                             LOW-VALUES)          |           
012600             MOVE    0               TO      AX-RET-TIPO          |           
012700             GO                      TO      010-S-PROCEDURE.     |           
012800                                                                  |           
012900                                                                  |           
013000                                                                  |           
013100     IF      AX-PLAC (04)            =       "0"     AND          |           
013200             AX-PLAC (05)            =       "0"     AND          |           
013300             AX-PLAC (06)            =       "0"     AND          |           
013400             AX-PLAC (07)            =       "0"                  |           
013500             MOVE    0               TO      AX-RET-TIPO          |           
013600             GO                      TO      010-S-PROCEDURE.     |           
013700                                                                  |           
013800                                                                  |           
013900                                                                  |           
014000     MOVE    AX-LET                  TO      AX-RET-LET.          |           
014100     MOVE    AX-NUM1                 TO      AX-RET-NUM1.         |           
014200     MOVE    AX-NUM34                TO      AX-RET-NUM34.        |           
014300                                                                  |           
014400                                                                  |           
014500                                                                  |           
014600     IF      AX-PLAC (05)            =       "0"                  |           
014700             MOVE    "A"             TO      AX-RET-NUM2          |           
014800     ELSE                                                         |           
014900     IF      AX-PLAC (05)            =       "1"                  |           
015000             MOVE    "B"             TO      AX-RET-NUM2          |           
015100     ELSE                                                         |           
015200      IF     AX-PLAC (05)            =       "2"                  |           
015300             MOVE    "C"             TO      AX-RET-NUM2          |           
015400     ELSE                                                         |           
015500     IF      AX-PLAC (05)            =       "3"                  |           
015600             MOVE    "D"             TO      AX-RET-NUM2          |           
015700     ELSE                                                         |           
015800     IF      AX-PLAC (05)            =       "4"                  |           
015900             MOVE    "E"             TO      AX-RET-NUM2          |           
016000     ELSE                                                         |           
016100     IF      AX-PLAC (05)            =       "5"                  |           
016200             MOVE    "F"             TO      AX-RET-NUM2          |           
016300     ELSE                                                         |           
016400     IF      AX-PLAC (05)            =       "6"                  |           
016500             MOVE    "G"             TO      AX-RET-NUM2          |           
016600     ELSE                                                         |           
016700     IF      AX-PLAC (05)            =       "7"                  |           
016800             MOVE    "H"             TO      AX-RET-NUM2          |           
016900     ELSE                                                         |           
017000     IF      AX-PLAC (05)            =       "8"                  |           
017100             MOVE    "I"             TO      AX-RET-NUM2          |           
017200     ELSE                                                         |           
017300     IF      AX-PLAC (05)            =       "9"                  |           
017400             MOVE    "J"             TO      AX-RET-NUM2.         |           
017500                                                                  |           
017600                                                                  |           
017700     MOVE    1                       TO      AX-RET-TIPO.         |           
017800                                                                  |           
017900                                                                  |           
018000                                                                  |           
018100 010-S-PROCEDURE.                                                 |           
018200     EXIT PROGRAM.                                                |           
018300***************************************************************** |           
