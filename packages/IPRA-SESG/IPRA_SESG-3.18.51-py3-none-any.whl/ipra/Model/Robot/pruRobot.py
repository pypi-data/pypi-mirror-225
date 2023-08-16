
import time
from bs4 import BeautifulSoup
import xlsxwriter
from ipra.Utility.ConfigUtility import GetConfigSingletion
from ipra.Model.Robot.baseRobot import BaseRobot
import threading
from selenium.webdriver.common.by import By

class PruRobot(BaseRobot):
    def __init__(self, policyList, frame, reportPath,inputPath,downloadReport):
        super().__init__(policyList, frame, reportPath,inputPath,downloadReport)
        self.logger.writeLogString('PRU-INIT','ROBOT INIT')
        self.maxPolicyListSize = len(policyList)
        self.workbook = xlsxwriter.Workbook(self.reportPath+'PRU_report.xlsx')
        self.worksheet = self.workbook.add_worksheet(name="Basic")
        self.worksheet.write(0, 0, "Policy No.")

        self.finWorksheet = self.workbook.add_worksheet(name="Loan")
        self.finWorksheet.write(0, 0, "Policy No.")

        self.paymentWorksheet = self.workbook.add_worksheet(name="Payment")
        self.paymentWorksheet.write(0, 0, "Policy No.")

        self.logger.writeLogString('PRU-INIT','maxPolicyListSize:'+str(self.maxPolicyListSize))
        self.configParser = GetConfigSingletion()

    def waitingLoginComplete(self):
        self.logger.writeLogString('PRU-LOGIN','START LOGIN')
        self.browser.get("https://salesforce.prudential.com.hk/")
        self.frame.setStatusLableText(self.stringValue.waitingLogin.get())
        while not self.isLogin and not self.isStopped:
            try:
                self.browser.find_element(By.XPATH, "/html/body/div[@id='wrapper']/div[@id='footer']/div[1]/a[1]")
                self.isLogin=True  
            except:
                time.sleep(3)
        else:
            pass

        if self.isLogin:
            self.frame.setStatusLableText(self.stringValue.loginSuccess.get())
            self.logger.writeLogString('PRU-LOGIN','LOGIN COMPLETED')

    def scrapPolicy(self):
        url_link = 'https://aes.prudential.com.hk/saes/proposalpolicy/policyDetails?&policy_no={0}&agent_cd={1}&branch_cd=&user_id={2}&locale=zh'
        
        for policy in self.policyList:

            if self.isStopped:
                return
            
            self.frame.setStatusLableText(self.stringValue.processing.get().format(str(policy)))
            self.logger.writeLogString('PRU','PROCESSING:'+str(policy))
            try:
                policy_url_link = url_link.format(policy,self.configParser.ReadConfig('insurer','pru_agent_cd'),self.configParser.ReadConfig('insurer','pru_user_id'))
                self.browser.get(policy_url_link)
                #self.browser.switch_to.window(self.browser.window_handles[1])
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                file1 = open(self.reportPath+policy+".txt","a",encoding="utf-8")#append mode 
                file1.write(soup.prettify()) 
                file1.close()
                #self.browser.close()
                #self.browser.switch_to.window(self.browser.window_handles[0])
                self.downloadPolicyReport(str(policy))
            except Exception as ex:
                self.frame.setStatusLableText(self.stringValue.processException.get().format(str(policy),str(ex)))
                self.logger.writeLogString('PRU',str(policy)+" throws Exception:" + str(ex))
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            finally:
                self.frame.setStatusLableText(self.stringValue.processCompleted.get().format(str(policy)))
                self.logger.writeLogString('PRU',str(policy)+" COMPLETED")
                self.frame.setStatusProgresValueByValue(1)
                self.buildReportQueue.append(policy)
                self.buildHeaderQueue.append(policy)
    
    def downloadPolicyReport(self, policy):
        if not self.downloadReport:
            return
        
        report_link = 'https://aes.prudential.com.hk/saes/proposalpolicy/policyDetails?policy_no={0}&agent_cd={1}&branch_cd=&user_id={2}&locale=zh&color=bw&fontSize=12&basicInformation=1&financialOverview=1&autopayInformation=1&specialCondition=1&policyMovementEnquiry=1&claimHistory=1'.format(policy,self.configParser.ReadConfig('insurer','pru_agent_cd'),self.configParser.ReadConfig('insurer','pru_user_id'))
        self.logger.writeLogString('PRU','DOWNLOADING REPORT:'+str(policy))
        try:
            self.browser.get(report_link)
            #self.browser.switch_to.window(self.browser.window_handles[1])
            self.browser.execute_script('window.print();')
            #self.browser.close()
            #self.browser.switch_to.window(self.browser.window_handles[0])
        except:
            self.frame.setStatusLableText(policy+" is not found")
            self.logger.writeLogString('PRU',str(policy)+" DOWNLOAD FAILED")
        finally:
            self.frame.setStatusLableText(policy+" download report completed")
            self.logger.writeLogString('PRU',str(policy)+" DOWNLOAD REPORT COMPLETED")
    

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
        self.logger.writeLogString('PRU-HEADER','START BUILD HEADER FULLFLOW')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildHeaderQueue:
                self.logger.writeLogString('PRU-HEADER','POLICY NO.:{0}'.format(str(policy)))
                if self.isStopped:
                    return
                try:
                    file = open(self.reportPath+policy+".txt",encoding="utf-8")#append mode 
                    #Full Html src
                    soup_all_src = BeautifulSoup(file.read(), 'lxml')
                    file.close()
                    
                    soup_blockPolicyDetail_src = self.SearchByIdValue(soup_all_src,'blockPolicyDetail')
                    self.__PolicyDetailHeader(soup_blockPolicyDetail_src,self.worksheet)

                    soup_blockFinancialInfo_src = self.SearchByIdValue(soup_all_src,'blockFinancialInfo')
                    self.__FinancialInfoHeader(soup_blockFinancialInfo_src,self.finWorksheet)

                    soup_blockAutoPayInfo_src = self.SearchByIdValue(soup_all_src,'blockAutopayInfo')
                    self.__PaymentInfoHandling(soup_blockAutoPayInfo_src,self.paymentWorksheet,policy_iteration,policy)

                    #Start get blockBasicInfo
                    soup_blockBasicInfo_src = self.SearchByIdValue(soup_all_src,'blockBasicInfo')
                    soup_blockBasicInfo_table_result_details = self.SearchByHtmlTagClassValue(soup_blockBasicInfo_src,'table','result_details')
                    table_idx = 0
                    for single_table in soup_blockBasicInfo_table_result_details.find_all('table'):

                        soup_single_table = BeautifulSoup(str(single_table),'lxml')

                        if table_idx == 0:#Client Information
                            self.__ClientInfotmationHeader(soup_single_table,self.worksheet)
                        elif table_idx == 1: #Policy Information
                            self.__PolicyInformationHeader(soup_single_table,self.worksheet)
                        elif table_idx == 2: #Premium Information
                            self.__PremiumInformationHeader(soup_single_table,self.worksheet)
                            #print(str(soup_single_table).encode('utf-8'))
                        table_idx = table_idx + 1
                 
                    #No error when building the header,break all loop and then stop this thread
                    policy_iteration = self.maxPolicyListSize + 1
                    self.logger.writeLogString('PRU-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                    break
                except FileNotFoundError:
                    self.logger.writeLogString('PRU-HEADER','FILE NOT FOUND')
                except Exception as ex :
                    self.logger.writeLogString('PRU-HEADER','EXCEPTION:'+str(ex))
                finally:
                    policy_iteration = policy_iteration + 1
                    if policy in self.buildHeaderQueue:
                        self.buildHeaderQueue.remove(policy)
            else:
                time.sleep(1)

    
    def __buildReportHeaderHalfFlow(self):
        self.logger.writeLogString('PRU-HEADER','START BUILD HEADER HALFFLOW')
        for policy in self.policyList:
            self.logger.writeLogString('PRU-HEADER','POLICY NO.:{0}'.format(str(policy)))
            if self.isStopped:
                return
            try:
                file = open(self.inputPath+policy+".txt",encoding="utf-8")#append mode 
                #Full Html src
                soup_all_src = BeautifulSoup(file.read(), 'lxml')
                file.close()

                soup_blockPolicyDetail_src = self.SearchByIdValue(soup_all_src,'blockPolicyDetail')
                self.__PolicyDetailHeader(soup_blockPolicyDetail_src,self.worksheet)

                soup_blockFinancialInfo_src = self.SearchByIdValue(soup_all_src,'blockFinancialInfo')
                self.__FinancialInfoHeader(soup_blockFinancialInfo_src,self.finWorksheet)
                
                #Start get blockBasicInfo
                soup_blockBasicInfo_src = self.SearchByIdValue(soup_all_src,'blockBasicInfo')
                soup_blockBasicInfo_table_result_details = self.SearchByHtmlTagClassValue(soup_blockBasicInfo_src,'table','result_details')
                table_idx = 0
                for single_table in soup_blockBasicInfo_table_result_details.find_all('table'):

                    soup_single_table = BeautifulSoup(str(single_table),'lxml')

                    if table_idx == 0:#Client Information
                        self.__ClientInfotmationHeader(soup_single_table,self.worksheet)
                    elif table_idx == 1: #Policy Information
                        self.__PolicyInformationHeader(soup_single_table,self.worksheet)
                    elif table_idx == 2: #Premium Information
                        self.__PremiumInformationHeader(soup_single_table,self.worksheet)
                        #print(str(soup_single_table).encode('utf-8'))
                    table_idx = table_idx + 1
                                   
                #No error when building the header,break all loop and then stop this thread
                self.logger.writeLogString('PRU-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                break
            except FileNotFoundError as ex:
                self.logger.writeLogString('PRU-HEADER','FILE NOT FOUND')
            except Exception as ex:
                self.logger.writeLogString('PRU-HEADER','EXCEPTION:'+str(ex))
      
    def __buildReport(self):
        self.logger.writeLogString('PRU-CONTENT','START BUILD REPORT')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildReportQueue:

                if self.isStopped:
                    return
                
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),""))
                self.logger.writeLogString('PRU-CONTENT','POLICY NO.:{0}'.format(str(policy)))
                try:
                    file = open(self.reportPath+policy+".txt",encoding="utf-8")#append mode 
                    #Full Html src
                    soup_all_src = BeautifulSoup(file.read(), 'lxml')
                    file.close()
                    soup_blockPolicyDetail_src = self.SearchByIdValue(soup_all_src,'blockPolicyDetail')
                    self.__PolicyDetailHandling(soup_blockPolicyDetail_src,self.worksheet,policy_iteration)

                    soup_blockFinancialInfo_src = self.SearchByIdValue(soup_all_src,'blockFinancialInfo')
                    self.__FinancialInfoHandling(soup_blockFinancialInfo_src,self.finWorksheet,policy_iteration,policy)

                    soup_blockAutoPayInfo_src = self.SearchByIdValue(soup_all_src,'blockAutopayInfo')
                    self.__PaymentInfoHandling(soup_blockAutoPayInfo_src,self.paymentWorksheet,policy_iteration,policy)

                    #Start get blockBasicInfo
                    soup_blockBasicInfo_src = self.SearchByIdValue(soup_all_src,'blockBasicInfo')
                    soup_blockBasicInfo_table_result_details = self.SearchByHtmlTagClassValue(soup_blockBasicInfo_src,'table','result_details')
                    table_idx = 0
                    soup_preprocess = soup_blockBasicInfo_table_result_details.find_all('table')
                
                    if len(soup_preprocess) > 0:
    
                        for single_table in soup_preprocess:

                            soup_single_table = BeautifulSoup(str(single_table),'lxml')

                            if table_idx == 0:#Client Information
                                self.__ClientInfotmationHandling(soup_single_table,self.worksheet,policy_iteration)
                            elif table_idx == 1: #Policy Information
                                self.__PolicyInformationHandling(soup_single_table,self.worksheet,policy_iteration)
                            elif table_idx == 2: #Premium Information
                                self.__PremiumInformationHandling(soup_single_table,self.worksheet,policy_iteration)
                                #print(str(soup_single_table).encode('utf-8'))
                            table_idx = table_idx + 1
                    else:
                        self.worksheet.write(policy_iteration+1,0,str(policy))
                        self.worksheet.write(policy_iteration+1,1,"Policy maybe removed. Please check manually.")
                        self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"failed"))
                        self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
                        
                except FileNotFoundError:
                    self.worksheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                    self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"not found"))
                    self.logger.writeLogString('PRU-CONTENT','FILE NOT FOUND')
                    self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
                except Exception as ex:
                    self.worksheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!")
                    self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"failed"))
                    self.logger.writeLogString('PRU-CONTENT','EXCEPTION:'+str(ex))
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
        self.logger.writeLogString('PRU-CONTENT','COMPLETED BUILD REPORT')

    def __buildReportOnly(self):
        self.logger.writeLogString('PRU-CONTENT','START BUILD REPORT OFFLINE MODE')
        for policy_iteration,policy in enumerate(self.policyList):

            if self.isStopped:
                return
            
            self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),""))
            self.logger.writeLogString('PRU-CONTENT','POLICY NO.:{0}'.format(str(policy)))

            try:
                file = open(self.inputPath+policy+".txt",encoding="utf-8")#append mode 
                #Full Html src
                soup_all_src = BeautifulSoup(file.read(), 'lxml')
                file.close()
                soup_blockPolicyDetail_src = self.SearchByIdValue(soup_all_src,'blockPolicyDetail')
                self.__PolicyDetailHandling(soup_blockPolicyDetail_src,self.worksheet,policy_iteration)

                soup_blockFinancialInfo_src = self.SearchByIdValue(soup_all_src,'blockFinancialInfo')
                self.__FinancialInfoHandling(soup_blockFinancialInfo_src,self.finWorksheet,policy_iteration,policy)
                
                soup_blockAutoPayInfo_src = self.SearchByIdValue(soup_all_src,'blockAutopayInfo')
                self.__PaymentInfoHandling(soup_blockAutoPayInfo_src,self.paymentWorksheet,policy_iteration,policy)
                
                #Start get blockBasicInfo
                soup_blockBasicInfo_src = self.SearchByIdValue(soup_all_src,'blockBasicInfo')
                soup_blockBasicInfo_table_result_details = self.SearchByHtmlTagClassValue(soup_blockBasicInfo_src,'table','result_details')
                table_idx = 0
                
                soup_preprocess = soup_blockBasicInfo_table_result_details.find_all('table')
                
                if len(soup_preprocess) > 0:
                    for single_table in soup_preprocess:

                        soup_single_table = BeautifulSoup(str(single_table),'lxml')

                        if table_idx == 0:#Client Information
                            self.__ClientInfotmationHandling(soup_single_table,self.worksheet,policy_iteration)
                        elif table_idx == 1: #Policy Information
                            self.__PolicyInformationHandling(soup_single_table,self.worksheet,policy_iteration)
                        elif table_idx == 2: #Premium Information
                            self.__PremiumInformationHandling(soup_single_table,self.worksheet,policy_iteration)
                            #print(str(soup_single_table).encode('utf-8'))
                        table_idx = table_idx + 1
                else:
                    self.worksheet.write(policy_iteration+1,0,str(policy))
                    self.worksheet.write(policy_iteration+1,1,"Policy maybe removed. Please check manually.")
                    self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"failed"))
                    self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)

            except FileNotFoundError:
                self.worksheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"not found"))
                self.logger.writeLogString('PRU-CONTENT','FILE NOT FOUND')
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            except Exception as ex:
                self.worksheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!")
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"failed"))
                self.logger.writeLogString('PRU-CONTENT','EXCEPTION:'+str(ex))
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            finally:
                self.frame.setStatusProgresValueByValue(2)
                self.frame.setListItemColor(str(policy),self.STATUS_REPORT_COMPLETE)
                
        self.buildHeaderThread.join()
        self.workbook.close()
        self.frame.setStatusLableText(self.stringValue.completed.get())
        self.logger.writeLogString('PRU-CONTENT','COMPLETED BUILD REPORT OFFLINE MODE')

    def __PolicyDetailHandling(self,single_table,worksheet,row_idx):
        soup_blockPolicyDetail_table_result_details = self.SearchByHtmlTagClassValue(single_table,'table','result_details')
        soup_blockPolicyDetail_table_value = self.SearchByHtmlTagClassValue(soup_blockPolicyDetail_table_result_details,'td','result_value')

        #row_value = []
        for col,strong_tag in enumerate(soup_blockPolicyDetail_table_value.find_all('td')):
            #row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            worksheet.write(row_idx+1, col, strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        #for col_num, data in enumerate(row_value):
        #    worksheet.write(row_idx+1, col_num, data)

    def __PolicyDetailHeader(self,single_table,worksheet):
        soup_blockPolicyDetail_table_result_details = self.SearchByHtmlTagClassValue(single_table,'table','result_details')
        soup_blockPolicyDetail_table_header = self.SearchByHtmlTagClassValue(soup_blockPolicyDetail_table_result_details,'td','result_key')

        #row_header = []
        for col,strong_tag in enumerate(soup_blockPolicyDetail_table_header.find_all('td')):
            #row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            worksheet.write(0, col, strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        #for col_num, data in enumerate(row_header):
            #worksheet.write(0, col_num, data)

    def __ClientInfotmationHandling(self,single_table,worksheet,row_idx):
        i = 0
        j = 9
        k = 13
        
        i = 1
        soup_a_single_value = self.SearchByHtmlTagClassValue(single_table,'td','result_value')
        for strong_tag in soup_a_single_value.find_all('td')[0:7]:
            tag_value = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
            if i % 2 != 0 and i<6:
                #this case only run 3 times
                worksheet.write(row_idx+1, j, tag_value)
                j = j + 1
            else:
                worksheet.write(row_idx+1, k, tag_value)
                k = k + 1
            i = i + 1

    def __ClientInfotmationHeader(self,single_table,worksheet):
        i = 0
        soup_a_single_header = self.SearchByHtmlTagClassValue(single_table,'td','result_key polOwner')
        for strong_tag in soup_a_single_header.find_all('td'):
            tag_value = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
            worksheet.write(0, 8+i, tag_value)
            i = i + 1
        soup_a_single_header = self.SearchByHtmlTagClassValue(single_table,'td','result_key lifeAssured')
        for strong_tag in soup_a_single_header.find_all('td'):
            tag_value = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
            worksheet.write(0, 8+i, tag_value)
            i = i + 1

    def __PolicyInformationHandling(self,single_table,worksheet,row_idx):
        #print(str(single_table).encode('utf-8'))
        soup_a_single_value = self.SearchByHtmlTagClassValue(single_table,'td','result_value')
        #print(str(soup_a_single_value).encode('utf-8'))
        #row_value = []
        for col,strong_tag in enumerate(soup_a_single_value.find_all('td')):
            #row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            worksheet.write(row_idx+1,col+17,strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        #for col_num, data in enumerate(row_value):
        #    worksheet.write(row_idx+1, col_num+17, data)

    def __PolicyInformationHeader(self,single_table,worksheet):
        #print(str(single_table).encode('utf-8'))
        soup_a_single_header = self.SearchByHtmlTagClassValue(single_table,'td','result_key')
        #print(str(soup_a_single_value).encode('utf-8'))
        #row_header = []
        for col,strong_tag in enumerate(soup_a_single_header.find_all('td')):
            #row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            worksheet.write(0,col+17,strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        #for col_num, data in enumerate(row_header):
            #worksheet.write(0, col_num+17, data)

    def __PremiumInformationHandling(self,single_table,worksheet,row_idx):
        #Remove the 2 pop-up div class first
        #Total Current Modal Premium & Levy Modal ;; Premium & Levy at Next Anniversary Date*
        single_table.find('div', class_="benefit_breakdown_container").decompose()
        single_table.find('div', class_="benefit_breakdown_container").decompose()

        soup_a_single_value = self.SearchByHtmlTagClassValue(single_table,'td','result_value')
        self.SearchByHtmlTagClassValue(single_table,'table','popup_details')
        
        #row_value = []
        for col,strong_tag in enumerate(soup_a_single_value.find_all('td')):
            #row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            worksheet.write(row_idx+1, col+31, strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        #for col_num, data in enumerate(row_value):
        #    worksheet.write(row_idx+1, col_num+31, data)

    def __PremiumInformationHeader(self,single_table,worksheet):
        #Remove the 2 pop-up div class first
        #Total Current Modal Premium & Levy Modal ;; Premium & Levy at Next Anniversary Date*
        single_table.find('div', class_="benefit_breakdown_container").decompose()
        single_table.find('div', class_="benefit_breakdown_container").decompose()

        soup_a_single_header = self.SearchByHtmlTagClassValue(single_table,'td','result_key')
        self.SearchByHtmlTagClassValue(single_table,'table','popup_details')
        row_header = []
        for col,strong_tag in enumerate(soup_a_single_header.find_all('td')):
            #row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            worksheet.write(0, col+31, strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        #for col_num, data in enumerate(row_header):
        #    worksheet.write(0, col_num+31, data)
        
    def __FinancialInfoHeader(self,single_table, worksheet):
        worksheet.write(0, 0, "Policy No.")
        '''
        try:
            single_table.find('table',class_="result_details").decompose()
            single_table.find('table',class_="result_details").decompose()
            single_table.find('table',class_="result_details").decompose()
            single_table.find('table',class_="result_details").decompose()
        except:
            pass
        soup_a_single_header = self.SearchByHtmlTagClassValue(single_table,'td','result_key')
        #print(str(soup_a_single_value).encode('utf-8'))
        #row_header = []
        for col,strong_tag in enumerate(soup_a_single_header.find_all('td')):
            #row_header.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            worksheet.write(0,col+1,strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        #for col_num, data in enumerate(row_header):
            #worksheet.write(0, col_num+17, data)
        '''

        for table in single_table.find_all('table',class_="result_details"):
            testA = BeautifulSoup(str(table), 'lxml')
            testB = testA.find('td',class_="result_header result_header_last")
            if testB == None or len(testB) == 0:
                continue
            elif "貸款" in testB.text or "Loan" in testB.text:
                for col, tag in enumerate(testA.find_all('td',class_="result_key")):
                    worksheet.write(0,col+1,tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        pass

    def __FinancialInfoHandling(self,single_table,worksheet,row_idx,policy):
        worksheet.write(row_idx+ 1, 0, str(policy))

        '''
        try:
            single_table.find('table',class_="result_details").decompose()
            single_table.find('table',class_="result_details").decompose()
            single_table.find('table',class_="result_details").decompose()
            single_table.find('table',class_="result_details").decompose()
        except:
            pass

        soup_blockPolicyDetail_table_value = self.SearchByHtmlTagClassValue(single_table,'td','result_value')
        
        #row_value = []
        for col,strong_tag in enumerate(soup_blockPolicyDetail_table_value.find_all('td')):
            #row_value.append(strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
            worksheet.write(row_idx+1, col+1, strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))
        #for col_num, data in enumerate(row_value):
        #    worksheet.write(row_idx+1, col_num, data)

        pass
        '''
        for table in single_table.find_all('table',class_="result_details"):
            testA = BeautifulSoup(str(table), 'lxml')
            testB = testA.find('td',class_="result_header result_header_last")
            if testB == None or len(testB) == 0:
                continue
            elif "貸款" in testB.text or "Loan" in testB.text:
                for col, tag in enumerate(testA.find_all('td',class_="result_value")):
                    worksheet.write(row_idx+1,col+1,tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' '))

    def __PaymentInfoHandling(self,single_table,worksheet,row_idx,policy):
        worksheet.write(row_idx+ 1, 0, str(policy))
        paymentMethodContent = single_table.find('div',id = 'payMethod')
        worksheet.write(row_idx+ 1, 1, paymentMethodContent.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ').replace(' ',''))
        
        for col,table in enumerate(single_table.find_all('td')):
            testA = BeautifulSoup(str(table), 'lxml')
            content = testA.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
            if len(content) == 0:
                continue
            else:
                worksheet.write(row_idx+ 1, col+2, str(content))