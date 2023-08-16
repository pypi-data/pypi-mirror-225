import configparser
from datetime import datetime
import os
from ipra.Utility.ConfigUtility import GetConfigSingletion
class Logger:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        try:
            self.config_obj = GetConfigSingletion()
            self.loggerPath = self.config_obj.ReadConfig('logger_path','loggerpath')

            if not os.path.exists(self.loggerPath):
                os.makedirs(self.loggerPath)

        except Exception as ex:
            self.writeLogString('LOGGER','EXCEPTION:'+str(ex))
            self.loggerPath = 'C:/IPRA/LOG/'


    def setLogPath(self,path):
        self.loggerPath = path
        #if path not exist, create
        if not os.path.isdir(self.loggerPath):
            os.makedirs(self.loggerPath)

    def __formLogFileName(self):
        logFileName = "IPRA."+datetime.today().strftime('%Y%m%d')+".log"
        return logFileName

    #log file content format
    #<YYYY-MM-DD HH:MM:SS>[PAYMENT TYPE]:{Content to display}
    def writeLogString(self,prefix,content):
        with open(self.loggerPath+ self.__formLogFileName(), "a", encoding='utf8') as f:
            f.write(datetime.today().strftime('<%Y-%m-%d %H:%M:%S>') + "[" + prefix + "]:"+content+"\n")
            f.close()
    

