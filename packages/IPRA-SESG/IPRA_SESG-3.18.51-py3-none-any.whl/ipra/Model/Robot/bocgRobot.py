import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import xlsxwriter
from ipra.Model.Robot.baseRobot import BaseRobot
import threading
from selenium.webdriver.common.by import By

class BOCGRobot(BaseRobot):

    def __init__(self, policyList, frame, reportPath,inputPath):
        super().__init__(policyList, frame, reportPath,inputPath)
        self.logger.writeLogString('BOCG-INIT','ROBOT INIT')
        self.maxPolicyListSize = len(policyList)
        self.workbook = xlsxwriter.Workbook(self.reportPath+'BOCG_report.xlsx')
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.write(0, 0, "Policy No.")
        self.logger.writeLogString('BOCG-INIT','maxPolicyListSize:'+str(self.maxPolicyListSize))

    def waitingLoginComplete(self):
        self.logger.writeLogString('BOCG-LOGIN','START LOGIN')
        self.browser.get("https://www.boclifeonline.com/SalesPortal/login2.html")
        self.frame.setStatusLableText(self.stringValue.waitingLogin.get())
        while not self.isLogin and not self.isStopped:
            try:
                self.browser.find_element(By.XPATH, "/html/body/section/div/div/div/div/ul/li[2]/a").click()
                self.browser.find_element(By.XPATH, "/html/body/section/div/div/div/div/ul/li[2]/div/a[1]/span").click()
                self.isLogin=True
            except:
                time.sleep(3)
        else:
            pass

        if self.isLogin:
            self.frame.setStatusLableText(self.stringValue.loginSuccess.get())
            self.logger.writeLogString('BOCG-LOGIN','LOGIN COMPLETED')

    def scrapPolicy(self):
        for policy in self.policyList:

            if self.isStopped:
                return

            self.frame.setStatusLableText(self.stringValue.processing.get().format(str(policy)))
            self.logger.writeLogString('BOCG','PROCESSING:'+str(policy))
            try:
                WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/div/form/div[1]/div[3]/div[1]/div[2]/div/input")))
                input_field = self.browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/div/form/div[1]/div[3]/div[1]/div[2]/div/input")
                input_field.click()
                input_field.clear()
                time.sleep(1)
                input_field.send_keys(policy)
                search_button = self.browser.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/div/form/div[1]/div[4]/div/div/button[1]")
                search_button.click()
                time.sleep(1)
                element = self.browser.find_element(By.LINK_TEXT, policy)
                element.send_keys(Keys.CONTROL + Keys.RETURN)
                self.browser.switch_to.window(self.browser.window_handles[1])
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                file1 = open(self.reportPath+policy+".txt","a",encoding="utf-8")#append mode 
                file1.write(soup.prettify()) 
                file1.close()
                self.browser.close()
                self.browser.switch_to.window(self.browser.window_handles[0])
            except Exception as ex:
                self.frame.setStatusLableText(self.stringValue.processException.get().format(str(policy),str(ex)))
                self.logger.writeLogString('BOCG',str(policy)+" throws Exception:" + str(ex))
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            finally:
                self.frame.setStatusLableText(self.stringValue.processCompleted.get().format(str(policy)))
                self.logger.writeLogString('BOCG',str(policy)+" COMPLETED")
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
 
    def __buildReportHeaderFullFlow(self):
        self.logger.writeLogString('BOCG-HEADER','START BUILD HEADER FULLFLOW')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildHeaderQueue:
                self.logger.writeLogString('BOCG-HEADER','POLICY NO.:{0}'.format(str(policy)))
                if self.isStopped:
                    return
                try:
                    file = open(self.reportPath+policy+".txt",encoding="utf-8")#append mode 
                    #Full Html src
                    soup_all_src = BeautifulSoup(file.read(), 'lxml')
                    file.close()

                    soup_basic = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','basic-info')
                    soup_insured = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','insured-info')
                    soup_policy = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','policy-value')
                    soup_payment = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','payment-status')
                    
                    next_idx = 1
                    for strong_tag in soup_basic.find_all('th'):
                        #row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        self.worksheet.write(0,next_idx,strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        next_idx = next_idx + 1
                    for strong_tag in soup_insured.find_all('th'):
                        #row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        self.worksheet.write(0,next_idx,strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        next_idx = next_idx + 1
                    for strong_tag in soup_policy.find_all('th'):
                        #row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        self.worksheet.write(0,next_idx,strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        next_idx = next_idx + 1
                    for strong_tag in soup_payment.find_all('th'):
                        #row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        self.worksheet.write(0,next_idx,strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                        next_idx = next_idx + 1
                    #for col_num, data in enumerate(row_header):
                    #    self.worksheet.write(0, col_num+1, data)
                        
                    #No error when building the header,break all loop and then stop this thread
                    policy_iteration = self.maxPolicyListSize + 1
                    self.logger.writeLogString('BOCG-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                    break
                except FileNotFoundError:
                    self.logger.writeLogString('BOCG-HEADER','FILE NOT FOUND')
                except Exception as ex:
                    self.logger.writeLogString('BOCG-HEADER','EXCEPTION:'+str(ex))
                finally:
                    policy_iteration = policy_iteration + 1
                    if policy in self.buildHeaderQueue:
                        self.buildHeaderQueue.remove(policy)
            else:
                time.sleep(1)                        
    
    def __buildReportHeaderHalfFlow(self):
        self.logger.writeLogString('BOCG-HEADER','START BUILD HEADER HALFFLOW')
        for policy in self.policyList:
            self.logger.writeLogString('BOCG-HEADER','POLICY NO.:{0}'.format(str(policy)))
            if self.isStopped:
                return
            try:
                file = open(self.inputPath+policy+".txt",encoding="utf-8")#append mode 
                #Full Html src
                soup_all_src = BeautifulSoup(file.read(), 'lxml')
                file.close()

                soup_basic = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','basic-info')
                soup_insured = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','insured-info')
                soup_policy = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','policy-value')
                soup_payment = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','payment-status')
                
                next_idx = 1
                for strong_tag in soup_basic.find_all('th'):
                    #row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    self.worksheet.write(0,next_idx,strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    next_idx = next_idx + 1
                for strong_tag in soup_insured.find_all('th'):
                    #row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    self.worksheet.write(0,next_idx,strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    next_idx = next_idx + 1
                for strong_tag in soup_policy.find_all('th'):
                    #row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    self.worksheet.write(0,next_idx,strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    next_idx = next_idx + 1
                for strong_tag in soup_payment.find_all('th'):
                    #row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    self.worksheet.write(0,next_idx,strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    next_idx = next_idx + 1
                #for col_num, data in enumerate(row_header):
                #    self.worksheet.write(0, col_num+1, data)
                    
                #No error when building the header,break all loop and then stop this thread
                self.logger.writeLogString('BOCG-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                break
            except FileNotFoundError as ex:
                self.logger.writeLogString('BOCG-HEADER','FILE NOT FOUND')
            except Exception as ex:
                self.logger.writeLogString('BOCG-HEADER','EXCEPTION:'+str(ex))

    def __buildReport(self):
        self.logger.writeLogString('BOCG-CONTENT','START BUILD REPORT')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildReportQueue:
                if self.isStopped:
                    return
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),""))
                self.logger.writeLogString('BOCG-CONTENT','POLICY NO.:{0}'.format(str(policy)))
                try:
                    self.worksheet.write(policy_iteration+1,0,str(policy))
                    file = open(self.reportPath+policy+".txt",encoding="utf-8")#append mode 
                    #Full Html src
                    soup_all_src = BeautifulSoup(file.read(), 'html.parser')
                    file.close()
                    
                    soup_basic = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','basic-info')
                    soup_insured = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','insured-info')
                    soup_policy = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','policy-value')
                    soup_payment = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','payment-status')
                    
                    row_value = []
                    for strong_tag in soup_basic.find_all('td'):
                        row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    for strong_tag in soup_insured.find_all('td'):
                        row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    for strong_tag in soup_policy.find_all('td'):
                        row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    for strong_tag in soup_payment.find_all('td'):
                        row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    for col_num, data in enumerate(row_value):
                        self.worksheet.write(policy_iteration+1, col_num+1, data)
                    
                except FileNotFoundError:
                    self.worksheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                    self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"not found"))
                    self.logger.writeLogString('BOCG-CONTENT','FILE NOT FOUND')
                    self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
                except Exception as ex :
                    self.worksheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!")
                    self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"failed"))
                    self.logger.writeLogString('BOCG-CONTENT','EXCEPTION:'+str(ex))
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
        self.logger.writeLogString('BOCG-CONTENT','COMPLETED BUILD REPORT')

    def __buildReportOnly(self):
        self.logger.writeLogString('BOCG-CONTENT','START BUILD REPORT OFFLINE MODE')
        for policy_iteration,policy in enumerate(self.policyList):
            if self.isStopped:
                return
            self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),""))
            self.logger.writeLogString('BOCG-CONTENT','POLICY NO.:{0}'.format(str(policy)))
            try:
                self.worksheet.write(policy_iteration+1,0,str(policy))
                file = open(self.inputPath+policy+".txt",encoding="utf-8")#append mode 
                #Full Html src
                soup_all_src = BeautifulSoup(file.read(), 'html.parser')
                file.close()
                
                soup_basic = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','basic-info')
                soup_insured = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','insured-info')
                soup_policy = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','policy-value')
                soup_payment = self.SearchByHtmlTagValueKey(soup_all_src,'div','id','payment-status')
                
                row_value = []
                for strong_tag in soup_basic.find_all('td'):
                    row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                for strong_tag in soup_insured.find_all('td'):
                    row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                for strong_tag in soup_policy.find_all('td'):
                    row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                for strong_tag in soup_payment.find_all('td'):
                    row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                for col_num, data in enumerate(row_value):
                    self.worksheet.write(policy_iteration+1, col_num+1, data)
                
            except FileNotFoundError:
                self.worksheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"not found"))
                self.logger.writeLogString('BOCG-CONTENT','FILE NOT FOUND')
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            except Exception as ex :
                self.worksheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!")
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"not found"))
                self.logger.writeLogString('BOCG-CONTENT','EXCEPTION:'+str(ex))
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            finally:
                self.frame.setStatusProgresValueByValue(2)
                self.frame.setListItemColor(str(policy),self.STATUS_REPORT_COMPLETE)
                      
        self.buildHeaderThread.join()
        self.workbook.close()
        self.frame.setStatusLableText(self.stringValue.completed.get())
        self.logger.writeLogString('BOCG-CONTENT','COMPLETED BUILD REPORT OFFLINE MODE')

