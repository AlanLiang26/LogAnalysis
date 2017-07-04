import time
import os
class PushClick(object):
    def __init__(self, log):
        loginfo = log.split(',')
        #print(loginfo)
        if len(loginfo) < 14:
            return
        self.sid = loginfo[1]
        if len(loginfo[2]) > 2:
            self.uid = loginfo[2]
        else:
            self.uid = "NotLoginIn"
        self.app = loginfo[3]
        self.profile = loginfo[4]
        self.action_time = time.localtime(int(loginfo[5])/1000) # time action happened
        #print(self.action_time.tm_hour)
        if loginfo[6] == "WIFI":
            self.network = loginfo[6]
        elif loginfo[6] in ["CTNET", "ctlte", "ctnet"]:
            self.network = "ChinaTelecom"
        elif loginfo[6] in ["cmnet", "cmwap"]:
            self.network = "ChineMobile"
        elif loginfo[6] in ["3gnet", "3gwap"]:
            self.network = "ChinaUnicom"
        else:
            self.network = "Else"
        self.wid = loginfo[7]
        if len(loginfo[7]) > 1:
            self.v_id = loginfo[7]
        else:
            self.v_id = "NoName"
        ctag = loginfo[11]
        self.temp=ctag
        self.algorithm = "other"
        if "fcfg" in ctag:
            self.algorithm = "recomm"
        if "new" in ctag:
            self.algorithm = "new"
        if loginfo[14] == '\n':
            self.push_time = None
        else:
            self.push_time = time.localtime(int(loginfo[14])/1000)
        ID = loginfo[7]

class PushExpo(object):
    def __init__(self, log):
        loginfo = log.split(',')
        if len(loginfo) < 14:
            self.good = False
            return
        self.good = True

        self.sid = loginfo[1]
        if len(loginfo[2]) > 2:
            self.uid = loginfo[2]
        else:
            self.uid = "NotLoginIn"

        self.app = loginfo[3]
        self.profile = loginfo[4]
        try:
            self.expo_time = time.localtime(int(loginfo[5])/1000) # time action happened
        except:
            print(loginfo)
            self.good = False
            return

        if loginfo[6] == "WIFI":
            self.network = loginfo[6]
        elif loginfo[6] in ["CTNET","ctlte","ctnet"]:
            self.network = "ChinaTelecom"
        elif loginfo[6] in ["cmnet","cmwap"]:
            self.network = "ChineMobile"
        elif loginfo[6] in ["3gnet","3gwap"]:
            self.network = "ChinaUnicom"
        else:
            self.network = "Else"
        self.wid = loginfo[7]
        if len(loginfo[10])>1:
            self.v_id = loginfo[10]
        else:
            self.v_id="NoName"
        ctag = loginfo[11]
        self.temp=ctag
        self.algorithm = "other"
        if "fcfg" in ctag:
            self.algorithm = "recomm"
        if "new" in ctag:
            self.algorithm = "new"

        if len(loginfo) < 14 or loginfo[14] == 'null\n' or loginfo[14] == '\n' :
            self.push_time = None
            self.good = False
        else:
            try:
                self.push_time = time.localtime(int(loginfo[14])/1000)
            except:
                print(loginfo)
                self.good = False

class PushData(object):
    def __init__(self, action_file_name,expo_file_name):
        self.action_file_name = action_file_name
        self.expo_file_name = expo_file_name
        self.load_click_log()
        self.load_expo_log()

    def load_click_log(self):
        if os.path.isfile("ProPush"+self.action_file_name[6:]):
            print("ProPush"+self.action_file_name[6:]+"  exited")
            return
        outputfile = open("ProPush"+self.action_file_name[6:],'w')
        action_file = open(self.action_file_name,'r')
        for info in action_file.readlines():
            c=PushClick(info)
            if len(c.uid)>1:
                outputfile.write(c.sid+','+c.uid+','+c.app+','+c.profile+','+str(c.action_time)+','+c.network+','+c.wid+','+c.v_id+','+c.algorithm+','+str(c.push_time)+','+c.temp+',\n')
        outputfile.close()
        action_file.close()

    def load_expo_log(self):
        if os.path.isfile("ProPush"+self.expo_file_name[6:]):
            print("ProPush"+self.expo_file_name[6:]+"  exited")
            return
        outputfile = open("ProPush"+self.expo_file_name[6:],'w')
        expo_file = open(self.expo_file_name,'r')
        for info in expo_file.readlines():
            c=PushExpo(info)
            if c.good == True:
                outputfile.write(c.sid + ',' + c.uid + ',' + c.app + ',' + c.profile + ',' + str(c.expo_time) + ',' + c.network + ',' + c.wid + ',' + c.v_id + ',' + c.algorithm + ',' + str(c.push_time) +','+c.temp+ ',\n')
        outputfile.close()
        expo_file.close()



