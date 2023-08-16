from genericpath import exists
import time
from bs4 import BeautifulSoup
from ipra.Model.Robot.baseRobot import BaseRobot
from selenium.webdriver.common.by import By
import xlsxwriter
import threading

class AiaRobot(BaseRobot):
    def __init__(self, policyList, frame, reportPath,inputPath,downloadReport):
        super().__init__(policyList, frame, reportPath,inputPath,downloadReport)

        self.logger.writeLogString('AIA-INIT','ROBOT INIT')

        self.maxPolicyListSize = len(policyList)
        self.workbook = xlsxwriter.Workbook(self.reportPath+'AIA_report.xlsx')

        self.basicInfo_sheet = self.workbook.add_worksheet(name="General Information")
        self.basicInfo_sheet.write(0, 0, "Policy No.")

        self.scope_sheet = self.workbook.add_worksheet(name="Coverage Information")
        self.scope_sheet.write(0, 0, "Policy No.")

        self.value_sheet = self.workbook.add_worksheet(name="FinancialValue GeneralQuotation")
        self.value_sheet.write(0, 0, "Policy No.")

        self.value_payment = self.workbook.add_worksheet(name="Payment Information")
        self.value_payment.write(0, 0, "Policy No.")

        self.logger.writeLogString('AIA-INIT','maxPolicyListSize:'+str(self.maxPolicyListSize))


    def waitingLoginComplete(self):
        self.frame.setStatusLableText(self.stringValue.waitingLogin.get())
        self.logger.writeLogString('AIA-LOGIN','START LOGIN')
        self.browser.get("https://www3.aia.com.hk/ebusiness/login.do")

        while not self.isLogin and not self.isStopped:
            try:
                self.browser.find_element(By.XPATH, "/html/body/div[1]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/ul/li[2]/a").click()
                time.sleep(1)
                self.isLogin=True
            except Exception as ex:
                time.sleep(3)
        else:
            pass

        if self.isLogin:
            self.frame.setStatusLableText(self.stringValue.loginSuccess.get())
            self.logger.writeLogString('AIA-LOGIN','LOGIN COMPLETED')
        
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])

    def scrapPolicy(self):
        for policy in self.policyList:
            if self.isStopped:
                return
            try:
                self.frame.setStatusLableText(self.stringValue.processing.get().format(str(policy)))
                self.logger.writeLogString('AIA','PROCESSING:'+str(policy))

                input = self.browser.find_element(By.XPATH, "/html/body/table/tbody/tr[3]/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[2]/input")
                input.clear()
                input.send_keys(str(policy))
                self.browser.find_element(By.XPATH,"/html/body/table/tbody/tr[3]/td[2]/table/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/table[1]/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[1]/td/table/tbody/tr/td[4]/input").click()
                self.browser.find_element(By.LINK_TEXT,str(policy)).click()

                time.sleep(5)
                self.browser.switch_to.frame("polFrm")
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                file1 = open(str(self.reportPath+policy)+"_basic"+".txt","a",encoding="utf-8")#append mode 
                file1.write(soup.prettify()) 
                file1.close()
                
                #Download Report execute here
                try:
                    self.downloadPolicyReport(str(policy))
                except:
                    pass

                try:
                    self.browser.find_element(By.XPATH,"/html/body/div[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[1]/table/tbody/tr/td[2]/table/tbody/tr/td[2]").click()
                except:
                    self.browser.find_element(By.XPATH,"/html/body/div[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[1]/table[1]/tbody/tr/td[2]/table/tbody/tr/td[2]").click()

                time.sleep(5)

                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                file1 = open(str(self.reportPath+policy)+"_scope"+".txt","a",encoding="utf-8")#append mode 
                file1.write(soup.prettify()) 
                file1.close()

                try:
                    value = self.browser.find_element(By.XPATH,"/html/body/div[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[1]/table/tbody/tr/td[3]/table/tbody/tr/td[2]").click()
                except:
                    value = self.browser.find_element(By.XPATH,"/html/body/div[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[1]/table[1]/tbody/tr/td[3]/table/tbody/tr/td[2]").click()

                time.sleep(5)
                self.browser.find_element(By.XPATH,"/html/body/div[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[3]/form/table/tbody/tr[4]/td/table/tbody/tr[5]/td[2]/input").click()
                time.sleep(5)

                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                file1 = open(str(self.reportPath+policy)+"_value"+".txt","a",encoding="utf-8")#append mode 
                file1.write(soup.prettify()) 
                file1.close()
                try:
                    payment = self.browser.find_element(By.XPATH,"/html/body/div[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[1]/table/tbody/tr/td[4]/table/tbody/tr/td[2]").click()
                except:
                    payment = self.browser.find_element(By.XPATH,"/html/body/div[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[1]/table[1]/tbody/tr/td[4]/table/tbody/tr/td[2]").click()

                time.sleep(5)
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                file1 = open(str(self.reportPath+policy)+"_payment"+".txt","a",encoding="utf-8")#append mode 
                file1.write(soup.prettify()) 
                file1.close()

                #self.browser.switch_to.default_content()
            except Exception as ex:
                self.logger.writeLogString('AIA',str(policy)+" throws Exception")
                self.frame.setStatusLableText(self.stringValue.processException.get().format(str(policy),str(ex)))
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            finally:
                self.frame.setStatusLableText(self.stringValue.processCompleted.get().format(str(policy)))
                self.logger.writeLogString('AIA',str(policy)+" COMPLETED")
                self.frame.setStatusProgresValueByValue(1)
                self.browser.switch_to.default_content()
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
        
        try:
            self.browser.find_element(By.XPATH,"/html/body/div[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div[3]/table/tbody/tr[1]/td/form/table/tbody/tr/td/table[1]/tbody/tr/td[6]/a/img").click()
        except:
            self.browser.find_element(By.XPATH,"/html/body/div[2]/table/tbody/tr/td/table/tbody/tr/td/div[2]/table/tbody/tr[1]/td/form/table/tbody/tr/td/table[1]/tbody/tr/td[6]/a/img").click()
                      
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser.find_element(By.XPATH,"/html/body/table[2]/tbody/tr/td[2]/a/img").click()
        
        #Selenium no build-in check download complete listerner, check by file exist in path
        reportFullPath = self.reportPath+"Policy_Details_{0}.pdf".format(policy)
        while exists(reportFullPath) == False:
            time.sleep(1)
        
        self.browser.switch_to.window(self.browser.window_handles[2])
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.switch_to.frame("polFrm")

    def __buildReportHeaderFullFlow(self):
        self.logger.writeLogString('AIA-HEADER','START BUILD HEADER FULLFLOW')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildHeaderQueue:
                self.logger.writeLogString('AIA-HEADER','POLICY NO.:{0}'.format(str(policy)))
                if self.isStopped:
                    return
                try:

                    self.__formatBasicInfoHeader(policy,self.basicInfo_sheet,self.reportPath)
                    self.__formatScopeInfoHeader(policy,self.scope_sheet,self.reportPath)
                    self.__formatValueHeader(policy,self.value_sheet,self.reportPath)
                    self.__formatPaymentHeader(policy,self.value_payment,self.reportPath)
                        
                    #No error when building the header,break all loop and then stop this thread
                    policy_iteration = self.maxPolicyListSize + 1
                    self.logger.writeLogString('AIA-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                    break
                except FileNotFoundError:
                    self.logger.writeLogString('AIA-HEADER','FILE NOT FOUND')
                except Exception as ex:
                    self.logger.writeLogString('AIA-HEADER','EXCEPTION:'+str(ex))
                finally:
                    policy_iteration = policy_iteration + 1
                    if policy in self.buildHeaderQueue:
                        self.buildHeaderQueue.remove(policy)
            else:
                time.sleep(1)

    def __buildReportHeaderHalfFlow(self):
        self.logger.writeLogString('AIA-HEADER','START BUILD HEADER HALFFLOW')
        for policy in self.policyList:
            self.logger.writeLogString('AIA-HEADER','POLICY NO.:{0}'.format(str(policy)))
            if self.isStopped:
                return
            try:

                self.__formatBasicInfoHeader(policy,self.basicInfo_sheet,self.inputPath)
                self.__formatScopeInfoHeader(policy,self.scope_sheet,self.inputPath)
                self.__formatValueHeader(policy,self.value_sheet,self.inputPath)
                self.__formatPaymentHeader(policy,self.value_payment,self.inputPath)
                    
                #No error when building the header,break all loop and then stop this thread
                self.logger.writeLogString('AIA-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                break
            except FileNotFoundError as ex:
                self.logger.writeLogString('AIA-HEADER','FILE NOT FOUND')
            except Exception as ex:
                self.logger.writeLogString('AIA-HEADER','EXCEPTION:'+str(ex))

    def __buildReport(self):
        self.logger.writeLogString('AIA-CONTENT','START BUILD REPORT')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildReportQueue:
                if self.isStopped:
                    return
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),""))
                self.logger.writeLogString('AIA-CONTENT','POLICY NO.:{0}'.format(str(policy)))
                try:
                    self.basicInfo_sheet.write(policy_iteration+1,0,str(policy))
                    self.scope_sheet.write(policy_iteration+1,0,str(policy))
                    self.value_sheet.write(policy_iteration+1,0,str(policy))
                    self.value_payment.write(policy_iteration+1,0,str(policy))

                    thread_basicInfo = threading.Thread(target = self.__formatBasicInfo, args=[policy_iteration,policy,self.basicInfo_sheet,self.reportPath])
                    thread_basicInfo.start()

                    thread_scopeInfo = threading.Thread(target = self.__formatScopeInfo, args=[policy_iteration,policy,self.scope_sheet,self.reportPath])
                    thread_scopeInfo.start()

                    thread_value = threading.Thread(target = self.__formatValue, args=[policy_iteration,policy,self.value_sheet,self.reportPath])
                    thread_value.start()

                    thread_payment = threading.Thread(target = self.__formatPayment, args=[policy_iteration,policy,self.value_payment,self.reportPath])
                    thread_payment.start()

                except FileNotFoundError:
                    self.basicInfo_sheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                    self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"not found"))
                    self.logger.writeLogString('AIA-CONTENT','FILE NOT FOUND')
                    self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
                except Exception as ex:
                    self.basicInfo_sheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!"+str(ex))
                    self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"failed"))
                    self.logger.writeLogString('AIA-CONTENT','EXCEPTION:'+str(ex))
                    self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
                finally:
                    thread_basicInfo.join()
                    thread_scopeInfo.join()
                    thread_value.join()
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
        self.logger.writeLogString('AIA-CONTENT','COMPLETED BUILD REPORT')

    def __buildReportOnly(self):
        self.logger.writeLogString('AIA-CONTENT','START BUILD REPORT OFFLINE MODE')
        for policy_iteration,policy in enumerate(self.policyList):
            if self.isStopped:
                return
            self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),""))
            self.logger.writeLogString('AIA-CONTENT','POLICY NO.:{0}'.format(str(policy)))
            try:
                self.basicInfo_sheet.write(policy_iteration+1,0,str(policy))
                self.scope_sheet.write(policy_iteration+1,0,str(policy))
                self.value_sheet.write(policy_iteration+1,0,str(policy))
                self.value_payment.write(policy_iteration+1,0,str(policy))

                thread_basicInfo = threading.Thread(target = self.__formatBasicInfo, args=[policy_iteration,policy,self.basicInfo_sheet,self.inputPath])
                thread_basicInfo.start()

                thread_scopeInfo = threading.Thread(target = self.__formatScopeInfo, args=[policy_iteration,policy,self.scope_sheet,self.inputPath])
                thread_scopeInfo.start()

                thread_value = threading.Thread(target = self.__formatValue, args=[policy_iteration,policy,self.value_sheet,self.inputPath])
                thread_value.start()

                thread_payment = threading.Thread(target = self.__formatPayment, args=[policy_iteration,policy,self.value_payment,self.inputPath])
                thread_payment.start()

            except FileNotFoundError:
                self.basicInfo_sheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"not found"))
                self.logger.writeLogString('AIA-CONTENT','FILE NOT FOUND')
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            except Exception as ex:
                self.basicInfo_sheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!"+str(ex))
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"failed"))
                self.logger.writeLogString('AIA-CONTENT','EXCEPTION:'+str(ex))
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            finally:
                thread_basicInfo.join()
                thread_scopeInfo.join()
                thread_value.join()
                thread_payment.join()
                self.frame.setStatusProgresValueByValue(2)
                self.frame.setListItemColor(str(policy),self.STATUS_REPORT_COMPLETE)

        self.buildHeaderThread.join()
        self.workbook.close()
        self.frame.setStatusLableText(self.stringValue.completed.get())
        self.logger.writeLogString('AIA-CONTENT','COMPLETED BUILD REPORT OFFLINE MODE')

    def __formatPayment(self,policy_iteration,policy,worksheet,path):
        file = open(path+policy+"_payment.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()

        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','loadTable')
        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','type1')
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()

        row_value = []

        soup_payment = soup_basic.find('tbody').find('tbody')
        try:
            soup_payment.find('b').decompose()
            soup_payment.find('b').decompose()
            soup_payment.find('b').decompose()
            soup_payment.find('b').decompose()
            for strong_tag in soup_payment.find_all('td'):
                value = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                if value != '':
                    row_value.append(value)
        except:
            row_value.append("N/A")
            row_value.append("N/A")
            row_value.append("N/A")
            row_value.append("N/A")

        
        for col_num, data in enumerate(row_value):
            worksheet.write(policy_iteration+1, col_num+1, data)

        try:
            soup_basic.find('tr').decompose()
            soup_basic.find('tr').decompose()
            soup_basic.find('tr').decompose()
            soup_charge = soup_basic.find('tbody').find('tbody')
        except:
            soup_basic.find('tr').decompose()
            soup_charge = soup_basic.find('tbody').find('tbody')

        soup_charge.find('tr').decompose()
        soup_charge.find('tr', attrs={'style':'display:none'}).decompose()

        soup_temp = BeautifulSoup(str(soup_charge.find_all('tr')), 'lxml')

        row_value2 = []

        for strong_tag in soup_temp.find_all('td'):
            row_value2.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))

        for col_num, data in enumerate(row_value2):
            worksheet.write(policy_iteration+1, len(row_value)+1+col_num, data)

        return

    def __formatPaymentHeader(self,policy,worksheet,path):
        file = open(path+policy+"_payment.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()

        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','loadTable')
        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','type1')
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_payment = soup_basic.find('tbody').find('tbody')

        row_header = []
        for strong_tag in soup_payment.find_all('b'):
            header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
            if(header != ''):
                row_header.append(header)
        idx = 1
        for data in row_header:
            worksheet.write(0, idx, data)
            idx = idx + 1 

        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()

        soup_charge = soup_basic.find('tbody').find('tbody')
        soup_header = self.SearchByHtmlTagValueKey(soup_charge,'tr','class','tableHeaderWithBorder')
        soup_charge.find('tr').decompose()
        soup_charge.find('tr', attrs={'style':'display:none'}).decompose()

        list_white = soup_charge.find_all('tr',attrs={'class':'bgWhiteColor'})
        num_of_plan = len(list_white)


        row_header2 = []
        for strong_tag in soup_header.find_all('td'):
            row_header2.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))

        row_header2 = row_header2 * (num_of_plan)

        for data in row_header2:
            worksheet.write(0, idx, data)
            idx = idx + 1
        return

    def __formatValue(self,policy_iteration,policy,worksheet,path):
        file = open(path+policy+"_value.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()

        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','loadTable')
        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','type1')
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_value = soup_basic.find('tr').find('tbody').find('tbody')

        soup_value.find('tr').decompose()
        soup_temp = BeautifulSoup(str(soup_value.find_all('tr')), 'lxml')
        row_value = []

        for strong_tag in soup_temp.find_all('td'):
            row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        
        policyValueRow = row_value[0:len(row_value)-4] 
        policyValueTotalRow = row_value[len(row_value)-4:]   
        dummy = ['','','','','','','']
        
        pendingInsert = policyValueRow + dummy * (6 - int(len(policyValueRow) /7))
        pendingInsert = pendingInsert + policyValueTotalRow
        row_value = pendingInsert
        
        for col_num, data in enumerate(pendingInsert):
            worksheet.write(policy_iteration+1, col_num+1, data)

        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        try:
            soup_basic.find('tr').find('tbody').find('tbody')
        except:
            soup_basic.find('tr').decompose()
        soup_borrow = soup_basic.find('tr').find('tbody').find('tbody')

        soup_borrow.find('tr').decompose()
        soup_temp = BeautifulSoup(str(soup_borrow.find_all('tr')), 'lxml')
        row_value2 = []

        for strong_tag in soup_temp.find_all('td'):
            row_value2.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        
        if len(row_value2) == 2:
            row_value2.append('')

        for col_num, data in enumerate(row_value2):
            worksheet.write(policy_iteration+1,  len(row_value)+1+col_num, data)


        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        try:
            soup_basic.find('tr').find('tbody').find('tbody')
        except:
            soup_basic.find('tr').decompose()
            soup_basic.find('tr').decompose()
        soup_fee = soup_basic.find('tr').find('tbody').find('tbody')

        soup_fee.find('tr').decompose()
        soup_temp = BeautifulSoup(str(soup_fee.find_all('tr')), 'lxml')
        row_value3 = []
        
        for strong_tag in soup_temp.find_all('td'):
            if strong_tag.text.strip() != "":
                row_value3.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))

        for col_num, data in enumerate(row_value3):
            worksheet.write(policy_iteration+1,  len(row_value+row_value2)+1+col_num, data)

    def __formatValueHeader(self,policy,worksheet,path):
        file = open(path+policy+"_value.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()

        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','loadTable')
        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','type1')
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_value = soup_basic.find('tr').find('tbody').find('tbody')

        soup_header = self.SearchByHtmlTagValueKey(soup_value,'tr','class','tableHeaderWithBorder')
        soup_value.find('tr').decompose()
        row_header = []

        for strong_tag in soup_header.find_all('td'):
            row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            
        #current found max 6 row
        row_header = row_header * 6
        for col_num, data in enumerate(row_header):
            worksheet.write(0, col_num+1, data)

        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        try:
            soup_basic.find('tr').find('tbody').find('tbody')
        except:
            soup_basic.find('tr').decompose()
        soup_borrow = soup_basic.find('tr').find('tbody').find('tbody')

        soup_header = self.SearchByHtmlTagValueKey(soup_borrow,'tr','class','tableHeaderWithBorder')

        soup_borrow.find('tr').decompose()
        row_header2 = []

        for strong_tag in soup_header.find_all('td'):
            row_header2.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))

        for col_num, data in enumerate(row_header2):
            worksheet.write(0, len(row_header2)+1+col_num, data)

        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        try:
            soup_basic.find('tr').find('tbody').find('tbody')
        except:
            soup_basic.find('tr').decompose()
            soup_basic.find('tr').decompose()
        soup_fee = soup_basic.find('tr').find('tbody').find('tbody')

        soup_fee.find('tr').decompose()
        
    def __formatScopeInfo(self,policy_iteration,policy,worksheet,path):
        file = open(path+policy+"_scope.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()

        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','loadTable')
        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','type1')
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_scope = soup_basic.find('tr').find('tbody').find('tbody')

        list_white = soup_scope.find_all('tr',attrs={'class':'bgWhiteColor'})
        list_gray = soup_scope.find_all('tr',attrs={'class':'bgGrayColor'})
        list_total = list_white + list_gray
        soup_plan = BeautifulSoup(str(list_total), 'lxml')
        
        #soup_total_header = SearchByTagValue(soup_scope,'tr','class','tableLeftTopGrayBorder')
        #soup_total_value = SearchByTagValue(soup_scope,'td','id','totalPrem')
        soup_total_header = soup_scope('tr',attrs={'class':'tableLeftTopGrayBorder'})
        soup_total_value = soup_scope('td',attrs={'id':'totalPrem'})
        
        dummy = ['','','','','','','','','']
        row_value = []
        for strong_tag in soup_plan.find_all('td'):
            row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ').replace(' ',''))
        
        pendingInsert = 4 - int(len(row_value) / 9)
        row_value = row_value + dummy*pendingInsert
        
        row_temp_value = []
        for strong_tag in BeautifulSoup(str(soup_total_value), 'lxml').find_all('b'):
            row_temp_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        
        if(len(row_temp_value) < 4):
            row_temp_value.insert(1,"")

        row_value = row_value + row_temp_value

        for col_num, data in enumerate(row_value):
            worksheet.write(policy_iteration+1, col_num+1, data)

    def __formatScopeInfoHeader(self,policy,worksheet,path):
        file = open(path+policy+"_scope.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()

        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','loadTable')
        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','type1')
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_scope = soup_basic.find('tr').find('tbody').find('tbody')

        soup_header = self.SearchByHtmlTagValueKey(soup_scope,'tr','class','tableHeaderWithBorder')
        #list_white = soup_scope.find_all('tr',attrs={'class':'bgWhiteColor'})
        #list_gray = soup_scope.find_all('tr',attrs={'class':'bgGrayColor'})
        #list_total = list_white + list_gray
        num_of_plan = 4
        
        #soup_total_header = SearchByTagValue(soup_scope,'tr','class','tableLeftTopGrayBorder')
        #soup_total_value = SearchByTagValue(soup_scope,'td','id','totalPrem')
        soup_total_header = soup_scope('tr',attrs={'class':'tableLeftTopGrayBorder'})

        row_header = []
        for strong_tag in soup_header.find_all('td'):
            row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        row_header = row_header * num_of_plan

        row_temp_header = []
        for idx,strong_tag in enumerate(BeautifulSoup(str(soup_total_header), 'lxml').find_all('td')):
            if idx % 2 == 0:
                row_temp_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        
        if(len(row_temp_header) < 4):
            row_temp_header.insert(1,"")
        row_header = row_header +row_temp_header

        for col_num, data in enumerate(row_header):
            worksheet.write(0, col_num+1, data)

    def __formatBasicInfo(self,policy_iteration,policy,worksheet,path):
        file = open(path+policy+"_basic.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()

        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','loadTable')
        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','type1')
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()

        soup_basic_info = soup_basic.find('tr').find('td')
        soup_basic_info_left = soup_basic_info.find('td')
        soup_basic_info_right = soup_basic_info.find('td').find_next_sibling("td")
        soup_basic_info_left = soup_basic_info_left.find('tbody')
        soup_basic_info_right = soup_basic_info_right.find('tbody')

        row_value = []
        for strong_tag in soup_basic_info_left.find_all('tr'):
            strong_tag.find('td').decompose()
            row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        for strong_tag in soup_basic_info_right.find_all('tr'):
            if strong_tag.has_attr('style'):
                continue
            strong_tag.find('td').decompose()
            row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        
        if len(row_value) <= 19:
            row_value.append('N/A')
            row_value.append('N/A')
            row_value.append('N/A')
            row_value.append('N/A')

        elif len(row_value) <=21:
            if row_value[19] == '是' or row_value[19] == '否' or row_value[19] == 'Yes' or row_value[19] == 'No':
                row_value.insert(19,'N/A')
                row_value.insert(20,'N/A')
            else:
                row_value.append('N/A')
                row_value.append('N/A')

        
        soup_basic.find('tr').decompose()

        while True:
            try:
                soup_basic_next_info = soup_basic.find('tr')
                if soup_basic_next_info.has_attr('style') and soup_basic_next_info['style'] == 'display:none':
                    soup_basic.find('tr').decompose()
                else:
                    soup_basic_next_info = soup_basic.find('tr').find('tbody').find('tbody')
                    break
            except:
                soup_basic.find('tr').decompose()

        soup_basic_next_data = soup_basic_next_info.find_all('tr')
        soup_basic_next_data.pop(0)
        soup_basic_next_data.pop()
        soup_basic_next_data = BeautifulSoup(str(soup_basic_next_data), 'lxml')

        max_supported = 20
        nextAmount = []
        for strong_tag in soup_basic_next_data.find_all('b'):
            max_supported -= 1
            temp_value = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
            idx = temp_value.find("(")
            if idx > 0:#there is a ()
                brinket = temp_value[idx:]
                idx_e = brinket.find("HK$")
                idx_c = brinket.find("港元")
                if idx_e>0 or idx_c >0:
                    temp_value = temp_value[0:idx]
                
                nextAmount.append(temp_value)

            else:
                nextAmount.append(temp_value)

        if any( ('下期保費' in nextAmountValue or 'Next Modal Premium' in nextAmountValue) for nextAmountValue in nextAmount):
            nextAmount += [''] * max_supported
            for value in nextAmount:
                row_value.append(value)
            
            soup_basic.find('tr').decompose()
            
        else:
            row_value += [''] * 20     
                   

        while True:
            try:
                soup_basic_insuered_info = soup_basic.find('tr')
                if soup_basic_insuered_info.has_attr('style') and soup_basic_insuered_info['style'] == 'display:none':
                    soup_basic.find('tr').decompose()
                else:
                    soup_basic_insuered_info = soup_basic.find('tr').find('tbody').find('tbody')
                    break
            except:
                soup_basic.find('tr').decompose()

        for strong_tag in soup_basic_insuered_info.find_all('tr'):
            try:
                strong_tag.find('td').decompose()
                row_value.append(strong_tag.find('td').text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                strong_tag.find('td').decompose()
                strong_tag.find('td').decompose()
                strong_tag.find('td').decompose()
                row_value.append(strong_tag.find('td').text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            except:
                continue
        
        soup_basic.find('tr').decompose()
        
        while True:
            try:
                soup_basic_insuered_info = soup_basic.find('tr')
                if soup_basic_insuered_info.has_attr('style') and soup_basic_insuered_info['style'] == 'display:none':
                    soup_basic.find('tr').decompose()
                else:
                    soup_basic_insuered_info = soup_basic.find('tr').find('tbody').find('tbody')
                    
                    #speical handling for 1 box
                    if soup_basic_insuered_info.find('td').has_attr('width') and (soup_basic_insuered_info.find('td')['width'] == '100%' or soup_basic_insuered_info.find('td')['width'] == '33%'):
                        soup_basic.find('tr').decompose()
                    else:
                        break

            except:
                soup_basic.find('tr').decompose()


        for strong_tag in soup_basic_insuered_info.find_all('tr'):
            try:
                strong_tag.find('td').decompose()
                row_value.append(strong_tag.find('td').text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                strong_tag.find('td').decompose()
                strong_tag.find('td').decompose()
                strong_tag.find('td').decompose()
                if strong_tag.find('td').text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ') == '':
                    continue
                else:
                    row_value.append(strong_tag.find('td').text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            except:
                continue

        soup_basic.find('tr').decompose()
  
        while True:
            try:
                soup_basic_benefit = soup_basic.find('tr')
                if soup_basic_benefit.has_attr('style') and soup_basic_benefit['style'] == 'display:none':
                    soup_basic.find('tr').decompose()
                else:
                    soup_basic_benefit = soup_basic.find('tr').find('tbody').find('tbody')
                    
                    #speical handling for 1 box
                    if soup_basic_benefit.find('td').has_attr('width') and (soup_basic_benefit.find('td')['width'] == '100%' or soup_basic_benefit.find('td')['width'] == '33%'):
                        soup_basic.find('tr').decompose()
                    else:
                        break
            except:
                soup_basic.find('tr').decompose()



        for iteration,strong_tag in enumerate(soup_basic_benefit.find_all('tr')):
            try:
                try:
                    if iteration == 0:
                        continue
                    row_value.append(strong_tag.find('td').text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    strong_tag.find('td').decompose()
                    row_value.append(strong_tag.find('td').text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    strong_tag.find('td').decompose()
                    row_value.append(strong_tag.find('td').text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    strong_tag.find('td').decompose()
                except:
                    break
            except:
                continue

        soup_basic.find('tr').decompose()

        while True:
            try:
                soup_basic_benefit = soup_basic.find('tr')
                if soup_basic_benefit.has_attr('style') and soup_basic_benefit['style'] == 'display:none':
                    soup_basic.find('tr').decompose()
                else:
                    soup_basic_benefit = soup_basic.find('tr').find('tbody').find('tbody')
                    
                    #speical handling for 1 box
                    if soup_basic_benefit.find('td').has_attr('width') and (soup_basic_benefit.find('td')['width'] == '100%' or soup_basic_benefit.find('td')['width'] == '33%'):
                        soup_basic.find('tr').decompose()
                    else:
                        break
            except:
                if soup_basic.find('tr') != None:
                    soup_basic.find('tr').decompose()
                else:
                    break
                
        max_supported = 12
        if soup_basic_benefit != None:
            for index,strong_tag in enumerate(soup_basic_benefit.find_all('tr')):
                try:
                    if index == 0:
                        continue
                    max_supported -= 1
                    row_value.append(strong_tag.find('td').text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    strong_tag.find('td').decompose()
                    row_value.append(strong_tag.find('td').text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    strong_tag.find('td').decompose()
                    row_value.append(strong_tag.find('td').text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
                    strong_tag.find('td').decompose()
                except:
                    break

        row_value += [''] * max_supported

        for col_num, data in enumerate(row_value):
            worksheet.write(policy_iteration+1, col_num+1, data)

    def __formatBasicInfoHeader(self,policy,worksheet,path):
        file = open(path+policy+"_basic.txt",encoding="utf-8")#append mode 
        #Full Html src
        basic = BeautifulSoup(file.read(), 'lxml')
        file.close()

        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','loadTable')
        soup_basic = self.SearchByHtmlTagValueKey(basic,'div','id','type1')
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()
        soup_basic.find('tr').decompose()

        soup_basic_info = soup_basic.find('tr').find('td')
        soup_basic_info_left = soup_basic_info.find('td')
        soup_basic_info_right = soup_basic_info.find('td').find_next_sibling("td")
        soup_basic_info_left = soup_basic_info_left.find('tbody')
        soup_basic_info_right = soup_basic_info_right.find('tbody')

        idx = 0
        for strong_tag in soup_basic_info_left.find_all('b'):
            worksheet.write(0, idx+1, strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1
        
        bufferToInsert = []
        for iteration,strong_tag in enumerate(soup_basic_info_right.find_all('tr')):
            if strong_tag.has_attr('style') and strong_tag['style'] == 'display:none':
                continue
            strong_tag = strong_tag.find('b')
            content = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
            if iteration >= 11:
                bufferToInsert.append((idx,content))
                pass
            else:
                worksheet.write(0, idx+1, content)
            idx = idx + 1
        
        if len(bufferToInsert)>=4:
            for x in range(0,len(bufferToInsert)):
                worksheet.write(0,bufferToInsert[x][0]+1,bufferToInsert[x][1])
        else:#expect len == 2 only
            if bufferToInsert[0][1] == '保費回贈餘額保費:' and bufferToInsert[1][1] == '保費回贈日期:':
                worksheet.write(0,bufferToInsert[0][0]+1,bufferToInsert[0][1])
                worksheet.write(0,bufferToInsert[1][0]+1,bufferToInsert[1][1])
                worksheet.write(0,bufferToInsert[1][0]+2,'自動扣除保費徵費選擇:')
                worksheet.write(0,bufferToInsert[1][0]+3,'接收逾期保費徵費通知選擇:')            
            else:
                worksheet.write(0,bufferToInsert[0][0]+1,"保費回贈餘額保費:")
                worksheet.write(0,bufferToInsert[1][0]+1,"保費回贈日期:")
                worksheet.write(0,bufferToInsert[1][0]+2,bufferToInsert[0][1])
                worksheet.write(0,bufferToInsert[1][0]+3,bufferToInsert[1][1])
            idx = idx + 2

        idx = idx + 20
        
        soup_basic.find('tr').decompose()
 
        while True:
            try:
                soup_basic_insuered_info = soup_basic.find('tr')
                if soup_basic_insuered_info.has_attr('style') and soup_basic_insuered_info['style'] == 'display:none':
                    soup_basic.find('tr').decompose()
                else:
                    soup_basic_insuered_info = soup_basic.find('tr').find('tbody').find('tbody')
                    break
            except:
                soup_basic.find('tr').decompose()

        soup_basic.find('tr').decompose()

        while True:
            try:
                soup_basic_insuered_info = soup_basic.find('tr')
                if soup_basic_insuered_info.has_attr('style') and soup_basic_insuered_info['style'] == 'display:none':
                    soup_basic.find('tr').decompose()
                else:
                    soup_basic_insuered_info = soup_basic.find('tr').find('tbody').find('tbody')
                    
                    #speical handling for 1 box
                    if soup_basic_insuered_info.find('td').has_attr('width') and (soup_basic_insuered_info.find('td')['width'] == '100%' or soup_basic_insuered_info.find('td')['width'] == '33%'):
                        soup_basic.find('tr').decompose()
                    else:
                        break
            except:
                soup_basic.find('tr').decompose()
        
        for strong_tag in soup_basic_insuered_info.find_all('b'):
            worksheet.write(0, idx+1, strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1
        
        soup_basic.find('tr').decompose()
        
        while True:
            try:
                soup_basic_benefit = soup_basic.find('tr')
                if soup_basic_benefit.has_attr('style') and soup_basic_benefit['style'] == 'display:none':
                    soup_basic.find('tr').decompose()
                else:
                    soup_basic_benefit = soup_basic.find('tr').find('tbody').find('tbody')
                    
                    #speical handling for 1 box
                    if soup_basic_benefit.find('td').has_attr('width') and (soup_basic_benefit.find('td')['width'] == '100%' or soup_basic_benefit.find('td')['width'] == '33%'):
                        soup_basic.find('tr').decompose()
                    else:
                        break
            except:
                soup_basic.find('tr').decompose()

        for strong_tag in soup_basic_benefit.find_all('b'):
            worksheet.write(0, idx+1, strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            idx = idx + 1
        
        soup_basic.find('tr').decompose()
        while True:
            try:
                soup_basic_benefit = soup_basic.find('tr')
                if soup_basic_benefit.has_attr('style') and soup_basic_benefit['style'] == 'display:none':
                    soup_basic.find('tr').decompose()
                else:
                    soup_basic_benefit = soup_basic.find('tr').find('tbody').find('tbody')
                    break
            except:
                soup_basic.find('tr').decompose()


        header = []
        for strong_tag in soup_basic_benefit.find_all('b'):
            header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        
        for x in range(0,9):
            worksheet.write(0, idx+1, header[x%3])
            idx = idx + 1


