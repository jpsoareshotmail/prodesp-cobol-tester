 $ SET SHARING = SHAREDBYALL                                            
                                                                        
BEGIN                                                                   
                                                                        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
%                                                                    %  
% V=004 - 08/03/91 ==> PROCEDURE CALCDATA2, FOI INCLUIDO AS OP['ES   %  
% 14 (DATADIA2 - ANO COM 4 DIGITOS), 15 (DIASEMANA1 - ANO COM 4 DI-  %  
% GITOS) E 16 (SUBTRDATA1 - ANO COM 4 DIGITOS). FOI INCLUIDO  TAM-   %  
% BEM UMA BOOLEAN PROCEDURE QUE RETORNA SE O ANO E BISSEXTO.         %  
%                                                                    %  
% V=005 - 03/09/93 ==> PROCEDURE SUBTDATA NAO ESTAVA FAZENDO A SUB-  %  
% TRA[]O CORRETA DAS DATAS PASSADAS, NO IF DIA1 GEQ DIAT[MES3] THEN  %  
% LINHA 69600) FOI ALTERADO PARA "GTR".                              %  
%                                                                    %  
% V=006 - 27/09/94 ==> INCLUSAO DAS PROCEDURES "GREG_TO_JULIAN" E    %  
% "JULIAN_TO_GREG".                                                  %  
%                                                                    %  
% V=007 - 16/09/94 ==> ALTERACAO DAS PROCEDURES "GREG_TO_JULIAN" E   %  
% "JULIAN_TO_GREG" PARA ACEITAR ANO COM QUATRO POSICOES.             %  
%                                                                    %  
%                                                                    %  
% V=010 - 11/01/99 ==> ALTERADO A PROCEDURE ANOBISSEXTO    AHM/OSM   %  
%                                                                    %  
% V=011 - MARCO/99 ==> GERADO A PROCEDURE SUBTDATA2        DGL       %  
%                                                                    %  
%                                                                    %  
% V=012 - MARCO/99 ==> ALTERADO A PROCEDURE ANOBISSEXTO              %  
%                      GERADO A PROCEDURE CALCDATA3        DGL       %  
%                                                                    %  
% V=015 - 08/10/99 ==> ACERTO DA OPCAO 4 DA CALCDATA3 E A DA OPCAO 7 %  
%                      DA CALCDATA2                        OSM       %  
%                                                                    %  
% V=021 - 02/01/02 ==> FOI ALTERADO O ANO (2002) NAS LINHAS 2193000  %  
%                      E 3919000 E INCLUIDO OS FERIADOS DE CARNAVAL, %  
%                      PAIXAO E CORPUS CRISTI                        %  
%                                                                    %  
% V=022 - 16/12/02 ==> FOI ALTERADA A DATA LIMITE PARA 2012(2193000  %  
%                      E 3919000)E INCLUIDO OS FERIADOS DE CARNAVAL, %  
%                      PAIXAO E CORPUS CRISTI ATE 2012, INCLUIDA  A  %  
%                      DATA DE 09/07 NOS FERIADOS FIXOS NAS ROTINAS  %  
%                      CALCDATA2 (OPCAO 10) E CALCDATA3 (OPCAO 9).   %  
%                                                           OSMAR.   %  
% V=023 - 25/03/04 ==> ALTERADAS AS SEQUENCIAS ABAIXO                %  
%01990000 %  IF   DIA2  EQL  29  AND  MES2  EQL  03  AND NOT BRESTO29%  
%1990100  %    THEN                                                  %  
%1991000  %       BEGIN                                              %  
%1992000  %       ANOB:=ANO2;                                        %  
%1993000  %       IF    ANOBISSEXTO  THEN                            %  
%1994000  %             BEGIN                                        %  
%1995000  %               MES2:=*  -  1;                             %  
%1996000  %               DIA2:=29;                                  %  
%1997000  %             END;                                         %  
%1998000  %       END;                                               %  
% V=024 - 25/03/04 ==> INSERIDAS AS SEQUENCIAS ABAIXO                %  
%          2245025           OR ANO1 EQL 2012 OR ANO1 EQL 2016       %  
%          2746020           OR ANO1 EQL 2012 OR ANO1 EQL 2016       %  
%          3244770           OR ANO1 EQL 2012 OR ANO1 EQL 2016       %  
%          3971050         OR ANO1 EQL 2012 OR ANO1 EQL 2016         %  
% V=025 - 27/02/12 ==> FOI ALTERADA A DATA LIMITE PARA 2016(2193000  %  
%                      E 3919000) E INCLUIDOS OS FERIADOS DE CARNAVAL,% 
%                      PAIXAO E CORPUS CRISTI ATE 2016.              %  
%                                                                    %  
% V=026 - 15/12/16 ==> FOI ALTERADA A DATA LIMITE PARA 2036(2193000  %  
%                      E 3919000) E INCLUIDOS OS FERIADOS DE CARNAVAL,% 
%                      PAIXAO E CORPUS CRISTI ATE 2036.              %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%                                                                    %  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
                                                                        
                                                                        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
%                                                                    %  
%                       LIBRARY     DATAEX                           %  
%                                                                    %  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
                                                                        
PROCEDURE DATAEX(A1,A2);                                                
EBCDIC ARRAY A1,A2[0];                                                  
                                                                        
 BEGIN                                                                  
     FILE REM(KIND=REMOTE,MAXRECSIZE=22);                               
                                                                        
     ARRAY DIAS    [0:30,0:2],                                          
           MESES   [0:11,0:1],                                          
           DECADAS [0:2,0:1],                                           
           A       [0:43],                                              
           C       [0:0];                                               
                                                                        
     INTEGER DIA,                                                       
             MES,                                                       
             ANO,                                                       
             ANO10;                                                     
                                                                        
     POINTER PA,                                                        
             PB;                                                        
                                                                        
     LABEL   FIM;                                                       
                                                                        
     PROCEDURE ESTICA(A,B);                                             
     ARRAY B[*]; POINTER A;                                             
                                                                        
     BEGIN                                                              
         INTEGER I,J,K,L,M,N,TAM;                                       
         TAM := INTEGER(POINTER(B),6);                                  
                                                                        
         BEGIN                                                          
             EBCDIC ARRAY AUX[0:TAM-1];                                 
             LABEL FIM2;                                                
             POINTER PA,PB;                                             
             PA:=A+TAM;                                                 
             FOR I:=1 STEP 1 UNTIL TAM DO                               
                                                                        
             BEGIN                                                      
                 SCAN PA - I FOR J:1 UNTIL NEQ " ";                     
                 IF J > 0 THEN                                          
                                                                        
                 BEGIN                                                  
                     PA:=PA-I;                                          
                     J:=TAM-I+1;                                        
                     I:=TAM+1;                                          
                 END;                                                   
                                                                        
             END;                                                       
             IF J = 0 OR J = TAM THEN GO TO FIM2;                       
             K := TAM - J;                                              
             I:=0;                                                      
             FOR M:=1 STEP 1 UNTIL J-1 DO                               
                                                                        
             BEGIN                                                      
                 SCAN PA - M FOR N:1 UNTIL EQL " ";                     
                 IF N > 0 THEN  I:=I+1;                                 
             END;                                                       
             PA:=A;                                                     
             PB:=AUX[0];                                                
             FOR L:=1 STEP 1 UNTIL I DO                                 
                                                                        
             BEGIN                                                      
                 REPLACE PB:PB BY PA:PA WHILE NEQ " ";                  
                 REPLACE PB:PB BY PA:PA FOR 1;                          
                 IF K DIV I > 0 THEN                                    
                    REPLACE PB:PB BY " " FOR K DIV I;                   
                 IF K MOD I > 0 AND L > I - K MOD I THEN                
                    REPLACE PB:PB BY " ";                               
             END;                                                       
             REPLACE PB:PB BY PA:PA FOR TAM - DELTA(A,PA) - K + 1;      
             REPLACE A BY AUX[0] FOR TAM;                               
             FIM2:                                                      
         END;                                                           
     END;                                                               
                                                                        
     PROCEDURE DIVIDE(A,B);                                             
     POINTER A; ARRAY B[*];                                             
                                                                        
     BEGIN                                                              
         INTEGER I,J,TAM; POINTER PA,PB;                                
         EBCDIC ARRAY AUX[0:65];                                        
         REPLACE AUX BY " " FOR 12;                                     
         IF ( A+56 NEQ " " FOR 1 AND A+57 EQL " " FOR 1 ) OR            
            ( A+56 EQL " " FOR 1 AND A+57 NEQ " " FOR 1 ) THEN          
             BEGIN                                                      
                 IF A + 57 EQL " " FOR 1 THEN                           
                 REPLACE AUX[09] BY A+57 FOR 57                         
                 ELSE                                                   
                    REPLACE AUX[10] BY A+57 FOR 56;                     
             END                                                        
         ELSE                                                           
            BEGIN                                                       
                PA:=A;                                                  
                J:=INTEGER(POINTER(B),6);                               
                WHILE J > 0 DO                                          
                                                                        
                BEGIN                                                   
                    SCAN PA:PA FOR J:J WHILE NEQ " ";                   
                    IF J > 0 THEN                                       
                    PB:=PA;                                             
                    PA:=PA+1;                                           
                    J:=J-1;                                             
                END;                                                    
                                                                        
                REPLACE AUX[10] BY PB+1 FOR 56;                         
                REPLACE PB+1 BY " " FOR 56;                             
            END;                                                        
                                                                        
            FOR J:=64 STEP -2 UNTIL 0 DO                                
            IF AUX[J] NEQ "  " THEN                                     
                                                                        
               BEGIN                                                    
                   I:=J;                                                
                   J:=-2;                                               
               END                                                      
            ELSE                                                        
               REPLACE AUX[J+1] BY "-" FOR 1;                           
                                                                        
            IF AUX[I+1] EQL " " THEN                                    
               REPLACE AUX[I+1] BY "-" FOR 1;                           
            REPLACE A+57 BY AUX FOR 66;                                 
            ESTICA(A,B);                                                
     END;                                                               
                                                                        
     FILL DIAS    [00,*] WITH "08PRIMEIRO        ";                     
     FILL DIAS    [01,*] WITH "04DOIS            ";                     
     FILL DIAS    [02,*] WITH "04TRES            ";                     
     FILL DIAS    [03,*] WITH "06QUATRO          ";                     
     FILL DIAS    [04,*] WITH "05CINCO           ";                     
     FILL DIAS    [05,*] WITH "04SEIS            ";                     
     FILL DIAS    [06,*] WITH "04SETE            ";                     
     FILL DIAS    [07,*] WITH "04OITO            ";                     
     FILL DIAS    [08,*] WITH "04NOVE            ";                     
     FILL DIAS    [09,*] WITH "03DEZ             ";                     
     FILL DIAS    [10,*] WITH "04ONZE            ";                     
     FILL DIAS    [11,*] WITH "04DOZE            ";                     
     FILL DIAS    [12,*] WITH "05TREZE           ";                     
     FILL DIAS    [13,*] WITH "08QUATORZE        ";                     
     FILL DIAS    [14,*] WITH "06QUINZE          ";                     
     FILL DIAS    [15,*] WITH "09DEZESSEIS        ";                    
     FILL DIAS    [16,*] WITH "09DEZESSETE        ";                    
     FILL DIAS    [17,*] WITH "07DEZOITO         ";                     
     FILL DIAS    [18,*] WITH "08DEZENOVE        ";                     
     FILL DIAS    [19,*] WITH "05VINTE           ";                     
     FILL DIAS    [20,*] WITH "10VINTE E UM      ";                     
     FILL DIAS    [21,*] WITH "12VINTE E DOIS    ";                     
     FILL DIAS    [22,*] WITH "12VINTE E TRES    ";                     
     FILL DIAS    [23,*] WITH "14VINTE E QUATRO  ";                     
     FILL DIAS    [24,*] WITH "13VINTE E CINCO   ";                     
     FILL DIAS    [25,*] WITH "12VINTE E SEIS    ";                     
     FILL DIAS    [26,*] WITH "12VINTE E SETE    ";                     
     FILL DIAS    [27,*] WITH "12VINTE E OITO    ";                     
     FILL DIAS    [28,*] WITH "12VINTE E NOVE    ";                     
     FILL DIAS    [29,*] WITH "06TRINTA          ";                     
     FILL DIAS    [30,*] WITH "11TRINTA E UM     ";                     
     FILL MESES   [00,*] WITH "07JANEIRO   ";                           
     FILL MESES   [01,*] WITH "09FEVEREIRO ";                           
     FILL MESES   [02,*] WITH "05MARCO     ";                           
     FILL MESES   [03,*] WITH "05ABRIL     ";                           
     FILL MESES   [04,*] WITH "04MAIO      ";                           
     FILL MESES   [05,*] WITH "05JUNHO     ";                           
     FILL MESES   [06,*] WITH "05JULHO     ";                           
     FILL MESES   [07,*] WITH "06AGOSTO    ";                           
     FILL MESES   [08,*] WITH "08SETEMBRO  ";                           
     FILL MESES   [09,*] WITH "07OUTUBRO   ";                           
     FILL MESES   [10,*] WITH "08NOVEMBRO  ";                           
     FILL MESES   [11,*] WITH "08DEZEMBRO  ";                           
     FILL DECADAS [00,*] WITH "07SETENTA   ";                           
     FILL DECADAS [01,*] WITH "07OITENTA   ";                           
     FILL DECADAS [02,*] WITH "07NOVENTA   ";                           
     DIA:=INTEGER(A1[0],2);                                             
     MES:=INTEGER(A1[2],2);                                             
     ANO:=INTEGER(A1[4],2);                                             
     ANO10:=ANO-10;                                                     
     FILL A[*] WITH 44("      ");                                       
     PA:=POINTER(A);                                                    
     REPLACE PA:PA BY DIA FOR 2 DIGITS;                                 
     REPLACE PA:PA BY "/";                                              
     REPLACE PA:PA BY MES FOR 2 DIGITS;                                 
     REPLACE PA:PA BY "/";                                              
     REPLACE PA:PA BY ANO10 FOR 2 DIGITS;                               
     REPLACE PA:PA BY " ";                                              
     REPLACE PA:PA BY "(";                                              
     REPLACE PA:PA BY POINTER(DIAS[DIA-1,0])+2 FOR                      
                      INTEGER(POINTER(DIAS[DIA-1,0]),2) ;               
     REPLACE PA:PA BY " DE ";                                           
     REPLACE PA:PA BY POINTER(MESES[MES-1,0])+2 FOR                     
                      INTEGER(POINTER(MESES[MES-1,0]),2);               
     REPLACE PA:PA BY " DE MIL NOVECENTOS E ";                          
     REPLACE PA:PA BY POINTER(DECADAS[ANO DIV 10 - 8,0])+2 FOR          
                      INTEGER(POINTER(DECADAS[ANO DIV 10 - 7,0]),2);    
     IF ANO MOD 10 >   1 THEN                                           
                                                                        
        BEGIN                                                           
            REPLACE PA:PA BY " E ";                                     
            REPLACE PA:PA BY POINTER(DIAS[ANO MOD 10 - 1,0])+2 FOR      
                    INTEGER(POINTER(DIAS[ANO MOD 10 - 1,0]),2);         
        END                                                             
                                                                        
     ELSE                                                               
        IF ANO MOD 10 = 1 THEN                                          
                                                                        
           BEGIN                                                        
               REPLACE PA:PA BY " E ";                                  
               REPLACE PA:PA BY "UM";                                   
           END;                                                         
                                                                        
     REPLACE PA:PA BY ")*A";                                            
     PB:=POINTER(A)+132;                                                
     REPLACE PB:PB BY DIA FOR 2 DIGITS;                                 
     REPLACE PB:PB BY "/";                                              
     REPLACE PB:PB BY MES FOR 2 DIGITS;                                 
     REPLACE PB:PB BY "/";                                              
     REPLACE PB:PB BY ANO FOR 2 DIGITS;                                 
     REPLACE PB:PB BY " ";                                              
     REPLACE PB:PB BY "(";                                              
     REPLACE PB:PB BY POINTER(DIAS[DIA-1,0])+2 FOR                      
                      INTEGER(POINTER(DIAS[DIA-1,0]),2) ;               
     REPLACE PB:PB BY " DE ";                                           
     REPLACE PB:PB BY POINTER(MESES[MES-1,0])+2 FOR                     
                      INTEGER(POINTER(MESES[MES-1,0]),2);               
     REPLACE PB:PB BY " DE MIL NOVECENTOS E ";                          
     REPLACE PB:PB BY POINTER(DECADAS[ANO DIV 10 - 7,0])+2 FOR          
                      INTEGER(POINTER(DECADAS[ANO DIV 10 - 7,0]),2);    
     IF ANO MOD 10 >   1 THEN                                           
                                                                        
        BEGIN                                                           
            REPLACE PB:PB BY " E ";                                     
            REPLACE PB:PB BY POINTER(DIAS[ANO MOD 10 - 1,0])+2 FOR      
                    INTEGER(POINTER(DIAS[ANO MOD 10 - 1,0]),2);         
        END                                                             
     ELSE                                                               
        IF ANO MOD 10 = 1 THEN                                          
           BEGIN                                                        
               REPLACE PB:PB BY " E ";                                  
               REPLACE PB:PB BY "UM";                                   
           END;                                                         
                                                                        
     REPLACE PB:PB BY "),";                                             
     REPLACE POINTER(C) BY "000057";                                    
                                                                        
     IF DELTA(POINTER(A)+09,PA) < 58 THEN                               
        BEGIN                                                           
            PA:=POINTER(A)+09;                                          
            ESTICA(PA,C);                                               
        END                                                             
     ELSE                                                               
        BEGIN                                                           
            PA:=POINTER(A)+09;                                          
            DIVIDE(PA,C);                                               
        END;                                                            
                                                                        
     IF DELTA(POINTER(A)+141,PB) < 58 THEN                              
        BEGIN                                                           
            PB:=POINTER(A)+141;                                         
            ESTICA(PB,C);                                               
        END                                                             
     ELSE                                                               
        BEGIN                                                           
            PB:=POINTER(A)+141;                                         
            DIVIDE(PB,C);                                               
%       END;                                                            
        END;                                                            
     SCAN PA:POINTER(A) FOR 132 WHILE NEQ "*";                          
     REPLACE PA BY " " FOR 1;                                           
     REPLACE A2[0] BY POINTER(A) FOR 264;                               
 FIM:                                                                   
 END OF DATAEX;                                                         
                                                                        
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
 %                                                                   %  
 %                        LIBRARY     DATAEX72                       %  
 %                                                                   %  
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
                                                                        
 PROCEDURE DATAEX72(A1,A2);                                             
 EBCDIC ARRAY A1,A2[0];                                                 
                                                                        
 BEGIN                                                                  
     FILE REM(KIND=REMOTE,MAXRECSIZE=22);                               
                                                                        
     ARRAY DIAS[0:30,0:2],                                              
           MESES[0:11,0:1],                                             
           DECADAS[0:2,0:1],                                            
           A[0:47],                                                     
           C[0:0];                                                      
                                                                        
     INTEGER DIA,                                                       
             MES,                                                       
             ANO,                                                       
             ANO10;                                                     
                                                                        
     POINTER PA,                                                        
             PB;                                                        
                                                                        
     LABEL FIM;                                                         
                                                                        
     PROCEDURE ESTICA(A,B);                                             
     ARRAY B[*]; POINTER A;                                             
                                                                        
     BEGIN                                                              
         INTEGER I,J,K,L,M,N,TAM;                                       
         TAM := INTEGER(POINTER(B),6);                                  
         BEGIN                                                          
             EBCDIC ARRAY AUX[0:TAM-1];                                 
             LABEL FIM2;                                                
             POINTER PA,PB;                                             
             PA:=A+TAM;                                                 
             FOR I:=1 STEP 1 UNTIL TAM DO                               
             BEGIN                                                      
                 SCAN PA - I FOR J:1 UNTIL NEQ " ";                     
                 IF J > 0 THEN                                          
                    BEGIN                                               
                        PA:=PA-I;                                       
                        J:=TAM-I+1;                                     
                        I:=TAM+1;                                       
                    END;                                                
             END;                                                       
             IF J = 0 OR J = TAM THEN GO TO FIM2;                       
             K := TAM - J;                                              
             I:=0;                                                      
             FOR M:=1 STEP 1 UNTIL J-1 DO                               
                 BEGIN                                                  
                     SCAN PA - M FOR N:1 UNTIL EQL " ";                 
                     IF N > 0 THEN  I:=I+1;                             
                 END;                                                   
             PA:=A;                                                     
             PB:=AUX[0];                                                
             FOR L:=1 STEP 1 UNTIL I DO                                 
                 BEGIN                                                  
                     REPLACE PB:PB BY PA:PA WHILE NEQ " ";              
                     REPLACE PB:PB BY PA:PA FOR 1;                      
                     IF K DIV I > 0 THEN                                
                     REPLACE PB:PB BY " " FOR K DIV I;                  
                     IF K MOD I > 0 AND L > I - K MOD I THEN            
                     REPLACE PB:PB BY " ";                              
                 END;                                                   
             REPLACE PB:PB BY PA:PA FOR TAM - DELTA(A,PA) - K + 1;      
             REPLACE A BY AUX[0] FOR TAM;                               
             FIM2:                                                      
         END;                                                           
     END;                                                               
     PROCEDURE DIVIDE(A,B);                                             
     POINTER A; ARRAY B[*];                                             
                                                                        
     BEGIN                                                              
         INTEGER I,J,TAM; POINTER PA,PB;                                
         EBCDIC ARRAY AUX[0:71];                                        
         REPLACE AUX BY " " FOR 12;                                     
         IF ( A+62 NEQ " " FOR 1 AND A+63 EQL " " FOR 1 ) OR            
            ( A+62 EQL " " FOR 1 AND A+63 NEQ " " FOR 1 ) THEN          
                                                                        
            BEGIN                                                       
                IF A + 63 EQL " " FOR 1 THEN                            
                   REPLACE AUX[09] BY A+63 FOR 63                       
                ELSE                                                    
                   REPLACE AUX[10] BY A+63 FOR 62;                      
            END                                                         
                                                                        
         ELSE                                                           
                                                                        
             BEGIN                                                      
                 PA:=A;                                                 
                 J:=INTEGER(POINTER(B),6);                              
                 WHILE J > 0 DO                                         
                 BEGIN                                                  
                     SCAN PA:PA FOR J:J WHILE NEQ " ";                  
                     IF J > 0 THEN                                      
                     PB:=PA;                                            
                     PA:=PA+1;                                          
                     J:=J-1;                                            
                 END;                                                   
                 REPLACE AUX[10] BY PB+1 FOR 62;                        
                 REPLACE PB+1 BY " " FOR 62;                            
             END;                                                       
             FOR J:=70 STEP -2 UNTIL 0 DO                               
             IF AUX[J] NEQ "  " THEN                                    
                BEGIN                                                   
                    I:=J;                                               
                    J:=-2;                                              
                END                                                     
             ELSE                                                       
                REPLACE AUX[J+1] BY "-" FOR 1;                          
             IF AUX[I+1] EQL " " THEN                                   
                REPLACE AUX[I+1] BY "-" FOR 1;                          
             REPLACE A+63 BY AUX FOR 72;                                
             ESTICA(A,B);                                               
     END;                                                               
     FILL DIAS    [00,*] WITH "08PRIMEIRO        ";                     
     FILL DIAS    [01,*] WITH "04DOIS            ";                     
     FILL DIAS    [02,*] WITH "04TRES            ";                     
     FILL DIAS    [03,*] WITH "06QUATRO          ";                     
     FILL DIAS    [04,*] WITH "05CINCO           ";                     
     FILL DIAS    [05,*] WITH "04SEIS            ";                     
     FILL DIAS    [06,*] WITH "04SETE            ";                     
     FILL DIAS    [07,*] WITH "04OITO            ";                     
     FILL DIAS    [08,*] WITH "04NOVE            ";                     
     FILL DIAS    [09,*] WITH "03DEZ             ";                     
     FILL DIAS    [10,*] WITH "04ONZE            ";                     
     FILL DIAS    [11,*] WITH "04DOZE            ";                     
     FILL DIAS    [12,*] WITH "05TREZE           ";                     
     FILL DIAS    [13,*] WITH "08QUATORZE        ";                     
     FILL DIAS    [14,*] WITH "06QUINZE          ";                     
     FILL DIAS    [15,*] WITH "09DEZESSEIS       ";                     
     FILL DIAS    [16,*] WITH "09DEZESSETE       ";                     
     FILL DIAS    [17,*] WITH "07DEZOITO         ";                     
     FILL DIAS    [18,*] WITH "08DEZENOVE        ";                     
     FILL DIAS    [19,*] WITH "05VINTE           ";                     
     FILL DIAS    [20,*] WITH "10VINTE E UM      ";                     
     FILL DIAS    [21,*] WITH "12VINTE E DOIS    ";                     
     FILL DIAS    [22,*] WITH "12VINTE E TRES    ";                     
     FILL DIAS    [23,*] WITH "14VINTE E QUATRO  ";                     
     FILL DIAS    [24,*] WITH "13VINTE E CINCO   ";                     
     FILL DIAS    [25,*] WITH "12VINTE E SEIS    ";                     
     FILL DIAS    [26,*] WITH "12VINTE E SETE    ";                     
     FILL DIAS    [27,*] WITH "12VINTE E OITO    ";                     
     FILL DIAS    [28,*] WITH "12VINTE E NOVE    ";                     
     FILL DIAS    [29,*] WITH "06TRINTA          ";                     
     FILL DIAS    [30,*] WITH "11TRINTA E UM     ";                     
     FILL MESES   [00,*] WITH "07JANEIRO         ";                     
     FILL MESES   [01,*] WITH "09FEVEREIRO       ";                     
     FILL MESES   [02,*] WITH "05MARCO           ";                     
     FILL MESES   [03,*] WITH "05ABRIL           ";                     
     FILL MESES   [04,*] WITH "04MAIO            ";                     
     FILL MESES   [05,*] WITH "05JUNHO           ";                     
     FILL MESES   [06,*] WITH "05JULHO           ";                     
     FILL MESES   [07,*] WITH "06AGOSTO          ";                     
     FILL MESES   [08,*] WITH "08SETEMBRO        ";                     
     FILL MESES   [09,*] WITH "07OUTUBRO         ";                     
     FILL MESES   [10,*] WITH "08NOVEMBRO        ";                     
     FILL MESES   [11,*] WITH "08DEZEMBRO        ";                     
     FILL DECADAS [00,*] WITH "07SETENTA         ";                     
     FILL DECADAS [01,*] WITH "07OITENTA         ";                     
     FILL DECADAS [02,*] WITH "07NOVENTA         ";                     
                                                                        
     DIA:=INTEGER(A1[0],2);                                             
     MES:=INTEGER(A1[2],2);                                             
     ANO:=INTEGER(A1[4],2);                                             
     ANO10:=ANO-10;                                                     
     FILL A[*] WITH 48("      ");                                       
     PA:=POINTER(A);                                                    
     REPLACE PA:PA BY DIA FOR 2 DIGITS;                                 
     REPLACE PA:PA BY "/";                                              
     REPLACE PA:PA BY MES FOR 2 DIGITS;                                 
     REPLACE PA:PA BY "/";                                              
     REPLACE PA:PA BY ANO10 FOR 2 DIGITS;                               
     REPLACE PA:PA BY " ";                                              
     REPLACE PA:PA BY "(";                                              
     REPLACE PA:PA BY POINTER(DIAS[DIA-1,0])+2 FOR                      
                      INTEGER(POINTER(DIAS[DIA-1,0]),2) ;               
     REPLACE PA:PA BY " DE ";                                           
     REPLACE PA:PA BY POINTER(MESES[MES-1,0])+2 FOR                     
                    INTEGER(POINTER(MESES[MES-1,0]),2);                 
     REPLACE PA:PA BY " DE MIL NOVECENTOS E ";                          
     REPLACE PA:PA BY POINTER(DECADAS[ANO DIV 10 - 8,0])+2 FOR          
                      INTEGER(POINTER(DECADAS[ANO DIV 10 - 7,0]),2);    
     IF ANO MOD 10 >   1 THEN                                           
        BEGIN                                                           
            REPLACE PA:PA BY " E ";                                     
            REPLACE PA:PA BY POINTER(DIAS[ANO MOD 10 - 1,0])+2 FOR      
            INTEGER(POINTER(DIAS[ANO MOD 10 - 1,0]),2);                 
        END                                                             
     ELSE                                                               
        IF ANO MOD 10 = 1 THEN                                          
           BEGIN                                                        
               REPLACE PA:PA BY " E ";                                  
               REPLACE PA:PA BY "UM";                                   
           END;                                                         
     REPLACE PA:PA BY ")*A";                                            
     PB:=POINTER(A)+144;                                                
     REPLACE PB:PB BY DIA FOR 2 DIGITS;                                 
     REPLACE PB:PB BY "/";                                              
     REPLACE PB:PB BY MES FOR 2 DIGITS;                                 
     REPLACE PB:PB BY "/";                                              
     REPLACE PB:PB BY ANO FOR 2 DIGITS;                                 
     REPLACE PB:PB BY " ";                                              
     REPLACE PB:PB BY "(";                                              
     REPLACE PB:PB BY POINTER(DIAS[DIA-1,0])+2 FOR                      
                      INTEGER(POINTER(DIAS[DIA-1,0]),2) ;               
     REPLACE PB:PB BY " DE ";                                           
     REPLACE PB:PB BY POINTER(MESES[MES-1,0])+2 FOR                     
                      INTEGER(POINTER(MESES[MES-1,0]),2);               
     REPLACE PB:PB BY " DE MIL NOVECENTOS E ";                          
     REPLACE PB:PB BY POINTER(DECADAS[ANO DIV 10 - 7,0])+2 FOR          
                      INTEGER(POINTER(DECADAS[ANO DIV 10 - 7,0]),2);    
     IF ANO MOD 10 >   1 THEN                                           
        BEGIN                                                           
            REPLACE PB:PB BY " E ";                                     
            REPLACE PB:PB BY POINTER(DIAS[ANO MOD 10 - 1,0])+2 FOR      
            INTEGER(POINTER(DIAS[ANO MOD 10 - 1,0]),2);                 
        END                                                             
     ELSE                                                               
        IF ANO MOD 10 = 1 THEN                                          
           BEGIN                                                        
               REPLACE PB:PB BY " E ";                                  
               REPLACE PB:PB BY "UM";                                   
           END;                                                         
     REPLACE PB:PB BY "),";                                             
     REPLACE POINTER(C) BY "000063";                                    
     IF DELTA(POINTER(A)+09,PA) < 64 THEN                               
        BEGIN                                                           
            PA:=POINTER(A)+09;                                          
            ESTICA(PA,C);                                               
        END                                                             
     ELSE                                                               
        BEGIN                                                           
            PA:=POINTER(A)+09;                                          
            DIVIDE(PA,C);                                               
        END;                                                            
                                                                        
     IF DELTA(POINTER(A)+153,PB) < 64 THEN                              
        BEGIN                                                           
            PB:=POINTER(A)+153;                                         
            ESTICA(PB,C);                                               
        END                                                             
     ELSE                                                               
        BEGIN                                                           
            PB:=POINTER(A)+153;                                         
            DIVIDE(PB,C);                                               
        END;                                                            
                                                                        
     SCAN PA:POINTER(A) FOR 144 WHILE NEQ "*";                          
     REPLACE PA BY " " FOR 1;                                           
     REPLACE A2[0] BY POINTER(A) FOR 288;                               
     FIM:                                                               
 END OF DATAEX72;                                                       
                                                                        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
