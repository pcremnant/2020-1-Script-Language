from tkinter import *
from xmlManager import *
from DataSet import *

key = 'serviceKey=' + get_data(PRIVATE_DATA_SERVICE_KEY)
year = '&baseYY=' + str(2017)
api_url = "openapi.q-net.or.kr"
api_query = '/api/service/rest/InquiryExamQualPtcondSVC/getExamRecpList?' + key + year


# class MainGUI:
#     def __init__(self):
#         self.window = Tk()
#         self.window.geometry("800x600")
#         self.window.resizable(False, False)
#         self.window.title('test')


strXml = loadOpenAPI(api_url, api_query)


def searchYear(strXml):
    infoList = {}
    try:
        tree = ElementTree.fromstring(strXml)
    except Exception:
        print("Element tree parsing error")
        return None
    tmp = []

    elementIter = tree.iter('item')
    for eIter in elementIter:
        tmp.append(eIter.find('grdNm').text)
    return tmp

a = searchYear(strXml)
for i in a:
    if i is not None:
        print(i)