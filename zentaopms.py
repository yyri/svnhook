# -*- coding: utf8 -*-

import os, sys, requests, cookielib, urllib2, urllib

global cj
global opener
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPSHandler(debuglevel=1))
urllib2.install_opener(opener)

class zentaopms:
    url_base = "http://192.168.30.124/zentaopms7/www/index.php?"
    url_login = url_base + "m=user&f=login"
    url_index = url_base + "m=index&f=index&"
    url_view = url_base + "m=task&f=view&t=json&"
    # replace TASKID in url_comment and POST to the url
    url_comment = url_base + "m=[IDTYPE]&f=edit&[IDTYPE]ID=[OBJECTID]&comment=true"


    def __init__(self, taskType, idType, objectID, comment):
        self.taskType = taskType
        self.idType = idType
        self.objectID = objectID
        self.comment = comment

    # check input id existance
    def checkId(self):
        return True

    def getPostUrl(self):
        if self.taskType == "comment":
            return self.url_comment.replace("[IDTYPE]", self.idType).replace("[OBJECTID]", str(self.objectID))
        elif self.taskType == "??":
            return self.url_comment + "bugID=" + str(self.bugID)
        else:
            return ""

    def getViewUrl(self):
        if self.taskID > 0:
            return self.url_view + "taskID=" + str(self.taskID)
        elif self.bugID > 0:
            return self.url_view + "bugID=" + str(self.bugID)
        else:
            return ""


def getzentao():
    print("getzentao" + zentaopms.url_index)
    print(zentaopms(777, 999).getPostUrl())
    r = requests.get(zentaopms(430, 999).getPostUrl())
    print(r.status_code)
    print(r.content)
    print('Python is a programming language' in r.content)


def postzentao(jobtype, idtype, id, comment):
    print("postzentao")
    loginzentao()
    comment = str(comment).replace("\\n","<br>")
    post_data = urllib.urlencode({'comment': comment})
    # resp = opener.open(zentaopms.url_index)
    # print(resp.read())
    # print cj

    zentaopmsJob = zentaopms(jobtype, idtype, id, comment);
    print("job url:"+zentaopmsJob.getPostUrl())
    req = urllib2.Request(zentaopmsJob.getPostUrl(), post_data)
    resp = opener.open(req)
    print("job result:\n"+resp.read())


def loginzentao():
    # form data : account=yueyang&password=yueyang&keepLogin%5B%5D=on

    data = {"account": "SVNRobot", "password": "SVNRobot"}  # , "keepLogin[]": "on"
    post_data = urllib.urlencode(data)

    req = urllib2.Request(zentaopms.url_login, post_data)
    resp = opener.open(req)
    print(resp.read())
    print cj


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Usage: python " + sys.argv[0] + " comment|finish task|bug taskID/bugID \"Your Comment\".")
        print("Example: python " + sys.argv[0] + " comment task 1234 \"this task need more info.\"")
    else:
        for i in range(0, len(sys.argv)):
            print "Parameter[", i, "]", sys.argv[i]
        if len(sys.argv) != 5:
            print("Parameters count not match.")
            exit(0)
        elif sys.argv[1] not in {"comment", "finish"}:
            print("Wrong command. Please input \"comment|task\".")
            exit(0)
        elif sys.argv[2] not in {"task", "bug"}:
            print("Wrong type. Please input \"task|bug\".")
            exit(0)
        elif not str(sys.argv[3]).isdigit():
            print("Wrong ID. Please input a number as taskID or bugID.")
            exit(0)
        elif len(sys.argv[4]) < 1:
            print("Comment too short.")
            exit(0)
        else:
            # do login and post
            # loginzentao()
            postzentao(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
