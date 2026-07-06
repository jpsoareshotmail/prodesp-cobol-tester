      ******************************************************************
      * WSGLDB - Working-Storage Global Database Variables
      * Stub para compilacao com GnuCOBOL (sem acesso real a DB)
      ******************************************************************
       01  WS-DB-GLOBAL.
           05  WS-DB-STATUS          PIC X(002) VALUE "00".
           05  WS-DB-SQLCODE         PIC S9(009) COMP VALUE ZEROS.
           05  WS-DB-ROWS            PIC 9(009) VALUE ZEROS.
       01  DATABASE-OPEN-MODE        PIC X(010) VALUE "INPUT".
       01  DATABASE-NAME             PIC X(030) VALUE "PRODESP".
       01  DATABASE-STATUS           PIC X(002) VALUE "00".
       01  DATABASE-RETURN-CODE      PIC S9(004) COMP VALUE ZEROS.
       01  DATABASE-OPEN             PIC X(010) VALUE SPACES.
       01  SQLCODE                   PIC S9(009) COMP VALUE ZEROS.
       01  SQLERRMC                  PIC X(070) VALUE SPACES.
       01  SQLSTATE                  PIC X(005) VALUE "00000".
       01  SQL-STATUS                PIC X(002) VALUE "00".
       01  SQL-RETURN-CODE           PIC S9(009) COMP VALUE ZEROS.
       01  WS-SQLCODE                PIC S9(009) COMP VALUE ZEROS.
       01  WS-ROWCOUNT               PIC 9(009) VALUE ZEROS.
       01  ROWCOUNT                  PIC 9(009) VALUE ZEROS.
       01  DMSTATUS-S                PIC X(002) VALUE "00".
       01  DMSTATUS                  PIC S9(004) COMP VALUE ZEROS.
       01  DM-STATUS                 PIC X(002) VALUE "00".
       01  ROUTINE-REF               PIC X(030) VALUE SPACES.
       01  COMMAND-COD               PIC X(010) VALUE SPACES.
