 $SET SHARING=SHAREDBYALL                                               
%-----------------------------------------------------------------------
%  LIBRARY :  PF/LIB/DIGITCHECK/000                                     
%             PC/LIB/DIGITCHECK                                         
%                                                                       
%  ESTA LIBRARY FOI GERADA PARA SUBSTITUIR AS ROTINAS: - DIGITPASEP     
%                                                      - DIGITCGC       
%                                                      - DIGITCPF       
%                                                      - DIGITM10       
%                                                      - DIGITM11       
%                                                        DIGITM114      
%                                                        DIGITM115      
%                                                      - DIGITCID       
%                                                                       
%-----------------------------------------------------------------------
%  OBS.: COMPILAR:  A18  ->  FREEZE (PERMANENT);                        
%                   NX   ->  FREEZE (TEMPORARY);                        
%                                                                       
%-----------------------------------------------------------------------
%  ALTERACOES:                                                          
%  30/07/92 - TEMPORARY PARA PERMANENT. CODIGO GERADO SO NO A5.    OSMAR
%  06/12/95 - DIGITRENACH, CRIADO A PARTIR DA DIGITM11.           AILTON
%  03/06/96 - DIGITIPVA21, CRIADO A PARTIR DA DIGITM10.           AILTON
% 004  26/12/96 - DIGITIPVA, CRIADO A PARTIR DA DIGITIPVA21, COM        
%                 44 POSICOES.                                      AHM 
% 005  28/07/98 - INCLUSAO DIGITSEDEX, A PEDIDO DO EPV.             AHM 
%                                                                       
% 008  29/05/19 - CRIADA A DIGITCERTID. GERA OU VALIDA O DC DA          
%                 CERTIDAO DE MATRICULA DE CARTORIO CIVIL.              
%                 SOLICITACAO DO PAULO EPV/MARCIA ZANOLO. (OSM)         
%                                                                       
% 008  18/06/19 - INCLUIDA A DOCUMENTACAO DA ROTINA DIGITCERTID. (OSM)  
%                                                                       
% 009  15/08/19 - INCLUSAO DIGITITULO GERA OU VALIDA O DC DO TIULO DE   
%                 ELEITOR COM 8 OU 9 DIGITOS.                           
%                 A PEDIDO DO EPV/MARCIA ZANOLO. (OSM)                  
%                 IMPLANTADA NA PRODUCAO EM 17/09/2019.                 
%                                                                       
%                                                                       
%                                                                       
%                                                                       
%-----------------------------------------------------------------------
 $PAGE                                                                  
BEGIN                                                                   
%-----------------------------------------------------------------------
%  INICIO DA LIBRARY:  DIGITPASEP                                       
%                                                                       
%  LIBRARY CRIADA EM 16/07/86. A PARTIR DO FONTE: PF/SUB/DIGITPASEP/001 
%                                                                       
%-----------------------------------------------------------------------
  PROCEDURE DIGITPASEP(A);                                              
  EBCDIC ARRAY A[0];                                                    
  BEGIN                                                                 
    POINTER PA; LABEL EXIT; INTEGER COUNT,ACUM,I;                       
    TRUTHSET NUMERO("0123456789");                                      
    PA:=A;                                                              
    %===============================================================%   
    %   CONSISTENCIA DO NUMERO DO PASEP EM CASO DE ERRO DEVOLVE :   %   
    %   "1" => CAMPO N]O NUMERICO                                   %   
    %===============================================================%   
    COUNT:=10;                                                          
    SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                         
    IF COUNT NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE A[11] BY "1" ; GO TO EXIT;                             
       END;                                                             
    %================================================================%  
    %   CONSISTENCIA DO PRIMEIRO DIGITO, EM CASO DE ERRO DEVOLVE :   %  
    %   "2" => PRIMEIRO DIGITO NAO E "1"                             %  
    %================================================================%  
    IF A[0] NEQ "1" AND A[0] NEQ "2"                                    
      THEN                                                              
       BEGIN                                                            
         REPLACE A[11] BY "2" ; GO TO EXIT;                             
       END;                                                             
    %====================================================%              
    %   CALCULO DO DIGIT CHECK E VERIFICACAO DO DIGITO   %              
    %====================================================%              
    ACUM:=ACUM + 3*INTEGER(A[0],1)+2*INTEGER(A[1],1)+9*INTEGER(A[2],1)+ 
                 8*INTEGER(A[3],1)+7*INTEGER(A[4],1)+6*INTEGER(A[5],1)+ 
                 5*INTEGER(A[6],1)+4*INTEGER(A[7],1)+3*INTEGER(A[8],1)+ 
                 2*INTEGER(A[9],1);                                     
    I:=IF ACUM MOD 11 = 0 THEN 0                                        
    ELSE                                                                
        11-(ACUM MOD 11);                                               
    %===========================================================%       
    %   QDO A DIFERENCA FOR 10, O NUMERO DO PASEP E" INVALIDO   %       
    %===========================================================%       
    IF I = 10 THEN                                                      
       BEGIN                                                            
         REPLACE A[11] BY "3"; GO TO EXIT;                              
       END;                                                             
    IF I NEQ INTEGER(A[10],1) THEN                                      
       REPLACE A[11] BY "4"                                             
    ELSE                                                                
        REPLACE A[11] BY "0";                                           
    EXIT:                                                               
  END OF DIGITPASEP;                                                    
 $PAGE                                                                  
%-----------------------------------------------------------------------
%  INICIO DA LIBRARY:  DIGITCGC                                         
%                                                                       
%  LIBRARY CRIADA EM 16/07/86. A PARTIR DO FONTE: PF/SUB/DIGITCGC/001   
%                                                                       
%-----------------------------------------------------------------------
  PROCEDURE DIGITCGC(AREAA,AREAB);                                      
  EBCDIC ARRAY AREAA, AREAB[0];                                         
  BEGIN                                                                 
    POINTER PTP,PTR; LABEL SAIDA; INTEGER Q1,DIMEN,ACUM,I,J;            
    TRUTHSET CODIGO ("CV"), DIGITO("0123456789");                       
    %==========================================================%        
    %   CONSISTENCIA DA DIMENSAO , EM CASO DE ERRO DEVOLVE :   %        
    %      "5" => DIMENSAO INVALIDA                            %        
    %==========================================================%        
    PTP:=AREAB[2];                                                      
    Q1:=2;                                                              
    SCAN PTP FOR Q1:Q1 WHILE IN DIGITO;                                 
    IF Q1 NEQ 0 THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "5";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    DIMEN:=INTEGER(PTP,2);                                              
    IF DIMEN GTR 20 THEN                                                
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "5";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO CODIGO , EM CASO DE ERRO DEVOLVE :   %          
    %      "2" => CODIGO INVALIDO                            %          
    %========================================================%          
    Q1:=1;                                                              
    PTP:=AREAB;                                                         
    SCAN PTP FOR Q1:Q1 WHILE IN CODIGO;                                 
    IF Q1 NEQ 0 THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "2";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO NUMERO , EM CASO DE ERRO DEVOLVE :   %          
    %      "3" => NUMERO INVALIDO                            %          
    %========================================================%          
    IF PTP EQL "V" THEN                                                 
       I:=DIMEN  +  2                                                   
    ELSE                                                                
        I:=DIMEN;                                                       
    PTP:=AREAA;                                                         
    Q1:=I;                                                              
    SCAN PTP FOR Q1:Q1 WHILE IN DIGITO;                                 
    Q1:=I - Q1;                                                         
    IF Q1 NEQ I THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "3";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO DIGITO , EM CASO DE ERRO DEVOLVE :   %          
    %      "4" => DIGITO INVALIDO                            %          
    %========================================================%          
    ACUM:=0;                                                            
    I:=2;                                                               
    Q1:=DIMEN - 1;                                                      
    PTP:=AREAA;                                                         
    FOR J:=Q1 STEP -1 UNTIL 0 DO                                        
        BEGIN                                                           
          ACUM:=* + I * INTEGER(PTP + J,1);                             
          I:=* + 1;                                                     
          IF I GTR 9 THEN                                               
             I:=2;                                                      
        END;                                                            
    I:=ACUM MOD 11;                                                     
    I:=11 - I;                                                          
    IF I GTR 9 THEN                                                     
       I:=0;                                                            
    PTR:=AREAB;                                                         
    IF PTR EQL "V" THEN                                                 
       BEGIN                                                            
         PTP:=AREAA[DIMEN];                                             
         J:=INTEGER(PTP,1);                                             
         IF I NEQ J THEN                                                
            BEGIN                                                       
              PTP:=AREAB[1];                                            
              REPLACE PTP BY "4";                                       
              GO TO SAIDA;                                              
            END;                                                        
       END;                                                             
    PTP:=AREAA[DIMEN];                                                  
    REPLACE PTP BY I FOR 1 DIGITS;                                      
    ACUM:=0;                                                            
    I:=2;                                                               
    PTP:=AREAA;                                                         
    FOR J:=DIMEN STEP - 1 UNTIL 0 DO                                    
        BEGIN                                                           
          ACUM:=* + I * INTEGER(PTP + J,1);                             
          I:=* + 1;                                                     
          IF I GTR 9 THEN                                               
          I:=2;                                                         
        END;                                                            
    I:=ACUM MOD 11;                                                     
    I:=11 - I;                                                          
    IF I GTR 9 THEN                                                     
       I:=0;                                                            
    PTR:=AREAB;                                                         
    IF PTR EQL "V" THEN                                                 
       BEGIN                                                            
         Q1:=DIMEN + 1;                                                 
         PTP:=AREAA[Q1];                                                
         J:=INTEGER(PTP,1);                                             
         IF I NEQ J THEN                                                
            BEGIN                                                       
              PTP:=AREAB[1];                                            
              REPLACE PTP BY "4";                                       
              GO TO SAIDA;                                              
            END;                                                        
       END;                                                             
    PTP:=AREAB[1];                                                      
    REPLACE PTP BY "1";                                                 
    Q1:=DIMEN + 1;                                                      
    PTP:=AREAA[Q1];                                                     
    REPLACE PTP BY I FOR 1 DIGITS;                                      
    SAIDA:                                                              
  END OF DIGITCGC;                                                      
 $PAGE                                                                  
