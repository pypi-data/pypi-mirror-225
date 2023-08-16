from genericpath import exists
import os
from ipra.Model.Robot.baseRobot import BaseRobot
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import xlsxwriter
import threading

class ChubbRobot(BaseRobot):
    def __init__(self, policyList, frame, reportPath,inputPath,downloadReport):
        super().__init__(policyList, frame, reportPath,inputPath,downloadReport)
        self.logger.writeLogString('CHUBB-INIT','ROBOT INIT')

        self.maxPolicyListSize = len(policyList)
        self.workbook = xlsxwriter.Workbook(self.reportPath+'CHUBB_report.xlsx')
        self.worksheet = self.workbook.add_worksheet(name="General Information")
        self.worksheet.write(0, 0, "Policy No.")
        self.logger.writeLogString('CHUBB-INIT','maxPolicyListSize:'+str(self.maxPolicyListSize))

        pass

    def waitingLoginComplete(self):
        self.frame.setStatusLableText(self.stringValue.waitingLogin.get())
        self.logger.writeLogString('CHUBB-LOGIN','START LOGIN')
        
        try:
            self.browser.get("https://sss.chubblife.com.hk/a3s/web/main/login.jsp?fromChgV=Y&closewindow=null")
            self.browser.switch_to.window(self.browser.window_handles[1])
            self.browser.close()
            self.browser.switch_to.window(self.browser.window_handles[0])
        except:
            pass
            
        while not self.isLogin and not self.isStopped:
            try:
                self.browser.find_element(By.ID, 'sideBar_QuickLink')
                self.browser.get("https://sss.chubblife.com.hk/a3s/goHome.do?reqCode=goToHomePage&ssolink=Y&func_code=FN090090")
                time.sleep(3)
                self.browser.find_element(By.XPATH, "//a[text()='電子服務']").click()
                time.sleep(2)
                self.browser.close()
                self.browser.switch_to.window(self.browser.window_handles[0])
                self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/section/div/div/es-twocolumn-page/div/div[2]/div[2]/es-twocolumn-bottomside/div/es-sidelink/div/a[2]/div/div/h5").click()
                time.sleep(2)
                self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div/es-footer/footer/div/div[1]/a[5]").click()
                self.isLogin=True
                time.sleep(1)
                
            except:
                time.sleep(3)
        else:
            pass
        
        if self.isLogin:
            self.frame.setStatusLableText(self.stringValue.loginSuccess.get())
            self.logger.writeLogString('CHUBB-LOGIN','LOGIN COMPLETED')

    def scrapPolicy(self):
        for policy in self.policyList:
            if self.isStopped:
                return
            try:
                self.frame.setStatusLableText(self.stringValue.processing.get().format(str(policy)))
                self.logger.writeLogString('CHUBB','PROCESSING:'+str(policy))

                input = self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/section/div/div/es-twocolumn-page/div/div[2]/div[1]/es-twocolumn-body/div/es-panel[1]/div/div[2]/div[2]/div[3]/div/input")
                input.clear()
                input.send_keys(str(policy))
                
                self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/section/div/div/es-twocolumn-page/div/div[2]/div[1]/es-twocolumn-body/div/es-panel[1]/div/div[2]/div[5]/div[2]/button").click()
                
                time.sleep(3)

                self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/section/div/div/es-twocolumn-page/div/div[2]/div[1]/es-twocolumn-body/div/es-panel[2]/div/div[2]/div/es-table/div/table/tbody/tr[1]/td[2]/span/div/span").click()
                
                time.sleep(1)
                
                isWaitingPrompt = True
                while isWaitingPrompt:
                    try:
                        self.browser.find_element(By.LINK_TEXT, str(policy)).click()
                        isWaitingPrompt = False
                    except:
                        time.sleep(1)

                isWaitingPrompt = True
                while isWaitingPrompt:
                    try:
                        self.browser.switch_to.window(self.browser.window_handles[1])
                        isWaitingPrompt = False
                    except:
                        time.sleep(1)
                        
                isWaitingPrompt = True
                while isWaitingPrompt:
                    try:
                        self.browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/section/div/div/es-twocolumn-page/div/div[2]/div[1]/es-twocolumn-body/div/es-panel/div/div[2]/div/div[1]/div[1]/div[1]")
                        isWaitingPrompt = False
                    except:
                        time.sleep(1)
                
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                file1 = open(str(self.reportPath+policy)+".txt","a",encoding="utf-8")#append mode 
                file1.write(soup.prettify()) 
                file1.close()
                
                self.downloadPolicyReport(str(policy))
                    
                self.browser.close()
                self.browser.switch_to.window(self.browser.window_handles[0])
                
            except Exception as ex:
                self.frame.setStatusLableText(self.stringValue.processException.get().format(str(policy),str(ex)))
                self.logger.writeLogString('CHUBB',str(policy)+" throws Exception:" + str(ex))
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            finally:
                self.frame.setStatusLableText(self.stringValue.processCompleted.get().format(str(policy)))
                self.logger.writeLogString('CHUBB',str(policy)+" COMPLETED")
                self.frame.setStatusProgresValueByValue(1)
                self.buildReportQueue.append(policy)
                self.buildHeaderQueue.append(policy)
                self.frame.setListItemColor(str(policy),self.STATUS_SCRAP_COMPLETE)

    def buildReport(self):
        self.buildReportThread = threading.Thread(target = self.__buildReport)
        self.buildReportThread.start()
        self.buildReportHeaderFullFlow()
        pass

    def buildReportOnly(self):
        self.buildReportThread = threading.Thread(target = self.__buildReportOnly)
        self.buildReportThread.start()
        self.buildReportHeaderHalfFlow()
        pass

    def buildReportHeaderFullFlow(self):
        self.buildHeaderThread = threading.Thread(target = self.__buildReportHeaderFullFlow)
        self.buildHeaderThread.start()
        pass
    
    def buildReportHeaderHalfFlow(self):
        self.buildHeaderThread = threading.Thread(target = self.__buildReportHeaderHalfFlow)
        self.buildHeaderThread.start()
        pass

    def downloadPolicyReport(self, policy):
        if not self.downloadReport:
            return
        
        reportFullPath = self.reportPath+"安達電子服務平台.pdf"
        self.browser.execute_script('window.print();')
        while exists(reportFullPath) == False:
            time.sleep(1)
        os.rename(reportFullPath,self.reportPath+policy+".pdf")

    def __buildReportHeaderFullFlow(self):
        self.logger.writeLogString('CHUBB-HEADER','START BUILD HEADER FULLFLOW')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildHeaderQueue:
                self.logger.writeLogString('CHUBB-HEADER','POLICY NO.:{0}'.format(str(policy)))
                if self.isStopped:
                    return
                try:
                    file = open(self.reportPath+policy+".txt",encoding="utf-8")#append mode 
                    #Full Html src
                    soup_all_src = BeautifulSoup(file.read(), 'lxml')
                    file.close()
                    
                    soupPrimary = soup_all_src.find('div',attrs={'ui-view':'content-primary'})
                    soupPrimary.find('div',attrs={'class':'row ng-scope'}).decompose()
                    
                    idx = 0
                    for tag in soupPrimary.find_all('strong',attrs={'class':'ng-binding'}):
                        self.worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        idx = idx + 1
                        
                        
                    soupSecondary = soup_all_src.find('div',attrs={'ui-view':'content-secondary'})
                    soupValue = soupSecondary.find('div',attrs={'class':'row page-break ng-scope'})
                    
                    for tag in soupValue.find_all('strong',attrs={'class':'ng-binding'}):
                        self.worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        idx = idx + 1
                    
                    soupPayment = soupSecondary.find_all('es-panel')
                    #The first one is policy value, remove it
                    soupPayment.pop()
                    temp = soupPayment.pop()
                    soupPayment = temp.find_all('tbody')
                    for tbody in soupPayment:
                        for tag in tbody.find_all('tr'):
                            if tag.has_attr('class'):
                                continue
                            else:
                                self.worksheet.write(0, idx+1, tag.find('strong').text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                                idx = idx + 1

                    soupPlan = str(soupSecondary.find('uib-accordion'))
                    soupSecondary.find('uib-accordion').decompose()
                    soupBenefit = soupSecondary.find('uib-accordion')
                    
                    headerList = []
                    for tag in soupBenefit.find_all('th'):
                        headerList.append(tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        
                    headerList = headerList * 3
                    for header in headerList:
                        self.worksheet.write(0, idx+1, header)
                        idx = idx + 1
                        
                    soupPlan = BeautifulSoup(soupPlan,'lxml')
                    for tag in soupPlan.find_all('th'):
                        self.worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        idx = idx + 1
                    #No error when building the header,break all loop and then stop this thread
                    policy_iteration = self.maxPolicyListSize + 1
                    self.logger.writeLogString('CHUBB-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                    break
                except FileNotFoundError:
                    self.logger.writeLogString('CHUBB-HEADER','FILE NOT FOUND')
                except Exception as ex:
                    self.logger.writeLogString('CHUBB-HEADER','EXCEPTION:'+str(ex))
                finally:
                    policy_iteration = policy_iteration + 1
                    if policy in self.buildHeaderQueue:
                        self.buildHeaderQueue.remove(policy)
            else:
                time.sleep(1)                        

    def __buildReportHeaderHalfFlow(self):
        self.logger.writeLogString('CHUBB-HEADER','START BUILD HEADER HALFFLOW')
        for policy in self.policyList:
            self.logger.writeLogString('CHUBB-HEADER','POLICY NO.:{0}'.format(str(policy)))
            if self.isStopped:
                return
            try:
                file = open(self.inputPath+policy+".txt",encoding="utf-8")#append mode 
                #Full Html src
                soup_all_src = BeautifulSoup(file.read(), 'lxml')
                file.close()
                
                soupPrimary = soup_all_src.find('div',attrs={'ui-view':'content-primary'})
                soupPrimary.find('div',attrs={'class':'row ng-scope'}).decompose()
                
                idx = 0
                for tag in soupPrimary.find_all('strong',attrs={'class':'ng-binding'}):
                    self.worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    idx = idx + 1
                    
                    
                soupSecondary = soup_all_src.find('div',attrs={'ui-view':'content-secondary'})
                soupValue = soupSecondary.find('div',attrs={'class':'row page-break ng-scope'})
                
                for tag in soupValue.find_all('strong',attrs={'class':'ng-binding'}):
                    self.worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    idx = idx + 1
                
                soupPayment = soupSecondary.find_all('es-panel')
                #The first one is policy value, remove it
                soupPayment.pop()
                temp = soupPayment.pop()
                soupPayment = temp.find_all('tbody')
                for tbody in soupPayment:
                    for tag in tbody.find_all('tr'):
                        if tag.has_attr('class'):
                            continue
                        else:
                            self.worksheet.write(0, idx+1, tag.find('strong').text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                            idx = idx + 1

                soupPlan = str(soupSecondary.find('uib-accordion'))
                soupSecondary.find('uib-accordion').decompose()
                soupBenefit = soupSecondary.find('uib-accordion')
                
                headerList = []
                for tag in soupBenefit.find_all('th'):
                    headerList.append(tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    
                headerList = headerList * 3
                for header in headerList:
                    self.worksheet.write(0, idx+1, header)
                    idx = idx + 1
                    
                soupPlan = BeautifulSoup(soupPlan,'lxml')
                for tag in soupPlan.find_all('th'):
                    self.worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    idx = idx + 1

                #No error when building the header,break all loop and then stop this thread
                self.logger.writeLogString('CHUBB-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                break
            except FileNotFoundError as ex:
                self.logger.writeLogString('CHUBB-HEADER','FILE NOT FOUND')
            except Exception as ex:
                self.logger.writeLogString('CHUBB-HEADER','EXCEPTION:'+str(ex))

    def __buildReport(self):
        self.logger.writeLogString('CHUBB-CONTENT','START BUILD REPORT')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildReportQueue:
                if self.isStopped:
                    return
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),""))
                self.logger.writeLogString('CHUBB-CONTENT','POLICY NO.:{0}'.format(str(policy)))
                try:
                    self.worksheet.write(policy_iteration+1,0,str(policy))
                    file = open(self.reportPath+policy+".txt",encoding="utf-8")#append mode 
                    #Full Html src
                    soup_all_src = BeautifulSoup(file.read(), 'lxml')
                    file.close()
                    
                    soupPrimary = soup_all_src.find('div',attrs={'ui-view':'content-primary'})
                    soupPrimary.find('div',attrs={'class':'row ng-scope'}).decompose()
                    
                    idx = 0
                    for tag in soupPrimary.find_all('td',attrs={'class':'ng-binding'}):
                        self.worksheet.write(policy_iteration+1, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        idx = idx + 1
                        
                    soupSecondary = soup_all_src.find('div',attrs={'ui-view':'content-secondary'})
                    soupValue = soupSecondary.find('div',attrs={'class':'row page-break ng-scope'})
                    
                    for tag in soupValue.find_all('div',attrs={'class':'col-md-6 col-sm-6 col-xs-6 text-right ng-binding'}):
                        self.worksheet.write(policy_iteration+1, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        idx = idx + 1
                    
                    
                    soupPayment = soupSecondary.find_all('es-panel')
                    #The first one is policy value, remove it
                    soupPayment.pop()
                    temp = soupPayment.pop()
                    soupPayment = temp.find_all('tbody')
                    for tbody in soupPayment:
                        for tag in tbody.find_all('tr'):
                            if tag.has_attr('class'):
                                continue
                            else:
                                self.worksheet.write(policy_iteration+1, idx+1, 
                                                    tag.find('td',attrs={'class':'col-sm-3 col-xs-6 col-print-3 ng-binding'}).
                                                    text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                                idx = idx + 1
                    
                    soupPlan = str(soupSecondary.find('uib-accordion'))
                    soupSecondary.find('uib-accordion').decompose()
                    soupBenefit = soupSecondary.find('uib-accordion')
                    
                    valueList = ['','','','','','','','','','','','']
                    for iteration,tag in enumerate(soupBenefit.find_all('td')):
                        valueList[iteration] = tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')

                    for value in valueList:
                        self.worksheet.write(policy_iteration+1, idx+1, value)
                        idx = idx + 1
                        
                    soupPlan = BeautifulSoup(soupPlan,'lxml')
                    soupPlan = soupPlan.find('tbody')
                    while soupPlan.find('table') != None:
                        soupPlan.find('table').decompose()
                    for tag in soupPlan.find_all('td'):
                        self.worksheet.write(policy_iteration+1, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        idx = idx + 1
                except FileNotFoundError:
                    self.worksheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                    self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"not found"))
                    self.logger.writeLogString('CHUBB-CONTENT','FILE NOT FOUND')
                    self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
                except Exception as ex:
                    self.worksheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!"+str(ex))
                    self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"failed"))
                    self.logger.writeLogString('CHUBB-CONTENT','EXCEPTION:'+str(ex))
                    self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
                finally:
                    self.frame.setStatusProgresValueByValue(1)
                    policy_iteration = policy_iteration + 1
                    if policy in self.buildReportQueue:
                        self.buildReportQueue.remove(policy)
                    self.frame.setListItemColor(str(policy),self.STATUS_REPORT_COMPLETE)
            else:
                time.sleep(1)                    
                    
        self.buildHeaderThread.join()
        self.workbook.close()
        self.frame.setStatusLableText(self.stringValue.completed.get())
        self.logger.writeLogString('CHUBB-CONTENT','COMPLETED BUILD REPORT')

    def __buildReportOnly(self):
        self.logger.writeLogString('CHUBB-CONTENT','START BUILD REPORT OFFLINE MODE')
        for policy_iteration,policy in enumerate(self.policyList):
            if self.isStopped:
                return
            self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),""))
            self.logger.writeLogString('CHUBB-CONTENT','POLICY NO.:{0}'.format(str(policy)))
            try:
                self.worksheet.write(policy_iteration+1,0,str(policy))
                file = open(self.inputPath+policy+".txt",encoding="utf-8")#append mode 
                #Full Html src
                soup_all_src = BeautifulSoup(file.read(), 'lxml')
                file.close()
                
                soupPrimary = soup_all_src.find('div',attrs={'ui-view':'content-primary'})
                soupPrimary.find('div',attrs={'class':'row ng-scope'}).decompose()
                
                idx = 0
                for tag in soupPrimary.find_all('td',attrs={'class':'ng-binding'}):
                    self.worksheet.write(policy_iteration+1, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    idx = idx + 1
                    
                soupSecondary = soup_all_src.find('div',attrs={'ui-view':'content-secondary'})
                soupValue = soupSecondary.find('div',attrs={'class':'row page-break ng-scope'})
                
                for tag in soupValue.find_all('div',attrs={'class':'col-md-6 col-sm-6 col-xs-6 text-right ng-binding'}):
                    self.worksheet.write(policy_iteration+1, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    idx = idx + 1
                
                
                soupPayment = soupSecondary.find_all('es-panel')
                #The first one is policy value, remove it
                soupPayment.pop()
                temp = soupPayment.pop()
                soupPayment = temp.find_all('tbody')
                for tbody in soupPayment:
                    for tag in tbody.find_all('tr'):
                        if tag.has_attr('class'):
                            continue
                        else:
                            self.worksheet.write(policy_iteration+1, idx+1, 
                                                tag.find('td',attrs={'class':'col-sm-3 col-xs-6 col-print-3 ng-binding'}).
                                                text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                            idx = idx + 1
                
                soupPlan = str(soupSecondary.find('uib-accordion'))
                soupSecondary.find('uib-accordion').decompose()
                soupBenefit = soupSecondary.find('uib-accordion')
                
                valueList = ['','','','','','','','','','','','']
                for iteration,tag in enumerate(soupBenefit.find_all('td')):
                    valueList[iteration] = tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')

                for value in valueList:
                    self.worksheet.write(policy_iteration+1, idx+1, value)
                    idx = idx + 1
                    
                soupPlan = BeautifulSoup(soupPlan,'lxml')
                soupPlan = soupPlan.find('tbody')
                while soupPlan.find('table') != None:
                    soupPlan.find('table').decompose()
                for tag in soupPlan.find_all('td'):
                    self.worksheet.write(policy_iteration+1, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    idx = idx + 1

                    
            except FileNotFoundError:
                self.worksheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"not found"))
                self.logger.writeLogString('CHUBB-CONTENT','FILE NOT FOUND')
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            except Exception as ex:
                self.worksheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!"+str(ex))
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"failed"))
                self.logger.writeLogString('CHUBB-CONTENT','EXCEPTION:'+str(ex))
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            finally:
                self.frame.setStatusProgresValueByValue(2)
                self.frame.setListItemColor(str(policy),self.STATUS_REPORT_COMPLETE)

        self.buildHeaderThread.join()
        self.workbook.close()
        self.frame.setStatusLableText(self.stringValue.completed.get())
        self.logger.writeLogString('CHUBB-CONTENT','COMPLETED BUILD REPORT OFFLINE MODE')
