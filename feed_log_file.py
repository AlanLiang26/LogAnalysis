import time
import os
class Click(object):
    def __init__(self, log ):
        loginfo = log.split(',')
        self.algorithm = "no"   #avoid bug for line 122
        self.play_time = 0.0
        if len(loginfo) <= 0:
            return
        if len(loginfo[5]) <= 0: #alan
            return       #alan
        if "child"in loginfo[3]:
            return

        #time server get this info
        #self.server_time = time.localtime(loginfo[0]/1000)
        self.servertime = loginfo[0]
        self.sid = loginfo[1]
        if len(loginfo[2]) > 2:
            self.uid = loginfo[2]
        else:
            self.uid = self.sid

        self.app = loginfo[3]
        self.profile = loginfo[4]
        #self.action_time = time.localtime(int((loginfo[5]))/1000) # time action happened  #alan float()
        #print(self.action_time.tm_hour)
        self.network = loginfo[6]
        self.wid = loginfo[7]
        if len(loginfo[8])>0:
            self.tid = loginfo[8] #topic id
        else:
            self.tid = "NoTopic"

        self.play_time = float(loginfo[9])/(1000*60) # play time for minitue
        ctag = loginfo[12]
        self.algorithm = "other"
        if "vhcf" in ctag:
            self.algorithm = "cf"
        elif "tb" in ctag:
            self.algorithm = "tb"
        elif "igqbp" in ctag:
            self.algorithm = "igqbp"
        elif "ldacf" in ctag:
            self.algorithm = "ldacf"
        else:
            #print(loginfo)
            self.algorithm = "other"

class Expo(object):
    def __init__(self, servertime,sid,uid, app, profile, action_time, network, wid, algorithm,tid):
        self.servertime = servertime
        self.sid = sid
        self.uid = uid
        self.app = app
        self.profile = profile
        self.action_time = action_time
        self.network = network
        self.algorithm = algorithm
        self.wid = wid
        self.tid = tid   #0621