%-----------------------------------------------------------------------
%  INICIO DA LIBRARY:  DIGITCPF                                         
%                                                                       
%  LIBRARY CRIADA EM 16/07/86. A PARTIR DO FONTE: PF/SUB/DIGITCPF/001   
%                                                                       
%-----------------------------------------------------------------------
  PROCEDURE DIGITCPF(AREAA,AREAB);                                      
  EBCDIC ARRAY AREAA, AREAB[0];                                         
  BEGIN                                                                 
    POINTER PTP,PTR; LABEL SAIDA; INTEGER Q1,DIMEN,ACUM,I,J;            
    TRUTHSET CODIGO ("CV"), DIGITO("0123456789");                       
    %==========================================================%        
    %   CONSISTENCIA DA DIMENSAO , EM CASO DE ERRO DEVOLVE :   %        
    %      "5" => DIMENSAO INVALIDA                            %        
    %==========================================================%        
    PTP:=AREAB[2];                                                      
    Q1:=2;                                                              
    SCAN PTP FOR Q1:Q1 WHILE IN DIGITO;                                 
    IF Q1 NEQ 0 THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "5";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    DIMEN:=INTEGER(PTP,2);                                              
    IF DIMEN GTR 20 THEN                                                
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "5";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO CODIGO , EM CASO DE ERRO DEVOLVE :   %          
    %      "2" => CODIGO INVALIDO                            %          
    %========================================================%          
    Q1:=1;                                                              
    PTP:=AREAB;                                                         
    SCAN PTP FOR Q1:Q1 WHILE IN CODIGO;                                 
    IF Q1 NEQ 0 THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "2";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO NUMERO , EM CASO DE ERRO DEVOLVE :   %          
    %      "3" => NUMERO INVALIDO                            %          
    %========================================================%          
    IF PTP EQL "V" THEN                                                 
       I:=DIMEN + 2                                                     
    ELSE                                                                
        I:=DIMEN;                                                       
    PTP:=AREAA;                                                         
    Q1:=I;                                                              
    SCAN PTP FOR Q1:Q1 WHILE IN DIGITO;                                 
    Q1:=I - Q1;                                                         
    IF Q1 NEQ I THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "3";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO DIGITO , EM CASO DE ERRO DEVOLVE :   %          
    %      "4" => DIGITO INVALIDO                            %          
    %========================================================%          
    ACUM:=0;                                                            
    I:=2;                                                               
    Q1:=DIMEN - 1;                                                      
    PTP:=AREAA;                                                         
    FOR J:=Q1 STEP -1 UNTIL 0 DO                                        
        BEGIN                                                           
          ACUM:=* + I * INTEGER(PTP + J,1);                             
          I:=* + 1;                                                     
        END;                                                            
    I:=ACUM MOD 11;                                                     
    I:=11 - I;                                                          
    IF I GTR 9 THEN                                                     
       I:=0;                                                            
    PTR:=AREAB;                                                         
    IF PTR EQL "V" THEN                                                 
       BEGIN                                                            
         PTP:=AREAA[DIMEN];                                             
         J:=INTEGER(PTP,1);                                             
         IF I NEQ J THEN                                                
            BEGIN                                                       
              PTP:=AREAB[1];                                            
              REPLACE PTP BY "4";                                       
              GO TO SAIDA;                                              
            END;                                                        
       END;                                                             
    PTP:=AREAA[DIMEN];                                                  
    REPLACE PTP BY I FOR 1 DIGITS;                                      
    ACUM:=0;                                                            
    I:=2;                                                               
    PTP:=AREAA;                                                         
    FOR J:=DIMEN STEP - 1 UNTIL 0 DO                                    
        BEGIN                                                           
          ACUM:=* + I * INTEGER(PTP + J,1);                             
          I:=* + 1;                                                     
        END;                                                            
    I:=ACUM MOD 11;                                                     
    I:=11 - I;                                                          
    IF I GTR 9 THEN                                                     
       I:=0;                                                            
    PTR:=AREAB;                                                         
    IF PTR EQL "V" THEN                                                 
       BEGIN                                                            
         Q1:=DIMEN + 1;                                                 
         PTP:=AREAA[Q1];                                                
         J:=INTEGER(PTP,1);                                             
         IF I NEQ J THEN                                                
            BEGIN                                                       
              PTP:=AREAB[1];                                            
              REPLACE PTP BY "4";                                       
              GO TO SAIDA;                                              
            END;                                                        
       END;                                                             
    PTP:=AREAB[1];                                                      
    REPLACE PTP BY "1";                                                 
    Q1:=DIMEN + 1;                                                      
    PTP:=AREAA[Q1];                                                     
    REPLACE PTP BY I FOR 1 DIGITS;                                      
    SAIDA:                                                              
  END OF DIGITCPF;                                                      
 $PAGE                                                                  
%-----------------------------------------------------------------------
%  INICIO DA LIBRARY:  DIGITM10                                         
%                                                                       
%  LIBRARY CRIADA EM 16/07/86. A PARTIR DO FONTE: PF/SUB/DIGITM10/001   
%                                                                       
%-----------------------------------------------------------------------
  PROCEDURE DIGITM10(AREAA,AREAB);                                      
  EBCDIC ARRAY AREAA, AREAB[0];                                         
  BEGIN                                                                 
    POINTER PTP; LABEL SAIDA; INTEGER Q1,DIMEN,ACUM,I,J;                
    TRUTHSET CODIGO ("CV"), DIGITO("0123456789");                       
    %==========================================================%        
    %   CONSISTENCIA DA DIMENSAO , EM CASO DE ERRO DEVOLVE :   %        
    %      "5" => DIMENSAO INVALIDA                            %        
    %==========================================================%        
    PTP:=AREAB[2];                                                      
    Q1:=2;                                                              
    SCAN PTP FOR Q1:Q1 WHILE IN DIGITO;                                 
    IF Q1 NEQ 0 THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "5";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    DIMEN:=INTEGER(PTP,2);                                              
    IF DIMEN GTR 20 THEN                                                
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY"5";                                             
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO CODIGO , EM CASO DE ERRO DEVOLVE :   %          
    %      "2" => CODIGO INVALIDO                            %          
    %========================================================%          
    Q1:=1;                                                              
    PTP:=AREAB;                                                         
    SCAN PTP FOR Q1:Q1 WHILE IN CODIGO;                                 
    IF Q1 NEQ 0 THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "2";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO NUMERO , EM CASO DE ERRO DEVOLVE :   %          
    %      "3" => NUMERO INVALIDO                            %          
    %========================================================%          
    IF PTP EQL "V" THEN                                                 
       I:=DIMEN  +  1                                                   
    ELSE                                                                
        I:=DIMEN;                                                       
    PTP:=AREAA;                                                         
    Q1:=I;                                                              
    SCAN PTP FOR Q1:Q1 WHILE IN DIGITO;                                 
    Q1:=I - Q1;                                                         
    IF Q1 NEQ I THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "3";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO DIGITO , EM CASO DE ERRO DEVOLVE :   %          
    %      "4" => DIGITO INVALIDO                            %          
    %========================================================%          
    ACUM:=0;                                                            
    I:=DIMEN MOD 2;                                                     
    IF I EQL 0 THEN                                                     
       BEGIN                                                            
          FOR J:=0 STEP 2 UNTIL DIMEN - 1 DO                            
              ACUM:=* + 1 * INTEGER(PTP + J,1);                         
          FOR J:=1 STEP 2 UNTIL DIMEN DO                                
              BEGIN                                                     
                I:=2 * INTEGER(PTP + J,1);                              
                IF I GTR 9 THEN                                         
                   I:=I - 9;                                            
                ACUM:=* + I;                                            
              END;                                                      
       END                                                              
    ELSE                                                                
        BEGIN                                                           
          FOR J:=0 STEP 2 UNTIL DIMEN DO                                
              BEGIN                                                     
                I:=2 * INTEGER(PTP + J,1);                              
                IF I GTR 9 THEN                                         
                   I:=I - 9;                                            
                ACUM:=* + I;                                            
              END;                                                      
          FOR J:=1 STEP 2 UNTIL DIMEN - 2 DO                            
              ACUM:=* + 1 * INTEGER(PTP + J,1);                         
        END;                                                            
    I:=ACUM MOD 10;                                                     
    I:=10 - I;                                                          
    IF I EQL 10 THEN                                                    
       I:=0;                                                            
    PTP:=AREAB;                                                         
    IF PTP EQL "V" THEN                                                 
       BEGIN                                                            
         PTP:=AREAA[DIMEN];                                             
         J:=INTEGER(PTP,1);                                             
         IF I NEQ J THEN                                                
            BEGIN                                                       
              PTP:=AREAB[1];                                            
              REPLACE PTP BY "4";                                       
              GO TO SAIDA;                                              
            END;                                                        
       END;                                                             
    PTP:=AREAB[1];                                                      
    REPLACE PTP BY "1";                                                 
    PTP:=AREAA[DIMEN];                                                  
    REPLACE PTP BY I FOR 1 DIGITS;                                      
    SAIDA:                                                              
  END OF DIGITM10;                                                      
 $PAGE                                                                  
%-----------------------------------------------------------------------
%                                                                       
%  INICIO DA LIBRARY:  DIGITIPVA21                                      
%                                                                       
%  LIBRARY CRIADA PARA EMISSAO DE GUIA DE RECOLHIMENTO DE IPVA, COM     
%  21 POSICOES NUMERICAS.                                               
%                                                                       
%-----------------------------------------------------------------------
  PROCEDURE DIGITIPVA21(AREAA,AREAB);                                   
  EBCDIC ARRAY AREAA, AREAB[0];                                         
  BEGIN                                                                 
    POINTER PTP; LABEL SAIDA; INTEGER Q1,DIMEN,ACUM,I,J;                
    TRUTHSET CODIGO ("CV"), DIGITO("0123456789");                       
    %==========================================================%        
    %   CONSISTENCIA DA DIMENSAO , EM CASO DE ERRO DEVOLVE :   %        
    %      "5" => DIMENSAO INVALIDA                            %        
    %==========================================================%        
    PTP:=AREAB[2];                                                      
    Q1:=2;                                                              
    SCAN PTP FOR Q1:Q1 WHILE IN DIGITO;                                 
    IF Q1 NEQ 0 THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "5";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    DIMEN:=INTEGER(PTP,2);                                              
    IF DIMEN GTR 21 THEN                                                
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "5";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO CODIGO , EM CASO DE ERRO DEVOLVE :   %          
    %      "2" => CODIGO INVALIDO                            %          
    %========================================================%          
    Q1:=1;                                                              
    PTP:=AREAB;                                                         
    SCAN PTP FOR Q1:Q1 WHILE IN CODIGO;                                 
    IF Q1 NEQ 0 THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "2";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO NUMERO , EM CASO DE ERRO DEVOLVE :   %          
    %      "3" => NUMERO INVALIDO                            %          
    %========================================================%          
    IF PTP EQL "V" THEN                                                 
       I:=DIMEN + 1                                                     
    ELSE                                                                
        I:=DIMEN;                                                       
    PTP:=AREAA;                                                         
    Q1:=I;                                                              
    SCAN PTP FOR Q1:Q1 WHILE IN DIGITO;                                 
    Q1:=I - Q1;                                                         
    IF Q1 NEQ I THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "3";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO DIGITO , EM CASO DE ERRO DEVOLVE :   %          
    %      "4" => DIGITO INVALIDO                            %          
    %========================================================%          
    ACUM:=0;                                                            
    I:=DIMEN MOD 2;                                                     
    IF I EQL 0 THEN                                                     
       BEGIN                                                            
          FOR J:=0 STEP 2 UNTIL DIMEN - 1 DO                            
              ACUM:=* + 1 * INTEGER(PTP + J,1);                         
          FOR J:=1 STEP 2 UNTIL DIMEN DO                                
              BEGIN                                                     
                I:=2 * INTEGER(PTP + J,1);                              
                IF I GTR 9 THEN                                         
                   I:=I - 9;                                            
                ACUM:=* + I;                                            
              END;                                                      
       END                                                              
    ELSE                                                                
        BEGIN                                                           
          FOR J:=0 STEP 2 UNTIL DIMEN DO                                
              BEGIN                                                     
                I:=2 * INTEGER(PTP + J,1);                              
                IF I GTR 9 THEN                                         
                   I:=I - 9;                                            
                ACUM:=* + I;                                            
              END;                                                      
          FOR J:=1 STEP 2 UNTIL DIMEN - 2 DO                            
              ACUM:=* + 1 * INTEGER(PTP + J,1);                         
        END;                                                            
    I:=ACUM MOD 10;                                                     
    I:=10 - I;                                                          
    IF I EQL 10 THEN                                                    
       I:=0;                                                            
    PTP:=AREAB;                                                         
    IF PTP EQL "V" THEN                                                 
       BEGIN                                                            
         PTP:=AREAA[DIMEN];                                             
         J:=INTEGER(PTP,1);                                             
         IF I NEQ J THEN                                                
            BEGIN                                                       
              PTP:=AREAB[1];                                            
              REPLACE PTP BY "4";                                       
              GO TO SAIDA;                                              
            END;                                                        
       END;                                                             
    PTP:=AREAB[1];                                                      
    REPLACE PTP BY "1";                                                 
    PTP:=AREAA[DIMEN];                                                  
    REPLACE PTP BY I FOR 1 DIGITS;                                      
    SAIDA:                                                              
  END OF DIGITIPVA21;                                                   
 $PAGE                                                                  
