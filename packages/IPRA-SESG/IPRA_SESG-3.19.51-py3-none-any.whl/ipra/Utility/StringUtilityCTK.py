from customtkinter import StringVar

from ipra.Utility.ConfigUtility import GetConfigSingletion


class _StringSingletonCTK:
    _stringInstance = None

    zhString = [ 
        "導入保單",
        "手工導入保單",
        "清除保單",
        "啟動機器人",
        "匯出保單報告",
        "導入錯誤",
        "保單格式錯誤，請更改資料再重試。",
        "更改設定",
        "設定",
        "關於",
        "支援下例系統：",
        "版本:{0}",
        "更新日期:{0}",
        "校驗值:{0}",
        "匯出路徑",
        "導入路徑",
        "選擇路徑",
        "儲存並離開",
        "繁體中文",
        "ENGLISH",
        "{0} 下載保單報告",
        "等待執行",
        "檢查登入狀態中．．．",
        "登入成功",
        "匯出完成",
        "{0} 處理中．．．",
        "{0} 處理錯誤：{1}",
        "{0} 處理完成",
        "匯出保單報告:{0} {1}",
        "日誌路徑",
        "下載保單報告",
        "語言設定更新將於下次啟動時生效",
        "檢查更新",
        "檢查更新中:{0}",
        "有可更新。請重新啓動IPRA並\"現在更新\"",
        "没有可用的更新",
        "電郵系統",
        "未找到以下配置設定或未初始化：\n",
    ]

    enString = [
        "Import Policy No.",
        "Manual Import Policy No. List",
        "RESET POLICY",
        "START ROBOT",
        "BUILD REPORT ONLY",
        "Import Error",
        "Read File Error.\nPlease correct worksheet name or format",
        "Edit Setting",
        "Setting",
        "About", 
        "Support Below System:",
        "Version:{0}",
        "Release Date:{0}",
        "Checksum:{0}",
        "Output Path",
        "Input Path",
        "Select Path",
        "Save and Return",
        "繁體中文",
        "ENGLISH",
        "{0} Download Policy Report",
        "Waiting Execute",
        "Login Checking in Progress...",
        "Login Success",
        "Export Completed",
        "Processing {0}...",
        "{0} Process Error: {1}",
        "{0} Process Completed",
        "Build Policy Report:{0} {1}",
        "Log Path",
        "Download Policy Report",
        "Language setting update will effect in next start up",
        "Check for Update",
        "Checking for Update:{0}",
        "Update Available. Please restart IPRA and select \"Update Now\"",
        "There are no updates available",
        "Email System",
        "Below Config Setting not found or not initialize:\n",
    ]

    def __init__(self) -> None:

        #Main Frame related
        self.importPolicy       = StringVar()
        self.importManualPolicy = StringVar()
        self.clear              = StringVar()
        self.startRobot         = StringVar()
        self.exportReport       = StringVar()
        self.importError        = StringVar()
        self.formatError        = StringVar()
        self.editSetting        = StringVar()
        self.setting            = StringVar()
        self.about              = StringVar()
        self.supportSystem      = StringVar()
        self.versionString      = StringVar()
        self.releaseDate        = StringVar()
        self.checksum           = StringVar()

        self.outputPath         = StringVar()
        self.inputPath          = StringVar()
        self.selectPath         = StringVar()
        self.saveAndReturn      = StringVar()
        self.zhHK               = StringVar()
        self.english            = StringVar()
        self.logPath            = StringVar()


        self.downloadReport     = StringVar()
        self.waitingExe         = StringVar()
        self.waitingLogin       = StringVar()
        self.loginSuccess       = StringVar()
        self.completed          = StringVar()
        self.processing         = StringVar()
        self.processException   = StringVar()
        self.processCompleted   = StringVar()
        self.buildReport        = StringVar()

        self.sliderMenuRobot    = StringVar()
        self.languageUpdate     = StringVar()

        self.checkForUpdate     = StringVar()
        self.checkPackage       = StringVar()
        self.updateCompleted    = StringVar()
        self.updateCompleted    = StringVar()
        self.noUpdate           = StringVar()

        self.emailSystem        = StringVar()

        self.configNotFound     = StringVar()

        self.SetString()
        pass

    def SetString(self):
        self.config = GetConfigSingletion()

        if self.config.IsConfigExist('language','display') == False:
            self.config.WriteConfig('language','display','zh')

        if self.config.ReadConfig("language","display") == "zh":
            self.importPolicy.set(self.zhString[0])
            self.importManualPolicy.set(self.zhString[1])
            self.clear.set(self.zhString[2])
            self.startRobot.set(self.zhString[3])
            self.exportReport.set(self.zhString[4])
            self.importError.set(self.zhString[5])
            self.formatError.set(self.zhString[6])
            self.editSetting.set(self.zhString[7])
            self.setting.set(self.zhString[8])
            self.about.set(self.zhString[9])
            self.supportSystem.set(self.zhString[10])
            self.versionString.set(self.zhString[11])
            self.releaseDate.set(self.zhString[12])
            self.checksum.set(self.zhString[13])
            self.outputPath.set(self.zhString[14])
            self.inputPath.set(self.zhString[15])
            self.selectPath.set(self.zhString[16])
            self.saveAndReturn.set(self.zhString[17])
            self.zhHK.set(self.zhString[18]) 
            self.english.set(self.zhString[19])
            self.downloadReport.set(self.zhString[20])
            self.waitingExe.set(self.zhString[21])
            self.waitingLogin.set(self.zhString[22])
            self.loginSuccess.set(self.zhString[23])
            self.completed.set(self.zhString[24])
            self.processing.set(self.zhString[25])
            self.processException.set(self.zhString[26])
            self.processCompleted.set(self.zhString[27])
            self.buildReport.set(self.zhString[28])
            self.logPath.set(self.zhString[29])
            self.sliderMenuRobot.set(self.zhString[30])
            self.languageUpdate.set(self.zhString[31])
            self.checkForUpdate.set(self.zhString[32])
            self.checkPackage.set(self.zhString[33])
            self.updateCompleted.set(self.zhString[34])
            self.noUpdate.set(self.zhString[35])
            self.emailSystem.set(self.zhString[36])
            self.configNotFound.set(self.zhString[37])

        else:
            self.importPolicy.set(self.enString[0])
            self.importManualPolicy.set(self.enString[1])
            self.clear.set(self.enString[2])
            self.startRobot.set(self.enString[3])
            self.exportReport.set(self.enString[4])
            self.importError.set(self.enString[5])
            self.formatError.set(self.enString[6])
            self.editSetting.set(self.enString[7])
            self.setting.set(self.enString[8])
            self.about.set(self.enString[9])
            self.supportSystem.set(self.enString[10])
            self.versionString.set(self.enString[11])
            self.releaseDate.set(self.enString[12])
            self.checksum.set(self.enString[13])
            self.outputPath.set(self.enString[14])
            self.inputPath.set(self.enString[15])
            self.selectPath.set(self.enString[16])
            self.saveAndReturn.set(self.enString[17])
            self.zhHK.set(self.enString[18]) 
            self.english.set(self.enString[19])
            self.downloadReport.set(self.enString[20])
            self.waitingExe.set(self.enString[21])
            self.waitingLogin.set(self.enString[22])
            self.loginSuccess.set(self.enString[23])
            self.completed.set(self.enString[24])
            self.processing.set(self.enString[25])
            self.processException.set(self.enString[26])
            self.processCompleted.set(self.enString[27])
            self.buildReport.set(self.enString[28])
            self.logPath.set(self.enString[29])
            self.sliderMenuRobot.set(self.enString[30])
            self.languageUpdate.set(self.enString[31])
            self.checkForUpdate.set(self.enString[32])
            self.checkPackage.set(self.enString[33])
            self.updateCompleted.set(self.enString[34])
            self.noUpdate.set(self.enString[35])
            self.emailSystem.set(self.enString[36])
            self.configNotFound.set(self.enString[37])


        
    def CompanyFullName(self,companyName):
        if companyName == 'PRU':
            return 'PRUDENTIAL'
        else:
            return companyName

def GetStringSingletionCTK():
    if _StringSingletonCTK._stringInstance is None:
        _StringSingletonCTK._stringInstance = _StringSingletonCTK()

    return _StringSingletonCTK._stringInstance