@echo off
title create ipsec policy to block port 135,137,138,139,445
netsh ipsec static add policy name=soft
netsh ipsec static add filterlist name=Filter1
netsh ipsec static add filter filterlist=Filter1 srcaddr=any dstaddr=any dstport=135 protocol=TCP
netsh ipsec static add filter filterlist=Filter1 srcaddr=any dstaddr=any dstport=137 protocol=TCP
netsh ipsec static add filter filterlist=Filter1 srcaddr=any dstaddr=any dstport=138 protocol=TCP
netsh ipsec static add filter filterlist=Filter1 srcaddr=any dstaddr=any dstport=139 protocol=TCP
netsh ipsec static add filter filterlist=Filter1 srcaddr=any dstaddr=any dstport=445 protocol=TCP
netsh ipsec static add filter filterlist=Filter1 srcaddr=any dstaddr=any dstport=135 protocol=UDP
netsh ipsec static add filter filterlist=Filter1 srcaddr=any dstaddr=any dstport=137 protocol=UDP
netsh ipsec static add filter filterlist=Filter1 srcaddr=any dstaddr=any dstport=138 protocol=UDP
netsh ipsec static add filter filterlist=Filter1 srcaddr=any dstaddr=any dstport=139 protocol=UDP
netsh ipsec static add filter filterlist=Filter1 srcaddr=any dstaddr=any dstport=445 protocol=UDP
netsh ipsec static add filteraction name=FilteraAtion1 action=block
netsh ipsec static add rule name=Rule1 policy=soft filterlist=Filter1 filteraction=FilteraAtion1
netsh ipsec static set policy name=soft assign=y
exit