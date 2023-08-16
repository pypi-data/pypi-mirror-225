from concurrent.futures import thread
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
import zipfile

class GeneraliRobot(BaseRobot):
    def __init__(self, policyList, frame, reportPath,inputPath,downloadReport):
        super().__init__(policyList, frame, reportPath,inputPath,downloadReport)

        self.logger.writeLogString('GENERALI-INIT','ROBOT INIT')

        self.maxPolicyListSize = len(policyList)
        self.workbook = xlsxwriter.Workbook(self.reportPath+'GENERALI_report.xlsx')

        self.basicInfo_sheet = self.workbook.add_worksheet(name="General Information")
        self.basicInfo_sheet.write(0, 0, "Policy No.")

        self.customer_sheet = self.workbook.add_worksheet(name="Customer Information")
        self.customer_sheet.write(0, 0, "Policy No.")

        self.payment_sheet = self.workbook.add_worksheet(name="Payment Information")
        self.payment_sheet.write(0, 0, "Policy No.")

        self.logger.writeLogString('GENERALI-INIT','maxPolicyListSize:'+str(self.maxPolicyListSize))

    def waitingLoginComplete(self):
        self.frame.setStatusLableText(self.stringValue.waitingLogin.get())
        self.logger.writeLogString('GENERALI-LOGIN','START LOGIN')
        self.browser.get("https://genconnect.generali.com.hk/pos/")

        while not self.isLogin and not self.isStopped:
            try:
                self.browser.find_element(By.XPATH,"/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-nav/app-home-landing/ion-content/div/div/div[4]/app-home-item/div/div[1]").click()
                time.sleep(1)
                self.isLogin=True

            except:
                time.sleep(3)
        else:
            pass

        if self.isLogin:
            self.frame.setStatusLableText(self.stringValue.loginSuccess.get())
            self.logger.writeLogString('GENERALI-LOGIN','LOGIN COMPLETED')

    def scrapPolicy(self):
        for policy in self.policyList:
            if self.isStopped:
                return
            try:
                self.frame.setStatusLableText(self.stringValue.processing.get().format(str(policy)))
                self.logger.writeLogString('GENERALI','PROCESSING:'+str(policy))
                
                self.DoClickUntilNoException("/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-nav/app-policy-inquiry/ion-content/div/div/div[2]/div/ion-row/ion-col/app-search-criteria-input/ion-grid/ion-row/ion-col[1]/div")
                time.sleep(1)
                self.DoClickUntilNoException("/html/body/app-root/ion-app/ion-popover/div[2]/div[2]/ion-select-popover/ion-list/ion-radio-group/ion-item[3]")
                time.sleep(1)
                
                input = self.browser.find_element(By.XPATH,"/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-nav/app-policy-inquiry/ion-content/div/div/div[2]/div/ion-row/ion-col/app-search-criteria-input/ion-grid/ion-row/ion-col[2]/ion-row/ion-col[1]/ion-input/input")
                input.clear()
                input.send_keys(str(policy))
                time.sleep(1)
                
                #Add policy no. to search rule
                self.DoClickUntilNoException("/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-nav/app-policy-inquiry/ion-content/div/div/div[2]/div/ion-row/ion-col/app-search-criteria-input/ion-grid/ion-row/ion-col[2]/ion-row/ion-col[2]/div")
                time.sleep(1)
                
                #Click to search
                self.DoClickUntilNoException("/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-nav/app-policy-inquiry/ion-content/div/div/div[3]/div/div/div[2]")
                
                #Download report ZIP
                self.downloadPolicyReport(str(policy))
                
                #Click policy link
                self.DoClickUntilNoException("/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-nav/app-policy-inquiry/ion-content/div/div/div[4]/div/app-datatable-pagination/div[3]/ion-grid/div/ion-row/ion-col[2]")
                time.sleep(7)
                
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                file1 = open(str(self.reportPath+policy)+"_basic.txt","a",encoding="utf-8")#append mode 
                file1.write(soup.prettify())
                file1.close()
                
                self.DoClickUntilNoException("/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-nav/app-policy-detail/ion-content/ion-segment/ion-segment-button[2]")
                time.sleep(8)
                
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                file1 = open(str(self.reportPath+policy)+"_customer.txt","a",encoding="utf-8")#append mode 
                file1.write(soup.prettify())
                file1.close()
                
                self.DoClickUntilNoException("/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-nav/app-policy-detail/ion-content/ion-segment/ion-segment-button[3]")
                time.sleep(8)
                
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                file1 = open(str(self.reportPath+policy)+"_payment.txt","a",encoding="utf-8")#append mode 
                file1.write(soup.prettify())
                file1.close()
                

                self.DoClickUntilNoException("/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-nav/app-policy-detail/nano-title-bar/ion-header/ion-toolbar/ion-button/div")
                time.sleep(3)
                self.DoClickUntilNoException("/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-nav/app-policy-inquiry/ion-content/div/div/div[2]/div/ion-row/ion-col/app-search-criteria-input/ion-row/ion-col/app-search-criteria/div/div[2]")
                time.sleep(1)
                pass
            except Exception as ex:
                self.frame.setStatusLableText(self.stringValue.processException.get().format(str(policy),str(ex)))
                self.logger.writeLogString('GENERALI',str(policy)+" throws Exception:" + str(ex))
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            finally:
                self.frame.setStatusLableText(self.stringValue.processCompleted.get().format(str(policy)))
                self.logger.writeLogString('GENERALI',str(policy)+" COMPLETED")
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
        
        #Click header "Select All", max wait 20s
        self.DoClickUntilNoException("/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-nav/app-policy-inquiry/ion-content/div/div/div[4]/div/app-datatable-pagination/div[3]/ion-grid/div/ion-row/ion-col[1]/ion-checkbox",20)
        time.sleep(1)
        self.DoClickUntilNoException("/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-nav/app-policy-inquiry/ion-content/div/div/div[4]/div/app-datatable-pagination/div[2]/div[1]/ion-button")
        
        reportFullPath = self.reportPath+"policy_summary.zip"
        while exists(reportFullPath) == False:
            time.sleep(1)
        os.rename(reportFullPath,self.reportPath+policy+".zip")
        
        #unzip
        with zipfile.ZipFile(self.reportPath+policy+".zip", 'r') as zip_ref:
            zip_ref.extractall(self.reportPath)
        


    def __buildReportHeaderFullFlow(self):
        self.logger.writeLogString('GENERALI-HEADER','START BUILD HEADER FULLFLOW')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildHeaderQueue:
                self.logger.writeLogString('GENERALI-HEADER','POLICY NO.:{0}'.format(str(policy)))
                if self.isStopped:
                    return
                try:
                    
                    self.__formatBasicInfoHeader(policy,self.basicInfo_sheet,self.reportPath)
                    self.__formatCustomerInfoHeader(policy,self.customer_sheet,self.reportPath)
                    self.__formatPaymentHeader(policy,self.payment_sheet,self.reportPath)
                        
                    #No error when building the header,break all loop and then stop this thread
                    policy_iteration = self.maxPolicyListSize + 1
                    self.logger.writeLogString('GENERALI-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                    break
                except FileNotFoundError:
                    self.logger.writeLogString('GENERALI-HEADER','FILE NOT FOUND')
                except Exception as ex:
                    self.logger.writeLogString('GENERALI-HEADER','EXCEPTION:'+str(ex))
                finally:
                    policy_iteration = policy_iteration + 1
                    if policy in self.buildHeaderQueue:
                        self.buildHeaderQueue.remove(policy)
            else:
                time.sleep(1)

    def __buildReportHeaderHalfFlow(self):
        self.logger.writeLogString('GENERALI-HEADER','START BUILD HEADER HALFFLOW')
        for policy in self.policyList:
            self.logger.writeLogString('GENERALI-HEADER','POLICY NO.:{0}'.format(str(policy)))
            if self.isStopped:
                return
            try:
                self.__formatBasicInfoHeader(policy,self.basicInfo_sheet,self.inputPath)
                self.__formatCustomerInfoHeader(policy,self.customer_sheet,self.inputPath)
                self.__formatPaymentHeader(policy,self.payment_sheet,self.inputPath)                    
                #No error when building the header,break all loop and then stop this thread
                self.logger.writeLogString('GENERALI-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                break
            except FileNotFoundError as ex:
                self.logger.writeLogString('GENERALI-HEADER','FILE NOT FOUND')
            except Exception as ex:
                self.logger.writeLogString('GENERALI-HEADER','EXCEPTION:'+str(ex))

    def __buildReport(self):
        self.logger.writeLogString('GENERALI-CONTENT','START BUILD REPORT')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildReportQueue:
                if self.isStopped:
                    return
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),""))
                self.logger.writeLogString('GENERALI-CONTENT','POLICY NO.:{0}'.format(str(policy)))
                try:
                    self.basicInfo_sheet.write(policy_iteration+1,0,str(policy))
                    self.customer_sheet.write(policy_iteration+1,0,str(policy))
                    self.payment_sheet.write(policy_iteration+1,0,str(policy))

                    thread_basicInfo = threading.Thread(target = self.__formatBasicInfo, args=[policy_iteration,policy,self.basicInfo_sheet,self.reportPath])
                    thread_basicInfo.start()
                    
                    thread_customerInfo = threading.Thread(target = self.__formatCustomerInfo, args=[policy_iteration,policy,self.customer_sheet,self.reportPath])
                    thread_customerInfo.start()

                    thread_payment = threading.Thread(target = self.__formatPayment, args=[policy_iteration,policy,self.payment_sheet,self.reportPath])
                    thread_payment.start()
                    
                    pass
                except FileNotFoundError:
                    self.basicInfo_sheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                    self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"not found"))
                    self.logger.writeLogString('GENERALI-CONTENT','FILE NOT FOUND')
                    self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
                except Exception as ex:
                    self.basicInfo_sheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!"+str(ex))
                    self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"failed"))
                    self.logger.writeLogString('GENERALI-CONTENT','EXCEPTION:'+str(ex))
                    self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
                finally:
                    thread_basicInfo.join()
                    thread_customerInfo.join()
                    thread_payment.join()
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
        self.logger.writeLogString('GENERALI-CONTENT','COMPLETED BUILD REPORT')

    def __buildReportOnly(self):
        self.logger.writeLogString('GENERALI-CONTENT','START BUILD REPORT OFFLINE MODE')
        for policy_iteration,policy in enumerate(self.policyList):
            if self.isStopped:
                return
            self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),""))
            self.logger.writeLogString('GENERALI-CONTENT','POLICY NO.:{0}'.format(str(policy)))
            try:
                
                self.basicInfo_sheet.write(policy_iteration+1,0,str(policy))
                self.customer_sheet.write(policy_iteration+1,0,str(policy))
                self.payment_sheet.write(policy_iteration+1,0,str(policy))

                thread_basicInfo = threading.Thread(target = self.__formatBasicInfo, args=[policy_iteration,policy,self.basicInfo_sheet,self.inputPath])
                thread_basicInfo.start()
                
                thread_customerInfo = threading.Thread(target = self.__formatCustomerInfo, args=[policy_iteration,policy,self.customer_sheet,self.inputPath])
                thread_customerInfo.start()

                thread_payment = threading.Thread(target = self.__formatPayment, args=[policy_iteration,policy,self.payment_sheet,self.inputPath])
                thread_payment.start()
                pass
            except FileNotFoundError:
                self.basicInfo_sheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"not found"))
                self.logger.writeLogString('GENERALI-CONTENT','FILE NOT FOUND')
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            except Exception as ex:
                self.basicInfo_sheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!"+str(ex))
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"failed"))
                self.logger.writeLogString('GENERALI-CONTENT','EXCEPTION:'+str(ex))
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            finally:
                thread_basicInfo.join()
                thread_customerInfo.join()
                thread_payment.join()
                self.frame.setStatusProgresValueByValue(2)
                self.frame.setListItemColor(str(policy),self.STATUS_REPORT_COMPLETE)

        self.buildHeaderThread.join()
        self.workbook.close()
        self.frame.setStatusLableText(self.stringValue.completed.get())
        self.logger.writeLogString('GENERALI-CONTENT','COMPLETED BUILD REPORT OFFLINE MODE')
    
    def __formatBasicInfo(self,policy_iteration,policy,worksheet,path):
        file = open(path+policy+"_basic.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()    
        
        idx = 0
        soupBasic = basic.find('div',attrs={'id':'content'})
        
        for tag in soupBasic.find_all('div',attrs={'class':'policy-detail-content value'}):
            worksheet.write(policy_iteration+1, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1
        
        basic.find('div',attrs={'id':'content'}).decompose()
        basic.find('div',attrs={'id':'content'}).decompose()
        
        soupBasic = basic.find('div',attrs={'id':'content'})
        policyValue = []
        for iteration, tag in enumerate(soupBasic.find_all('div',attrs={'class':'policy-detail-content value'})):
            if iteration % 2 == 1:
                policyValue.append(tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                #worksheet.write(policy_iteration+1, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                #idx = idx + 1
                
        if len(policyValue) == 0:
            policyValue.append("N/A")
            policyValue.append("N/A")
            policyValue.append("N/A")
            policyValue.append("N/A")
            policyValue.append("N/A")
        elif len(policyValue) == 2:
            policyValue.insert(1,"終期紅利")
            policyValue.insert(2,"保障累積賬戶")
            policyValue.insert(3,"保費預存賬戶")
            basic.find('div',attrs={'id':'content'}).decompose()
            soupBasic = basic.find('div',attrs={'id':'content'})
        else:
            basic.find('div',attrs={'id':'content'}).decompose()
            soupBasic = basic.find('div',attrs={'id':'content'})
        
        for value in policyValue:
            worksheet.write(policy_iteration+1, idx+1, value)
            idx = idx + 1

        for tag in soupBasic.find_all('ion-label',attrs={'class':'sc-ion-label-ios-h sc-ion-label-ios-s ios hydrated'}):
            worksheet.write(policy_iteration+1, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1

        pass
    
    def __formatBasicInfoHeader(self,policy,worksheet,path):
        file = open(path+policy+"_basic.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()
        
        idx = 0
        soupBasic = basic.find('div',attrs={'id':'content'})
        
        for tag in soupBasic.find_all('div',attrs={'class':'policy-detail-content label'}):
            worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1
            
        basic.find('div',attrs={'id':'content'}).decompose()
        basic.find('div',attrs={'id':'content'}).decompose()
        
        soupBasic = basic.find('div',attrs={'id':'content'})
        policyValue = []
        for iteration, tag in enumerate(soupBasic.find_all('div',attrs={'class':'policy-detail-content value'})):
            if iteration % 2 == 0:
                policyValue.append(tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                #worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                #idx = idx + 1
                
        
        if len(policyValue) == 0:
            policyValue.append("保證現金價值")
            policyValue.append("終期紅利")
            policyValue.append("保障累積賬戶")
            policyValue.append("保費預存賬戶")
            policyValue.append("保單貸款")
        elif len(policyValue) == 2:
            policyValue.insert(1,"終期紅利")
            policyValue.insert(2,"保障累積賬戶")
            policyValue.insert(3,"保費預存賬戶")
            basic.find('div',attrs={'id':'content'}).decompose()
            soupBasic = basic.find('div',attrs={'id':'content'})  
        else:
            basic.find('div',attrs={'id':'content'}).decompose()
            soupBasic = basic.find('div',attrs={'id':'content'})
                  
        for header in policyValue:
            worksheet.write(0, idx+1, header)
            idx = idx + 1

        
        for tag in soupBasic.find_all('ion-label',attrs={'class':'label sc-ion-label-ios-h sc-ion-label-ios-s ios hydrated'}):
            worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1
        
        
        pass
    
    def __formatCustomerInfo(self,policy_iteration,policy,worksheet,path):
        file = open(path+policy+"_customer.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()

        content = ['']
        soupBasic = basic.find('div',attrs={'id':'content'})
        
        for tag in soupBasic.find_all('div',attrs={'class':'client-info-content value'}):
            content.append(tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        
        if len(content) == 13:
            content.insert(8,'')
        elif len(content) == 12:
            content.insert(7,'')
            content.insert(8,'')
        
        basic.find('div',attrs={'id':'content'}).decompose()
        
        content.append('')
        soupBasic = basic.find('div',attrs={'id':'content'})
                
        for tag in soupBasic.find_all('div',attrs={'class':'client-info-content value'}):
            content.append(tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            
        basic.find('div',attrs={'id':'content'}).decompose()
        soupBasic = basic.find('div',attrs={'id':'content'})
        row = soupBasic.find_all('ion-row',attrs={'class':'body ios hydrated'})
        soup_row = BeautifulSoup(str(row),'lxml')
        for tag in soup_row.find_all('ion-label',attrs={'class':'sc-ion-label-ios-h sc-ion-label-ios-s ios hydrated'}):
            content.append(tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            
        for iteration,value in enumerate(content):
            worksheet.write(policy_iteration+1, iteration+1,value)
        
        pass
    
    def __formatCustomerInfoHeader(self,policy,worksheet,path):
        file = open(path+policy+"_customer.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()
        
        idx = 0
        soupBasic = basic.find('div',attrs={'id':'container'})
        
        for tag in soupBasic.find_all('ion-label',attrs={'class':'sc-ion-label-ios-h sc-ion-label-ios-s ios hydrated'}):
            worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1
        
        for iteration,tag in enumerate(soupBasic.find_all('div',attrs={'class':'client-info-content label'})):
            worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1
            if iteration == 3:
                worksheet.write(0, idx+1, "")
                idx = idx + 1
                worksheet.write(0, idx+1, "")
                idx = idx + 1
                worksheet.write(0, idx+1, "")
                idx = idx + 1
                worksheet.write(0, idx+1, "")
                idx = idx + 1
                        
        basic.find('div',attrs={'id':'container'}).decompose()
        
        soupBasic = basic.find('div',attrs={'id':'container'})
        
        for tag in soupBasic.find_all('ion-label',attrs={'class':'sc-ion-label-ios-h sc-ion-label-ios-s ios hydrated'}):
            worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1
        
        for iteration,tag in enumerate(soupBasic.find_all('div',attrs={'class':'client-info-content label'})):
            worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1
        
        basic.find('div',attrs={'id':'container'}).decompose()
        
        soupBasic = basic.find('div',attrs={'id':'container'})
        benifitHeader = soupBasic.find('ion-row',attrs={'class':'header ios hydrated'})
        for tag in benifitHeader.find_all('ion-label',attrs={'class':'label sc-ion-label-ios-h sc-ion-label-ios-s ios hydrated'}):
            worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1
            
        pass
    
    def __formatPayment(self,policy_iteration,policy,worksheet,path):
        file = open(path+policy+"_payment.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()  

        idx = 0
        soupBasic = basic.find('div',attrs={'id':'content'})
        
        for tag in soupBasic.find_all('div',attrs={'class':'payment-info-content value'}):
            worksheet.write(policy_iteration+1, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1
 
        pass
    def __formatPaymentHeader(self,policy,worksheet,path):
        file = open(path+policy+"_payment.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close() 
        
        idx = 0
        soupBasic = basic.find('div',attrs={'id':'content'})
        
        for tag in soupBasic.find_all('div',attrs={'class':'payment-info-content label'}):
            worksheet.write(0, idx+1, tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1
  
        pass
