000000* VERSION  2.1   ; SAVED 20240613 10:35:26                    |2.0|2.00001    
000100$$ SET SHARING=SHAREDBYALL                                        |           
000200$$ SET TEMPORARY                                                  |           
000300 IDENTIFICATION  DIVISION.                                        |           
000400**************************                                        |           
000500*                                                                 |           
000600* LIBRARY PC/GBA/L062                                             |           
000700*                                                                 |           
000800 AUTHOR.         MARLEY C. TAVARES.                               |           
000900*                                                                 |           
001000 DATE-WRITTEN.   12/06/2006.                                      |           
001100*                                                                 |           
001200 DATE-COMPILED.                                                   |           
001300*                                                                 |           
001400*================================================================*|           
001500*    PC/GBA/L062                                                 *|           
001600*                                                                *|           
001700*    ESTA LIBRARY TEM POR OBJETIVO CONSISTIR O NOME DO CONDU-    *|           
001800*    TOR PARA A EMISSAO DO "PID"- PERMISSAO INTERNACIONAL PARA   *|           
001900*    DIRIGIR.                                                    *|           
002000*                                                                *|           
002100*    RECEBE O NOME DO CONDUTOR VIA PARAMETRO, CONSISTE E         *|           
002200*    DEVOLVE O NOME E SOBRENOME - "C" (CORRETO) OU "E" (ERRADO). *|           
002300*                                                                *|           
002400*                                                                *|           
002500*    O NOME PODE TER ATE 60 CARACTERES, SENDO MINIMO DE 4        *|           
002600*    CARACTERES, O PRIMEIRO NAO PODE SER BRANCO, E NAO           *|           
002700*    PODE TER ESPACOS DUPLOS ENTRE CARACTERES.                   *|           
002800*                                                                *|           
002900*----------------------------------------------------------------*|           
003000                                                                  |           
003100                                                                  |           
003200/----------------------------------------------------------------*|           
003300*                                                                *|           
003400*                 ALTERACOES EFETUADAS                           *|           
003500*                 ====================                           *|           
003600*                                                                *|           
003700*                                                                *|           
003800*     DATA     TASK  DEMANDA / INC   PROGRAMADOR     ANALISTA    *|2.00001    
003900*  ==========  ====  ==============  ===========  =============  *|2.00001    
004000*  04/06/2024   001         #211793  SUELY        MARCIO         *|2.00001    
004100*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
004200*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
004300*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
004400*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
004500*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
004600*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
004700*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
004800*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
004900*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
005000*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
005100*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
005200*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
005300*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
005400*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
005500*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
005600*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
005700*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
005800*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
005900*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
006000*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
006100*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
006200*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
006300*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
006400*  __/__/____  ____  ______________  ___________  _____________  *|2.00001    
006500*                                                                *|           
006600*================================================================*|           
006700/                                                                 |           
006800 ENVIRONMENT     DIVISION.                                        |           
006900*------------------------*                                        |           
007000*                                                                 |           
007100 CONFIGURATION   SECTION.                                         |           
007200*                                                                 |           
007300 SPECIAL-NAMES.                                                   |           
007400                                                                  |           
007500     DECIMAL-POINT   IS  COMMA.                                   |           
007600                                                                  |           
007700*                                                                 |           
007800 INPUT-OUTPUT    SECTION.                                         |           
007900                                                                  |           
008000 FILE-CONTROL.                                                    |           
008100                                                                  |           
008200                                                                  |           
008300                                                                  |           
008400                                                                  |           
008500 DATA        DIVISION.                                            |           
008600*--------------------*                                            |           
008700*                                                                 |           
008800                                                                  |           
008900 FILE        SECTION.                                             |           
009000                                                                  |           
009100                                                                  |           
009200                                                                  |           
009300/                                                                 |           
009400 WORKING-STORAGE SECTION.                                         |           
009500*-----------------------*                                         |           
009600*                                                                 |           
009700 77          IX1             PIC 9(002)  BINARY.                  |           
009800                                                                  |           
009900                                                                  |           
010000 01          CH-ESPACO-DUPLO PIC X(001).                          |           
010100                                                                  |           
010200 01          CH-ERRO         PIC X(001).                          |           
010300                                                                  |           
010400                                                                  |           
010500                                                                  |           
010600 01          AX-NOME         PIC X(061).                          |           
010700 01          AX-NOME-R1      REDEFINES   AX-NOME.                 |           
010800     05      AX-NOME-POS1    PIC X(001).                          |           
010900     05      AX-NOME-DESLOC  PIC X(060).                          |           
011000 01          AX-NOME-R2      REDEFINES   AX-NOME.                 |           
011100     05      AX-NOME-POS-1-3 PIC X(003).                          |           
011200     05      AX-NOME-RESTO   PIC X(058).                          |           
011300 01          AX-NOME-R3      REDEFINES   AX-NOME.                 |           
011400     05      AX-NOME-POS-PAR PIC X(002)  OC  30.                  |           
011500     05      AX-NOME-POS-ULT PIC X(001).                          |           
011600 01          AX-NOME-R4      REDEFINES   AX-NOME.                 |           
011700     05      AX-NOME-43POS   PIC X(043).                          |           
011800     05      AX-NOME-P44-60  PIC X(017).                          |           
011900     05      FILLER          PIC X(001).                          |           
012000                                                                  |           
012100                                                                  |           
012200 01          WS-NOMES.                                            |           
012300     05      WS-NOME1        PIC X(060).                          |           
012400     05      WS-NOME2        PIC X(060).                          |           
012500     05      WS-NOME3        PIC X(060).                          |           
012600     05      WS-NOME4        PIC X(060).                          |           
012700     05      WS-NOME5        PIC X(060).                          |           
012800     05      WS-NOME6        PIC X(060).                          |           
012900     05      WS-NOME7        PIC X(060).                          |           
013000     05      WS-NOME8        PIC X(060).                          |           
013100     05      WS-NOME9        PIC X(060).                          |           
013200     05      WS-NOME10       PIC X(060).                          |           
013300     05      WS-NOME11       PIC X(060).                          |           
013400     05      WS-NOME12       PIC X(060).                          |           
013500     05      WS-NOME13       PIC X(060).                          |           
013600     05      WS-NOME14       PIC X(060).                          |           
013700     05      WS-NOME15       PIC X(060).                          |           
013800                                                                  |           
013900 01          WS-COUNTS.                                           |           
014000     05      WS-COUNT1       PIC 9(002).                          |           
014100     05      WS-COUNT2       PIC 9(002).                          |           
014200     05      WS-COUNT3       PIC 9(002).                          |           
014300     05      WS-COUNT4       PIC 9(002).                          |           
014400     05      WS-COUNT5       PIC 9(002).                          |           
014500     05      WS-COUNT6       PIC 9(002).                          |           
014600     05      WS-COUNT7       PIC 9(002).                          |           
014700     05      WS-COUNT8       PIC 9(002).                          |           
014800     05      WS-COUNT9       PIC 9(002).                          |           
014900     05      WS-COUNT10      PIC 9(002).                          |           
015000     05      WS-COUNT11      PIC 9(002).                          |           
015100     05      WS-COUNT12      PIC 9(002).                          |           
015200     05      WS-COUNT13      PIC 9(002).                          |           
015300     05      WS-COUNT14      PIC 9(002).                          |           
015400     05      WS-COUNT15      PIC 9(002).                          |           
015500                                                                  |           
015600 01          WS-SOBRENOME    PIC X(060).                          |           
015700     88      WS-SOBRENOM     VALUE   "FILHO"                      |           
015800                                     "NETO"                       |           
015900                                     "JUNIOR"                     |           
016000                                     "SOBRINHO"                   |           
016100                                     "I"                          |           
016200                                     "II"                         |           
016300                                     "III"                        |           
016400                                     "PRIMEIRO"                   |           
016500                                     "SEGUNDO"                    |           
016600                                     "TERCEIRO"                   |           
016700                                     "FILHA"                      |           
016800                                     "NETA"                       |           
016900                                     "SOBRINHA"                   |           
017000                                     "JR"                         |           
017100                                     "JR."                        |           
017200                                     "JR,"                        |           
017300                                     "FO"                         |           
017400                                     "FO.".                       |           
017500                                                                  |           
017600                                                                  |           
017700 01          WS-NOME-60P     PIC X(060).                          |           
017800 01          WS-NOME-60P-R   REDEFINES       WS-NOME-60P.         |           
017900     05      WS-NOME-44P     PIC X(044).                          |           
018000     05      FILLER          PIC X(016).                          |           
018100                                                                  |           
018200                                                                  |           
018300                                                                  |           
018400/                                                                 |           
018500*                                                                 |           
018600*------------ AREA DE PASSAGEM DOS PARAMETROS -------------------*|           
018700*                                                                *|           
018800*      (ENTRADA):    LC-NOME-ENTR                                *|           
018900*                                                                *|           
019000*      (SAIDA  ):    LC-RESP   ("C" = CORRETO, "E" = ERRADO )    *|           
019100*                    LC-NOME-SAI                                 *|           
019200*                                                                *|           
019300*----------------------------------------------------------------*|           
019400                                                                  |           
019500 01          LC-PARAM.                                            |           
019600     05      LC-NOME-ENTR    PIC X(060).                          |           
019700     05      LC-RESP         PIC X(001).                          |           
019800     05      LC-NOME-SAI     PIC X(044).                          |           
019900     05      LC-SOBRENOME    PIC X(044).                          |           
020000                                                                  |           
020100                                                                  |           
020200/                                                                 |           
020300 PROCEDURE   DIVISION        USING           LC-PARAM.            |           
020400                                                                  |           
020500*----------------------------------------------------------------*|           
020600*    ROTINA PRINCIPAL DO PROGRAMA.                               *|           
020700*----------------------------------------------------------------*|           
020800*                                                                 |           
020900 000-E-PROGRAMA   SECTION.                                        |           
021000                                                                  |           
021100 000-E-PRINCIPAL.                                                 |           
021200*                                                                 |           
021300                                                                  |           
021400                                                                  |           
021500     MOVE    SPACES                  TO      AX-NOME              |           
021600                                             WS-NOMES             |           
021700                                             WS-NOME-60P          |           
021800                                             WS-SOBRENOME         |           
021900                                             LC-NOME-SAI          |           
022000                                             LC-SOBRENOME.        |           
022100     MOVE    "E"                     TO      LC-RESP.             |           
022200                                                                  |           
022300     MOVE    LOW-VALUES              TO      WS-COUNTS.           |           
022400                                                                  |           
022500*----------------------------------------------------------------*|           
022600                                                                  |           
022700     MOVE    LC-NOME-ENTR            TO      AX-NOME.             |           
022800                                                                  |           
022900                                                                  |           
023000     IF      AX-NOME                 NOT     ALPHABETIC  OR       |           
023100             AX-NOME                 =       SPACES      OR       |           
023200                                             LOW-VALUES           |           
023300             GO                      TO      000-S-PRINCIPAL      |           
023400     ELSE                                                         |           
023500             NEXT    SENTENCE.                                    |           
023600                                                                  |           
023700*----------------------------------------------------------------*|           
023800                                                                  |           
023900     IF      AX-NOME-RESTO           =       SPACES  OR           |           
024000                                             LOW-VALUES           |           
024100             GO                      TO      000-S-PRINCIPAL      |           
024200     ELSE                                                         |           
024300             NEXT    SENTENCE.                                    |           
024400                                                                  |           
024500*----------------------------------------------------------------*|           
024600                                                                  |           
024700     MOVE    "N"                     TO      CH-ERRO              |           
024800                                             CH-ESPACO-DUPLO.     |           
024900                                                                  |           
025000                                                                  |           
025100     PERFORM 010-E-VERIF             THRU    010-S-VERIF          |           
025200             VARYING IX1             FROM    1                    |           
025300                                     BY      1                    |           
025400             UNTIL   IX1             >       30  OR               |           
025500                     CH-ERRO         =       "S".                 |           
025600                                                                  |           
025700                                                                  |           
025800     IF      CH-ERRO                 =       "S"                  |           
025900             GO                      TO      000-S-PRINCIPAL      |           
026000     ELSE                                                         |           
026100             NEXT    SENTENCE.                                    |           
026200                                                                  |           
026300*----------------------------------------------------------------*|           
026400                                                                  |           
026500     MOVE    "N"                     TO      CH-ESPACO-DUPLO.     |           
026600     MOVE    SPACES                  TO      AX-NOME-POS1.        |           
026700     MOVE    LC-NOME-ENTR            TO      AX-NOME-DESLOC.      |           
026800                                                                  |           
026900                                                                  |           
027000     PERFORM 010-E-VERIF             THRU    010-S-VERIF          |           
027100             VARYING IX1             FROM    1                    |           
027200                                     BY      1                    |           
027300             UNTIL   IX1             >       30  OR               |           
027400                     CH-ERRO         =       "S".                 |           
027500                                                                  |           
027600                                                                  |           
027700                                                                  |           
027800     IF      CH-ERRO                 =       "S"                  |           
027900             GO                      TO      000-S-PRINCIPAL      |           
028000     ELSE                                                         |           
028100       IF    CH-ESPACO-DUPLO         =       "S" AND              |           
028200             (AX-NOME-POS-ULT        NOT =   SPACES AND           |           
028300                                             LOW-VALUES)          |           
028400             GO                      TO      000-S-PRINCIPAL      |           
028500       ELSE                                                       |           
028600             NEXT    SENTENCE.                                    |           
028700                                                                  |           
028800*----------------------------------------------------------------*|           
028900                                                                  |           
029000                                                                  |           
029100     MOVE    "C"                     TO      LC-RESP.             |           
029200                                                                  |           
029300                                                                  |           
029400     MOVE    LC-NOME-ENTR            TO      AX-NOME-DESLOC.      |           
029500                                                                  |           
029600                                                                  |           
029700     UNSTRING AX-NOME-DESLOC  DELIMITED BY SPACES  OR LOW-VALUES  |           
029800              INTO    WS-NOME1, COUNT IN  WS-COUNT1               |           
029900                      WS-NOME2, COUNT IN  WS-COUNT2               |           
030000                      WS-NOME3, COUNT IN  WS-COUNT3               |           
030100                      WS-NOME4, COUNT IN  WS-COUNT4               |           
030200                      WS-NOME5, COUNT IN  WS-COUNT5               |           
030300                      WS-NOME6, COUNT IN  WS-COUNT6               |           
030400                      WS-NOME7, COUNT IN  WS-COUNT7               |           
030500                      WS-NOME8, COUNT IN  WS-COUNT8               |           
030600                      WS-NOME9, COUNT IN  WS-COUNT9               |           
030700                      WS-NOME10, COUNT IN  WS-COUNT10             |           
030800                      WS-NOME11, COUNT IN  WS-COUNT11             |           
030900                      WS-NOME12, COUNT IN  WS-COUNT12             |           
031000                      WS-NOME13, COUNT IN  WS-COUNT13             |           
031100                      WS-NOME14, COUNT IN  WS-COUNT14             |           
031200                      WS-NOME15, COUNT IN  WS-COUNT15.            |           
031300                                                                  |           
031400                                                                  |           
031500*----------------------------------------------------------------*|           
031600                                                                  |           
031700                                                                  |           
031705*### 211793 - Formatacao do NOME, SOBRENOME na PID diferenciada   |2.00001    
031710*    REGISTRO 03030897824, CPF 34052105850                        |2.00001    
031715*    NOME:  VINICIUS MURIJO MELATTO                               |2.00001    
031720                                                                  |2.00001    
031725     IF      LC-NOME-ENTR         =  "VINICIUS MURIJO MELATTO"    |2.00001    
031730             MOVE       "VINICIUS"          TO  LC-NOME-SAI       |2.00001    
031735             MOVE       "MURIJO MELATTO"    TO  LC-SOBRENOME      |2.00001    
031740             GO                             TO  000-S-PRINCIPAL.  |2.00001    
031745                                                                  |2.00001    
031750*.................................................................|2.00001    
031755                                                                  |2.00001    
031800     IF      WS-NOME15           NOT =       SPACES  AND          |           
031900                                             LOW-VALUES           |           
032000             MOVE    WS-NOME15       TO      WS-SOBRENOME         |           
032100       IF    WS-SOBRENOM                                          |           
032200             STRING  WS-NOME14 FOR WS-COUNT14,                    |           
032300                     " " FOR 1,                                   |           
032400                     WS-NOME15 FOR WS-COUNT15                     |           
032500                     INTO     LC-SOBRENOME                        |           
032600             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
032700                     " " FOR 1,                                   |           
032800                     WS-NOME2 FOR WS-COUNT2,                      |           
032900                     " " FOR 1,                                   |           
033000                     WS-NOME3 FOR WS-COUNT3,                      |           
033100                     " " FOR 1,                                   |           
033200                     WS-NOME4 FOR WS-COUNT4,                      |           
033300                     " " FOR 1,                                   |           
033400                     WS-NOME5 FOR WS-COUNT5,                      |           
033500                     " " FOR 1,                                   |           
033600                     WS-NOME6 FOR WS-COUNT6,                      |           
033700                     " " FOR 1,                                   |           
033800                     WS-NOME7 FOR WS-COUNT7,                      |           
033900                     " " FOR 1,                                   |           
034000                     WS-NOME8 FOR WS-COUNT8,                      |           
034100                     " " FOR 1,                                   |           
034200                     WS-NOME9 FOR WS-COUNT9,                      |           
034300                     " " FOR 1,                                   |           
034400                     WS-NOME10 FOR WS-COUNT10,                    |           
034500                     " " FOR 1,                                   |           
034600                     WS-NOME11 FOR WS-COUNT11,                    |           
034700                     " " FOR 1                                    |           
034800                     WS-NOME12 FOR WS-COUNT12,                    |           
034900                     " " FOR 1                                    |           
035000                     WS-NOME13 FOR WS-COUNT13                     |           
035100                     INTO     LC-NOME-SAI                         |           
035200             GO                      TO      000-S-PRINCIPAL      |           
035300                                                                  |           
035400       ELSE                                                       |           
035500             MOVE    WS-NOME15       TO      WS-NOME-60P          |           
035600             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
035700             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
035800                     " " FOR 1,                                   |           
035900                     WS-NOME2 FOR WS-COUNT2,                      |           
036000                     " " FOR 1,                                   |           
036100                     WS-NOME3 FOR WS-COUNT3,                      |           
036200                     " " FOR 1,                                   |           
036300                     WS-NOME4 FOR WS-COUNT4,                      |           
036400                     " " FOR 1,                                   |           
036500                     WS-NOME5 FOR WS-COUNT5,                      |           
036600                     " " FOR 1,                                   |           
036700                     WS-NOME6 FOR WS-COUNT6,                      |           
036800                     " " FOR 1,                                   |           
036900                     WS-NOME7 FOR WS-COUNT7,                      |           
037000                     " " FOR 1,                                   |           
037100                     WS-NOME8 FOR WS-COUNT8,                      |           
037200                     " " FOR 1,                                   |           
037300                     WS-NOME9 FOR WS-COUNT9,                      |           
037400                     " " FOR 1,                                   |           
037500                     WS-NOME10 FOR WS-COUNT10,                    |           
037600                     " " FOR 1,                                   |           
037700                     WS-NOME11 FOR WS-COUNT11,                    |           
037800                     " " FOR 1                                    |           
037900                     WS-NOME12 FOR WS-COUNT12,                    |           
038000                     " " FOR 1                                    |           
038100                     WS-NOME13 FOR WS-COUNT13,                    |           
038200                     " " FOR 1                                    |           
038300                     WS-NOME14 FOR WS-COUNT14                     |           
038400                     INTO     LC-NOME-SAI                         |           
038500             GO                      TO      000-S-PRINCIPAL      |           
038600     ELSE                                                         |           
038700             NEXT    SENTENCE.                                    |           
038800                                                                  |           
038900                                                                  |           
039000*----------------------------------------------------------------*|           
039100                                                                  |           
039200                                                                  |           
039300     IF      WS-NOME14           NOT =       SPACES  AND          |           
039400                                             LOW-VALUES           |           
039500             MOVE    WS-NOME14       TO      WS-SOBRENOME         |           
039600       IF    WS-SOBRENOM                                          |           
039700             STRING  WS-NOME13 FOR WS-COUNT13,                    |           
039800                     " " FOR 1,                                   |           
039900                     WS-NOME14 FOR WS-COUNT14                     |           
040000                     INTO     LC-SOBRENOME                        |           
040100             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
040200                     " " FOR 1,                                   |           
040300                     WS-NOME2 FOR WS-COUNT2,                      |           
040400                     " " FOR 1,                                   |           
040500                     WS-NOME3 FOR WS-COUNT3,                      |           
040600                     " " FOR 1,                                   |           
040700                     WS-NOME4 FOR WS-COUNT4,                      |           
040800                     " " FOR 1,                                   |           
040900                     WS-NOME5 FOR WS-COUNT5,                      |           
041000                     " " FOR 1,                                   |           
041100                     WS-NOME6 FOR WS-COUNT6,                      |           
041200                     " " FOR 1,                                   |           
041300                     WS-NOME7 FOR WS-COUNT7,                      |           
041400                     " " FOR 1,                                   |           
041500                     WS-NOME8 FOR WS-COUNT8,                      |           
041600                     " " FOR 1,                                   |           
041700                     WS-NOME9 FOR WS-COUNT9,                      |           
041800                     " " FOR 1,                                   |           
041900                     WS-NOME10 FOR WS-COUNT10,                    |           
042000                     " " FOR 1,                                   |           
042100                     WS-NOME11 FOR WS-COUNT11,                    |           
042200                     " " FOR 1                                    |           
042300                     WS-NOME12 FOR WS-COUNT12                     |           
042400                     INTO     LC-NOME-SAI                         |           
042500             GO                      TO      000-S-PRINCIPAL      |           
042600                                                                  |           
042700       ELSE                                                       |           
042800             MOVE    WS-NOME14       TO      WS-NOME-60P          |           
042900             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
043000             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
043100                     " " FOR 1,                                   |           
043200                     WS-NOME2 FOR WS-COUNT2,                      |           
043300                     " " FOR 1,                                   |           
043400                     WS-NOME3 FOR WS-COUNT3,                      |           
043500                     " " FOR 1,                                   |           
043600                     WS-NOME4 FOR WS-COUNT4,                      |           
043700                     " " FOR 1,                                   |           
043800                     WS-NOME5 FOR WS-COUNT5,                      |           
043900                     " " FOR 1,                                   |           
044000                     WS-NOME6 FOR WS-COUNT6,                      |           
044100                     " " FOR 1,                                   |           
044200                     WS-NOME7 FOR WS-COUNT7,                      |           
044300                     " " FOR 1,                                   |           
044400                     WS-NOME8 FOR WS-COUNT8,                      |           
044500                     " " FOR 1,                                   |           
044600                     WS-NOME9 FOR WS-COUNT9,                      |           
044700                     " " FOR 1,                                   |           
044800                     WS-NOME10 FOR WS-COUNT10,                    |           
044900                     " " FOR 1,                                   |           
045000                     WS-NOME11 FOR WS-COUNT11,                    |           
045100                     " " FOR 1                                    |           
045200                     WS-NOME12 FOR WS-COUNT12,                    |           
045300                     " " FOR 1                                    |           
045400                     WS-NOME13 FOR WS-COUNT13                     |           
045500                     INTO     LC-NOME-SAI                         |           
045600             GO                      TO      000-S-PRINCIPAL      |           
045700     ELSE                                                         |           
045800             NEXT    SENTENCE.                                    |           
045900                                                                  |           
046000                                                                  |           
046100*----------------------------------------------------------------*|           
046200                                                                  |           
046300                                                                  |           
046400     IF      WS-NOME13           NOT =       SPACES  AND          |           
046500                                             LOW-VALUES           |           
046600             MOVE    WS-NOME13       TO      WS-SOBRENOME         |           
046700       IF    WS-SOBRENOM                                          |           
046800             STRING  WS-NOME12 FOR WS-COUNT12,                    |           
046900                     " " FOR 1,                                   |           
047000                     WS-NOME13 FOR WS-COUNT13                     |           
047100                     INTO     LC-SOBRENOME                        |           
047200             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
047300                     " " FOR 1,                                   |           
047400                     WS-NOME2 FOR WS-COUNT2,                      |           
047500                     " " FOR 1,                                   |           
047600                     WS-NOME3 FOR WS-COUNT3,                      |           
047700                     " " FOR 1,                                   |           
047800                     WS-NOME4 FOR WS-COUNT4,                      |           
047900                     " " FOR 1,                                   |           
048000                     WS-NOME5 FOR WS-COUNT5,                      |           
048100                     " " FOR 1,                                   |           
048200                     WS-NOME6 FOR WS-COUNT6,                      |           
048300                     " " FOR 1,                                   |           
048400                     WS-NOME7 FOR WS-COUNT7,                      |           
048500                     " " FOR 1,                                   |           
048600                     WS-NOME8 FOR WS-COUNT8,                      |           
048700                     " " FOR 1,                                   |           
048800                     WS-NOME9 FOR WS-COUNT9,                      |           
048900                     " " FOR 1,                                   |           
049000                     WS-NOME10 FOR WS-COUNT10,                    |           
049100                     " " FOR 1,                                   |           
049200                     WS-NOME11 FOR WS-COUNT11                     |           
049300                     INTO     LC-NOME-SAI                         |           
049400             GO                      TO      000-S-PRINCIPAL      |           
049500                                                                  |           
049600       ELSE                                                       |           
049700             MOVE    WS-NOME13       TO      WS-NOME-60P          |           
049800             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
049900             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
050000                     " " FOR 1,                                   |           
050100                     WS-NOME2 FOR WS-COUNT2,                      |           
050200                     " " FOR 1,                                   |           
050300                     WS-NOME3 FOR WS-COUNT3,                      |           
050400                     " " FOR 1,                                   |           
050500                     WS-NOME4 FOR WS-COUNT4,                      |           
050600                     " " FOR 1,                                   |           
050700                     WS-NOME5 FOR WS-COUNT5,                      |           
050800                     " " FOR 1,                                   |           
050900                     WS-NOME6 FOR WS-COUNT6,                      |           
051000                     " " FOR 1,                                   |           
051100                     WS-NOME7 FOR WS-COUNT7,                      |           
051200                     " " FOR 1,                                   |           
051300                     WS-NOME8 FOR WS-COUNT8,                      |           
051400                     " " FOR 1,                                   |           
051500                     WS-NOME9 FOR WS-COUNT9,                      |           
051600                     " " FOR 1,                                   |           
051700                     WS-NOME10 FOR WS-COUNT10,                    |           
051800                     " " FOR 1,                                   |           
051900                     WS-NOME11 FOR WS-COUNT11,                    |           
052000                     " " FOR 1                                    |           
052100                     WS-NOME12 FOR WS-COUNT12                     |           
052200                     INTO     LC-NOME-SAI                         |           
052300             GO                      TO      000-S-PRINCIPAL      |           
052400     ELSE                                                         |           
052500             NEXT    SENTENCE.                                    |           
052600                                                                  |           
052700                                                                  |           
052800*----------------------------------------------------------------*|           
052900                                                                  |           
053000                                                                  |           
053100     IF      WS-NOME12           NOT =       SPACES  AND          |           
053200                                             LOW-VALUES           |           
053300             MOVE    WS-NOME12       TO      WS-SOBRENOME         |           
053400       IF    WS-SOBRENOM                                          |           
053500             STRING  WS-NOME11 FOR WS-COUNT11,                    |           
053600                     " " FOR 1,                                   |           
053700                     WS-NOME12 FOR WS-COUNT12                     |           
053800                     INTO     LC-SOBRENOME                        |           
053900             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
054000                     " " FOR 1,                                   |           
054100                     WS-NOME2 FOR WS-COUNT2,                      |           
054200                     " " FOR 1,                                   |           
054300                     WS-NOME3 FOR WS-COUNT3,                      |           
054400                     " " FOR 1,                                   |           
054500                     WS-NOME4 FOR WS-COUNT4,                      |           
054600                     " " FOR 1,                                   |           
054700                     WS-NOME5 FOR WS-COUNT5,                      |           
054800                     " " FOR 1,                                   |           
054900                     WS-NOME6 FOR WS-COUNT6,                      |           
055000                     " " FOR 1,                                   |           
055100                     WS-NOME7 FOR WS-COUNT7,                      |           
055200                     " " FOR 1,                                   |           
055300                     WS-NOME8 FOR WS-COUNT8,                      |           
055400                     " " FOR 1,                                   |           
055500                     WS-NOME9 FOR WS-COUNT9,                      |           
055600                     " " FOR 1,                                   |           
055700                     WS-NOME10 FOR WS-COUNT10                     |           
055800                     INTO     LC-NOME-SAI                         |           
055900             GO                      TO      000-S-PRINCIPAL      |           
056000                                                                  |           
056100       ELSE                                                       |           
056200             MOVE    WS-NOME12       TO      WS-NOME-60P          |           
056300             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
056400             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
056500                     " " FOR 1,                                   |           
056600                     WS-NOME2 FOR WS-COUNT2,                      |           
056700                     " " FOR 1,                                   |           
056800                     WS-NOME3 FOR WS-COUNT3,                      |           
056900                     " " FOR 1,                                   |           
057000                     WS-NOME4 FOR WS-COUNT4,                      |           
057100                     " " FOR 1,                                   |           
057200                     WS-NOME5 FOR WS-COUNT5,                      |           
057300                     " " FOR 1,                                   |           
057400                     WS-NOME6 FOR WS-COUNT6,                      |           
057500                     " " FOR 1,                                   |           
057600                     WS-NOME7 FOR WS-COUNT7,                      |           
057700                     " " FOR 1,                                   |           
057800                     WS-NOME8 FOR WS-COUNT8,                      |           
057900                     " " FOR 1,                                   |           
058000                     WS-NOME9 FOR WS-COUNT9,                      |           
058100                     " " FOR 1,                                   |           
058200                     WS-NOME10 FOR WS-COUNT10,                    |           
058300                     " " FOR 1,                                   |           
058400                     WS-NOME11 FOR WS-COUNT11                     |           
058500                     INTO    LC-NOME-SAI                          |           
058600             GO                      TO      000-S-PRINCIPAL      |           
058700     ELSE                                                         |           
058800             NEXT    SENTENCE.                                    |           
058900                                                                  |           
059000                                                                  |           
059100*----------------------------------------------------------------*|           
059200                                                                  |           
059300                                                                  |           
059400     IF      WS-NOME11           NOT =       SPACES  AND          |           
059500                                             LOW-VALUES           |           
059600             MOVE    WS-NOME11       TO      WS-SOBRENOME         |           
059700       IF    WS-SOBRENOM                                          |           
059800             STRING  WS-NOME11 FOR WS-COUNT11,                    |           
059900                     " " FOR 1,                                   |           
060000                     WS-NOME10 FOR WS-COUNT10                     |           
060100                     INTO     LC-SOBRENOME                        |           
060200             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
060300                     " " FOR 1,                                   |           
060400                     WS-NOME2 FOR WS-COUNT2,                      |           
060500                     " " FOR 1,                                   |           
060600                     WS-NOME3 FOR WS-COUNT3,                      |           
060700                     " " FOR 1,                                   |           
060800                     WS-NOME4 FOR WS-COUNT4,                      |           
060900                     " " FOR 1,                                   |           
061000                     WS-NOME5 FOR WS-COUNT5,                      |           
061100                     " " FOR 1,                                   |           
061200                     WS-NOME6 FOR WS-COUNT6,                      |           
061300                     " " FOR 1,                                   |           
061400                     WS-NOME7 FOR WS-COUNT7,                      |           
061500                     " " FOR 1,                                   |           
061600                     WS-NOME8 FOR WS-COUNT8,                      |           
061700                     " " FOR 1,                                   |           
061800                     WS-NOME9 FOR WS-COUNT9                       |           
061900                     INTO     LC-NOME-SAI                         |           
062000             GO                      TO      000-S-PRINCIPAL      |           
062100                                                                  |           
062200       ELSE                                                       |           
062300             MOVE    WS-NOME11       TO      WS-NOME-60P          |           
062400             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
062500             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
062600                     " " FOR 1,                                   |           
062700                     WS-NOME2 FOR WS-COUNT2,                      |           
062800                     " " FOR 1,                                   |           
062900                     WS-NOME3 FOR WS-COUNT3,                      |           
063000                     " " FOR 1,                                   |           
063100                     WS-NOME4 FOR WS-COUNT4,                      |           
063200                     " " FOR 1,                                   |           
063300                     WS-NOME5 FOR WS-COUNT5,                      |           
063400                     " " FOR 1,                                   |           
063500                     WS-NOME6 FOR WS-COUNT6,                      |           
063600                     " " FOR 1,                                   |           
063700                     WS-NOME7 FOR WS-COUNT7,                      |           
063800                     " " FOR 1,                                   |           
063900                     WS-NOME8 FOR WS-COUNT8,                      |           
064000                     " " FOR 1,                                   |           
064100                     WS-NOME9 FOR WS-COUNT9,                      |           
064200                     " " FOR 1,                                   |           
064300                     WS-NOME10 FOR WS-COUNT10                     |           
064400                     INTO    LC-NOME-SAI                          |           
064500             GO                      TO      000-S-PRINCIPAL      |           
064600     ELSE                                                         |           
064700             NEXT    SENTENCE.                                    |           
064800                                                                  |           
064900                                                                  |           
065000*----------------------------------------------------------------*|           
065100                                                                  |           
065200                                                                  |           
065300     IF      WS-NOME10           NOT =       SPACES  AND          |           
065400                                             LOW-VALUES           |           
065500             MOVE    WS-NOME10       TO      WS-SOBRENOME         |           
065600       IF    WS-SOBRENOM                                          |           
065700             STRING  WS-NOME9  FOR WS-COUNT9,                     |           
065800                     " " FOR 1,                                   |           
065900                     WS-NOME10 FOR WS-COUNT10                     |           
066000                     INTO     LC-SOBRENOME                        |           
066100             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
066200                     " " FOR 1,                                   |           
066300                     WS-NOME2 FOR WS-COUNT2,                      |           
066400                     " " FOR 1,                                   |           
066500                     WS-NOME3 FOR WS-COUNT3,                      |           
066600                     " " FOR 1,                                   |           
066700                     WS-NOME4 FOR WS-COUNT4,                      |           
066800                     " " FOR 1,                                   |           
066900                     WS-NOME5 FOR WS-COUNT5,                      |           
067000                     " " FOR 1,                                   |           
067100                     WS-NOME6 FOR WS-COUNT6,                      |           
067200                     " " FOR 1,                                   |           
067300                     WS-NOME7 FOR WS-COUNT7,                      |           
067400                     " " FOR 1,                                   |           
067500                     WS-NOME8 FOR WS-COUNT8                       |           
067600                     INTO     LC-NOME-SAI                         |           
067700             GO                      TO      000-S-PRINCIPAL      |           
067800                                                                  |           
067900       ELSE                                                       |           
068000             MOVE    WS-NOME10       TO      WS-NOME-60P          |           
068100             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
068200             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
068300                     " " FOR 1,                                   |           
068400                     WS-NOME2 FOR WS-COUNT2,                      |           
068500                     " " FOR 1,                                   |           
068600                     WS-NOME3 FOR WS-COUNT3,                      |           
068700                     " " FOR 1,                                   |           
068800                     WS-NOME4 FOR WS-COUNT4,                      |           
068900                     " " FOR 1,                                   |           
069000                     WS-NOME5 FOR WS-COUNT5,                      |           
069100                     " " FOR 1,                                   |           
069200                     WS-NOME6 FOR WS-COUNT6,                      |           
069300                     " " FOR 1,                                   |           
069400                     WS-NOME7 FOR WS-COUNT7,                      |           
069500                     " " FOR 1,                                   |           
069600                     WS-NOME8 FOR WS-COUNT8,                      |           
069700                     " " FOR 1,                                   |           
069800                     WS-NOME9 FOR WS-COUNT9                       |           
069900                     INTO     LC-NOME-SAI                         |           
070000             GO                      TO      000-S-PRINCIPAL      |           
070100     ELSE                                                         |           
070200             NEXT    SENTENCE.                                    |           
070300                                                                  |           
070400                                                                  |           
070500                                                                  |           
070600*----------------------------------------------------------------*|           
070700                                                                  |           
070800                                                                  |           
070900     IF      WS-NOME9            NOT =       SPACES  AND          |           
071000                                             LOW-VALUES           |           
071100             MOVE    WS-NOME9        TO      WS-SOBRENOME         |           
071200       IF    WS-SOBRENOM                                          |           
071300             STRING  WS-NOME8  FOR WS-COUNT8,                     |           
071400                     " " FOR 1,                                   |           
071500                     WS-NOME9 FOR WS-COUNT9                       |           
071600                     INTO     LC-SOBRENOME                        |           
071700             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
071800                     " " FOR 1,                                   |           
071900                     WS-NOME2 FOR WS-COUNT2,                      |           
072000                     " " FOR 1,                                   |           
072100                     WS-NOME3 FOR WS-COUNT3,                      |           
072200                     " " FOR 1,                                   |           
072300                     WS-NOME4 FOR WS-COUNT4,                      |           
072400                     " " FOR 1,                                   |           
072500                     WS-NOME5 FOR WS-COUNT5,                      |           
072600                     " " FOR 1,                                   |           
072700                     WS-NOME6 FOR WS-COUNT6,                      |           
072800                     " " FOR 1,                                   |           
072900                     WS-NOME7 FOR WS-COUNT7                       |           
073000                     INTO    LC-NOME-SAI                          |           
073100             GO                      TO      000-S-PRINCIPAL      |           
073200                                                                  |           
073300       ELSE                                                       |           
073400             MOVE    WS-NOME9        TO      WS-NOME-60P          |           
073500             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
073600             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
073700                     " " FOR 1,                                   |           
073800                     WS-NOME2 FOR WS-COUNT2,                      |           
073900                     " " FOR 1,                                   |           
074000                     WS-NOME3 FOR WS-COUNT3,                      |           
074100                     " " FOR 1,                                   |           
074200                     WS-NOME4 FOR WS-COUNT4,                      |           
074300                     " " FOR 1,                                   |           
074400                     WS-NOME5 FOR WS-COUNT5,                      |           
074500                     " " FOR 1,                                   |           
074600                     WS-NOME6 FOR WS-COUNT6,                      |           
074700                     " " FOR 1,                                   |           
074800                     WS-NOME7 FOR WS-COUNT7,                      |           
074900                     " " FOR 1,                                   |           
075000                     WS-NOME8 FOR WS-COUNT8                       |           
075100                     INTO    LC-NOME-SAI                          |           
075200             GO                      TO      000-S-PRINCIPAL      |           
075300     ELSE                                                         |           
075400             NEXT    SENTENCE.                                    |           
075500                                                                  |           
075600                                                                  |           
075700                                                                  |           
075800*----------------------------------------------------------------*|           
075900                                                                  |           
076000                                                                  |           
076100     IF      WS-NOME8            NOT =       SPACES  AND          |           
076200                                             LOW-VALUES           |           
076300             MOVE    WS-NOME8        TO      WS-SOBRENOME         |           
076400       IF    WS-SOBRENOM                                          |           
076500             STRING  WS-NOME7  FOR WS-COUNT7,                     |           
076600                     " " FOR 1,                                   |           
076700                     WS-NOME8  FOR WS-COUNT8                      |           
076800                     INTO     LC-SOBRENOME                        |           
076900             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
077000                     " " FOR 1,                                   |           
077100                     WS-NOME2 FOR WS-COUNT2,                      |           
077200                     " " FOR 1,                                   |           
077300                     WS-NOME3 FOR WS-COUNT3,                      |           
077400                     " " FOR 1,                                   |           
077500                     WS-NOME4 FOR WS-COUNT4,                      |           
077600                     " " FOR 1,                                   |           
077700                     WS-NOME5 FOR WS-COUNT5,                      |           
077800                     " " FOR 1,                                   |           
077900                     WS-NOME6 FOR WS-COUNT6                       |           
078000                     INTO     LC-NOME-SAI                         |           
078100             GO                      TO      000-S-PRINCIPAL      |           
078200                                                                  |           
078300       ELSE                                                       |           
078400             MOVE    WS-NOME8        TO      WS-NOME-60P          |           
078500             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
078600             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
078700                     " " FOR 1,                                   |           
078800                     WS-NOME2 FOR WS-COUNT2,                      |           
078900                     " " FOR 1,                                   |           
079000                     WS-NOME3 FOR WS-COUNT3,                      |           
079100                     " " FOR 1,                                   |           
079200                     WS-NOME4 FOR WS-COUNT4,                      |           
079300                     " " FOR 1,                                   |           
079400                     WS-NOME5 FOR WS-COUNT5,                      |           
079500                     " " FOR 1,                                   |           
079600                     WS-NOME6 FOR WS-COUNT6,                      |           
079700                     " " FOR 1,                                   |           
079800                     WS-NOME7 FOR WS-COUNT7                       |           
079900                     INTO     LC-NOME-SAI                         |           
080000             GO                      TO      000-S-PRINCIPAL      |           
080100     ELSE                                                         |           
080200             NEXT    SENTENCE.                                    |           
080300                                                                  |           
080400                                                                  |           
080500*----------------------------------------------------------------*|           
080600                                                                  |           
080700                                                                  |           
080800     IF      WS-NOME7            NOT =       SPACES  AND          |           
080900                                             LOW-VALUES           |           
081000             MOVE    WS-NOME7        TO      WS-SOBRENOME         |           
081100       IF    WS-SOBRENOM                                          |           
081200             STRING  WS-NOME6  FOR WS-COUNT6,                     |           
081300                     " " FOR 1,                                   |           
081400                     WS-NOME7  FOR WS-COUNT7                      |           
081500                     INTO     LC-SOBRENOME                        |           
081600             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
081700                     " " FOR 1,                                   |           
081800                     WS-NOME2 FOR WS-COUNT2,                      |           
081900                     " " FOR 1,                                   |           
082000                     WS-NOME3 FOR WS-COUNT3,                      |           
082100                     " " FOR 1,                                   |           
082200                     WS-NOME4 FOR WS-COUNT4,                      |           
082300                     " " FOR 1,                                   |           
082400                     WS-NOME5 FOR WS-COUNT5,                      |           
082500                     INTO     LC-NOME-SAI                         |           
082600             GO                      TO      000-S-PRINCIPAL      |           
082700                                                                  |           
082800       ELSE                                                       |           
082900             MOVE    WS-NOME7        TO      WS-NOME-60P          |           
083000             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
083100             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
083200                     " " FOR 1,                                   |           
083300                     WS-NOME2 FOR WS-COUNT2,                      |           
083400                     " " FOR 1,                                   |           
083500                     WS-NOME3 FOR WS-COUNT3,                      |           
083600                     " " FOR 1,                                   |           
083700                     WS-NOME4 FOR WS-COUNT4,                      |           
083800                     " " FOR 1,                                   |           
083900                     WS-NOME5 FOR WS-COUNT5,                      |           
084000                     " " FOR 1,                                   |           
084100                     WS-NOME6 FOR WS-COUNT6                       |           
084200                     INTO     LC-NOME-SAI                         |           
084300             GO                      TO      000-S-PRINCIPAL      |           
084400     ELSE                                                         |           
084500             NEXT    SENTENCE.                                    |           
084600                                                                  |           
084700                                                                  |           
084800*----------------------------------------------------------------*|           
084900                                                                  |           
085000                                                                  |           
085100     IF      WS-NOME6            NOT =       SPACES  AND          |           
085200                                             LOW-VALUES           |           
085300             MOVE    WS-NOME6        TO      WS-SOBRENOME         |           
085400       IF    WS-SOBRENOM                                          |           
085500             STRING  WS-NOME5  FOR WS-COUNT5,                     |           
085600                     " " FOR 1,                                   |           
085700                     WS-NOME6  FOR WS-COUNT6                      |           
085800                     INTO     LC-SOBRENOME                        |           
085900             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
086000                     " " FOR 1,                                   |           
086100                     WS-NOME2 FOR WS-COUNT2,                      |           
086200                     " " FOR 1,                                   |           
086300                     WS-NOME3 FOR WS-COUNT3,                      |           
086400                     " " FOR 1,                                   |           
086500                     WS-NOME4 FOR WS-COUNT4                       |           
086600                     INTO     LC-NOME-SAI                         |           
086700             GO                      TO      000-S-PRINCIPAL      |           
086800                                                                  |           
086900       ELSE                                                       |           
087000             MOVE    WS-NOME6        TO      WS-NOME-60P          |           
087100             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
087200             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
087300                     " " FOR 1,                                   |           
087400                     WS-NOME2 FOR WS-COUNT2,                      |           
087500                     " " FOR 1,                                   |           
087600                     WS-NOME3 FOR WS-COUNT3,                      |           
087700                     " " FOR 1,                                   |           
087800                     WS-NOME4 FOR WS-COUNT4,                      |           
087900                     " " FOR 1,                                   |           
088000                     WS-NOME5 FOR WS-COUNT5                       |           
088100                     INTO     LC-NOME-SAI                         |           
088200             GO                      TO      000-S-PRINCIPAL      |           
088300     ELSE                                                         |           
088400             NEXT    SENTENCE.                                    |           
088500                                                                  |           
088600                                                                  |           
088700*----------------------------------------------------------------*|           
088800                                                                  |           
088900                                                                  |           
089000     IF      WS-NOME5            NOT =       SPACES  AND          |           
089100                                             LOW-VALUES           |           
089200             MOVE    WS-NOME5        TO      WS-SOBRENOME         |           
089300       IF    WS-SOBRENOM                                          |           
089400             STRING  WS-NOME4  FOR WS-COUNT4,                     |           
089500                     " " FOR 1,                                   |           
089600                     WS-NOME5  FOR WS-COUNT5                      |           
089700                     INTO     LC-SOBRENOME                        |           
089800             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
089900                     " " FOR 1,                                   |           
090000                     WS-NOME2 FOR WS-COUNT2,                      |           
090100                     " " FOR 1,                                   |           
090200                     WS-NOME3 FOR WS-COUNT3                       |           
090300                     INTO     LC-NOME-SAI                         |           
090400             GO                      TO      000-S-PRINCIPAL      |           
090500                                                                  |           
090600       ELSE                                                       |           
090700             MOVE    WS-NOME5        TO      WS-NOME-60P          |           
090800             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
090900             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
091000                     " " FOR 1,                                   |           
091100                     WS-NOME2 FOR WS-COUNT2,                      |           
091200                     " " FOR 1,                                   |           
091300                     WS-NOME3 FOR WS-COUNT3,                      |           
091400                     " " FOR 1,                                   |           
091500                     WS-NOME4 FOR WS-COUNT4                       |           
091600                     INTO     LC-NOME-SAI                         |           
091700             GO                      TO      000-S-PRINCIPAL      |           
091800     ELSE                                                         |           
091900             NEXT    SENTENCE.                                    |           
092000                                                                  |           
092100                                                                  |           
092200*----------------------------------------------------------------*|           
092300                                                                  |           
092400                                                                  |           
092500     IF      WS-NOME4            NOT =       SPACES  AND          |           
092600                                             LOW-VALUES           |           
092700             MOVE    WS-NOME4        TO      WS-SOBRENOME         |           
092800       IF    WS-SOBRENOM                                          |           
092900             STRING  WS-NOME3  FOR WS-COUNT3,                     |           
093000                     " " FOR 1,                                   |           
093100                     WS-NOME4  FOR WS-COUNT4                      |           
093200                     INTO     LC-SOBRENOME                        |           
093300             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
093400                     " " FOR 1,                                   |           
093500                     WS-NOME2 FOR WS-COUNT2                       |           
093600                     INTO     LC-NOME-SAI                         |           
093700             GO                      TO      000-S-PRINCIPAL      |           
093800                                                                  |           
093900       ELSE                                                       |           
094000             MOVE    WS-NOME4        TO      WS-NOME-60P          |           
094100             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
094200             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
094300                     " " FOR 1,                                   |           
094400                     WS-NOME2 FOR WS-COUNT2,                      |           
094500                     " " FOR 1,                                   |           
094600                     WS-NOME3 FOR WS-COUNT3                       |           
094700                     INTO     LC-NOME-SAI                         |           
094800             GO                      TO      000-S-PRINCIPAL      |           
094900     ELSE                                                         |           
095000             NEXT    SENTENCE.                                    |           
095100                                                                  |           
095200                                                                  |           
095300*----------------------------------------------------------------*|           
095400                                                                  |           
095500                                                                  |           
095600     IF      WS-NOME3            NOT =       SPACES  AND          |           
095700                                             LOW-VALUES           |           
095800             MOVE    WS-NOME3        TO      WS-SOBRENOME         |           
095900       IF    WS-SOBRENOM                                          |           
096000             STRING  WS-NOME2 FOR WS-COUNT2,                      |           
096100                     " " FOR 1,                                   |           
096200                     WS-NOME3 FOR WS-COUNT3                       |           
096300                     INTO     LC-SOBRENOME                        |           
096400             STRING  WS-NOME1 FOR WS-COUNT1                       |           
096500                     INTO     LC-NOME-SAI                         |           
096600             GO                      TO      000-S-PRINCIPAL      |           
096700                                                                  |           
096800       ELSE                                                       |           
096900             MOVE    WS-NOME3        TO      WS-NOME-60P          |           
097000             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
097100             STRING  WS-NOME1 FOR WS-COUNT1,                      |           
097200                     " " FOR 1,                                   |           
097300                     WS-NOME2 FOR WS-COUNT2                       |           
097400                     INTO     LC-NOME-SAI                         |           
097500             GO                      TO      000-S-PRINCIPAL      |           
097600     ELSE                                                         |           
097700             NEXT    SENTENCE.                                    |           
097800                                                                  |           
097900                                                                  |           
098000*----------------------------------------------------------------*|           
098100                                                                  |           
098200                                                                  |           
098300     IF      WS-NOME2            NOT =       SPACES  AND          |           
098400                                             LOW-VALUES           |           
098500             MOVE    WS-NOME2        TO      WS-SOBRENOME         |           
098600       IF    WS-SOBRENOM                                          |           
098700             STRING  WS-NOME2  FOR WS-COUNT2                      |           
098800                     INTO     LC-SOBRENOME                        |           
098900             STRING  WS-NOME1 FOR WS-COUNT1                       |           
099000                     INTO    LC-NOME-SAI                          |           
099100             GO                      TO      000-S-PRINCIPAL      |           
099200                                                                  |           
099300       ELSE                                                       |           
099400             MOVE    WS-NOME2        TO      WS-NOME-60P          |           
099500             MOVE    WS-NOME-44P     TO      LC-SOBRENOME         |           
099600             MOVE    SPACES          TO      WS-NOME-60P          |           
099700             MOVE    WS-NOME1        TO      WS-NOME-60P          |           
099800             MOVE    WS-NOME-44P     TO      LC-NOME-SAI          |           
099900             GO                      TO      000-S-PRINCIPAL      |           
100000     ELSE                                                         |           
100100             MOVE    WS-NOME1        TO      WS-NOME-60P          |           
100200             MOVE    WS-NOME-44P     TO      LC-NOME-SAI          |           
100300             MOVE    SPACES          TO      LC-SOBRENOME.        |           
100400                                                                  |           
100500                                                                  |           
100600                                                                  |           
100700                                                                  |           
100800                                                                  |           
100900                                                                  |           
101000                                                                  |           
101100 000-S-PRINCIPAL.                                                 |           
101200     EXIT    PROGRAM.                                             |           
101300                                                                  |           
101400*----------------------------------------------------------------*|           
101500                                                                  |           
101600/                                                                 |           
101700*----------------------------------------------------------------*|           
101800*    VERIFICAR  ESPACO  DUPLO  ENTRE  CARACTERES                 *|           
101900*----------------------------------------------------------------*|           
102000                                                                  |           
102100 010-E-VERIF.                                                     |           
102200                                                                  |           
102300                                                                  |           
102400                                                                  |           
102500     IF      AX-NOME-POS-PAR (IX1)   =       SPACES  OR           |           
102600                                             LOW-VALUES           |           
102700             MOVE    "S"             TO      CH-ESPACO-DUPLO      |           
102800     ELSE                                                         |           
102900       IF    CH-ESPACO-DUPLO         =       "S"                  |           
103000             MOVE    "S"             TO      CH-ERRO              |           
103100       ELSE                                                       |           
103200             NEXT    SENTENCE.                                    |           
103300                                                                  |           
103400                                                                  |           
103500                                                                  |           
103600 010-S-VERIF.                                                     |           
103700     EXIT.                                                        |           
103800                                                                  |           
103900                                                                  |           
104000                                                                  |           
