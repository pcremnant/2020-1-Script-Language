from get_data import get_data
PRIVATE_DATA_GMAIL_ID = 0
PRIVATE_DATA_GMAIL_PW = 1
PRIVATE_DATA_GMAIL_PORT = 2
PRIVATE_DATA_SERVICE_KEY = 3


apiUrl = 'openapi.q-net.or.kr'

serviceKey = get_data(PRIVATE_DATA_SERVICE_KEY)

SEARCH_PAGE_SIZE = 15
INFO_PAGE_SIZE = 18
INFO_LABEL_WIDTH = 40

PREV_PAGE = 0
NEXT_PAGE = 1


QUALIFICATION_LIST = 0
QUALIFICATION_LIST_TAG = {'series code': 0, 'job name': 1, 'job code': 2}

QUALIFICATION_INFO = 1
QUALIFICATION_INFO_TAG = {'job name kr': 0, 'job name en': 1, 'series name': 2}

TAG = [QUALIFICATION_LIST_TAG, QUALIFICATION_INFO_TAG]

XML_FILES = ['qualificationInquiryList.xml', 'qualificationInfo.xml']

OPEN_API_URL = ["openapi.q-net.or.kr", "openapi.q-net.or.kr"]
OPEN_API_NAME = ['/api/service/rest/InquiryListNationalQualifcationSVC/getList?',
                 '/api/service/rest/InquiryQualInfo/getList?']
OPEN_API_QUERY = [{'serviceKey=': serviceKey},
                  {'serviceKey=': serviceKey, 'seriesCd=': '01'}]

DATA_TAG = [
    ['seriescd', 'jmfldnm', 'jmcd',  'qualgbcd', 'qualgbnm',  'seriesnm', 'obligfldcd', 'obligfldnm', 'mdobligfldcd', 'mdobligfldnm'],
    ['jmNm', 'engJmNm', 'seriesNm', 'career', 'hist', 'implNm', 'instiNm', 'job', 'mdobligFldNm', 'summary', 'trend']
]
TAG_TO_STRING = {'jmNm': '[자격명]', 'engJmNm': '[자격 영문명]', 'seriesNm': '[자격 등급]', 'career': '[진로 및 전망]', 'hist': '[변천 과정]',
                 'implNm': '[시행 기관]', 'instiNm': '[관련 부처]', 'job': '[수행 직무]', 'mdobligFldNm': '[직종]', 'summary': '[개요]',
                 'trend': '[출제 경향]'}

TEST_API_BASE_URL = "openapi.q-net.or.kr"
TEST_API_URL = {
    '01': '/api/service/rest/InquiryTestInformationNTQSVC/getPEList?',
    '02': '/api/service/rest/InquiryTestInformationNTQSVC/getMCList?',
    '03': '/api/service/rest/InquiryTestInformationNTQSVC/getEList?',
    '04': '/api/service/rest/InquiryTestInformationNTQSVC/getCList?'
}
TEST_API_QUERY = 'serviceKey=' + serviceKey

# 나중에 c++ dll 파일로 작성하기
MAIL_HOST = 'smtp.gmail.com'
MAIL_PORT = get_data(PRIVATE_DATA_GMAIL_PORT)
MAIL_SENDER = get_data(PRIVATE_DATA_GMAIL_ID)
MAIL_PASSWORD = get_data(PRIVATE_DATA_GMAIL_PW)