%-----------------------------------------------------------------------
%                                                                       
%  INICIO DA LIBRARY:  DIGITIPVA                                        
%                                                                       
%  LIBRARY CRIADA PARA EMISSAO DE GUIA DE RECOLHIMENTO DE IPVA, COM     
%  44 POSICOES.                                                         
%                                                                       
%-----------------------------------------------------------------------
  PROCEDURE DIGITIPVA(AREAA,AREAB);                                     
  EBCDIC ARRAY AREAA, AREAB[0];                                         
  BEGIN                                                                 
    POINTER PTP; LABEL SAIDA; INTEGER Q1,DIMEN,ACUM,I,J;                
    TRUTHSET CODIGO ("CV"), DIGITO("0123456789");                       
    %==========================================================%        
    %   CONSISTENCIA DA DIMENSAO , EM CASO DE ERRO DEVOLVE :   %        
    %      "5" => DIMENSAO INVALIDA                            %        
    %==========================================================%        
    PTP:=AREAB[2];                                                      
    Q1:=2;                                                              
    SCAN PTP FOR Q1:Q1 WHILE IN DIGITO;                                 
    IF Q1 NEQ 0 THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "5";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    DIMEN:=INTEGER(PTP,2);                                              
    IF DIMEN GTR 44 THEN                                                
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "5";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO CODIGO , EM CASO DE ERRO DEVOLVE :   %          
    %      "2" => CODIGO INVALIDO                            %          
    %========================================================%          
    Q1:=1;                                                              
    PTP:=AREAB;                                                         
    SCAN PTP FOR Q1:Q1 WHILE IN CODIGO;                                 
    IF Q1 NEQ 0 THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "2";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO NUMERO , EM CASO DE ERRO DEVOLVE :   %          
    %      "3" => NUMERO INVALIDO                            %          
    %========================================================%          
    IF PTP EQL "V" THEN                                                 
       I:=DIMEN + 1                                                     
    ELSE                                                                
        I:=DIMEN;                                                       
    PTP:=AREAA;                                                         
    Q1:=I;                                                              
    SCAN PTP FOR Q1:Q1 WHILE IN DIGITO;                                 
    Q1:=I - Q1;                                                         
    IF Q1 NEQ I THEN                                                    
       BEGIN                                                            
         PTP:=AREAB[1];                                                 
         REPLACE PTP BY "3";                                            
         GO TO SAIDA;                                                   
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO DIGITO , EM CASO DE ERRO DEVOLVE :   %          
    %      "4" => DIGITO INVALIDO                            %          
    %========================================================%          
    ACUM:=0;                                                            
    I:=DIMEN MOD 2;                                                     
    IF I EQL 0 THEN                                                     
       BEGIN                                                            
          FOR J:=0 STEP 2 UNTIL DIMEN - 1 DO                            
              ACUM:=* + 1 * INTEGER(PTP + J,1);                         
          FOR J:=1 STEP 2 UNTIL DIMEN DO                                
              BEGIN                                                     
                I:=2 * INTEGER(PTP + J,1);                              
                IF I GTR 9 THEN                                         
                   I:=I - 9;                                            
                ACUM:=* + I;                                            
              END;                                                      
       END                                                              
    ELSE                                                                
        BEGIN                                                           
          FOR J:=0 STEP 2 UNTIL DIMEN DO                                
              BEGIN                                                     
                I:=2 * INTEGER(PTP + J,1);                              
                IF I GTR 9 THEN                                         
                   I:=I - 9;                                            
                ACUM:=* + I;                                            
              END;                                                      
          FOR J:=1 STEP 2 UNTIL DIMEN - 2 DO                            
              ACUM:=* + 1 * INTEGER(PTP + J,1);                         
        END;                                                            
    I:=ACUM MOD 10;                                                     
    I:=10 - I;                                                          
    IF I EQL 10 THEN                                                    
       I:=0;                                                            
    PTP:=AREAB;                                                         
    IF PTP EQL "V" THEN                                                 
       BEGIN                                                            
         PTP:=AREAA[DIMEN];                                             
         J:=INTEGER(PTP,1);                                             
         IF I NEQ J THEN                                                
            BEGIN                                                       
              PTP:=AREAB[1];                                            
              REPLACE PTP BY "4";                                       
              GO TO SAIDA;                                              
            END;                                                        
       END;                                                             
    PTP:=AREAB[1];                                                      
    REPLACE PTP BY "1";                                                 
    PTP:=AREAA[DIMEN];                                                  
    REPLACE PTP BY I FOR 1 DIGITS;                                      
    SAIDA:                                                              
  END OF DIGITIPVA;                                                     
 $PAGE                                                                  
%-----------------------------------------------------------------------
%  INICIO DA LIBRARY:  DIGITM11                                         
%                                                                       
%  LIBRARY CRIADA EM 16/07/86. A PARTIR DO FONTE: PF/SUB/DIGITM11/001   
%                                                                       
%-----------------------------------------------------------------------
  PROCEDURE DIGITM11(A,B);                                              
  EBCDIC ARRAY A, B[0];                                                 
  BEGIN                                                                 
    POINTER PA,PB; LABEL EXIT; INTEGER COUNT,DIMEN,POSF,ACUM,I,J;       
    TRUTHSET CODIGO ("CV"), NUMERO("0123456789"),NUMEROX("0123456789X");
    PA:=A; PB:=B;                                                       
    %========================================================%          
    %   CONSISTENCIA DO CODIGO , EM CASO DE ERRO DEVOLVE :   %          
    %     " 3" => CODIGO INVALIDO                            %          
    %========================================================%          
    COUNT:=1;                                                           
    SCAN PA:PA FOR COUNT:COUNT WHILE IN CODIGO;                         
    IF COUNT NEQ 0 THEN                                                 
    BEGIN                                                               
      REPLACE PB BY " 3"; GO TO EXIT;                                   
    END;                                                                
    %==========================================================%        
    %   CONSISTENCIA DA DIMENS]O , EM CASO DE ERRO DEVOLVE :   %        
    %     " 4" => DIMENS]O N]O NUMERICA                        %        
    %     " 5" => DIMENS]O = A ZERO                            %        
    %==========================================================%        
    COUNT:=2;                                                           
    SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                         
    IF COUNT NEQ 0 THEN                                                 
    BEGIN                                                               
      REPLACE PB BY " 4"; GO TO EXIT;                                   
    END;                                                                
    DIMEN:=INTEGER(A[1],2);                                             
    IF DIMEN = 0 THEN                                                   
    BEGIN                                                               
      REPLACE PB BY " 5"; GO TO EXIT;                                   
    END;                                                                
    %=======================================================%           
    %   CONSISTENCIA DO CAMPO , EM CASO DE ERRO DEVOLVE :   %           
    %     " 6" => CAMPO N]O NUMERICO                        %           
    %=======================================================%           
    COUNT:=DIMEN;                                                       
    SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                         
    IF COUNT NEQ 0 THEN                                                 
    BEGIN                                                               
      REPLACE PB BY " 6"; GO TO EXIT;                                   
    END;                                                                
    %========================================================%          
    %   CONSISTENCIA DO DIGITO , EM CASO DE ERRO DEVOLVE :   %          
    %     " 7" => DIGITO INVALIDO                            %          
    %========================================================%          
    IF A[0] = "V" THEN                                                  
    BEGIN                                                               
      COUNT:=1;                                                         
      SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMEROX;                      
      IF COUNT NEQ 0 THEN                                               
      BEGIN                                                             
        REPLACE PB BY " 7"; GO TO EXIT;                                 
      END;                                                              
    END;                                                                
    %====================================================%              
    %   CALCULO DO DIGIT CHECK E VERIFICACAO DO DIGITO   %              
    %====================================================%              
    POSF:=3 + DIMEN + 1;                                                
    FOR I:=2 STEP 1 UNTIL 10 DO                                         
    FOR J:=POSF-I STEP -9 UNTIL 3 DO                                    
        ACUM:=ACUM + I*INTEGER(A[J],1);                                 
    I:=ACUM MOD 11;                                                     
    IF I NEQ 10 THEN                                                    
       REPLACE B[0] BY I FOR 1 DIGITS                                   
    ELSE                                                                
        REPLACE B[0] BY "X";                                            
    IF A[0] = "C" FOR 1 THEN                                            
       REPLACE B[1] BY "2"                                              
    ELSE                                                                
        IF B[0] = A[DIMEN + 3 ] FOR 1 THEN                              
           REPLACE B[1] BY "0"                                          
        ELSE                                                            
            REPLACE B[1] BY "1";                                        
    EXIT:                                                               
  END OF DIGITM11;                                                      
 $PAGE                                                                  
