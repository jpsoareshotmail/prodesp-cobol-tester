000000* VERSION   1.1  ; SAVED 20210816 10:08:35                    |000|0001.01    
000100$$SET SHARING=PRIVATE                                             |           
000200$$SET TEMPORARY                                                   |           
000300 IDENTIFICATION  DIVISION.                                        |           
000400**************************                                        |           
000500*                                                                 |           
000600*                                                                 |           
000700*PROGRAM-ID.     PC/GAT/L030/DB.                                  |           
000800 AUTHOR.         JORGE CORTEZ.                                    |           
000900*                                                                 |           
001000*ANALISTA        JORGE CORTEZ.                                    |           
001100*                                                                 |           
001200 DATE-WRITTEN.   18/06/2021.                                      |           
001300 DATE-COMPILED.                                                   |           
001400*                                                                 |           
001500*----------------------------------------------------------------*|           
001600*                                                                *|           
001700*    O B J E T I V O :                                           *|           
001800*                                                                *|           
001900*    PESQUISA NO BANCO BLOQUEIODS E RETORNA OS TIPOS DE          *|           
002000*          RESTRICAO QUE SERµO ENVIADOS PARA A BIN.              *|           
002100*                                                                *|           
002200*                                                                *|           
002300*                                                                *|           
002400*                                                                *|           
002500*----------------------------------------------------------------*|           
002600*                                                                *|           
002700*            A L T E R A C O E S   E F E T U A D A S             *|           
002800*            ---------------------------------------             *|           
002900*                                                                *|           
003000*      DATA      ANA / PROG    COMENTARIO                        *|           
003100*    --------    ----  -----   --------------------------------- *|           
003200*                                                                *|           
003300*    --/--/--    ----  -----   --------------------------------- *|           
003400*    --/--/--    ----  -----   --------------------------------- *|           
003500*    --/--/--    ----  -----   --------------------------------- *|           
003600*    --/--/--    ----  -----   --------------------------------- *|           
003700*    --/--/--    ----  -----   --------------------------------- *|           
003800*    --/--/--    ----  -----   --------------------------------- *|           
003900*    --/--/--    ----  -----   --------------------------------- *|           
004000*    --/--/--    ----  -----   --------------------------------- *|           
004100*    --/--/--    ----  -----   --------------------------------- *|           
004200*    --/--/--    ----  -----   --------------------------------- *|           
004300*    --/--/--    ----  -----   --------------------------------- *|           
004400*    --/--/--    ----  -----   --------------------------------- *|           
004500*    --/--/--    ----  -----   --------------------------------- *|           
004600*    --/--/--    ----  -----   --------------------------------- *|           
004700*    --/--/--    ----  -----   --------------------------------- *|           
004800*    --/--/--    ----  -----   --------------------------------- *|           
004900*                                                                *|           
005000*----------------------------------------------------------------*|           
005100*                                                                *|           
005200*----------------------------------------------------------------*|           
005300/                                                                 |           
005400 ENVIRONMENT     DIVISION.                                        |           
005500**************************                                        |           
005600*                                                                 |           
005700*                                                                 |           
005800 CONFIGURATION   SECTION.                                         |           
005900*************************                                         |           
006000*                                                                 |           
006100 SPECIAL-NAMES.                                                   |           
006200*                                                                 |           
006300     DECIMAL-POINT           IS      COMMA.                       |           
006400*                                                                 |           
006500/                                                                 |           
006600 DATA            DIVISION.                                        |           
006700**************************                                        |           
006800*                                                                 |           
006900*                                                                 |           
007000*                                                                 |           
007100*                                                                 |           
007200 DATA-BASE       SECTION.                                         |           
007300*************************                                         |           
007400*                                                                 |           
007500*                                                                 |           
007600 DB          DB01    =       TDBBLOQUEIOS.                        |           
007700*                                                                 |           
007800*                                                                 |           
007900 01          BLOQUEIODS.                                          |           
008000                                                                  |           
008100/                                                                 |           
008200 01          RENAJUDDS.                                           |           
008300*                                                                 |           
008400                                                                  |           
008500*                                                                 |           
008600*                                                                 |           
008700 WORKING-STORAGE SECTION.                                         |           
008800*                                                                 |           
008900*                                                                 |           
009000*                                                                 |           
009100/                                                                 |           
009200*----------------------------------------------------------------*|           
009300*                                                                *|           
009400*            C H A V E S                                         *|           
009500*                                                                *|           
009600*----------------------------------------------------------------*|           
009700*                                                                 |           
009800 77          CH-NOTFOUND             PIC X(001).                  |           
009900 77          CH-BCO                  PIC X(001)  VALUE "N".       |           
010000 77          CH-CHASSIS              PIC X(022).                  |           
010100*                                                                 |           
010200                                                                  |           
010300                                                                  |           
010400/----------------------------------------------------------------*|           
010500*    PARAMETRO PARA VERIFICACAO DE BLOQUEIO NO DBBLOQUEIO        *|           
010600*----------------------------------------------------------------*|           
010700*                                                                 |           
010800*                                                                 |           
010900 01          AX-LIB-GATL030.                                      |           
011000     05      AX-GATL030-CHASS        PIC X(022).                  |           
011100                                                                  |           
011200*                                                                 |           
011300 01          AX-GAT-RETL030.                                      |           
011400                                                                  |           
011500     05      AX-RETL030-PLAMERC      PIC X(010).                  |           
011600     05      AX-RETL030-MUNIC        PIC 9(005).                  |           
011700     05      AX-RETL030-CHASS        PIC X(022).                  |           
011800     05      AX-RETL030-FLAG         PIC 9(001).                  |           
011900     05      AX-RETL030-BLOQUEIO.                                 |           
012000       10    AX-RETL030-RESTRBIN     PIC 9(002)  OCCURS  4.       |           
012100*                                                                 |           
012200**    AX-RETL030-FLAG   = 0  ==> NAO ENCONTROU NENHUM BLOQUEIO    |           
012300**                      = 1  ==> ENCONTROU PELO MENOS 1 BLOQUEIO  |           
012400**                      = 3  ==> CHASSIS EM BRANCO                |           
012500*                                                                 |           
012600******************************************************************|           
012700***  AX-RETL030-BLOQUEIO =  Todos Bloqueios                       |           
012800***  BIN-Jud = 4    01 JUDICIAL                                   |           
012900***  BIN-Adm = 5    02 FALTA DE TRANSFERENCIA                     |           
013000***  BIN-Adm = 5    03 DANOS DE GRANDE MONTA                      |           
013100***  BIN-Trib= 7    04 VEICULO IMPORTADO USADO                    |           
013200***  BIN-Trib= 7    05 VEICULO IMPORTADO - PREMIO                 |           
013300***  BIN-Trib= 7    06 VEICULO IMPORTADO - CORPO CONSULAR         |           
013400***  BIN-Jud = 4    07 PENDENCIA JUDICIAL E/OU ADMINISTRATIVA     |           
013500***  BIN-Trib= 7    08 VEICULO P/ DEFICIENTE FISICO               |           
013600***  BIN-Trib= 7    09 VEICULO COM ISENCAO FISCAL                 |           
013700***  BIN-Trib= 7    10 VEICULO CONSULAR C/ ISENCAO                |           
013800***  BIN-Jud = 4    11 ACAO JUDICIAL (ANTIGO MANDATO DE SEGURANCA)|           
013900***  BIN-Adm = 5    12 BLOQUEIO DIVERSOS                          |           
014000***  BIN-Adm = 5    13 VEICULO RELACIONADO P/ LEILAO              |           
014100***  BIN-Adm = 5    14 VEICULO SINISTRADO                         |           
014200***                 15 VEICULO DUBLE                              |           
014300***                 16 BLOQ PROVISORIO PARA LICENCIAMENTO (JUD)   |           
014400******                 libera o licenciamento por um tempo -      |           
014500******                 feito por cnpj                             |           
014600***  BIN-Adm = 5    17 CADIN - INCONSISTENCIA CADASTRAL           |           
014700***                 18 PENHORA (615-A-CPC)(ART.615 COD.PROC.CIVIL)|           
014800***  BIN-Adm = 5    19 OBITO REGISTRADO INSS                      |           
014900***  BIN-Adm = 5    20 VEICULO APRENDIZAGEM                       |           
015000***                 21 DIRETORIA DE VEICULO - CADASTRO INCORRETO  |           
015100**** N¡o vai para BIN                                             |           
015200***  BIN-Adm = 5    22 VEICULO SUSPEITO DE DUPLICIDADE DE PLACA   |           
015300***  BIN-Adm = 5    23 TRANSFERENCIA - DETRAN  (ART.233 DO CTB)   |           
015400***                 24 PAGAMENTOS FRAUDULENTOS                    |           
015500***                 29 BAIXA POR EXPORTACAO / TRANSF.P/OUTRO PAIS |           
015600***                 30 BAIXA PERMANENTE  (Nao eh restricao )      |           
015700**** Eh enviada transacao de baixa permanente,                    |           
015800**** eh tratado de forma diferente - transa§¥o 205.               |           
015900***  BIN-Adm = 5    31 VEIC. BLOQUEADO PELO DETRAN                |           
016000***  BIN-Jud = 4    35 JUDICIAL- LIBERA LICENCIAMENTO             |           
016100***  BIN-Adm = 5    40 VEIC.SINISTRADO MEDIA MONTA                |           
016200***  BIN-Adm = 5    41 VEIC.SINISTRADO GRANDE MONTA               |           
016300***                 51 RENAJUD - TRANSFERENCIA                    |           
016400***                 52 RENAJUD - LICENCIAMENTO                    |           
016500***                 53 RENAJUD - CIRCULACAO                       |           
016600***                 54 RENAJUD - PENHORA                          |           
016700******************************************************************|           
016800                                                                  |           
016900                                                                  |           
017000                                                                  |           
017100/                                                                 |           
017200 PROCEDURE   DIVISION                USING   AX-LIB-GATL030       |           
017300                                             AX-GAT-RETL030.      |           
017400*----------------------------------------------------------------*|           
017500*    ROTINA PRINCIPAL DO PROGRAMA                                *|           
017600*----------------------------------------------------------------*|           
017700*                                                                 |           
017800 000-E-PROCEDURE.                                                 |           
017900*                                                                 |           
018000     IF      CH-BCO                  =       "S"                  |           
018100             GO                      TO      000-05.              |           
018200                                                                  |           
018300     OPEN    INQUIRY DB01                                         |           
018400       ON    EXCEPTION                                            |           
018500             DISPLAY "PC/GAT/L030/DB - ERRO ABERTURA DBBLOQUEIOS" |           
018600             CALL    SYSTEM  DMTERMINATE.                         |           
018700                                                                  |           
018800     MOVE    "S"                     TO      CH-BCO.              |           
018900                                                                  |           
019000 000-05.                                                          |           
019100                                                                  |           
019200     MOVE    ZEROS                   TO      AX-RETL030-FLAG      |           
019300                                             AX-RETL030-MUNIC.    |           
019400     MOVE    SPACES                  TO      AX-RETL030-PLAMERC   |           
019500                                             AX-RETL030-CHASS     |           
019600                                             AX-RETL030-BLOQUEIO. |           
019700     MOVE    " "                     TO      CH-NOTFOUND.         |           
019800                                                                  |           
019900                                                                  |           
020000     IF      AX-GATL030-CHASS        NOT =  LOW-VALUES AND        |           
020100                                            SPACES     AND        |           
020200                                            ZEROS                 |           
020300             MOVE    AX-GATL030-CHASS TO    CH-CHASSIS            |           
020400             SET     BLOCHASSE       TO     ENDING                |           
020500     ELSE                                                         |           
020600             MOVE     3              TO     AX-RETL030-BLOQUEIO   |           
020700             GO                      000-S-EXIT.                  |           
020800                                                                  |           
020900                                                                  |           
021000                                                                  |           
021100                                                                  |           
021300                                                                  |           
021400*                                                                 |           
021500*                                                                 |           
021600                                                                  |           
021700     PERFORM 010-E-FIND-BLOQ         THRU    010-S-FIND-BLOQ      |           
021800             UNTIL   CH-NOTFOUND     =       "S".                 |           
021900                                                                  |           
022000                                                                  |           
022100                                                                  |           
022200                                                                  |           
022300                                                                  |           
022400 000-S-EXIT.                                                      |           
022500     EXIT PROGRAM.                                                |           
022600/----------------------------------------------------------------*|           
022700*    P E S Q U I S A   N O   S E T  -   B L O C H A S S E        *|           
022800*----------------------------------------------------------------*|           
022900*                                                                 |           
023000 010-E-FIND-BLOQ.                                                 |           
023100*                                                                 |           
023200                                                                  |           
023300                                                                  |           
023400*                                                                 |           
023500     FIND    PRIOR    BLOCHASSE      AT                           |           
023600             BLO-CHASSIS             =      CH-CHASSIS            |           
023700      ON     EXCEPTION                                            |           
023800       IF    DMSTATUS (NOTFOUND)                                  |           
023900             MOVE    "S"             TO     CH-NOTFOUND           |           
024000             IF  AX-RETL030-FLAG     =      ZEROS                 |           
024100                 GO                  010-S-FIND-BLOQ              |           
024200             ELSE                                                 |           
024300                 GO                  010-2-RESTR                  |           
024400        ELSE                                                      |           
024500             DISPLAY "PC/GAT/L030/DB : FIND ERROR NEXT BLOCHASSE" |           
024600             CALL    SYSTEM          DMTERMINATE.                 |           
024700                                                                  |           
024800                                                                  |           
024900     MOVE    1                       TO     AX-RETL030-FLAG.      |           
025000                                                                  |           
025100     IF      BLO-TIP-BLOQ            =      1 OR 7 OR 11 OR 35    |           
025200        IF   AX-RETL030-RESTRBIN(1)  =      0                     |           
025300             MOVE    4               TO     AX-RETL030-RESTRBIN(1)|           
025400        ELSE                                                      |           
025500        IF  (AX-RETL030-RESTRBIN(2)  =      0 )  AND              |           
025600            (AX-RETL030-RESTRBIN(1)  NOT =  4 )                   |           
025700             MOVE    4               TO     AX-RETL030-RESTRBIN(2)|           
025800        ELSE                                                      |           
025900        IF  (AX-RETL030-RESTRBIN(3)  =      0)   AND              |           
026000            (AX-RETL030-RESTRBIN(1)  NOT =  4)   AND              |           
026100            (AX-RETL030-RESTRBIN(2)  NOT =  4)                    |           
026200             MOVE    4               TO     AX-RETL030-RESTRBIN(3)|           
026300        ELSE                                                      |           
026400        IF  (AX-RETL030-RESTRBIN(4)  =      0)   AND              |           
026500            (AX-RETL030-RESTRBIN(1)  NOT =  4)   AND              |           
026600            (AX-RETL030-RESTRBIN(2)  NOT =  4)   AND              |           
026700            (AX-RETL030-RESTRBIN(3)  NOT =  4)                    |           
026800             MOVE    4               TO     AX-RETL030-RESTRBIN(4)|           
026900             GO                      010-2-RESTR                  |           
027000        ELSE                                                      |           
027100             NEXT    SENTENCE                                     |           
027200     ELSE                                                         |           
027300     IF      BLO-TIP-BLOQ            =      2  OR  3   OR  12  OR |           
027400                                            13 OR  14  OR  22  OR |           
027500                                            23 OR  24  OR 40   OR |           
027600                                            41                    |           
027700        IF   AX-RETL030-RESTRBIN(1)  =       0                    |           
027800             MOVE    5               TO     AX-RETL030-RESTRBIN(1)|           
027900        ELSE                                                      |           
028000        IF  (AX-RETL030-RESTRBIN(2)  =      0)  AND               |           
028100            (AX-RETL030-RESTRBIN(1)  NOT =  5)                    |           
028200             MOVE    5               TO     AX-RETL030-RESTRBIN(2)|           
028300        ELSE                                                      |           
028400        IF  (AX-RETL030-RESTRBIN(3)  =      0)  AND               |           
028500            (AX-RETL030-RESTRBIN(1)  NOT =  5)  AND               |           
028600            (AX-RETL030-RESTRBIN(2)  NOT =  5)                    |           
028700             MOVE    5               TO     AX-RETL030-RESTRBIN(3)|           
028800        ELSE                                                      |           
028900        IF  (AX-RETL030-RESTRBIN(4)  =      0)  AND               |           
029000            (AX-RETL030-RESTRBIN(1)  NOT =  5)  AND               |           
029100            (AX-RETL030-RESTRBIN(2)  NOT =  5)   AND              |           
029200            (AX-RETL030-RESTRBIN(3)  NOT =  5)                    |           
029300             MOVE    5               TO     AX-RETL030-RESTRBIN(4)|           
029400             GO                      010-2-RESTR                  |           
029500        ELSE                                                      |           
029600             NEXT    SENTENCE                                     |           
029700     ELSE                                                         |           
029800     IF      BLO-TIP-BLOQ            =      4 OR 05  OR  06  OR   |           
029900                                            8 OR 09  OR  10       |           
030000        IF   AX-RETL030-RESTRBIN(1)  =      0                     |           
030100             MOVE    7               TO     AX-RETL030-RESTRBIN(1)|           
030200        ELSE                                                      |           
030300        IF  (AX-RETL030-RESTRBIN(2)  =      0)  AND               |           
030400            (AX-RETL030-RESTRBIN(1)  NOT =  7)                    |           
030500             MOVE    7               TO     AX-RETL030-RESTRBIN(2)|           
030600        ELSE                                                      |           
030700        IF  (AX-RETL030-RESTRBIN(3)  =      0)  AND               |           
030800            (AX-RETL030-RESTRBIN(1)  NOT =  7)  AND               |           
030900            (AX-RETL030-RESTRBIN(2)  NOT =  7)                    |           
031000             MOVE    7               TO     AX-RETL030-RESTRBIN(3)|           
031100        ELSE                                                      |           
031200        IF  (AX-RETL030-RESTRBIN(4)  =      0)  AND               |           
031300            (AX-RETL030-RESTRBIN(1)  NOT =  7)  AND               |           
031400            (AX-RETL030-RESTRBIN(2)  NOT =  7)  AND               |           
031500            (AX-RETL030-RESTRBIN(3)  NOT =  7)                    |           
031600             MOVE    7               TO     AX-RETL030-RESTRBIN(4)|           
031700             GO                      TO     010-2-RESTR.          |           
031800                                                                  |           
031900     GO                              010-E-FIND-BLOQ.             |           
032000                                                                  |           
032100 010-2-RESTR.                                                     |           
032200                                                                  |           
032300                                                                  |           
032400     MOVE    BLO-PLACA-MERC          TO     AX-RETL030-PLAMERC.   |           
032500     MOVE    BLO-MUNICIPIO           TO     AX-RETL030-MUNIC.     |           
032600     MOVE    BLO-CHASSIS             TO     AX-RETL030-CHASS.     |           
032700                                                                  |           
032800                                                                  |           
032900 010-S-FIND-BLOQ.                                                 |           
033000     EXIT.                                                        |           
033100                                                                  |           
