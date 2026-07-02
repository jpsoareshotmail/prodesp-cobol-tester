000000* VERSION  14.1  ; SAVED 20230111 11:03:35                    |001|0014.01    
000100                                                                  |           
000200$$ SET SHARING=PRIVATE                                            |           
000300$$ SET TEMPORARY                                                  |           
000400**$  SET LIST MAP  LINEINFO                                       |           
000500 IDENTIFICATION DIVISION.                                         |           
000600                                                                  |           
000700*PROGRAM-ID.     PC-GAA-L160.                                     |           
000800                                                                  |           
000900 AUTHOR.         JORGE CORTEZ.                                    |           
001000*ANALISTA        JORGE CORTEZ.                                    |           
001100                                                                  |           
001200 DATE-WRITTEN.   NOVEMBRO/2021.                                   |           
001300                                                                  |           
001400 DATE-COMPILED.                                                   |           
001500                                                                  |           
001600 SECURITY.                                                        |           
001700                                                                  |           
001800******************************************************************|           
001900*                                                                *|           
002000*     RECEBER OU SOLICITAR DADOS DO CAMPO OBSERVACOES            *|           
002100*        REFERENTES A TRANSACAO 237 ENVIADA PARA SERPRO(BIN)     *|           
002200*                 WEBSERVICE DO SISTEMA RENAVAN-WS               *|           
002300******************************************************************|           
002400*                       A L T E R A C O E S                      *|           
002500*                                                                *|           
002600*                                                                *|0005.01    
002700*      DATA     ANA    PROGR   OBSERVACAO                        *|           
002800*  ===========  ====   =====   ================================= *|           
002900*                                                                 |           
003000*  .22./.12../2021   JWD JWD    RETIRADA DA LIB L170 ........... *|0002.01    
003100*  .23/12/2021       JWD JWD    INCLUSAO DE DISPLAYS............ *|0004.01    
003200*  .23/12/2021       JWD JWD    RETIRADA DE DISPLAYS             *|0005.01    
003300*   29/12/2021       JWD JWD    AJUSTE P/ MOV AX-ENTRADA L170    *|0006.01    
003400*   10/01/2022       JWD DJCD   INCLUSAO DE GRV DE ARQ DE MONIT  *|0007.01    
003500*   24/01/2022       DJCD DJCD  RETIRADA DA GRV DO LOG DA LIB    *|0011.01    
003600*                           A GRAVACAO PASSOU PARA A LIB GAAL170 *|0009.01    
003700*   01/06/2022       DJCD DJCD  NOVA PESQUISA RESTR ATIVAS       *|0011.01    
003800*   05/09/2022       DJCD DJCD  INCLUIR O NRO-PROC NO ENVIO 8004 *|0012.01    
003900*   09/12/2022       DJCD SSE   AJUSTAR OBS 8036 E 8037 P/INCLUIR*|0013.01    
004000*                               O ENVIO NRO PROC                 *|0013.01    
004100*   13/12/2022       DJCD SSE   AJUSTAR PARAMETRIZACAO PARA ATEN-*|0014.01    
004200*                               DER QUALQUER TIPO DE OBSERVACAO  *|0014.01    
004300*  ../.../....  ....  .......  ................................. *|           
004400*  ../.../....  ....  .......  ................................. *|           
004500*  ../.../....  ....  .......  ................................. *|           
004600*  ../.../....  ....  .......  ................................. *|           
004700*  ../.../....  ....  .......  ................................. *|           
004800                                                                  |           
004900******************************************************************|           
005000/                                                                 |           
005100                                                                  |           
005200 ENVIRONMENT     DIVISION.                                        |           
005300                                                                  |           
005400 CONFIGURATION   SECTION.                                         |           
005500                                                                  |           
005600 SPECIAL-NAMES.                                                   |           
005700                                                                  |           
005800     DECIMAL-POINT   IS  COMMA.                                   |           
005900/                                                                 |           
005905 INPUT-OUTPUT    SECTION.                                         |           
005910                                                                  |           
005915 FILE-CONTROL.                                                    |           
005920                                                                  |           
006000 DATA    DIVISION.                                                |           
006100                                                                  |           
006101 FILE        SECTION.                                             |           
006102*--------------------                                             |           
006103                                                                  |0009.01    
006200/                                                                 |           
006300 WORKING-STORAGE     SECTION.                                     |           
006400                                                                  |           
006401 01          WS-GAAL160S             PIC X(1080).                 |0007.01    
006500 77          MY-INTERFACE-VERSION    PIC 9(011)  VA 4   BINARY.   |           
006600 77          EF-INTERFACE-VERSION    PIC 9(011)  VA 1   BINARY.   |           
006700 77          CHARSET-EBCDIC          PIC 9(011)  VA 4   BINARY.   |           
006800                                                                  |           
006900 77          WS-RESULT               PIC S9(11)  VA 0   BINARY.   |           
007000      88     WS-OK                               VA 1.            |           
007100      88     WS-NO-OP                            VA 0.            |           
007200      88     WS-BADID                            VA -1.           |           
007300      88     WS-DENIED                           VA -2.           |           
007400      88     WS-SOFTERR                          VA -3.           |           
007500      88     WS-NOTAVAIL                         VA -4.           |           
007600      88     WS-BUFTOOSMALL                      VA -18.          |           
007700      88     WS-SYNTAXERROR                      VA -19.          |           
007800      88     WS-LENTOOSMALL                      VA -20.          |           
007900      88     WS-NOSOCKET                         VA -48.          |           
008000      88     WS-NOSOCKETWRITE                    VA -49.          |           
008100      88     WS-NOSOCKETREAD                     VA -50.          |           
008200      88     WS-PARSEXMLERROR                    VA -51.          |           
008300      88     WS-JPMNOTCONFIGURED                 VA -54.          |           
008400      88     WS-INVALIDHOST                      VA -70.          |           
008450                                                                  |0014.01    
008500 01          AX-TRAB                 PIC X(200).                  |0014.01    
008600                                                                  |           
008800** TAM 13                                                         |           
008900 01          AX-REQ-CODIGO.                                       |           
009000     05      FILLER                  PIC X(007)  VA               |           
009100             "codigo=".                                           |           
009200     05       AX-RC-COD              PIC 999999  VA ZEROS.        |           
009300                                                                  |           
009800                                                                  |           
009900* Tam 031                                                         |           
010000 01          AX-REQ-PROCESSO.                                     |           
010100     05      FILLER                  PIC X(016)  VA               |           
010200             "&numeroProcesso=".                                  |           
010300     05      AX-RC-NRO-PROC          PIC 9(015)  VA ZEROS.        |0007.01    
010400                                                                  |           
010600*                                                                 |           
010700* Tam 024                                                         |           
01080001           AX-REQ-VRNUMER.                                      |           
010900     05      FILLER                  PIC X(015)  VA               |           
011000             "&valorNumerico=".                                   |           
011100     05      AX-RC-VLR-NUM           PIC X(009)  VA SPACES.       |           
011200                                                                  |           
011800*                                                                 |           
011900* Tam 42                                                          |           
012000 01          AX-REQ-TEXTO.                                        |           
012100     05      FILLER                  PIC X(012)  VA               |           
012200             "&valorTexto=".                                      |           
012300     05      AX-RC-TEXTO             PIC X(030)  VA SPACES.       |           
012400                                                                  |           
012500*                                                                 |           
012800*                                                                 |           
012900* Tam 040                                                         |           
013000 01          AX-REQ-IDENTREL.                                     |           
013100     05      FILLER                  PIC X(026)  VA               |           
013200             "&identificacaoRelacionada=".                        |           
013300     05      AX-RC-IDTREL            PIC X(014)  VA SPACES.       |           
013400                                                                  |           
013500*                                                                 |           
013600*Tam 063                                                          |           
013700 01          AX-REQ-CHASSI.                                       |           
013800     05      FILLER                  PIC X(008)  VA               |           
013900             "&chassi=".                                          |           
014000     05      AX-RC-CHASSI            PIC X(021)  VA SPACES.       |           
014100                                                                  |           
014200                                                                  |           
014300 01          AX-REQ-PLACA.                                        |           
014400     05      FILLER                  PIC X(007)  VA               |           
014500             "&placa=".                                           |           
014600     05      AX-RC-PLACA             PIC X(007)  VA SPACES.       |           
014700                                                                  |           
01480001          AX-REQ-RENAVAM.                                       |           
014900     05      FILLER                  PIC X(009)  VA               |           
015000             "&renavam=".                                         |           
015100     05      AX-RC-RENAVAM           PIC 9(011)  VA  ZEROS.       |           
015200     05      AX-LOW-VALUES           PIC X(004)  VA LOW-VALUES.   |0014.01    
015240                                                                  |0014.01    
015300                                                                  |           
015400                                                                  |           
015500                                                                  |           
015600                                                                  |           
015700** Consulta por ID                                                |           
015800 01          AX-REQ-RESTR-P-ID.                                   |           
015900     05      FILLER                  PIC X(003) VA "id=".         |           
016000     05      AX-RC-ID                PIC X(020).                  |           
016100     05      FILLER                  PIC X(004) VA LOW-VALUES.    |           
016200                                                                  |           
016300** APAGAR(FINALIZAR) AS OBS NO SERPRO                             |           
016400*  CPF...                                                         |           
016500 01          AX-REQ-CPF.                                          |           
016600     05      FILLER                  PIC X(015)  VA               |           
016700             "cpfResponsavel=".                                   |           
016800     05      AX-RC-CPF               PIC 9(011)  VA ZEROS.        |           
016900                                                                  |           
017000** MOTIVO                                                         |           
017100                                                                  |           
017200 01          AX-REQ-MOTIVO.                                       |           
017300     05      FILLER                  PIC X(014)  VA               |           
017400             "&motivoEvento=".                                    |           
017500     05      AX-RC-MOTIVO            PIC X(014)  VA SPACES.       |           
017600                                                                  |           
017700** OBSERVACOES                                                    |           
017800                                                                  |           
017900 01          AX-REQ-OBSERV.                                       |           
018000     05      FILLER                  PIC X(013)  VA               |           
018100             "&observacoes=".                                     |           
018200     05      AX-RC-OBSERV            PIC X(020)  VA SPACES.       |           
018300                                                                  |           
018400                                                                  |           
018500** RENAVAM PARA EXCLUIR..                                         |           
018600                                                                  |           
01870001          AX-REQ-RENA-FIN.                                      |           
018800     05      FILLER                  PIC X(009)  VA               |           
018900             "&renavam=".                                         |           
019000     05      AX-RC-RENA-FIN          PIC 9(011)  VA  ZEROS.       |           
019005     05      FILLER                  PIC X(001)  VA "&".          |           
019100                                                                  |           
019200*-----------------FIM REG PARA FINALIZACAO (EXCLUSAO) ------------|           
019300                                                                  |           
019400                                                                  |           
019500 01          AX-DADOS-IDENT          PIC X(212).                  |           
019520                                                                  |0014.01    
019540* 01          AX-DADOS-IDENTR.                                    |0014.01    
019550*     05      AX-DADOS-IDENT2         PIC X(212) VA SPACES.       |0014.01    
019560*     05      AX-SPACESR              PIC X(004) VA SPACES.       |0014.01    
019600                                                                  |           
019700                                                                  |           
019800/*****************************************************************|           
019900*                        PARAMETROS                              *|           
020000******************************************************************|           
020100                                                                  |           
020200*===========================>                                     |           
020300 01          L160-PARAM-E.                                        |           
020400     05      L160-CHASSI             PIC X(021).                  |           
020500     05      L160-PLACA              PIC X(007).                  |           
020600     05      L160-RENAVAM            PIC 9(011).                  |           
020700     05      L160-DADOS-OBS.                                      |           
020800       10    L160-COD-RESTR          PIC 9(006).                  |           
020900       10    L160-IDENT-RELAC        PIC X(014).                  |           
021000       10    L160-NRO-PROCESSO.                                   |0007.01    
021100          15 L160-NRO-PROC           PIC 9(011).                  |0007.01    
021200          15 L160-ANO-PROC           PIC 9(004).                  |0007.01    
021300       10    L160-VLR-NUMERICO       PIC 9(009).                  |           
021400       10    L160-TEXTO              PIC X(030).                  |           
021500     05      L160-ID                 PIC X(019).                  |0007.01    
021600     05      L160-CPF                PIC 99999999999.             |           
021700     05      L160-MOTIVO             PIC X(014).                  |           
021800     05      L160-OBSERV             PIC X(020).                  |           
021900     05      L160-SOLIC              PIC 9(001).                  |           
021950     05      L160-LOGFILE            PIC X(021).                  |0009.01    
022000                                                                  |           
022100******TIPOS DE MOTIVO (L160-MOTIVO)                               |           
022200                                                                  |           
022300* - CANCELAMENTO                                                  |           
022400* - DESCONSIDERADA                                                |           
022500* - REGULARIZACAO                                                 |           
022600* - DEVOLVIDA                                                     |           
022700                                                                  |           
022800 01          L160-PARAM-S.                                        |           
022900     05      L160-RETORNO            PIC 9(003).                  |           
023000     05      L160-RETORNO-BIN.                                    |           
023100       10    L160-RET-BIN            PIC 9(003).                  |           
023200       10    L160-ID-RET-BIN         PIC X(019).                  |0007.01    
023210       10    L160-RETMSG             PIC X(070).                  |0007.01    
023300       10    L160-FILLER             PIC X(4908).                 |0011.01    
023400                                                                  |           
023500                                                                  |           
023600*****  AREA DE PASSAGEM DOS PARAMETROS NA LIBRARY ****************|           
023700*                                                                *|           
023800*                                                                *|           
023900*    L160-PARAM-E       (ENTRADA):                               *|           
024000*    ==========                                                  *|           
024100*                                                                *|           
024200*    L160-CHASSI        CHASSI VEICULO                           *|           
024300*    L160-PLACA         PLACA                                    *|           
024400*    L160-RENAVAN       RENAVAM                                  *|           
024500*    L160-DADOS-OBS     DADOS DA OBSERVACAO                      *|           
024600*                                                                *|           
024700*                                                                *|           
024800*    L160-PARAM-S     (RESPOSTA):                                *|           
024900*    ==========                                                  *|           
025000*                                                                *|           
025100*                                                                *|           
025200*    L160-RETORNO(DESTA LIB) -  0 - PARAMETRO OK                 *|           
025300*                     2,3,4,5.... - INCONSISTENCIA NO PARAMETRO  *|           
025400*                                                                *|           
025500*    L160-RET-BIN       -  201 - PARAMETRO OK                    *|           
025600*                          401 - NAO AUTORIZADO                  *|           
025700*                          403 - PROIBIDO                        *|           
025800*                          404 - NAO ENCONTRADO                  *|           
025900*                                                                *|           
026000*    L160-ID-RET-BIN    -  PID - CHAVE DE 19 POSICOES GERADA     *|0009.01    
026100*                                                                *|           
026200*                                                                *|           
026300***------------------------------------------------------------***|           
026400*        PARAMETRO QUE INDICA O AMBIENTE QUE ESTA RODANDO        *|           
026500*            PRODUCAO OU DESENVOLVIMENTO                         *|           
026600***------------------------------------------------------------***|           
026700                                                                  |           
026750 01          AX-ENDERECO.                                         |           
026800**              Endereco IP usado pela LIB                        |0009.01    
026850     05      AX-IP                   PIC X(045).                  |0009.01    
026950                                                                  |0009.01    
027000**              Endereco IP usado pela LIB na Producao            |0009.01    
027050     05      AX-IP-PROD              PIC X(045) VALUE             |0009.01    
027100             "http://10.200.76.111:80/SevConsulta/rest/api/".     |0009.01    
027150                                                                  |0009.01    
027200**              Endereco IP usado pela LIB no Desenvolvimento     |0009.01    
027250     05      AX-IP-HOMO              PIC X(045) VALUE             |0009.01    
027300             "http://10.200.77.119:80/SevConsulta/rest/api/".     |0009.01    
027350                                                                  |0009.01    
027600     05      AX-COMPLEMENTO          PIC X(030).                  |           
027605                                                                  |0009.01    
027610     05      AX-HOSTNAME             PIC X(012).                  |0009.01    
027700*----------------------------------------------------------------*|           
027800** 01                                                             |           
027900 01          AX-CONS-RESTR           PIC X(030)  VALUE            |           
028000             "restricao?                    ".                    |           
028100 01          AX-CONS-RESTR-ID        PIC X(030)  VALUE            |           
028200             "restricao/id?                 ".                    |           
028300 01          AX-INCL-RESTR           PIC X(030)  VALUE            |           
028400             "restricoes?                   ".                    |           
028500 01          AX-EXC-RESTR            PIC X(030)  VALUE            |           
028600             "restricoes/finalizar?         ".                    |           
028700 01          AX-SIT-VEIC             PIC X(030)  VALUE            |           
028800             "situacao-restricoes-veiculo?  ".                    |           
028900 01          AX-TIPOS-RESTR          PIC X(030)  VALUE            |           
029000             "tipos-restricao'              ".                    |           
029100 01          AX-DESC-COD-RESTR       PIC X(030)  VALUE            |           
029200             "tipos-restricao/codigo?       ".                    |           
029210 01          AX-CONS-RESTR-ATIVAS    PIC X(030)  VALUE            |0011.01    
029220             "restricaomf?                  ".                    |0011.01    
029300                                                                  |           
029400*----------------------------------------------------------------*|           
029500                                                                  |           
029600                                                                  |           
029700*================================================================*|           
029800*     AREA DE COMUNICACAO COM A LIBRARY  OBJECT/WEB/SERVICE/LIB  *|           
029900*                                                                *|           
030000*----------------------------------------------------------------*|           
030100 01          AX-PARAM.                                            |           
030200     05      AX-PARAM-DADOS          PIC X(5000).                 |0011.01    
031300*----------------------------------------------------------------*|           
031305                                                                  |0009.01    
031310*================================================================*|           
031315*     AREA DE COMUNICACAO COM A LIBRARY  ALGOL GAAL170           *|0009.01    
031320*                                                                *|           
031325*----------------------------------------------------------------*|           
031330                                                                  |0009.01    
031335 01          AX-PARAM01              PIC X(021).                  |0009.01    
031340 01          AX-PARAM02              PIC X(5000).                 |0011.01    
031345 01          AX-PARAM03              PIC X(5000).                 |0011.01    
031350 01          AX-PARAM04              PIC X(300).                  |0009.01    
031400/                                                                 |           
031500 PROCEDURE   DIVISION    USING   L160-PARAM-E  L160-PARAM-S.      |           
031600******************************************************************|           
031700*        M O N I T O R A                                         *|           
031800******************************************************************|           
031900*                                                                 |           
032000 000-E-MONITORA.                                                  |           
032100                                                                  |           
032110     MOVE ATTRIBUTE HOSTNAME OF MYSELF TO AX-HOSTNAME.            |0009.01    
032120                                                                  |0009.01    
032130     IF   AX-HOSTNAME             =         "HNPRDSP06.  "        |0009.01    
032140       MOVE  AX-IP-HOMO           TO        AX-IP                 |0009.01    
032150     ELSE                                                         |0009.01    
032160       MOVE  AX-IP-PROD           TO        AX-IP.                |0009.01    
032170                                                                  |0009.01    
032180     MOVE    SPACES               TO        L160-PARAM-S.         |0009.01    
032190                                                                  |0009.01    
032200     PERFORM 010-E-INICIO         THRU      010-S-INICIO.         |           
032300                                                                  |           
032400     IF      L160-RETORNO         >         0                     |           
032500             GO                   TO        000-S-MONITORA.       |           
032600                                                                  |           
032700     PERFORM 020-E-PROCESSA       THRU      020-S-PROCESSA.       |0014.01    
032800                                                                  |           
033000 000-S-MONITORA.                                                  |           
033100     EXIT    PROGRAM.                                             |           
033200/                                                                 |           
033300******************************************************************|           
033400*        I N I C I A L I Z A C A O                               *|           
033500******************************************************************|           
033600*                                                                 |           
033700 010-E-INICIO.                                                    |           
033800                                                                  |           
033900     MOVE    LOW-VALUES              TO      AX-PARAM-DADOS       |0014.01    
034000                                             AX-DADOS-IDENT.      |0014.01    
034050     MOVE    SPACES                  TO      AX-TRAB.             |0014.01    
034100     MOVE    AX-IP                   TO      AX-PARAM-DADOS.      |           
034200     MOVE    ZEROS                   TO      L160-RETORNO.        |           
034300     MOVE    SPACES                  TO      L160-ID-RET-BIN.     |           
034400                                                                  |           
034500     MOVE    ZEROS                   TO      AX-RC-COD            |           
034600                                             AX-RC-NRO-PROC       |           
034700                                             AX-RC-VLR-NUM.       |0014.01    
034800     MOVE    SPACES                  TO      AX-RC-IDTREL         |0014.01    
034900                                             AX-RC-TEXTO.         |0014.01    
035000                                                                  |           
035010                                                                  |0014.01    
035080                                                                  |0014.01    
035100** Seleciona opcao(solicitacao)                                   |           
035200                                                                  |           
035300     IF      L160-SOLIC              =      1   OR  3  OR  8      |0011.01    
035400             NEXT SENTENCE                                        |           
035500     ELSE                                                         |           
035600     IF      L160-SOLIC              =      2                     |           
035700        IF   L160-ID                 =      ZEROS  OR             |           
035800                                            SPACES OR             |           
035900                                            LOW-VALUES            |           
036000** ID Zerado Invalido                                             |           
036100             MOVE    11              TO     L160-RETORNO          |           
036200             GO                      010-S-INICIO                 |           
036300        ELSE                                                      |           
036400             MOVE L160-ID            TO     AX-RC-ID              |           
036500             GO         010-010-MONTA-STRING                      |           
036600     ELSE                                                         |           
036700     IF      L160-SOLIC              =      4                     |           
036800*        IF   L160-CPF                =      ZEROS     OR         |           
036900        IF   (L160-MOTIVO            =      ZEROS     OR          |           
037000                                            SPACES    OR          |           
037100                                            LOW-VALUES) OR        |           
037200*             (L160-OBSERV            =      ZEROS     OR         |0007.01    
037300*                                            SPACES    OR         |0007.01    
037400*                                            LOW-VALUES)  OR      |0007.01    
037500             (L160-CHASSI            =      ZEROS     OR          |           
037600                                            SPACES    OR          |           
037700                                            LOW-VALUES)  OR       |           
037800             (L160-PLACA             =      ZEROS     OR          |           
037900                                            SPACES    OR          |           
038000                                            LOW-VALUES)  OR       |           
038100             L160-RENAVAM            =      ZEROS     OR          |           
038200             (L160-ID                =      ZEROS     OR          |           
038300                                            SPACES    OR          |           
038400                                            LOW-VALUES)           |           
038500             MOVE 12                 TO     L160-RETORNO          |           
038600             GO                      010-S-INICIO                 |           
038700        ELSE                                                      |           
038800             MOVE  L160-CPF          TO     AX-RC-CPF             |           
038900             MOVE  L160-MOTIVO       TO     AX-RC-MOTIVO          |           
039000             MOVE  L160-OBSERV       TO     AX-RC-OBSERV          |           
039100             MOVE  L160-CHASSI       TO     AX-RC-CHASSI          |           
039200             MOVE  L160-PLACA        TO     AX-RC-PLACA           |           
039300             MOVE  L160-RENAVAM      TO     AX-RC-RENA-FIN        |           
039400             MOVE  L160-ID           TO     AX-RC-ID              |           
039500             GO                      010-010-MONTA-STRING         |           
039600     ELSE                                                         |           
039700** Nao Implementado opcoes 5(sit.Veic.), 6(tipos-restr) e         |           
039800**   7   (Tipos Restr. Codigo)                                    |           
039900             MOVE 13                 TO     L160-RETORNO          |           
040000             GO                      010-S-INICIO.                |           
040100                                                                  |           
040150                                                                  |0014.01    
040200                                                                  |           
040300     IF      (L160-CHASSI            =      ZEROS     OR          |           
040400                                            SPACES    OR          |           
040500                                            LOW-VALUES)  AND      |           
040600             (L160-PLACA             =      ZEROS     OR          |           
040700                                            SPACES    OR          |           
040800                                            LOW-VALUES)  AND      |           
040900             L160-RENAVAM            =      ZEROS                 |           
041000             MOVE    1               TO      L160-RETORNO         |           
041100             GO                      TO      010-S-INICIO.        |           
041200                                                                  |           
041300*============>   CONSISTE CHASSI                                  |           
041400     IF      L160-CHASSI             =      ZEROS     OR          |           
041500                                            SPACES    OR          |           
041600                                            LOW-VALUES            |           
041700             MOVE    2               TO     L160-RETORNO          |           
041800             GO                      TO     010-S-INICIO.         |           
041900                                                                  |           
042000*============>   CONSISTE PLACA                                   |           
042100     IF      L160-PLACA              =      ZEROS     OR          |           
042200                                            SPACES    OR          |           
042300                                            LOW-VALUE             |           
042400             MOVE    3               TO     L160-RETORNO          |           
042500             GO                      TO     010-S-INICIO.         |           
042600                                                                  |           
042700                                                                  |           
042800     IF      L160-RENAVAM            =      ZEROS                 |           
042900             MOVE    4               TO     L160-RETORNO          |           
043000             GO                      TO     010-S-INICIO.         |           
043010                                                                  |0011.01    
043020     IF      L160-SOLIC              =      8                     |0011.01    
043030             GO                      TO     010-05-MONTA-CHAVES.  |0011.01    
043040                                                                  |0011.01    
043100*============>   CONSISTE CODIGOS                                 |           
043200                                                                  |           
043300*============> IDENTIFICACAO RELACIONADA                          |0014.01    
043400*                                                                 |0014.01    
043500                                                                  |0014.01    
043600     IF      L160-COD-RESTR          =      ZEROS                 |           
043700             MOVE    10              TO     L160-RETORNO          |           
043800             GO                      TO     010-S-INICIO          |           
043900     ELSE                                                         |           
044000     IF      L160-IDENT-RELAC        =      ZEROS     OR          |0014.01    
044100                                            SPACES    OR          |           
044200                                            LOW-VALUES            |           
044300             NEXT   SENTENCE                                      |0014.01    
044400         ELSE                                                     |           
044500             MOVE L160-IDENT-RELAC   TO     AX-RC-IDTREL.         |0014.01    
044600                                                                  |0014.01    
044700                                                                  |0014.01    
044800*============> NUMERO PROCESSO                                    |0014.01    
044900*                                                                 |0014.01    
045000                                                                  |0014.01    
045100     IF      L160-NRO-PROCESSO       =      ZEROS     OR          |0014.01    
045200                                            SPACES    OR          |0014.01    
045300                                            LOW-VALUES            |0014.01    
045400             NEXT   SENTENCE                                      |0014.01    
045500         ELSE                                                     |0014.01    
045600             MOVE L160-NRO-PROCESSO  TO     AX-RC-NRO-PROC.       |0014.01    
045700                                                                  |0014.01    
045800                                                                  |0014.01    
045900*============> VALOR NUMERICO                                     |0014.01    
046000*                                                                 |0014.01    
046100                                                                  |0014.01    
046200     IF      L160-VLR-NUMERICO       =      ZEROS     OR          |0014.01    
046300                                            SPACES    OR          |0014.01    
046400                                            LOW-VALUES            |0014.01    
046500             NEXT   SENTENCE                                      |0014.01    
046600         ELSE                                                     |0014.01    
046700             MOVE L160-VLR-NUMERICO  TO     AX-RC-VLR-NUM.        |0014.01    
046800                                                                  |0014.01    
046900                                                                  |0014.01    
047000*============> VALOR TEXTO                                        |0014.01    
047100*                                                                 |0014.01    
047200                                                                  |0014.01    
047300      IF     L160-TEXTO              =      ZEROS     OR          |0014.01    
047400                                            SPACES    OR          |           
047500                                            LOW-VALUES            |0014.01    
047600             NEXT   SENTENCE                                      |0014.01    
047700         ELSE                                                     |0014.01    
047800             MOVE L160-TEXTO         TO     AX-RC-TEXTO.          |0014.01    
047900                                                                  |0014.01    
048000                                                                  |0014.01    
051760                                                                  |0014.01    
051800                                                                  |           
051900**                                                                |           
051910                                                                  |0011.01    
051920 010-05-MONTA-CHAVES.                                             |0011.01    
051930                                                                  |0011.01    
052000*--- MONTAGEM DO CAMPO AX-REQ-CHAVES                              |           
052100                                                                  |           
052200     MOVE    L160-CHASSI             TO     AX-RC-CHASSI.         |           
052300     MOVE    L160-PLACA              TO     AX-RC-PLACA.          |           
052400     MOVE    L160-RENAVAM            TO     AX-RC-RENAVAM.        |           
052500                                                                  |           
052700**                                                                |           
052800                                                                  |           
052900 010-010-MONTA-STRING.                                            |           
053000                                                                  |           
053100                                                                  |           
053200** Consulta Restricao(1)                                          |           
053300     IF      L160-SOLIC              =      1                     |           
053400             MOVE AX-CONS-RESTR      TO     AX-COMPLEMENTO        |           
053500             STRING  AX-REQ-CHASSI  DELIMITED BY SPACES           |           
053600                     AX-REQ-PLACA   DELIMITED BY SPACES           |           
053700                     AX-REQ-RENAVAM DELIMITED BY LOW-VALUES       |0014.01    
053800                                     INTO   AX-DADOS-IDENT        |           
053900            GO          010-099-MONTA-MENSAGEM                    |           
054000     ELSE                                                         |           
054100** Consulta Restricao por ID(2)                                   |           
054200     IF      L160-SOLIC              =      2                     |           
054300             MOVE AX-REQ-RESTR-P-ID  TO     AX-COMPLEMENTO        |           
054400             STRING  AX-REQ-RESTR-P-ID    DELIMITED BY LOW-VALUES |           
054500                                     INTO   AX-DADOS-IDENT        |           
054600             GO          010-099-MONTA-MENSAGEM                   |           
054700     ELSE                                                         |           
054800** Inclui Restricao(3)                                            |           
054900     IF      L160-SOLIC              =      3                     |           
055000             MOVE AX-INCL-RESTR      TO     AX-COMPLEMENTO        |           
055100     ELSE                                                         |           
055200** Finaliza (exclui) Restricao(4)                                 |           
055300     IF      L160-SOLIC              =      4                     |           
055400             MOVE AX-EXC-RESTR       TO     AX-COMPLEMENTO        |           
055500             STRING  AX-REQ-CPF     DELIMITED BY SPACES           |           
055600                     AX-REQ-MOTIVO  DELIMITED BY SPACES           |           
055700                     AX-REQ-OBSERV  DELIMITED BY SPACES           |           
055800                     AX-REQ-CHASSI  DELIMITED BY SPACES           |           
055900                     AX-REQ-PLACA   DELIMITED BY SPACES           |           
056000                     AX-REQ-RENA-FIN DELIMITED BY SPACES          |           
056100                     AX-REQ-RESTR-P-ID  DELIMITED BY LOW-VALUES   |           
056200                                     INTO   AX-DADOS-IDENT        |           
056300            GO          010-099-MONTA-MENSAGEM                    |           
056400                                                                  |           
056500     ELSE                                                         |           
056600**************  CONSULTAS ABAIXO NAO FORAM IMPLEMENTADAS ******** |           
056700** Consulta situacao do Veiculo(5)                                |           
056800     IF      L160-SOLIC              =      5                     |           
056900             MOVE AX-SIT-VEIC        TO     AX-COMPLEMENTO        |           
057000     ELSE                                                         |           
057100     IF      L160-SOLIC              =      6                     |           
057200             MOVE AX-TIPOS-RESTR     TO     AX-COMPLEMENTO        |           
057300     ELSE                                                         |           
057400** consulta Descr do Cod Restricao(7)                             |           
057500     IF      L160-SOLIC              =      7                     |           
057600             MOVE AX-DESC-COD-RESTR  TO     AX-COMPLEMENTO        |0011.01    
057610     ELSE                                                         |           
057620** consulta restricoes ativas do Veiculo                          |0011.01    
057630     IF      L160-SOLIC              =      8                     |0011.01    
057640             MOVE AX-CONS-RESTR-ATIVAS  TO  AX-COMPLEMENTO        |0011.01    
057650             STRING  AX-REQ-CHASSI  DELIMITED BY SPACES           |           
057660                     AX-REQ-PLACA   DELIMITED BY SPACES           |           
057670                     AX-REQ-RENAVAM DELIMITED BY LOW-VALUES       |0014.01    
057680                                     INTO   AX-DADOS-IDENT        |           
057690            GO          010-099-MONTA-MENSAGEM.                   |0011.01    
057700                                                                  |           
057800                                                                  |           
057900**                                                                |           
058000*--- MONTAGEM DO CAMPO AX-REQ-CHAVES                              |           
058100                                                                  |           
058200     MOVE    L160-CHASSI             TO     AX-RC-CHASSI.         |           
058300     MOVE    L160-PLACA              TO     AX-RC-PLACA.          |           
058400     MOVE    L160-RENAVAM            TO     AX-RC-RENAVAM.        |           
058500                                                                  |           
058600*--- MONTAGEM DO CAMPO AX-REQ-CODIGO                              |           
058700                                                                  |           
058800     MOVE    L160-COD-RESTR          TO     AX-RC-COD.            |           
058900                                                                  |           
059000** MONTAGEM CAMPO AX-REQ-IDENTREL                                 |           
059020                                                                  |0014.01    
059100                                                                  |0014.01    
059110     STRING  AX-REQ-CODIGO           DELIMITED BY SPACES          |0014.01    
059120                                     INTO   AX-TRAB.              |0014.01    
059130                                                                  |0014.01    
059140                                                                  |0014.01    
059144** MONTAGEM CAMPO AX-REQ-IDENTREL                                 |           
059150                                                                  |           
059200     IF      AX-RC-IDTREL            =  LOW-VALUES      OR        |0014.01    
059300                                            SPACES      OR        |0014.01    
059400                                            ZEROS                 |0014.01    
059500             NEXT    SENTENCE                                     |0014.01    
059600     ELSE                                                         |0014.01    
059700             STRING  AX-TRAB         DELIMITED BY SPACES,         |0014.01    
059800                     AX-REQ-IDENTREL DELIMITED BY SPACES          |0014.01    
060300                                     INTO   AX-TRAB.              |0014.01    
060400                                                                  |0014.01    
060420                                                                  |0014.01    
060450** MONTAGEM CAMPO AX-REQ-PROCESSO                                 |0014.01    
060500                                                                  |0014.01    
060550       IF    AX-RC-NRO-PROC          =  LOW-VALUES     OR         |0014.01    
060600                                            ZEROS      OR         |0014.01    
060650                                            SPACES                |0014.01    
060660            NEXT SENTENCE                                         |0014.01    
060680       ELSE                                                       |0014.01    
060700             STRING  AX-TRAB         DELIMITED BY SPACES,         |0014.01    
060750                     AX-REQ-PROCESSO DELIMITED BY SPACES          |0014.01    
060800                                     INTO   AX-TRAB.              |0014.01    
060820                                                                  |0014.01    
060860                                                                  |0014.01    
060950** MONTAGEM CAMPO AX-REQ-PROCVRNUMER                              |0014.01    
061000                                                                  |0014.01    
061050       IF    AX-RC-VLR-NUM           =  LOW-VALUES     OR         |0014.01    
061100                                            SPACES     OR         |0014.01    
061150                                            ZEROS                 |0014.01    
061160             NEXT    SENTENCE                                     |0014.01    
061180       ELSE                                                       |0014.01    
061200             STRING  AX-TRAB         DELIMITED BY SPACES,         |0014.01    
061250                     AX-REQ-VRNUMER  DELIMITED BY SPACES          |0014.01    
061300                                     INTO   AX-TRAB.              |0014.01    
061400                                                                  |0014.01    
061460                                                                  |0014.01    
061500** MONTAGEM CAMPO AX-REQ-TEXTO                                    |0014.01    
061550                                                                  |           
061806                                                                  |0014.01    
061808     IF      AX-RC-TEXTO             =  LOW-VALUES  OR            |0014.01    
061810                                            SPACES  OR            |0014.01    
061812                                            ZEROS                 |0014.01    
061814             NEXT    SENTENCE                                     |0014.01    
061816     ELSE                                                         |0014.01    
061820             STRING  AX-TRAB         DELIMITED BY SPACES,         |0014.01    
061822                     AX-REQ-TEXTO    DELIMITED BY SPACES          |0014.01    
061824                                     INTO   AX-TRAB.              |0014.01    
061828                                                                  |0014.01    
061860                                                                  |0014.01    
061900                                                                  |0014.01    
061950** MONTAGEM CAMPO PARA AS DEMAIS OBSERVACOES                      |0014.01    
061955                                                                  |0014.01    
061960     STRING  AX-TRAB                 DELIMITED BY SPACES,         |0014.01    
061965             AX-REQ-CHASSI           DELIMITED BY SPACES,         |0014.01    
061970             AX-REQ-PLACA            DELIMITED BY SPACES,         |0014.01    
061975             AX-REQ-RENAVAM          DELIMITED BY LOW-VALUES      |0014.01    
061980                                     INTO   AX-DADOS-IDENT.       |0014.01    
061990                                                                  |0014.01    
061995                                                                  |0014.01    
064000                                                                  |0014.01    
072660                                                                  |0012.01    
072700 010-099-MONTA-MENSAGEM.                                          |           
072800                                                                  |           
072900     STRING  AX-IP                    DELIMITED BY SPACES,        |           
073000             AX-COMPLEMENTO           DELIMITED BY SPACES,        |           
073100             AX-DADOS-IDENT           DELIMITED BY SIZE           |0014.01    
073200             INTO                     AX-PARAM-DADOS.             |           
073300                                                                  |           
073500                                                                  |           
073600 010-S-INICIO.                                                    |           
073700     EXIT.                                                        |           
073800                                                                  |           
073900/----------------------------------------------------------------*|           
074000*        ROTINA  DE  TRATAMENTO  DAS  TRANSACOES  DO  PROGRAMA   *|           
074100*----------------------------------------------------------------*|           
074200                                                                  |           
074300 020-E-PROCESSA.                                                  |           
074400*                                                                 |           
074500*    DISPLAY " GAA/L160-IDA = "AX-PARAM-DADOS.                    |0009.01    
074600                                                                  |0009.01    
074700*    INICIALIZA A AREA DE PARAMETROS DA LIB ALGOL GAAL170         |0009.01    
074800     MOVE      SPACES               TO      AX-PARAM01            |0009.01    
074900                                            AX-PARAM02            |0009.01    
075000                                            AX-PARAM03            |0009.01    
075100                                            AX-PARAM04.           |0009.01    
075200                                                                  |0009.01    
075300     MOVE      L160-LOGFILE         TO      AX-PARAM01.           |0009.01    
075400     MOVE      AX-PARAM-DADOS       TO      AX-PARAM02.           |0009.01    
075500                                                                  |0004.01    
075600*----- LIBRARY DO ALDEMIR                                         |           
075700                                                                  |0009.01    
075800     CALL    "WEBSERVICE  IN  PC/LIB/WEBAPPSUPPORT"               |0009.01    
075900                    USING              AX-PARAM.                  |0009.01    
076000                                                                  |           
076100*------------------------                                         |           
076200                                                                  |0007.01    
076300     MOVE      AX-PARAM             TO      AX-PARAM03            |0009.01    
076400                                                                  |0009.01    
076410                                                                  |0011.01    
076420     IF      L160-SOLIC             =       8                     |0011.01    
076455        MOVE    AX-PARAM03          TO      L160-RETORNO-BIN      |0011.01    
076460        GO      TO         020-S-PROCESSA.                        |0011.01    
076470                                                                  |0011.01    
076500*----- LIBRARY ALGOL GAAL170 DOMINGOS                             |0009.01    
076600                                                                  |0004.01    
076700     CALL    "PESQSTRING OF PC/GAA/L170"                          |0003.01    
076800                        USING        AX-PARAM01                   |0009.01    
076900                                     AX-PARAM02                   |0009.01    
077000                                     AX-PARAM03                   |0009.01    
077100                                     AX-PARAM04.                  |0009.01    
077200                                                                  |0009.01    
077300     MOVE      AX-PARAM04           TO      L160-RETORNO-BIN.     |0009.01    
077400*                                                                 |0009.01    
077500*                                                                 |           
077600 020-S-PROCESSA.                                                  |           
077700     EXIT.                                                        |           
077800*----------------------------------------------------------------*|           
