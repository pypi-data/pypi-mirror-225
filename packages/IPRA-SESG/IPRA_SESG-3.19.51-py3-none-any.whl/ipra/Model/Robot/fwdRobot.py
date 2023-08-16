import os
import time
from ipra.Model.Robot.baseRobot import BaseRobot
from bs4 import BeautifulSoup
import xlsxwriter
import threading
from genericpath import exists
from selenium.webdriver.common.by import By

class FwdRobot(BaseRobot):
    
    def __init__(self, policyList, frame, reportPath,inputPath,downloadReport):
        super().__init__(policyList, frame, reportPath,inputPath,downloadReport)
        self.logger.writeLogString('FWD-INIT','ROBOT INIT')
        self.maxPolicyListSize = len(policyList)
        self.workbook = xlsxwriter.Workbook(self.reportPath+'FWD_report.xlsx')
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.write(0, 0, "Policy No.")
        self.logger.writeLogString('FWD-INIT','maxPolicyListSize:'+str(self.maxPolicyListSize))


    def waitingLoginComplete(self):
        self.logger.writeLogString('FWD-LOGIN','START LOGIN')
        self.browser.get("https://home.fwd.com.hk/life/aesnet/ClientPolicySearch.aspx")
        while not self.isLogin and not self.isStopped:
            try:
                time.sleep(5)
                self.browser.find_element(By.XPATH, "/html/body/form/div[3]/div[1]/div[4]/div/input[1]")
                self.isLogin = True
                self.frame.setStatusLableText(self.stringValue.loginSuccess.get())
                self.logger.writeLogString('FWD-LOGIN','LOGIN COMPLETED')
            except:
                pass

    def scrapPolicy(self):
        for policy in self.policyList:
            if self.isStopped:
                return
            try:
                self.frame.setStatusLableText(self.stringValue.processing.get().format(str(policy)))
                self.logger.writeLogString('FWD','PROCESSING:'+str(policy))

                input = self.browser.find_element(By.XPATH, "/html/body/form/div[3]/div[1]/div[4]/div/input[1]")
                input.clear()
                input.send_keys(str(policy))
                serach = self.browser.find_element(By.XPATH, "/html/body/form/div[3]/div[1]/div[4]/div/input[2]")
                serach.click()

                time.sleep(2)
                expand = self.browser.find_element(By.XPATH, "/html/body/form/div[3]/div[5]/div/div[1]/table/tbody/tr[2]/td[1]/input")
                expand.click()
                time.sleep(2)
                self.browser.find_element(By.LINK_TEXT, str(policy)).click()
                #This sleep should be wait unit loading complete
                time.sleep(15)
                
                soup = BeautifulSoup(self.browser.page_source, 'lxml')
                file1 = open(self.reportPath+policy+".txt","a",encoding="utf-8")#append mode 
                file1.write(soup.prettify()) 
                file1.close()
                
                self.downloadPolicyReport(str(policy))
                
            except Exception as ex:
                self.frame.setStatusLableText(self.stringValue.processException.get().format(str(policy),str(ex)))
                self.logger.writeLogString('FWD',str(policy)+" throws Exception:" + str(ex))
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            finally:
                self.frame.setStatusLableText(self.stringValue.processCompleted.get().format(str(policy)))
                self.logger.writeLogString('FWD',str(policy)+" COMPLETED")
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
        
        reportFullPath = self.reportPath+"Agency Enquiry System.pdf"
        self.browser.execute_script('window.print();')
        #self.browser.get_screenshot_as_file(reportFullPath)
        while exists(reportFullPath) == False:
            time.sleep(1)
        os.rename(reportFullPath,self.reportPath+policy+".pdf")

    def __buildReportHeaderFullFlow(self):
        self.logger.writeLogString('FWD-HEADER','START BUILD HEADER FULLFLOW')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildHeaderQueue:
                self.logger.writeLogString('FWD-HEADER','POLICY NO.:{0}'.format(str(policy)))
                if self.isStopped:
                    return
                try:
                    file = open(self.reportPath+policy+".txt",encoding="utf-8")#append mode 
                    #Full Html src
                    soup = BeautifulSoup(file.read(), 'lxml')
                    file.close()

                    row_header = []
                    
                    row_temp = []
                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table8')
                    for strong_tag in soup_basic.find_all('td'):
                        header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                        if header == '' or header == ':':
                            continue
                        else:
                            row_temp.append(header)
                    
                    for x in range(3):
                        row_header.append(row_temp[x+5])
                        row_header.append(row_temp[0])
                        row_header.append(row_temp[1])
                        row_header.append(row_temp[2])
                        row_header.append(row_temp[3])
                        row_header.append(row_temp[4])

                    row_temp = []
                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table9')
                    for strong_tag in soup_basic.find_all('td'):
                        header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                        if header == '' or header == ':':
                            continue
                        else:
                            row_temp.append(header)
                    row_header.append(row_temp[0])
                    row_header += ['']*3
                    row_header.append(row_temp[1])
                    row_header.append('')
                    row_header.append(row_temp[2])
                    row_header.append('')
                    row_header.append(row_temp[3])
                    row_header.append('')
                    row_header.append(row_temp[4])

                    row_temp = []
                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table10')
                    soup_basic.find("td", id="MainContent_tlcEPolicyEnabled").decompose()
                    soup_basic.find("td", id="MainContent_tlcEPolicyLinkGroup").decompose()
                    for strong_tag in soup_basic.find_all('td'):
                        header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                        if header == '' or header == ':':
                            continue
                        else:
                            row_header.append(header)
                            row_header.append('')
                            row_header.append('')
                    
                    row_temp = ['','','','']
                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table2')
                    for iteration,strong_tag in enumerate(soup_basic.find_all('th')):
                        header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                        row_temp[iteration] = header
                    
                    for x in range(0,4,1):
                        row_header.append(row_temp[x])
                                    
                    row_temp = []
                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table5')
                    for strong_tag in soup_basic.find_all('td'):
                        header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                        if header == '' or header == ':':
                            continue
                        else:
                            row_header.append(header)

                    row_temp = []
                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table11')
                    soup_basic.find("input", id="MainContent_updRmk").decompose()

                    for strong_tag in soup_basic.find_all('td'):
                        header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                        if header == '' or header == ':':
                            continue
                        else:
                            row_header.append(header)
                            
                    row_temp = []
                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table16')
                    soup_basic.find("tr", style=lambda value: value and 'background-color:LightGoldenrodYellow' in value).decompose()
                    soup_basic.find('b').decompose()
                    soup_basic.find('b').decompose()
                    soup_basic.find('b').decompose()
                    soup_basic.find("span",id="MainContent_lblDisClaim").decompose()
                    soup_basic.find("ol").decompose()
                    
                    for strong_tag in soup_basic.find_all('td'):
                        header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                        if header == '' or header == ':':
                            continue
                        else:
                            row_header.append(header)
                            
                    #Build Plan details
                    #first remove policy Remarks
                    row_temp = []
                    soup_basic = soup.find("table",id="MainContent_Table4").find_next_sibling("table").find_next_sibling("table")
                    for strong_tag in soup_basic.find_all('span'):
                        header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                        row_header.append(header)

                    for col_num, data in enumerate(row_header):
                        self.worksheet.write(0, col_num+1, data)
                        
                    #No error when building the header,break all loop and then stop this thread
                    policy_iteration = self.maxPolicyListSize + 1
                    self.logger.writeLogString('FWD-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                    break
                except FileNotFoundError:
                    self.logger.writeLogString('FWD-HEADER','FILE NOT FOUND')
                except Exception as ex:
                    self.logger.writeLogString('FWD-HEADER','EXCEPTION:'+str(ex))
                finally:
                    policy_iteration = policy_iteration + 1
                    if policy in self.buildHeaderQueue:
                        self.buildHeaderQueue.remove(policy)
            else:
                time.sleep(1)
                
    def __buildReportHeaderHalfFlow(self):
        self.logger.writeLogString('FWD-HEADER','START BUILD HEADER HALFFLOW')
        for policy in self.policyList:
            self.logger.writeLogString('FWD-HEADER','POLICY NO.:{0}'.format(str(policy)))
            if self.isStopped:
                return
            try:
                file = open(self.inputPath+policy+".txt",encoding="utf-8")#append mode 
                #Full Html src
                soup = BeautifulSoup(file.read(), 'lxml')
                file.close()

                row_header = []
                
                row_temp = []
                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table8')
                for strong_tag in soup_basic.find_all('td'):
                    header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                    if header == '' or header == ':':
                        continue
                    else:
                        row_temp.append(header)
                
                for x in range(3):
                    row_header.append(row_temp[x+5])
                    row_header.append(row_temp[0])
                    row_header.append(row_temp[1])
                    row_header.append(row_temp[2])
                    row_header.append(row_temp[3])
                    row_header.append(row_temp[4])

                row_temp = []
                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table9')
                for strong_tag in soup_basic.find_all('td'):
                    header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                    if header == '' or header == ':':
                        continue
                    else:
                        row_temp.append(header)
                row_header.append(row_temp[0])
                row_header += ['']*3
                row_header.append(row_temp[1])
                row_header.append('')
                row_header.append(row_temp[2])
                row_header.append('')
                row_header.append(row_temp[3])
                row_header.append('')
                row_header.append(row_temp[4])

                row_temp = []
                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table10')
                soup_basic.find("td", id="MainContent_tlcEPolicyEnabled").decompose()
                soup_basic.find("td", id="MainContent_tlcEPolicyLinkGroup").decompose()
                for strong_tag in soup_basic.find_all('td'):
                    header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                    if header == '' or header == ':':
                        continue
                    else:
                        row_header.append(header)
                        row_header.append('')
                        row_header.append('')
                
                row_temp = ['','','','']
                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table2')
                for iteration,strong_tag in enumerate(soup_basic.find_all('th')):
                    header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                    row_temp[iteration] = header
                
                for x in range(0,4,1):
                    row_header.append(row_temp[x])
                                
                row_temp = []
                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table5')
                for strong_tag in soup_basic.find_all('td'):
                    header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                    if header == '' or header == ':':
                        continue
                    else:
                        row_header.append(header)

                row_temp = []
                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table11')
                soup_basic.find("input", id="MainContent_updRmk").decompose()

                for strong_tag in soup_basic.find_all('td'):
                    header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                    if header == '' or header == ':':
                        continue
                    else:
                        row_header.append(header)
                        

                row_temp = []
                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table16')
                soup_basic.find("tr", style=lambda value: value and 'background-color:LightGoldenrodYellow' in value).decompose()
                soup_basic.find('b').decompose()
                soup_basic.find('b').decompose()
                soup_basic.find('b').decompose()
                soup_basic.find("span",id="MainContent_lblDisClaim").decompose()
                soup_basic.find("ol").decompose()
                
                for strong_tag in soup_basic.find_all('td'):
                    header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                    if header == '' or header == ':':
                        continue
                    else:
                        row_header.append(header)

                #Build Plan details
                #first remove policy Remarks
                row_temp = []
                soup_basic = soup.find("table",id="MainContent_Table4").find_next_sibling("table").find_next_sibling("table")
                for strong_tag in soup_basic.find_all('span'):
                    header = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                    row_header.append(header)

                for col_num, data in enumerate(row_header):
                    self.worksheet.write(0, col_num+1, data)

                self.logger.writeLogString('FWD-HEADER','BUILD HEADER COMPLETED, BREAK LOOP')
                break
            except FileNotFoundError as ex:
                self.logger.writeLogString('FWD-HEADER','FILE NOT FOUND')
            except Exception as ex:
                self.logger.writeLogString('FWD-HEADER','EXCEPTION:'+str(ex))

    def __buildReport(self):
        self.logger.writeLogString('FWD-CONTENT','START BUILD REPORT')
        policy_iteration = 0
        while policy_iteration < self.maxPolicyListSize:
            for policy in self.buildReportQueue:
                if self.isStopped:
                    return
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),""))
                self.logger.writeLogString('FWD-CONTENT','POLICY NO.:{0}'.format(str(policy)))
                try:
                    self.worksheet.write(policy_iteration+1,0,str(policy))
                    file = open(self.reportPath+policy+".txt",encoding="utf-8")#append mode 
                    #Full Html src
                    soup = BeautifulSoup(file.read(), 'lxml')
                    file.close()

                    row_value = []
                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table8')
                    for iteration,strong_tag in enumerate(soup_basic.find_all('input')):
                        if iteration % 5 == 0:
                            row_value.append('')
                        try:
                            value = strong_tag['value']
                        except:
                            value = ''
                        row_value.append(value)
                    
                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table9')
                    for x in range(1,5):
                        try:
                            value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtAdd{0}'.format(x)).find_all('input')
                            row_value.append(value[0]['value'])
                        except:
                            row_value.append('')

                    try:
                        value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtBusTel').find_all('input')
                        row_value.append(value[0]['value'])
                    except:
                        row_value.append('')
                    try:
                        value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtBusFax').find_all('input')
                        row_value.append(value[0]['value'])
                    except:
                        row_value.append('')
                    try:
                        value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtResTel').find_all('input')
                        row_value.append(value[0]['value'])
                    except:
                        row_value.append('')
                    try:
                        value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtResFax').find_all('input')
                        row_value.append(value[0]['value'])
                    except:
                        row_value.append('')
                    try:
                        value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtPager').find_all('input')
                        row_value.append(value[0]['value'])
                    except:
                        row_value.append('')
                    try:
                        value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtMobile').find_all('input')
                        row_value.append(value[0]['value'])
                    except:
                        row_value.append('')
                    try:
                        value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtEmail').find_all('input')
                        row_value.append(value[0]['value'])
                    except:
                        row_value.append('')

                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table10')
                    soup_basic.find("td", id="MainContent_tlcEPolicyEnabled").decompose()
                    soup_basic.find("td", id="MainContent_tlcEPolicyLinkGroup").decompose()
                    for iteration,strong_tag in enumerate(soup_basic.find_all('input')):
                        try:
                            value = strong_tag['value']
                        except:
                            value = ''
                        row_value.append(value)

                    row_temp2 = ['','','','']
                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table2')
                    
                    idx = 0    
                    for strong_tag in soup_basic.find_all('span'):
                        value = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                        if value != '':
                            row_temp2[idx] = value
                            idx = idx + 1
                    
                    for x in range(0,4,1):
                        #row_header.append(row_temp[x])
                        row_value.append(row_temp2[x])
                    
                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table5')
                    for iteration,strong_tag in enumerate(soup_basic.find_all('input')):
                        try:
                            value = strong_tag['value']
                        except:
                            value = ''
                        row_value.append(value)

                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table11')
                    soup_basic.find("input", id="MainContent_updRmk").decompose()
                    
                    for iteration,strong_tag in enumerate(soup_basic.find_all('input')):
                        try:
                            value = strong_tag['value']
                        except:
                            value = ''
                        row_value.append(value)

                    textarea = soup_basic.find("textarea", id="MainContent_txtPolRmk")
                    try:
                        row_value.append(textarea.__getattribute__('value'))
                    except:
                        row_value.append('')

                    soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table16')
                    soup_basic.find("tr", style=lambda value: value and 'background-color:LightGoldenrodYellow' in value).decompose()
                    soup_basic.find('b').decompose()
                    soup_basic.find('b').decompose()
                    soup_basic.find('b').decompose()
                    soup_basic.find("span",id="MainContent_lblDisClaim").decompose()
                    soup_basic.find("ol").decompose()
                    
                    for iteration,strong_tag in enumerate(soup_basic.find_all('input')):
                        try:
                            value = strong_tag['value']
                        except:
                            value = ''
                        row_value.append(value)

                    #Build Plan details
                    #first remove policy Remarks
                    try:
                        soup_basic = soup.find("table",id="MainContent_Table4").find_next_sibling("table").find_next_sibling("table")
                        soup_basic.find("tr",class_="grid_header").decompose()
                        soup_basic.find("tr",class_="grid_header").decompose()
                        soup_basic.find("tr",class_="grid_header").decompose()
                    except:
                        # To skip 1 more table : "Customer Risk Profile"
                        soup_basic = soup_basic.find_next_sibling("table")
                        soup_basic.find("tr",class_="grid_header").decompose()
                        soup_basic.find("tr",class_="grid_header").decompose()
                        soup_basic.find("tr",class_="grid_header").decompose()
                    
                    for strong_tag in soup_basic.find_all('td'):
                        value = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                        row_value.append(value)

                    for col_num, data in enumerate(row_value):
                        self.worksheet.write(policy_iteration+1, col_num+1, data)

                        
                except FileNotFoundError:
                    self.worksheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                    self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"not found"))
                    self.logger.writeLogString('FWD-CONTENT','FILE NOT FOUND')
                    self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
                except Exception as ex:
                    self.worksheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!")
                    self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"failed"))
                    self.logger.writeLogString('FWD-CONTENT','EXCEPTION:'+str(ex))
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
        self.logger.writeLogString('FWD-CONTENT','COMPLETED BUILD REPORT')

    def __buildReportOnly(self):
        self.logger.writeLogString('FWD-CONTENT','START BUILD REPORT OFFLINE MODE')
        for policy_iteration,policy in enumerate(self.policyList):
            if self.isStopped:
                return
            self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),""))
            self.logger.writeLogString('FWD-CONTENT','POLICY NO.:{0}'.format(str(policy)))
            try:
                self.worksheet.write(policy_iteration+1,0,str(policy))
                file = open(self.inputPath+policy+".txt",encoding="utf-8")#append mode 
                #Full Html src
                soup = BeautifulSoup(file.read(), 'lxml')
                file.close()

                row_value = []
                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table8')
                for iteration,strong_tag in enumerate(soup_basic.find_all('input')):
                    if iteration % 5 == 0:
                        row_value.append('')
                    try:
                        value = strong_tag['value']
                    except:
                        value = ''
                    row_value.append(value)
                
                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table9')
                for x in range(1,5):
                    try:
                        value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtAdd{0}'.format(x)).find_all('input')
                        row_value.append(value[0]['value'])
                    except:
                        row_value.append('')

                try:
                    value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtBusTel').find_all('input')
                    row_value.append(value[0]['value'])
                except:
                    row_value.append('')
                try:
                    value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtBusFax').find_all('input')
                    row_value.append(value[0]['value'])
                except:
                    row_value.append('')
                try:
                    value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtResTel').find_all('input')
                    row_value.append(value[0]['value'])
                except:
                    row_value.append('')
                try:
                    value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtResFax').find_all('input')
                    row_value.append(value[0]['value'])
                except:
                    row_value.append('')
                try:
                    value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtPager').find_all('input')
                    row_value.append(value[0]['value'])
                except:
                    row_value.append('')
                try:
                    value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtMobile').find_all('input')
                    row_value.append(value[0]['value'])
                except:
                    row_value.append('')
                try:
                    value = self.SearchByHtmlTagValueKey(soup_basic,'input','id','MainContent_txtEmail').find_all('input')
                    row_value.append(value[0]['value'])
                except:
                    row_value.append('')

                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table10')
                soup_basic.find("td", id="MainContent_tlcEPolicyEnabled").decompose()
                soup_basic.find("td", id="MainContent_tlcEPolicyLinkGroup").decompose()
                for iteration,strong_tag in enumerate(soup_basic.find_all('input')):
                    try:
                        value = strong_tag['value']
                    except:
                        value = ''
                    row_value.append(value)

                row_temp2 = ['','','','']
                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table2')
                
                idx = 0    
                for strong_tag in soup_basic.find_all('span'):
                    value = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                    if value != '':
                        row_temp2[idx] = value
                        idx = idx + 1
                
                for x in range(0,4,1):
                    #row_header.append(row_temp[x])
                    row_value.append(row_temp2[x])
                
                
                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table5')
                for iteration,strong_tag in enumerate(soup_basic.find_all('input')):
                    try:
                        value = strong_tag['value']
                    except:
                        value = ''
                    row_value.append(value)

                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table11')
                soup_basic.find("input", id="MainContent_updRmk").decompose()
                
                for iteration,strong_tag in enumerate(soup_basic.find_all('input')):
                    try:
                        value = strong_tag['value']
                    except:
                        value = ''
                    row_value.append(value)

                textarea = soup_basic.find("textarea", id="MainContent_txtPolRmk")
                try:
                    row_value.append(textarea.__getattribute__('value'))
                except:
                    row_value.append('')

                soup_basic = self.SearchByHtmlTagValueKey(soup,'table','id','MainContent_Table16')
                soup_basic.find("tr", style=lambda value: value and 'background-color:LightGoldenrodYellow' in value).decompose()
                soup_basic.find('b').decompose()
                soup_basic.find('b').decompose()
                soup_basic.find('b').decompose()
                soup_basic.find("span",id="MainContent_lblDisClaim").decompose()
                soup_basic.find("ol").decompose()
                
                for iteration,strong_tag in enumerate(soup_basic.find_all('input')):
                    try:
                        value = strong_tag['value']
                    except Exception as e:
                        value = ''
                    row_value.append(value)

                #Build Plan details
                #first remove policy Remarks
                try:
                    soup_basic = soup.find("table",id="MainContent_Table4").find_next_sibling("table").find_next_sibling("table")
                    soup_basic.find("tr",class_="grid_header").decompose()
                    soup_basic.find("tr",class_="grid_header").decompose()
                    soup_basic.find("tr",class_="grid_header").decompose()
                except:
                    # To skip 1 more table : "Customer Risk Profile"
                    soup_basic = soup_basic.find_next_sibling("table")
                    soup_basic.find("tr",class_="grid_header").decompose()
                    soup_basic.find("tr",class_="grid_header").decompose()
                    soup_basic.find("tr",class_="grid_header").decompose()
                
                for strong_tag in soup_basic.find_all('td'):
                    value = strong_tag.text.strip().replace('\t','').replace('\n','').replace(u'\xa0', u' ')
                    row_value.append(value)

                for col_num, data in enumerate(row_value):
                    self.worksheet.write(policy_iteration+1, col_num+1, data)
                
            except FileNotFoundError:
                self.worksheet.write(policy_iteration+1,1,str(policy)+" not found in this A/C, please check other A/C")
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"not found"))
                self.logger.writeLogString('FWD-CONTENT','FILE NOT FOUND')
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            except Exception as ex :
                self.worksheet.write(policy_iteration+1,1,"System Error ! Please contact IT Support!")
                self.frame.setStatusLableText(self.stringValue.buildReport.get().format(str(policy),"failed"))
                self.logger.writeLogString('FWD-CONTENT','EXCEPTION:'+str(ex))
                self.frame.setListItemColor(str(policy),self.STATUS_EXCEPTION)
            finally:
                self.frame.setStatusProgresValueByValue(2)
                self.frame.setListItemColor(str(policy),self.STATUS_REPORT_COMPLETE)
                
        self.buildHeaderThread.join()
        self.workbook.close()
        self.frame.setStatusLableText(self.stringValue.completed.get())
        self.logger.writeLogString('FWD-CONTENT','COMPLETED BUILD REPORT OFFLINE MODE')