%                                                                    %  
%                         LIBRARY     DATACOMP                       %  
%                                                                    %  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
                                                                        
 PROCEDURE DATACOMP(A);                                                 
 EBCDIC ARRAY A[0];                                                     
 BEGIN                                                                  
     POINTER PA;                                                        
     ARRAY B[0:0];                                                      
     B[0]:=TIME(7);                                                     
     PA := A[0];                                                        
     REPLACE PA    BY B[0].[29:06]  FOR 2 DIGITS;                       
     REPLACE PA+02 BY B[0].[35:06]  FOR 2 DIGITS;                       
     REPLACE PA+04 BY B[0].[47:12]  FOR 4 DIGITS;                       
     REPLACE PA+08 BY B[0].[23:06]  FOR 2 DIGITS;                       
     REPLACE PA+10 BY B[0].[17:06]  FOR 2 DIGITS;                       
     REPLACE PA+12 BY B[0].[11:06]  FOR 2 DIGITS;                       
     REPLACE PA+14 BY B[0].[05:06]  FOR 1 DIGITS;                       
 END OF DATACOMP;                                                       
                                                                        
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
 %                                                                  %   
 %                        LIBRARY     SUBTDATA                      %   
 %                                                                  %   
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
                                                                        
 PROCEDURE  SUBTDATA (CONS,AREAA);                                      
 EBCDIC  ARRAY  CONS,AREAA[0];                                          
 BEGIN                                                                  
      FILE  IMP(KIND=PRINTER,MAXRECSIZE=132,BLOCKSIZE=132,UNITS=1);     
      EBCDIC  ARRAY   DATAV[1:6];                                       
      REAL  VALUE  ARRAY  DIAT(0,31,28,31,30,31,30,31,31,30,31,30,31);  
      INTEGER  DIAV,                                                    
               MESV,                                                    
               ANOV,                                                    
               DIA1,                                                    
               DIA2,                                                    
               DIA3,                                                    
               MES1,                                                    
               MES2,                                                    
               MES3,                                                    
               ANO1,                                                    
               ANO2,                                                    
               ANO3,                                                    
               RESTO,                                                   
               Q1;                                                      
                                                                        
      POINTER  PTP,PTQ,PTR,PTS;                                         
      BOOLEAN  RESULT,ERRO,DIAUTIL,ACABOU;                              
      TRUTHSET   DIGITO  ("0123456789");                                
                                                                        
      PROCEDURE  VALIDATA;                                              
      BEGIN                                                             
          RESULT:=TRUE;                                                 
          PTQ:=DATAV;                                                   
          PTP:=AREAA;                                                   
          SCAN  PTQ  FOR  Q1:6  WHILE  IN  DIGITO;                      
          Q1:=6  -  Q1;                                                 
          IF     Q1     EQL   6   THEN                                  
             BEGIN                                                      
             ANOV:=INTEGER (PTQ,2);                                     
             MESV:=INTEGER (PTQ  +  2,2);                               
             DIAV:=INTEGER (PTQ  +  4,2);                               
             IF    MESV     LSS    1   OR                               
                   MESV     GTR    12  OR                               
                   DIAV     LSS    1   THEN                             
                   RESULT:=FALSE                                        
             ELSE                                                       
                BEGIN                                                   
                    IF   (DIAV   GTR  DIAT[MESV]  AND                   
                          MESV   NEQ        2) THEN                     
                          RESULT:=FALSE                                 
                    ELSE                                                
                       IF  MESV   EQL        2   THEN                   
                          BEGIN                                         
                              IF  DIAV  GTR  DIAT[MESV]  THEN           
                                BEGIN                                   
                                    RESTO:=ANOV  MOD  4;                
                                    IF   RESTO    NEQ   0  OR           
                                        (RESTO   EQL   0  AND           
                                         DIAV     NEQ   29)   THEN      
                                         RESULT:=FALSE;                 
                                END                                     
                          END                                           
                END                                                     
             END                                                        
      ELSE                                                              
         RESULT:=FALSE;                                                 
         PTR:=CONS;                                                     
         IF    NOT  RESULT  THEN                                        
               REPLACE  PTR   BY  "E"                                   
         ELSE                                                           
            REPLACE  PTR  BY  "C";                                      
      END;                                                              
                                                                        
 BEGIN                                                                  
     LABEL  SAIDA,RESP;                                                 
     PTP:=AREAA[6];                                                     
     PTQ:=DATAV;                                                        
     REPLACE  PTQ  BY  PTP:PTP  FOR  6;                                 
     ANOV:=ANO1:=INTEGER (PTQ,2);                                       
     MESV:=MES1:=INTEGER (PTQ + 2,2);                                   
     DIAV:=DIA1:=INTEGER (PTQ + 4,2);                                   
     SCAN  PTQ  FOR  Q1:6  WHILE  IN  DIGITO;                           
     Q1:=6  -  Q1;                                                      
     IF     Q1     EQL   6   THEN                                       
        BEGIN                                                           
            IF  MES1  GTR      11     OR                                
                DIA1  GTR      31     OR                                
                ANO1  GTR      ANOV   THEN                              
                BEGIN                                                   
                    PTR:=CONS;                                          
                    REPLACE  PTR  BY  "E";                              
                    GO    TO    SAIDA;                                  
                END;                                                    
        END;                                                            
     PTP:=AREAA;                                                        
     PTQ:=DATAV;                                                        
     REPLACE  PTQ  BY  PTP:PTP  FOR  6;                                 
     ANOV:=INTEGER (PTQ,2);                                             
     MESV:=INTEGER (PTQ + 2,2);                                         
     DIAV:=INTEGER (PTQ + 4,2);                                         
     VALIDATA;                                                          
     IF     NOT   RESULT    THEN                                        
        BEGIN                                                           
            PTR:=CONS;                                                  
            REPLACE  PTR  BY  "E";                                      
            GO    TO    SAIDA;                                          
        END;                                                            
     ANO3:=ANOV  -  ANO1;                                               
     IF      MESV   GTR   MES1     THEN                                 
             MES3:=MESV   -   MES1                                      
     ELSE                                                               
        BEGIN                                                           
            ANO3:=ANO3   -   1;                                         
            MES3:=MESV   +   12;                                        
            MES3:=MES3   -   MES1;                                      
        END;                                                            
     IF      DIA1   EQL   0        THEN                                 
        BEGIN                                                           
            DIA3:=DIAV;                                                 
            IF     DIA3     GTR  DIAT[MES3]   THEN                      
                   DIA3:=DIAT[MES3];                                    
                   RESTO:=ANO3   MOD  4;                                
            IF     RESTO   EQL  0    THEN                               
                   DIA3:=DIA3   +    1;                                 
                   GO     TO    RESP;                                   
        END;                                                            
        IF   DIA1   GTR   DIAT[MES3]    THEN                            
             IF   MES3    NEQ   2             THEN                      
                  BEGIN                                                 
                      PTR:=CONS;                                        
                      REPLACE  PTR  BY  "E";                            
                      GO    TO    SAIDA;                                
                  END                                                   
             ELSE                                                       
                BEGIN                                                   
                    RESTO:=ANO3   MOD   4;                              
                    IF  RESTO   EQL   0     THEN                        
                        BEGIN                                           
                            IF   DIA1    GEQ   29    THEN               
                                 BEGIN                                  
                                     PTR:=CONS;                         
                                     REPLACE  PTR  BY  "E";             
                                     GO    TO    SAIDA;                 
                                 END;                                   
                        END;                                            
                END;                                                    
     IF   DIAV   EQL   DIAT[MESV]    THEN                               
          BEGIN                                                         
              DIAV:=DIAT[MES3];                                         
              RESTO:=ANO3   MOD  4;                                     
              IF   RESTO   EQL  0    THEN                               
                   DIAV:=DIAV   +    1;                                 
          END;                                                          
     IF   DIAV   GTR   DIA1     THEN                                    
          DIA3:=DIAV   -   DIA1                                         
     ELSE                                                               
        BEGIN                                                           
            MES3:=MES3   -  1;                                          
            IF  MES3   EQL   0    THEN                                  
                BEGIN                                                   
                    ANO3:=ANO3  -   1;                                  
                    MES3:=12;                                           
                END;                                                    
            DIA3:=(DIAT[MES3]  +  DIAV)  -  DIA1;                       
            IF  MES3   EQL   2    THEN                                  
                BEGIN                                                   
                RESTO:=ANO3   MOD   4;                                  
                IF    RESTO   EQL   0    THEN                           
                      DIA3:=DIA3  +  1;                                 
                END;                                                    
        END;                                                            
     RESP:                                                              
     PTP:=AREAA[12];                                                    
     REPLACE    PTP:PTP   BY  ANO3  FOR  2  DIGITS;                     
     REPLACE    PTP:PTP   BY  MES3  FOR  2  DIGITS;                     
     REPLACE    PTP:PTP   BY  DIA3  FOR  2  DIGITS;                     
     PTQ:=CONS;                                                         
     REPLACE    PTQ       BY  "C";                                      
     SAIDA:                                                             
     END;                                                               
 END OF SUBDATA;                                                        
                                                                        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                                                                      %
%                       LIBRARY     SUBTDATA2                          %
%                                                                      %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                                        
 PROCEDURE  SUBTDATA2 (CONS,AREAA);                                     
 EBCDIC  ARRAY  CONS,AREAA[0];                                          
 BEGIN                                                                  
      FILE  IMP(KIND=PRINTER,MAXRECSIZE=132,BLOCKSIZE=132,UNITS=1);     
      EBCDIC  ARRAY   DATAV[1:8];                                       
      REAL  VALUE  ARRAY  DIAT(0,31,28,31,30,31,30,31,31,30,31,30,31);  
      INTEGER  DIAV,                                                    
               MESV,                                                    
               ANOV,                                                    
               DIA1,                                                    
               DIA2,                                                    
               DIA3,                                                    
               MES1,                                                    
               MES2,                                                    
               MES3,                                                    
               ANO1,                                                    
               ANO2,                                                    
               ANO3,                                                    
               RESTO,                                                   
               Q1;                                                      
                                                                        
      POINTER  PTP,PTQ,PTR,PTS;                                         
      BOOLEAN  RESULT,ERRO,DIAUTIL,ACABOU;                              
      TRUTHSET   DIGITO  ("0123456789");                                
                                                                        
      PROCEDURE  VALIDATA;                                              
      BEGIN                                                             
          RESULT:=TRUE;                                                 
          PTQ:=DATAV;                                                   
          PTP:=AREAA;                                                   
          SCAN  PTQ  FOR  Q1:8  WHILE  IN  DIGITO;                      
          Q1:=8  -  Q1;                                                 
          IF     Q1     EQL   8   THEN                                  
             BEGIN                                                      
             ANOV:=INTEGER (PTQ,4);                                     
             MESV:=INTEGER (PTQ  +  4,2);                               
             DIAV:=INTEGER (PTQ  +  6,2);                               
             IF    MESV     LSS    1   OR                               
                   MESV     GTR    12  OR                               
                   DIAV     LSS    1   THEN                             
                   RESULT:=FALSE                                        
             ELSE                                                       
                BEGIN                                                   
                    IF   (DIAV   GTR  DIAT[MESV]  AND                   
                          MESV   NEQ        2) THEN                     
                          RESULT:=FALSE                                 
                    ELSE                                                
                       IF  MESV   EQL        2   THEN                   
                          BEGIN                                         
                              IF  DIAV  GTR  DIAT[MESV]  THEN           
                                BEGIN                                   
                                    RESTO:=ANOV  MOD  4;                
                                    IF   RESTO    NEQ   0  OR           
                                        (RESTO   EQL   0  AND           
                                         DIAV     NEQ   29)   THEN      
                                         RESULT:=FALSE;                 
                                END                                     
                          END                                           
                END                                                     
             END                                                        
      ELSE                                                              
         RESULT:=FALSE;                                                 
         PTR:=CONS;                                                     
         IF    NOT  RESULT  THEN                                        
               REPLACE  PTR   BY  "F"                                   
         ELSE                                                           
            REPLACE  PTR  BY  "C";                                      
      END;                                                              
                                                                        
 BEGIN                                                                  
     LABEL  SAIDA,RESP;                                                 
     PTP:=AREAA[8];                                                     
     PTQ:=DATAV;                                                        
     REPLACE  PTQ  BY  PTP:PTP  FOR  8;                                 
     ANOV:=ANO1:=INTEGER (PTQ,4);                                       
     MESV:=MES1:=INTEGER (PTQ + 4,2);                                   
     DIAV:=DIA1:=INTEGER (PTQ + 6,2);                                   
     SCAN  PTQ  FOR  Q1:8  WHILE  IN  DIGITO;                           
     Q1:=8  -  Q1;                                                      
     IF     Q1     EQL   8   THEN                                       
        BEGIN                                                           
            IF  MES1  GTR      11     OR                                
                DIA1  GTR      31     OR                                
                ANO1  GTR      ANOV   THEN                              
                BEGIN                                                   
                    PTR:=CONS;                                          
                    REPLACE  PTR  BY  "E";                              
                    GO    TO    SAIDA;                                  
                END;                                                    
        END;                                                            
     PTP:=AREAA;                                                        
     PTQ:=DATAV;                                                        
     REPLACE  PTQ  BY  PTP:PTP  FOR  8;                                 
     ANOV:=INTEGER (PTQ,4);                                             
     MESV:=INTEGER (PTQ + 4,2);                                         
     DIAV:=INTEGER (PTQ + 6,2);                                         
     VALIDATA;                                                          
     IF     NOT   RESULT    THEN                                        
        BEGIN                                                           
            PTR:=CONS;                                                  
            REPLACE  PTR  BY  "E";                                      
            GO    TO    SAIDA;                                          
        END;                                                            
     ANO3:=ANOV  -  ANO1;                                               
     IF      MESV   GTR   MES1     THEN                                 
             MES3:=MESV   -   MES1                                      
     ELSE                                                               
        BEGIN                                                           
            ANO3:=ANO3   -   1;                                         
            MES3:=MESV   +   12;                                        
            MES3:=MES3   -   MES1;                                      
        END;                                                            
     IF      DIA1   EQL   0        THEN                                 
        BEGIN                                                           
            DIA3:=DIAV;                                                 
            IF     DIA3     GTR  DIAT[MES3]   THEN                      
                   DIA3:=DIAT[MES3];                                    
                   RESTO:=ANO3   MOD  4;                                
            IF     RESTO   EQL  0    THEN                               
                   DIA3:=DIA3   +    1;                                 
                   GO     TO    RESP;                                   
        END;                                                            
        IF   DIA1   GTR   DIAT[MES3]    THEN                            
             IF   MES3    NEQ   2             THEN                      
                  BEGIN                                                 
                      PTR:=CONS;                                        
                      REPLACE  PTR  BY  "E";                            
                      GO    TO    SAIDA;                                
                  END                                                   
             ELSE                                                       
                BEGIN                                                   
                    RESTO:=ANO3   MOD   4;                              
                    IF  RESTO   EQL   0     THEN                        
                        BEGIN                                           
                            IF   DIA1    GEQ   29    THEN               
                                 BEGIN                                  
                                     PTR:=CONS;                         
                                     REPLACE  PTR  BY  "E";             
                                     GO    TO    SAIDA;                 
                                 END;                                   
                        END;                                            
                END;                                                    
     IF   DIAV   EQL   DIAT[MESV]    THEN                               
          BEGIN                                                         
              DIAV:=DIAT[MES3];                                         
              RESTO:=ANO3   MOD  4;                                     
              IF   RESTO   EQL  0    THEN                               
                   DIAV:=DIAV   +    1;                                 
          END;                                                          
     IF   DIAV   GTR   DIA1     THEN                                    
          DIA3:=DIAV   -   DIA1                                         
     ELSE                                                               
        BEGIN                                                           
            MES3:=MES3   -  1;                                          
            IF  MES3   EQL   0    THEN                                  
                BEGIN                                                   
                    ANO3:=ANO3  -   1;                                  
                    MES3:=12;                                           
                END;                                                    
            DIA3:=(DIAT[MES3]  +  DIAV)  -  DIA1;                       
            IF  MES3   EQL   2    THEN                                  
                BEGIN                                                   
                RESTO:=ANO3   MOD   4;                                  
                IF    RESTO   EQL   0    THEN                           
                      DIA3:=DIA3  +  1;                                 
                END;                                                    
        END;                                                            
     RESP:                                                              
     PTP:=AREAA[16];                                                    
     REPLACE    PTP:PTP   BY  ANO3  FOR  4  DIGITS;                     
     REPLACE    PTP:PTP   BY  MES3  FOR  2  DIGITS;                     
     REPLACE    PTP:PTP   BY  DIA3  FOR  2  DIGITS;                     
     PTQ:=CONS;                                                         
     REPLACE    PTQ       BY  "C";                                      
     SAIDA:                                                             
     END;                                                               
 END OF SUBDATA2;                                                       
                                                                        
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
 %                                                                   %  
 %                        LIBRARY     CALCDATA2                      %  
 %                                                                   %  
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
                                                                        
 PROCEDURE   CALCDATA2 (OPCONS,AREAA);                                  
 EBCDIC  ARRAY  OPCONS,AREAA[0];                                        
 BEGIN                                                                  
     FILE  IMP (KIND=PRINTER,MAXRECSIZE=132,BLOCKSIZE=132,UNITS=1);     
     EBCDIC  ARRAY   DATAV[1:6],                                        
                     DISP01[1:30],                                      
                     DATAV2[1:8];                                       
     BOOLEAN BRESTO29;  % OSM-08/10/99                                  
     %---------------------------------------------------------------%  
     %  ARRAY C = CONTEM A QUANTIDADE DE DIAS ACUMULADO NO ANO       %  
     %                                                               %  
     %  ARRAY F = CONTEM A QUANTIDADE DE DIAS DO MES (ANO NORMAL)    %  
     %                                                               %  
     %  ARRAY F1= CONTEM A QUANTIDADE DE DIAS DO MES (ANO BISSEXTO)  %  
     %                                                               %  
     %  ARRAY FER = CONTEM A DATA DOS FERIADOS MOVEIS DE 1983 ATE O  %  
     %              ANO 2012 (FERIADOS : CARNAVAL , SEXTA FEIRA DA   %  
     %                                   PAIXAO E CORPUS CHRISTUS)   %  
     %                                                               %  
     %  ARRAY CENTURY = FORNECE SE O DIA DA SEMANA EM QUE 1 DE       %  
     %                  JANEIRO CAIU NO SECULO DO ANO PROCURADO      %  
     %                                                               %  
     %  ARRAY LEAPYEAR = VERIFICA SE O ANO PROCURADO E BISSEXTO      %  
     %                                                               %  
     %---------------------------------------------------------------%  
                                                                        
     REAL VALUE ARRAY C  (0,  0, 31, 59, 90,120,151,                    
                            181,212,243,273,304,334);                   
                                                                        
     REAL VALUE ARRAY F1 (0,31,29,31,30,31,30,31,31,30,31,30,31);       
                                                                        
     REAL VALUE ARRAY F  (0,31,28,31,30,31,30,31,31,30,31,30,31);       
                                                                        
     REAL VALUE ARRAY FER(0,1502,0104,0206,0603,2004,2106, % 1983/1984  
                            1902,0504,0606,1102,2803,2905, % 1985/1986  
                            0303,1704,1806,1602,0104,0206, % 1987/1988  
                            0702,2403,2505,2702,1304,1406, % 1989/1990  
                            1202,2903,3005,0303,1704,1806, % 1991/1992  
                            2302,0904,1006,1502,0104,0206, % 1993/1994  
                            2802,1404,1506,2002,0504,0606, % 1995/1996  
                            1102,2803,2905,2402,1004,1106, % 1997/1998  
                            1602,0204,0306,0703,2104,2206, % 1999/2000  
                            2702,1304,1406,1202,2903,3005, % 2001/2002  
                            0403,1804,1906,2402,0904,1006, % 2003/2004  
                            0802,2503,2605,2802,1404,1506, % 2005/2006  
                            2002,0604,0706,0502,2103,2205, % 2007/2008  
                            2402,1004,1106,1602,0204,0306, % 2009/2010  
                            0803,2204,2306,2102,0604,0706, % 2011/2012  
                            1202,2903,3005,0403,1804,1906, % 2013/2014  
                            1702,0304,0406,0902,2503,2605, % 2015/2016  
                            2802,1404,1506,1302,3003,3105, % 2017/2018  
                            0503,1904,2006,2502,1004,1106, % 2019/2020  
                            1602,0204,0306,0103,1504,1606, % 2021/2022  
                            2102,0704,0806,1302,2903,3005, % 2023/2024  
                            0403,1804,1906,1702,0304,0406, % 2025/2026  
                            0902,2603,2705,2902,1404,1506, % 2027/2028  
                            1302,3003,3105,0503,1904,2006, % 2029/2030  
                            2502,1104,1206,1002,2603,2705, % 2031/2032  
                            0103,1504,1606,2102,0704,0806, % 2033/2034  
                            0602,2306,2405,2602,1104,1206);% 2035/2036  
                                                                        
                                                                        
                                                                        
     REAL  ARRAY  D[1:20];                                              
                                                                        
     INTEGER VALUE ARRAY CENTURY (6,4,2,0);                             
                                                                        
     BOOLEAN VALUE ARRAY LEAPYEAR (TRUE,24(TRUE),FALSE,24(TRUE),FALSE,  
                                        24(TRUE),FALSE,24(TRUE));       
                                                                        
     INTEGER  DIAV,  DIA1,  DIA2,  DIA3,   X,    Y,    Z,               
              MESV,  MES1,  MES2,  MES3,   R,   R1,   R2,               
              ANOV,  ANO1,  ANO2,  ANO3,  R3,   R4,   R6,               
                Q1, RESTO,   QTD,     N,   I,   I2,  JAN,               
                A1,    A2,    M2,    D1,  D2, DATE,   R8,               
                M1,     S,  ANOB,    AA;                                
                                                                        
     REAL     DATA1,  DATA3,  DIASAC,  AUXDATA;                         
                                                                        
     LABEL    FIM1;                                                     
                                                                        
     POINTER  PTP,    PTQ,    PTR,    PTS;                              
                                                                        
     BOOLEAN  RESULT, ERRO, DIAUTIL, ACABOU, ANOBI;                     
                                                                        
     EBCDIC ARRAY AREAAUX[00:29];                                       
                                                                        
     TRUTHSET DIGITO  ("0123456789");                                   
                                                                        
