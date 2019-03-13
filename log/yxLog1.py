

# -------------------------------------------------------------------------------------------------------------
# movoto第一次上生产环境经验:
# 代码里的各种分支还有关键函数的参数等处,都需要打出log,
# 一个好的log可以帮助程序员一眼就定位到程序的bug,很大的提高修代码bug的效率 !!!!
# -------------------------------------------------------------------------------------------------------------

# yxLog1.py as a module
import logging

# config logging's logger alias yx_logger:
yx_logger = logging.getLogger('yx_log')
hdlr = logging.FileHandler('/var/log/yx/yx.log')    # chmod -R 777  /var/log/yx 
formatter = logging.Formatter('%(asctime)s %(levelname)s --> %(message)s')
hdlr.setFormatter(formatter)
yx_logger.addHandler(hdlr)
yx_logger.setLevel(logging.DEBUG)

yxdebug = yx_logger.debug

'''
usage:    
            # mkdir  /var/log/yx     
            # chmod -R 777  /var/log/yx

            from yxLog1 import yxdebug
            yxdebug("==============debug info")

            # tailf  /var/log/yx/yx.log
'''

#----------------------------------------------------------------------------------------------------#
# if add (filemode='w'), will refresh log every time. 

'''
import logging
logging.basicConfig(filename='/var/log/yx.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s --> %(message)s')

# usage:
logging.debug('---->>')
'''

#----------------------------------------------------------------------------------------------------#
'''
import logging  
logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%a, %d %b %Y %H:%M:%S',  
                    filename='/var/yx.log')                      
# usage:
logging.debug('---->')
'''

#----------------------------------------------------------------------------------------------------#

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=(
            '%(levelname) -s %(asctime)s %(filename) -s %(funcName) -s %(lineno) -d: %(message)s'))
LOGGER.info('---->')

#----------------------------------------------------------------------------------------------------#
'''
import logging
logging.basicConfig(filename='log.log',
                    format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=10)
  
logging.debug('debug')
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.critical('critical')
logging.log(10,'log')
'''

#----------------------------------------------------------------------------------------------------#
'''
# 定义文件
file_1_1 = logging.FileHandler('l1_1.log', 'a')
fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s")
file_1_1.setFormatter(fmt)

file_1_2 = logging.FileHandler('l1_2.log', 'a')
fmt = logging.Formatter()
file_1_2.setFormatter(fmt)

# 定义日志
logger1 = logging.Logger('s1', level=logging.ERROR)
logger1.addHandler(file_1_1)
logger1.addHandler(file_1_2)


# 写日志
logger1.critical('1111')
'''


