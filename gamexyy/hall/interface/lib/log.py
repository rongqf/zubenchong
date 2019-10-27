#coding:utf-8



__all__ = ['getLogger', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']

import time,sys
import logging
import logging.handlers
from logging import getLogger, INFO, WARN, DEBUG, ERROR, FATAL




logger = getLogger('hell')

initflag = False
def initlog():
    global initflag
    if initflag:
        return 

    initflag = True

    LOG_FILE_MAXBYTES = 1024 * 1024 * 30     # 3 Mb
    LOG_FILE_BACKUPCOUNT = 1000

    LOG_LEVEL = logging.DEBUG
    #LOG_LEVEL = logging.INFO
    MODULE_NAME = 'web'
    filename = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    LOG_FILENAME = 'logs/{module_name}-{filename}.log'.format(module_name=MODULE_NAME, filename=filename)
    FORMAT = '[%(asctime)s]-%(levelname)-8s<%(name)s>{%(filename)s:%(lineno)s} -> %(message)s'

    
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                    maxBytes = LOG_FILE_MAXBYTES,
                                                    backupCount = LOG_FILE_BACKUPCOUNT,
                                                    )
    formatter = logging.Formatter(FORMAT)
    handler.setFormatter(formatter)
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(handler)
    #rf_handler = logging.StreamHandler(sys.stdout) 
    #rf_handler.setFormatter(logging.Formatter("%(asctime)s -%(levelname)s %(name)s:%(lineno)s -> %(message)s"))
    #logger.addHandler(rf_handler)
    handler_err = logging.handlers.RotatingFileHandler("logs/error.log",
                                                    maxBytes = LOG_FILE_MAXBYTES,
                                                    backupCount = LOG_FILE_BACKUPCOUNT,
                                                    )

    handler_err.setFormatter(formatter)
    handler_err.setLevel(logging.ERROR)
    logger.addHandler(handler_err)

initlog()



def __add_options(parser):
    levels = ('DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
    parser.add_option('--log-level',
                      choices=levels,
                      default='INFO',
                      dest='loglevel',
                      help=('Amount of detail in build-time console messages '
                            '(default: %%default, choose one of %s)'
                            % ', '.join(levels))
                      )

def __process_options(parser, opts):
    try:
        level = getattr(logging, opts.loglevel.upper())
    except AttributeError:
        parser.error('Unknown log level `%s`' % opts.loglevel)
    logger.setLevel(level)



try:
    unicode
    _unicode = True
except NameError:
    _unicode = False

class MyHandler(logging.Handler):
    def __init__(self, stream=None):
        logging.Handler.__init__(self)
        self.stream = stream
        self.setFormatter(formatter)
        self.count = 0

    def emit(self, record):
        try:
            msg = self.format(record)
            #print 'test', msg, record
            stream = self.stream
            self.count += 1
            #fs = "%s:%s" % (self, self.count) + ", %s"
            fs = "%s" 
            if not _unicode: #if no unicode support...
                stream(fs % msg)
            else:
                stream(fs % msg.encode("UTF-8"))
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


if __name__ == '__main__':

    logger.debug("debuggggggg")

    logger.info("infooooooooooo")

    logger.warning("warninggggggg")

    logger.error("errorrrrrrrrrrrr")

    logger.critical("criticallllllll")

    logger.debug('%s, %s', *('debug1', 'debug2'))
    logger.debug('%(m)s, %(s)s', {'m': 'debug1', 's': 'debug2'})


    logger.removeHandler(handler)

    
    def log(x):
        print 'mylog', x


    logger.addHandler(MyHandler(log))


    logger.debug('%s, %s', *('debug1', 'debug2'))
    logger.warning("aaaaa%s", 'cccc')
    logger.error("bbbbb")