%-----------------------------------------------------------------------
%  INICIO DA LIBRARY:  DIGITCID                                         
%                                                                       
%  LIBRARY CRIADA EM 22/04/88. A PARTIR DO FONTE: PF/LIB/DIGITCID/000   
%                                                                       
%-----------------------------------------------------------------------
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  ROTINA PARA CRIACAO OU VERIFICACAO DE CHECK DIGIT-MODULO 11 - PARA  %
%  CAMPOS DE 01 A 99 DIGITOS PARA O CODIGO INTERNACIONAL DE DOENCAS:   %
%                                                                      %
% 1 - FUNCAO                                                           %
%     A FUNCAO DESTA ROTINA E A CRIACAO OU VERIFICACAO DE CHECK DIGIT- %
%     MODULO 11, PARA CAMPOS DE 01 A 99 DIGITOS.                       %
% 2 - CHAMADA E CARACTERISTICAS DA ROTINA                              %
%     DEVERA SER CHAMADO PELA COMANDO ENTER, DA SEGUINTE MANEIRA:      %
%                ENTER  DIGITCID  USING CAMPO1 CAMPO2                  %
%     SENDO QUE CAMPO1 E CAMPO2, FORAM DEFINIDOS ASSIM:                %
%        01    CAMPO1                                                  %
%          02  CODIGO       PIC X.                                     %
%          02  DIMENSAO     PIC 99.                                    %
%          02  CAMPO        PIC 9(NN).                                 %
%          02  DIG          PIC 9.                                     %
%                                                                      %
%        01    CAMPO2                                                  %
%          02  CH-DIG       PIC 9.                                     %
%          02  CONS         PIC 9.                                     %
%                                                                      %
%        ONDE:                                                         %
%          CODIGO     - INDICA O QUE A ROTINA DEVE FAZER:              %
%                       C = CRIAR     DIGITO                           %
%                       V = VERIFICAR DIGITO                           %
%                                                                      %
%          DIMENSAO   - QUANTIDADE DE DIGITOS DO CAMPO DO QUAL SE QUER %
%                       CALCULAR O CHECK DIGIT.  PODE TER  COMO  VALOR %
%                       01 A 99.                                       %
%                                                                      %
%          CAMPO      - NUMERO DO QUAL SERA CALCULADO O CHECK DIGIT.   %
%                       PODE TER COMPRIMENTO DE 1 A 99 BYTES, COMO,    %
%                       INDICADO EM DIMENSAO.                          %
%                                                                      %
%          DIG        - DIGITO JA CALCULADO PARA VERIFICACAO.          %
%                       NAO E CONSIDERADO QUANDO SE VAI CRIAR O CHECK  %
%                       DIGIT.                                         %
%                                                                      %
%          CH-DIG     - CHECK DIGIT CALCULADO PELA ROTINA.             %
%                                                                      %
%          CONS       - CODIGO DADO PELA ROTINA. PODERA SER:           %
%                         0 = DIGITO CORRETO                           %
%                         1 = DIGITO ERRADO                            %
%                         2 = DIGITO CALCULADO                         %
%                                                                      %
%     O CHECK DIGIT E" CALCULADO MULTIPLICANDO-SE OS ALGARISMOS DO NU- %
%     MERO, DA DIREITA PARA A ESQUERDA, POR 2,3,4,...10,2,3,4,...10,2, %
%     3,4,...10,2..., SENDO A SOMA DOS PRODUTOS DIVIDIDA POR 11.  SE O %
%     RESTO FOR IGUAL A 0 (ZERO) OU IGUAL A 1 (UM) O CHECK DIGIT  SERA %
%     0 (ZERO), CASO CONTRARIO O CHECK DIGIT SERA IGUAL A 11 MENOS   O %
%     RESTO, OU SEJA:                                                  %
%          IF RESTO EQL 0 OR RESTO EQL 1 THEN                          %
%             CHECK-DIGIT:= 0 ELSE                                     %
%             CHECK-DIGIT:= 11-RESTO                                   %
%                                                                      %
%     OBS.: ESTA ROTINA E" SIMILAR A ROTINA DIGITM11, CUJA DEFINICAO   %
%           CONSTA NO:                                                 %
%           - MANUAL TECNICO - BOLETIM TECNICO                         %
%           - ROTINAS UTILITARIAS                                      %
%           - VOLUME E-SEDE                                            %
%           - CAPITULO II                                              %
%           - PAGINA 02200                                             %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                                        
  PROCEDURE DIGITCID(A,B);                                              
  EBCDIC ARRAY A, B[0];                                                 
  BEGIN                                                                 
    POINTER PA,PB; LABEL EXIT; INTEGER COUNT,DIMEN,POSF,ACUM,I,J;       
    TRUTHSET CODIGO ("CV"), NUMERO("0123456789");                       
    PA:=A; PB:=B;                                                       
    %========================================================%          
    %   CONSISTENCIA DO CODIGO , EM CASO DE ERRO DEVOLVE :   %          
    %     " 3" => CODIGO INVALIDO                            %          
    %========================================================%          
    COUNT:=1;                                                           
    SCAN PA:PA FOR COUNT:COUNT WHILE IN CODIGO;                         
    IF COUNT NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE PB BY " 3"; GO TO EXIT;                                
       END;                                                             
    %==========================================================%        
    %   CONSISTENCIA DA DIMENS]O , EM CASO DE ERRO DEVOLVE :   %        
    %     " 4" => DIMENS]O N]O NUMERICA                        %        
    %     " 5" => DIMENS]O = A ZERO                            %        
    %==========================================================%        
    COUNT:=2;                                                           
    SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                         
    IF COUNT NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE PB BY " 4"; GO TO EXIT;                                
       END;                                                             
    DIMEN:=INTEGER(A[1],2);                                             
    IF DIMEN = 0 THEN                                                   
       BEGIN                                                            
         REPLACE PB BY " 5"; GO TO EXIT;                                
       END;                                                             
    %=======================================================%           
    %   CONSISTENCIA DO CAMPO , EM CASO DE ERRO DEVOLVE :   %           
    %     " 6" => CAMPO N]O NUMERICO                        %           
    %=======================================================%           
    COUNT:=DIMEN;                                                       
    SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                         
    IF COUNT NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE PB BY " 6"; GO TO EXIT;                                
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO DIGITO , EM CASO DE ERRO DEVOLVE :   %          
    %     " 7" => DIGITO INVALIDO                            %          
    %========================================================%          
    IF A[0] = "V" THEN                                                  
       BEGIN                                                            
         COUNT:=1;                                                      
         SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                    
         IF COUNT NEQ 0 THEN                                            
            BEGIN                                                       
              REPLACE PB BY " 7"; GO TO EXIT;                           
            END;                                                        
       END;                                                             
    %====================================================%              
    %   CALCULO DO DIGIT CHECK E VERIFICACAO DO DIGITO   %              
    %====================================================%              
    POSF:=3 + DIMEN + 1;                                                
    FOR I:=2 STEP 1 UNTIL 10 DO                                         
    FOR J:=POSF-I STEP -9 UNTIL 3 DO                                    
        ACUM:=ACUM + I*INTEGER(A[J],1);                                 
    I:=ACUM MOD 11;                                                     
    IF I EQL 0 OR  I EQL 1 THEN                                         
       REPLACE B[0] BY "0"                                              
    ELSE                                                                
        BEGIN                                                           
          I:= 11 - I;                                                   
          REPLACE B[0] BY I FOR 1 DIGITS                                
        END;                                                            
    IF A[0] = "C" FOR 1 THEN                                            
       REPLACE B[1] BY "2"                                              
    ELSE                                                                
        IF B[0] = A[DIMEN + 3 ] FOR 1 THEN                              
           REPLACE B[1] BY "0"                                          
        ELSE                                                            
            REPLACE B[1] BY "1";                                        
    EXIT:                                                               
                                                                        
  END OF DIGITCID;                                                      
 $PAGE                                                                  
%-----------------------------------------------------------------------
%  INICIO DA LIBRARY:  DIGITRENACH                                      
%                                                                       
%  LIBRARY CRIADA EM 06/12/95. A PARTIR DA DIGITM11                     
%                                                                       
%-----------------------------------------------------------------------
  PROCEDURE DIGITRENACH (A,B);                                          
  EBCDIC ARRAY A, B[0];                                                 
  BEGIN                                                                 
    POINTER PA,PB; LABEL EXIT; INTEGER COUNT,DIMEN,POSF,ACUM,D1,D2,I,J; 
    TRUTHSET CODIGO ("CV"), NUMERO("0123456789");                       
    PA:=A; PB:=B;                                                       
    %========================================================%          
    %   CONSISTENCIA DO CODIGO , EM CASO DE ERRO DEVOLVE :   %          
    %      "3" => CODIGO INVALIDO                            %          
    %========================================================%          
    COUNT:=1;                                                           
    SCAN PA:PA FOR COUNT:COUNT WHILE IN CODIGO;                         
    IF COUNT NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE B[0] BY "003"; GO TO EXIT;                             
       END;                                                             
    %==========================================================%        
    %   CONSISTENCIA DA DIMENSAO , EM CASO DE ERRO DEVOLVE :   %        
    %      "4" => DIMENSAO NAO NUMERICA                        %        
    %      "5" => DIMENSAO IGUAL A ZERO                        %        
    %==========================================================%        
    COUNT:=2;                                                           
    SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                         
    IF COUNT NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE B[0] BY "004"; GO TO EXIT;                             
       END;                                                             
    DIMEN:=INTEGER(A[1],2);                                             
    IF DIMEN = 0 THEN                                                   
       BEGIN                                                            
         REPLACE B[0] BY "005"; GO TO EXIT;                             
       END;                                                             
    %=======================================================%           
    %   CONSISTENCIA DO CAMPO , EM CASO DE ERRO DEVOLVE :   %           
    %      "6" => CAMPO NAO NUMERICO                        %           
    %=======================================================%           
    COUNT:=DIMEN;                                                       
    SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                         
    IF COUNT NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE B[0] BY "006"; GO TO EXIT;                             
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO DIGITO , EM CASO DE ERRO DEVOLVE :   %          
    %      "7" => DIGITO INVALIDO                            %          
    %========================================================%          
    IF A[0] = "V" THEN                                                  
       BEGIN                                                            
         COUNT:=2;                                                      
         SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                    
         IF COUNT NEQ 0 THEN                                            
            BEGIN                                                       
              REPLACE B[0] BY "007"; GO TO EXIT;                        
            END;                                                        
       END;                                                             
    %====================================================%              
    %   CALCULO DO DIGIT CHECK E VERIFICACAO DO DIGITO   %              
    %====================================================%              
    ACUM:=   2*INTEGER(A[3],1)                                          
           + 3*INTEGER(A[4],1)                                          
           + 4*INTEGER(A[5],1)                                          
           + 5*INTEGER(A[6],1)                                          
           + 6*INTEGER(A[7],1)                                          
           + 7*INTEGER(A[8],1)                                          
           + 8*INTEGER(A[9],1)                                          
           + 9*INTEGER(A[10],1)                                         
           +10*INTEGER(A[11],1);                                        
    D1:= IF ACUM MOD 11 = 0 OR            % CALCULO DO DIGITO D1:       
            ACUM MOD 11 = 1 THEN 0        %   R = 0 --> D1 = 0          
         ELSE                             %   R = 1 --> D1 = 0          
             11 - (ACUM MOD 11);          %   R > 1 --> D1 = 11 - R     
                                                                        
    ACUM:=0;                                                            
    ACUM:=   2*D1                                                       
           + 3*INTEGER(A[3],1)                                          
           + 4*INTEGER(A[4],1)                                          
           + 5*INTEGER(A[5],1)                                          
           + 6*INTEGER(A[6],1)                                          
           + 7*INTEGER(A[7],1)                                          
           + 8*INTEGER(A[8],1)                                          
           + 9*INTEGER(A[9],1)                                          
           +10*INTEGER(A[10],1)                                         
           +11*INTEGER(A[11],1);                                        
    D2:= IF ACUM MOD 11 = 0 OR            % CALCULO DO DIGITO D2:       
            ACUM MOD 11 = 1 THEN 0        %   R = 0  --> D2 = 0         
         ELSE                             %   R = 1  --> D2 = 0         
             11 - (ACUM MOD 11);          %   R > 1  --> D2 = 11 - R    
                                                                        
    IF A[0] = "C" FOR 1 THEN                                            
       BEGIN                                                            
         REPLACE B[0] BY D1 FOR 1 DIGITS;                               
         REPLACE B[1] BY D2 FOR 1 DIGITS;                               
         REPLACE B[2] BY "2";                                           
       END                                                              
    ELSE                                                                
        IF INTEGER(A[12],1) = D1 AND                                    
           INTEGER(A[13],1) = D2 THEN                                   
           BEGIN                                                        
             REPLACE B[0] BY D1 FOR 1 DIGITS;                           
             REPLACE B[1] BY D2 FOR 1 DIGITS;                           
             REPLACE B[2] BY "0";                                       
           END                                                          
        ELSE                                                            
            REPLACE B[0] BY "001";                                      
    EXIT:                                                               
  END OF DIGITRENACH;                                                   
 $PAGE                                                                  
