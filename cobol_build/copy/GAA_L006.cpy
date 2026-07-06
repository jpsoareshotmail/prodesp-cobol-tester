000000* VERSION   1.1  ; SAVED 20111107 15:22:24                    |000|0001.01    
000100$$SET SHARING=SHAREDBYALL                                         |           
000200$$SET TEMPORARY                                                   |           
000300 IDENTIFICATION  DIVISION.                                        |           
000400**************************                                        |           
000500*                                                                 |           
000600*PROGRAM-ID.     PC-GAA-L006.                                     |           
000700 AUTHOR.         SIDNEY.                                          |           
000800 DATE-WRITTEN.   21/09/92.                                        |           
000900 SECURITY.                                                        |           
001000*                                                                 |           
001100******************************************************************|           
001200*    OBJETIVO:                                                   *|           
001300*            CONSISTE PLACA INFORMANDO AO CHAMADOR O FORMATO     *|           
001400*            DA PLACA (2 OU 3 LETRAS)                            *|           
001500*                                                                *|           
001600******************************************************************|           
001700/                                                                 |           
001800******************************************************************|           
001900*                A   L   T   E   R   A   [   ]   O               *|           
002000******************************************************************|           
002100*                                                                *|           
002200*  SEQ      DATA     O.S.     PATCH       ANALISTA/PROGRAMADOR   *|           
002300*  ===      ====     ===      =====       ====================   *|           
002400*  ---    --/--/--   ----      ---        --------/------        *|           
002500*  ---    --/--/--   ----      ---        --------/------        *|           
002600*  ---    --/--/--   ----      ---        --------/------        *|           
002700******************************************************************|           
002800/                                                                 |           
002900 ENVIRONMENT DIVISION.                                            |           
003000**********************                                            |           
003100*                                                                 |           
003200 CONFIGURATION   SECTION.                                         |           
003300*************************                                         |           
003400*                                                                 |           
003500 OBJECT-COMPUTER.    A15.                                         |           
003600 SPECIAL-NAMES.                                                   |           
003700*                                                                 |           
003800     DECIMAL-POINT                   IS      COMMA.               |           
003900/                                                                 |           
004000 DATA        DIVISION.                                            |           
004100                                                                  |           
004200 WORKING-STORAGE SECTION.                                         |           
004300*************************                                         |           
004400*                                                                 |           
004500 01          AX-PARM-PLACA   PIC X(007).                          |           
004600 01          AX-PARM-PLACA-R REDEFINES   AX-PARM-PLACA.           |           
004700     05      AX-PLACA-1-6    PIC X(006).                          |           
004800     05      AX-PLACA-7      PIC X(001).                          |           
004900*                                                                 |           
005000*====> AX-TIPO =  0 : PLACA INVALIDA                              |           
005100*                 1 : PLACA DE MOTO                               |           
005200*                 2 : PLACA COM 2 LETRAS                          |           
005300*                 3 : PLACA COM 3 LETRAS                          |           
005400                                                                  |           
005500 01          AX-RETORNO.                                          |           
005600     05      AX-RET-TIPO     PIC X(001).                          |           
005700     05      AX-RET-LET      PIC X(003).                          |           
005800     05      AX-RET-NUMERO   PIC 9(004)  COMP.                    |           
005900     05      AX-RET-NUMERO-R REDEFINES   AX-RET-NUMERO.           |           
006000        10   AX-RET-NUM123   PIC 9(003)  COMP.                    |           
006100        10   AX-RET-NUM4     PIC 9(001)  COMP.                    |           
006200                                                                  |           
006300 01          AX-PLACA.                                            |           
006400     05      FILLER         PIC X(001).                           |           
006500     05      AX-PLAC-2-7    PIC X(006).                           |           
006600 01          AX-PLACA-R     REDEFINES    AX-PLACA.                |           
006700     05      AX-PLAC        PIC X(001)   OC  7.                   |           
006800 01          AX-PLACA-R2    REDEFINES    AX-PLACA.                |           
006900     05      AX-LET-R       PIC X(003).                           |           
007000     05      AX-MOTO        PIC X(001).                           |           
007100     05      AX-MOTO-R      REDEFINES    AX-MOTO                  |           
007200                            PIC 9(001).                           |           
007300     05      AX-NUM-R       PIC 9(003).                           |           
007400 01          AX-PLACA-R3    REDEFINES    AX-PLACA.                |           
007500     05      FILLER         PIC X(003).                           |           
007600     05      AX-NUMERO      PIC 9(004).                           |           
007700                                                                  |           
007800 01          AX-HIGH-VAL    PIC X(001)   VA  HIGH-VALUES.         |           
007900 01          AX-HIGH-VAL-R  REDEFINES    AX-HIGH-VAL.             |           
008000     05      AX-HIGH        PIC 9(001)   COMP.                    |           
008100     05      FILLER         PIC 9(001)   COMP.                    |           
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
009500                                                                  |           
009600     IF      AX-PLACA-7              =       SPACES  OR           |           
009700                                             LOW-VALUES           |           
009800             MOVE    AX-PLACA-1-6    TO      AX-PLAC-2-7          |           
009900     ELSE                                                         |           
010000             MOVE    AX-PARM-PLACA   TO      AX-PLACA.            |           
010100                                                                  |           
010200     IF      AX-PLAC (01)            =       SPACES               |           
010300             NEXT    SENTENCE                                     |           
010400     ELSE                                                         |           
010500     IF      AX-PLAC (01)            NOT     ALPHABETIC           |           
010600             MOVE    0               TO      AX-RET-TIPO          |           
010700             GO                      TO      010-S-PROCEDURE.     |           
010800                                                                  |           
010900     IF     (AX-PLAC (02)            NOT     ALPHABETIC OR        |           
011000             AX-PLAC (02)            =       SPACES     OR        |           
011100                                             LOW-VALUES)     OR   |           
011200            (AX-PLAC (03)            NOT     ALPHABETIC OR        |           
011300             AX-PLAC (03)            =       SPACES     OR        |           
011400                                             LOW-VALUES)          |           
011500             MOVE    0               TO      AX-RET-TIPO          |           
011600             GO                      TO      010-S-PROCEDURE.     |           
011700                                                                  |           
011800     IF      AX-PLAC (04)            NOT     NUMERIC AND          |           
011900             AX-PLAC (04)            NOT =   "M"                  |           
012000             MOVE    0               TO      AX-RET-TIPO          |           
012100             GO                      TO      010-S-PROCEDURE.     |           
012200                                                                  |           
012300     IF     (AX-PLAC (05)            NOT     NUMERIC OR           |           
012400             AX-PLAC (05)            =       SPACES  OR           |           
012500                                             LOW-VALUES)     OR   |           
012600            (AX-PLAC (06)            NOT     NUMERIC OR           |           
012700             AX-PLAC (06)            =       SPACES  OR           |           
012800                                             LOW-VALUES)     OR   |           
012900            (AX-PLAC (07)            NOT     NUMERIC OR           |           
013000             AX-PLAC (07)            =       SPACES  OR           |           
013100                                             LOW-VALUES)          |           
013200             MOVE    0               TO      AX-RET-TIPO          |           
013300             GO                      TO      010-S-PROCEDURE.     |           
013400                                                                  |           
013500     IF      AX-MOTO                 =       "M"                  |           
013600       IF    AX-NUM-R                =       ZEROS   OR           |           
013700             AX-LET-R                >       " ZZ"                |           
013800             MOVE      0             TO      AX-RET-TIPO          |           
013900             GO                      TO      010-S-PROCEDURE      |           
014000       ELSE                                                       |           
014100             MOVE      1             TO      AX-RET-TIPO          |           
014200             GO                      TO      010-1-PROCEDURE.     |           
014300                                                                  |           
014400     IF      AX-NUMERO               =       ZEROS                |           
014500             MOVE      0             TO      AX-RET-TIPO          |           
014600             GO                      TO      010-S-PROCEDURE.     |           
014700                                                                  |           
014800     IF      AX-LET-R                <       "AAA"                |           
014900             MOVE      2             TO      AX-RET-TIPO          |           
015000     ELSE                                                         |           
015100             MOVE      3             TO      AX-RET-TIPO.         |           
015200                                                                  |           
015300 010-1-PROCEDURE.                                                 |           
015400                                                                  |           
015500     MOVE    AX-LET-R                TO      AX-RET-LET.          |           
015600                                                                  |           
015700     IF      AX-RET-TIPO             =       1                    |           
015800             MOVE    AX-HIGH         TO      AX-RET-NUM4          |           
015900             MOVE    AX-NUM-R        TO      AX-RET-NUM123        |           
016000     ELSE                                                         |           
016100             MOVE    AX-NUMERO       TO      AX-RET-NUMERO.       |           
016200                                                                  |           
016300 010-S-PROCEDURE.                                                 |           
016400                                                                  |           
016500*                                                                 |           
016600*                                                                 |           
016700     EXIT PROGRAM.                                                |           
016800***************************************************************** |           
