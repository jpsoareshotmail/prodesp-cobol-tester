      *                                 DIA 18/09/2020     HORA 20:14:35
       01  COFI11 REDEFINES C-MAPA.                                     
      *        05  FILLER      PIC X(25).                               
               05  COFI11-MENS.                                         
                   07  FI11CODE.                                        
                       09  1ST-FI11CODE           PICTURE X(001).       
                       09  FILLER                 PICTURE X(003).       
                   07  FI11CONT.                                        
                       09  1ST-FI11CONT           PICTURE X(001).       
                       09  FILLER                 PICTURE X(071).       
                   07  FI11DATA.                                        
                       09  1ST-FI11DATA           PICTURE X(001).       
                       09  FILLER                 PICTURE X(009).       
                   07  FI11HORA.                                        
                       09  1ST-FI11HORA           PICTURE X(001).       
                       09  FILLER                 PICTURE X(007).       
                   07  FI11PLAC.                                        
                       09  1ST-FI11PLAC           PICTURE X(001).       
                       09  FILLER                 PICTURE X(006).       
                   07  FI11MUNI-NUL.                                    
                       09  FI11MUNI               PICTURE 9(005).       
                   07  FI11CNPJ-NUL.                                    
                       09  FI11CNPJ               PICTURE 9(014).       
                   07  FI11PROT-NUL.                                    
                       09  FI11PROT               PICTURE 9(008).       
                   07  FI11PANO-NUL.                                    
                       09  FI11PANO               PICTURE 9(004).       
                   07  FI11OPC1.                                        
                       09  1ST-FI11OPC1           PICTURE X(001).       
                   07  FI11OPC2.                                        
                       09  1ST-FI11OPC2           PICTURE X(001).       
                   07  FI11OPC3.                                        
                       09  1ST-FI11OPC3           PICTURE X(001).       
                   07  FI11OPC4.                                        
                       09  1ST-FI11OPC4           PICTURE X(001).       
                   07  FI11BDUT.                                        
                       09  1ST-FI11BDUT           PICTURE X(001).       
                       09  FILLER                 PICTURE X(007).       
                   07  FI11TAXA.                                        
                       09  1ST-FI11TAXA           PICTURE X(001).       
                       09  FILLER                 PICTURE X(017).       
                   07  FI11DRK-NUL.                                     
                       09  FI11DRK                PICTURE 9(001).       
                   07  FI11MENS.                                        
                       09  1ST-FI11MENS           PICTURE X(001).       
                       09  FILLER                 PICTURE X(072).       
               05 FILLER PIC X(1764).                                   
