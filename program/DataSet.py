apiUrl = 'openapi.q-net.or.kr'
serviceKey = 'aYfjcFBQW5DXnjHqWMmLyALqC77Mh1RoSNDEM3YrOTm%2FIZXGfUzAaEYpAm5dE2wG30rvybkoBPVt0wnQzIKZRA%3D%3D'

SEARCH_PAGE_SIZE = 15
INFO_PAGE_SIZE = 18
INFO_LABEL_WIDTH = 40

PREV_PAGE = 0
NEXT_PAGE = 1


INQUIRY_LIST = 0
INQUIRY_LIST_TAG = {'series code': 0, 'job name': 1, 'job code': 2}

QUALIFICATION_INFO = 1
QUALIFICATION_INFO_TAG = {'job name kr': 0, 'job name en': 1, 'series name': 2}

TAG = [INQUIRY_LIST_TAG, QUALIFICATION_INFO_TAG]

XML_FILES = ['qualificationInquiryList.xml', 'qualificationInfo.xml']

OPEN_API_CONN = ["openapi.q-net.or.kr", "openapi.q-net.or.kr"]
OPEN_API_REQ = ["/api/service/rest/InquiryListNationalQualifcationSVC/getList?serviceKey=aYfjcFBQW5DXnjHqWMmLyALqC77Mh1RoSNDEM3YrOTm%2FIZXGfUzAaEYpAm5dE2wG30rvybkoBPVt0wnQzIKZRA%3D%3D",
                "/api/service/rest/InquiryQualInfo/getList?serviceKey=aYfjcFBQW5DXnjHqWMmLyALqC77Mh1RoSNDEM3YrOTm%2FIZXGfUzAaEYpAm5dE2wG30rvybkoBPVt0wnQzIKZRA%3D%3D&seriesCd=01"]

# loadOpenAPI("openapi.q-net.or.kr",
#             "/api/service/rest/InquiryListNationalQualifcationSVC/getList?serviceKey=aYfjcFBQW5DXnjHqWMmLyALqC77Mh1RoSNDEM3YrOTm%2FIZXGfUzAaEYpAm5dE2wG30rvybkoBPVt0wnQzIKZRA%3D%3D")


DATA_TAG = [
    ['seriescd', 'jmfldnm', 'jmcd',  'qualgbcd', 'qualgbnm',  'seriesnm', 'obligfldcd', 'obligfldnm', 'mdobligfldcd', 'mdobligfldnm'],
    ['jmNm', 'engJmNm', 'seriesNm', 'career', 'hist', 'implNm', 'instiNm', 'job', 'mdobligFldNm', 'summary', 'trend']
]
TAG_TO_STRING = {'jmNm': '[자격명]', 'engJmNm': '[자격 영문명]', 'seriesNm': '[자격 등급]', 'career': '[진로 및 전망]', 'hist': '[변천 과정]',
                 'implNm': '[시행 기관]', 'instiNm': '[관련 부처]', 'job': '[수행 직무]', 'mdobligFldNm': '[직종]', 'summary': '[개요]',
                 'trend': '[출제 경향]'}
