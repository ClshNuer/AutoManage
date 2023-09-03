# Windows 软件安装

<!--last modify: 20230728-->



```yaml
url: 
    python: https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
    vscode: https://az764295.vo.msecnd.net/stable/695af097c7bd098fbf017ce3ac85e09bbc5dda06/VSCodeUserSetup-x64-1.79.2.exe
    pycharm: https://download.jetbrains.com/python/pycharm-professional-2023.1.2.exe
```

```powershell
cmd = f'{pkg_name} /quiet InstallAllUsers=1 PrependPath=1 TargetDir={PY_PATH}'
subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
```

### python 安装

- shell
  ```powershell
  pip config set global.index-url $url
  pip config set global.extra-index-url $url
  pip config set global.cache-dir $cache-dir
  pip config set install.trusted-host $trusted-host
  ```