%-----------------------------------------------------------------------
%  INICIO DA LIBRARY:  DIGITSEDEX                                       
%                                                                       
%  LIBRARY CRIADA EM 28/07/98                                           
%                                                                       
%-----------------------------------------------------------------------
  PROCEDURE DIGITSEDEX (A,B);                                           
  EBCDIC ARRAY A,B [0];                                                 
  BEGIN                                                                 
    INTEGER ACUM, COUNT, DIMEN, D1; LABEL EXIT;                         
    TRUTHSET NUMEROS ("0123456789");                                    
    POINTER PA, PB;                                                     
    PA:=A; PB:=B;                                                       
                                                                        
    %========================================================%          
    %   CONSISTENCIA DA DIMENSAO E DO NUMERO DO SEDEX, EM    %          
    %   CASO DE ERRO, DEVOLVE:                               %          
    %          "0" -> DIGITO CALCULADO                       %          
    %          "1" -> DIMENSAO INVALIDA                      %          
    %          "2" -> DIMENSAO IGUAL A ZERO                  %          
    %          "3" -> NUMERO INVALIDO                        %          
    %========================================================%          
    DIMEN:=INTEGER(A[0],2);                                             
    IF DIMEN GTR 01 AND                                                 
       DIMEN LSS 08 THEN                                                
       BEGIN                                                            
         REPLACE B[1] BY "1"; GO TO EXIT;                               
       END                                                              
    ELSE                                                                
        IF DIMEN EQL 00 THEN                                            
           BEGIN                                                        
             REPLACE B[1] BY "2"; GO TO EXIT;                           
           END;                                                         
                                                                        
    COUNT:=DIMEN;                                                       
    SCAN PA:PA+2 FOR COUNT:COUNT WHILE IN NUMEROS;                      
    COUNT:= DIMEN - COUNT;                                              
    IF COUNT NEQ DIMEN THEN                                             
       BEGIN                                                            
         REPLACE B[1] BY "3"; GO TO EXIT;                               
       END;                                                             
                                                                        
    %====================================================%              
    %               CALCULO DO DIGIT CHECK               %              
    %====================================================%              
    ACUM:=0;                                                            
    ACUM:=   8*INTEGER(A[2],1)                                          
           + 6*INTEGER(A[3],1)                                          
           + 4*INTEGER(A[4],1)                                          
           + 2*INTEGER(A[5],1)                                          
           + 3*INTEGER(A[6],1)                                          
           + 5*INTEGER(A[7],1)                                          
           + 9*INTEGER(A[8],1)                                          
           + 7*INTEGER(A[9],1);                                         
                                                                        
    IF (ACUM MOD 11) = 0 THEN                  % CALCULO DO DIGITO D1:  
       BEGIN                                                            
         D1 := 5;                              %   R=0 --> D1 = 5       
         REPLACE B[0] BY D1 FOR 1 DIGITS;                               
       END                                                              
    ELSE                                                                
        IF (ACUM MOD 11) = 1 THEN              %   R=1 --> D1 = 0       
           BEGIN                                                        
             D1 := 0;                                                   
             REPLACE B[0] BY D1 FOR 1 DIGITS;                           
           END                                                          
        ELSE                                                            
            BEGIN                              %   R>1 --> D1 = 11 - R  
              D1 := 11 - (ACUM MOD 11);                                 
              REPLACE B[0] BY D1 FOR 1 DIGITS;                          
            END;                                                        
  EXIT:                                                                 
  END OF DIGITSEDEX;                                                    
                                                                        
%-----------------------------------------------------------------------
%  INICIO DA LIBRARY:  DIGITDUT                                         
%                                                                       
%  LIBRARY CRIADA EM 14/05/99. SOLICITACAO DA SILVIA SALIA.             
%                                                                       
%-----------------------------------------------------------------------
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  ROTINA PARA CRIACAO OU VERIFICACAO DE CHECK DIGIT-MODULO 11 - PARA  %
%  CAMPOS DE 01 A 99 DIGITOS PARA O DUT E DUAL.                        %
%                                                                      %
% 1 - FUNCAO                                                           %
%     A FUNCAO DESTA ROTINA E A CRIACAO OU VERIFICACAO DE CHECK DIGIT- %
%     MODULO 11, PARA CAMPOS DE 01 A 99 DIGITOS.                       %
% 2 - CHAMADA E CARACTERISTICAS DA ROTINA                              %
%     DEVERA SER CHAMADA PELO COMANDO:                                 %
%     CALL "DIGITDUT OF *PC/LIB/DIGITCHECK" USING AX-CAMPO1 AX-CAMPO2. %
%     SENDO QUE CAMPO1 E CAMPO2, FORAM DEFINIDOS ASSIM:                %
%        01    CAMPO1                                                  %
%          02  CODIGO       PIC X.                                     %
%          02  DIMENSAO     PIC 99.                                    %
%          02  CAMPO        PIC 9(NN).                                 %
%          02  DIG          PIC 9.                                     %
%                                                                      %
%        01    CAMPO2                                                  %
%          02  CH-DIG       PIC 9.                                     %
%          02  CONS         PIC 9.                                     %
%                                                                      %
%        ONDE:                                                         %
%          CODIGO     - INDICA O QUE A ROTINA DEVE FAZER:              %
%                       C = CRIAR     DIGITO                           %
%                       V = VERIFICAR DIGITO                           %
%                                                                      %
%          DIMENSAO   - QUANTIDADE DE DIGITOS DO CAMPO DO QUAL SE QUER %
%                       CALCULAR O CHECK DIGIT.  PODE TER  COMO  VALOR %
%                       01 A 99.                                       %
%                                                                      %
%          CAMPO      - NUMERO DO QUAL SERA CALCULADO O CHECK DIGIT.   %
%                       PODE TER COMPRIMENTO DE 1 A 99 BYTES, COMO,    %
%                       INDICADO EM DIMENSAO.                          %
%                                                                      %
%          DIG        - DIGITO JA CALCULADO PARA VERIFICACAO.          %
%                       NAO E CONSIDERADO QUANDO SE VAI CRIAR O CHECK  %
%                       DIGIT.                                         %
%                                                                      %
%          CH-DIG     - CHECK DIGIT CALCULADO PELA ROTINA.             %
%                                                                      %
%          CONS       - CODIGO DADO PELA ROTINA. PODERA SER:           %
%                         0 = DIGITO CORRETO                           %
%                         1 = DIGITO ERRADO                            %
%                         2 = DIGITO CALCULADO                         %
%                                                                      %
%     O CHECK DIGIT E" CALCULADO MULTIPLICANDO-SE OS ALGARISMOS DO NU- %
%     MERO, DA DIREITA PARA A ESQUERDA, POR 2,3,4,...9,2,3,4,...9,2,3, %
%     4,...9,2..., SENDO A SOMA DOS PRODUTOS DIVIDIDA POR 11. SE     O %
%     RESTO FOR IGUAL A 0 (ZERO) OU IGUAL A 1 (UM) O CHECK DIGIT  SERA %
%     0 (ZERO), CASO CONTRARIO O CHECK DIGIT SERA IGUAL A 11 MENOS   O %
%     RESTO, OU SEJA:                                                   
%          IF RESTO EQL 0 OR RESTO EQL 1 THEN                          %
%             CHECK-DIGIT:= 0 ELSE                                     %
%             CHECK-DIGIT:= 11-RESTO                                   %
%                                                                      %
%     OBS.: ESTA ROTINA E" SIMILAR A ROTINA DIGITM11, CUJA DEFINICAO   %
%           CONSTA NO:                                                 %
%           - MANUAL TECNICO - BOLETIM TECNICO                         %
%           - ROTINAS UTILITARIAS                                      %
%           - VOLUME E-SEDE                                            %
%           - CAPITULO II                                              %
%           - PAGINA 02200                                             %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                                        
  PROCEDURE DIGITDUT(A,B);                                              
   EBCDIC ARRAY A, B[0];                                                
   BEGIN                                                                
    FILE DEBUG1(KIND=REMOTE);  % USAR UM DOS DOIS PARA AVALIAR OS       
    FILE DEBUG2(KIND=PRINTER); % RESULTADOS                             
    INTEGER DIMEN,POSF,ACUM,CONT1,CONT2,CONT3,CONT4,REST1,REST2;        
    POINTER PA,PB; LABEL EXIT;                                          
    TRUTHSET CODIGO ("CV"), NUMERO("0123456789");                       
    PROCEDURE IMPRIME;                                                  
     BEGIN                                                              
    % WRITE (DEBUG1,*/,                                                 
      WRITE (DEBUG2[SPACE 1],*/,                                        
             DIMEN,POSF,ACUM,CONT1,CONT2,CONT3,CONT4,REST1,REST2);      
     END;                                                               
    PROCEDURE IMPRIM2;                                                  
     BEGIN                                                              
    % WRITE (DEBUG1,                                                    
      WRITE (DEBUG2[SPACE 1],                                           
             <"CODIGO=",A1," DIMENSAO=",A2," NUMERO=",A30>,             
               A[0],A[1],A[3]);                                         
    % WRITE(DEBUG1,                                                     
    % WRITE(DEBUG2,                                                     
    %        <"DIGITO=",A1,"CODIGO=",A2>,A[0],A[1]);                    
     END;                                                               
    PA:=A; PB:=B;                                                       
    %========================================================%          
    %   CONSISTENCIA DO CODIGO , EM CASO DE ERRO DEVOLVE :   %          
    %     " 3" => CODIGO INVALIDO                            %          
    %========================================================%          
    CONT1:=1;                                                           
    SCAN PA:PA FOR CONT1:CONT1 WHILE IN CODIGO;                         
    IF CONT1 NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE PB BY " 3"; GO TO EXIT;                                
       END;                                                             
    %==========================================================%        
    %   CONSISTENCIA DA DIMENS]O , EM CASO DE ERRO DEVOLVE :   %        
    %     " 4" => DIMENS]O N]O NUMERICA                        %        
    %     " 5" => DIMENS]O = A ZERO                            %        
    %==========================================================%        
    CONT1:=2;                                                           
    SCAN PA:PA FOR CONT1:CONT1 WHILE IN NUMERO;                         
    IF CONT1 NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE PB BY " 4"; GO TO EXIT;                                
       END;                                                             
    DIMEN:=INTEGER(A[1],2);                                             
    IF DIMEN = 0 THEN                                                   
       BEGIN                                                            
         REPLACE PB BY " 5"; GO TO EXIT;                                
       END;                                                             
    %=======================================================%           
    %   CONSISTENCIA DO CAMPO , EM CASO DE ERRO DEVOLVE :   %           
    %     " 6" => CAMPO N]O NUMERICO                        %           
    %=======================================================%           
    CONT1:=DIMEN;                                                       
    SCAN PA:PA FOR CONT1:CONT1 WHILE IN NUMERO;                         
    IF CONT1 NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE PB BY " 6"; GO TO EXIT;                                
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO DIGITO , EM CASO DE ERRO DEVOLVE :   %          
    %     " 7" => DIGITO INVALIDO                            %          
    %========================================================%          
    IF A[0] = "V" THEN                                                  
       BEGIN                                                            
         CONT1:=1;                                                      
         SCAN PA:PA FOR CONT1:CONT1 WHILE IN NUMERO;                    
         IF CONT1 NEQ 0 THEN                                            
            BEGIN                                                       
              REPLACE PB BY " 7"; GO TO EXIT;                           
            END;                                                        
       END;                                                             
    %====================================================%              
    %   CALCULO DO DIGIT CHECK E VERIFICACAO DO DIGITO   %              
    %====================================================%              
    POSF:=3 + DIMEN;                                                    
    CONT1:= DIMEN DIV 8;                                                
    REST1:= DIMEN MOD 8;                                                
 %  IMPRIME;                                                            
    CONT4:=1;                                                           
    IF CONT1 NEQ 0                                                      
     THEN                                                               
      BEGIN                                                             
       FOR CONT2:=1 STEP 1 UNTIL CONT1 DO                               
        BEGIN                                                           
 %       IMPRIME;                                                       
         FOR CONT3:=2 STEP 1 UNTIL 9 DO                                 
          BEGIN                                                         
           ACUM:=ACUM + CONT3*INTEGER(A[POSF-CONT4],1);                 
           CONT4:= CONT4 + 1;                                           
 %         IMPRIME;                                                     
          END;                                                          
        END;                                                            
      END;                                                              
    IF REST1 NEQ 0                                                      
     THEN                                                               
      BEGIN                                                             
 %     IMPRIME;                                                         
       FOR CONT3:=2 STEP 1 UNTIL REST1+1 DO                             
        BEGIN                                                           
         ACUM:=ACUM + CONT3*INTEGER(A[POSF-CONT4],1);                   
         CONT4:= CONT4 + 1;                                             
 %       IMPRIME;                                                       
        END;                                                            
      END;                                                              
    REST2:=ACUM MOD 11;                                                 
 %  IMPRIME;                                                            
    IF REST2 EQL 0 OR  REST2 EQL 1 THEN                                 
       REPLACE B[0] BY "0"                                              
    ELSE                                                                
        BEGIN                                                           
          REST2:= 11 - REST2;                                           
          REPLACE B[0] BY REST2 FOR 1 DIGITS                            
        END;                                                            
    IF A[0] = "C" FOR 1 THEN                                            
       REPLACE B[1] BY "2"                                              
    ELSE                                                                
        IF B[0] = A[DIMEN + 3 ] FOR 1 THEN                              
           REPLACE B[1] BY "0"                                          
        ELSE                                                            
            REPLACE B[1] BY "1";                                        
 %  IMPRIM2;                                                            
    EXIT:                                                               
                                                                        
  END OF DIGITDUT;                                                      
 $PAGE                                                                  
