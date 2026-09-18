      ******************************************************************
      * WSGL - Working-Storage Global Variables
      * Stub para compilacao com GnuCOBOL
      ******************************************************************
       01  WS-GLOBAL-VARS.
           05  WS-RETURN-CODE        PIC 9(004) VALUE ZEROS.
           05  WS-ERROR-FLAG         PIC 9(001) VALUE ZEROS.
           05  WS-ERROR-MSG          PIC X(080) VALUE SPACES.
           05  WS-PROGRAM-NAME       PIC X(010) VALUE SPACES.
           05  WS-TIMESTAMP          PIC X(026) VALUE SPACES.
       01  MYSELF.
           05  TASKVALUE        PIC X(008) VALUE SPACES.
      * Controle de transacao DMS (mainframe) - inferido para compilacao
       01  TRANSACTION-MODE         PIC X(020) VALUE SPACES.
       01  TRANSACTION-DATASET      PIC X(030) VALUE SPACES.
      * C-MAPA fica por ultimo de proposito: programas que recebem tela via
      * "RECEIVE ... MESSAGE INTO C-MAPA" (neutralizado neste ambiente sem
      * DMS/CICS real) enxergam o mesmo buffer atraves de varios copybooks
      * de tela (GERA01/COFI04/RENA01/etc, cada um "01 X REDEFINES C-MAPA")
      * copiados em pontos diferentes do fonte. COBOL exige que um REDEFINES
      * venha logo apos o item original (sem outro 01-level no meio) - com
      * C-MAPA no final daqui, o pre-processador (ver
      * sql_preprocessor._agrupar_copies_mapa_tela) so' precisa mover os
      * COPYs de tela pra logo depois do 'COPY WSGL.' do fonte, sem ter que
      * tocar na ordem interna deste copybook de novo.
       01  C-MAPA                   PIC X(008) VALUE SPACES.