%  ARRAY                                                                
%    CALENDAR[0:365];      % DATE CONVERSION TABLE.                     
%                                                                       
%  DEFINE                                                               
%                                                                       
%        % CONDITIONAL BOOLEAN OPERATORS                                
%    CAND (A, B) = (IF (A) THEN (B)  ELSE FALSE) #,                     
%    COR  (A, B) = (IF (A) THEN TRUE ELSE (B)  ) #,                     
%    CIMP (A, B) = (IF (A) THEN (B)  ELSE TRUE ) #,                     
%    XOR  (A, B) = (NOT (A) EQV (B)) #,                                 
%                                                                       
%          % FIELDS IN THE CALENDAR TABLE.                              
%    CALMONTHF  =  [15: 8]#,  % MONTH NUMBER (1 RELATIVE).              
%    CALDAYF    =  [ 7: 8]#,  % DAY OF MONTH NUMBER (1 RELATIVE).       
%                                                                       
%    STARTYEAR = 1601 #;                                                
%                                                                       
%BOOLEAN PROCEDURE GETLEAPYEAR (YEAR);                                  
%  VALUE YEAR;                                                          
%  INTEGER YEAR;                                                        
%  BEGIN                                                                
%      %% Returns TRUE if the specified year is a leap year             
%      %% and FALSE otherwise.                                          
%  IF YEAR MOD 400 = 0 THEN                                             
%    GETLEAPYEAR := TRUE                                                
%  ELSE                                                                 
%  IF YEAR MOD 100 = 0 THEN                                             
%    GETLEAPYEAR := FALSE                                               
%  ELSE                                                                 
%  IF YEAR MOD 4 = 0 THEN                                               
%    GETLEAPYEAR := TRUE                                                
%  ELSE                                                                 
%    GETLEAPYEAR := FALSE;                                              
%  END GETLEAPYEAR;                                                     
%BOOLEAN PROCEDURE VERIFYDATE (MONTH, DAY, YEAR);                       
%  VALUE MONTH, DAY, YEAR;                                              
%  INTEGER MONTH, DAY, YEAR;                                            
%  BEGIN                                                                
%      %% Returns TRUE if the month/day/year combination is             
%      %% valid and FALSE otherwise.                                    
%  IF YEAR < STARTYEAR OR                                               
%     MONTH < 1 OR                                                      
%     MONTH > 12 THEN                                                   
%    VERIFYDATE := FALSE                                                
%  ELSE                                                                 
%  IF DAY < 1 OR                                                        
%     DAY > CASE MONTH OF (0, 31, 28+REAL(GETLEAPYEAR(YEAR)), 31,       
%                          30, 31, 30, 31, 31, 30, 31, 30, 31) THEN     
%    VERIFYDATE := FALSE                                                
%  ELSE                                                                 
%    VERIFYDATE := TRUE;                                                
%  END VERIFYDATE;                                                      
%INTEGER PROCEDURE DATETODAYCOUNT (MONTH, DAY, YEAR);                   
%  VALUE MONTH, DAY, YEAR;                                              
%  INTEGER MONTH, DAY, YEAR;                                            
%  BEGIN                                                                
%      %% Converts the specified month, day, and year                   
%      %% into an offset count from the STARTYEAR.                      
%  INTEGER                                                              
%    DOFFSET,            % Day count being calculated.                  
%    QUADCENTURY,        % Number of 400-year periods.                  
%    TEMPYEAR;                                                          
%  REAL                                                                 
%    MONTHSLOP;          % Days after 28 in each month.                 
%                                                                       
%  IF VERIFYDATE (MONTH, DAY, YEAR) THEN                                
%    BEGIN                                                              
%    QUADCENTURY := (YEAR - STARTYEAR) DIV 400;                         
%    TEMPYEAR := (YEAR - 1) MOD 400;                                    
%    CASE (TEMPYEAR DIV 100) OF                                         
%      BEGIN                                                            
%      DOFFSET := 0;      % Date is in the first century.               
%      DOFFSET := 36524;  % Date is in the second century.              
%      DOFFSET := 73048;  % Date is in the third century.               
%      DOFFSET := 109572; % Date is in the fourth century.              
%      END CASE;                                                        
%    MONTHSLOP := 4"373773737070" &                                     
%                 REAL(GETLEAPYEAR(YEAR))[8:1];                         
%    DOFFSET := * +      % Century start.                               
%                        % Plus offset to year start.                   
%               INTEGERT((TEMPYEAR MOD 100) * 365.25) +                 
%                        % Plus offset to month start.                  
%               (28 * (MONTH-1)) +                                      
%               ONES(MONTHSLOP.[(MONTH*4)-1:MONTH*4]) +                 
%                        % Plus actual date offset.                     
%               DAY;                                                    
%    DATETODAYCOUNT :=                                                  
%      DOFFSET + (QUADCENTURY * 146097);                                
%    END                                                                
%  ELSE                                                                 
%    DATETODAYCOUNT := -1;                                              
%  END DATETODAYCOUNT;                                                  
%INTEGER PROCEDURE DAYCOUNTTODATE                                       
%    (DAYCOUNT, MONTH, DAY, YEAR);                                      
%  VALUE DAYCOUNT;                                                      
%  INTEGER                                                              
%    DAYCOUNT,   % Input value.                                         
%    MONTH,      % Returned values.                                     
%    DAY,                                                               
%    YEAR;                                                              
%  BEGIN                                                                
%      %% Converts a day offset count to a month, day, and              
%      %% year value.  The procedure result is 0 if the                 
%      %% the DAYCOUNT is valid and -1 otherwise.                       
%  INTEGER                                                              
%    CENTFACTOR,         % Century factor (0, 1, 2, or 3).              
%    COFFSET,            % Offset within the century.                   
%    LEAPGROUPS,         % Which group of 4 years it is in.             
%    LEAPOFFSET,         % Day remainder within this leap group.        
%    QUADCENTURY,        % 400-year group for the year.                 
%    TEMPYEAR,           % Year the date falls on.                      
%    YOFFSET;            % Date within that year.                       
%                                                                       
%  IF DAYCOUNT < 1 THEN                                                 
%    DAYCOUNTTODATE := -1                                               
%  ELSE                                                                 
%    BEGIN                                                              
%    DAYCOUNT := * - 1;  % Make zero-relative.                          
%    QUADCENTURY := DAYCOUNT DIV 146097;                                
%    DAYCOUNT := DAYCOUNT MOD 146097;                                   
%                                                                       
%    IF DAYCOUNT = 146096 THEN                                          
%      BEGIN                                                            
%          % It's Dec 31 in the 400th year.                             
%      CENTFACTOR := 3;                                                 
%      COFFSET := 36524;                                                
%      END                                                              
%    ELSE                                                               
%      BEGIN                                                            
%      CENTFACTOR := DAYCOUNT DIV 36524;                                
%      COFFSET := DAYCOUNT MOD 36524;                                   
%      END;                                                             
%                                                                       
%    LEAPGROUPS := COFFSET DIV 1461; % Number of leap years past.       
%    LEAPOFFSET := COFFSET MOD 1461;                                    
%                                                                       
%    IF LEAPOFFSET = 1460 THEN                                          
%      BEGIN                                                            
%          % Last day of the 4th year.                                  
%      TEMPYEAR := 3;                                                   
%      YOFFSET := 365;                                                  
%      END                                                              
%    ELSE                                                               
%      BEGIN                                                            
%      TEMPYEAR := LEAPOFFSET DIV 365;                                  
%      YOFFSET := LEAPOFFSET MOD 365;                                   
%      END;                                                             
%                                                                       
%    YEAR := TEMPYEAR +                                                 
%            (LEAPGROUPS * 4) +                                         
%            (CENTFACTOR * 100) +                                       
%            (QUADCENTURY * 400) +                                      
%            STARTYEAR;                                                 
%                                                                       
%    IF CAND(NOT GETLEAPYEAR(YEAR),                                     
%            YOFFSET >= 59) THEN                                        
%      YOFFSET := * + 1;                                                
%    MONTH := CALENDAR[YOFFSET].CALMONTHF;                              
%    DAY := CALENDAR[YOFFSET].CALDAYF;                                  
%    DAYCOUNTTODATE := 0;                                               
%    END;                                                               
%  END DAYCOUNTTODATE;                                                  
                                                                        
     %---------------------------------------------------------------%  
     %               INICIO  DA PROCEDURE  ANOBISSEXTO               %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   ESTA PROCEDURE DEVOLVE PARA A ROTINA SE O ANO SOLICITADO    %  
     %   E UM ANO BISSEXTO.                                          %  
     %                                                               %  
     %---------------------------------------------------------------%  
                                                                        
     BOOLEAN  PROCEDURE  ANOBISSEXTO;                                   
                                                                        
     BEGIN                                                              
       EBCDIC ARRAY AREATRAB[0:7];                                      
       POINTER PTRAB;                                                   
       INTEGER AA;                                                      
                                                                        
       AA:=ANOB;                                                        
       IF (AA MOD 100) = 0 THEN                                         
          BEGIN                                                         
            IF (AA MOD 400) = 0 THEN                                    
               ANOBISSEXTO:=TRUE                                        
            ELSE                                                        
                ANOBISSEXTO:=FALSE                                      
          END                                                           
       ELSE                                                             
           IF (AA MOD 4) = 0 THEN                                       
              ANOBISSEXTO:=TRUE                                         
           ELSE                                                         
               ANOBISSEXTO:=FALSE                                       
     END; % DA PROCEDURE                                                
                                                                        
     %---------------------------------------------------------------%  
     %         INICIO  DA OP[]O ZERO      =      DATA DO DIA         %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   1  -  PARAMETRO                                             %  
     %         OP[]O  (2 BYTES)   =  00 (ZERO)                       %  
     %                                                               %  
     %   2  -  RETORNO                                               %  
     %         DATA DO DIA        =  DD/MM/AA                        %  
     %---------------------------------------------------------------%  
                                                                        
                                                                        
     PROCEDURE  DATADIA;                                                
     BEGIN                                                              
         PICTURE    ABC(N/9(2)I9(2)I9(2));                              
         PTP:=AREAA;                                                    
         AUXDATA:=TIME(15);                                             
         DATA3.[47:16]:=AUXDATA.[31:16];                                
         DATA3.[31:16]:=AUXDATA.[47:16];                                
         DATA3.[15:16]:=AUXDATA.[15:16];                                
         PTQ:=DATAV;                                                    
         REPLACE  PTQ      BY  DATA3   FOR  1  WORDS;                   
         REPLACE  PTP:PTP  BY  PTQ      WITH  ABC;                      
         PTR:=OPCONS[2];                                                
         REPLACE   PTR    BY  "C";                                      
     END;                                                               
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %             OP[]O   UM    =    VERIFICA A VALIDADE DE DATA    %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   1 - PARAMETROS                                              %  
     %       1.1  -  OPCAO (2 BYTES)  =  01;                         %  
     %       1.2  -  DATA             =  DDMMAA;                     %  
     %                                                               %  
     %   2 - RETORNO                                                 %  
     %       CONS (1 BYTE)  =  "C" (CERTO)  OU  "E"  (ERRADO);       %  
     %---------------------------------------------------------------%  
                                                                        
     PROCEDURE  VALIDATA;                                               
     BEGIN                                                              
         RESULT:=TRUE;                                                  
         PTQ:=DATAV;                                                    
         PTP:=AREAA;                                                    
         SCAN  PTQ  FOR  Q1:6  WHILE  IN  DIGITO;                       
         Q1:=6  -  Q1;                                                  
         IF   Q1     EQL   6   THEN                                     
          BEGIN                                                         
              DIAV:=INTEGER (PTQ,2);                                    
              MESV:=INTEGER (PTQ  +  2,2);                              
              ANOV:=INTEGER (PTQ  +  4,2);                              
              IF   MESV     LSS    1   OR                               
                   MESV     GTR    12  OR                               
                   DIAV     LSS    1   THEN                             
                   RESULT:=FALSE                                        
              ELSE                                                      
               BEGIN                                                    
                   IF   (DIAV   GTR  F[MESV]  AND                       
                         MESV   NEQ        2) THEN                      
                         RESULT:=FALSE                                  
                   ELSE                                                 
                   IF  MESV   EQL        2   THEN                       
                    BEGIN                                               
                        IF  DIAV  GTR  F[MESV]  THEN                    
                         BEGIN                                          
                             ANOB:=ANOV;                                
                             IF  NOT  ANOBISSEXTO  OR                   
                                 (ANOBISSEXTO       AND                 
                                   DIAV NEQ 29)    THEN                 
                                       RESULT:=FALSE;                   
                                                                        
                         END                                            
                    END                                                 
               END                                                      
          END                                                           
          ELSE                                                          
          RESULT:=FALSE;                                                
          PTR:=OPCONS[2];                                               
          IF   NOT  RESULT  THEN                                        
               REPLACE  PTR   BY  "E"                                   
          ELSE                                                          
               REPLACE  PTR  BY  "C";                                   
     END;                                                               
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %        OP[]O  02 (DOIS)   =   VERIFICA O DIA DA SEMANA        %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   1 - PARAMETROS                                              %  
     %       1.1 - OPCAO (2 BYTES)  =  2;                            %  
     %       1.2 - DATA            =  DDMMAA;                        %  
     %       1.3 - FERIADOS MOVEIS =  DDMM,DDMM,....,ETC.;           %  
     %                                                               %  
     %   2 - RETORNO                                                 %  
     %       2.1 - CONS (1 BYTE) = "C" (CERTO)  OU  "E" (ERRADO);    %  
     %       2.2 - DIA DA SEMANA = DIA UTIL, SABADO , DOMINGO OU     %  
     %                             FERIADO                           %  
     %---------------------------------------------------------------%  
                                                                        
     PROCEDURE  DIASEMANA;                                              
     BEGIN                                                              
         LABEL  SAISEM;                                                 
         FILL  D[*]  WITH  0101,2104,0105,0709,1210,0211,1511,2512;     
         PTS:=AREAA; PTQ:=DATAV;                                        
         PTR:=AREAA;                                                    
         REPLACE  PTQ  BY  PTS  FOR  6;                                 
         DIAV:=INTEGER (PTQ,2);                                         
         DIA1:=INTEGER (PTQ,2);                                         
         MESV:=INTEGER (PTQ + 2,2);                                     
         MES1:=INTEGER (PTQ + 2,2);                                     
         ANOV:=INTEGER (PTQ + 4,2);                                     
         ANO1:=INTEGER (PTQ + 4,2);                                     
         ERRO:=FALSE;                                                   
         VALIDATA;                                                      
         IF   RESULT    THEN                                            
          BEGIN                                                         
              ERRO:=FALSE;                                              
              PTS:=PTS+2;                                               
              S:=8;                                                     
              PTR:=AREAA[7];                                            
              SCAN  PTR  FOR  Q1:52  WHILE IN DIGITO;                   
              Q1:=52  -  Q1  + 1;                                       
              X:=INTEGERT (Q1  /  4);                                   
              IF   X   GTR   10  THEN                                   
              X:=0;                                                     
              THRU   X   DO                                             
              BEGIN                                                     
                  PTS:=PTS + 4;                                         
                  AUXDATA:=INTEGER  (PTS,4);                            
                  REPLACE  PTQ  BY  PTS  FOR  4;                        
                  VALIDATA;                                             
                  IF  RESULT    THEN                                    
                  BEGIN                                                 
                      S:=S + 1;                                         
                      D[S]:=AUXDATA;                                    
                  END                                                   
                  ELSE                                                  
                  ERRO:=TRUE;                                           
              END                                                       
          END                                                           
         ELSE                                                           
            ERRO:=TRUE;                                                 
                                                                        
         PTP:=AREAA[06];                                                
         X:=X  *  4;                                                    
         PTP:=*  +  X;                                                  
         IF   (ERRO     OR  NOT  RESULT)  THEN                          
              BEGIN                                                     
                  REPLACE   PTP      BY  "INVALIDO";                    
                  GO        TO       SAISEM;                            
              END;                                                      
         ANOB:=ANO1;                                                    
         IF   ANOBISSEXTO  THEN                                         
              IF  MES1  GTR   2   THEN                                  
              DIA1:=DIA1 + 1;                                           
                                                                        
         X:=(INTEGERT ((ANO1 - 1) * 365)) + (INTEGERT((ANO1 - 1) / 4)); 
         Y:=X + (C[MES1] + DIA1);                                       
         R:=Y  MOD  7;                                                  
         IF   R         EQL       5       THEN                          
              REPLACE   PTP       BY      "SABADO "                     
         ELSE                                                           
            IF  R       EQL       6       THEN                          
                REPLACE   PTP       BY    "DOMINGO"                     
            ELSE                                                        
               BEGIN                                                    
                   DIAUTIL:=TRUE;                                       
                   PTQ:=AREAA;                                          
                   AUXDATA:=INTEGER (PTQ,4);                            
                   I:=0;                                                
                   DO                                                   
                        BEGIN                                           
                            I:=I + 1;                                   
                            IF  AUXDATA   EQL       D[I]      THEN      
                                BEGIN                                   
                                    DIAUTIL:=FALSE;                     
                                    I:=99;                              
                                END                                     
                        END                                             
                   UNTIL   I    GTR        S;                           
                   IF    DIAUTIL     THEN                               
                         REPLACE  PTP       BY       "DIA UTIL"         
                   ELSE                                                 
                      REPLACE  PTP       BY       "FERIADO";            
               END;                                                     
         SAISEM:                                                        
     END;                                                               
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %            OP[]O 03 (TRES)   =   DIFERENCA DE DATAS           %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %  1 - PARAMETROS                                               %  
     %      1.1 - OPCAO (2 BYTES)  =  03;                            %  
     %      1.2 - DATA INFERIOR    =  DDMMAA;                        %  
     %      1.3 - DATA SUPERIOR    =  DDMMAA;                        %  
     %                                                               %  
     %  2 - RETORNO                                                  %  
     %      2.1 - DIFERENCA EM NUMEROS DE DIAS;                      %  
     %      2.2 - DIFERENCA EM ANOS, MESES E DIAS;                   %  
     %---------------------------------------------------------------%  
     PROCEDURE   DIFDATA2;FORWARD;                                      
     PROCEDURE   DIFDATA;                                               
      BEGIN                                                             
       IF AREAA[04] GEQ 48"F0F0" AND AREAA[04] LSS 48"F3F1" % 2000-2030 
        THEN                                                            
         BEGIN                                                          
          REPLACE AREAAUX[0] BY AREAA[0] FOR 24;                        
          REPLACE AREAA[04] BY "20" FOR 2;                              
          REPLACE AREAA[06] BY AREAAUX[04] FOR 6;                       
          REPLACE AREAA[12] BY "20" FOR 2;                              
          REPLACE AREAA[14] BY AREAAUX[10] FOR 2;                       
          RESIZE(AREAA,32,RETAIN);                                      
          DIFDATA2;                                                     
          REPLACE AREAA[00] BY AREAAUX[0] FOR 12;                       
          REPLACE AREAA[12] BY AREAA[18] FOR 6;                         
          REPLACE AREAA[18] BY AREAA[26] FOR 2;                         
          REPLACE AREAA[20] BY AREAA[28] FOR 2;                         
          REPLACE AREAA[22] BY AREAA[30] FOR 2;                         
          RESIZE(AREAA,24,RETAIN);                                      
         END                                                            
        ELSE                                                            
         IF AREAA[10] GEQ 48"F0F0" AND AREAA[10] LSS 48"F3F1"           
          THEN                                                          
           BEGIN                                                        
            REPLACE AREAAUX[0] BY AREAA[0] FOR 24;                      
            REPLACE AREAA[04] BY "19" FOR 2;                            
            REPLACE AREAA[06] BY AREAAUX[04] FOR 6;                     
            REPLACE AREAA[12] BY "20" FOR 2;                            
            REPLACE AREAA[14] BY AREAAUX[10] FOR 2;                     
            RESIZE(AREAA,32,RETAIN);                                    
            DIFDATA2;                                                   
            REPLACE AREAA[00] BY AREAAUX[0] FOR 12;                     
            REPLACE AREAA[12] BY AREAA[18] FOR 6;                       
            REPLACE AREAA[18] BY AREAA[26] FOR 2;                       
            REPLACE AREAA[20] BY AREAA[28] FOR 2;                       
            REPLACE AREAA[22] BY AREAA[30] FOR 2;                       
            RESIZE(AREAA,24,RETAIN);                                    
           END                                                          
          ELSE                                                          
           BEGIN                                                        
            LABEL  SAIDA,CALCMES;                                       
            PTP:=AREAA;                                                 
            PTQ:=DATAV;                                                 
            REPLACE  PTQ  BY  PTP:PTP  FOR  6;                          
            DIAV:=INTEGER (PTQ,2);                                      
            MESV:=INTEGER (PTQ + 2,2);                                  
            ANOV:=INTEGER (PTQ + 4,2);                                  
            VALIDATA;                                                   
            IF   NOT   RESULT   THEN                                    
              BEGIN                                                     
                  PTR:=OPCONS[2];                                       
                  REPLACE  PTR  BY  "E";                                
                  GO    TO    SAIDA;                                    
              END;                                                      
                                                                        
            PTP:=AREAA[6];                                              
            PTQ:=DATAV;                                                 
            REPLACE  PTQ  BY  PTP  FOR  6;                              
            DIAV:=INTEGER (PTQ,2);                                      
            MESV:=INTEGER (PTQ + 2,2);                                  
            ANOV:=INTEGER (PTQ + 4,2);                                  
            VALIDATA;                                                   
            IF   NOT   RESULT   THEN                                    
              BEGIN                                                     
                  PTR:=OPCONS[2];                                       
                  REPLACE  PTR  BY  "E";                                
                  GO    TO    SAIDA;                                    
              END;                                                      
                                                                        
            PTP:=AREAA;                                                 
            D1:=DIA1:=INTEGER (PTP,2);                                  
            M1:=R8:=Z:=MES1:=INTEGER (PTP  + 2,2);                      
            A1:=R6:=ANO1:=INTEGER (PTP + 4,2);                          
            D2:=DIA2:=INTEGER (PTP + 6,2);                              
            M2:=MES2:=INTEGER (PTP + 8,2);                              
            A2:=ANO2:=INTEGER (PTP + 10,2);                             
                                                                        
            IF   ANO1   GTR    ANO2    OR                               
             (ANO1   EQL    ANO2    AND                                 
              MES1   GTR    MES2)   OR                                  
             (ANO1   EQL    ANO2    AND                                 
              MES1   EQL    MES2    AND                                 
              DIA1   GTR    DIA2)   THEN                                
              BEGIN                                                     
                  PTR:=OPCONS[2];                                       
                  REPLACE  PTR  BY  "E";                                
                  GO    TO    SAIDA;                                    
              END;                                                      
                                                                        
            IF   ANO2   EQL    ANO1    AND                              
              MES2  EQL  MES1       AND                                 
              DIA2  EQL  DIA1       THEN                                
              BEGIN                                                     
                  DIASAC:=0;                                            
                  R:=0;                                                 
                  MES1:=0;                                              
                  DIA1:=0;                                              
                  GO     TO   SAIDA;                                    
              END;                                                      
                                                                        
     %---------------------------------------------------------------%  
     %             CALCULO   DO   NUMERO    DE   ANOS                %  
     %---------------------------------------------------------------%  
                                                                        
            R:=0;                                                       
            IF   ANO2   GTR   ANO1   THEN                               
              BEGIN                                                     
                  R:=ANO2  -  ANO1;                                     
                  IF   R   EQL   1   THEN                               
                       BEGIN                                            
                           IF   MES2   GTR   MES1   OR                  
                               (MES2   EQL   MES1   AND                 
                                DIA2   GEQ   DIA1)  THEN                
                                GO     TO    CALCMES                    
                           ELSE                                         
                              R:=0;                                     
                       END;                                             
              END;                                                      
           R6:=R;                                                       
                                                                        
     %---------------------------------------------------------------%  
     %             CALCULO   DO   NUMERO    DE   MESES               %  
     %---------------------------------------------------------------%  
                                                                        
            CALCMES:                                                    
            R2:=0;                                                      
                                                                        
            IF   MES2   GTR   MES1   THEN                               
              BEGIN                                                     
                  R2:=MES2  -  MES1;                                    
                  IF   DIA2   LSS   DIA1   THEN                         
                       R2:=R2  -  1;                                    
              END                                                       
            ELSE                                                        
             IF  MES1   GTR   MES2   THEN                               
                 BEGIN                                                  
                     R6:=R:=ANO2  -  (ANO1  +  1);                      
                     R2:=(12  -  MES1)  +  MES2;                        
                     IF   DIA2   LSS   DIA1   THEN                      
                          R2:=R2  -  1;                                 
                 END;                                                   
                                                                        
            MES1:=R2;                                                   
                                                                        
     %---------------------------------------------------------------%  
     %             CALCULO   DO   NUMERO    DE   DIAS                %  
     %---------------------------------------------------------------%  
                                                                        
            R6:=R4:=DIASAC:=0;                                          
                                                                        
            IF   DIA2   GTR   DIA1   THEN                               
              DIASAC:=DIA2  -  DIA1                                     
            ELSE                                                        
            IF   DIA1   GTR   DIA2   THEN                               
                 BEGIN                                                  
                     IF   Z   EQL   MES2   THEN                         
                          BEGIN                                         
                              IF    Z    EQL   1   THEN                 
                                    I2:=12                              
                               ELSE                                     
                                  I2:=Z  -  1;                          
                               DIASAC:=(F[I2]  -  DIA1)  +  DIA2;       
                               IF    I2   EQL   2   THEN                
                                     BEGIN                              
                                         ANOB:=ANO2;                    
                                         IF  ANOBISSEXTO    THEN        
                                              DIASAC:=*  +  1;          
                                     END;                               
                          END                                           
                     ELSE                                               
                       BEGIN                                            
                         ANOB:=ANO1;                                    
                         IF ANOBISSEXTO THEN                            
                            DIASAC:=(F1[Z] - DIA1) + DIA2               
                         ELSE                                           
                            DIASAC:=(F[Z]  -  DIA1)  +  DIA2;           
                       END;                                             
                                                                        
                  IF   (Z  +  1)  GTR   MES2  THEN                      
                      BEGIN                                             
                      R:=R6:=ANO2  -  (ANO1  +  1);                     
                      MES1:=(MES2  +  12)  -  (Z + 1);                  
                      END                                               
                  ELSE                                                  
                      MES1:=MES2  -  (Z  +  1);                         
                 END;                                                   
            R4:=DIASAC;                                                 
                                                                        
     %---------------------------------------------------------------%  
     %     CALCULO DOS DIAS ACUMULADOS ENTRE AS DATAS FORNECIDA      %  
     %---------------------------------------------------------------%  
                                                                        
            ANOB:=ANO1;                                                 
            IF ANOBISSEXTO  THEN                                        
               BEGIN                                                    
                IF  M1    GTR  2   THEN                                 
                   A1:=365                                              
                 ELSE                                                   
                   A1:=366;                                             
               END                                                      
            ELSE                                                        
               A1:=365;                                                 
                                                                        
            ANOB:=ANO2;                                                 
            IF ANOBISSEXTO THEN                                         
               A2:=366                                                  
             ELSE                                                       
               A2:=365;                                                 
                                                                        
            IF   (ANO2 - ANO1) EQL   0    THEN                          
              BEGIN                                                     
               DIASAC:=0;                                               
               IF M2 GTR 2 THEN                                         
               A2:=365;                                                 
               DIASAC:=(A1 - C[M1] - DIA1);                             
               DIASAC:=(DIASAC - (A2 - (C[M2] + DIA2 )));               
                                                                        
               GO TO SAIDA;                                             
              END;                                                      
                                                                        
            IF (ANO2 - ANO1)   EQL   1    THEN                          
               BEGIN                                                    
                DIASAC:=0;                                              
                DIASAC:=((A1 - C[M1] - DIA1) + (DIA2 + C[M2]));         
                                                                        
                IF A2 EQL 366 AND M2 GTR 2 THEN                         
                  DIASAC:= * + 1;                                       
                GO TO SAIDA;                                            
               END;                                                     
                                                                        
            IF (ANO2 - ANO1)   GTR   1    THEN                          
               BEGIN                                                    
                DIASAC:=0;                                              
                R8:=(ANO2  - ANO1) - 1;                                 
                DIASAC:=((A1 - C[M1] - DIA1) + (DIA2 + C[M2]));         
                                                                        
                IF  A2  EQL  366 AND M2 GTR 2 THEN                      
                  DIASAC:= * + 1;                                       
                                                                        
                THRU   R8    DO                                         
                  BEGIN                                                 
                   ANO1:= * + 1;                                        
                   ANOB:=ANO1;                                          
                   IF ANOBISSEXTO THEN                                  
                     DIASAC:= * + 366                                   
                   ELSE                                                 
                     DIASAC:= * + 365;                                  
                  END;                                                  
               END;                                                     
            SAIDA:                                                      
            PTR:=DISP01;                                                
            REPLACE  PTR  BY  "PROC DIF DE DATAS";                      
            PTP:=AREAA[12];                                             
            REPLACE  PTP:PTP  BY  DIASAC  FOR  6  DIGITS;               
            REPLACE  PTP:PTP  BY  R       FOR  2  DIGITS;               
            REPLACE  PTP:PTP  BY  MES1    FOR  2  DIGITS;               
            REPLACE  PTP:PTP  BY  R4      FOR  2  DIGITS;               
           END;                                                         
      END;                                                              
                                                                        
     %---------------------------------------------------------------%  
     %            OP[]O 04 (QUATRO)  =  VERIFICA DATA FUTURA         %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %  1 - PARAMETROS                                               %  
     %      1.1 - OPCAO (2 BYTES)             =  04;                 %  
     %      1.2 - DATA                        =  DDMMAA;             %  
     %      1.3 - QUANTIDADE DE DIAS (1 WORD) =  NNNNNN;             %  
     %                                                               %  
     %  2 - RETORNO                                                  %  
     %      1.1 - CONS (1 BYTE)   = "C" (CERTO) OU "E" (ERRADO);     %  
     %      1.2 - DATA FUTURA     = DDMMAA;                          %  
     %---------------------------------------------------------------%  
                                                                        
     PROCEDURE   DFUTURA;                                               
     BEGIN                                                              
         LABEL  SAIFUT;                                                 
         PTS:=AREAA;                                                    
         PTQ:=DATAV;                                                    
         REPLACE  PTQ  BY  PTS:PTS  FOR  6;                             
         VALIDATA;                                                      
         IF      NOT  RESULT   THEN                                     
                 BEGIN                                                  
                     PTR:=OPCONS[2];                                    
                     REPLACE  PTR  BY  "E";                             
                     GO   TO       SAIFUT;                              
                 END;                                                   
         SCAN  PTS  FOR  Q1:6  WHILE  IN  DIGITO;                       
         Q1:=6  -  Q1;                                                  
         IF      Q1    NEQ    6   THEN                                  
                 BEGIN                                                  
                     PTR:=OPCONS[2];                                    
                     REPLACE  PTR  BY  "E";                             
                     GO    TO      SAIFUT;                              
                 END;                                                   
         PTP:=AREAA;                                                    
         DIA1:=INTEGER (PTQ,2);                                         
         MES1:=INTEGER (PTQ + 2,2);                                     
         ANO1:=INTEGER (PTQ + 4,2);                                     
         MES2:=MES1;                                                    
         ANO2:=ANO1;                                                    
         QTD:=INTEGER(PTP + 6,6);                                       
         R2:=0;                                                         
         R1:=QTD   +  DIA1;                                             
         DO                                                             
           BEGIN                                                        
               IF MES1 EQL 2 THEN                                       
               BEGIN                                                    
                   ANOB:=ANO2;                                          
                   IF ANOBISSEXTO THEN                                  
                   BEGIN                                                
                       IF R1 GTR F1[MES1] THEN                          
                       BEGIN                                            
                           MES2:=*  +  1;                               
                           IF MES2 GTR 12  THEN                         
                           BEGIN                                        
                               ANO2:=ANO2  +  1;                        
                               MES2:=1;                                 
                           END;                                         
                           DIA2:=F1[MES2];                              
                           R1:=R1  -  F1[MES1];                         
                       END                                              
                       ELSE                                             
                         BEGIN                                          
                             DIA2:=R1;                                  
                             R1:=  0 ;                                  
                         END                                            
                   END                                                  
                      ELSE                                              
                      BEGIN                                             
                         IF R1 GTR F[MES1]  THEN                        
                         BEGIN                                          
                            MES2:=*  +  1;                              
                            IF MES2 GTR 12  THEN                        
                            BEGIN                                       
                                ANO2:=ANO2  +  1;                       
                                MES2:=1;                                
                            END;                                        
                            DIA2:=F[MES2];                              
                            R1:=R1  -  F[MES1];                         
                         END                                            
                         ELSE                                           
                            BEGIN                                       
                                DIA2:=R1;                               
                                R1:=0;                                  
                            END;                                        
                      END                                               
                   END                                                  
                   ELSE                                                 
        BEGIN                                                           
         IF R1 GTR F[MES1]  THEN                                        
          BEGIN                                                         
           MES2:=*  +  1;                                               
           IF MES2 GTR 12  THEN                                         
            BEGIN                                                       
             ANO2:=ANO2  +  1;                                          
             MES2:=1;                                                   
            END;                                                        
           DIA2:=F[MES2];                                               
           R1:=R1  -  F[MES1];                                          
          END                                                           
                           ELSE                                         
          BEGIN                                                         
           DIA2:=R1;                                                    
           R1:=0;                                                       
          END                                                           
        END;                                                            
       IF MES2 GTR 12  THEN                                             
        BEGIN                                                           
         ANO2:=ANO2  +  1;                                              
         MES2:=1;                                                       
        END;                                                            
      MES1 := MES2;                                                     
     END                                                                
     UNTIL  R1  LEQ  R2;                                                
     PTP:=AREAA[12];                                                    
     REPLACE PTP:PTP BY DIA2 FOR 2 DIGITS;                              
     REPLACE PTP:PTP BY MES2 FOR 2 DIGITS;                              
     REPLACE PTP:PTP BY ANO2 FOR 2 DIGITS;                              
    SAIFUT:                                                             
  END;                                                                  
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %            OP[]O 05 (CINCO)  =  VALIDADE DE DATAS             %  
     %                                 ANO COM 4 DIGITOS             %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   1 - PARAMETROS                                              %  
     %       1.1  -  OPCAO (2 BYTES)  = 05;                          %  
     %       1.2  -  DATA             = DDMMAAAA;                    %  
     %                                                               %  
     %   2 - RETORNO                                                 %  
     %       CONS (1 BYTE)  =  "C" (CERTO)  OU  "E"  (ERRADO);       %  
     %---------------------------------------------------------------%  
                                                                        
    PROCEDURE  VALIDATA2;                                               
    BEGIN                                                               
    RESULT:=TRUE;                                                       
    PTQ:=DATAV2;                                                        
    PTP:=AREAA;                                                         
    SCAN  PTQ  FOR  Q1:8  WHILE  IN  DIGITO;                            
    Q1:=8  -  Q1;                                                       
    IF     Q1     EQL   8   THEN                                        
           BEGIN                                                        
           DIAV:=INTEGER (PTQ,2);                                       
           MESV:=INTEGER (PTQ  +  2,2);                                 
           ANOV:=INTEGER (PTQ  +  4,4);                                 
           IF    MESV     LSS    1   OR                                 
                 MESV     GTR    12  OR                                 
                 DIAV     LSS    1   THEN                               
                 RESULT:=FALSE                                          
            ELSE                                                        
            BEGIN                                                       
            IF   (DIAV   GTR  F[MESV]  AND                              
                  MESV   NEQ        2) THEN                             
                  RESULT:=FALSE                                         
            ELSE                                                        
              IF  MESV   EQL        2   THEN                            
                BEGIN                                                   
                IF  DIAV  GTR  F[MESV]  THEN                            
                  BEGIN                                                 
                  ANOB:=ANOV;                                           
                  IF NOT ANOBISSEXTO  OR                                
                       (ANOBISSEXTO  AND                                
                       DIAV     NEQ   29)   THEN                        
                       RESULT:=FALSE;                                   
                   END                                                  
                END                                                     
             END                                                        
           END                                                          
    ELSE                                                                
         RESULT:=FALSE;                                                 
    PTR:=OPCONS[2];                                                     
    IF    NOT  RESULT  THEN                                             
          REPLACE  PTR   BY  "E"                                        
    ELSE                                                                
          REPLACE  PTR  BY  "C";                                        
       END;                                                             
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %            OP[]O 06 (SEIS)   =   DIFERENCA DE DATAS           %  
     %                                  ANO COM 4 DIGITOS            %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %  1 - PARAMETROS                                               %  
     %      1.1 - OPCAO (2 BYTES)  =  06;                            %  
     %      1.2 - DATA INFERIOR    =  DDMMAAAA;                      %  
     %      1.3 - DATA SUPERIOR    =  DDMMAAAA;                      %  
     %                                                               %  
     %  2 - RETORNO                                                  %  
     %      2.1 - DIFERENCA EM NUMEROS DE DIAS;                      %  
     %      2.2 - DIFERENCA EM ANOS, MESES E DIAS;                   %  
     %---------------------------------------------------------------%  
                                                                        
    PROCEDURE   DIFDATA2;                                               
    BEGIN                                                               
    LABEL  SAIDA2,CALCMES2;                                             
    PTP:=AREAA;                                                         
    PTQ:=DATAV2;                                                        
    REPLACE  PTQ  BY  PTP:PTP  FOR  8;                                  
    DIAV:=INTEGER (PTQ,2);                                              
    MESV:=INTEGER (PTQ + 2,2);                                          
    ANOV:=INTEGER (PTQ + 4,4);                                          
    VALIDATA2;                                                          
    IF     NOT   RESULT    THEN                                         
           BEGIN                                                        
           PTR:=OPCONS[2];                                              
           REPLACE  PTR  BY  "E";                                       
           GO    TO    SAIDA2;                                          
           END;                                                         
    PTP:=AREAA[8];                                                      
    PTQ:=DATAV2;                                                        
    REPLACE  PTQ  BY  PTP  FOR  8;                                      
    DIAV:=INTEGER (PTQ,2);                                              
    MESV:=INTEGER (PTQ + 2,2);                                          
    ANOV:=INTEGER (PTQ + 4,4);                                          
    VALIDATA2;                                                          
    IF     NOT   RESULT   THEN                                          
           BEGIN                                                        
           PTR:=OPCONS[2];                                              
           REPLACE  PTR  BY  "E";                                       
           GO    TO    SAIDA2;                                          
           END;                                                         
    PTP:=AREAA;                                                         
    D1:=DIA1:=INTEGER (PTP,2);                                          
    M1:=Z:=MES1:=INTEGER (PTP  + 2,2);                                  
    A1:=R6:=ANO1:=INTEGER (PTP + 4,4);                                  
    D2:=DIA2:=INTEGER (PTP + 8,2);                                      
    M2:=MES2:=INTEGER (PTP + 10,2);                                     
    A2:=ANO2:=INTEGER (PTP + 12,4);                                     
    IF     ANO1     GTR   ANO2    OR                                    
           (ANO1    EQL   ANO2    AND                                   
            MES1    GTR   MES2)   OR                                    
           (ANO1    EQL   ANO2    AND                                   
            MES1    EQL   MES2    AND                                   
            DIA1    GTR   DIA2)   THEN                                  
           BEGIN                                                        
           PTR:=OPCONS[2];                                              
           REPLACE  PTR  BY  "E";                                       
           GO    TO    SAIDA2;                                          
           END;                                                         
    IF     ANO2  EQL  ANO1   AND                                        
           MES2  EQL  MES1   AND                                        
           DIA2  EQL  DIA1   THEN                                       
           BEGIN                                                        
           DIASAC:=0;                                                   
           R:=0;                                                        
           MES1:=0;                                                     
           DIA1:=0;                                                     
           GO     TO   SAIDA2;                                          
           END;                                                         
                                                                        
     %---------------------------------------------------------------%  
     %             CALCULO   DO   NUMERO    DE   ANOS                %  
     %---------------------------------------------------------------%  
                                                                        
    R:=0;                                                               
    IF     ANO2  GTR  ANO1    THEN                                      
           BEGIN                                                        
           R:=ANO2  -  ANO1;                                            
           IF     R        EQL   1      THEN                            
                  BEGIN                                                 
                  IF    MES2   GTR  MES1    OR                          
                        (MES2  EQL  MES1   AND                          
                        DIA2   GEQ  DIA1) THEN                          
                        GO     TO     CALCMES2                          
                  ELSE                                                  
                        R:=0;                                           
                  END;                                                  
           END;                                                         
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %             CALCULO   DO   NUMERO    DE   MESES               %  
     %---------------------------------------------------------------%  
                                                                        
   CALCMES2:                                                            
    R2:=0;                                                              
    IF    MES2    GTR   MES1   THEN                                     
          BEGIN                                                         
          R2:=MES2  -  MES1;                                            
          IF   DIA2    LSS   DIA1   THEN                                
               R2:=R2  -  1;                                            
          END                                                           
    ELSE                                                                
          IF   MES1   GTR  MES2   THEN                                  
               BEGIN                                                    
               R:=R6:=ANO2  -  (ANO1  +  1);                            
               R2:=(12  -  MES1)  +  MES2;                              
               IF    DIA2    LSS   DIA1   THEN                          
                     R2:=R2  -  1;                                      
               END;                                                     
   IF     R2     EQL   1      AND                                       
          DIA1   EQL   DIA2  THEN                                       
          BEGIN                                                         
          DIASAC:=F[Z];                                                 
          IF     Z    EQL     2    THEN                                 
                 BEGIN                                                  
                 ANOB:=ANO1;                                            
                 IF    ANOBISSEXTO  THEN                                
                       DIASAC:=*  +  1;                                 
                 END;                                                   
          MES1:=R2;                                                     