%-----------------------------------------------------------------------
%  INICIO DA LIBRARY:  DIGITCERTID                                      
%                                                                       
%  CRIACAO DA LIBRARY 15/05/2019 A 29/05/2019                           
%                                                                       
%-----------------------------------------------------------------------
% 11. DIGITCERTID                                                       
%                                                                       
% 11.01 - FUNCOES                                                       
%                                                                       
%       ESTA LIBRARY FAZ A CRIACAO OU VERIFICACAO DE CHECK DIGIT        
%       MODULO 11, PARA CAMPOS DE 30 BYTES (DIGITOS).                   
%       O CHECK DIGIT E COMPOSTO POR 2 DIGITOS.                         
%                                                                       
%       O CALCULO DO PRIMEIRO DIGITO E FEITO DA SEGUINTE FORMA:         
%       SOMATORIA DA MULTIPLICACAO DA ESQUERDA PARA A DIREITA,          
%       DE CADA UM DOS TRINTA NUMEROS PELA SEGUINTE SEQUENCIA:          
%       2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9.  
%       D1 = AO RESTO DE (N1*2+N2*3+N3*4+N4*5+...+N30*9) / 11.          
%       SE O RESTO FOR IGUAL A DEZ ENTAO D1=1.                          
%                                                                       
%       O CALCULO DO SEGUNDO  DIGITO E FEITO DA SEGUINTE FORMA:         
%       SOMATORIA DA MULTIPLICACAO DA ESQUERDA PARA A DIREITA,          
%       DE CADA UM DOS TRINTA NUMEROS E D1 PELA SEGUINTE SEQUENCIA:     
%       1,2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9,10,0,1,2,3,4,5,6,7,8,9 
%        D2 = AO RESTO DE (N1*1+N2*2+N3*3+N4*4+...+N30*8+D1*9) / 11.    
%        SE O RESTO FOR IGUAL A DEZ ENTAO D2=1.                         
%                                                                       
% 11.02 - PARAMETROS                                                    
%                                                                       
%        11.02.1 - AX-CAMPO1                                            
%                                                                       
%                  AX-CODIGO   - "C" (CRIACAO) OU "V" (VERIFICACAO)     
%                                                                       
%                  AX-DIMENSAO - QUANTIDADE DE NUMEROS DO NUMERO DE     
%                                MATRICULA QUE SERA CALCULADO O DIGIT   
%                                CHECK. NUMERO FIXO. VALUE 30.          
%                                                                       
%                  AX-NUMERO   - NUMERO DE MATRICULA QUE SERA CALCULADO 
%                                O DIGIT CHECK. SEMPRE COM 30 DIGITOS   
%                                                                       
%        11.02.2 - AX-CAMPO2                                            
%                                                                       
%                  AX-DIGITCHECK - DIGIT CHECK CALCULADO OU VERIFICADO  
%                                  PELA ROTINA                          
%                  AX-CODRETORNO - CODIGO DE RETORNO DADO PELA ROTINA.  
%                                  PODERA SER:                          
%                                                                       
%                                0 -> DIGIT CHECK CORRETO (OPCAO "V")   
%                                1 -> DIGIT CHECK ERRADO  (OPCAO "V")   
%                                2 -> DIGIT CHECK CALCULADO (OPCAO "C") 
%                                3 -> CODIGO DIFERENTE DE C OU V        
%                                4 => DIMENSAO NAO NUMERICA             
%                                5 => DIMENSAO IGUAL A ZERO             
%                                6 => AX-NUMERO NAO NUMERICO            
%                                7 => DIGIT CHECK NAO NMERICO           
% 11.03 - EXEMPLO                                                       
%                                                                       
%         WORKING-STORAGE  SECTION.                                     
%         01  AX-CAMPO1.                                                
%                05    AX-CODIGO           PIC X(01).                   
%                05    AX-DIMENSAO         PIC 9(02) VALUE 30.          
%                05    AX-NUMERO           PIC 9(30).                   
%                                                                       
%         01  AX-CAMPO2.                                                
%                05    AX-DIGITCHECK      PIC X(02).                    
%                05    AX-CODRETORNO       PIC 9(01).                   
%                                                                       
%        PROCEDURE  DIVISION.                                           
%        CALL   "DIGITCERTID OF   PC/LIB/DIGITCHECK"                    
%                                    USING  AX-CAMPO1                   
%                                           AX-CAMPO2.                  
%                                                                       
%        STOP   RUN.                                                    
  PROCEDURE DIGITCERTID (A,B);                                          
  EBCDIC ARRAY A, B[0];                                                 
  BEGIN                                                                 
    POINTER PA,PB; LABEL EXIT; INTEGER COUNT,DIMEN,POSF,ACUM,D1,D2,I,J; 
    TRUTHSET CODIGO ("CV"), NUMERO("0123456789");                       
    PA:=A; PB:=B;                                                       
    %========================================================%          
    %   CONSISTENCIA DO CODIGO , EM CASO DE ERRO DEVOLVE :   %          
    %      "3" => CODIGO INVALIDO                            %          
    %========================================================%          
    COUNT:=1;                                                           
    SCAN PA:PA FOR COUNT:COUNT WHILE IN CODIGO;                         
    IF COUNT NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE B[0] BY "003"; GO TO EXIT;                             
       END;                                                             
    %==========================================================%        
    %   CONSISTENCIA DA DIMENSAO , EM CASO DE ERRO DEVOLVE :   %        
    %      "4" => DIMENSAO NAO NUMERICA                        %        
    %      "5" => DIMENSAO IGUAL A ZERO                        %        
    %==========================================================%        
    COUNT:=2;                                                           
    SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                         
    IF COUNT NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE B[0] BY "004"; GO TO EXIT;                             
       END;                                                             
    DIMEN:=INTEGER(A[1],2);                                             
    IF DIMEN = 0 THEN                                                   
       BEGIN                                                            
         REPLACE B[0] BY "005"; GO TO EXIT;                             
       END;                                                             
    %=======================================================%           
    %   CONSISTENCIA DO CAMPO , EM CASO DE ERRO DEVOLVE :   %           
    %      "6" => CAMPO NAO NUMERICO                        %           
    %=======================================================%           
    COUNT:=DIMEN;                                                       
    SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                         
    IF COUNT NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE B[0] BY "006"; GO TO EXIT;                             
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO DIGITO , EM CASO DE ERRO DEVOLVE :   %          
    %      "7" => DIGITO INVALIDO                            %          
    %========================================================%          
    IF A[0] = "V" THEN                                                  
       BEGIN                                                            
         COUNT:=2;                                                      
         SCAN PB:PB FOR COUNT:COUNT WHILE IN NUMERO;                    
         IF COUNT NEQ 0 THEN                                            
            BEGIN                                                       
              REPLACE B[0] BY "007"; GO TO EXIT;                        
            END;                                                        
       END;                                                             
    %====================================================%              
    %   CALCULO DO DIGIT CHECK E VERIFICACAO DO DIGITO   %              
    %====================================================%              
    ACUM:=   2*INTEGER(A[3],1)                                          
           + 3*INTEGER(A[4],1)                                          
           + 4*INTEGER(A[5],1)                                          
           + 5*INTEGER(A[6],1)                                          
           + 6*INTEGER(A[7],1)                                          
           + 7*INTEGER(A[8],1)                                          
           + 8*INTEGER(A[9],1)                                          
           + 9*INTEGER(A[10],1)                                         
           +10*INTEGER(A[11],1)                                         
           + 0*INTEGER(A[12],1)                                         
           + 1*INTEGER(A[13],1)                                         
           + 2*INTEGER(A[14],1)                                         
           + 3*INTEGER(A[15],1)                                         
           + 4*INTEGER(A[16],1)                                         
           + 5*INTEGER(A[17],1)                                         
           + 6*INTEGER(A[18],1)                                         
           + 7*INTEGER(A[19],1)                                         
           + 8*INTEGER(A[20],1)                                         
           + 9*INTEGER(A[21],1)                                         
           +10*INTEGER(A[22],1)                                         
           + 0*INTEGER(A[23],1)                                         
           + 1*INTEGER(A[24],1)                                         
           + 2*INTEGER(A[25],1)                                         
           + 3*INTEGER(A[26],1)                                         
           + 4*INTEGER(A[27],1)                                         
           + 5*INTEGER(A[28],1)                                         
           + 6*INTEGER(A[29],1)                                         
           + 7*INTEGER(A[30],1)                                         
           + 8*INTEGER(A[31],1)                                         
           + 9*INTEGER(A[32],1);                                        
    D1:= IF ACUM MOD 11 = 10 THEN 1       % CALCULO DO DIGITO D1:       
          ELSE      (ACUM MOD 11);        %   R = 10 --> D1 = 1         
