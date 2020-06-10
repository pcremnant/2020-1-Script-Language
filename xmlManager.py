# -*- coding: cp949 -*-
from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree


def LoadXMLFromFile(fileName):
    try:
        xmlFileData = open(fileName, 'r', encoding='utf-8')
    except IOError:
        print("Invalid file name or path")
    else:
        try:
            dom = parse(xmlFileData)
        except Exception:
            print("Loading Fail")
        else:
            print("XML Document loading complete")
            return dom
    return None


def searchFromInquiry(dataDoc, seriesCode, keyword=None):
    searchResult = []
    if not checkDocument(dataDoc):
        return None
    try:
        tree = ElementTree.fromstring(str(dataDoc.toxml()))
    except Exception:
        print("Element tree parsing error")
        return None

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


def searchQualificationInfo(dataDoc, jobName, tags):
    infoList = {}

    if not checkDocument(dataDoc):
        return None
    try:
        tree = ElementTree.fromstring(str(dataDoc.toxml()))
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
