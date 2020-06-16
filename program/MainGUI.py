from tkinter import *
from tkinter import font

from DataSet import *
from xmlManager import *
# from .data.xmlManager import *
# from .data.DataSet import *


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

        self.fontSearchButton = font.Font(self.window, size=16, weight='bold', family='consolas')
        self.fontSearchResult = font.Font(self.window, size=12, weight='bold', family='consolas')
        self.fontInfo = font.Font(self.window, size=12, weight='bold', family='consolas')

        self.frameSearch = Frame(self.window, width=1000, height=100, relief='flat', bg='light gray', bd=2)
        self.frameSearch.place(x=0, y=0)

        self.frameSearchResult = Frame(self.window, width=400, height=500, relief='flat', bg='gray95')
        self.frameSearchResult.place(x=0, y=100)

        self.frameInfo = Frame(self.window, width=600, height=500, relief='flat', bg='blue')
        self.frameInfo.place(x=400, y=100)

        self.xmlFileData = []
        self.strXml = []

        for i in range(2):
            self.strXml.append(loadOpenAPI(OPEN_API_CONN[i], OPEN_API_REQ[i]))

        self.currentSearchPage = 0
        self.maxSearchPage = 0
        self.SeriesCode = '01'
        self.searchResult = []
        self.qualificationInfo = []
        self.currentInfoPage = 0
        self.maxInfoPage = 0

        # entry
        self.entrySearch = None

        # labels
        self.labelSearchResult = None
        self.labelInfo = []
        self.labelInfoPageNumber = None
        self.labelSearchPageNumber = None

        # buttons
        self.buttonSearch = None
        self.buttonSeriesSelect = []
        self.buttonSearchResult = []
        self.buttonSearchPage = []
        self.buttonInfoPage = []

        # set up
        self.setEntries()
        self.setButtons()
        self.setLabels()
        self.resetInfoPage()

        self.search(None)

        self.window.mainloop()

    def setButtons(self):
        # search button
        self.buttonSearch = (Button(self.frameSearch, font=self.fontSearchButton, text='검색', width=5, height=1,
                                    command=self.pressedSearch))
        self.buttonSearch.place(x=900, y=30)

        # series selection button
        strSelectButton = ['기술사', '기능장', '기사', '기능사']
        funcSelectButton = [self.pressedSeries1, self.pressedSeries2, self.pressedSeries3, self.pressedSeries4]
        for i in range(4):
            self.buttonSeriesSelect.append(
                Button(self.frameSearch, font=self.fontSearchButton, text=strSelectButton[i], width=5, height=1
                       , command=funcSelectButton[i]))
            self.buttonSeriesSelect[i].place(x=40 + 100 * i, y=30)

        # search result
        funcSearchResult = [self.pressedSearchResult1, self.pressedSearchResult2, self.pressedSearchResult3,
                            self.pressedSearchResult4, self.pressedSearchResult5, self.pressedSearchResult6,
                            self.pressedSearchResult7, self.pressedSearchResult8, self.pressedSearchResult9,
                            self.pressedSearchResult10, self.pressedSearchResult11, self.pressedSearchResult12,
                            self.pressedSearchResult13, self.pressedSearchResult14, self.pressedSearchResult15]
        for i in range(SEARCH_PAGE_SIZE):
            self.buttonSearchResult.append(Button(self.frameSearchResult, font=self.fontSearchResult, text='',
                                                  width=44, height=1, bd=0, command=funcSearchResult[i]))
            self.buttonSearchResult[i].place(x=0, y=15 + 29 * i)

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
        self.entrySearch.place(x=500, y=35)

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
        searchResult = searchFromInquiry(self.strXml[INQUIRY_LIST], self.SeriesCode, keyword)
        self.resetSearchResultButton()
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
            self.showSearchResult()

        self.setSearchResultButtonAction()

    def showSearchResult(self):
        for i in range(SEARCH_PAGE_SIZE):
            if self.currentSearchPage * SEARCH_PAGE_SIZE + i >= len(self.searchResult):
                break
            else:
                self.buttonSearchResult[i].configure(
                    text=self.searchResult[self.currentSearchPage * SEARCH_PAGE_SIZE + i])

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
            if series[i] != self.SeriesCode:
                buttonActive(self.buttonSeriesSelect[i])
            else:
                buttonDisabled(self.buttonSeriesSelect[i])

    # button command ------------------------------------------------
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
        self.SeriesCode = '01'
        self.setButtonAction()
        self.search()

    def pressedSeries2(self):
        self.SeriesCode = '02'
        self.setButtonAction()
        self.search()

    def pressedSeries3(self):
        self.SeriesCode = '03'
        self.setButtonAction()
        self.search()

    def pressedSeries4(self):
        self.SeriesCode = '04'
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
    def showInfo(self):
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
                                             self.buttonSearchResult[self.currentSearchPage * SEARCH_PAGE_SIZE + index][
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