%   DISPLAY("D1 = " CAT STRING(D1,*));                                  
                                                                        
    ACUM:=0;                                                            
    ACUM:=   1*INTEGER(A[3],1)                                          
           + 2*INTEGER(A[4],1)                                          
           + 3*INTEGER(A[5],1)                                          
           + 4*INTEGER(A[6],1)                                          
           + 5*INTEGER(A[7],1)                                          
           + 6*INTEGER(A[8],1)                                          
           + 7*INTEGER(A[9],1)                                          
           + 8*INTEGER(A[10],1)                                         
           + 9*INTEGER(A[11],1)                                         
           +10*INTEGER(A[12],1)                                         
           + 0*INTEGER(A[13],1)                                         
           + 1*INTEGER(A[14],1)                                         
           + 2*INTEGER(A[15],1)                                         
           + 3*INTEGER(A[16],1)                                         
           + 4*INTEGER(A[17],1)                                         
           + 5*INTEGER(A[18],1)                                         
           + 6*INTEGER(A[19],1)                                         
           + 7*INTEGER(A[20],1)                                         
           + 8*INTEGER(A[21],1)                                         
           + 9*INTEGER(A[22],1)                                         
           +10*INTEGER(A[23],1)                                         
           + 0*INTEGER(A[24],1)                                         
           + 1*INTEGER(A[25],1)                                         
           + 2*INTEGER(A[26],1)                                         
           + 3*INTEGER(A[27],1)                                         
           + 4*INTEGER(A[28],1)                                         
           + 5*INTEGER(A[29],1)                                         
           + 6*INTEGER(A[30],1)                                         
           + 7*INTEGER(A[31],1)                                         
           + 8*INTEGER(A[32],1)                                         
           + 9*D1              ;                                        
    D2:= IF ACUM MOD 11 = 10 THEN 1       % CALCULO DO DIGITO D1:       
          ELSE      (ACUM MOD 11);        %   R = 10 --> D2 = 1         
%   DISPLAY("ACUM=" CAT STRING(ACUM,*));                                
%   DISPLAY("D2 = " CAT STRING(D2,*));                                  
                                                                        
    IF A[0] = "C" FOR 1 THEN                                            
       BEGIN                                                            
         REPLACE B[0] BY D1 FOR 1 DIGITS;                               
         REPLACE B[1] BY D2 FOR 1 DIGITS;                               
         REPLACE B[2] BY "2";                                           
       END                                                              
    ELSE                                                                
        IF INTEGER(B[0],1) = D1 AND                                     
           INTEGER(B[1],1) = D2 THEN                                    
           BEGIN                                                        
 %           REPLACE B[2] BY D1 FOR 1 DIGITS;                           
 %           REPLACE B[1] BY D2 FOR 1 DIGITS;                           
             REPLACE B[2] BY "0";                                       
           END                                                          
        ELSE                                                            
            REPLACE B[0] BY "001";                                      
    EXIT:                                                               
  END OF DIGITCERTID;                                                   
 $PAGE                                                                  
%-----------------------------------------------------------------------
%  INICIO DA LIBRARY:  DIGITITULO                                       
%                                                                       
%  CRIACAO DA LIBRARY 15/08/2019 A 09/09/2019                           
%                                                                       
%-----------------------------------------------------------------------
% 11. DIGITITULO                                                        
%                                                                       
% 11.01 - FUNCOES                                                       
%                                                                       
%       ESTA LIBRARY FAZ A CRIACAO OU VERIFICACAO DO DIGIT CHECK        
%       MODULO 11 PARA O TITULO DE ELEITOR COM 8 OU 9 BYTES (DIGITOS).  
%       O CHECK DIGIT E COMPOSTO POR 2 DIGITOS.                         
%                                                                       
% 11.02 - COMPOSICAO DO NUMERO DO TITULO                                
%                                                                       
%       NUMERO : XXXXXXXXXYYZW                                          
%                                                                       
%       ONDE :                                                          
%                                                                       
%       X = NUMERO SEQUENCIAL COM 9(NOVE) POSICOES.                     
%                                                                       
%       Y = SIGLA DO ESTADO COM 2(DUAS) POSICOES.                       
%                                                                       
%       AS SIGLAS DAS UF SAO:                                           
%                                                                       
%       01-SP, 02-MG, 03-RJ, 04-RS, 05-BA, 06-PR, 07-CE, 08-PE, 09-SC,  
%       10-GO, 11-MA, 12-PB, 13-PA, 14-ES, 15-PI, 16-RN, 17-AL, 18-MT,  
%       19-MS, 20-DF, 21-SE, 22-AM, 23-RO, 24-AC, 25-AP, 26-RR, 27-TO,  
%       28-EXTERIOR.                                                    
%                                                                       
%       Z = PRIMEIRO DIGITO VERIFICADOR 1(UMA) POSICAO.                 
%                                                                       
%       W = SEGUNDO  DIGITO VERIFICADOR 1(UMA) POSICAO.                 
%                                                                       
% 11.03 - FORMULA DE CALCULO                                            
%                                                                       
% 11.03.01 - APURACAO DO PRIMEIRO NUMERO DO DIGITO VERIFICADOR - D1     
%                                                                       
%       O CALCULO DO PRIMEIRO DIGITO E FEITO DA SEGUINTE FORMA:         
%                                                                       
%       SOMATORIA DA MULTIPLICACAO DA ESQUERDA PARA A DIREITA DE CADA   
%       UM DOS NOVE NUMEROS PELA SEGUINTE SEQUENCIA:                    
%       2, 9, 8, 7, 6, 5, 4, 3, E 2                                     
%                                                                       
%       EXEMPLO: TITULO N. 008368450                                    
%                                                                       
%       A)SOMATORIA DA MULTIPLICACAO                                    
%                                                                       
%       0 0 8 3 6 8 4 5 0 (NOVE DIGITOS)                                
%       x x x x x x x x x                                               
%       2 9 8 7 6 5 4 3 2                                               
%                                                                       
%       SOMATORIA = 0+0+64+21+36+40+16+15+0 = 192                       
%                                                                       
%       B) DIVIDIR O RESULTADO DA SOMA PELO MODULO 11.                  
%                                                                       
%       192/11 = 17 + (RESTO 5)                                         
%                                                                       
%       D1 = 11 - 5                                                     
%                                                                       
%       D1 = 6                                                          
%                                                                       
% 11.03.02 - APURACAO DO SEGUNDO NUMERO DO DIGITO VERIFICADOR - D2      
%                                                                       
%       O CALCULO DO SEGUNDO  DIGITO E FEITO DA SEGUINTE FORMA:         
%                                                                       
%       COLOCAR A DIREITA DA SIGLA DO ESTADO O PRIMEIRO DIGITO APURADO  
%       D1.                                                             
%                                                                       
%       SOMATORIA DA MULTIPLICACAO DA ESQUERDA PARA A DIREITA DE CADA   
%       UM DOS NUMEROS PELA SEGUINTE SEQUENCIA: 4, 3 E 2                
%                                                                       
%       EXEMPLO: SIGLA  01    (SAO PAULO)                               
%                                                                       
%                D1  =  6                                               
%                                                                       
%       A) SOMATORIA DA MULTIPLICACAO                                   
%                                                                       
%          016                                                          
%          xxx                                                          
%          432                                                          
%                                                                       
%    SOMATORIA = 0+3+12 = 15                                            
%                                                                       
%    B) DIVIDIR O RESULTADO DA SOMA PELO MODULO 11.                     
%                                                                       
%       15/11 = 1 + (RESTO 4)                                           
%                                                                       
%       D2 = 11 - 4                                                     
%                                                                       
%       D2 = 7                                                          
%                                                                       
% 11.04 - EXCECOES PARA O CALCULO DO D1 E D2.                           
%                                                                       
% 11.04.01 - PARA OS ESTADOS DE SAO PAULO (01) E MINAS GERAIS (02):     
%                                                                       
%       A) SE O RESTO DA DIVISAO FOR 0 ---> O VALOR DO DV SERA 1.       
%                                                                       
%       B) SE O RESTO DA DIVISAO FOR 1 ---> O VALOR DO DV SERA 0.       
%                                                                       
%       C) SE O DIVIDENDO FOR MENOR QUE O DIVISOR, CONSIDERAR COMO      
%          SENDO O RESTO O PROPRIO DIVIDENDO.                           
%                                                                       
% 11.04.02 - PARA OS DEMAIS ESTADOS:                                    
%                                                                       
%       A) SE O RESTO DA DIVISAO FOR 0 ---> O VALOR DO DV SERA 0.       
%                                                                       
%       B) SE O RESTO DA DIVISAO FOR 1 ---> O VALOR DO DV SERA 0.       
%                                                                       
% 11.05 - PARAMETROS                                                    
%                                                                       
% 11.05.01 - OS PARAMETROS SERAO PASSADOS PARA A LIBRARY DA SEGUINTE    
%            FORMA.                                                     
%                                                                       
%       AX-CAMPO1                                                       
%                                                                       
%       AX-CODIGO   - "C" (CRIACAO) OU "V" (VERIFICACAO)                
%                                                                       
%       AX-DIMENSAO - QUANTIDADE DE NUMEROS QUE COMPOEM O TITULO.       
%                     NUMERO FIXO. VALUE 9.                             
%                                                                       
%       AX-NUMERO   - NUMERO DO TITULO QUE SERA CALCULADO O DIGIT       
%                     CHECK. SE NECESSARIO PREENCHER COM  ZERO(S)       
%                     A ESQUERDA, OU SEJA SEMPRE COM 9 DIGITOS.         
%                                                                       
%       AX-ESTADO   - CODIGO DO ESTADO.                                 
%                                                                       
%       AX-CAMPO2                                                       
%                                                                       
%       AX-DIGITCHECK - DIGIT CHECK CALCULADO OU VERIFICADO             
%                       PELA ROTINA                                     
%                                                                       
%       AX-CODRETORNO - CODIGO DE RETORNO DADO PELA ROTINA.             
%                       PODERA SER:                                     
%                                                                       
%                       0 -> DIGIT CHECK CORRETO (OPCAO "V")            
%                       1 -> DIGIT CHECK ERRADO  (OPCAO "V")            
%                       2 -> DIGIT CHECK CALCULADO (OPCAO "C")          
%                       3 -> CODIGO DIFERENTE DE C OU V                 
%                       4 => DIMENSAO NAO NUMERICA                      
%                       5 => DIMENSAO IGUAL A ZERO                      
%                       6 => AX-TITULO NAO NUMERICO                     
%                       7 => CODIGO DO ESTADO NAO NUMERICO              
%                       8 => DIGIT CHECK NAO NUMERICO                   
%                                                                       
% 11.06 - EXEMPLO PROGRAMA COBOL                                        
%                                                                       
%       WORKING-STORAGE  SECTION.                                       
%                                                                       
%       01  AX-CAMPO1.                                                  
%              05    AX-CODIGO           PIC X(01).                     
%              05    AX-DIMENSAO         PIC 9(01) VALUE 9.             
%              05    AX-TITULO           PIC 9(9).                      
%              05    AX-ESTADO           PIC 9(2).                      
%                                                                       
%       01  AX-CAMPO2.                                                  
%              05    AX-DIGITCHECK      PIC X(02).                      
%              05    AX-CODRETORNO      PIC 9(01).                      
%                                                                       
%       PROCEDURE  DIVISION.                                            
%       CALL   "DIGITITULO OF   PC/LIB/DIGITCHECK"                      
%                               USING  AX-CAMPO1                        
%                                      AX-CAMPO2.                       
%                                                                       
%       STOP   RUN.                                                     
%                                                                       
%                                                                       
  PROCEDURE DIGITITULO(A,B);                                            
  EBCDIC ARRAY A, B[0];                                                 
  BEGIN                                                                 
    POINTER PA,PB; LABEL EXIT;                                          
    INTEGER COUNT,DIMEN,POSF,ACUM,D1,D2,I,J,RESTO;                      
    TRUTHSET CODIGO ("CV"), NUMERO("0123456789");                       
    PA:=A; PB:=B;                                                       
    %========================================================%          
    %   CONSISTENCIA DO CODIGO, EM CASO DE ERRO DEVOLVE :    %          
    %      "3" => CODIGO INVALIDO                            %          
    %========================================================%          
    COUNT:=1;                                                           
    SCAN PA:PA FOR COUNT:COUNT WHILE IN CODIGO;                         
    IF COUNT NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE B[0] BY "003"; GO TO EXIT;                             
       END;                                                             
    %==========================================================%        
    %   CONSISTENCIA DA DIMENSAO, EM CASO DE ERRO DEVOLVE :    %        
    %      "4" => DIMENSAO NAO NUMERICA                        %        
    %      "5" => DIMENSAO IGUAL A ZERO                        %        
    %==========================================================%        
    COUNT:=1;                                                           
    SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                         
    IF COUNT NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE B[0] BY "004"; GO TO EXIT;                             
       END;                                                             
    DIMEN:=INTEGER(A[1],1);                                             
    IF DIMEN = 0 THEN                                                   
       BEGIN                                                            
         REPLACE B[0] BY "005"; GO TO EXIT;                             
       END;                                                             
    %=======================================================%           
    %   CONSISTENCIA DO CAMPO , EM CASO DE ERRO DEVOLVE :   %           
    %      "6" => CAMPO NAO NUMERICO                        %           
    %=======================================================%           
    COUNT:=DIMEN;                                                       
    SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                         
    IF COUNT NEQ 0 THEN                                                 
       BEGIN                                                            
         REPLACE B[0] BY "006"; GO TO EXIT;                             
       END;                                                             
    %========================================================%          
    %   CONSISTENCIA DO ESTADO, EM CASO DE ERRO DEVOLVE :    %          
    %      "7" => CODIGO DO ESTADO NAO NUMERICO.             %          
    %========================================================%          
    COUNT:=2;                                                           
    SCAN PA:PA FOR COUNT:COUNT WHILE IN NUMERO;                         
    IF COUNT NEQ 0 THEN                                                 
     BEGIN                                                              
      REPLACE B[0] BY "007"; GO TO EXIT;                                
     END;                                                               
    %========================================================%          
    %   CONSISTENCIA DO DIGITO , EM CASO DE ERRO DEVOLVE :   %          
    %      "8" => DIGITO INVALIDO                            %          
    %========================================================%          
    IF A[0] = "V" THEN                                                  
       BEGIN                                                            
         COUNT:=2;                                                      
         SCAN PB:PB FOR COUNT:COUNT WHILE IN NUMERO;                    
         IF COUNT NEQ 0 THEN                                            
            BEGIN                                                       
              REPLACE B[0] BY "008"; GO TO EXIT;                        
            END;                                                        
       END;                                                             
    %====================================================%              
    %   CALCULO DO DIGIT CHECK E VERIFICACAO DO DIGITO   %              
    %====================================================%              
                                                                        
    %   CALCULO DE D1                                                   
                                                                        
    ACUM:=   2*INTEGER(A[2],1)                                          
           + 9*INTEGER(A[3],1)                                          
           + 8*INTEGER(A[4],1)                                          
           + 7*INTEGER(A[5],1)                                          
           + 6*INTEGER(A[6],1)                                          
           + 5*INTEGER(A[7],1)                                          
           + 4*INTEGER(A[8],1)                                          
           + 3*INTEGER(A[9],1)                                          
           + 2*INTEGER(A[10],1);                                        
                                                                        
