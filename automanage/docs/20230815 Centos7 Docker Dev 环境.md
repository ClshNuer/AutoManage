# CentOS7 Docker Dev 环境

<!--last modify: 20230815-->



- centos7

  ```shell
  sudo yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel wget
  wget https://www.python.org/ftp/python/3.10.11/Python-3.10.11.tgz
  tar -xf Python-3.10.11.tgz
  cd Python-3.10.11
  ./configure --enable-optimizations
  make -j 4 # -j 4 表示使用 4 个线程进行编译
  sudo make altinstall # 使用 altinstall 而不是 install 可以避免覆盖系统默认的 Python 版本。
  ```

- centos7 docker

  ```shell
  docker pull centos:centos7.9.2009
  docker run -it --name centos7-dev centos:centos7.9.2009 /bin/bash
  
  docker pull openeuler/openeuler:latest # 更新存在问题
  docker run -it --name openeuler-dev openeuler/openeuler:latest /bin/bash
  ```
  
  



