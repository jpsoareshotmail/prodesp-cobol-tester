 $SET SHARING = SHAREDBYALL                                             
                                                                        
BEGIN                                                                   
%--------------------------------------------------------------------%  
%   LIBRARY  :  PF/LIB/CONVERTCHARACTER/000                          %  
%               PC/LIB/CONVERTCHARACTER                              %  
%                                                                    %  
%                                                                    %  
%  V=001  24/JAN/91  INCLUSAO DA ROTINA "SUBTRADUZ" E CORRE[]O NO    %  
%                    TRANSLATETABLE DO "TRADUZ" ("]" POR "'").       %  
%                                                        LINA        %  
%  V=002  30/JUL/92  TEMPORARY PARA PERMANENT. CODIGO GERADO SO NO   %  
%                    A5.                                             %  
%                                                                    %  
%  V=003  14/JUN/94  INCLUSAO DAS ROTINAS TEXT_TO_BIN E BIN_TO_TEXT  %  
%                    (UTILIZADAS EM SISTEMAS MICRO UTILIZANDO APIS)  %  
%                                                                    %  
%  V=004    /NOV/94  INCLUSAO DA ROTINA ASCII_TO_EBCDIC              %  
%                    (UTILIZADAS EM SISTEMAS QUE GRAVAM CARACTERES   %  
%                    PELA TEXT_TO_BIN E PRECISAM EXIBIR DADOS   EM   %  
%                    TERMINAIS DE VIDEO.                             %  
%                                        DPP-CECILIA                 %  
%                                                                    %  
% V=005   24/OUT/99  INCLUSAO DA ROTINA EBCDIC_TO_ASC                %  
%                                                                    %  
%   ESTA LIBRARY FOI GERADA PARA SUBSTITUIR AS SUBROUTINAS:          %  
%                                                                    %  
%   - OTIMIZA                                                        %  
%   - SUBTRADUZ                                                      %  
%   - TRADUZ                                                         %  
%   - HEXTOEBC                                                       %  
%   - BCLPARAEBCDIC                                                  %  
%   - EBCDICPARABCL                                                  %  
%   - TEXT_TO_BIN                                                    %  
%   - BIN_TO_TEXT                                                    %  
%   - EBCDIC_TO_ASC                                                  %  
%                                                 DORIAN :  10/12/90 %  
%--------------------------------------------------------------------%  
  $PAGE                                                                 
 %-------------------------------------------------------------------%  
 %    INICIO DA LIBRARY  :  BCLPARAEBCDIC                            %  
 %                                                                   %  
 %    LIBRARY GERADA A PARTIR DO FONTE : "PF/LIB/BCLPARAEBCDIC/003"  %  
 %    CRIADA EM "31/07/90                                            %  
 %                                                                   %  
 %    ABAIXO TABELA DA CONFIGURA[]O INTERNA                          %  
 %                                                                   %  
 %-------------------  CONFIGURA[]O INTERNA  ------------------------%  
 %                                                                   %  
 %       BCL      EBCDIC                BCL      EBCDIC              %  
 %                                                                   %  
 %      000000   11110000   0          000001   11110001   1         %  
 %      000010   11110010   2          000011   11110011   3         %  
 %      000100   11110100   4          000101   11110101   5         %  
 %      000110   11110110   6          000111   11110111   7         %  
 %      001000   11111000   8          001001   11111001   9         %  
 %      001010   01111011   #          001011   01111100   @         %  
 %      001100   01101111   ?          001100   01111001   `         %  
 %      001101   01111010   :          001110   01101110   >         %  
 %      001111   01111101   '          010000   01001110   +         %  
 %      010001   11000001   A          010010   11000010   B         %  
 %      010011   11000011   C          010100   11000100   D         %  
 %      010101   11000101   E          010110   11000110   F         %  
 %      010111   11000111   G          011000   11001000   H         %  
 %      011001   11001001   I          011010   01001011   .         %  
 %      011011   01001010   [          011100   01010000   &         %  
 %      011101   01001101   (          011110   01001100   <         %  
 %      011111   01001111   !          100001   11010001   J         %  
 %      100010   11010010   K          100011   11010011   L         %  
 %      100100   11010100   M          100101   11010101   N         %  
 %      100110   11010110   O          100111   11010111   P         %  
 %      101000   11011000   Q          101001   11011001   R         %  
 %      101010   01011011   $          101011   01011100   *         %  
 %      101100   01100000   -          101101   01011101   )         %  
 %      101110   01011110   ;          110001   01100001   /         %  
 %      110010   11100010   S          110011   11100011   T         %  
 %      110100   11100100   U          110101   11100101   V         %  
 %      110110   11100110   W          110111   11100111   X         %  
 %      111000   11101000   Y          111001   11101001   Z         %  
 %      111010   01101011   ,          111011   01101100   %         %  
 %      111100   01101101   _          111101   01111110   =         %  
 %      111110   01011010   ]          111111   01111111   "         %  
 %                                                                   %  
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
 $PAGE                                                                  
 PROCEDURE BCLPARAEBCDIC(BCL01,EBCDIC01);                               
  EBCDIC ARRAY BCL01[0],EBCDIC01[0];                                    
  BEGIN                                                                 
   ARRAY PROV[0] = BCL01[*];                                            
   DEFINE BCLCHAR(A,C) = A[(C) DIV 8].[47-((C) MOD 8)*6:6] #;           
   VALUE ARRAY                                                          
        FROMBCLTOEBCDIC(                                                
                       48"F0F1F2F3F4F5F6F7F8F97B7C6F7A6E7D4EC1"  % 00-17
                      ,48"C2C3C4C5C6C7C8C94B4A504D4C4FD0D1D2D3"  % 18-35
                      ,48"D4D5D6D7D8D95B5C605D5E5F4061E2E3E4E5"  % 36-53
                      ,48"E6E7E8E96B6C6D7E5A7F");                % 54-64
   POINTER PTCOMUM;                                                     
   REAL BCLSZ   ,                                                       
        EBCDICSZ;                                                       
   INTEGER TEMP,BCLCHAROFFSET;                                          
   PTCOMUM:=BCL01[0];                                                   
   BCLSZ  :=SIZE(BCL01);                                                
   PTCOMUM:=EBCDIC01[0];                                                
   EBCDICSZ :=SIZE(EBCDIC01);                                           
   IF BCL01[0] = " "  FOR BCLSZ                                         
   THEN REPLACE EBCDIC01[0] BY " " FOR EBCDICSZ                         
    ELSE                                                                
     BEGIN                                                              
      PTCOMUM:=EBCDIC01[0];                                             
      BCLCHAROFFSET:=0;                                                 
      WHILE EBCDICSZ > 0 DO                                             
       BEGIN                                                            
        TEMP := BCLCHAR(PROV,BCLCHAROFFSET);                            
        REPLACE PTCOMUM:PTCOMUM BY 0 & FROMBCLTOEBCDIC                  
         [TEMP DIV 6] [47:(47-((TEMP MOD 6)*8)):8] FOR 1;               
        EBCDICSZ:=*-1;                                                  
        BCLCHAROFFSET:=*+1;                                             
       END;                                                             
     END;                                                               
 END;                                                                   
                                                                        
                                                                        
 $PAGE                                                                  
 %-------------------------------------------------------------------%  
 %    INICIO DA LIBRARY  :  EBCDICPARABCL                            %  
 %                                                                   %  
 %    LIBRARY GERADA A PARTIR DO FONTE : "PF/LIB/EBCDICPARABCL/003"  %  
 %    CRIADA EM "31/07/90"                                           %  
 %                                                                   %  
 %    ABAIXO TABELA DA CONFIGURA[]O INTERNA                          %  
 %                                                                   %  
 %--------------------  CONFIGURA[]O INTERNA   ----------------------%  
 %                                                                   %  
 %            EBCDIC     BCL                EBCDIC     BCL           %  
 %                                                                   %  
 %       [   01001010   011011         .   01001011   011010         %  
 %       <   01001100   011110         (   01001101   011101         %  
 %       +   01001110   010000         !   01001111   011111         %  
 %       &   01010000   011100         ]   01011010   111110         %  
 %       $   01011011   101010         *   01011100   101011         %  
 %       )   01011101   101101         ;   01011110   101110         %  
 %       -   01100000   101100         /   01100001   110001         %  
 %       ,   01101011   111010         %   01101100   111011         %  
 %       _   01101101   111100         >   01101110   001110         %  
 %       ?   01101111   001100         `   01111001   001100         %  
 %       :   01111010   001101         #   01111011   001010         %  
 %       #   01111011   001010         @   01111100   001011         %  
 %       '   01111101   001111         =   01111110   111101         %  
 %       "   01111111   111111         A   11000001   010001         %  
 %       B   11000010   010010         C   11000011   010011         %  
 %       D   11000100   010100         E   11000101   010101         %  
 %       F   11000110   010110         G   11000111   010111         %  
 %       H   11001000   011000         I   11001001   011001         %  
 %       J   11010001   100001         K   11010010   100010         %  
 %       L   11010011   100011         M   11010100   100100         %  
 %       N   11010101   100101         O   11010110   100110         %  
 %       P   11010111   100111         Q   11011000   101000         %  
 %       Q   11011000   101000         R   11011001   101001         %  
 %       S   11100010   110010         T   11100011   110011         %  
 %       U   11100100   110100         V   11100101   110101         %  
 %       W   11100110   110110         X   11100111   110111         %  
 %       Y   11101000   111000         Z   11101001   111001         %  
 %       0   11110000   000000         1   11110001   000001         %  
 %       2   11110010   000010         3   11110011   000011         %  
 %       4   11110100   000100         5   11110101   000101         %  
 %       6   11110110   000110         7   11110111   000111         %  
 %       8   11111000   001000         9   11111001   001001         %  
 %                                                                   %  
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
 $PAGE                                                                  
                                                                        
 PROCEDURE EBCDICPARABCL(EBCDIC01,BCL01);                               
  EBCDIC ARRAY EBCDIC01[0],BCL01[0];                                    
  BEGIN                                                                 
   ARRAY PROV[0] = BCL01[*];                                            
   DEFINE EBCDICCHAR(A,C) = A[(C) DIV 8].[47-((C) MOD 8)*6:6] #;        
   VALUE ARRAY                                                          
    FROMEBCDICTOBCL(                                                    
        48"30C30C30C30C30C30C30C30C"              % 000-015             
       ,48"30C30C30C30C30C30C30C30C"              % 016-031             
       ,48"30C30C30C30C30C30C30C30C"              % 032-047             
       ,48"30C30C30C30C30C30C30C30C"              % 048-063             
       ,48"C0C30C30C30C7EF6DA79D41F"              % 064-079             
       ,48"70C30C30C30C33CFAAAEDBAF"              % 080-095             
       ,48"B3130C30C30C30F33AEFC38C"              % 096-111             
       ,48"30C30C30C30C30C34A2CFF7F"              % 112-127             
       ,48"30C30C30C30C30C30C30C30C"              % 128-143             
       ,48"30C30C30C30C30C30C30C30C"              % 144-159             
       ,48"30C30C30C30C30C30C30C30C"              % 160-175             
       ,48"30C30C30C30C30C30C30C30C"              % 176-191             
       ,48"41149351559761930C30C30C"              % 192-207             
       ,48"8218A39259A7A2930C30C30C"              % 208-223             
       ,48"80CCB3D35DB7E3930C30C30C"              % 224-239             
       ,48"00108310518720930C30C30C"              % 240-255             
       );                                                               
   POINTER EBCDICPTR;                                                   
   REAL EBCDICSZ ,                                                      
        BCLSZ    ;                                                      
   INTEGER EBCDICCHAROFFSET;                                            
   EBCDICSZ:=SIZE(EBCDIC01);                                            
   BCLSZ   :=SIZE(BCL01);                                               
   IF EBCDIC01[0] = " " FOR EBCDICSZ                                    
    THEN REPLACE BCL01[0] BY " " FOR BCLSZ                              
    ELSE                                                                
     BEGIN                                                              
      EBCDICPTR:=EBCDIC01[0];                                           
      EBCDICCHAROFFSET:=0;                                              
      WHILE EBCDICSZ > 0 DO                                             
       BEGIN                                                            
        EBCDICCHAR(PROV,EBCDICCHAROFFSET):=          % 016-031          
         EBCDICCHAR(FROMEBCDICTOBCL,REAL(EBCDICPTR,1));                 
        EBCDICPTR:=*+1;                                                 
        EBCDICCHAROFFSET:=*+1;                                          
        EBCDICSZ:=*-1;                                                  
       END;                                                             
     END;                                                               
  END;                                                                  
 $PAGE                                                                  
 %-------------------------------------------------------------------%  
 %    INICIO DA LIBRARY  :  HEXTOEBC                                 %  
 %                                                                   %  
 %    LIBRARY GERADA A PARTIR DO FONTE : "PF/LIB/HEXTOEBC/001"       %  
 %    CRIADA EM "19/11/87"                                           %  
 %-------------------------------------------------------------------%  
                                                                        
                                                                        
                                                                        
PROCEDURE HEXTOEBC (AHEX,AEBC,TAM);                                     
  EBCDIC ARRAY AHEX[0];                                                 
  EBCDIC ARRAY AEBC[0];                                                 
  INTEGER TAM;                                                          
BEGIN                                                                   
  HEX    ARRAY TEMP[0]=AHEX;                                            
  REPLACE AEBC BY TEMP FOR TAM WITH HEXTOEBCDIC;                        
END OF HEXTOEBC;                                                        
                                                                        
                                                                        
 $PAGE                                                                  
 %-------------------------------------------------------------------%  
 %    INICIO DA LIBRARY  :  OTIMIZA                                  %  
 %                                                                   %  
 %    LIBRARY GERADA A PARTIR DO FONTE : "PF/SUB/OTIMIZA/001"        %  
 %    CRIADA EM "16/07/86"                                           %  
 %-------------------------------------------------------------------%  
                                                                        
                                                                        
 PROCEDURE OTIMIZA(E,F,C);                                              
 EBCDIC ARRAY E[0],F[0],C[0];                                           
   BEGIN %                                                              
 REAL ARRAY A[0:4],B[0:3];                                              
     INTEGER I; %                                                       
     INTEGER CONT;                                                      
     REAL J; %                                                          
       POINTER PA,PB,PC;                                                
     TRUTHSET TRU(ALPHA AND NOT "0123456789" OR ".&-,'" OR 48"0040");   
     TRANSLATETABLE TRANS("ABCDEFGHIJKLMNOPQRSTUVWXYZ.&-,'" TO          
          48"0102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1
E1F"); %                                                                
 REPLACE A BY E FOR 30;                                                 
     SCAN PA:=A[0] FOR CONT:30 WHILE IN TRU;                            
     IF CONT NEQ 0 THEN                                                 
      REPLACE C[0] BY "N" FOR 1                                         
     ELSE BEGIN %                                                       
      REPLACE PA:=A[0] BY PB:=A[0] FOR 30 WITH TRANS; %                 
      FOR I:=0 STEP 1 UNTIL 29 DO                                       
        IF 48 - (I*5) MOD 48 < 5 THEN                                   
          BEGIN                                                         
            J:=(I*5) MOD 48;                                            
            B[(I*5) DIV 48].[47-J:48-J]:=                               
            A[I DIV 6].[44-(I MOD 6)*8:48-J];                           
            B[(I*5) DIV 48 + 1].[47:5+J-48]:=                           
            A[ I DIV 6].[44-(I MOD 6)*8+J-48:5+J-48];                   
          END ELSE                                                      
            B[(I*5) DIV 48].[47-(I*5) MOD 48:5]:=                       
            A[I DIV 6].[44-(I MOD 6)*8:5];                              
      REPLACE C[0] BY "S" FOR 1;                                        
       B[3].[41:2]:=0; %                                                
 REPLACE F BY POINTER(B) FOR 19;                                        
       END;                                                             
   END;                                                                 
 $PAGE                                                                  
 %-------------------------------------------------------------------%  
 %    INICIO DA LIBRARY  :  SUBTRADUZ                                %  
 %                                                                   %  
 %    LIBRARY GERADA A PARTIR DO FONTE : "PF/SUB/TRADUZ/001"         %  
 %    CRIADA EM "16/07/86"                                           %  
 %-------------------------------------------------------------------%  
                                                                        
 PROCEDURE SUBTRADUZ(E,F); %                                            
                                                                        
 EBCDIC ARRAY E[0],F[0];                                                
                                                                        
 BEGIN                                                                  
ARRAY B[0] = E[*];                                                      
     ARRAY A[0:4];                                                      
   TRANSLATETABLE TRANS(48"000102030405060708090A0B0C0D0E0F1011121314151
61718191A1B1C1D1E1F" TO " ABCDEFGHIJKLMNOPQRSTUVWXYZ.&-,'");            
                                                                        
   INTEGER I;                                                           
                                                                        
   REAL J;                                                              
   REPLACE     A[0] BY 48"00" FOR 30;                                   
      FOR I:=0 STEP 1 UNTIL 29 DO                                       
      IF 48 - (I*5) MOD 48 < 5 THEN                                     
        BEGIN                                                           
        J:=(I*5) MOD 48;                                                
        A[I DIV 6].[44 - (I MOD 6)*8:48-J]:=                            
        B[(I*5) DIV 48].[47-J:48-J];                                    
        A[I DIV 6].[44-(I MOD 6)*8+J-48:5+J-48]:=                       
        B[(I*5) DIV 48+1].[47:5+J-48];                                  
        END ELSE                                                        
        A[I DIV 6].[44-(I MOD 6)*8:5]:=                                 
        B[(I*5) DIV 48].[47-(I*5) MOD 48:5];                            
 REPLACE F BY A FOR 30 WITH TRANS;                                      
 END;                                                                   
 $PAGE                                                                  
 %-------------------------------------------------------------------%  
 %    INICIO DA LIBRARY  :  TRADUZ                                   %  
 %                                                                   %  
 %    LIBRARY GERADA A PARTIR DO FONTE : "PF/LIB/TRADUZ/002"         %  
 %    CRIADA EM "17/08/90"                                           %  
 %-------------------------------------------------------------------%  
                                                                        
 PROCEDURE TRADUZ(E,F,R); %                                             
                                                                        
 EBCDIC ARRAY E[0],F[0],R[0];                                           
                                                                        
 BEGIN                                                                  
                                                                        
   ARRAY B [0:18];                                                      
   ARRAY A [0:4];                                                       
   ARRAY TR[0:4];                                                       
                                                                        
   TRANSLATETABLE TRANS(48"000102030405060708090A0B0C0D0E0F1011121314151
61718191A1B1C1D1E1F" TO " ABCDEFGHIJKLMNOPQRSTUVWXYZ.&-,'");            
                                                                        
   TRANSLATETABLE TROCA (EBCDIC TO EBCDIC,                              
                         ","    TO "C"   ,                              
                         "-"    TO "A"   ,                              
                         "'"    TO " "   ,                              
                         "."    TO "O");                                
                                                                        
   INTEGER I,T;                                                         
                                                                        
   REAL J;                                                              
                                                                        
   LABEL FIM;                                                           
                                                                        
   IF (SIZE(F) DIV 30)  <  (SIZE(E) DIV 19) THEN                        
      BEGIN                                                             
        REPLACE R BY "1";   %AREA DE SAIDA INCOMPATIVEL COM A ENTRADA   
        GO TO FIM;                                                      
      END;                                                              
                                                                        
   FOR T := 0 STEP 19 UNTIL (SIZE(E) -19)  DO                           
     BEGIN                                                              
       REPLACE B[0] BY E[T]  FOR 19;                                    
       REPLACE A[0] BY 48"00" FOR 30;                                   
       IF B    NEQ " " FOR 19 THEN                                      
          FOR I:=0 STEP 1 UNTIL 29 DO                                   
           BEGIN                                                        
             IF 48 - (I*5) MOD 48 < 5 THEN                              
                BEGIN                                                   
                  J:=(I*5) MOD 48;                                      
                  A[I DIV 6].[44 - (I MOD 6)*8:48-J]:=                  
                  B[(I*5) DIV 48].[47-J:48-J];                          
                  A[I DIV 6].[44-(I MOD 6)*8+J-48:5+J-48]:=             
                  B[(I*5) DIV 48+1].[47:5+J-48];                        
                END                                                     
             ELSE                                                       
                  A[I DIV 6].[44-(I MOD 6)*8:5]:=                       
                  B[(I*5) DIV 48].[47-(I*5) MOD 48:5];                  
           END;                                                         
                                                                        
       REPLACE TR             BY A  FOR 30 WITH TRANS;                  
                                                                        
       REPLACE F[((T/19)*30)] BY TR FOR 30 WITH TROCA;                  
                                                                        
     END;                                                               
                                                                        
 REPLACE R BY " ";                                                      
                                                                        
 FIM:                                                                   
                                                                        
 END;                                                                   
 $ PAGE                                                                 
  PROCEDURE TEXT_TO_BIN(TEXTOIN,TAMANHO);                               
  %------------------------------------                                 
  EBCDIC  ARRAY   TEXTOIN[0];                                           
  INTEGER TAMANHO;                                                      
  BEGIN                                                                 
    %-------------------------------------------------%                 
    % Converte caracteres seguidos de <DLE> (10-HEXA) %                 
    %-------------------------------------------------%                 
                                                                        
    ARRAY TEXTO[0]=TEXTOIN[*];                                          
                                                                        
    INTEGER SALVATAM,                                                   
             VARREEBCDIC;                                               
                                                                        
    POINTER PTEXTO,                                                     
             PMODTEXT;                                                  
                                                                        
    DEFINE  HEXA1   = POINTER(TEXTO[0],4)+((OFFSET(PTEXTO)*2)+3)#,      
            HEXA2   = POINTER(TEXTO[0],4)+((OFFSET(PTEXTO)*2)+5)#,      
            P4TEXTO = POINTER(TEXTO[0],4)+(OFFSET(PTEXTO)*2)#,          
                                                                        
            DLE     = 48"10"#,                                          
                                                                        
            TAB_EBC = 48"404F7F7B5B6C507D4D5D5C4E6B604B61"              
                      48"F0F1F2F3F4F5F6F7F8F97A5E4C7E6E6F"              
                      48"7CC1C2C3C4C5C6C7C8C9D1D2D3D4D5D6"              
                      48"D7D8D9E2E3E4E5E6E7E8E94AE05A5F6D"              
                      48"79818283848586878889919293949596"              
                      48"979899A2A3A4A5A6A7A8A9C06AD0A107"#,            
                                                                        
            TAB_ASC = 48"202122232425262728292A2B2C2D2E2F"              
                      48"303132333435363738393A3B3C3D3E3F"              
                      48"404142434445464748494A4B4C4D4E4F"              
                      48"505152535455565758595A5B5C5D5E5F"              
                      48"606162636465666768696A6B6C6D6E6F"              
                      48"707172737475767778797A7B7C7D7E7F"#;            
    % Translate declarations                                            
                                                                        
    TRANSLATETABLE EBCDIC_TO_ASCII (                                    
        TAB_EBC TO TAB_ASC                                              
                                   );                                   
                                                                        
    TRANSLATETABLE EBCDIC_TO_3X(                                        
        EBCDIC TO EBCDIC,                                               
        48"7A5E4C7E6E6F" TO 48"3A3B3C3D3E3F"                            
                               );                                       
                                                                        
    PTEXTO:=TEXTO[0];                                                   
                                                                        
    IF TAMANHO > SIZE(TEXTOIN) THEN                                     
       TAMANHO:=SIZE(TEXTOIN);                                          
    SALVATAM:=TAMANHO;                                                  
                                                                        
    WHILE TAMANHO > 0 DO                                                
       BEGIN                                                            
         VARREEBCDIC:=TAMANHO;                                          
         SCAN PTEXTO  FOR TAMANHO:TAMANHO  UNTIL EQL DLE;               
         VARREEBCDIC:=*-TAMANHO;                                        
         REPLACE PTEXTO:PTEXTO BY PTEXTO  FOR VARREEBCDIC               
                                          WITH EBCDIC_TO_ASCII;         
         IF  TAMANHO > 0 THEN                                           
             BEGIN                                                      
              REPLACE PTEXTO+1 BY PTEXTO+1 FOR 2 WITH EBCDIC_TO_3X;     
              REPLACE P4TEXTO BY HEXA1 FOR 1,                           
                                 HEXA2 FOR 1;                           
              TAMANHO:= *-3;                                            
                                                                        
              IF TAMANHO > 0  THEN                                      
                 BEGIN                                                  
                   PMODTEXT:=PTEXTO+3;                                  
                   PTEXTO  :=*+1;                                       
                   REPLACE PTEXTO BY PMODTEXT FOR TAMANHO;              
                 END                                                    
              ELSE                                                      
                 PTEXTO:=*+1;                                           
            END;                                                        
       END WHILE;                                                       
                                                                        
    TAMANHO:= OFFSET(PTEXTO);                                           
    SALVATAM:= * - TAMANHO;                                             
    IF SALVATAM > 0 THEN                                                
       BEGIN                                                            
         PTEXTO:=POINTER(TEXTO[0])+TAMANHO;                             
         REPLACE PTEXTO BY 48"40" FOR SALVATAM;                         
       END;                                                             
                                                                        
  END TEXT_TO_BIN;                                                      
 $PAGE                                                                  
  PROCEDURE BIN_TO_TEXT(TEXTOOUT,TAMANHO);                              
  %------------------------------------                                 
  EBCDIC  ARRAY   TEXTOOUT[0];                                          
  INTEGER TAMANHO;                                                      
  BEGIN                                                                 
    %----------------------------------------------------------%        
    % Converte caracteres hexa abaixo de 20 e acima de 7F em:  %        
    % <DLE><3X><3Y>, onde X e o primeiro caracter hexadecimal e%        
    % Y o segundo.                                             %        
    %----------------------------------------------------------%        
                                                                        
    ARRAY AUX[0:0];                                                     
                                                                        
    ARRAY TEXTO[0] = TEXTOOUT[*];                                       
                                                                        
    INTEGER VARREASCII;                                                 
                                                                        
    POINTER PAUX,                                                       
             PTEXTO;                                                    
                                                                        
    DEFINE  BIN1    = POINTER(TEXTO[0],4)+(OFFSET(PTEXTO)*2)#,          
            BIN2    = POINTER(TEXTO[0],4)+((OFFSET(PTEXTO)*2)+1)#,      
                                                                        
            P4AUX   = POINTER(AUX[0],4)+(OFFSET(PAUX)*2)#,              
                                                                        
            C3      = 4"3"#,                                            
                                                                        
            DLE     = 48"10"#,                                          
                                                                        
            TAB_EBC = 48"404F7F7B5B6C507D4D5D5C4E6B604B61"              
                      48"F0F1F2F3F4F5F6F7F8F97A5E4C7E6E6F"              
                      48"7CC1C2C3C4C5C6C7C8C9D1D2D3D4D5D6"              
                      48"D7D8D9E2E3E4E5E6E7E8E94AE05A5F6D"              
                      48"79818283848586878889919293949596"              
                      48"979899A2A3A4A5A6A7A8A9C06AD0A107"#,            
                                                                        
            TAB_ASC = 48"202122232425262728292A2B2C2D2E2F"              
                      48"303132333435363738393A3B3C3D3E3F"              
                      48"404142434445464748494A4B4C4D4E4F"              
                      48"505152535455565758595A5B5C5D5E5F"              
                      48"606162636465666768696A6B6C6D6E6F"              
                      48"707172737475767778797A7B7C7D7E7F"#;            
                                                                        
    % Truthset declarations                                             
                                                                        
    TRUTHSET VALALPHA(                                                  
                      TAB_ASC);                                         
                                                                        
    % Translate declarations                                            
                                                                        
    TRANSLATETABLE ASCII_TO_EBCDIC (                                    
         TAB_ASC TO TAB_EBC                                             
                                   );                                   
                                                                        
                                                                        
    TRANSLATETABLE T3X_TO_EBCDIC(                                       
           EBCDIC TO EBCDIC,                                            
           48"303132333435363738393A3B3C3D3E3F"                         
        TO 48"F0F1F2F3F4F5F6F7F8F97A5E4C7E6E6F"                         
                                );                                      
                                                                        
    PTEXTO:=TEXTO[0];                                                   
    PAUX  :=AUX[0];                                                     
                                                                        
    RESIZE (AUX,(TAMANHO*3));                                           
                                                                        
    WHILE TAMANHO > 0 DO                                                
      BEGIN                                                             
        VARREASCII:= TAMANHO;                                           
        SCAN PTEXTO FOR TAMANHO:TAMANHO                                 
                WHILE IN VALALPHA;                                      
        VARREASCII:= * - TAMANHO;                                       
        REPLACE PAUX:PAUX BY PTEXTO:PTEXTO FOR VARREASCII               
                                               WITH ASCII_TO_EBCDIC;    
        IF TAMANHO > 0 THEN                                             
           BEGIN                                                        
             REPLACE PAUX:PAUX BY DLE FOR 1;                            
             REPLACE P4AUX     BY C3   FOR 1,                           
                                  BIN1 FOR 1,                           
                                  C3   FOR 1,                           
                                  BIN2 FOR 1;                           
             REPLACE PAUX:PAUX BY PAUX FOR 2 WITH T3X_TO_EBCDIC;        
             TAMANHO:=*-1;                                              
             PTEXTO:=*+1;                                               
           END;                                                         
      END;                                                              
                                                                        
    TAMANHO:= OFFSET(PAUX);                                             
    IF TAMANHO > SIZE(TEXTOOUT) THEN                                    
       BEGIN                                                            
         PTEXTO:=TEXTO[0];                                              
         REPLACE PTEXTO BY " " FOR SIZE(TEXTOOUT);                      
       END                                                              
    ELSE                                                                
       BEGIN                                                            
         PAUX:=AUX[0];                                                  
         PTEXTO:=TEXTO[0];                                              
         REPLACE PTEXTO BY PAUX FOR TAMANHO;                            
       END;                                                             
                                                                        
                                                                        
 END BIN_TO_TEXT;                                                       
$PAGE                                                                   
 PROCEDURE ASCII_TO_EBCDIC(TEXTOIN,TAMANHO);                            
 %------------------------------------------                            
 EBCDIC  ARRAY   TEXTOIN[0];                                            
 INTEGER TAMANHO;                                                       
 BEGIN                                                                  
    %-----------------------------------------------------------------% 
    % Converte caracteres da tabela ASCII (256 caracteres) para EBCDIC% 
    % A conversao e feita conforme tabela T_ASCII_TO_EBCDIC, onde  sao% 
    % codificados qq caracteres abaixo de 20(HEXA) e acima de 7F(HEXA)% 
    % para branco (40-hexa) e as vogais acentuadas para ela mesma, sem% 
    % acento.                                                         % 
    % Esta library e para ser utilizada para exibir dados gravados  em% 
    % ASCII (pela rotina TEXT_TO_BIN) para terminais de video.        % 
    %-----------------------------------------------------------------% 
                                                                        
  ARRAY TEXTO[0]=TEXTOIN[*];                                            
                                                                        
  POINTER  PTEXTO;                                                      
  % Translate declarations                                              
  TRANSLATETABLE T_ASCII_TO_EBCDIC (                                    
                    48"000102030405060708090A0B0C0D0E0F"                
              TO    48"40404040404040404040404040404040",               
                    48"101112131415161718191A1B1C1D1E1F"                
              TO    48"40404040404040404040404040404040",               
                    48"202122232425262728292A2B2C2D2E2F"                
              TO    48"404F7F7B5B6C507D4D5D5C4E6B604B61",               
                    48"303132333435363738393A3B3C3D3E3F"                
              TO    48"F0F1F2F3F4F5F6F7F8F97A5E4C7E6E6F",               
                    48"404142434445464748494A4B4C4D4E4F"                
              TO    48"7CC1C2C3C4C5C6C7C8C9D1D2D3D4D5D6",               
                    48"505152535455565758595A5B5C5D5E5F"                
              TO    48"D7D8D9E2E3E4E5E6E7E8E94AE05A5F6D",               
                    48"606162636465666768696A6B6C6D6E6F"                
              TO    48"79818283848586878889919293949596",               
                    48"707172737475767778797A7B7C7D7E7F"                
              TO    48"979899A2A3A4A5A6A7A8A9C06AD0A107",               
                    48"808182838485868788898A8B8C8D8E8F"                
              TO    48"C3408581408140838540404040404040",               
                    48"909192939495969798999A9B9C9D9E9F"                
              TO    48"C5404096404040404040404040404040",               
                    48"A0A1A2A3A4A5A6A7A8A9AAABACADAEAF"                
              TO    48"818996A4404081964040404040404040",               
                    48"B0B1B2B3B4B5B6B7B8B9BABBBCBDBEBF"                
              TO    48"404040404040C1C140C1404040404040",               
                    48"C0C1C2C3C4C5C6C7C8C9CACBCCCDCECF"                
              TO    48"40404040404081C14040404040404040",               
                    48"D0D1D2D3D4D5D6D7D8D9DADBDCDDDEDF"                
              TO    48"4040C5404040C9404040404040404040",               
                    48"E0E1E2E3E4E5E6E7E8E9EAEBECEDEEEF"                
              TO    48"D640D64096D6404040E4404040404040",               
                    48"F0F1F2F3F4F5F6F7F8F9FAFBFCFDFEFF"                
              TO    48"40404040404040404040404040404040"                
                    );                                                  
    PTEXTO:=TEXTO[0];                                                   
                                                                        
    TAMANHO:=MIN(TAMANHO,SIZE(TEXTOIN));                                
    REPLACE PTEXTO BY PTEXTO FOR TAMANHO WITH T_ASCII_TO_EBCDIC;        
                                                                        
 END ASCII_TO_EBCDIC;                                                   
$PAGE                                                                   
 PROCEDURE EBCDIC_TO_ASC(TEXTOIN,TAMANHO);                              
 %------------------------------------------                            
 EBCDIC  ARRAY   TEXTOIN[0];                                            
 INTEGER TAMANHO;                                                       
 BEGIN                                                                  
    %-----------------------------------------------------------------% 
    % Converte caracteres da tabela EBCDIC para ASCII                 % 
    % Esta library devera ser utilizada para enviar arquivos  em      % 
    % formato imagem  por ftp                                         % 
    %-----------------------------------------------------------------% 
                                                                        
  ARRAY TEXTO[0]=TEXTOIN[*];                                            
                                                                        
  POINTER  PTEXTO;                                                      
  % Translate declarations                                              
  TRANSLATETABLE  T_EBCDIC_TO_ASC   (                                   
                            EBCDIC TO ASCII                             
                                  );                                    
                                                                        
    PTEXTO:=TEXTO[0];                                                   
                                                                        
    TAMANHO:=MIN(TAMANHO,SIZE(TEXTOIN));                                
    REPLACE PTEXTO BY PTEXTO FOR TAMANHO WITH T_EBCDIC_TO_ASC;          
                                                                        
 END EBCDIC_TO_ASC;                                                     
$PAGE                                                                   
 $ PAGE                                                                 
 EXPORT BCLPARAEBCDIC                                                   
       ,EBCDICPARABCL                                                   
       ,HEXTOEBC                                                        
       ,OTIMIZA                                                         
       ,SUBTRADUZ                                                       
       ,TRADUZ                                                          
       ,TEXT_TO_BIN                                                     
       ,BIN_TO_TEXT                                                     
       ,ASCII_TO_EBCDIC                                                 
       ,EBCDIC_TO_ASC                                                   
       ;                                                                
                                                                        
 FREEZE (TEMPORARY);                                                    
END.                                                                    
