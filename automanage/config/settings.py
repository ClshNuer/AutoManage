# coding=utf-8
'''
AutoManage 自定义配置
'''

import pathlib

# 路径设置
BASE_PATH = pathlib.Path(__file__).parent.parent # AutoManage 代码相对路径
DATA_PATH = BASE_PATH.joinpath('data') # 数据存放目录

# AutoManage入口参数设置
ENABLE_CHECK_VERSION = True # 开启版本检测
RESULT_SAVE_FORMAT = 'csv' # 结果保存格式
RESULT_SAVE_PATH = None # 结果保存路径(默认None)

# 代理设置
ENABLE_REQUEST_PROXY = False # 是否开启代理(默认False)
REQUEST_PROXY_POOL = {'http': 'http://127.0.0.1:1080',
                       'https': 'http://127.0.0.1:1080'}  # 代理池

# 请求设置
REQUEST_TIMEOUT_SECOND = (13, 27)  # 请求超时秒数(默认connect timout推荐略大于3秒)
REQUEST_SSL_VERIFY = True  # 请求SSL验证(默认False)
# 默认请求头 可以在headers里添加自定义请求头
REQUEST_DEFAULT_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,'
              'application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    'DNT': '1',
    'Referer': 'https://www.google.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
    'X-Forwarded-For': '127.0.0.1'
}
ENABLE_RANDOM_UA = True  # 使用随机UA(默认True，开启可以覆盖request_default_headers的UA)
# UA列表(默认使用chrome UA)
REQUEST_USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) '
    'Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/68.0']

# Win Apps Download Urls
PKG_PATH = DATA_PATH.joinpath('packages') # 软件包存放目录
INSTALL_PATH = 'D:\\Softwares\\' # 软件安装目录
WIN_DOWNLOAD_URLS = {
    'PyCharm' : 'https://download.jetbrains.com/python/pycharm-professional-2023.1.2.exe'
    'Thunder11': 'https://down.sandai.net/thunder11/XunLeiWebSetup11.4.8.2122xl11.exe',
    'Huorong' : 'https://www.huorong.cn/downloadfullv5.html?status=hrstat&src=17'
}


# UI
goby_path = "G:\\AllInOne\\02_VulnerabilityAnalysis\\Goby\\"
goby_name = "Goby.exe"
yujian_path = "G:\\AllInOne\\01_InformationGathering\\01x11_DirectoryBruteforce\\"
yujian_name = "御剑2.0.exe"
yujian_path = "G:\\AllInOne\\01_InformationGathering\\01x11_DirectoryBruteforce\\御剑\\御剑1.4终结版\\"
yujian_name = "御剑1.4.exe"
yujian_path = "G:\\AllInOne\\01_InformationGathering\\01x11_DirectoryBruteforce\\御剑\\御剑1.5-注入版\\"
yujian_name = "New御剑1.5.exe"
yujian_path = "G:\\AllInOne\\01_InformationGathering\\01x11_DirectoryBruteforce\\御剑\\御剑后台扫描珍藏版\\"
yujian_name = "御剑后台扫描工具.exe"
burpsuite_path = "G:\\AllInOne\\03_WebApplicationAnalysis\\0301_WebApplicationProxies\\Burpsuite\\"
burpsuite_name = "burpsuite"
xray_gui_path = "G:\\AllInOne\\03_WebApplicationAnalysis\\0303_WebVulnerabilityScanners\\Xray\\"
xray_gui_name = "gamma-gui-windows-amd64.exe"
cyberchef_path = "G:\\AllInOne\\05_PasswordAttacks\\0503_PasswordProfiling&Wordlists\\CyberChef_v9.55.0\\"
cyberchef_name = "CyberChef_v9.55.0.html"
snetcracker_path = "G:\\AllInOne\\05_PasswordAttacks\\0503_PasswordProfiling&Wordlists\\超级弱口令检查工具 V1.0\\超级弱口令检查工具V1.0 Beta28 20190715\\"
snetcracker_name = "SNETCracker.exe"
dictionary_list_path = "G:\\AllInOne\\05_PasswordAttacks\\0503_PasswordProfiling&Wordlists\\Dicts\\"
dictionary_list_name = ""
winmd5_path = "G:\\AllInOne\\05_PasswordAttacks\\0503_PasswordProfiling&Wordlists\\"
winmd5_name = "WinMD5.exe"
skhash_path = "G:\\AllInOne\\05_PasswordAttacks\\0503_PasswordProfiling&Wordlists\\"
skhash_name = "深空HASH计算工具.exe"

