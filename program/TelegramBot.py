import telepot
import http.client
from pprint import pprint
import traceback
import sys
import time
from DataSet import *
from xml.etree import ElementTree

from datetime import date, datetime, timedelta

MAX_MSG_LENGTH = 300

key = get_data(PRIVATE_DATA_SERVICE_KEY)
token = get_data(PRIVATE_DATA_TELEGRAM_TOKEN)

baseUrl = "openapi.q-net.or.kr"
apiName = {
    1: '/api/service/rest/InquiryTestInformationNTQSVC/getPEList?',
    2: '/api/service/rest/InquiryTestInformationNTQSVC/getMCList?',
    3: '/api/service/rest/InquiryTestInformationNTQSVC/getEList?',
    4: '/api/service/rest/InquiryTestInformationNTQSVC/getCList?'
}
toNumber = {
    '01': 1, '1': 1, '기술사': 1,
    '02': 2, '2': 2, '기능장': 2,
    '03': 3, '3': 3, '기사': 3, '산업기사': 3,
    '04': 4, '4': 4, '기능사': 4
}

apiQuery = 'serviceKey=' + key


def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)


def getData(series_code):
    res_list = []
    strXml = loadOpenAPI(baseUrl, apiName[series_code] + apiQuery)
    try:
        tree = ElementTree.fromstring(strXml)
    except Exception:
        print('Etree error')
        return
    elementIter = tree.iter('item')
    for eIter in elementIter:
        testName = eIter.find('description').text
        registerDocTest = eIter.find('docregstartdt').text + ' ~ ' + eIter.find('docregenddt').text
        docTest = eIter.find('docexamdt').text
        row = testName + '\n필기시험 접수\n' + registerDocTest + '\n필기시험 일자\n' + docTest + '\n\n'
        res_list.append(row)

    return res_list


def replyQualificationData(user, series_code):
    print(user, series_code)
    res_list = None
    if series_code in toNumber:
        res_list = getData(toNumber[series_code])
    else:
        sendMessage(user, '해당 데이터가 없습니다.\n')
        return
    msg = ''
    for r in res_list:
        print(str(datetime.now()).split('.')[0], r)
        if len(r + msg) + 1 > MAX_MSG_LENGTH:
            sendMessage(user, msg)
            msg = r + '\n'
        else:
            msg += r + '\n'

    if msg:
        sendMessage(user, msg)
    else:
        sendMessage(user, '해당 데이터가 없습니다.\n')


def loadOpenAPI(apiUrl, searchQuery):
    conn = http.client.HTTPConnection(apiUrl)
    conn.request("GET", searchQuery)
    req = conn.getresponse()
    print(req.status, req.reason)
    return req.read().decode('utf-8')


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '텍스트 메세지만 처리할 수 있습니다.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('시험') and len(args) > 1:
        print('try to 시험', args[1])
        replyQualificationData(chat_id, args[1])
    else:
        sendMessage(chat_id, '모르는 명령어입니다.\n시험 [종목코드]')
    # 종목 코드


bot = telepot.Bot(token)
pprint(bot.getMe())
bot.message_loop(handle)

print('Listening...')

while 1:
    time.sleep(10)