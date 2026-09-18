      *                                 DIA 18/09/2020     HORA 20:15:00
       01  CAPA01 REDEFINES C-MAPA.                                     
      *        05  FILLER      PIC X(25).                               
               05  CAPA01-MENS.                                         
                   07  PA01CODE.                                        
                       09  1ST-PA01CODE           PICTURE X(001).       
                       09  FILLER                 PICTURE X(003).       
                   07  PA01CONT.                                        
                       09  1ST-PA01CONT           PICTURE X(001).       
                       09  FILLER                 PICTURE X(071).       
                   07  PA01DATE.                                        
                       09  1ST-PA01DATE           PICTURE X(001).       
                       09  FILLER                 PICTURE X(009).       
                   07  PA01TIME.                                        
                       09  1ST-PA01TIME           PICTURE X(001).       
                       09  FILLER                 PICTURE X(007).       
                   07  PA01PLAC.                                        
                       09  1ST-PA01PLAC           PICTURE X(001).       
                       09  FILLER                 PICTURE X(006).       
                   07  PA01MUN-NUL.                                     
                       09  PA01MUN                PICTURE 9(005).       
                   07  PA01DOCT-NUL.                                    
                       09  PA01DOCT               PICTURE 9(001).       
                   07  PA01DOCN-NUL.                                    
                       09  PA01DOCN               PICTURE 9(014).       
                   07  PA01AUTD.                                        
                       09  1ST-PA01AUTD           PICTURE X(001).       
                       09  FILLER                 PICTURE X(007).       
                   07  PA01TAXA.                                        
                       09  1ST-PA01TAXA           PICTURE X(001).       
                       09  FILLER                 PICTURE X(017).       
                   07  PA01DRK-NUL.                                     
                       09  PA01DRK                PICTURE 9(001).       
                   07  PA01MENS.                                        
                       09  1ST-PA01MENS           PICTURE X(001).       
                       09  FILLER                 PICTURE X(072).       
               05 FILLER PIC X(1779).                                   