%         GO     TO    SAIDA2;                                          
          END;                                                          
    MES1:=R2;                                                           
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %             CALCULO   DO   NUMERO    DE   DIAS                %  
     %---------------------------------------------------------------%  
                                                                        
   R6:=R4:=DIASAC:=0;                                                   
   IF     DIA2   GTR   DIA1  THEN                                       
          DIASAC:=DIA2  -  DIA1                                         
   ELSE                                                                 
          IF    DIA1   GTR   DIA2  THEN                                 
                BEGIN                                                   
                IF    Z     EQL    MES2  THEN                           
                      BEGIN                                             
                      IF    Z    EQL   1   THEN                         
                            I2:=12                                      
                      ELSE                                              
                            I2:=Z  -  1;                                
                      DIASAC:=(F[I2]  -  DIA1)  +  DIA2;                
                      IF    I2   EQL   2   THEN                         
                            BEGIN                                       
                            ANOB:=ANO2;                                 
                            IF   ANOBISSEXTO THEN                       
                                 DIASAC:=*  +  1;                       
                            END;                                        
                      END                                               
                   ELSE                                                 
                      BEGIN                                             
                        ANOB:=ANO1;                                     
                        IF ANOBISSEXTO THEN                             
                           DIASAC:=(F1[Z] - DIA1)  + DIA2               
                        ELSE                                            
                           DIASAC:=(F[Z]  -  DIA1)  +  DIA2;            
                      END;                                              
                                                                        
                IF   (Z  +  1)  GTR   MES2  THEN                        
                      BEGIN                                             
                      R:=R6:=ANO2  -  (ANO1  +  1);                     
                      MES1:=(MES2  +  12)  -  (Z + 1);                  
                      END                                               
                ELSE                                                    
                      MES1:=MES2  -  (Z  +  1);                         
                END;                                                    
   R4:=DIASAC;                                                          
                                                                        
     %---------------------------------------------------------------%  
     %     CALCULO DOS DIAS ACUMULADOS ENTRE AS DATAS FORNECIDA      %  
     %---------------------------------------------------------------%  
                                                                        
      ANOB:=ANO1;                                                       
      IF ANOBISSEXTO THEN                                               
         BEGIN                                                          
           IF M1  GTR  2  THEN                                          
              A1:=365                                                   
           ELSE                                                         
              A1:=366;                                                  
         END                                                            
      ELSE                                                              
         A1:=365;                                                       
                                                                        
      ANOB:=ANO2;                                                       
      IF ANOBISSEXTO THEN                                               
         A2:=366                                                        
      ELSE                                                              
         A2:=365;                                                       
                                                                        
      IF   ( ANO2 - ANO1 )   EQL   0   THEN                             
           BEGIN                                                        
             DIASAC:=0;                                                 
             IF M2 GTR 2 THEN                                           
             A2:=365;                                                   
             DIASAC:=(A1 - C[M1] - DIA1);                               
             DIASAC:=(DIASAC - (A2 - (C[M2] + DIA2 )));                 
             GO TO SAIDA2;                                              
           END;                                                         
                                                                        
      IF   ( ANO2 - ANO1 )  EQL   1   THEN                              
           BEGIN                                                        
             DIASAC:=0;                                                 
             DIASAC:=(( A1 - C[M1] - DIA1) + (DIA2 + C[M2]));           
             IF A2  EQL   366   AND   M2   GTR   2   THEN               
                DIASAC:= * + 1;                                         
             GO TO SAIDA2;                                              
           END;                                                         
                                                                        
            IF (ANO2 - ANO1)  GTR   1   THEN                            
              BEGIN                                                     
                DIASAC:=0;                                              
                R8:= (ANO2 - ANO1) - 1;                                 
                DIASAC:=((A1 - C[M1] - DIA1) + (DIA2 + C[M2]));         
                IF A2 EQL 366 AND M2 GTR 2 THEN                         
                   DIASAC:= * + 1;                                      
                                                                        
                THRU   R8   DO                                          
                  BEGIN                                                 
                    ANO1:=  *  +  1;                                    
                    ANOB:=ANO1;                                         
                    IF  ANOBISSEXTO THEN                                
                         DIASAC:= * + 366                               
                    ELSE                                                
                         DIASAC:= * + 365;                              
                  END;                                                  
              END;                                                      
  SAIDA2:                                                               
    PTR:=DISP01;                                                        
    REPLACE  PTR  BY  "PROC DIF DE DATAS";                              
    PTP:=AREAA[16];                                                     
    REPLACE  PTP:PTP  BY  DIASAC  FOR  8  DIGITS;                       
    REPLACE  PTP:PTP  BY  R       FOR  4  DIGITS;                       
    REPLACE  PTP:PTP  BY  MES1    FOR  2  DIGITS;                       
    REPLACE  PTP:PTP  BY  R4      FOR  2  DIGITS;                       
    END;                                                                
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %            OP[]O 07 (SETE)   =   VERIFICA A DATA FUTURA       %  
     %                                  ANO COM 4 DIGITOS            %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %  1 - PARAMETROS                                               %  
     %      1.1 - OPCAO (2 BYTES)              =  07;                %  
     %      1.2 - DATA                         =  DDMMAAAA;          %  
     %      1.3 - QUANTIDADE DE DIAS (1 WORD)  =  NNNNNN;            %  
     %                                                               %  
     %  2 - RETORNO                                                  %  
     %      1.1 - CONS (1 BYTE)   = "C" (CERTO) OU "E" (ERRADO);     %  
     %      1.2 - DATA FUTURA     = DDMMAAAA;                        %  
     %---------------------------------------------------------------%  
                                                                        
    PROCEDURE   DFUTURA2;                                               
    BEGIN                                                               
    LABEL  SAIFUT2;                                                     
    PTS:=AREAA;                                                         
    PTQ:=DATAV2;                                                        
    REPLACE  PTQ  BY  PTS:PTS  FOR  8;                                  
    VALIDATA2;                                                          
    IF      NOT  RESULT   THEN                                          
            BEGIN                                                       
            PTR:=OPCONS[2];                                             
            REPLACE  PTR  BY  "E";                                      
            GO   TO       SAIFUT2;                                      
            END;                                                        
    SCAN  PTS  FOR  Q1:6  WHILE  IN  DIGITO;                            
    Q1:=6  -  Q1;                                                       
    IF      Q1    NEQ    6   THEN                                       
            BEGIN                                                       
            PTR:=OPCONS[2];                                             
            REPLACE  PTR  BY  "E";                                      
            GO    TO      SAIFUT2;                                      
            END;                                                        
    PTP:=AREAA;                                                         
    DIA1:=INTEGER (PTQ,2);                                              
    MES1:=INTEGER (PTQ + 2,2);                                          
    ANO1:=INTEGER (PTQ + 4,4);                                          
    MES2:=MES1;                                                         
    ANO2:=ANO1;                                                         
    QTD:=INTEGER(PTP + 8,6);                                            
    IF      (QTD + DIA1)   GTR  F[MES1]  THEN                           
            BEGIN                                                       
            R2:=0;                                                      
            R1:=QTD   +  DIA1;                                          
            DO    BEGIN                                                 
                  IF    R1   GTR   F[MES1]  THEN                        
                        BEGIN                                           
                        MES2:=*  +  1;                                  
                        IF     MES2   GTR  12  THEN                     
                               BEGIN                                    
                               ANO2:=ANO2  +  1;                        
                               MES2:=1;                                 
                               END;                                     
                        DIA2:=F[MES2];                                  
                        R1:=R1  -  F[MES1];                             
                        IF   MES1  EQL  2   THEN                        
                             BEGIN                                      
                             ANOB:=ANO2;                                
                             IF    ANOBISSEXTO THEN                     
                                   BEGIN                                
                                     R1:=R1  -  1;                      
                                     DIA2:=29;                          
                                     IF R1 EQL 29   %  OSM-08/10/99     
                                      THEN BRESTO29:= TRUE              
                                      ELSE                              
                                      IF R1 EQL 0                       
                                       THEN MES2:= * - 1;               
                                   END;                                 
                             END;                                       
                         END                                            
                  ELSE                                                  
                        BEGIN                                           
                        DIA2:=R1;                                       
                        R1:=0;                                          
                        END;                                            
                  MES1:=  MES2;                                         
                  END                                                   
                      UNTIL  R1  LEQ  R2;                               
              END                                                       
          ELSE                                                          
              DIA2:=DIA1  +  QTD;                                       
 %  IF   DIA2  EQL  29  AND  MES2  EQL  03  AND NOT BRESTO29            
 %    THEN                                                              
 %       BEGIN                                                          
 %       ANOB:=ANO2;                                                    
 %       IF    ANOBISSEXTO  THEN                                        
 %             BEGIN                                                    
 %               MES2:=*  -  1;                                         
 %               DIA2:=29;                                              
 %             END;                                                     
 %       END;                                                           
    PTP:=AREAA[14];                                                     
    REPLACE  PTP:PTP  BY  DIA2  FOR  2  DIGITS;                         
    REPLACE  PTP:PTP  BY  MES2  FOR  2  DIGITS;                         
    REPLACE  PTP:PTP  BY  ANO2  FOR  4  DIGITS;                         
 SAIFUT2:                                                               
    END;                                                                
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %      OP[]O 08 (TRES)   =   VERIFICA QUAL E O DIA DA SEMANA    %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   1 - PARAMETROS                                              %  
     %       1.1 - OPCAO (2 BYTES)    =   08;                        %  
     %       1.2 - DATA               =   DDMMAA;                    %  
     %       1.3 - FERIADOS MOVEIS    =   DDMM,DDMM,....,ETC.;       %  
     %                                                               %  
     %   2 - RETORNO                                                 %  
     %       2.1 - CONS (1 BYTE)  =  "C" (CERTO)  OU  "E" (ERRADO);  %  
     %       2.2 - DIA DA SEMANA  =  SEGUNDA, TERCA, QUARTA, QUINTA, %  
     %                               SEXTA, SABADO  E DOMINGO        %  
     %---------------------------------------------------------------%  
    PROCEDURE DIASEMANA1; FORWARD;                                      
    PROCEDURE   DSEMANA2;                                               
    BEGIN                                                               
     IF AREAA[04] GEQ 48"F0F0" AND AREAA[04] LSS 48"F3F1" % 2000 A 2030 
      THEN                                                              
       BEGIN                                                            
        REPLACE AREAA[06] BY AREAA[04] FOR 2;                           
        REPLACE AREAA[04] BY "20";                                      
        DIASEMANA1;                          % OPCAO 15 ANO C/ 4 DIG.   
        REPLACE AREAA[04] BY AREAA[06] FOR 2;                           
        CASE R OF                                                       
         BEGIN                                                          
          0: REPLACE PTP - 2   BY "SEGUNDA    ";                        
          1: REPLACE PTP - 2   BY "TER[A      ";                        
          2: REPLACE PTP - 2   BY "QUARTA     ";                        
          3: REPLACE PTP - 2   BY "QUINTA     ";                        
          4: REPLACE PTP - 2   BY "SEXTA      ";                        
          5: REPLACE PTP - 2   BY "SABADO     ";                        
          6: REPLACE PTP - 2   BY "DOMINGO    ";                        
          ELSE:                                ;                        
         END;                                                           
       END                                                              
      ELSE                                                              
       BEGIN                                                            
        DIASEMANA;                                                      
                                                                        
        IF   R         EQL       0       THEN                           
           REPLACE   PTP       BY      "SEGUNDA "                       
                                         ELSE                           
        IF  R       EQL       1       THEN                              
            REPLACE   PTP       BY    "TER[A    "                       
                                      ELSE                              
        IF  R       EQL       2       THEN                              
            REPLACE   PTP       BY    "QUARTA   "                       
                                      ELSE                              
        IF  R       EQL       3       THEN                              
            REPLACE   PTP       BY    "QUINTA   "                       
                                      ELSE                              
        IF  R       EQL       4       THEN                              
            REPLACE   PTP       BY    "SEXTA    ";                      
       END;                                                             
   END;                                                                 
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %    OP[]O 09 (NOVE)  =  VERIFICA QUAL E O DIA DA SEMANA        %  
     %                        UTILIZADA PELO  TRIBUNAL DE JUSTI[A    %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   1 - PARAMETROS                                              %  
     %       1.1 - OPCAO (2 BYTES)  =  9;                            %  
     %       1.2 - DATA             =  DDMMAA;                       %  
     %                                                               %  
     %   2 - RETORNO                                                 %  
     %       2.1 - CONS (1 BYTE)    =  "C" (CERTO)  OU  "E" (ERRADO);%  
     %       2.2 - DIA DA SEMANA    =  DIA UTIL, SABADO , DOMINGO OU %  
     %                                 FERIADO                       %  
     %---------------------------------------------------------------%  
                                                                        
   PROCEDURE  DSEMANA3;                                                 
   BEGIN                                                                
   LABEL  SAI03;                                                        
   FILL  D[*]  WITH  0101,2501,2104,0105,0709,1210,2810,0211,1511,2512; 
   PTS:=AREAA; PTQ:=DATAV;                                              
   PTR:=AREAA;                                                          
   REPLACE  PTQ  BY  PTS  FOR  6;                                       
   DIAV:=INTEGER (PTQ,2);                                               
   DIA1:=INTEGER (PTQ,2);                                               
   MESV:=INTEGER (PTQ + 2,2);                                           
   MES1:=INTEGER (PTQ + 2,2);                                           
   ANOV:=INTEGER (PTQ + 4,2);                                           
   ANO1:=INTEGER (PTQ + 4,2);                                           
   VALIDATA;                                                            
   PTP:=AREAA[06];                                                      
   IF    NOT  RESULT   THEN                                             
         BEGIN                                                          
         REPLACE   PTP      BY  "INVALIDO";                             
         GO        TO       SAI03;                                      
         END;                                                           
   ERRO:=FALSE;                                                         
   IF    RESULT    THEN                                                 
         BEGIN                                                          
         IF    ANO1    EQL  00  THEN                                    
               Q1:=52                                                   
         ELSE                                                           
           IF  ANO1    GTR  82  THEN                                    
               Q1:=((ANO1 - 83) * 3) + 1                                
           ELSE                                                         
               ERRO:=TRUE;                                              
         END                                                            
    ELSE                                                                
          ERRO:=TRUE;                                                   
    D[11]:=FER[Q1];                                                     
    R6:=Q1+1;                                                           
    D[12]:=FER[R6];                                                     
    R6:=Q1+2;                                                           
    D[13]:=FER[R6];                                                     
    IF    (ERRO     OR  NOT  RESULT)  THEN                              
          BEGIN                                                         
          REPLACE   PTP      BY  "INVALIDO";                            
          GO        TO       SAI03;                                     
          END;                                                          
    ANOB:=ANO1;                                                         
    IF    ANOBISSEXTO          AND                                      
          MES1      GTR       2         THEN                            
          DIA1:=DIA1 + 1;                                               
                                                                        
    X:=(INTEGERT ((ANO1 - 1) * 365)) + (INTEGERT((ANO1 - 1) / 4));      
    Y:=X + (C[MES1] + DIA1);                                            
    R:=Y  MOD  7;                                                       
    S:=13;                                                              
    IF   R         EQL       5       THEN                               
         REPLACE   PTP       BY      "SABADO "                          
    ELSE                                                                
      IF  R       EQL       6       THEN                                
          REPLACE   PTP       BY    "DOMINGO"                           
      ELSE                                                              
          BEGIN                                                         
          DIAUTIL:=TRUE;                                                
          PTQ:=AREAA;                                                   
          AUXDATA:=INTEGER (PTQ,4);                                     
          I:=0;                                                         
          DO   BEGIN                                                    
               I:=I + 1;                                                
               IF  AUXDATA   EQL       D[I]      THEN                   
                   BEGIN                                                
                   DIAUTIL:=FALSE;                                      
                   I:=99;                                               
                   END                                                  
               END                                                      
                   UNTIL   I    GTR        S;                           
         IF    DIAUTIL     THEN                                         
                BEGIN                                                   
                IF  R         EQL       0       THEN                    
                    REPLACE   PTP       BY      "SEGUNDA "              
                ELSE                                                    
                IF  R         EQL       1       THEN                    
                    REPLACE   PTP       BY    "TER[A    "               
                ELSE                                                    
                IF  R         EQL       2       THEN                    
                    REPLACE   PTP       BY    "QUARTA   "               
                ELSE                                                    
                IF  R         EQL       3       THEN                    
                    REPLACE   PTP       BY    "QUINTA   "               
                ELSE                                                    
                IF  R         EQL       4       THEN                    
                    REPLACE   PTP       BY    "SEXTA    ";              
                END                                                     
         ELSE                                                           
               REPLACE  PTP       BY       "FERIADO";                   
          END;                                                          
  SAI03:                                                                
    END;                                                                
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %   OP[]O 10 (DEZ)   =   VERIFICA QUAL E O DIA DA SEMANA        %  
     %                        UTILIZADA PELO TRIBUNAL DE JUSTI[A     %  
     %                        ANO COM 4  DIGITOS                     %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   1 - PARAMETROS                                              %  
     %       1.1 - OPCAO (2 BYTES)  =   10;                          %  
     %       1.2 - DATA             =   DDMMAAAA;                    %  
     %                                                               %  
     %   2 - RETORNO                                                 %  
     %       2.1 - CONS (1 BYTE)    =  "C" (CERTO)  OU  "E" (ERRADO);%  
     %       2.2 - DIA DA SEMANA    =  DIA UTIL, SABADO , DOMINGO OU %  
     %                                 FERIADO                       %  
     %---------------------------------------------------------------%  
                                                                        
   PROCEDURE  DSEMANA4;                                                 
   BEGIN                                                                
   LABEL  SAI04;                                                        
   FILL  D[*]  WITH  % FERIADOS FIXOS                                   
               0101,2501,2104,0105,0907,0709,1210,2810,0211,1511,2512;  
   PTS:=AREAA; PTQ:=DATAV2;                                             
   PTR:=AREAA;                                                          
   REPLACE  PTQ  BY  PTS  FOR  8;                                       
   DIAV:=INTEGER (PTQ,2);                                               
   DIA1:=INTEGER (PTQ,2);                                               
   MESV:=INTEGER (PTQ + 2,2);                                           
   MES1:=INTEGER (PTQ + 2,2);                                           
   ANOV:=INTEGER (PTQ + 4,4);                                           
   ANO1:=INTEGER (PTQ + 4,4);                                           
   VALIDATA2;                                                           
   PTP:=AREAA[08];                                                      
   IF    NOT  RESULT   THEN                                             
         BEGIN                                                          
         REPLACE   PTP      BY  "INVALIDO";                             
         GO        TO       SAI04;                                      
         END;                                                           
   ERRO:=FALSE;                                                         
   IF    RESULT    THEN                                                 
         BEGIN                                                          
         IF    ANO1    LSS  1983  OR                                    
               ANO1    GTR  2032  THEN                                  
               ERRO:=TRUE                                               
         ELSE                                                           
           IF  ANO1    EQL  1983  THEN                                  
               Q1:=1                                                    
           ELSE                                                         
                Q1:=((ANO1 - 1983) * 3) + 1;                            
         END                                                            
    ELSE                                                                
          ERRO:=TRUE;                                                   
    D[12]:=FER[Q1];  % CARNAVAL                                         
    R6:=Q1+1;                                                           
    D[13]:=FER[R6];  % SEXTA FEIRA DA PAIXAO                            
    R6:=Q1+2;                                                           
    D[14]:=FER[R6];  % CORPUS CRISTI                                    
    IF    (ERRO     OR  NOT  RESULT)  THEN                              
          BEGIN                                                         
          REPLACE   PTP      BY  "INVALIDO";                            
          GO        TO       SAI04;                                     
          END;                                                          
                                                                        
    %VERIFICA SE E ANO BISSEXTO                                         
                                                                        
    R:=ANO1  MOD  400;  % A CADA 400 ANOS O CALENDARIO SE REPETE        
                                                                        
    DATE:=C[MES1]+DIA1-1; %NUMERO DE DIAS DE 1 DE JANEIRO ATE O DIA     
                          %SOLICITADO                                   
    ANOB:=R;                                                            
    IF    ANOBISSEXTO   THEN                                            
          IF LEAPYEAR [R DIV 4] THEN BEGIN                              
          IF  MES1 > 2 THEN                                             
          DIA1:=DIA1 + 1; ANOBI:= TRUE; END;                            
                                                                        
 %  IF  R = 0 THEN % O ANO E MULTIPLO DE 400                            
 %     MES1:=MES1-1;                                                    
                                                                        
    JAN:=CENTURY[ R DIV 100];                                           
    R:=R MOD 100;                                                       
                                                                        
    IF R > 0 THEN                                                       
       BEGIN                                                            
                                                                        
       X:= R DIV 4;                                                     
       Y:= R MOD 4;                                                     
                                                                        
       JAN := JAN + (X*5) + Y;                                          
                                                                        
       IF Y = 0 THEN JAN:=JAN-1;                                        
       END;                                                             
       IF JAN < 0 THEN JAN:=JAN + 7;                                    
       DATE := (DATE+JAN) MOD 7;                                        
                                                                        
      S:=14;                                                            
      IF ANOBI THEN BEGIN                                               
       IF ANO1 LSS 2000 OR ANO1 EQL 2004 OR ANO1 EQL 2008 OR            
          ANO1 EQL 2012 OR ANO1 EQL 2016 OR ANO1 EQL 2020 OR            
          ANO1 EQL 2024 OR ANO1 EQL 2028 OR ANO1 EQL 2032 OR            
          ANO1 EQL 2036                                                 
        THEN                                                            
         IF MES1 > 2                                                    
          THEN                                                          
           BEGIN                                                        
            IF DATE EQL 6 THEN DATE:= 0                                 
                       ELSE DATE:= * + 1;                               
           END                                                          
          ELSE                                                          
        ELSE                                                            
         IF ANO1 EQL 2000                                               
          THEN                                                          
           BEGIN                                                        
            IF MES1 < 3                                                 
             THEN                                                       
              IF DATE EQL 0 THEN DATE:= 6                               
                         ELSE DATE := * -1;                             
           END; END;                                                    
                                                                        
      IF   DATE      EQL       5       THEN                             
           REPLACE   PTP       BY      "SABADO "                        
      ELSE                                                              
                                                                        
      IF   DATE    EQL       6         THEN                             
           REPLACE   PTP       BY      "DOMINGO"                        
      ELSE                                                              
          BEGIN                                                         
          DIAUTIL:=TRUE;                                                
          PTQ:=AREAA;                                                   
          AUXDATA:=INTEGER (PTQ,4);                                     
          I:=0;                                                         
          DO   BEGIN                                                    
               I:=I + 1;                                                
               IF  AUXDATA   EQL       D[I]      THEN                   
                   BEGIN                                                
                   DIAUTIL:=FALSE;                                      
                   I:=99;                                               
                   END                                                  
               END                                                      
                   UNTIL   I    GTR        S;                           
         IF    DIAUTIL     THEN                                         
               BEGIN                                                    
               IF  DATE      EQL       0       THEN                     
                   REPLACE   PTP       BY      "SEGUNDA "               
               ELSE                                                     
               IF  DATE      EQL       1       THEN                     
                   REPLACE   PTP       BY    "TER[A    "                
               ELSE                                                     
               IF  DATE      EQL       2       THEN                     
                   REPLACE   PTP       BY    "QUARTA   "                
               ELSE                                                     
               IF  DATE      EQL       3       THEN                     
                   REPLACE   PTP       BY    "QUINTA   "                
               ELSE                                                     
               IF  DATE      EQL       4       THEN                     
                   REPLACE   PTP       BY    "SEXTA    ";               
               END                                                      
         ELSE                                                           
               REPLACE  PTP       BY       "FERIADO";                   
          END;                                                          
  SAI04:                                                                
    END;                                                                
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %            OP[]O 11 (ONZE)   =   SUBTRAI ANOS, MESES E DIAS   %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %  1 - PARAMETROS                                               %  
     %      1.1 - OPCAO (2 BYTES)           =  11                    %  
     %      1.2 - DATA INFORMADA            =  DDMMAA;               %  
     %      1.3 - QTDE DE DIAS,MESES E ANOS =  DDMMAA;               %  
     %                                                               %  
     %  2 - RETORNO                                                  %  
     %      2.1 - C = CERTO;                                         %  
     %      2.2 - E = ERRADO;                                        %  
     %---------------------------------------------------------------%  
                                                                        
   PROCEDURE  SUBTRDATA;                                                
   BEGIN                                                                
   LABEL  SAIDA,RESP;                                                   
   PTP:=AREAA[6];                                                       
   PTQ:=DATAV;                                                          
   REPLACE  PTQ  BY  PTP  FOR  6;                                       
   DIAV:=DIA1:=INTEGER (PTQ ,2);                                        
   MESV:=MES1:=INTEGER (PTQ + 2,2);                                     
   ANOV:=ANO1:=INTEGER (PTQ + 4,2);                                     
   SCAN  PTQ  FOR  Q1:6  WHILE  IN  DIGITO;                             
   Q1:=6  -  Q1;                                                        
   IF     Q1     EQL   6   THEN                                         
          BEGIN                                                         
          IF  MES1  GTR      12     OR                                  
              DIA1  GTR      31     OR                                  
              ANO1  GTR      ANOV   THEN                                
              BEGIN                                                     
              PTR:=OPCONS[2];                                           
              REPLACE  PTR  BY  "E";                                    
              GO    TO    SAIDA;                                        
              END;                                                      
          END;                                                          
   PTP:=AREAA;                                                          
   PTQ:=DATAV;                                                          
   REPLACE  PTQ  BY  PTP  FOR  6;                                       
   DIAV:=INTEGER (PTQ ,2);                                              
   ANOV:=INTEGER (PTQ + 4,2);                                           
   MESV:=INTEGER (PTQ + 2,2);                                           
   VALIDATA;                                                            
   IF     NOT   RESULT    THEN                                          
          BEGIN                                                         
          PTR:=OPCONS[2];                                               
          REPLACE  PTR  BY  "E";                                        
          GO    TO    SAIDA;                                            
          END;                                                          
   ANO3:=ANOV  -  ANO1;                                                 
   IF      MESV   GTR   MES1     THEN                                   
           MES3:=MESV   -   MES1                                        
   ELSE                                                                 
           BEGIN                                                        
           ANO3:=ANO3   -   1;                                          
           MES3:=MESV   +   12;                                         
           MES3:=MES3   -   MES1;                                       
           END;                                                         
   IF      DIA1   EQL   0        THEN                                   
           BEGIN                                                        
           DIA3:=DIAV;                                                  
           IF     DIA3     GTR  F[MES3]   THEN                          
                  DIA3:=F[MES3];                                        
           ANOB:=ANO3;                                                  
           IF    ANOBISSEXTO THEN                                       
                   DIA3:=DIA3   +    1;                                 
                   GO     TO    RESP;                                   
           END;                                                         
   IF      DIA1   GEQ   F[MES3]    THEN                                 
     IF    MES3    NEQ   2             THEN                             
           BEGIN                                                        
           PTR:=OPCONS[2];                                              
           REPLACE  PTR  BY  "E";                                       
           GO    TO    SAIDA;                                           
           END                                                          
     ELSE                                                               
           BEGIN                                                        
           ANOB:=ANO3;                                                  
           IF ANOBISSEXTO THEN                                          
               BEGIN                                                    
               IF   DIA1    GEQ   29    THEN                            
                    BEGIN                                               
                    PTR:=OPCONS[2];                                     
                    REPLACE  PTR  BY  "E";                              
                    GO    TO    SAIDA;                                  
                    END;                                                
               END;                                                     
           END;                                                         
   IF      DIAV   EQL   F[MESV]   AND MESV EQL 02 THEN                  
           BEGIN                                                        
           DIAV:=F[MES3];                                               
           ANOB:=ANO3;                                                  
           IF ANOBISSEXTO THEN                                          
                 DIAV:=DIAV   +    1;                                   
           END;                                                         
   IF      DIAV   GTR   DIA1     THEN                                   
           DIA3:=DIAV   -   DIA1                                        
   ELSE                                                                 
           BEGIN                                                        
           MES3:=MES3   -  1;                                           
           IF  MES3   EQL   0    THEN                                   
               BEGIN                                                    
               ANO3:=ANO3  -   1;                                       
               MES3:=12;                                                
               END;                                                     
           DIA3:=(F[MES3]  +  DIAV)  -  DIA1;                           
           IF  MES3   EQL   2    THEN                                   
               BEGIN                                                    
               ANOB:=ANO3;                                              
               IF   ANOBISSEXTO THEN                                    
                     DIA3:=DIA3  +  1;                                  
               END;                                                     
           END;                                                         
 RESP:                                                                  
   PTP:=AREAA[0];                                                       
   REPLACE    PTP:PTP   BY  DIA3  FOR  2  DIGITS;                       
   REPLACE    PTP:PTP   BY  MES3  FOR  2  DIGITS;                       
   REPLACE    PTP:PTP   BY  ANO3  FOR  2  DIGITS;                       
   PTQ:=OPCONS[2];                                                      
   REPLACE    PTQ       BY  "C";                                        
  SAIDA:                                                                
    END;                                                                
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %            OP[]O 12 (DOZE)   =   VERIFICA DATA PASSADA        %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %  1 - PARAMETROS                                               %  
     %      1.1 - OPCAO (2 BYTES)             =  12;                 %  
     %      1.2 - DATA                        =  DDMMAA;             %  
     %      1.3 - QUANTIDADE DE DIAS (1 WORD) =  NNNNNN;             %  
     %                                                               %  
     %  2 - RETORNO                                                  %  
     %      1.1 - CONS (1 BYTE)   =  "C" (CERTO) OU "E" (ERRADO);    %  
     %      1.2 - DATA PASSADA    =  DDMMAA;                         %  
     %---------------------------------------------------------------%  
                                                                        
    PROCEDURE   DPASSADA;                                               
    BEGIN                                                               
    LABEL  SAIPAS;                                                      
    PTS:=AREAA;                                                         
    PTQ:=DATAV;                                                         
    REPLACE  PTQ  BY  PTS:PTS  FOR  6;                                  
    VALIDATA;                                                           
    IF      NOT  RESULT   THEN                                          
            BEGIN                                                       
            PTR:=OPCONS[2];                                             
            REPLACE  PTR  BY  "E";                                      
            GO   TO       SAIPAS;                                       
            END;                                                        
    SCAN  PTS  FOR  Q1:6  WHILE  IN  DIGITO;                            
    Q1:=6  -  Q1;                                                       
    IF      Q1    NEQ    6   THEN                                       
            BEGIN                                                       
            PTR:=OPCONS[2];                                             
            REPLACE  PTR  BY  "E";                                      
            GO    TO      SAIPAS;                                       
            END;                                                        
    PTP:=AREAA;                                                         
    DIA1:=INTEGER (PTQ,2);                                              
    MES1:=INTEGER (PTQ + 2,2);                                          
    ANO1:=INTEGER (PTQ + 4,2);                                          
    MES3:=MES2:=MES1;                                                   
    ANO3:=ANO2:=ANO1;                                                   
    QTD:=INTEGER(PTP + 6,6);                                            
    IF      QTD     GEQ    DIA1   THEN                                  
            BEGIN                                                       
            R2:=0;                                                      
            MES2:=* - 1;                                                
            IF     MES2   EQL   0  THEN                                 
                   BEGIN                                                
                   ANO2:=ANO2  -  1;                                    
                   MES2:=12;                                            
                   END;                                                 
            IF     MES1  EQL  2   THEN                                  
                   BEGIN                                                
                   ANOB:=ANO2;                                          
                   IF  ANOBISSEXTO  THEN                                
                         R1:=R1  -  1;                                  
                   END;                                                 
            R1:=QTD - DIA1;                                             
            MES1:=MES2;                                                 
            DO    BEGIN                                                 
                  IF    R1   GEQ   F[MES2]  THEN                        
                        BEGIN                                           
                        MES2:=*  -  1;                                  
                        IF     MES2   EQL   0  THEN                     
                               BEGIN                                    
                               ANO2:=ANO2  -  1;                        
                               MES2:=12;                                
                               END;                                     
                        DIA2:=F[MES2];                                  
                        R1:=R1 - F[MES1];                               
                        IF   MES1  EQL  2   THEN                        
                             BEGIN                                      
                             ANOB:=ANO2;                                
                             IF    ANOBISSEXTO THEN                     
                                   R1:=R1  -  1;                        
                             END;                                       
                         END                                            
                  ELSE                                                  
                        BEGIN                                           
                        DIA2:=F[MES2] - R1;                             
                        IF   MES2  EQL  2   THEN                        
                             BEGIN                                      
                             ANOB:=ANO2;                                
                             IF    ANOBISSEXTO   THEN                   
                                   DIA2:=*  +  1;                       
                             END;                                       
                        R1:=0;                                          
                        END;                                            
                  MES1 := MES2;                                         
                  END                                                   
                      UNTIL  R1  LEQ  R2;                               
              END                                                       
          ELSE                                                          
              DIA2:=DIA1  -  QTD;                                       
    PTP:=AREAA[0];                                                      
    REPLACE  PTP:PTP  BY  DIA2  FOR  2  DIGITS;                         
    REPLACE  PTP:PTP  BY  MES2  FOR  2  DIGITS;                         
    REPLACE  PTP:PTP  BY  ANO2  FOR  2  DIGITS;                         
  SAIPAS:                                                               
     END;                                                               
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %            OP[]O 13 (TREZE)  =   VERIFICA DATA PASSADA        %  
     %                                  ANO COM 4 DIGITOS            %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %  1 - PARAMETROS                                               %  
     %      1.1 - OPCAO (2 BYTES)              =  13;                %  
     %      1.2 - DATA                         =  DDMMAAAA;          %  
     %      1.3 - QUANTIDADE DE DIAS (1 WORD)  =  NNNNNN;            %  
     %                                                               %  
     %  2 - RETORNO                                                  %  
     %      1.1 - CONS (1 BYTE)   = "C" (CERTO) OU "E" (ERRADO);     %  
     %      1.2 - DATA PASSADA    = DDMMAAAA;                        %  
     %---------------------------------------------------------------%  
                                                                        
    PROCEDURE   DPASSADA2;                                              
    BEGIN                                                               
    LABEL  SAIPAS2;                                                     
    PTS:=AREAA;                                                         
    PTQ:=DATAV2;                                                        
    REPLACE  PTQ  BY  PTS:PTS  FOR  8;                                  
    VALIDATA2;                                                          
    IF      NOT  RESULT   THEN                                          
            BEGIN                                                       
            PTR:=OPCONS[2];                                             
            REPLACE  PTR  BY  "E";                                      
            GO   TO       SAIPAS2;                                      
            END;                                                        
    SCAN  PTS  FOR  Q1:6  WHILE  IN  DIGITO;                            
    Q1:=6  -  Q1;                                                       
    IF      Q1    NEQ    6   THEN                                       
            BEGIN                                                       
            PTR:=OPCONS[2];                                             
            REPLACE  PTR  BY  "E";                                      
            GO    TO      SAIPAS2;                                      
            END;                                                        
    PTP:=AREAA;                                                         
    DIA1:=INTEGER (PTQ,2);                                              
    MES1:=INTEGER (PTQ + 2,2);                                          
    ANO1:=INTEGER (PTQ + 4,4);                                          
    MES3:=MES2:=MES1;                                                   
    ANO3:=ANO2:=ANO1;                                                   
    QTD:=INTEGER(PTP + 8,6);                                            
    IF      QTD     GEQ    DIA1   THEN                                  
            BEGIN                                                       
            R2:=0;                                                      
            MES2:=*  -  1;                                              
            IF     MES2   EQL   0  THEN                                 
                   BEGIN                                                
                   ANO2:=ANO2  -  1;                                    
                   MES2:=12;                                            
                   END;                                                 
            IF     MES1  EQL  2   THEN                                  
                   BEGIN                                                
                   ANOB:=ANO2;                                          
                   IF    ANOBISSEXTO  THEN                              
                         R1:=R1  -  1;                                  
                   END;                                                 
            R1:=QTD - DIA1;                                             
            MES1:=MES2;                                                 
            DO    BEGIN                                                 
                  IF    R1   GEQ   F[MES2]  THEN                        
                        BEGIN                                           
                        MES2:=*  -  1;                                  
                        IF     MES2   EQL   0  THEN                     
                               BEGIN                                    
                               ANO2:=ANO2  -  1;                        
                               MES2:=12;                                
                               END;                                     
                        DIA2:=F[MES2];                                  
                        R1:=R1 - F[MES1];                               
                        IF   MES1  EQL  2   THEN                        
                             BEGIN                                      
                             ANOB:=ANO2;                                
                             IF   ANOBISSEXTO   THEN                    
                                   R1:=R1  -  1;                        
                             END;                                       
                         END                                            
                  ELSE                                                  
                        BEGIN                                           
                        DIA2:=F[MES2] - R1;                             
                        IF   MES2  EQL  2   THEN                        
                             BEGIN                                      
                             ANOB:=ANO2;                                
                             IF    ANOBISSEXTO THEN                     
                                   DIA2:=*  +  1;                       
                             END;                                       
                        R1:=0;                                          
                        END;                                            
                  MES1 := MES2;                                         
                  END                                                   
                      UNTIL  R1  LEQ  R2;                               
              END                                                       
          ELSE                                                          
              DIA2:=DIA1  -  QTD;                                       
    PTP:=AREAA[14];                                                     
    REPLACE  PTP:PTP  BY  DIA2  FOR  2  DIGITS;                         
    REPLACE  PTP:PTP  BY  MES2  FOR  2  DIGITS;                         
    REPLACE  PTP:PTP  BY  ANO2  FOR  4  DIGITS;                         
    SAIPAS2:                                                            
    END;                                                                
                                                                        
                                                                        
    %---------------------------------------------------------------%   
    %         INICIO  DA OP[]O 14 (QUATORZE) =  DATA DO DIA         %   
    %                                           ANO COM 4 DIGITOS   %   
    %---------------------------------------------------------------%   
    %                                                               %   
    %   1  -  PARAMETRO                                             %   
    %         OP[]O  (2 BYTES)   =  14 (QUATORZE)                   %   
    %                                                               %   
    %   2  -  RETORNO                                               %   
    %         DATA DO DIA        =  DD/MM/AAAA                      %   
    %---------------------------------------------------------------%   
                                                                        
    PROCEDURE DATADIA2;                                                 
    BEGIN                                                               
        ARRAY B[0:0];                                                   
        PTP:=AREAA;                                                     
        B[0]:=TIME(7);                                                  
        REPLACE PTP:PTP       BY B[0].[29:06]  FOR 2 DIGITS;            
        REPLACE PTP:PTP       BY "/";                                   
        REPLACE PTP:PTP       BY B[0].[35:06]  FOR 2 DIGITS;            
        REPLACE PTP:PTP       BY "/";                                   
        REPLACE PTP:PTP       BY B[0].[47:12]  FOR 4 DIGITS;            
        PTR:=OPCONS[2];                                                 
        REPLACE PTR BY "C";                                             
    END;                                                                
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %        OP[]O  15 (QUINZE)  =  VERIFICA O DIA DA SEMANA        %  
     %                               ANO COM 4 DIGITOS               %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   1 - PARAMETROS                                              %  
     %       1.1 - OPCAO (2 BYTES)  =  15;                           %  
     %       1.2 - DATA             =  DDMMAAAA;                     %  
     %       1.3 - FERIADOS MOVEIS  =  DDMM,DDMM,....,ETC.;          %  
     %                                                               %  
     %   2 - RETORNO                                                 %  
     %       2.1 - CONS (1 BYTE) = "C" (CERTO)  OU  "E" (ERRADO);    %  
     %       2.2 - DIA DA SEMANA = DIA UTIL, SABADO , DOMINGO OU     %  
     %                             FERIADO                           %  
     %---------------------------------------------------------------%  
                                                                        
     PROCEDURE  DIASEMANA1;                                             
     BEGIN                                                              
         LABEL  SAISEM;                                                 
         FILL  D[*]  WITH  0101,2104,0105,0709,1210,0211,1511,2512;     
         PTS:=AREAA; PTQ:=DATAV2;                                       
         PTR:=AREAA;                                                    
         REPLACE  PTQ  BY  PTS  FOR  8;                                 
         DIAV:=INTEGER (PTQ,2);                                         
         DIA1:=INTEGER (PTQ,2);                                         
         MESV:=INTEGER (PTQ + 2,2);                                     
         MES1:=INTEGER (PTQ + 2,2);                                     
         ANOV:=INTEGER (PTQ + 4,4);                                     
         ANO1:=INTEGER (PTQ + 4,4);                                     
         ERRO:=FALSE;                                                   
         VALIDATA2;                                                     
         IF   RESULT    THEN                                            
          BEGIN                                                         
              ERRO:=FALSE;                                              
              PTS:=PTS+4;                                               
              S:=8;                                                     
              PTR:=AREAA[9];                                            
              SCAN  PTR  FOR  Q1:52  WHILE IN DIGITO;                   
              Q1:=52  -  Q1  + 1;                                       
              X:=INTEGERT (Q1  /  4);                                   
              IF   X   GTR   10  THEN                                   
              X:=0;                                                     
              THRU   X   DO                                             
              BEGIN                                                     
                  PTS:=PTS + 4;                                         
                  AUXDATA:=INTEGER  (PTS,4);                            
                  REPLACE  PTQ  BY  PTS  FOR  4;                        
                  VALIDATA2;                                            
                  IF  RESULT    THEN                                    
                  BEGIN                                                 
                      S:=S + 1;                                         
                      D[S]:=AUXDATA;                                    
                  END                                                   
                  ELSE                                                  
                  ERRO:=TRUE;                                           
              END                                                       
          END                                                           
         ELSE                                                           
            ERRO:=TRUE;                                                 
                                                                        
         PTP:=AREAA[08];                                                
         X:=X  *  4;                                                    
         PTP:=*  +  X;                                                  
         IF   (ERRO     OR  NOT  RESULT)  THEN                          
              BEGIN                                                     
                  REPLACE   PTP      BY  "INVALIDO";                    
                  GO        TO       SAISEM;                            
              END;                                                      
                                                                        
         R:=ANO1  MOD  400;                                             
         DATE :=C[MES1] + DIA1 - 1;                                     
         ANOB:=R;                                                       
         IF ANOBISSEXTO          THEN         % PODE SER UM ANO BISSEXTO
         IF  LEAPYEAR [R DIV 4]  THEN BEGIN                             
             IF MES1 > 2  THEN                                          
             DIA1:=DIA1 + 1; ANOBI:= TRUE; END;                         
                                                                        
   %     IF R = 0 THEN                        % O ANO E MULTIPLO DE 400 
   %        MES1:=MES1-1;                                               
                                                                        
         JAN:=CENTURY[R DIV 100];                                       
         R:=R MOD 100;                                                  
                                                                        
         IF  R > 0 THEN                                                 
         BEGIN                                                          
             X:= R DIV 4;                                               
             Y:= R MOD 4;                                               
                                                                        
         JAN:=JAN + (X*5) + Y;                                          
                                                                        
         IF Y = 0 THEN                                                  
            JAN:=JAN-1;                                                 
         END;                                                           
                                                                        
         IF JAN < 0 THEN                                                
            JAN:=JAN+7;                                                 
                                                                        
         R:=(DATE+JAN) MOD 7;                                           
         IF ANOBI THEN BEGIN                                            
         IF ANO1 LSS 2000 OR ANO1 EQL 2004 OR ANO1 EQL 2008 OR          
            ANO1 EQL 2012 OR ANO1 EQL 2016 OR ANO1 EQL 2020 OR          
            ANO1 EQL 2024 OR ANO1 EQL 2028 OR ANO1 EQL 2032 OR          
            ANO1 EQL 2036                                               
          THEN                                                          
           IF MES1 > 2                                                  
            THEN                                                        
             BEGIN                                                      
              IF R EQL 6 THEN R:= 0                                     
                         ELSE R:= * + 1;                                
             END                                                        
            ELSE                                                        
          ELSE                                                          
           IF ANO1 EQL 2000                                             
            THEN                                                        
             BEGIN                                                      
              IF MES1 < 3                                               
               THEN                                                     
                IF R EQL 0 THEN R:= 6                                   
                           ELSE R:= * -1;                               
             END; END;                                                  
         IF   R         EQL       5       THEN                          
              REPLACE   PTP       BY      "SABADO "                     
         ELSE                                                           
            IF  R       EQL       6       THEN                          
                REPLACE   PTP       BY    "DOMINGO"                     
            ELSE                                                        
               BEGIN                                                    
                   DIAUTIL:=TRUE;                                       
                   PTQ:=AREAA;                                          
                   AUXDATA:=INTEGER (PTQ,4);                            
                   I:=0;                                                
                   DO                                                   
                        BEGIN                                           
                            I:=I + 1;                                   
                            IF  AUXDATA   EQL       D[I]      THEN      
                                BEGIN                                   
                                    DIAUTIL:=FALSE;                     
                                    I:=99;                              
                                END                                     
                        END                                             
                   UNTIL   I    GTR        S;                           
                   IF    DIAUTIL     THEN                               
                         REPLACE  PTP     BY       "DIA UTIL"           
                   ELSE                                                 
                       REPLACE  PTP       BY       "FERIADO";           
               END;                                                     
         SAISEM:                                                        
     END;                                                               
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %          OP[]O 16 (DEZESSEIS) =  SUBTRAI ANOS, MESES E DIAS   %  
     %                                  ANO COM 4 DIGITOS            %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %  1 - PARAMETROS                                               %  
     %      1.1 - OPCAO (2 BYTES)           =  16                    %  
     %      1.2 - DATA INFORMADA            =  DDMMAAAA;             %  
     %      1.3 - QTDE DE DIAS,MESES E ANOS =  DDMMAAAA;             %  
     %                                                               %  
     %  2 - RETORNO                                                  %  
     %      2.1 - C = CERTO;                                         %  
     %      2.2 - E = ERRADO;                                        %  
     %---------------------------------------------------------------%  
                                                                        
     PROCEDURE  SUBTRDATA1;                                             
     BEGIN                                                              
       LABEL  SAIDA,RESP;                                               
       PTP:=AREAA[8];                                                   
       PTQ:=DATAV2;                                                     
       REPLACE  PTQ  BY  PTP  FOR  8;                                   
                                                                        
       DIAV:=DIA1:=INTEGER (PTQ ,2);                                    
       MESV:=MES1:=INTEGER (PTQ + 2,2);                                 
       ANOV:=ANO1:=INTEGER (PTQ + 4,4);                                 
       SCAN  PTQ  FOR  Q1:8  WHILE  IN  DIGITO;                         
       Q1:=8  -  Q1;                                                    
       IF     Q1     EQL   8   THEN                                     
              BEGIN                                                     
              IF  MES1  GTR      12     OR                              
                  DIA1  GTR      31     OR                              
                  ANO1  GTR      ANOV   THEN                            
                  BEGIN                                                 
                  PTR:=OPCONS[2];                                       
                  REPLACE  PTR  BY  "E";                                
                  GO    TO    SAIDA;                                    
                  END;                                                  
              END;                                                      
       PTP:=AREAA;                                                      
       PTQ:=DATAV2;                                                     
                                                                        
       REPLACE  PTQ  BY  PTP  FOR  8;                                   
                                                                        
       DIAV:=INTEGER (PTQ ,2);                                          
       ANOV:=INTEGER (PTQ + 4,4);                                       
       MESV:=INTEGER (PTQ + 2,2);                                       
                                                                        
                                                                        
       VALIDATA2;                                                       
       IF     NOT   RESULT    THEN                                      
              BEGIN                                                     
              PTR:=OPCONS[2];                                           
              REPLACE  PTR  BY  "E";                                    
              GO    TO    SAIDA;                                        
              END;                                                      
       ANO3:=ANOV  -  ANO1;                                             
                                                                        
       IF      MESV   GTR   MES1     THEN                               
               MES3:=MESV   -   MES1                                    
       ELSE                                                             
               BEGIN                                                    
               ANO3:=ANO3   -   1;                                      
               MES3:=MESV   +   12;                                     
               MES3:=MES3   -   MES1;                                   
               END;                                                     
       IF      DIA1   EQL   0        THEN                               
               BEGIN                                                    
               DIA3:=DIAV;                                              
               IF     DIA3     GTR  F[MES3]   THEN                      
                      DIA3:=F[MES3];                                    
               ANOB:=ANO3;                                              
               IF   ANOBISSEXTO      THEN                               
                      DIA3:=DIA3   +    1;                              
               GO     TO    RESP;                                       
               END;                                                     
       IF      DIA1   GEQ   F[MES3]    THEN                             
         IF    MES3    NEQ   2             THEN                         
               BEGIN                                                    
               PTR:=OPCONS[2];                                          
               REPLACE  PTR  BY  "E";                                   
               GO    TO    SAIDA;                                       
               END                                                      
         ELSE                                                           
               BEGIN                                                    
               ANOB:=ANO3;                                              
               IF  ANOBISSEXTO         THEN                             
                   BEGIN                                                
                   IF   DIA1    GEQ   29    THEN                        
                        BEGIN                                           
                        PTR:=OPCONS[2];                                 
                        REPLACE  PTR  BY  "E";                          
                        GO    TO    SAIDA;                              
                        END;                                            
                   END;                                                 
               END;                                                     
       IF      DIAV   EQL   F[MESV]   AND MESV EQL 02 THEN              
               BEGIN                                                    
               DIAV:=F[MES3];                                           
               ANOB:=ANO3;                                              
               IF    ANOBISSEXTO       THEN                             
                     DIAV:=DIAV   +    1;                               
               END;                                                     
       IF      DIAV   GTR   DIA1     THEN                               
               DIA3:=DIAV   -   DIA1                                    
       ELSE                                                             
               BEGIN                                                    
               MES3:=MES3   -  1;                                       
               IF  MES3   EQL   0    THEN                               
                   BEGIN                                                
                   ANO3:=ANO3  -   1;                                   
                   MES3:=12;                                            
                   END;                                                 
               DIA3:=(F[MES3]  +  DIAV)  -  DIA1;                       
               IF  MES3   EQL   2    THEN                               
                   BEGIN                                                
                   ANOB:=ANO3;                                          
                   IF    ANOBISSEXTO        THEN                        
                         DIA3:=DIA3  +  1;                              
                   END;                                                 
               END;                                                     
     RESP:                                                              
       PTP:=AREAA[0];                                                   
       REPLACE    PTP:PTP   BY  DIA3  FOR  2  DIGITS;                   
       REPLACE    PTP:PTP   BY  MES3  FOR  2  DIGITS;                   
       REPLACE    PTP:PTP   BY  ANO3  FOR  4  DIGITS;                   
       PTQ:=OPCONS[2];                                                  
       REPLACE    PTQ       BY  "C";                                    
       PTP:=AREAA[0];                                                   
       SAIDA:                                                           
       END;                                                             
                                                                        
                                                                        
    %-----------------------------------------------------------------% 
    %   L O G I C A      P R I N C I P A L    -    C A L C D A T A 2  % 
    %-----------------------------------------------------------------% 
                                                                        
    BEGIN                                                               
    PTR:=OPCONS;                                                        
    N:=INTEGER (PTR,2);                                                 
    IF    N        GTR  16  THEN                                        
          BEGIN                                                         
           PTR:=OPCONS[2];                                              
           REPLACE PTR BY "E";                                          
           GO TO FIM1;                                                  
          END;                                                          
    IF    N        EQL  1  THEN                                         
          BEGIN                                                         
          PTP:=AREAA;                                                   
          PTQ:=DATAV;                                                   
          REPLACE  PTQ  BY  PTP  FOR  6;                                
          END;                                                          
    IF    N        EQL  5  THEN                                         
          BEGIN                                                         
          PTP:=AREAA;                                                   
          PTQ:=DATAV2;                                                  
          REPLACE  PTQ  BY  PTP  FOR  8;                                
          END;                                                          
    CASE  N  OF  BEGIN                                                  
                   DATADIA;                                             
                   VALIDATA;                                            
                   DIASEMANA;                                           
                   DIFDATA;                                             
                   DFUTURA;                                             
                   VALIDATA2;                                           
                   DIFDATA2;                                            
                   DFUTURA2;                                            
                   DSEMANA2;                                            
                   DSEMANA3;                                            
                   DSEMANA4;                                            
                   SUBTRDATA;                                           
                   DPASSADA;                                            
                   DPASSADA2;                                           
                   DATADIA2;                                            
                   DIASEMANA1;                                          
                   SUBTRDATA1;                                          
                 END                                                    
    END;                                                                
   FIM1:                                                                
END OF CALCDATA2;                                                       
                                                                        
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
 %                                                                   %  
 %                        LIBRARY     CALCDATA3                      %  
 %                                                                   %  
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
                                                                        
 PROCEDURE   CALCDATA3 (OPCONS,AREAA);                                  
 EBCDIC  ARRAY  OPCONS,AREAA[0];                                        
 BEGIN                                                                  
     FILE  IMP (KIND=PRINTER,MAXRECSIZE=132,BLOCKSIZE=132,UNITS=1);     
     EBCDIC  ARRAY   DATAV[1:6],                                        
                     DISP01[1:30],                                      
                     DATAV2[1:8];                                       
     BOOLEAN BRESTO29;  % OSM-08/10/99                                  
     %---------------------------------------------------------------%  
     %  ARRAY C = CONTEM A QUANTIDADE DE DIAS ACUMULADO NO ANO       %  
     %                                                               %  
     %  ARRAY F = CONTEM A QUANTIDADE DE DIAS DO MES (ANO NORMAL)    %  
     %                                                               %  
     %  ARRAY F1= CONTEM A QUANTIDADE DE DIAS DO MES (ANO BISSEXTO)  %  
     %                                                               %  
     %  ARRAY FER = CONTEM A DATA DOS FERIADOS MOVEIS DE 1983 ATE O  %  
     %              ANO 2000 (FERIADOS : CARNAVAL , SEXTA FEIRA DA   %  
     %                                   PAIXAO E CORPUS CHRISTUS)   %  
     %                                                               %  
     %  ARRAY CENTURY = FORNECE SE O DIA DA SEMANA EM QUE 1 DE       %  
     %                  JANEIRO CAIU NO SECULO DO ANO PROCURADO      %  
     %                                                               %  
     %  ARRAY LEAPYEAR = VERIFICA SE O ANO PROCURADO E BISSEXTO      %  
     %                                                               %  
     %---------------------------------------------------------------%  
                                                                        
     REAL VALUE ARRAY C  (0,  0, 31, 59, 90,120,151,                    
                            181,212,243,273,304,334);                   
                                                                        
     REAL VALUE ARRAY F1 (0,31,29,31,30,31,30,31,31,30,31,30,31);       
                                                                        
     REAL VALUE ARRAY F  (0,31,28,31,30,31,30,31,31,30,31,30,31);       
                                                                        
     REAL VALUE ARRAY FER(0,1502,0104,0206,0603,2004,2106, % 1983/1984  
                            1902,0504,0606,1102,2803,2905, % 1985/1986  
                            0303,1704,1806,1602,0104,0206, % 1987/1988  
                            0702,2403,2505,2702,1304,1406, % 1989/1990  
                            1202,2903,3005,0303,1704,1806, % 1991/1992  
                            2302,0904,1006,1502,0104,0206, % 1993/1994  
                            2802,1404,1506,2002,0504,0606, % 1995/1996  
                            1102,2803,2905,2402,1004,1106, % 1997/1998  
                            1602,0204,0306,0703,2104,2206, % 1999/2000  
                            2702,1304,1406,1202,2903,3005, % 2001/2002  
                            0403,1804,1906,2402,0904,1006, % 2003/2004  
                            0802,2503,2605,2802,1404,1506, % 2005/2006  
                            2002,0604,0706,0502,2103,2205, % 2007/2008  
                            2402,1004,1106,1602,0204,0306, % 2009/2010  
                            0803,2204,2306,2102,0604,0706, % 2011/2012  
                            1202,2903,3005,0403,1804,1906, % 2013/2014  
                            1702,0304,0406,0902,2503,2605, % 2015/2016  
                            2802,1404,1506,1302,3003,3105, % 2017/2018  
                            0503,1904,2006,2502,1004,1106, % 2019/2020  
                            1602,0204,0306,0103,1504,1606, % 2021/2022  
                            2102,0704,0806,1302,2903,3005, % 2023/2024  
                            0403,1804,1906,1702,0304,0406, % 2025/2026  
                            0902,2603,2705,2902,1404,1506, % 2027/2028  
                            1302,3003,3105,0503,1904,2006, % 2029/2030  
                            2502,1104,1206,1002,2603,2705, % 2031/2032  
                            0103,1504,1606,2102,0704,0806, % 2033/2034  
                            0602,2306,2405,2602,1104,1206);% 2035/2036  
                                                                        
                                                                        
                                                                        
     REAL  ARRAY  D[1:20];                                              
                                                                        
     INTEGER VALUE ARRAY CENTURY (6,4,2,0);                             
                                                                        
     BOOLEAN VALUE ARRAY LEAPYEAR (TRUE,24(TRUE),FALSE,24(TRUE),FALSE,  
                                        24(TRUE),FALSE,24(TRUE));       
                                                                        
     INTEGER  DIAV,  DIA1,  DIA2,  DIA3,   X,    Y,    Z,               
              MESV,  MES1,  MES2,  MES3,   R,   R1,   R2,               
              ANOV,  ANO1,  ANO2,  ANO3,  R3,   R4,   R6,               
                Q1, RESTO,   QTD,     N,   I,   I2,  JAN,               
                A1,    A2,    M2,    D1,  D2, DATE,   R8,               
                M1,     S,  ANOB,    AA;                                
                                                                        
     REAL     DATA1,  DATA3,  DIASAC,  AUXDATA;                         
                                                                        
     LABEL    FIM1;                                                     
                                                                        
     POINTER  PTP,    PTQ,    PTR,    PTS;                              
                                                                        
     BOOLEAN  RESULT, ERRO, DIAUTIL, ACABOU, ANOBI;                     
                                                                        
     TRUTHSET DIGITO  ("0123456789");                                   
                                                                        
     %---------------------------------------------------------------%  
     %               INICIO  DA PROCEDURE  ANOBISSEXTO               %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   ESTA PROCEDURE DEVOLVE PARA A ROTINA SE O ANO SOLICITADO    %  
     %   E UM ANO BISSEXTO.                                          %  
     %                                                               %  
     %---------------------------------------------------------------%  
                                                                        
     BOOLEAN  PROCEDURE  ANOBISSEXTO;                                   
     BEGIN                                                              
       EBCDIC ARRAY AREATRAB[0:7];                                      
       POINTER PTRAB;                                                   
       INTEGER AA;                                                      
                                                                        
       AA:=ANOB;                                                        
       IF (AA MOD 100) = 0 THEN                                         
          BEGIN                                                         
            IF (AA MOD 400) = 0 THEN                                    
               ANOBISSEXTO:=TRUE                                        
            ELSE                                                        
                ANOBISSEXTO:=FALSE                                      
          END                                                           
       ELSE                                                             
           IF (AA MOD 4) = 0 THEN                                       
              ANOBISSEXTO:=TRUE                                         
           ELSE                                                         
               ANOBISSEXTO:=FALSE                                       
     END; % DA PROCEDURE                                                
                                                                        
                                                                        
    %---------------------------------------------------------------%   
    %         INICIO  DA OP[]O 00 (ZERO)     =  DATA DO DIA         %   
    %                                           ANO COM 4 DIGITOS   %   
    %---------------------------------------------------------------%   
    %                                                               %   
    %   1  -  PARAMETRO                                             %   
    %         OP[]O  (2 BYTES)   =  00 (QUATORZE)                   %   
    %                                                               %   
    %   2  -  RETORNO                                               %   
    %         DATA DO DIA        =  DD/MM/AAAA                      %   
    %---------------------------------------------------------------%   
                                                                        
    PROCEDURE DATADIA2;                                                 
    BEGIN                                                               
        ARRAY B[0:0];                                                   
        PTP:=AREAA;                                                     
        B[0]:=TIME(7);                                                  
        REPLACE PTP:PTP       BY B[0].[29:06]  FOR 2 DIGITS;            
        REPLACE PTP:PTP       BY "/";                                   
        REPLACE PTP:PTP       BY B[0].[35:06]  FOR 2 DIGITS;            
        REPLACE PTP:PTP       BY "/";                                   
        REPLACE PTP:PTP       BY B[0].[47:12]  FOR 4 DIGITS;            
        PTR:=OPCONS[2];                                                 
        REPLACE PTR BY "C";                                             
    END;                                                                
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %            OP[]O 01 (UM)     =  VALIDADE DE DATAS             %  
     %                                 ANO COM 4 DIGITOS             %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   1 - PARAMETROS                                              %  
     %       1.1  -  OPCAO (2 BYTES)  = 01;                          %  
     %       1.2  -  DATA             = DDMMAAAA;                    %  
     %                                                               %  
     %   2 - RETORNO                                                 %  
     %       CONS (1 BYTE)  =  "C" (CERTO)  OU  "E"  (ERRADO);       %  
     %---------------------------------------------------------------%  
                                                                        
    PROCEDURE  VALIDATA2;                                               
    BEGIN                                                               
    RESULT:=TRUE;                                                       
    PTQ:=DATAV2;                                                        
    PTP:=AREAA;                                                         
    SCAN  PTQ  FOR  Q1:8  WHILE  IN  DIGITO;                            
    Q1:=8  -  Q1;                                                       
                                                                        
    IF     Q1     EQL   8   THEN                                        
           BEGIN                                                        
           DIAV:=INTEGER (PTQ,2);                                       
           MESV:=INTEGER (PTQ  +  2,2);                                 
           ANOV:=INTEGER (PTQ  +  4,4);                                 
           IF    MESV     LSS    1   OR                                 
                 MESV     GTR    12  OR                                 
                 DIAV     LSS    1   THEN                               
                 RESULT:=FALSE                                          
            ELSE                                                        
            BEGIN                                                       
            IF   (DIAV   GTR  F[MESV]  AND                              
                  MESV   NEQ        2) THEN                             
                  RESULT:=FALSE                                         
            ELSE                                                        
              IF  MESV   EQL        2   THEN                            
                BEGIN                                                   
                IF  DIAV  GTR  F[MESV]  THEN                            
                  BEGIN                                                 
                  ANOB:=ANOV;                                           
                  IF NOT ANOBISSEXTO  OR                                
                       (ANOBISSEXTO  AND                                
                       DIAV     NEQ   29)   THEN                        
                       RESULT:=FALSE;                                   
                   END                                                  
                END                                                     
             END                                                        
           END                                                          
    ELSE                                                                
         RESULT:=FALSE;                                                 
    PTR:=OPCONS[2];                                                     
    IF    NOT  RESULT  THEN                                             
          REPLACE  PTR   BY  "E"                                        
    ELSE                                                                
          REPLACE  PTR  BY  "C";                                        
       END;                                                             
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %        OP[]O  02 (DOIS)    =  VERIFICA O DIA DA SEMANA        %  
     %                               ANO COM 4 DIGITOS               %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   1 - PARAMETROS                                              %  
     %       1.1 - OPCAO (2 BYTES)  =  02;                           %  
     %       1.2 - DATA             =  DDMMAAAA;                     %  
     %       1.3 - FERIADOS MOVEIS  =  DDMM,DDMM,....,ETC.;          %  
     %                                                               %  
     %   2 - RETORNO                                                 %  
     %       2.1 - CONS (1 BYTE) = "C" (CERTO)  OU  "E" (ERRADO);    %  
     %       2.2 - DIA DA SEMANA = DIA UTIL, SABADO , DOMINGO OU     %  
     %                             FERIADO                           %  
     %---------------------------------------------------------------%  
                                                                        
     PROCEDURE  DIASEMANA1;                                             
     BEGIN                                                              
         LABEL  SAISEM;                                                 
         FILL  D[*]  WITH  0101,2104,0105,0709,1210,0211,1511,2512;     
         PTS:=AREAA; PTQ:=DATAV2;                                       
         PTR:=AREAA;                                                    
         REPLACE  PTQ  BY  PTS  FOR  8;                                 
         DIAV:=INTEGER (PTQ,2);                                         
         DIA1:=INTEGER (PTQ,2);                                         
         MESV:=INTEGER (PTQ + 2,2);                                     
         MES1:=INTEGER (PTQ + 2,2);                                     
         ANOV:=INTEGER (PTQ + 4,4);                                     
         ANO1:=INTEGER (PTQ + 4,4);                                     
         ERRO:=FALSE;                                                   
         VALIDATA2;                                                     
         IF   RESULT    THEN                                            
          BEGIN                                                         
              ERRO:=FALSE;                                              
              PTS:=PTS+4;                                               
              S:=8;                                                     
              PTR:=AREAA[8];                                            
              SCAN  PTR  FOR  Q1:52  WHILE IN DIGITO;                   
              Q1:=52  -  Q1  + 1;                                       
              X:=INTEGERT (Q1  /  4);                                   
              IF   X   GTR   10  THEN                                   
              X:=0;                                                     
              THRU   X   DO                                             
              BEGIN                                                     
                  PTS:=PTS + 4;                                         
                  AUXDATA:=INTEGER  (PTS,4);                            
                  REPLACE  PTQ  BY  PTS  FOR  4;                        
                  VALIDATA2;                                            
                  IF  RESULT    THEN                                    
                  BEGIN                                                 
                      S:=S + 1;                                         
                      D[S]:=AUXDATA;                                    
                  END                                                   
                  ELSE                                                  
                  ERRO:=TRUE;                                           
              END                                                       
          END                                                           
         ELSE                                                           
            ERRO:=TRUE;                                                 
                                                                        
         PTP:=AREAA[08];                                                
         X:=X  *  4;                                                    
         PTP:=*  +  X;                                                  
         IF   (ERRO     OR  NOT  RESULT)  THEN                          
              BEGIN                                                     
                  REPLACE   PTP      BY  "INVALIDO";                    
                  GO        TO       SAISEM;                            
              END;                                                      
                                                                        
         R:=ANO1  MOD  400;                                             
         DATE :=C[MES1] + DIA1 - 1;                                     
         ANOB:=R;                                                       
         IF ANOBISSEXTO          THEN         % PODE SER UM ANO BISSEXTO
         IF  LEAPYEAR [R DIV 4]  THEN BEGIN                             
             IF MES1 > 2  THEN                                          
             DIA1:=DIA1 + 1; ANOBI:= TRUE; END;                         
                                                                        
   %     IF R = 0 THEN                        % O ANO E MULTIPLO DE 400 
   %        MES1:=MES1-1;                                               
                                                                        
         JAN:=CENTURY[R DIV 100];                                       
         R:=R MOD 100;                                                  
                                                                        
         IF  R > 0 THEN                                                 
         BEGIN                                                          
             X:= R DIV 4;                                               
             Y:= R MOD 4;                                               
                                                                        
         JAN:=JAN + (X*5) + Y;                                          
                                                                        
         IF Y = 0 THEN                                                  
            JAN:=JAN-1;                                                 
         END;                                                           
                                                                        
         IF JAN < 0 THEN                                                
            JAN:=JAN+7;                                                 
                                                                        
         R:=(DATE+JAN) MOD 7;                                           
         IF ANOBI THEN BEGIN                                            
         IF ANO1 LSS 2000 OR ANO1 EQL 2004 OR ANO1 EQL 2008 OR          
            ANO1 EQL 2012 OR ANO1 EQL 2016 OR ANO1 EQL 2020 OR          
            ANO1 EQL 2024 OR ANO1 EQL 2028 OR ANO1 EQL 2032 OR          
            ANO1 EQL 2036                                               
          THEN                                                          
           IF MES1 > 2                                                  
            THEN                                                        
             BEGIN                                                      
              IF R EQL 6 THEN R:= 0                                     
                         ELSE R:= * + 1;                                
             END                                                        
            ELSE                                                        
          ELSE                                                          
           IF ANO1 EQL 2000                                             
            THEN                                                        
             BEGIN                                                      
              IF MES1 < 3                                               
               THEN                                                     
                IF R EQL 0 THEN R:= 6                                   
                           ELSE R:= * -1;                               
             END; END;                                                  
         IF   R         EQL       5       THEN                          
              REPLACE   PTP       BY      "SABADO "                     
         ELSE                                                           
            IF  R       EQL       6       THEN                          
                REPLACE   PTP       BY    "DOMINGO"                     
            ELSE                                                        
               BEGIN                                                    
                   DIAUTIL:=TRUE;                                       
                   PTQ:=AREAA;                                          
                   AUXDATA:=INTEGER (PTQ,4);                            
                   I:=0;                                                
                   DO                                                   
                        BEGIN                                           
                            I:=I + 1;                                   
                            IF  AUXDATA   EQL       D[I]      THEN      
                                BEGIN                                   
                                    DIAUTIL:=FALSE;                     
                                    I:=99;                              
                                END                                     
                        END                                             
                   UNTIL   I    GTR        S;                           
                   IF    DIAUTIL     THEN                               
                         REPLACE  PTP       BY       "DIA UTIL"         
                   ELSE                                                 
                      REPLACE  PTP       BY       "FERIADO";            
               END;                                                     
         SAISEM:                                                        
     END;                                                               
                                                                        
     %---------------------------------------------------------------%  
     %            OP[]O 03 (TRES)   =   DIFERENCA DE DATAS           %  
     %                                  ANO COM 4 DIGITOS            %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %  1 - PARAMETROS                                               %  
     %      1.1 - OPCAO (2 BYTES)  =  03;                            %  
     %      1.2 - DATA INFERIOR    =  DDMMAAAA;                      %  
     %      1.3 - DATA SUPERIOR    =  DDMMAAAA;                      %  
     %                                                               %  
     %  2 - RETORNO                                                  %  
     %      2.1 - DIFERENCA EM NUMEROS DE DIAS;                      %  
     %      2.2 - DIFERENCA EM ANOS, MESES E DIAS;                   %  
     %---------------------------------------------------------------%  
                                                                        
    PROCEDURE   DIFDATA3;                                               
    BEGIN                                                               
    LABEL  SAIDA2,CALCMES2;                                             
    PTP:=AREAA;                                                         
    PTQ:=DATAV2;                                                        
    REPLACE  PTQ  BY  PTP:PTP  FOR  8;                                  
    DIAV:=INTEGER (PTQ,2);                                              
    MESV:=INTEGER (PTQ + 2,2);                                          
    ANOV:=INTEGER (PTQ + 4,4);                                          
    VALIDATA2;                                                          
    IF     NOT   RESULT    THEN                                         
           BEGIN                                                        
           PTR:=OPCONS[2];                                              
           REPLACE  PTR  BY  "E";                                       
           GO    TO    SAIDA2;                                          
           END;                                                         
    PTP:=AREAA[8];                                                      
    PTQ:=DATAV2;                                                        
    REPLACE  PTQ  BY  PTP  FOR  8;                                      
    DIAV:=INTEGER (PTQ,2);                                              
    MESV:=INTEGER (PTQ + 2,2);                                          
    ANOV:=INTEGER (PTQ + 4,4);                                          
    VALIDATA2;                                                          
    IF     NOT   RESULT   THEN                                          
           BEGIN                                                        
           PTR:=OPCONS[2];                                              
           REPLACE  PTR  BY  "E";                                       
           GO    TO    SAIDA2;                                          
           END;                                                         
    PTP:=AREAA;                                                         
    D1:=DIA1:=INTEGER (PTP,2);                                          
    M1:=Z:=MES1:=INTEGER (PTP  + 2,2);                                  
    A1:=R6:=ANO1:=INTEGER (PTP + 4,4);                                  
    D2:=DIA2:=INTEGER (PTP + 8,2);                                      
    M2:=MES2:=INTEGER (PTP + 10,2);                                     
    A2:=ANO2:=INTEGER (PTP + 12,4);                                     
    IF     ANO1     GTR   ANO2    OR                                    
           (ANO1    EQL   ANO2    AND                                   
            MES1    GTR   MES2)   OR                                    
           (ANO1    EQL   ANO2    AND                                   
            MES1    EQL   MES2    AND                                   
            DIA1    GTR   DIA2)   THEN                                  
           BEGIN                                                        
           PTR:=OPCONS[2];                                              
           REPLACE  PTR  BY  "E";                                       
           GO    TO    SAIDA2;                                          
           END;                                                         
    IF     ANO2  EQL  ANO1   AND                                        
           MES2  EQL  MES1   AND                                        
           DIA2  EQL  DIA1   THEN                                       
           BEGIN                                                        
           DIASAC:=0;                                                   
           R:=0;                                                        
           MES1:=0;                                                     
           DIA1:=0;                                                     
           GO     TO   SAIDA2;                                          
           END;                                                         
                                                                        
    %---------------------------------------------------------------%   
    %             CALCULO   DO   NUMERO    DE   ANOS                %   
    %---------------------------------------------------------------%   
    R:=0;                                                               
    IF     ANO2  GTR  ANO1    THEN                                      
           BEGIN                                                        
           R:=ANO2  -  ANO1;                                            
           IF     R        EQL   1      THEN                            
                  BEGIN                                                 
                  IF    MES2   GTR  MES1    OR                          
                        (MES2  EQL  MES1   AND                          
                        DIA2   GEQ  DIA1) THEN                          
                        GO     TO     CALCMES2                          
                  ELSE                                                  
                        R:=0;                                           
                  END;                                                  
           END;                                                         
                                                                        
   %---------------------------------------------------------------%    
   %             CALCULO   DO   NUMERO    DE   MESES               %    
   %---------------------------------------------------------------%    
   CALCMES2:                                                            
    R2:=0;                                                              
    IF    MES2    GTR   MES1   THEN                                     
          BEGIN                                                         
          R2:=MES2  -  MES1;                                            
          IF   DIA2    LSS   DIA1   THEN                                
               R2:=R2  -  1;                                            
          END                                                           
    ELSE                                                                
          IF   MES1   GTR  MES2   THEN                                  
               BEGIN                                                    
               R:=R6:=ANO2  -  (ANO1  +  1);                            
               R2:=(12  -  MES1)  +  MES2;                              
               IF    DIA2    LSS   DIA1   THEN                          
                     R2:=R2  -  1;                                      
               END;                                                     
   IF     R2     EQL   1      AND                                       
          DIA1   EQL   DIA2  THEN                                       
          BEGIN                                                         
          DIASAC:=F[Z];                                                 
          IF     Z    EQL     2    THEN                                 
                 BEGIN                                                  
                 ANOB:=ANO1;                                            
                 IF    ANOBISSEXTO  THEN                                
                       DIASAC:=*  +  1;                                 
                 END;                                                   
          MES1:=R2;                                                     
%         GO     TO    SAIDA2;                                          
          END;                                                          
    MES1:=R2;                                                           
                                                                        
   %---------------------------------------------------------------%    
   %             CALCULO   DO   NUMERO    DE   DIAS                %    
   %---------------------------------------------------------------%    
   R6:=R4:=DIASAC:=0;                                                   
   IF     DIA2   GTR   DIA1  THEN                                       
          DIASAC:=DIA2  -  DIA1                                         
   ELSE                                                                 
          IF    DIA1   GTR   DIA2  THEN                                 
                BEGIN                                                   
                IF    Z     EQL    MES2  THEN                           
                      BEGIN                                             
                      IF    Z    EQL   1   THEN                         
                            I2:=12                                      
                      ELSE                                              
                            I2:=Z  -  1;                                
                      DIASAC:=(F[I2]  -  DIA1)  +  DIA2;                
                      IF    I2   EQL   2   THEN                         
                            BEGIN                                       
                            ANOB:=ANO2;                                 
                            IF   ANOBISSEXTO THEN                       
                                 DIASAC:=*  +  1;                       
                            END;                                        
                      END                                               
                   ELSE                                                 
                      BEGIN                                             
                        ANOB:=ANO1;                                     
                        IF ANOBISSEXTO THEN                             
                           DIASAC:=(F1[Z] - DIA1)  + DIA2               
                        ELSE                                            
                           DIASAC:=(F[Z]  -  DIA1)  +  DIA2;            
                      END;                                              
                                                                        
                IF   (Z  +  1)  GTR   MES2  THEN                        
                      BEGIN                                             
                      R:=R6:=ANO2  -  (ANO1  +  1);                     
                      MES1:=(MES2  +  12)  -  (Z + 1);                  
                      END                                               
                ELSE                                                    
                      MES1:=MES2  -  (Z  +  1);                         
                END;                                                    
   R4:=DIASAC;                                                          
                                                                        
     %---------------------------------------------------------------%  
     %     CALCULO DOS DIAS ACUMULADOS ENTRE AS DATAS FORNECIDA      %  
     %---------------------------------------------------------------%  
      ANOB:=ANO1;                                                       
      IF ANOBISSEXTO THEN                                               
         BEGIN                                                          
           IF M1  GTR  2  THEN                                          
              A1:=365                                                   
           ELSE                                                         
              A1:=366;                                                  
         END                                                            
      ELSE                                                              
         A1:=365;                                                       
                                                                        
      ANOB:=ANO2;                                                       
      IF ANOBISSEXTO THEN                                               
         A2:=366                                                        
      ELSE                                                              
         A2:=365;                                                       
                                                                        
      IF   ( ANO2 - ANO1 )   EQL   0   THEN                             
           BEGIN                                                        
             DIASAC:=0;                                                 
             IF M2 GTR 2 THEN                                           
             A2:=365;                                                   
             DIASAC:=(A1 - C[M1] - DIA1);                               
             DIASAC:=(DIASAC - (A2 - (C[M2] + DIA2 )));                 
             GO TO SAIDA2;                                              
           END;                                                         
                                                                        
      IF   ( ANO2 - ANO1 )  EQL   1   THEN                              
           BEGIN                                                        
             DIASAC:=0;                                                 
             DIASAC:=(( A1 - C[M1] - DIA1) + (DIA2 + C[M2]));           
             IF A2  EQL   366   AND   M2   GTR   2   THEN               
                DIASAC:= * + 1;                                         
             GO TO SAIDA2;                                              
           END;                                                         
                                                                        
            IF (ANO2 - ANO1)  GTR   1   THEN                            
              BEGIN                                                     
                DIASAC:=0;                                              
                R8:= (ANO2 - ANO1) - 1;                                 
                DIASAC:=((A1 - C[M1] - DIA1) + (DIA2 + C[M2]));         
                IF A2 EQL 366 AND M2 GTR 2 THEN                         
                   DIASAC:= * + 1;                                      
                                                                        
                THRU   R8   DO                                          
                  BEGIN                                                 
                    ANO1:=  *  +  1;                                    
                    ANOB:=ANO1;                                         
                    IF  ANOBISSEXTO THEN                                
                         DIASAC:= * + 366                               
                    ELSE                                                
                         DIASAC:= * + 365;                              
                  END;                                                  
              END;                                                      
  SAIDA2:                                                               
    PTR:=DISP01;                                                        
    REPLACE  PTR  BY  "PROC DIF DE DATAS";                              
    PTP:=AREAA[16];                                                     
    REPLACE  PTP:PTP  BY  DIASAC  FOR  6  DIGITS;                       
    REPLACE  PTP:PTP  BY  R       FOR  2  DIGITS;                       
    REPLACE  PTP:PTP  BY  MES1    FOR  2  DIGITS;                       
    REPLACE  PTP:PTP  BY  R4      FOR  2  DIGITS;                       
    END;                                                                
                                                                        
     %---------------------------------------------------------------%  
     %            OP[]O 04 (QUATRO) =   VERIFICA A DATA FUTURA       %  
     %                                  ANO COM 4 DIGITOS            %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %  1 - PARAMETROS                                               %  
     %      1.1 - OPCAO (2 BYTES)              =  04;                %  
     %      1.2 - DATA                         =  DDMMAAAA;          %  
     %      1.3 - QUANTIDADE DE DIAS (1 WORD)  =  NNNNNN;            %  
     %                                                               %  
     %  2 - RETORNO                                                  %  
     %      1.1 - CONS (1 BYTE)   = "C" (CERTO) OU "E" (ERRADO);     %  
     %      1.2 - DATA FUTURA     = DDMMAAAA;                        %  
     %---------------------------------------------------------------%  
                                                                        
    PROCEDURE   DFUTURA2;                                               
    BEGIN                                                               
    LABEL  SAIFUT2;                                                     
    PTS:=AREAA;                                                         
    PTQ:=DATAV2;                                                        
    REPLACE  PTQ  BY  PTS:PTS  FOR  8;                                  
    VALIDATA2;                                                          
    IF      NOT  RESULT   THEN                                          
            BEGIN                                                       
            PTR:=OPCONS[2];                                             
            REPLACE  PTR  BY  "E";                                      
            GO   TO       SAIFUT2;                                      
            END;                                                        
    SCAN  PTS  FOR  Q1:6  WHILE  IN  DIGITO;                            
    Q1:=6  -  Q1;                                                       
    IF      Q1    NEQ    6   THEN                                       
            BEGIN                                                       
            PTR:=OPCONS[2];                                             
            REPLACE  PTR  BY  "E";                                      
            GO    TO      SAIFUT2;                                      
            END;                                                        
    PTP:=AREAA;                                                         
    DIA1:=INTEGER (PTQ,2);                                              
    MES1:=INTEGER (PTQ + 2,2);                                          
    ANO1:=INTEGER (PTQ + 4,4);                                          
    MES2:=MES1;                                                         
    ANO2:=ANO1;                                                         
    QTD:=INTEGER(PTP + 8,6);                                            
    IF      (QTD + DIA1)   GTR  F[MES1]  THEN                           
            BEGIN                                                       
            R2:=0;                                                      
            R1:=QTD   +  DIA1;                                          
            DO    BEGIN                                                 
                  IF    R1   GTR   F[MES1]  THEN                        
                        BEGIN                                           
                        MES2:=*  +  1;                                  
                        IF     MES2   GTR  12  THEN                     
                               BEGIN                                    
                               ANO2:=ANO2  +  1;                        
                               MES2:=1;                                 
                               END;                                     
                        DIA2:=F[MES2];                                  
                        R1:=R1  -  F[MES1];                             
                        IF   MES1  EQL  2   THEN                        
                             BEGIN                                      
                             ANOB:=ANO2;                                
                             IF    ANOBISSEXTO THEN                     
                                   BEGIN                                
                                     R1:=R1  -  1;                      
                                     DIA2:=29;                          
                                     IF R1 EQL 29   %  OSM-08/10/99     
                                      THEN BRESTO29:= TRUE              
                                      ELSE                              
                                      IF R1 EQL 0                       
                                       THEN MES2:= * - 1;               
                                   END;                                 
                             END;                                       
                         END                                            
                  ELSE                                                  
                        BEGIN                                           
                        DIA2:=R1;                                       
                        R1:=0;                                          
                        END;                                            
                  MES1:=  MES2;                                         
                  END                                                   
                      UNTIL  R1  LEQ  R2;                               
              END                                                       
          ELSE                                                          
              DIA2:=DIA1  +  QTD;                                       
 %  IF   DIA2  EQL  29  AND  MES2  EQL  03  AND NOT BRESTO29            
 %    THEN                                                              
 %       BEGIN                                                          
 %                                                                      
 %       ANOB:=ANO2;                                                    
 %       IF    ANOBISSEXTO  THEN                                        
 %             BEGIN                                                    
 %               MES2:=*  -  1;                                         
 %               DIA2:=29;                                              
 %             END;                                                     
 %       END;                                                           
    PTP:=AREAA[14];                                                     
    REPLACE  PTP:PTP  BY  DIA2  FOR  2  DIGITS;                         
    REPLACE  PTP:PTP  BY  MES2  FOR  2  DIGITS;                         
    REPLACE  PTP:PTP  BY  ANO2  FOR  4  DIGITS;                         
 SAIFUT2:                                                               
    END;                                                                
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %            OP[]O 06 (SEIS)   =   DIFERENCA DE DATAS           %  
     %                                  ANO COM 4 DIGITOS            %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %  1 - PARAMETROS                                               %  
     %      1.1 - OPCAO (2 BYTES)  =  06;                            %  
     %      1.2 - DATA INFERIOR    =  DDMMAAAA;                      %  
     %      1.3 - DATA SUPERIOR    =  DDMMAAAA;                      %  
     %                                                               %  
     %  2 - RETORNO                                                  %  
     %      2.1 - DIFERENCA EM NUMEROS DE DIAS;                      %  
     %      2.2 - DIFERENCA EM ANOS, MESES E DIAS;                   %  
     %---------------------------------------------------------------%  
                                                                        
    PROCEDURE   DIFDATA2;                                               
    BEGIN                                                               
    LABEL  SAIDA2,CALCMES2;                                             
    PTP:=AREAA;                                                         
    PTQ:=DATAV2;                                                        
    REPLACE  PTQ  BY  PTP:PTP  FOR  8;                                  
    DIAV:=INTEGER (PTQ,2);                                              
    MESV:=INTEGER (PTQ + 2,2);                                          
    ANOV:=INTEGER (PTQ + 4,4);                                          
    VALIDATA2;                                                          
    IF     NOT   RESULT    THEN                                         
           BEGIN                                                        
           PTR:=OPCONS[2];                                              
           REPLACE  PTR  BY  "E";                                       
           GO    TO    SAIDA2;                                          
           END;                                                         
    PTP:=AREAA[8];                                                      
    PTQ:=DATAV2;                                                        
    REPLACE  PTQ  BY  PTP  FOR  8;                                      
    DIAV:=INTEGER (PTQ,2);                                              
    MESV:=INTEGER (PTQ + 2,2);                                          
    ANOV:=INTEGER (PTQ + 4,4);                                          
    VALIDATA2;                                                          
    IF     NOT   RESULT   THEN                                          
           BEGIN                                                        
           PTR:=OPCONS[2];                                              
           REPLACE  PTR  BY  "E";                                       
           GO    TO    SAIDA2;                                          
           END;                                                         
    PTP:=AREAA;                                                         
    D1:=DIA1:=INTEGER (PTP,2);                                          
    M1:=Z:=MES1:=INTEGER (PTP  + 2,2);                                  
    A1:=R6:=ANO1:=INTEGER (PTP + 4,4);                                  
    D2:=DIA2:=INTEGER (PTP + 8,2);                                      
    M2:=MES2:=INTEGER (PTP + 10,2);                                     
    A2:=ANO2:=INTEGER (PTP + 12,4);                                     
    IF     ANO1     GTR   ANO2    OR                                    
           (ANO1    EQL   ANO2    AND                                   
            MES1    GTR   MES2)   OR                                    
           (ANO1    EQL   ANO2    AND                                   
            MES1    EQL   MES2    AND                                   
            DIA1    GTR   DIA2)   THEN                                  
           BEGIN                                                        
           PTR:=OPCONS[2];                                              
           REPLACE  PTR  BY  "E";                                       
           GO    TO    SAIDA2;                                          
           END;                                                         
    IF     ANO2  EQL  ANO1   AND                                        
           MES2  EQL  MES1   AND                                        
           DIA2  EQL  DIA1   THEN                                       
           BEGIN                                                        
           DIASAC:=0;                                                   
           R:=0;                                                        
           MES1:=0;                                                     
           DIA1:=0;                                                     
           GO     TO   SAIDA2;                                          
           END;                                                         
                                                                        
     %---------------------------------------------------------------%  
     %             CALCULO   DO   NUMERO    DE   ANOS                %  
     %---------------------------------------------------------------%  
                                                                        
    R:=0;                                                               
    IF     ANO2  GTR  ANO1    THEN                                      
           BEGIN                                                        
           R:=ANO2  -  ANO1;                                            
           IF     R        EQL   1      THEN                            
                  BEGIN                                                 
                  IF    MES2   GTR  MES1    OR                          
                        (MES2  EQL  MES1   AND                          
                        DIA2   GEQ  DIA1) THEN                          
                        GO     TO     CALCMES2                          
                  ELSE                                                  
                        R:=0;                                           
                  END;                                                  
           END;                                                         
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %             CALCULO   DO   NUMERO    DE   MESES               %  
     %---------------------------------------------------------------%  
                                                                        
   CALCMES2:                                                            
    R2:=0;                                                              
    IF    MES2    GTR   MES1   THEN                                     
          BEGIN                                                         
          R2:=MES2  -  MES1;                                            
          IF   DIA2    LSS   DIA1   THEN                                
               R2:=R2  -  1;                                            
          END                                                           
    ELSE                                                                
          IF   MES1   GTR  MES2   THEN                                  
               BEGIN                                                    
               R:=R6:=ANO2  -  (ANO1  +  1);                            
               R2:=(12  -  MES1)  +  MES2;                              
               IF    DIA2    LSS   DIA1   THEN                          
                     R2:=R2  -  1;                                      
               END;                                                     
   IF     R2     EQL   1      AND                                       
          DIA1   EQL   DIA2  THEN                                       
          BEGIN                                                         
          DIASAC:=F[Z];                                                 
          IF     Z    EQL     2    THEN                                 
                 BEGIN                                                  
                 ANOB:=ANO1;                                            
                 IF    ANOBISSEXTO  THEN                                
                       DIASAC:=*  +  1;                                 
                 END;                                                   
          MES1:=R2;                                                     
%         GO     TO    SAIDA2;                                          
          END;                                                          
    MES1:=R2;                                                           
                                                                        
                                                                        
     %---------------------------------------------------------------%  
     %             CALCULO   DO   NUMERO    DE   DIAS                %  
     %---------------------------------------------------------------%  
                                                                        
   R6:=R4:=DIASAC:=0;                                                   
   IF     DIA2   GTR   DIA1  THEN                                       
          DIASAC:=DIA2  -  DIA1                                         
   ELSE                                                                 
          IF    DIA1   GTR   DIA2  THEN                                 
                BEGIN                                                   
                IF    Z     EQL    MES2  THEN                           
                      BEGIN                                             
                      IF    Z    EQL   1   THEN                         
                            I2:=12                                      
                      ELSE                                              
                            I2:=Z  -  1;                                
                      DIASAC:=(F[I2]  -  DIA1)  +  DIA2;                
                      IF    I2   EQL   2   THEN                         
                            BEGIN                                       
                            ANOB:=ANO2;                                 
                            IF   ANOBISSEXTO THEN                       
                                 DIASAC:=*  +  1;                       
                            END;                                        
                      END                                               
                   ELSE                                                 
                      BEGIN                                             
                        ANOB:=ANO1;                                     
                        IF ANOBISSEXTO THEN                             
                           DIASAC:=(F1[Z] - DIA1)  + DIA2               
                        ELSE                                            
                           DIASAC:=(F[Z]  -  DIA1)  +  DIA2;            
                      END;                                              
                                                                        
                IF   (Z  +  1)  GTR   MES2  THEN                        
                      BEGIN                                             
                      R:=R6:=ANO2  -  (ANO1  +  1);                     
                      MES1:=(MES2  +  12)  -  (Z + 1);                  
                      END                                               
                ELSE                                                    
                      MES1:=MES2  -  (Z  +  1);                         
                END;                                                    
   R4:=DIASAC;                                                          
                                                                        
     %---------------------------------------------------------------%  
     %     CALCULO DOS DIAS ACUMULADOS ENTRE AS DATAS FORNECIDA      %  
     %---------------------------------------------------------------%  
                                                                        
      ANOB:=ANO1;                                                       
      IF ANOBISSEXTO THEN                                               
         BEGIN                                                          
           IF M1  GTR  2  THEN                                          
              A1:=365                                                   
           ELSE                                                         
              A1:=366;                                                  
         END                                                            
      ELSE                                                              
         A1:=365;                                                       
                                                                        
      ANOB:=ANO2;                                                       
      IF ANOBISSEXTO THEN                                               
         A2:=366                                                        
      ELSE                                                              
         A2:=365;                                                       
                                                                        
      IF   ( ANO2 - ANO1 )   EQL   0   THEN                             
           BEGIN                                                        
             DIASAC:=0;                                                 
             IF M2 GTR 2 THEN                                           
             A2:=365;                                                   
             DIASAC:=(A1 - C[M1] - DIA1);                               
             DIASAC:=(DIASAC - (A2 - (C[M2] + DIA2 )));                 
             GO TO SAIDA2;                                              
           END;                                                         
                                                                        
      IF   ( ANO2 - ANO1 )  EQL   1   THEN                              
           BEGIN                                                        
             DIASAC:=0;                                                 
             DIASAC:=(( A1 - C[M1] - DIA1) + (DIA2 + C[M2]));           
             IF A2  EQL   366   AND   M2   GTR   2   THEN               
                DIASAC:= * + 1;                                         
             GO TO SAIDA2;                                              
           END;                                                         
                                                                        
            IF (ANO2 - ANO1)  GTR   1   THEN                            
              BEGIN                                                     
                DIASAC:=0;                                              
                R8:= (ANO2 - ANO1) - 1;                                 
                DIASAC:=((A1 - C[M1] - DIA1) + (DIA2 + C[M2]));         
                IF A2 EQL 366 AND M2 GTR 2 THEN                         
                   DIASAC:= * + 1;                                      
                                                                        
                THRU   R8   DO                                          
                  BEGIN                                                 
                    ANO1:=  *  +  1;                                    
                    ANOB:=ANO1;                                         
                    IF  ANOBISSEXTO THEN                                
                         DIASAC:= * + 366                               
                    ELSE                                                
                         DIASAC:= * + 365;                              
                  END;                                                  
              END;                                                      
  SAIDA2:                                                               
    PTR:=DISP01;                                                        
    REPLACE  PTR  BY  "PROC DIF DE DATAS";                              
    PTP:=AREAA[16];                                                     
    REPLACE  PTP:PTP  BY  DIASAC  FOR  8  DIGITS;                       
    REPLACE  PTP:PTP  BY  R       FOR  4  DIGITS;                       
    REPLACE  PTP:PTP  BY  MES1    FOR  2  DIGITS;                       
    REPLACE  PTP:PTP  BY  R4      FOR  2  DIGITS;                       
    END;                                                                
                                                                        
     %---------------------------------------------------------------%  
     %      OP[]O 08 (TRES)   =   VERIFICA QUAL E O DIA DA SEMANA    %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   1 - PARAMETROS                                              %  
     %       1.1 - OPCAO (2 BYTES)    =   08;                        %  
     %       1.2 - DATA               =   DDMMAAAA;                  %  
     %       1.3 - FERIADOS MOVEIS    =   DDMM,DDMM,....,ETC.;       %  
     %                                                               %  
     %   2 - RETORNO                                                 %  
     %       2.1 - CONS (1 BYTE)  =  "C" (CERTO)  OU  "E" (ERRADO);  %  
     %       2.2 - DIA DA SEMANA  =  SEGUNDA, TERCA, QUARTA, QUINTA, %  
     %                               SEXTA, SABADO  E DOMINGO        %  
     %---------------------------------------------------------------%  
                                                                        
    PROCEDURE   DSEMANA2;                                               
    BEGIN                                                               
    DIASEMANA1;                                                         
    IF   R         EQL       0       THEN                               
         REPLACE   PTP       BY      "SEGUNDA "                         
    ELSE                                                                
      IF  R       EQL       1       THEN                                
          REPLACE   PTP       BY    "TER[A    "                         
      ELSE                                                              
      IF  R       EQL       2       THEN                                
          REPLACE   PTP       BY    "QUARTA   "                         
      ELSE                                                              
      IF  R       EQL       3       THEN                                
          REPLACE   PTP       BY    "QUINTA   "                         
      ELSE                                                              
      IF  R       EQL       4       THEN                                
          REPLACE   PTP       BY    "SEXTA    ";                        
    END;                                                                
                                                                        
     %---------------------------------------------------------------%  
     %   OP[]O 09 (NOVE)  =   VERIFICA QUAL E O DIA DA SEMANA        %  
     %                        UTILIZADA PELO TRIBUNAL DE JUSTI[A     %  
     %                        ANO COM 4  DIGITOS                     %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %   1 - PARAMETROS                                              %  
     %       1.1 - OPCAO (2 BYTES)  =   09;                          %  
     %       1.2 - DATA             =   DDMMAAAA;                    %  
     %                                                               %  
     %   2 - RETORNO                                                 %  
     %       2.1 - CONS (1 BYTE)    =  "C" (CERTO)  OU  "E" (ERRADO);%  
     %       2.2 - DIA DA SEMANA    =  DIA UTIL, SABADO , DOMINGO OU %  
     %                                 FERIADO                       %  
     %---------------------------------------------------------------%  
                                                                        
   PROCEDURE  DSEMANA4;                                                 
   BEGIN                                                                
   LABEL  SAI04;                                                        
   FILL  D[*]  WITH  % FERIADOS FIXOS                                   
               0101,2501,2104,0105,0907,0709,1210,2810,0211,1511,2512;  
   PTS:=AREAA; PTQ:=DATAV2;                                             
   PTR:=AREAA;                                                          
   REPLACE  PTQ  BY  PTS  FOR  8;                                       
   DIAV:=INTEGER (PTQ,2);                                               
   DIA1:=INTEGER (PTQ,2);                                               
   MESV:=INTEGER (PTQ + 2,2);                                           
   MES1:=INTEGER (PTQ + 2,2);                                           
   ANOV:=INTEGER (PTQ + 4,4);                                           
   ANO1:=INTEGER (PTQ + 4,4);                                           
   VALIDATA2;                                                           
   PTP:=AREAA[08];                                                      
   IF    NOT  RESULT   THEN                                             
         BEGIN                                                          
         REPLACE   PTP      BY  "INVALIDO";                             
         GO        TO       SAI04;                                      
         END;                                                           
   ERRO:=FALSE;                                                         
   IF    RESULT    THEN                                                 
         BEGIN                                                          
         IF    ANO1    LSS  1983  OR                                    
               ANO1    GTR  2032  THEN                                  
               ERRO:=TRUE                                               
         ELSE                                                           
           IF  ANO1    EQL  1983  THEN                                  
               Q1:=1                                                    
           ELSE                                                         
                Q1:=((ANO1 - 1983) * 3) + 1;                            
         END                                                            
    ELSE                                                                
          ERRO:=TRUE;                                                   
    D[12]:=FER[Q1];  % CARNAVAL                                         
    R6:=Q1+1;                                                           
    D[13]:=FER[R6];  % SEXTA FEIRA DA PAIXAO                            
    R6:=Q1+2;                                                           
    D[14]:=FER[R6];  % CORPUS CRISTI                                    
    IF    (ERRO     OR  NOT  RESULT)  THEN                              
          BEGIN                                                         
          REPLACE   PTP      BY  "INVALIDO";                            
          GO        TO       SAI04;                                     
          END;                                                          
                                                                        
    %VERIFICA SE E ANO BISSEXTO                                         
                                                                        
    R:=ANO1  MOD  400;  % A CADA 400 ANOS O CALENDARIO SE REPETE        
                                                                        
    DATE:=C[MES1]+DIA1-1; %NUMERO DE DIAS DE 1 DE JANEIRO ATE O DIA     
                          %SOLICITADO                                   
    ANOB:=R;                                                            
    IF    ANOBISSEXTO   THEN                                            
          IF LEAPYEAR [R DIV 4] THEN BEGIN                              
          IF  MES1 > 2 THEN                                             
          DIA1:=DIA1 + 1; ANOBI:= TRUE; END;                            
                                                                        
 %  IF  R = 0 THEN % O ANO E MULTIPLO DE 400                            
 %     MES1:=MES1-1;                                                    
                                                                        
    JAN:=CENTURY[ R DIV 100];                                           
    R:=R MOD 100;                                                       
                                                                        
    IF R > 0 THEN                                                       
       BEGIN                                                            
                                                                        
       X:= R DIV 4;                                                     
       Y:= R MOD 4;                                                     
                                                                        
       JAN := JAN + (X*5) + Y;                                          
                                                                        
       IF Y = 0 THEN JAN:=JAN-1;                                        
       END;                                                             
       IF JAN < 0 THEN JAN:=JAN + 7;                                    
       DATE := (DATE+JAN) MOD 7;                                        
                                                                        
      S:=14;                                                            
      IF ANOBI THEN BEGIN                                               
       IF ANO1 LSS 2000 OR ANO1 EQL 2004 OR ANO1 EQL 2008 OR            
          ANO1 EQL 2012 OR ANO1 EQL 2016 OR ANO1 EQL 2020 OR            
          ANO1 EQL 2024 OR ANO1 EQL 2028 OR ANO1 EQL 2032 OR            
          ANO1 EQL 2036                                                 
        THEN                                                            
         IF MES1 > 2                                                    
          THEN                                                          
           BEGIN                                                        
            IF DATE EQL 6 THEN DATE:= 0                                 
                       ELSE DATE:= * + 1;                               
           END                                                          
          ELSE                                                          
        ELSE                                                            
         IF ANO1 EQL 2000                                               
          THEN                                                          
           BEGIN                                                        
            IF MES1 < 3                                                 
             THEN                                                       
              IF DATE EQL 0 THEN DATE:= 6                               
                         ELSE DATE := * -1;                             
           END; END;                                                    
                                                                        
      IF   DATE      EQL       5       THEN                             
           REPLACE   PTP       BY      "SABADO "                        
      ELSE                                                              
                                                                        
      IF   DATE    EQL       6         THEN                             
           REPLACE   PTP       BY      "DOMINGO"                        
      ELSE                                                              
          BEGIN                                                         
          DIAUTIL:=TRUE;                                                
          PTQ:=AREAA;                                                   
          AUXDATA:=INTEGER (PTQ,4);                                     
          I:=0;                                                         
          DO   BEGIN                                                    
               I:=I + 1;                                                
               IF  AUXDATA   EQL       D[I]      THEN                   
                   BEGIN                                                
                   DIAUTIL:=FALSE;                                      
                   I:=99;                                               
                   END                                                  
               END                                                      
                   UNTIL   I    GTR        S;                           
         IF    DIAUTIL     THEN                                         
               BEGIN                                                    
               IF  DATE      EQL       0       THEN                     
                   REPLACE   PTP       BY      "SEGUNDA "               
               ELSE                                                     
               IF  DATE      EQL       1       THEN                     
                   REPLACE   PTP       BY    "TER[A    "                
               ELSE                                                     
               IF  DATE      EQL       2       THEN                     
                   REPLACE   PTP       BY    "QUARTA   "                
               ELSE                                                     
               IF  DATE      EQL       3       THEN                     
                   REPLACE   PTP       BY    "QUINTA   "                
               ELSE                                                     
               IF  DATE      EQL       4       THEN                     
                   REPLACE   PTP       BY    "SEXTA    ";               
               END                                                      
         ELSE                                                           
               REPLACE  PTP       BY       "FERIADO";                   
          END;                                                          
  SAI04:                                                                
    END;                                                                
                                                                        
     %---------------------------------------------------------------%  
     %          OP[]O 11 (ONZE)      =  SUBTRAI ANOS, MESES E DIAS   %  
     %                                  ANO COM 4 DIGITOS            %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %  1 - PARAMETROS                                               %  
     %      1.1 - OPCAO (2 BYTES)           =  11                    %  
     %      1.2 - DATA INFORMADA            =  DDMMAAAA;             %  
     %      1.3 - QTDE DE DIAS,MESES E ANOS =  DDMMAAAA;             %  
     %                                                               %  
     %  2 - RETORNO                                                  %  
     %      2.1 - C = CERTO;                                         %  
     %      2.2 - E = ERRADO;                                        %  
     %---------------------------------------------------------------%  
                                                                        
     PROCEDURE  SUBTRDATA1;                                             
     BEGIN                                                              
       LABEL  SAIDA,RESP;                                               
       PTP:=AREAA[8];                                                   
       PTQ:=DATAV2;                                                     
       REPLACE  PTQ  BY  PTP  FOR  8;                                   
                                                                        
       DIAV:=DIA1:=INTEGER (PTQ ,2);                                    
       MESV:=MES1:=INTEGER (PTQ + 2,2);                                 
       ANOV:=ANO1:=INTEGER (PTQ + 4,4);                                 
       SCAN  PTQ  FOR  Q1:8  WHILE  IN  DIGITO;                         
       Q1:=8  -  Q1;                                                    
       IF     Q1     EQL   8   THEN                                     
              BEGIN                                                     
              IF  MES1  GTR      12     OR                              
                  DIA1  GTR      31     OR                              
                  ANO1  GTR      ANOV   THEN                            
                  BEGIN                                                 
                  PTR:=OPCONS[2];                                       
                  REPLACE  PTR  BY  "E";                                
                  GO    TO    SAIDA;                                    
                  END;                                                  
              END;                                                      
       PTP:=AREAA;                                                      
       PTQ:=DATAV2;                                                     
                                                                        
       REPLACE  PTQ  BY  PTP  FOR  8;                                   
                                                                        
       DIAV:=INTEGER (PTQ ,2);                                          
       ANOV:=INTEGER (PTQ + 4,4);                                       
       MESV:=INTEGER (PTQ + 2,2);                                       
                                                                        
                                                                        
       VALIDATA2;                                                       
       IF     NOT   RESULT    THEN                                      
              BEGIN                                                     
              PTR:=OPCONS[2];                                           
              REPLACE  PTR  BY  "E";                                    
              GO    TO    SAIDA;                                        
              END;                                                      
       ANO3:=ANOV  -  ANO1;                                             
                                                                        
                                                                        
       IF      MESV   GTR   MES1     THEN                               
               MES3:=MESV   -   MES1                                    
       ELSE                                                             
               BEGIN                                                    
               ANO3:=ANO3   -   1;                                      
               MES3:=MESV   +   12;                                     
               MES3:=MES3   -   MES1;                                   
               END;                                                     
       IF      DIA1   EQL   0        THEN                               
               BEGIN                                                    
               DIA3:=DIAV;                                              
               IF     DIA3     GTR  F[MES3]   THEN                      
                      DIA3:=F[MES3];                                    
               ANOB:=ANO3;                                              
               IF   ANOBISSEXTO      THEN                               
                      DIA3:=DIA3   +    1;                              
               GO     TO    RESP;                                       
               END;                                                     
       IF      DIA1   GEQ   F[MES3]    THEN                             
         IF    MES3    NEQ   2             THEN                         
               BEGIN                                                    
               PTR:=OPCONS[2];                                          
               REPLACE  PTR  BY  "E";                                   
               GO    TO    SAIDA;                                       
               END                                                      
         ELSE                                                           
               BEGIN                                                    
               ANOB:=ANO3;                                              
               IF  ANOBISSEXTO         THEN                             
                   BEGIN                                                
                   IF   DIA1    GEQ   29    THEN                        
                        BEGIN                                           
                        PTR:=OPCONS[2];                                 
                        REPLACE  PTR  BY  "E";                          
                        GO    TO    SAIDA;                              
                        END;                                            
                   END;                                                 
               END;                                                     
       IF      DIAV   EQL   F[MESV]   AND MESV EQL 02 THEN              
               BEGIN                                                    
               DIAV:=F[MES3];                                           
               ANOB:=ANO3;                                              
               IF    ANOBISSEXTO       THEN                             
                     DIAV:=DIAV   +    1;                               
               END;                                                     
       IF      DIAV   GTR   DIA1     THEN                               
               DIA3:=DIAV   -   DIA1                                    
       ELSE                                                             
               BEGIN                                                    
               MES3:=MES3   -  1;                                       
               IF  MES3   EQL   0    THEN                               
                   BEGIN                                                
                   ANO3:=ANO3  -   1;                                   
                   MES3:=12;                                            
                   END;                                                 
               DIA3:=(F[MES3]  +  DIAV)  -  DIA1;                       
               IF  MES3   EQL   2    THEN                               
                   BEGIN                                                
                   ANOB:=ANO3;                                          
                   IF    ANOBISSEXTO        THEN                        
                         DIA3:=DIA3  +  1;                              
                   END;                                                 
               END;                                                     
     RESP:                                                              
       PTP:=AREAA[0];                                                   
       REPLACE    PTP:PTP   BY  DIA3  FOR  2  DIGITS;                   
       REPLACE    PTP:PTP   BY  MES3  FOR  2  DIGITS;                   
       REPLACE    PTP:PTP   BY  ANO3  FOR  4  DIGITS;                   
       PTQ:=OPCONS[2];                                                  
       REPLACE    PTQ       BY  "C";                                    
       PTP:=AREAA[0];                                                   
       SAIDA:                                                           
       END;                                                             
                                                                        
     %---------------------------------------------------------------%  
     %            OP[]O 12 (DOZE)   =   VERIFICA DATA PASSADA        %  
     %                                  ANO COM 4 DIGITOS            %  
     %---------------------------------------------------------------%  
     %                                                               %  
     %  1 - PARAMETROS                                               %  
     %      1.1 - OPCAO (2 BYTES)              =  12;                %  
     %      1.2 - DATA                         =  DDMMAAAA;          %  
     %      1.3 - QUANTIDADE DE DIAS (1 WORD)  =  NNNNNN;            %  
     %                                                               %  
     %  2 - RETORNO                                                  %  
     %      1.1 - CONS (1 BYTE)   = "C" (CERTO) OU "E" (ERRADO);     %  
     %      1.2 - DATA PASSADA    = DDMMAAAA;                        %  
     %---------------------------------------------------------------%  
                                                                        
    PROCEDURE   DPASSADA2;                                              
    BEGIN                                                               
    LABEL  SAIPAS2;                                                     
    PTS:=AREAA;                                                         
    PTQ:=DATAV2;                                                        
    REPLACE  PTQ  BY  PTS:PTS  FOR  8;                                  
    VALIDATA2;                                                          
    IF      NOT  RESULT   THEN                                          
            BEGIN                                                       
            PTR:=OPCONS[2];                                             
            REPLACE  PTR  BY  "E";                                      
            GO   TO       SAIPAS2;                                      
            END;                                                        
    SCAN  PTS  FOR  Q1:6  WHILE  IN  DIGITO;                            
    Q1:=6  -  Q1;                                                       
    IF      Q1    NEQ    6   THEN                                       
            BEGIN                                                       
            PTR:=OPCONS[2];                                             
            REPLACE  PTR  BY  "E";                                      
            GO    TO      SAIPAS2;                                      
            END;                                                        
    PTP:=AREAA;                                                         
    DIA1:=INTEGER (PTQ,2);                                              
    MES1:=INTEGER (PTQ + 2,2);                                          
    ANO1:=INTEGER (PTQ + 4,4);                                          
    MES3:=MES2:=MES1;                                                   
    ANO3:=ANO2:=ANO1;                                                   
    QTD:=INTEGER(PTP + 8,6);                                            
    IF      QTD     GEQ    DIA1   THEN                                  
            BEGIN                                                       
            R2:=0;                                                      
            MES2:=*  -  1;                                              
            IF     MES2   EQL   0  THEN                                 
                   BEGIN                                                
                   ANO2:=ANO2  -  1;                                    
                   MES2:=12;                                            
                   END;                                                 
            IF     MES1  EQL  2   THEN                                  
                   BEGIN                                                
                   ANOB:=ANO2;                                          
                   IF    ANOBISSEXTO  THEN                              
                         R1:=R1  -  1;                                  
                   END;                                                 
            R1:=QTD - DIA1;                                             
            MES1:=MES2;                                                 
            DO    BEGIN                                                 
                  IF    R1   GEQ   F[MES2]  THEN                        
                        BEGIN                                           
                        MES2:=*  -  1;                                  
                        IF     MES2   EQL   0  THEN                     
                               BEGIN                                    
                               ANO2:=ANO2  -  1;                        
                               MES2:=12;                                
                               END;                                     
                        DIA2:=F[MES2];                                  
                        R1:=R1 - F[MES1];                               
                        IF   MES1  EQL  2   THEN                        
                             BEGIN                                      
                             ANOB:=ANO2;                                
                             IF   ANOBISSEXTO   THEN                    
                                   R1:=R1  -  1;                        
                             END;                                       
                         END                                            
                  ELSE                                                  
                        BEGIN                                           
                        DIA2:=F[MES2] - R1;                             
                        IF   MES2  EQL  2   THEN                        
                             BEGIN                                      
                             ANOB:=ANO2;                                
                             IF    ANOBISSEXTO THEN                     
                                   DIA2:=*  +  1;                       
                             END;                                       
                        R1:=0;                                          
                        END;                                            
                  MES1 := MES2;                                         
                  END                                                   
                      UNTIL  R1  LEQ  R2;                               
              END                                                       
          ELSE                                                          
              DIA2:=DIA1  -  QTD;                                       
    PTP:=AREAA[00];                                                     
    REPLACE  PTP:PTP  BY  DIA2  FOR  2  DIGITS;                         
    REPLACE  PTP:PTP  BY  MES2  FOR  2  DIGITS;                         
    REPLACE  PTP:PTP  BY  ANO2  FOR  4  DIGITS;                         
    SAIPAS2:                                                            
    END;                                                                
                                                                        
                                                                        
    %-----------------------------------------------------------------% 
    %   L O G I C A      P R I N C I P A L    -    C A L C D A T A 3  % 
    %-----------------------------------------------------------------% 
                                                                        
    BEGIN                                                               
    PTR:=OPCONS;                                                        
    N:=INTEGER (PTR,2);                                                 
    IF    N        GTR  16  THEN                                        
          BEGIN                                                         
           PTR:=OPCONS[2];                                              
           REPLACE PTR BY "E";                                          
           GO TO FIM1;                                                  
          END;                                                          
                                                                        
    IF    N        EQL  1  THEN                                         
          BEGIN                                                         
          PTP:=AREAA;                                                   
          PTQ:=DATAV2;                                                  
          REPLACE  PTQ  BY  PTP  FOR  8;                                
          END;                                                          
                                                                        
    IF    N        EQL  5  THEN                                         
          BEGIN                                                         
          PTP:=AREAA;                                                   
          PTQ:=DATAV2;                                                  
          REPLACE  PTQ  BY  PTP  FOR  8;                                
          END;                                                          
                                                                        
                                                                        
    CASE  N  OF  BEGIN                                                  
                   DATADIA2;      %00                                   
                   VALIDATA2;     %01                                   
                   DIASEMANA1;    %02                                   
                   DIFDATA3;      %03                                   
                   DFUTURA2;      %04                                   
                   VALIDATA2;     %05                                   
                   DIFDATA2;      %06                                   
                   DFUTURA2;      %07                                   
                   DSEMANA2;      %08                                   
                   DSEMANA4;      %09                                   
                   DSEMANA4;      %10                                   
                   SUBTRDATA1;    %11                                   
                   DPASSADA2;     %12                                   
                   DPASSADA2;     %13                                   
                   DATADIA2;      %14                                   
                   DIASEMANA1;    %15                                   
                   SUBTRDATA1;    %16                                   
                 END                                                    
    END;                                                                
   FIM1:                                                                
END OF CALCDATA3;                                                       
                                                                        
                                                                        
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %                                                                    %
  %                    G R E G _ T O _ J U L I A N                     %
  %                                                                    %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                                        
  PROCEDURE GREG_TO_JULIAN (PARAM);                                     
  EBCDIC ARRAY PARAM [0];                                               
  BEGIN                                                                 
    INTEGER MM, DD, YYYY,                                               
            GREG_DATE,                                                  
            JULIAN_DATE;                                                
                                                                        
    BOOLEAN INVALID_DATE,                                               
            LEAP_YEAR;                                                  
                                                                        
    DEFINE GREGDATE   = PARAM [00]#,                                    
           JULIANDATE = PARAM [08]#,                                    
           RETORNO    = PARAM [15]#;                                    
                                                                        
    VALUE ARRAY MONTH_VALUES (0, 31, 59, 90, 120, 151, 181,             
                              212, 243, 273, 304, 334, 365);            
                                                                        
    GREG_DATE:= INTEGER (GREGDATE,8);                                   
                                                                        
    MM  := GREG_DATE DIV 1000000;                                       
    DD  := GREG_DATE MOD 1000000 DIV 10000;                             
    YYYY:= GREG_DATE MOD 10000;                                         
                                                                        
%%  DISPLAY("MM= " CAT STRING(MM,*));                                   
%%  DISPLAY("DD= " CAT STRING(DD,*));                                   
%%  DISPLAY("YY= " CAT STRING(YYYY,*));                                 
                                                                        
                                                                        
    LEAP_YEAR:= YYYY NEQ 000 AND           % ANO 2000,     E" BISEXTO   
                YYYY MOD 4 = 0;            % =0, ANO BISEXTO            
                                                                        
    INVALID_DATE:= YYYY <    0 OR                                       
                   YYYY > 9999 OR                                       
                   DD LEQ 0;                                            
                                                                        
    IF NOT INVALID_DATE THEN                                            
       CASE MM OF                                                       
         BEGIN                                                          
           1: 3: 5: 7: 8: 10: 12:                                       
             INVALID_DATE:= DD > 31; % DISPLAY("DD > 31");              
           4: 6: 9: 11:                                                 
             INVALID_DATE:= DD > 30; % DISPLAY("DD > 30");              
           2:                                                           
             INVALID_DATE:= IF LEAP_YEAR THEN                           
                                DD > 29                                 
                            ELSE                                        
                                DD > 28;                                
           ELSE:                                                        
               INVALID_DATE:= TRUE;                                     
         END OF CASE ON MONTH;                                          
                                                                        
    IF NOT INVALID_DATE THEN                                            
       BEGIN                                                            
         JULIAN_DATE:= YYYY * 1000                                      
                     + MONTH_VALUES [MM - 1]                            
                     + DD;                                              
                                                                        
         IF MM > 2 AND LEAP_YEAR THEN                                   
            JULIAN_DATE:= * + 1;                                        
                                                                        
         REPLACE JULIANDATE BY JULIAN_DATE FOR 7 DIGITS;                
         REPLACE RETORNO    BY "0"         FOR 1;   % DATA CORRETA      
       END                                                              
    ELSE                                                                
        BEGIN                                                           
          REPLACE JULIANDATE BY "0" FOR 7;                              
          REPLACE RETORNO    BY "1" FOR 1;          % DATA ERRADA       
        END;                                                            
                                                                        
  END OF PROCEDURE GREG_TO_JULIAN;                                      
                                                                        
                                                                        
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  %                                                                    %
  %                      J U L I A N _ T O _ G R E G                   %
  %                                                                    %
  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                                        
  PROCEDURE JULIAN_TO_GREG (PARAM);                                     
  EBCDIC ARRAY PARAM [0];                                               
  BEGIN                                                                 
    INTEGER MM, DD, YYYY, DDD,                                          
            GREG_DATE,                                                  
            JULIAN_DATE;                                                
                                                                        
    BOOLEAN INVALID_DATE,                                               
            LEAP_YEAR;                                                  
                                                                        
    DEFINE GREGDATE   = PARAM [00]#,                                    
           JULIANDATE = PARAM [08]#,                                    
           RETORNO    = PARAM [15]#;                                    
                                                                        
    VALUE ARRAY MONTH_VALUES (0, 31, 59, 90, 120, 151, 181,             
                              212, 243, 273, 304, 334, 365);            
                                                                        
    JULIAN_DATE:= INTEGER (JULIANDATE,7);                               
                                                                        
    YYYY:= JULIAN_DATE DIV 1000;                                        
    DDD := JULIAN_DATE MOD 1000;                                        
                                                                        
    LEAP_YEAR:= YYYY NEQ 00 AND           % ANO 2000, NAO E" BISEXTO    
                YYYY MOD 4 = 0;           % =0, ANO BISEXTO             
                                                                        
    INVALID_DATE:= YYYY <    0 OR                                       
                   YYYY > 9999 OR                                       
                   DDD LEQ 0;                                           
                                                                        
    IF NOT INVALID_DATE THEN                                            
       INVALID_DATE:= IF LEAP_YEAR THEN                                 
                          DDD > 366                                     
                      ELSE                                              
                          DDD > 365;                                    
                                                                        
    IF NOT INVALID_DATE THEN                                            
       BEGIN                                                            
         IF LEAP_YEAR THEN                                              
             FOR MM:= 1 STEP 1 WHILE DDD > MONTH_VALUES[MM] + 1 DO      
         ELSE                                                           
             FOR MM:= 1 STEP 1 WHILE DDD > MONTH_VALUES[MM] DO;         
                                                                        
         IF LEAP_YEAR AND MM > 2 THEN                                   
             DD:= DDD - MONTH_VALUES[MM - 1] - 1                        
         ELSE                                                           
             DD:= DDD - MONTH_VALUES[MM - 1];                           
                                                                        
         GREG_DATE:= MM * 1000000                                       
                   + DD * 10000                                         
                   + YYYY;                                              
                                                                        
         REPLACE GREGDATE BY GREG_DATE FOR 8 DIGITS;                    
         REPLACE RETORNO  BY "0"       FOR 1;       % DATA CORRETA      
       END                                                              
    ELSE                                                                
        BEGIN                                                           
          REPLACE GREGDATE BY "0" FOR 8;                                
          REPLACE RETORNO  BY "1" FOR 1;            % DATA ERRADA       
        END;                                                            
                                                                        
  END OF PROCEDURE JULIAN_TO_GREG;                                      
                                                                        
                                                                        
                                                                        
EXPORT DATAEX,                                                          
       DATAEX72,                                                        
       DATACOMP,                                                        
       SUBTDATA,                                                        
       SUBTDATA2,                                                       
       CALCDATA2,                                                       
       CALCDATA3,                                                       
       GREG_TO_JULIAN,                                                  
       JULIAN_TO_GREG;                                                  
                                                                        
FREEZE (TEMPORARY);                                                     
END.                                                                    