class FeedData(object):
    def __init__(self, action_file_name,expo_file_name,header_file_name,ty):
        self.action_file_name = action_file_name
        self.expo_file_name = expo_file_name
        self.header_file_name = header_file_name
        self.type = type
        #self.expos = []
        if 5 not in ty:
            self.load_click_log()
        self.load_expo_log()
        if 4 in ty:
            self.appvadd()

    def appvadd(self):
        if os.path.isfile("Version" + self.action_file_name[10:]):
            print ("appv added file existed\n")
            return
        sids = {}
        # select the sid in headerfile where sid in expofile sids
        header_file = open(self.header_file_name, 'r')
        for info1 in header_file.readlines():
            info = info1.split(',')
            if len(info[1]) < 1:
                continue
            sids[info[1]] = info[3][:5]
        header_file.close()

        algoclickfile = open("ClickPro" + self.action_file_name[10:], 'r')
        clickversionfile = open("Version" + self.action_file_name[10:], 'w')
        algoExpofile = open("ExpoPro" + self.expo_file_name[10:], 'r')
        expoversionfile = open("Version" + self.expo_file_name[10:], 'w')
        for info in algoclickfile.readlines():
            cinfo = info.split(',')
            if sids.has_key(cinfo[3]):
                if sids[cinfo[3]] in ["5.0.5", "5.0.6", "5.0.7"]:
                    clickversionfile.write(cinfo[0] +','+cinfo[2] + ','+cinfo[3]+','+cinfo[4]+','+sids[cinfo[3]]+',' + cinfo[1]+',\n')
                else:
                    clickversionfile.write(cinfo[0] + ',' + cinfo[2] + ',' + cinfo[3] + ',' + cinfo[4] + ',other,' +cinfo[1] + ',\n')
        for info in algoExpofile.readlines():
            einfo = info.split(',')
            if sids.has_key(einfo[4]):
                if sids[einfo[4]] in ["5.0.5", "5.0.6", "5.0.7"]:
                    expoversionfile.write(einfo[3] + ',' + einfo[4]+','+einfo[5]+','+sids[einfo[4]]+','+einfo[0]+',\n')
                else:
                    expoversionfile.write(einfo[3] + ',' + einfo[4] + ',' + einfo[5] + ',other,' + einfo[0] + ',\n')
        clickversionfile.close()
        algoclickfile.close()
        algoExpofile.close()
        expoversionfile.close()
        print("add version sucessed")

    def load_click_log(self):
        if os.path.isfile("ClickPro"+self.action_file_name[10:]):
            print("ClickPro"+self.action_file_name[10:]+"  exited")
            return
        algoclickfile = open("ClickPro"+self.action_file_name[10:],'w')
        action_file = open(self.action_file_name, 'r')
        for info in action_file.readlines():
            clicks = Click(info)
            if clicks.algorithm in ["cf","tb","igqbp","other","ldacf"]:
                if clicks.play_time <200:
                    playtime=str(clicks.play_time)
                    algoclickfile.write(playtime+','+clicks.algorithm + ',' + clicks.servertime +','+clicks.sid + ',' + clicks.app +','+clicks.tid+','+clicks.wid+",\n") #clicks.uid + ',' + clicks.app + ',' + clicks.profile + ','  + clicks.network+','+clicks.wid+','+clicks.tid+','+clicks.action_time + ','
        print(self.action_file_name+" Finished")
        action_file.close()
        algoclickfile.close()

    def load_expo_log(self):
        expo_file = open(self.expo_file_name,'r')
        if os.path.isfile("ExpoPro"+self.expo_file_name[10:]):
            print("ExpoPro" + self.expo_file_name[10:] + "  exited")
            return
        algoExpofile = open("ExpoPro" + self.expo_file_name[10:],'w')
        for info in expo_file.readlines():
            expos = []
            for expo in self.process_expo(info):
                expos.append(expo)
            if len(expos)>0 :
                for expo in expos:
                    if len(expo.algorithm) <1:
                        continue
                    if expo.algorithm in ["cf","tb","igqbp","other","ldacf"]:
                        algoExpofile.write(expo.algorithm + "," + expo.uid + ','+ expo.wid + ',' +expo.servertime +','+ expo.sid + ',' + expo.app+',' +expo.tid+',' +  ",\n")  # expo.profile+','+expo.network+','+expo.wid+','+expo.action_time+','
            del expos
        print(self.expo_file_name+" Finished")
        expo_file.close()
        algoExpofile.close()

    def process_expo(self,log):
        loginfo = log.split(',')
        expor = []
        expoR = Expo('servertime','sid','uid','app','profile','action_time','network','wid','n','tid')   #none
        expor.append(expoR)
        if len(loginfo) <= 9:
            return expor
        if len(loginfo[5])<=0:    #alan avoid bug when time is empty,line 79
            return expor               #alan
        if len(loginfo[10])<=0:
            return  expor
        servertime = loginfo[0]
        sid = loginfo[1]
        if len(loginfo[2]) > 2:
            uid = loginfo[2]
        else:
            uid = sid

        app = loginfo[3]
        profile = loginfo[4]
        action_time = time.localtime(int(loginfo[5])/1000) # time action happened
        network = loginfo[6]
        expo_info = loginfo[7]
        if len(loginfo[10])>0:
            tids_info = loginfo[10]        #621
            tids = tids_info.split('~')    #621
        else:
            tids=["NoTopic"]
        tis_id = 0                 #621
        expos = []
        expos.append(expoR)
        for expo in expo_info.split('~'):
            if "NoTopic" in tids[0]:
                tid = tids[0]
            elif len(tids[tis_id])<1:
                tid = "NoTopic"
                tis_id += 1
            else:
                tid = tids[tis_id]    #621
                tis_id +=1        #621
            if tis_id>(len(tids)-1):
                break
            video_info = expo.split("#")
            if len(video_info) <= 2:
                continue
            wid = video_info[0]

            ctag = video_info[2]
            if "ctag" in video_info[1]:
                ctag = video_info[1]

            if "vhcf" in ctag:
                algorithm = "cf"
            elif "tb" in ctag:
                algorithm = "tb"
            elif "igqbp" in ctag:
                algorithm = "igqbp"
            elif "ldacf" in ctag:
                algorithm = "ldacf"
            else:
                algorithm = "other"
            if not "child" in app:
                expos.append(Expo(servertime,sid,uid,app,profile,action_time,network,wid,algorithm,tid))
        return expos



