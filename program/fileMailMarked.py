from mailMark import *


def saveMailMarked(mailMarkedList):
    file = None
    try:
        file = open('mailMarked.txt', 'w')
    except Exception:
        print('파일 쓰기 실패')
    for mark in mailMarkedList:
        file.write(mark.seriesCode + '/' + mark.name + '/' + mark.text + '\n')
    file.close()
    print('mail marked 파일 저장 완료')


def loadMailMarked():
    file = None
    try:
        file = open('mailMarked.txt', 'r')
    except Exception:
        print('mail marked 파일 읽기 실패')
        return None
    mailMarkedList = []
    readText = file.read()
    markList = readText.split('\n')
    if len(markList) > 1:
        for mark in markList:
            tmpMarked = mark.split('/')
            if len(tmpMarked) == 3:
                mailMarked = mailMark(tmpMarked[0], tmpMarked[1], tmpMarked[2])
                mailMarkedList.append(mailMarked)
    else:
        return None
    return mailMarkedList
