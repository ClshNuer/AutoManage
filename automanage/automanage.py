#!/usr/bin/python3
# coding=utf-8

"""
AutoManage is a automatic configuration management tool

:copyright: Copyright (c) 2019, Jing Ling. All rights reserved.
:license: GNU General Public License v1.0, see LICENSE for more details.
"""

import fire
from datetime import datetime

from common import utils
from config import settings
from config.log import logger
from modules import wildcard

yellow = '\033[01;33m'
white = '\033[01;37m'
green = '\033[01;32m'
blue = '\033[01;34m'
red = '\033[1;31m'
end = '\033[0m'

version = 'v0.0.1'
message = white + '{' + red + version + ' #dev' + white + '}'

automanage_banner = f"""
AutoManage is a automatic configuration management tool{yellow}
    ___         __        __  ___
   /   | __  __/ /_____  /  |/  /___ _____  ____ _____ ____
  / /| |/ / / / __/ __ \/ /|_/ / __ `/ __ \/ __ `/ __ `/ _ \  {message}{green}
 / ___ / /_/ / /_/ /_/ / /  / / /_/ / / / / /_/ / /_/ /  __/  {blue}
/_/  |_\__,_/\__/\____/_/  /_/\__,_/_/ /_/\__,_/\__, /\___/   {white}git.io/fjHT1
                                               /____/

{red}AutoManage is under development, please update before each use!{end}
"""


class BaseChecker():
    pass

class AutoManage(object):
    """
    AutoManage help summary page

    AutoManage is a automatic configuration management tool

    Example:
        python3 oneforall.py version
        python3 oneforall.py check
        python3 oneforall.py run


    Note:
        --port   small/medium/large  See details in ./config/setting.py(default small)
        --fmt    csv/json (result format)
        --path   Result path (default None, automatically generated)

    :param str  target:     One domain (target must be provided)
    :param str  fmt:        Result format (default csv)
    :param str  path:       Result path (default None, automatically generated)
    """
    def __init__(self, fmt = None, path = None):
        self.fmt = fmt
        self.path = path
        self.access_internet = False

    def config_param(self):
        '''
        Config parameters
        '''
        if self.fmt is None:
            self.fmt = settings.RESULT_SAVE_FORMAT
        if self.path is None:
            self.path = settings.RESULT_SAVE_PATH

    def check_param(self):
        '''
        Check parameters
        '''
        pass

    def export_data(self):
        '''
        Export data
        '''
        pass

    def main(self):
        '''
        AutoManage main process

        :return: *** results
        :rtype: list
        '''
        utils.init()

        if not self.access_internet:
            logger.log('ALERT', 'Due to inability to access the Internet, '
                       'AutoManage will not execute the update module!')
            
        if self.access_internet:
            # 检查更新
            # collect = Collect() # 收集更新软件集合
            # collect.run()
            pass

    def run(self):
        '''
        AutoManage running entrance

        :return: *** results
        :rtype: list
        '''
        print(automanage_banner)
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[*] Starting AutoManage @ {dt}\n')
        logger.log('DEBUG', 'Python ' + utils.python_version())
        logger.log('DEBUG', 'AutoManage ' + version)
        utils.check_dep()
        self.access_internet = utils.get_net_env()
        if self.access_internet and settings.ENABLE_CHECK_VERSION:
            utils.check_version(version)
        logger.log('INFOR', 'Start running AutoManage')
        self.config_param()
        self.check_param()

        self.main()

        logger.log('INFOR', 'Finshed AutoManage')

    @staticmethod
    def version():
        '''
        Print version information and exit
        '''
        print(automanage_banner)
        exit(0)

    @staticmethod
    def check():
        '''
        Check if there is a new version and exit
        '''
        utils.check_version(version)
        exit(0)


if __name__ == '__main__':
    fire.Fire(AutoManage)