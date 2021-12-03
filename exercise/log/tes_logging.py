import datetime
import logging
import logging.handlers
import logging.config


filename_path = "./log/logger.log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y/%m/%d %H:%M:%S %p"

logging.config.fileConfig("./log/logging.conf")
# logging.basicConfig(filename=filename_path, level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
logger1 = logging.getLogger("tex")
logger1.setLevel(logging.DEBUG)

logger1.debug("debug message")
logger1.info("info message")
logger1.warning('warn message')
logger1.error('error message')
logger1.critical("critical message")

# logging.log(logging.DEBUG, "This is a debug message.")
# logging.log(logging.INFO, "This is a info message.")
# logging.log(logging.WARN, "This is a warn message ")
# # logging.log(logging.WARNING, "This is a warning message")
# logging.log(logging.ERROR, "This is a error message.")
# logging.log(logging.CRITICAL, "This is a crirical message.")

'''
Logger 记录器，暴露了应用程序代码能直接使用的接口。
Handler 处理器，将（记录器产生的）日志记录发送至合适的目的地。
Filter 过滤器，提供了更好的粒度控制，它可以决定输出哪些日志记录。
Formatter 格式化器，指明了最终输出中日志记录的布局。
'''
"""
1）要求将所有级别的所有日志都写入磁盘文件中
2）all.log文件中记录所有的日志信息，日志格式为：日期和时间 - 日志级别 - 日志信息
3）error.log文件中单独记录error及以上级别的日志信息，日志格式为：日期和时间 - 日志级别 - 文件名[:行号] - 日志信息
4）要求all.log在每天凌晨进行日志切割
"""
# logger：记录器， 默认等级：warning 
logger = logging.getLogger("mylogger")
logger.setLevel(logging.DEBUG)

# Handler 处理器
rf_handler = logging.handlers.TimedRotatingFileHandler('./log/all.log', when='midnight', 
                                                        interval=1, backupCount=7,
                                                         atTime= datetime.time(0, 0, 0, 0))
rf_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))


f_handler = logging.FileHandler('./log/error.log')
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)d] - %(message)s"))

logger.addHandler(rf_handler)
logger.addHandler(f_handler)

logger.debug("debug message")
logger.info("info message")
logger.warning('warn message')
logger.error('error message')
logger.critical("critical message")