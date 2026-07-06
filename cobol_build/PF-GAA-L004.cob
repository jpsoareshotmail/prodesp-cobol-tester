       IDENTIFICATION  DIVISION.
       PROGRAM-ID.     PF-GAA-L004.

       ENVIRONMENT DIVISION.
       CONFIGURATION   SECTION.
       REPOSITORY.
           FUNCTION ALL INTRINSIC.

       DATA        DIVISION.
       WORKING-STORAGE SECTION.

       01  WS-PLACA-INPUT        PIC X(010).
       01  WS-RESULT             PIC 9(002) VALUE 0.

       01  LC-PLACA              PIC X(010).
       01  LC-PLACA-R            REDEFINES LC-PLACA.
           05  LC-FAIXA.
               10  FILLER        PIC X(002).
               10  LC-FAIXA-3    PIC X(001).
           05  LC-MILHAR         PIC X(001).
           05  LC-SERIE          PIC X(001).
           05  LC-DEZENA         PIC X(002).
           05  FILLER            PIC X(003).

       PROCEDURE DIVISION.
       MAIN-PARA.
           ACCEPT WS-PLACA-INPUT FROM ENVIRONMENT "COB_PLACA"
           MOVE UPPER-CASE(WS-PLACA-INPUT) TO LC-PLACA
           MOVE 0 TO WS-RESULT

           EVALUATE TRUE
               WHEN LC-PLACA = SPACES
                   MOVE 0 TO WS-RESULT

               WHEN LC-FAIXA-3 IS NUMERIC
                   IF LC-DEZENA = SPACES
                       MOVE 34 TO WS-RESULT
                   ELSE
                       MOVE 33 TO WS-RESULT
                   END-IF

               WHEN LC-MILHAR NOT NUMERIC
                   MOVE 0 TO WS-RESULT
               WHEN LC-DEZENA NOT NUMERIC
                   MOVE 0 TO WS-RESULT
               WHEN LC-FAIXA NOT ALPHABETIC
                   MOVE 0 TO WS-RESULT
               WHEN LC-SERIE NOT NUMERIC AND
                    LC-SERIE NOT ALPHABETIC
                   MOVE 0 TO WS-RESULT

               WHEN OTHER
                   IF  (LC-FAIXA >= "BFA" AND LC-FAIXA <= "GKI")
                    OR (LC-FAIXA >= "QSN" AND LC-FAIXA <= "QSZ")
                    OR (LC-FAIXA >= "SSR" AND LC-FAIXA <= "SWZ")
                    OR (LC-FAIXA >= "TIO" AND LC-FAIXA <= "TMJ")
                    OR (LC-FAIXA >= "UDA" AND LC-FAIXA <= "UGV")
                    OR (LC-FAIXA >= "UOG" AND LC-FAIXA <= "USB")
                       IF LC-SERIE IS NUMERIC
                           MOVE 22 TO WS-RESULT
                       ELSE
                           MOVE 12 TO WS-RESULT
                       END-IF
                   ELSE
                       IF LC-SERIE IS NUMERIC
                           MOVE 21 TO WS-RESULT
                       ELSE
                           MOVE 11 TO WS-RESULT
                       END-IF
                   END-IF
           END-EVALUATE

           DISPLAY WS-RESULT
           STOP RUN.
