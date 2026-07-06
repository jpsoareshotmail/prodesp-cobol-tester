000000* VERSION   3.1  ; SAVED 20180725 16:41:51                    |000|0003.01    
000200$$SET SHARING=SHAREDBYALL                                         |           
000300$$SET TEMPORARY                                                   |           
000400 IDENTIFICATION  DIVISION.                                        |           
000500**************************                                        |           
000600*                                                                 |           
000700*PROGRAM-ID.     PC-GAA-L017.                                     |0003.01    
000800 AUTHOR.         SSA.                                             |           
000900 DATE-WRITTEN.   JUNHO/2018.                                      |0002.01    
001000 SECURITY.                                                        |           
001100*                                                                 |           
001200******************************************************************|           
001300*    OBJETIVO:    RECEBER PLACA BCO E DESCOMPACTAR PARA PLACA    *|0002.01    
001400*                 MERCOSUL                                       *|0002.01    
001500******************************************************************|           
001600*                A   L   T   E   R   A   C   A   O               *|           
001700******************************************************************|           
001800*                                                                *|           
001900*  DATA       AN /PROGR    OBJETIVO                              *|           
002000*  ====       =========    ========                              *|           
002100*                                                                *|           
002200*  25/07/18   JAC/JAC      INIBIR PROGRAM-ID (SEGUNDO DERSIO)--  *|0003.01    
002300*  --/--/--   ---/---      ------------------------------------  *|           
002400*  --/--/--   ---/---      ------------------------------------  *|           
002500******************************************************************|           
002600*                                                                 |           
002700                                                                  |           
002800                                                                  |           
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
003900                                                                  |           
004000                                                                  |           
004100/                                                                 |           
004200 DATA        DIVISION.                                            |           
004300                                                                  |           
004400 WORKING-STORAGE SECTION.                                         |           
004500*************************                                         |           
004600*                                                                 |           
004700                                                                  |           
004800 01          AX-PLACA.                                            |0002.01    
004900     05      AX-PLC-LETRA    PIC X(003).                          |0002.01    
005000     05      AX-PLC-NUMERO   PIC 9(004).                          |0002.01    
005100     05      AX-PLC-NUMERO-R REDEFINES   AX-PLC-NUMERO.           |0002.01    
005200       10    AX-PLC-NUM12    PIC 9(002).                          |0002.01    
005300       10    AX-PLC-NUM34    PIC 9(002).                          |0002.01    
005400                                                                  |0002.01    
005500 01          AX-PLACA-2LET   REDEFINES   AX-PLACA.                |0002.01    
005600     05      AX-PLC-LETRA1   PIC X(002).                          |0002.01    
005700     05      AX-PLC-NUMERO1  PIC 9(004).                          |0002.01    
005800     05      AX-PLC-NUMERO1R REDEFINES   AX-PLC-NUMERO1.          |0002.01    
005900       10    AX-PLC-NUM12-R1 PIC 9(002).                          |0002.01    
006000       10    AX-PLC-NUM34-R1 PIC 9(002).                          |0002.01    
006100     05      AX-PLC-FILLER1  PIC X(001).                          |0002.01    
006200                                                                  |0002.01    
006300 01          AX-PLACA-MOTO   REDEFINES   AX-PLACA.                |0002.01    
006400     05      AX-PLC-LETRA2   PIC X(002).                          |0002.01    
006500     05      AX-PLC-NUM123-X.                                     |0002.01    
006600       10    AX-PLC-NUM123   PIC 9(003).                          |0002.01    
006700     05      AX-PLC-FILLER2  PIC X(002).                          |0002.01    
006800                                                                  |0002.01    
006900                                                                  |           
007000                                                                  |           
007100                                                                  |           
007200 01          AX-HIGH         PIC X(001)  VALUE   HIGH-VALUES.     |0002.01    
007300 01          AX-HIGH-R       REDEFINES   AX-HIGH.                 |0002.01    
007400     05      AX-HV           PIC 9(001)  COMP.                    |0002.01    
007500     05      FILLER          PIC 9(001)  COMP.                    |0002.01    
007600                                                                  |0002.01    
007700/                                                                 |0002.01    
007800                                                                  |0002.01    
007900***  PARAMETRO DE ENTRADA (PLACA NO FORMATO DO BCO TIPO PLC-PLACA)|0002.01    
008000*                                                                 |0002.01    
008100                                                                  |0002.01    
008200 01          AX-PARM-PLACA.                                       |0002.01    
008300     05      AX-DB-LETRA.                                         |0002.01    
008400       10    AX-DB-LET1      PIC X(001).                          |0002.01    
008500       10    AX-DB-LET23     PIC X(002).                          |0002.01    
008600     05      AX-DB-NUMERO    PIC 9(004)  COMP.                    |0002.01    
008700     05      AX-DB-NUMERO-R1 REDEFINES   AX-DB-NUMERO.            |0002.01    
008800       10    AX-DB-NUM12     PIC 9(002)  COMP.                    |0002.01    
008900       10    AX-DB-NUM34     PIC 9(002)  COMP.                    |0002.01    
009000     05      AX-DB-NUMERO-R2 REDEFINES   AX-DB-NUMERO.            |0002.01    
009100       10    AX-DB-NUM123    PIC 9(003)  COMP.                    |0002.01    
009200       10    AX-DB-NUM4      PIC 9(001)  COMP.                    |0002.01    
009300                                                                  |           
009400                                                                  |           
009500                                                                  |0002.01    
009600***  RETORNO DO PARAMETRO (PLACA MERCOSUL LLLNNNN/LLNNNN/LLNNN)   |0002.01    
009700***  PARA POPULAR O NOVO CAMPO SEM TRANSFORMA-LA)                 |0002.01    
009800*                                                                 |0002.01    
009900                                                                  |0002.01    
010000 01          AX-PARM-PLACA-MERC.                                  |0002.01    
010100       10    AX-PLACA-MERC           PIC X(007).                  |0002.01    
010200       10    FILLER                  PIC X(003).                  |0002.01    
010300                                                                  |0002.01    
010400                                                                  |0002.01    
010500                                                                  |0002.01    
010600                                                                  |           
010700                                                                  |           
010800/                                                                 |           
010900 PROCEDURE   DIVISION                USING   AX-PARM-PLACA        |0002.01    
011000                                             AX-PARM-PLACA-MERC.  |0002.01    
011100*************************                                         |0002.01    
011200                                                                  |           
011300*                                                                 |           
011400 010-E-PROCEDURE.                                                 |           
011500*                                                                 |           
011600*                                                                 |           
011700     MOVE    SPACES                  TO      AX-PLACA             |0002.01    
011800                                             AX-PARM-PLACA-MERC.  |0002.01    
011900                                                                  |           
012000                                                                  |           
012100     IF      AX-DB-LET1              =       SPACES OR LOW-VALUES |0002.01    
012200             MOVE    AX-DB-LET23     TO      AX-PLC-LETRA1        |0002.01    
012300                                                                  |0002.01    
012400             IF      AX-DB-NUM4      =       AX-HV                |0002.01    
012500                     MOVE    AX-DB-NUM123    TO    AX-PLC-NUM123  |0002.01    
012600             ELSE                                                 |0002.01    
012700                     MOVE    AX-DB-NUMERO    TO    AX-PLC-NUMERO1 |0002.01    
012800     ELSE                                                         |0002.01    
012900             MOVE    AX-DB-LETRA     TO      AX-PLC-LETRA         |0002.01    
013000             MOVE    AX-DB-NUMERO    TO      AX-PLC-NUMERO.       |0002.01    
013100                                                                  |0002.01    
013200                                                                  |0002.01    
013300     MOVE    AX-PLACA                TO      AX-PLACA-MERC.       |0002.01    
013400                                                                  |           
013500                                                                  |           
013600 010-S-PROCEDURE.                                                 |           
013700     EXIT PROGRAM.                                                |           
013800***************************************************************** |           
