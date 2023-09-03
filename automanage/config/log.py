import sys
import pathlib

from loguru import logger

# 路径设置
BASE_PATH = pathlib.Path(__file__).parent.parent # AutoManage 代码相对路径
RESULT_PATH = BASE_PATH.joinpath('results')  # 结果保存目录
LOG_PATH = RESULT_PATH.joinpath('automanage.log')  # AutoManage日志保存路径

# 日志配置
# 终端日志输出格式
stdout_fmt = '<cyan>{time:HH:mm:ss,SSS}</cyan> ' \
             '[<level>{level: <5}</level>] ' \
             '<blue>{module}</blue>:<cyan>{line}</cyan> - ' \
             '<level>{message}</level>'
# 日志文件记录格式
logfile_fmt = '<light-green>{time:YYYY-MM-DD HH:mm:ss,SSS}</light-green> ' \
              '[<level>{level: <5}</level>] ' \
              '<cyan>{process.name}({process.id})</cyan>:' \
              '<cyan>{thread.name: <18}({thread.id: <5})</cyan> | ' \
              '<blue>{module}</blue>.<blue>{function}</blue>:' \
              '<blue>{line}</blue> - <level>{message}</level>'

logger.remove()
logger.level(name='TRACE', color='<cyan><bold>')
logger.level(name='DEBUG', color='<blue><bold>')
logger.level(name='INFOR', no=20, color='<green><bold>')
logger.level(name='QUITE', no=25, color='<green><bold>')
logger.level(name='ALERT', no=30, color='<yellow><bold>')
logger.level(name='ERROR', color='<red><bold>')
logger.level(name='FATAL', no=50, color='<RED><bold>')

# 如果你想在命令终端静默运行AutoManage，可以将以下一行中的level设置为QUITE
# 命令终端日志级别默认为INFOR
logger.add(sys.stderr, level='DEBUG', format=stdout_fmt, enqueue=True)
# 日志文件默认为级别为DEBUG
logger.add(LOG_PATH, level='DEBUG', format=logfile_fmt, enqueue=True, encoding='utf-8')
