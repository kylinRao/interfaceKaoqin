# coding=utf-8
import requests
import json

import sys

reload(sys)

sys.setdefaultencoding('utf8')
import time

sys.path.append("..")
from conf.logControl import logControl
def time_cmp(first_time, second_time):
    print """ time.strftime("%H%M%S", {first_time})) - int(time.strftime("%H%M%S", {second_time})  """.format(first_time=first_time,second_time=second_time)
    print '{a} - {b}'.format(a=int(time.strftime("%H%M%S", first_time)),b=int(time.strftime("%H%M%S", second_time)))
    return (int(time.strftime("%H%M%S", first_time)) - int(time.strftime("%H%M%S", second_time)))

class interfaceKaoqin():
    loginOaUrl = "http://ics.chinasoftosg.com/login"
    loginChangeSession = "http://kq.chinasoftosg.com/workAttendance/encryptionAction_getCodeEncry"
    loginKaoqinUrl = "http://kq.chinasoftosg.com/workAttendance/loginAction"
    getKaoQinUrl = "http://kq.chinasoftosg.com/workAttendance/importsExamineAction_getImportsExamine"
    logoutOaUrl = "http://ics.chinasoftosg.com/logout"
    logger = logControl().getLogger()
    session = requests.Session()

    def __init__(self, userName, passWord):
        self.nowDate = time.strftime("%Y-%m")
        self.userName = userName
        self.passWord = passWord


    def loginOa(self):
        data = {'userid': self.userName, 'linkpage': '', 'userName': self.userName, 'j_username': self.userName,
                'password': self.passWord, 'j_password': self.passWord}
        r = self.session.post(url=self.loginOaUrl, data=data)
        self.logger.debug("登陆结果：")
        self.logger.debug(r)
        self.logger.debug(r.text)

        return

    def loginKaoQinXT(self):
        self.loginOa()
        pram = {"callbackparam": "success_jsonpCallback", "lobNumber": "00000" + self.userName}
        self.session.get(url=self.loginChangeSession, params=pram)
        self.session.get(url=self.loginKaoqinUrl)

    def getKaoqinData(self):
        self.loginKaoQinXT()
        data = {"importsExamineVo.page": "1", "importsExamineVo.pagesize": "25"}
        r = self.session.post(url=self.getKaoQinUrl, data=data)
        self.logger.debug("近期考勤结果：")
        self.logger.debug(r)
        self.logger.debug(r.text)
        res_value = r.json()

        # d1 = json.dumps(res_value,ensure_ascii=False, indent=4)
        kqList = res_value['Rows']
        for item in kqList:
            if (time_cmp(time.strptime( item["showBeginTime"],"%H:%M"), time.strptime( "09:00","%H:%M"))>0) or (time_cmp(time.strptime( "17:30","%H:%M"), time.strptime(item['showEndTime'],"%H:%M"))>0):
                item['showRecordDate'] = "【异常请留意】："+item['showRecordDate']
            # print item,len(kqList)
            # print self.nowDate,"----",item['showRecordDate']
            # if   (self.nowDate) in item['showRecordDate'] :
            #     if (time_cmp(time.strptime( item["showBeginTime"],"%H:%M"), time.strptime( "09:00","%H:%M"))>0) or (time_cmp(time.strptime( "17:30","%H:%M"), time.strptime(item['showEndTime'],"%H:%M"))>0):
            #         item['showRecordDate'] = "【异常请留意】："+item['showRecordDate']
            # #
            # else:
            #     print "remove",item['showRecordDate']
            #     kqList.remove(item)



        return kqList

    def logoutOa(self):
        r = self.session.get(url=self.logoutOaUrl)
        self.logger.debug("退出登录结果：")
        self.logger.debug(r)
        self.logger.debug(r.text)
        return


if __name__ == '__main__':
    rao = interfaceKaoqin(userName='68104', passWord="Rql*34704");
    res = rao.getKaoqinData()
    for kq in res:
        print kq['showRecordDate'], kq['showBeginTime'], kq['showEndTime'], kq['lastName']