# UI bak


# CMD
oneforall_path = "G:\\AllInOne\\01_InformationGathering\\01x10_SubDomains\\OneForAll\\"
oneforall_name = "oneforall.py"
jsfinder_path = "G:\\AllInOne\\01_InformationGathering\\01x10_SubDomains\\JSFinder\\"
jsfinder_name = "JSFinder.py"
sublist3r_path = "G:\\AllInOne\\01_InformationGathering\\01x10_SubDomains\\Sublist3r\\"
sublist3r_name = "sublist3r.py"
dirsearch_path = "G:\\AllInOne\\01_InformationGathering\\01x11_DirectoryBruteforce\\"
dirsearch_name = "dirsearch.py"
pocsuite3_path = "G:\\AllInOne\\03_WebApplicationAnalysis\\0300_CMS&FrameworkIdentification\\pocsuite3\\"
pocsuite3_name = "pocsuite3\\console.py"
burpsuitepro_path = "G:\\AllInOne\\03_WebApplicationAnalysis\\0301_WebApplicationProxies\\Burpsuite\\"
burpsuitepro_name = "burpsuitepro"
rad_path = "G:\\AllInOne\\03_WebApplicationAnalysis\\0302_WebCrawlers&DirectoryBruteforce\\Rad\\"
rad_name = "rad_windows_amd64.exe"
wfuzz_path = "G:\\AllInOne\\03_WebApplicationAnalysis\\0302_WebCrawlers&DirectoryBruteforce\\Wfuzz\\"
wfuzz_name = "src\\wfuzz.py"
xray_path = "G:\\AllInOne\\03_WebApplicationAnalysis\\0303_WebVulnerabilityScanners\\Xray\\"
xray_name = "xray_windows_amd64.exe"
sqlmap_path = "G:\\AllInOne\\04_DatabaseAssessment\\SQLMap\\"
sqlmap_name = "sqlmap.py"
heapdump_tool_path = "G:\\AllInOne\\08_ExploitationTools\\SpringBoot\\"
heapdump_tool_name = "heapdump_tool.jar"
jdumpsipider_path = "G:\\AllInOne\\08_ExploitationTools\\SpringBoot\\"
jdumpsipider_name = "JDumpSpider-1.1-SNAPSHOT-full.jar"
springboot_exploit_path = "G:\\AllInOne\\08_ExploitationTools\\SpringBoot\\"
springboot_exploit_name = "SpringBootExploit-1.3-SNAPSHOT-all.jar"
nc_path = "G:\\AllInOne\\09_Sniffing&Spoofing\\0900_NetworkSniffers\\NC\\"
nc_name = "nc.exe"
neo_regeorg_path = "G:\\AllInOne\\10_PostExploitation\\1001_Tunneling&Exfiltration\\Neo-reGeorg\\"
neo_regeorg_name = "neoreg.py"


# request_thread_count = None  # 请求线程数量(默认None，则根据情况自动设置)

# request_allow_redirect = True  # 请求允许重定向(默认True)
# request_redirect_limit = 10  # 请求跳转限制(默认10次)

# enable_check_network = True # 开启网络环境检测



# Double WeChat
# start D:\Softwares\scoop\apps\wechat\current\WeChat.exe
# start D:\Softwares\scoop\apps\wechat\current\WeChat.exe