%   DISPLAY("188400 ACUM D1 =  " CAT STRING(ACUM,*));                   
                                                                        
    IF ACUM LSS 11 % DIVIDENDO MENOR DO QUE 11                          
     THEN                                                               
      BEGIN                                                             
%      DISPLAY("188900 - D1 - DIVIDENDO MENOR DO QUE 11");              
       RESTO:= ACUM % CONSIDERAR O RESTO IGUAL AO DIVIDENDO             
      END                                                               
     ELSE                                                               
      BEGIN                                                             
       RESTO:= ACUM MOD 11; % DIVIDENDO IGUAL OU MAIOR DO QUE 11        
%      DISPLAY("189500  RESTO D1 = " CAT STRING(RESTO,*));              
      END;                                                              
    IF RESTO LSS 2   % PODE SER 0 OU 1                                  
     THEN                                                               
      BEGIN %                                                           
       IF INTEGER(A[11],2) LSS 03  % ESTADO PODE SER 01(SP) OU 02(MG)   
        THEN                                                            
         BEGIN                                                          
          IF RESTO EQL 0 % CONDICAO: RESTO = 0 E O ESTADO = 01 OU 02    
           THEN                                                         
            BEGIN                                                       
             D1:= 1                                                     
            END                                                         
           ELSE                                                         
            BEGIN                                                       
             D1:= 0                                                     
            END                                                         
         END                                                            
        ELSE  % ESTADO DIFERENTE DE 01 E 02                             
         BEGIN                                                          
%         DISPLAY("ESTADO DIFERENTE DE 1 OU 2");                        
          D1:= 0;                                                       
%         DISPLAY("D1   = " CAT STRING(D1  ,*));                        
         END                                                            
      END                                                               
     ELSE                                                               
      BEGIN                                                             
       D1:= 11 - RESTO;                                                 
%      DISPLAY("192300 D1   = " CAT STRING(D1  ,*));                    
      END;                                                              
    %   CALCULO DE D2                                                   
                                                                        
    ACUM:=   4*INTEGER(A[11],1)                                         
           + 3*INTEGER(A[12],1)                                         
           + 2*D1;                                                      
    IF ACUM LSS 11 % DIVIDENDO MENOR DO QUE 11                          
     THEN                                                               
      BEGIN                                                             
%      DISPLAY("193300 D2 - DIVIDENDO MENOR DO QUE 11");                
       RESTO:= ACUM % CONSIDERAR O RESTO IGUAL AO DIVIDENDO             
      END                                                               
     ELSE                                                               
      BEGIN                                                             
       RESTO:= ACUM MOD 11; % DIVIDENDO IGUAL OU MAIOR DO QUE 11        
%      DISPLAY("193900 RESTO D2 = " CAT STRING(RESTO,*));               
      END;                                                              
    IF RESTO LSS 2   % PODE SER 0 OU 1                                  
     THEN                                                               
      BEGIN %                                                           
       IF INTEGER(A[11],2) LSS 03  % ESTADO PODE SER 01(SP) OU 02(MG)   
        THEN                                                            
         BEGIN                                                          
          IF RESTO EQL 0 % CONDICAO: RESTO = 0 E O ESTADO = 01 OU 02    
           THEN                                                         
            BEGIN                                                       
             D2:= 1;                                                    
%            DISPLAY("195100 RESTO DE D2 =>" CAT STRING(RESTO,*));      
%            DISPLAY("195200 ENTAO D2 =>" CAT STRING(D2,*));            
            END                                                         
           ELSE                                                         
            BEGIN                                                       
             D2:= 0;                                                    
%            DISPLAY("195700 RESTO DE D2 =>" CAT STRING(RESTO,*));      
%            DISPLAY("195800 ENTAO D2 =>" CAT STRING(D2,*));            
            END                                                         
         END                                                            
        ELSE  % ESTADO DIFERENTE DE 01 E 02                             
         BEGIN                                                          
          D2:= 0;                                                       
%         DISPLAY("D2   = " CAT STRING(D2  ,*));                        
         END                                                            
      END                                                               
     ELSE                                                               
      BEGIN                                                             
       D2:= 11 - RESTO;                                                 
%      DISPLAY("D2   = " CAT STRING(D2  ,*));                           
      END;                                                              
%   DISPLAY("ACUM D2 =  " CAT STRING(ACUM,*));                          
%   DISPLAY("ACUM=" CAT STRING(ACUM,*));                                
%   DISPLAY("D2 = " CAT STRING(D2,*));                                  
                                                                        
    IF A[0] = "C" FOR 1 THEN                                            
       BEGIN                                                            
         REPLACE B[0] BY D1 FOR 1 DIGITS;                               
         REPLACE B[1] BY D2 FOR 1 DIGITS;                               
         REPLACE B[2] BY "2";                                           
       END                                                              
    ELSE                                                                
        IF INTEGER(B[0],1) = D1 AND                                     
           INTEGER(B[1],1) = D2 THEN                                    
           BEGIN                                                        
 %           REPLACE B[2] BY D1 FOR 1 DIGITS;                           
 %           REPLACE B[1] BY D2 FOR 1 DIGITS;                           
             REPLACE B[2] BY "0";                                       
           END                                                          
        ELSE                                                            
            REPLACE B[0] BY "001";                                      
    EXIT:                                                               
  END OF DIGITITULO;                                                    
 $PAGE                                                                  
                                                                        
EXPORT DIGITPASEP ,                                                     
       DIGITCGC   ,                                                     
       DIGITCPF   ,                                                     
       DIGITM10   ,                                                     
       DIGITIPVA21,                                                     
       DIGITIPVA  ,                                                     
       DIGITM11   ,                                                     
       DIGITCID   ,                                                     
       DIGITRENACH,                                                     
       DIGITSEDEX ,                                                     
       DIGITDUT   ,                                                     
       DIGITCERTID,                                                     
       DIGITITULO;                                                      
FREEZE (TEMPORARY);                                                     
                                                                        
END.                                                                    
