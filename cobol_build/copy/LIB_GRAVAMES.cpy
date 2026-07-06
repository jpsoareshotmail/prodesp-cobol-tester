      %$$ reset RELEASE deixar para o job de compilacao                       0000100001.001.000
                                                                              0000120001.001.000
      $$ sharing = sharedbyall                                                0000140001.001.000
      begin                                                                   00002000          
                                                                              0000300001.001.000
         library LibRvCh(title="*PC/LIB/EXTERNCOMM/GR.");                     0000430001.001.000
                                                                              0000450001.001.000
         procedure EnableQ(TimeLimitV);                                       00005000          
            ebcdic array TimeLimitV[0];                                       00006000          
         library LibRvCh(actualname="ENABLEGR");                              00007000          
                                                                              00008000          
         procedure DisableQ();                                                00009000          
         library LibRvCh(actualname="DISABLEGR");                             00010000          
                                                                              00011000          
         procedure SendQ(msg, tam, status);                                   00012000          
            ebcdic array msg, tam, status[0];                                 00013000          
         library LibRvCh(actualname="SENDGR");                                00014000          
                                                                              00015000          
         procedure ReceiveQ(msg, status);                                     00016000          
            ebcdic array msg, status[0];                                      00017000          
         library LibRvCh(actualname="RECEIVEGR");                             00018000          
                                                                              00019000          
                                                                              00020000          
         procedure EnableP(TimeLimitV);                                       00021000          
            ebcdic array TimeLimitV[0];                                       00022000          
         begin                                                                00023000          
            EnableQ(TimeLimitV);                                              00024000          
         end EnableP;                                                         00025000          
                                                                              00026000          
         procedure DisableP();                                                00027000          
         begin                                                                00028000          
            DisableQ();                                                       00029000          
         end DisableP;                                                        00030000          
                                                                              00031000          
         procedure ReceiveP(msg, status);                                     00032000          
            ebcdic array msg, status[0];                                      00033000          
         begin                                                                00034000          
            ReceiveQ(msg, status);                                            00035000          
         end ReceiveP;                                                        00036000          
                                                                              00037000          
         procedure SendP(msg, tam, status);                                   00038000          
            ebcdic array msg, tam, status[0];                                 00039000          
         begin                                                                00040000          
            SendQ(msg, tam, status);                                          00041000          
         end SendP;                                                           00042000          
                                                                              00043000          
      export                                                                  00044000          
            EnableP  as "ENABLE",                                             00045000          
            DisableP as "DISABLE",                                            00046000          
            ReceiveP as "RECEIVE",                                            00047000          
            SendP    as "SEND";                                               00048000          
                                                                              00049000          
            FREEZE(temporary);                                                00050000          
      end.                                                                    00051000          
