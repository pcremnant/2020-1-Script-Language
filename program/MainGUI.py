from tkinter import *
from tkinter import font

from DataSet import *
from xmlManager import *
from mailMark import *

from fileMailMarked import *


def buttonActive(button, color='white'):
    button['state'] = 'active'
    button['bg'] = color


def buttonDisabled(button, color='light gray'):
    button['state'] = 'disabled'
    button['bg'] = color


class MainGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("국가자격 Data")
        self.window.geometry("1000x600")
        self.window.configure(bg='white')
        self.window.resizable(False, False)

        self.fontSearchButton = font.Font(self.window, size=14, weight='bold', family='consolas')
        self.fontSearchResult = font.Font(self.window, size=12, weight='bold', family='consolas')
        self.fontInfo = font.Font(self.window, size=12, weight='bold', family='consolas')

        self.frameSearch = Frame(self.window, width=1000, height=100, relief='flat', bg='light gray', bd=2)
        self.frameSearch.place(x=0, y=0)

        self.frameSearchResult = Frame(self.window, width=400, height=500, relief='flat', bg='gray95')
        self.frameSearchResult.place(x=0, y=100)

        self.frameInfo = Frame(self.window, width=600, height=500, relief='flat', bg='blue')
        self.frameInfo.place(x=400, y=100)

        self.strXmlQualificationInfo = []

        scd = ['01', '02', '03', '04']
        for i in range(4):
            self.strXmlQualificationInfo.append(0)
            # strQuery = 'serviceKey=' + serviceKey + '&seriesCd=' + scd[i]
            # self.strXmlQualificationInfo.append(loadOpenAPI(OPEN_API_URL[QUALIFICATION_INFO], OPEN_API_NAME[QUALIFICATION_INFO] + strQuery))

        self.strXml = []

        strQuery = 'serviceKey=' + serviceKey
        self.strXml.append(loadOpenAPI(OPEN_API_URL[QUALIFICATION_LIST], OPEN_API_NAME[QUALIFICATION_LIST] + strQuery))
        self.strXml.append(self.strXmlQualificationInfo[0])

        self.currentSearchPage = 0
        self.maxSearchPage = 0
        self.seriesCode = '01'
        self.searchResult = []
        self.qualificationInfo = []
        self.currentInfoPage = 0
        self.maxInfoPage = 0

        self.strTestData = {}
        for i in range(4):
            self.strTestData.update({'0'+str(i+1): self.getTestData('0'+str(i + 1))})

        # text
        # 시리즈 코드 / 페이지 / 인덱스 x 자격명 / 텍스트
        self.mailMarked = []
        tmpMailMarked = loadMailMarked()
        if tmpMailMarked is not None:
            for mark in tmpMailMarked:
                self.mailMarked.append(mark)

        self.receiveMailAddr = ''

        # entry
        self.entrySearch = None
        self.entryMailAddr = None

        # labels
        self.labelSearchResult = None
        self.labelInfo = []
        self.labelInfoPageNumber = None
        self.labelSearchPageNumber = None

        # buttons
        self.buttonSearch = None
        self.buttonSendMail = None
        self.buttonShowMailMarked = None
        self.buttonSeriesSelect = []
        self.buttonSearchResult = []
        self.buttonSearchPage = []
        self.buttonInfoPage = []
        self.buttonMailMark = []

        # set up
        self.setEntries()
        self.setButtons()
        self.setLabels()
        self.resetInfoPage()

        self.search(None)

        self.window.mainloop()
        saveMailMarked(self.mailMarked)

    def setButtons(self):
        # search button
        self.buttonSearch = Button(self.frameSearch, font=self.fontSearchButton, text='검색', width=5, height=1,
                                   command=self.pressedSearch)
        self.buttonSearch.place(x=730, y=30)
        self.buttonSendMail = Button(self.frameSearch, font=self.fontSearchButton, text='메일전송', width=8, height=1,
                                     command=self.pressedSendMail)
        self.buttonSendMail.place(x=800, y=30)

        self.buttonShowMailMarked = Button(self.frameSearch, font=self.fontSearchButton, text='메일마크', width=8, height=1,
                                           command=self.pressedShowMailMarked)
        self.buttonShowMailMarked.place(x=900, y=30)

        # series selection button
        strSelectButton = ['기술사', '기능장', '기사', '기능사']
        funcSelectButton = [self.pressedSeries1, self.pressedSeries2, self.pressedSeries3, self.pressedSeries4]
        for i in range(4):
            self.buttonSeriesSelect.append(
                Button(self.frameSearch, font=self.fontSearchButton, text=strSelectButton[i], width=5, height=1
                       , command=funcSelectButton[i]))
            self.buttonSeriesSelect[i].place(x=40 + 80 * i, y=30)

        # search result
        funcSearchResult = [self.pressedSearchResult1, self.pressedSearchResult2, self.pressedSearchResult3,
                            self.pressedSearchResult4, self.pressedSearchResult5, self.pressedSearchResult6,
                            self.pressedSearchResult7, self.pressedSearchResult8, self.pressedSearchResult9,
                            self.pressedSearchResult10, self.pressedSearchResult11, self.pressedSearchResult12,
                            self.pressedSearchResult13, self.pressedSearchResult14, self.pressedSearchResult15]
        funcMailMark = [self.pressedMailMark1, self.pressedMailMark2, self.pressedMailMark3, self.pressedMailMark4,
                        self.pressedMailMark5, self.pressedMailMark6, self.pressedMailMark7, self.pressedMailMark8,
                        self.pressedMailMark9, self.pressedMailMark10, self.pressedMailMark11, self.pressedMailMark12,
                        self.pressedMailMark13, self.pressedMailMark14, self.pressedMailMark15]
        p = PhotoImage(file='mailMark.png')
        for i in range(SEARCH_PAGE_SIZE):
            self.buttonSearchResult.append(Button(self.frameSearchResult, font=self.fontSearchResult, text='',
                                                  width=44, height=1, bd=0, command=funcSearchResult[i]))
            self.buttonSearchResult[i].place(x=0, y=15 + 29 * i)
            button = Button(self.frameSearchResult, image=p, command=funcMailMark[i])
            button.image = p
            button.place(x=350, y=15 + 29 * i)
            self.buttonMailMark.append(button)

        # info page button
        self.buttonInfoPage.append(
            Button(self.frameInfo, font=self.fontSearchResult, text='이전', width=4, height=1,
                   bd=1, command=self.pressedPrevInfoPage))
        self.buttonInfoPage.append(
            Button(self.frameInfo, font=self.fontSearchResult, text='다음', width=4, height=1,
                   bd=1, command=self.pressedNextInfoPage))
        self.buttonInfoPage[PREV_PAGE].place(x=225, y=460)
        self.buttonInfoPage[NEXT_PAGE].place(x=325, y=460)

        # search page button
        self.buttonSearchPage.append(Button(self.frameSearchResult, font=self.fontSearchResult, text='이전', width=4,
                                            height=1, bd=1, command=self.pressedPrevSearchPage))
        self.buttonSearchPage.append(Button(self.frameSearchResult, font=self.fontSearchResult, text='다음', width=4,
                                            height=1, bd=1, command=self.pressedNextSearchPage))
        self.buttonSearchPage[PREV_PAGE].place(x=125, y=460)
        self.buttonSearchPage[NEXT_PAGE].place(x=225, y=460)

        self.setButtonAction()
        self.setSearchResultButtonAction()

    def setEntries(self):
        self.entrySearch = Entry(self.frameSearch, font=self.fontSearchButton, width=30)
        self.entrySearch.place(x=410, y=35)

    def setLabels(self):
        for i in range(INFO_PAGE_SIZE):
            self.labelInfo.append(Label(text='', width=66, height=1, font=self.fontInfo,
                                        bg='light blue', fg='black', anchor='w'))
            self.labelInfo[i].place(x=400, y=100 + 25 * i)

        self.labelInfoPageNumber = Label(text=str(self.currentInfoPage + 1), width=2, height=1, font=self.fontInfo,
                                         bg='light gray', fg='black')
        self.labelInfoPageNumber.place(x=685, y=563)

        self.labelSearchPageNumber = Label(text=str(self.currentSearchPage + 1), width=2, height=1,
                                           font=self.fontSearchResult, bg='light gray', fg='black')
        self.labelSearchPageNumber.place(x=185, y=563)

    def search(self, keyword=None):
        self.searchResult.clear()
        searchResult = searchFromInquiry(self.strXml[QUALIFICATION_LIST], self.seriesCode, keyword)
        self.resetSearchResultButton()
        self.maxSearchPage = 0
        self.currentSearchPage = 0
        if self.labelSearchResult is not None:
            self.labelSearchResult.destroy()
        if searchResult is None:
            self.labelSearchResult = Label(text='search return is none', width=20, height=1,
                                           font=self.fontSearchResult, bg='gray97', fg='cyan')
            self.labelSearchResult.place(x=0, y=100)
        elif len(searchResult) == 0:
            self.labelSearchResult = Label(text='검색 결과가 없습니다', width=20, height=1, font=self.fontSearchResult,
                                           bg='gray97', fg='black')
            self.labelSearchResult.place(x=100, y=350)
        else:
            for result in searchResult:
                self.searchResult.append(result)
            self.maxSearchPage = len(self.searchResult) // SEARCH_PAGE_SIZE
            self.showSearchResult()

        self.setSearchResultButtonAction()

    def showSearchResult(self):
        for i in range(SEARCH_PAGE_SIZE):
            if self.currentSearchPage * SEARCH_PAGE_SIZE + i >= len(self.searchResult):
                self.buttonSearchResult[i].configure(text='')
                self.buttonSearchResult[i]['state'] = 'disabled'
            else:
                self.buttonSearchResult[i].configure(
                    text=self.searchResult[self.currentSearchPage * SEARCH_PAGE_SIZE + i])
                if self.buttonSearchResult[i]['state'] == 'disabled':
                    self.buttonSearchResult[i]['state'] = 'active'
        self.setMailMark()
        self.setPageButton()

    def setSearchResultButtonAction(self):
        for button in self.buttonSearchResult:
            if button['text'] == '':
                buttonDisabled(button, 'gray99')
            else:
                buttonActive(button, 'gray95')

    def resetSearchResultButton(self):
        for button in self.buttonSearchResult:
            button['text'] = ''
        self.setSearchResultButtonAction()

    def setButtonAction(self):
        series = ['01', '02', '03', '04']
        for i in range(4):
            if series[i] != self.seriesCode:
                buttonActive(self.buttonSeriesSelect[i])
            else:
                buttonDisabled(self.buttonSeriesSelect[i])

    # button command ------------------------------------------------
    def pressedShowMailMarked(self):
        self.mailMarkedWindow = Tk()
        self.mailMarkedWindow.title('show mail marked')
        self.mailMarkedWindow.geometry('300x600')
        self.mailMarkedWindow.resizable(False, False)
        self.mailMarkedWindow.configure(bg='white')

        fontTitle = font.Font(self.mailMarkedWindow, size=14, weight='bold', family='consolas')
        fontMark = font.Font(self.mailMarkedWindow, size=12, weight='bold', family='consolas')

        Label(self.mailMarkedWindow, font=fontTitle, text='메일 전송 리스트', fg='black', bg='light gray', width=30).pack()

        i = 0
        for mark in self.mailMarked:
            Label(self.mailMarkedWindow, font=fontMark, width=30, height=1, text=mark.name, fg='black', bg='white').pack() # .place(x=10, y=i*30 + 10)
            i = i+1
        self.mailMarkedWindow.mainloop()

    def pressedSendMail(self):
        self.sendWindow = Tk()
        self.sendWindow.title('Send E-Mail')
        self.sendWindow.geometry('300x110')
        self.sendWindow.resizable(False, False)
        fontTitle = font.Font(self.sendWindow, size=14, family='consolas')
        fontButton = font.Font(self.sendWindow, size=14, weight='bold', family='consolas')

        label = Label(self.sendWindow, font=fontTitle, width=25, height=1, text='메일 주소를 입력하세요')
        label.pack() #place(x=10, y=5)

        self.entryMailAddr = Entry(self.sendWindow, font=fontTitle, width=22)
        self.entryMailAddr.pack() # place(x=25, y=40)
        button = Button(self.sendWindow, font=fontButton, text='보내기', command=self.pressedSend)
        button.pack(side='bottom') # place(x=110, y=70)
        self.sendWindow.mainloop()

    def pressedSend(self):
        from email.mime.text import MIMEText
        import smtplib
        text = ''
        for mark in self.mailMarked:
            text += mark.text + '\n'
        msg = MIMEText(text)
        msg['Subject'] = 'Qualification Info'
        msg['From'] = MAIL_SENDER
        msg['To'] = str(self.entryMailAddr.get())

        s = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(MAIL_SENDER, MAIL_PASSWORD)
        s.sendmail(MAIL_SENDER, [str(self.entryMailAddr.get())], msg.as_string())
        s.close()

        self.sendWindow.destroy()

    def getTestData(self, seriesCode):
        strXml = loadOpenAPI(TEST_API_BASE_URL, TEST_API_URL[seriesCode] + TEST_API_QUERY)
        text = ''
        try:
            tree = ElementTree.fromstring(strXml)
        except Exception:
            print('Etree error : Test data')
            return None
        elementIter = tree.iter('item')
        for eIter in elementIter:
            testName = eIter.find('description')
            if testName is not None:
                testName = testName.text
            else:
                return '시험정보 없음'

            registerDocTestStart, registerDocTestEnd = eIter.find('docregstartdt'), eIter.find('docregenddt')
            if registerDocTestStart is not None and registerDocTestEnd is not None:
                registerDocTest = registerDocTestStart.text + ' ~ ' + registerDocTestEnd.text
            else:
                return testName + '\n시험 정보 없음'

            docTest = eIter.find('docexamdt')
            if docTest is not None:
                docTest = docTest.text
            else:
                return testName + '\n시험 정보 없음'
            text += testName + '\n필기시험 접수\n' + registerDocTest + '\n필기시험 일자\n' + docTest + '\n\n'

        return text

    def pressedMailMark(self, index):
        isNotMarked = True
        for mark in self.mailMarked:
            if mark.isSameMark(self.seriesCode, self.searchResult[self.currentSearchPage * SEARCH_PAGE_SIZE + index]):
                p = PhotoImage(file='mailMark.PNG')
                self.buttonMailMark[index]['image'] = p
                self.buttonMailMark[index].image = p
                isNotMarked = False
                self.mailMarked.remove(mark)
                break
        if isNotMarked:
            # text에 시험 정보들을 넣을 예정
            text = self.searchResult[self.currentSearchPage * SEARCH_PAGE_SIZE + index] + '\n\n' + self.strTestData[self.seriesCode]
            # 여기에 넣는다..

            self.mailMarked.append(
                mailMark(self.seriesCode, self.searchResult[self.currentSearchPage * SEARCH_PAGE_SIZE + index], text))
            p = PhotoImage(file='mailMarked.PNG')
            self.buttonMailMark[index]['image'] = p
            self.buttonMailMark[index].image = p

    def pressedMailMark1(self):
        self.pressedMailMark(0)

    def pressedMailMark2(self):
        self.pressedMailMark(1)

    def pressedMailMark3(self):
        self.pressedMailMark(2)

    def pressedMailMark4(self):
        self.pressedMailMark(3)

    def pressedMailMark5(self):
        self.pressedMailMark(4)

    def pressedMailMark6(self):
        self.pressedMailMark(5)

    def pressedMailMark7(self):
        self.pressedMailMark(6)

    def pressedMailMark8(self):
        self.pressedMailMark(7)

    def pressedMailMark9(self):
        self.pressedMailMark(8)

    def pressedMailMark10(self):
        self.pressedMailMark(9)

    def pressedMailMark11(self):
        self.pressedMailMark(10)

    def pressedMailMark12(self):
        self.pressedMailMark(11)

    def pressedMailMark13(self):
        self.pressedMailMark(12)

    def pressedMailMark14(self):
        self.pressedMailMark(13)

    def pressedMailMark15(self):
        self.pressedMailMark(14)

    def pressedPrevInfoPage(self):
        if self.currentInfoPage <= 0:
            pass
        else:
            self.currentInfoPage -= 1
        self.showInfo()

    def pressedNextInfoPage(self):
        if self.currentInfoPage >= self.maxInfoPage:
            pass
        else:
            self.currentInfoPage += 1
        self.showInfo()

    def pressedPrevSearchPage(self):
        if self.currentSearchPage <= 0:
            pass
        else:
            self.currentSearchPage -= 1
        self.showSearchResult()

    def pressedNextSearchPage(self):
        if self.currentSearchPage >= self.maxSearchPage:
            pass
        else:
            self.currentSearchPage += 1
        self.showSearchResult()

    def pressedSeries1(self):
        self.seriesCode = '01'
        self.setStrXml()
        self.setButtonAction()
        self.search()

    def pressedSeries2(self):
        self.seriesCode = '02'
        self.setStrXml()
        self.setButtonAction()
        self.search()

    def pressedSeries3(self):
        self.seriesCode = '03'
        self.setStrXml()
        self.setButtonAction()
        self.search()

    def pressedSeries4(self):
        self.seriesCode = '04'
        self.setStrXml()
        self.setButtonAction()
        self.search()

    def pressedSearchResult1(self):
        self.setInfoString(0)

    def pressedSearchResult2(self):
        self.setInfoString(1)

    def pressedSearchResult3(self):
        self.setInfoString(2)

    def pressedSearchResult4(self):
        self.setInfoString(3)

    def pressedSearchResult5(self):
        self.setInfoString(4)

    def pressedSearchResult6(self):
        self.setInfoString(5)

    def pressedSearchResult7(self):
        self.setInfoString(6)

    def pressedSearchResult8(self):
        self.setInfoString(7)

    def pressedSearchResult9(self):
        self.setInfoString(8)

    def pressedSearchResult10(self):
        self.setInfoString(9)

    def pressedSearchResult11(self):
        self.setInfoString(10)

    def pressedSearchResult12(self):
        self.setInfoString(11)

    def pressedSearchResult13(self):
        self.setInfoString(12)

    def pressedSearchResult14(self):
        self.setInfoString(13)

    def pressedSearchResult15(self):
        self.setInfoString(14)

    def pressedSearch(self):
        self.search(self.entrySearch.get())
        self.resetInfoPage()

    # ---------------------------------------------------------------------
    def setStrXml(self):
        if self.seriesCode == '01':
            self.strXml[QUALIFICATION_INFO] = self.strXmlQualificationInfo[0]
        elif self.seriesCode == '02':
            self.strXml[QUALIFICATION_INFO] = self.strXmlQualificationInfo[1]
        elif self.seriesCode == '03':
            self.strXml[QUALIFICATION_INFO] = self.strXmlQualificationInfo[2]
        elif self.seriesCode == '04':
            self.strXml[QUALIFICATION_INFO] = self.strXmlQualificationInfo[3]

        # strQuery = 'serviceKey=' + serviceKey + '&seriesCd=' + self.seriesCode
        # self.strXml.append(loadOpenAPI(OPEN_API_URL[QUALIFICATION_INFO], OPEN_API_NAME[QUALIFICATION_INFO] + strQuery))

    def setMailMark(self):
        # 서치 리저트 페이지 이동 시
        # 시리즈 코드 변경 시
        # 메일 마크를 최신화 할 것
        for i in range(SEARCH_PAGE_SIZE):
            p = PhotoImage(file='mailMark.PNG')
            for mark in self.mailMarked:
                if self.currentSearchPage * SEARCH_PAGE_SIZE + i >= len(self.searchResult):
                    p = None
                elif mark.isSameMark(self.seriesCode, self.searchResult[self.currentSearchPage * SEARCH_PAGE_SIZE + i]):
                    p = PhotoImage(file='mailMarked.PNG')
            self.buttonMailMark[i]['image'] = p
            self.buttonMailMark[i].image = p

    def showInfo(self):
        if len(self.qualificationInfo) < 1:
            pass
        for i in range(INFO_PAGE_SIZE):
            if self.currentInfoPage * INFO_PAGE_SIZE + i >= len(self.qualificationInfo):
                self.labelInfo[i]['text'] = ''
            else:
                self.labelInfo[i]['text'] = self.qualificationInfo[
                    self.currentInfoPage * INFO_PAGE_SIZE + i]
        self.setPageButton()

    def setInfoString(self, index):
        self.resetInfoPage()
        searchInfo = searchQualificationInfo(self.strXml[QUALIFICATION_INFO],
                                             self.buttonSearchResult[index][
                                                 'text'],
                                             DATA_TAG[QUALIFICATION_INFO])
        if searchInfo is None:
            pass
        else:
            lineCount = 0
            for tag in DATA_TAG[QUALIFICATION_INFO]:
                lineCount += 1
                self.qualificationInfo.append(TAG_TO_STRING[tag])
                strInfo = searchInfo[tag]
                if strInfo is None or strInfo == ' ':
                    lineCount += 1
                    self.qualificationInfo.append('정보가 없습니다.')
                else:
                    # lineCount += line
                    strLen = len(strInfo)
                    line = strLen // INFO_LABEL_WIDTH + 1
                    lineCount += line

                    for l in range(line):
                        strLine = ''
                        for i in range(INFO_LABEL_WIDTH):
                            if (l * INFO_LABEL_WIDTH + i) >= strLen:
                                # self.qualificationInfo.append(strLine)
                                break
                            else:
                                strLine += strInfo[l * INFO_LABEL_WIDTH + i]
                        self.qualificationInfo.append(strLine)
                self.maxInfoPage = lineCount // INFO_PAGE_SIZE
                self.currentInfoPage = 0
        self.showInfo()

    def setPageButton(self):
        # info page
        if self.currentInfoPage <= 0:
            buttonDisabled(self.buttonInfoPage[PREV_PAGE])
        else:
            buttonActive(self.buttonInfoPage[PREV_PAGE])
        if self.currentInfoPage >= self.maxInfoPage:
            buttonDisabled(self.buttonInfoPage[NEXT_PAGE])
        else:
            buttonActive(self.buttonInfoPage[NEXT_PAGE])
        self.labelInfoPageNumber['text'] = str(self.currentInfoPage + 1)

        # search page
        if self.currentSearchPage <= 0:
            buttonDisabled(self.buttonSearchPage[PREV_PAGE])
        else:
            buttonActive(self.buttonSearchPage[PREV_PAGE])
        if self.currentSearchPage >= self.maxSearchPage:
            buttonDisabled(self.buttonSearchPage[NEXT_PAGE])
        else:
            buttonActive(self.buttonSearchPage[NEXT_PAGE])
        self.labelSearchPageNumber['text'] = str(self.currentSearchPage + 1)

    def resetInfoPage(self):
        self.qualificationInfo.clear()
        self.currentInfoPage = 0
        self.maxInfoPage = 0
        for label in self.labelInfo:
            label['text'] = ''
        self.setPageButton()
        self.labelInfoPageNumber['text'] = str(self.currentInfoPage + 1)


MainGUI()
