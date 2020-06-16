# -*- coding: cp949 -*-
from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree
import urllib
import http.client
from urllib.parse import urlparse
from DataSet import *


def loadOpenAPI(connection, url):
    conn = http.client.HTTPConnection(connection)
    conn.request("GET", url)
    req = conn.getresponse()
    print(req.status, req.reason)
    return req.read().decode('utf-8')


def LoadXMLFromOpenAPI(req):
    try:
        dom = parse(req)
    except Exception:
        print("Loading fail")
    else:
        print("Open API loading complete")
        return dom


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


url = 'openapi.q-net.or.kr'
serviceKey = 'serviceKey=aYfjcFBQW5DXnjHqWMmLyALqC77Mh1RoSNDEM3YrOTm%2FIZXGfUzAaEYpAm5dE2wG30rvybkoBPVt0wnQzIKZRA%3D%3D'
query = '&'

strXml = loadOpenAPI(url, '/api/service/rest/InquiryQualInfo/getList?' + serviceKey + '&seriesCd=01')
print(strXml)

search = searchQualificationInfo(strXml, '건축구조기술사', DATA_TAG[QUALIFICATION_INFO])

for k, v in search.items():
    print(k, ' : ', v)
