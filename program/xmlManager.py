# -*- coding: cp949 -*-
from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree
import urllib
import http.client

def searchFromInquiry(strXml, seriesCode, keyword=None):
    searchResult = []
    try:
        tree = ElementTree.fromstring(strXml)
    except Exception:
        print("Element tree parsing error")
        return None
    #
    elementIter = tree.iter('item')
    for eIter in elementIter:
        # 종목 코드를 받아온다
        strSeriesCode = eIter.find('seriescd')
        if strSeriesCode is None:
            pass
        elif seriesCode == strSeriesCode.text:
            if keyword is None:
                searchResult.append(eIter.find('jmfldnm').text)
            else:
                strSearch = eIter.find('jmfldnm')
                if strSearch.text.find(keyword) >= 0:
                    searchResult.append(strSearch.text)
    return searchResult


def searchQualificationInfo(strXml, jobName, tags):
    infoList = {}
    try:
        tree = ElementTree.fromstring(strXml)
    except Exception:
        print("Element tree parsing error")
        return None

    elementIter = tree.iter('item')
    for eIter in elementIter:
        strJobName = eIter.find('jmNm').text
        if strJobName == jobName:
            for tag in tags:
                strData = eIter.find(tag)
                infoList.update({tag: strData.text})
            return infoList
    return None


def checkDocument(dataDoc):
    if dataDoc is None:
        print("Error : Document is empty")
        return False
    return True


def loadOpenAPI(connection, url):
    conn = http.client.HTTPConnection(connection)
    conn.request("GET", url)
    req = conn.getresponse()
    print(req.status, req.reason)
    return req.read().decode('utf-8')

# loadOpenAPI("openapi.q-net.or.kr",
#             "/api/service/rest/InquiryListNationalQualifcationSVC/getList?serviceKey=aYfjcFBQW5DXnjHqWMmLyALqC77Mh1RoSNDEM3YrOTm%2FIZXGfUzAaEYpAm5dE2wG30rvybkoBPVt0wnQzIKZRA%3D%3D")
