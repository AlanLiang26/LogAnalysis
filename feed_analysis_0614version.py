from feed_log_file import Click,Expo,FeedData
import datetime
#import numpy as np
#import matplotlib.pyplot as plt
import gc
import os
import smtplib
from email.mime.text import MIMEText

ALGORITHM_ANALYSIS_TYPE  = 1
HOUR_ANALYSIS_TYPE  = 2
ALGORITHM_HOUR_ANALYSIS_TYPE  = 3
VERSION_ANALYSIS_TYPE = 4
ITEM_ANALYSIS_TYPE = 5
TOPIC_ANALYSIS_TYPT =6
FEED_ALGORITHMS = ["cf","tb","igqbp","other","ldacf"]
mailto_list=['liangyalun@waquer.com']
content=""
def send_mail(to_list,sub,content):
    me = "alanwaqu@163.com"
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect("smtp.163.com")
        server.login("alanwaqu@163.com","waqushiping666")
        server.sendmail(me,to_list,msg.as_string())
        server.close()
    except Exception,e:
        print str(e)
class USER(object):
    def __init__(self,uid,wid):
        self.uid = uid
        self.wids = []
        self.wids.append([wid,1.0])
    def appendwids(self,wid):
        self.wids.append([wid , 1.0])

    def counts(self,wid):
        count = 0
        for wid1 in self.wids:
            if wid in wid1:
                self.wids[count][1] += 1.0
                break
            else:
                count += 1

class ITEM(object):
    def __init__(self,wid,uid):
        self.wid = wid
        self.uids = []
        self.uids.append([uid,1.0])
    def appenduids(self,uid):
        self.uids.append([uid , 1.0])

    def counts(self,uid):
        count = 0
        TF = 0
        for uid1 in self.uids:
            if uid in uid1:
                self.uids[count][1] += 1.0
                TF = 1
                break
            else:
                count += 1
        if TF == 0:
            self.uids.append([uid,1.0])

class Analysis(object):
    def __init__(self, action_file_name,expo_file_name,header_file_name,type):
        self.feed_data = FeedData(action_file_name,expo_file_name,header_file_name,type)
        self.type = type
        self.action_file_name = action_file_name
        self.expo_file_name = expo_file_name
        self.header_file_name = header_file_name
        self.content=""
        print('Read file finish')

    def analysis(self):
        if ALGORITHM_ANALYSIS_TYPE in self.type:
            self.content+=("Algorithm_analysis\n")
            self.algorithm_analysis()
        if VERSION_ANALYSIS_TYPE in self.type:
            self.version_analysis()
        if ITEM_ANALYSIS_TYPE in self.type:
            self.item_analysis()
        if TOPIC_ANALYSIS_TYPT in self.type:
            #self.content += ("Topic_analysis\n")
            self.topic_analysis()

    def MergeSort(self,lists):
        if len(lists) <=1:
            return lists
        num = int(len(lists) / 2)
        left = self.MergeSort(lists[:num])
        right = self.MergeSort(lists[num:])
        return self.Merge(left, right)

    def Merge(self, left, right):
        r, l = 0, 0
        result = []
        while l < len(left) and r < len(right):
            if left[l].wid < right[r].wid:
                result.append(left[l])
                l += 1
            else:
                result.append(right[r])
                r += 1
        result += right[r:]
        result += left[l:]
        return result

    def algorithm_analysis(self):
        total_play_time = {"cf":0.0,"tb":0.0,"igqbp":0.0,"other":0.0,"ldacf":0.0}
        total_click_count = {"cf":0.0,"tb":0.0,"igqbp":0.0,"other":0.0,"ldacf":0.0}
        total_expo_count = {"cf":0.0,"tb":0.0,"igqbp":0.0,"other":0.0,"ldacf":0.0}
        all_total_play_time = 0.0
        all_total_click_count = 0.0
        all_total_expo_count = 0.0
        # PGC
        #pgcwidlist={}
        #tempfile = open("pgcvideo_widlist.txt",'r')
        # for tlog in tempfile.readlines():
        #     temp=tlog.split(',')
        #     n=len(temp[0])-1
        #     wid =temp[0][:n]
        #     pgcwidlist[wid]=1.0
        algoclickfile = open("ClickPro" + self.action_file_name[10:], 'r')
        for log in algoclickfile.readlines():
            click = log.split(',')
            #if pgcwidlist.has_key(click[6]):
            total_play_time[click[1]]+=float(click[0])
            total_click_count[click[1]] += 1.0
        algoclickfile.close()

        algoExpofile = open("ExpoPro" + self.expo_file_name[10:], 'r')
        for readlog in algoExpofile.readlines():
            log = readlog.split(',')
            #if pgcwidlist.has_key(log[2]):
            if log[0] in FEED_ALGORITHMS:
                total_expo_count[log[0]] += 1.0
        algoExpofile.close()

        for algo in FEED_ALGORITHMS:
            all_total_play_time += total_play_time[algo]
            all_total_click_count += total_click_count[algo]
            all_total_expo_count += total_expo_count[algo]

        feed_file = open('1FeedRult', 'a')
        now = datetime.datetime.now()
        todaydate = now.strftime("%Y%m%d")
        feed_file.write(str(todaydate) + '\n')
        for algo in FEED_ALGORITHMS:
            MeanPlayTime = total_play_time[algo] / (total_click_count[algo] + 1.0)
            CTR = total_click_count[algo] / (total_expo_count[algo] + 1.0)
            print('Algo: {0} PlayTime: {1:.1f} ClickCount: {2:.1f} TotalExpoCount: {3:.1f} MeanPlayTime: {4:.3f} CTR: {5:.3f}'.format(
            algo,
            total_play_time[algo],
            total_click_count[algo],
            total_expo_count[algo],
            MeanPlayTime,
            CTR
            ))
            feed_file.write(algo + "," + str(total_play_time[algo]) + "," + str(total_click_count[algo]) + "," + str(total_expo_count[algo]) + "," + str(MeanPlayTime) + "," + str(CTR) + "\n")
            self.content+=(algo + " , " + str(total_play_time[algo]) + " , " + str(total_click_count[algo]) + " , " + str(total_expo_count[algo]) + " , " + str(MeanPlayTime) + " , " + str(CTR) + "\n")
        MeanPlayTime = all_total_play_time / (all_total_click_count + 1.0)
        CTR = all_total_click_count / (all_total_expo_count + 1.0)
        print('Algo: {0} PlayTime: {1:.1f} ClickCount: {2:.1f} TotalExpoCount: {3:.1f} MeanPlayTime: {4:.3f} CTR: {5:.3f}'.format(
        "all",
        all_total_play_time,
        all_total_click_count,
        all_total_expo_count,
        MeanPlayTime,
        CTR
        ))
        feed_file.write("all," + str(all_total_play_time) + "," + str(all_total_click_count) + "," + str(all_total_expo_count) + "," +  str(MeanPlayTime) + "," + str(CTR) + '\n')
        self.content+=("all , " + str(all_total_play_time) + " , " + str(all_total_click_count) + " , " + str(all_total_expo_count) + " , " +  str(MeanPlayTime) + " , " + str(CTR) + '\n')
        feed_file.close()

    def version_analysis(self):
        verprintfile = open("Versionall" + self.action_file_name[10:], 'w')
        for appv in ["5.0.5","5.0.6","5.0.7","other"]:
            total_play_time = {"cf": 0.0, "tb": 0.0, "igqbp": 0.0, "other": 0.0, "ldacf": 0.0}
            total_click_count = {"cf": 0.0, "tb": 0.0, "igqbp": 0.0, "other": 0.0, "ldacf": 0.0}
            total_expo_count = {"cf": 0.0, "tb": 0.0, "igqbp": 0.0, "other": 0.0, "ldacf": 0.0}
            all_total_play_time = 0.0
            all_total_click_count = 0.0
            all_total_expo_count = 0.0

            #read  click file and count
            clickversionfile = open("Version" + self.action_file_name[10:], 'r')
            for log in clickversionfile.readlines():
                click = log.split(',')
                if click[4] in appv:
                    if click[5] in FEED_ALGORITHMS:
                        total_play_time[click[5]] += float(click[0])
                        total_click_count[click[5]] += 1.0
            clickversionfile.close()

            #read expo file and count
            expoversionfile = open("Version"+self.expo_file_name[10:], 'r')
            for log in expoversionfile.readlines():
                expo=log.split(',')
                if expo[3] in appv:
                    if expo[4] in FEED_ALGORITHMS:
                        total_expo_count[expo[4]] += 1.0
            expoversionfile.close()
            #print
            print(appv)
            verprintfile.write(appv+'\n')
            for algo in FEED_ALGORITHMS:
                MeanPlayTime = total_play_time[algo] / (total_click_count[algo] + 1.0)
                CTR = total_click_count[algo] / (total_expo_count[algo] + 1.0)
                print('Algo: {0} PlayTime: {1:.1f} ClickCount: {2:.1f} TotalExpoCount: {3:.1f} MeanPlayTime: {4:.4f} CTR: {5:.4f}'.format(
                    algo,
                    total_play_time[algo],
                    total_click_count[algo],
                    total_expo_count[algo],
                    MeanPlayTime,
                    CTR
                ))
                verprintfile.write(algo + "," + str(total_play_time[algo]) + "," + str(total_click_count[algo]) + "," + str(total_expo_count[algo]) + "," + str(MeanPlayTime) + "," + str(CTR) + "\n")
            for algo in FEED_ALGORITHMS:
                all_total_click_count+=total_click_count[algo]
                all_total_expo_count+=total_expo_count[algo]
                all_total_play_time+=total_play_time[algo]
            MeanPlayTime = all_total_play_time / (all_total_click_count + 1.0)
            CTR = all_total_click_count / (all_total_expo_count + 1.0)
            print('Algo: {0} PlayTime: {1:.1f} ClickCount: {2:.1f} TotalExpoCount: {3:.1f} MeanPlayTime: {4:.4f} CTR: {5:.4f}'.format(
                "all",
                all_total_play_time,
                all_total_click_count,
                all_total_expo_count,
                MeanPlayTime,
                CTR
            ))
            verprintfile.write("all:" + str(all_total_play_time) + "," + str(all_total_click_count) + "," + str(all_total_expo_count) + "," + str(MeanPlayTime) + "," + str(CTR) + '\n')
            del total_expo_count
            del total_click_count
            del total_play_time
        verprintfile.close()

    def item_analysis(self):
        #read file
        algoExpofile = open("ExpoPro" + self.expo_file_name[10:], 'r')
        #counttest = 0                                                        #for test
        itemfirst = []
        itemsfile = {}
        firstlist = '1234567890qwertyuiopasdfghjklzxcvbnm'
        for i in range(0,len(firstlist)):
            itemfirst.append(firstlist[i])
            itemsfile[firstlist[i]] = open(firstlist[i] + self.expo_file_name[10:],'w')
        for readlog in algoExpofile.readlines():
            log = readlog.split(',')
            if log[1] != "null":
                itemsfile[log[2][0]].write(log[2] + ',' +log[1] + ',' + '\n')
        for fn in itemfirst:
            itemsfile[fn].close()
            # counttest += 1                                                      #for test
            # if counttest >1000:                                                #for test
            #      break                                                         #for test
        algoExpofile.close()
        print('Read temp file  finished')

        #count user num
        itemfile = open("Item" + self.expo_file_name[10:], 'w')
        baditemfile = open("BadItem" + self.expo_file_name[10:],'w')
        itemfile.write(self.expo_file_name + '\n')
        baditemfile.write(self.expo_file_name + '\n')
        fnitemsfile = {}
        for fn in itemfirst:
            fnitemsfile[fn] = open(fn + self.expo_file_name[10:] , 'r' )
        countmultiple = 0
        baditemcount = 0
        itemcount = 0
        for fn in itemfirst:
            items = []
            for readlog in fnitemsfile[fn].readlines():
                log = readlog.split(',')
                items.append(ITEM(log[0],log[1]))
            #sort
            fnitemsfile[fn].close()
            os.remove(fn + self.expo_file_name[10:])
            tempitems = self.MergeSort(items)[:]
            del items
            items = tempitems[:]
            del tempitems
            print(fn + ' sort finished')
            #combine the same wid and count the users
            if len(items)>1:
                for i in range(0,len(items)-1):
                     for j in range(i , len(items)-1):
                        k = len(items) - 1
                        if i == k:
                            break
                        elif items[i].wid == items[i+1].wid:
                            items[i].counts(items[i+1].uids[0][0])
                            del items[i+1]
                            continue
                        else:
                            break
            # printfile
            for item in items:
                itemcount += 1
                widprint = 0
                badwidprint = 0
                for uid in item.uids:
                    if uid[1] > 1.0:
                        if widprint == 0:
                            itemfile.write(item.wid + ',')
                            widprint = 1
                            countmultiple += 1
                        itemfile.write(uid[0] + ',' + str(uid[1]) + ',')
                        if uid[1]>2.0:
                            if badwidprint == 0:
                                baditemfile.write(item.wid + ',')
                                badwidprint = 1
                                baditemcount +=1
                            baditemfile.write(uid[0] + ',' + str(uid[1]) + ',')
                if widprint == 1:
                    itemfile.write('\n')
                if badwidprint == 1:
                    baditemfile.write('\n')
            del items
        print('ItemTotal, '+str(itemcount) + ',')
        print( 'MultipleExpo ItemTotal ,'+str(countmultiple))
        print('BadItemCount,' + str(baditemcount))
        itemfile.write(str(itemcount) + ' , ' + str(countmultiple))
        baditemfile.write(str(itemcount) + ' , ' + str(baditemcount))
        itemfile.close()
        baditemfile.close()

    def topic_analysis(self):
        topicfile = open("topic_name.txt",'r')
        topicname={}
        for log in topicfile.readlines():
            topicmes = log.split(',')
            topicname[topicmes[0]]=topicmes[1]
        topicfile.close()
        outputfile = open("Topic" + self.action_file_name[10:], 'w')
        for algo in FEED_ALGORITHMS:
            play_time = {}
            click_count = {}
            expo_count = {}
            clickfile = open("ClickPro" + self.action_file_name[10:], 'r')
            for log in clickfile.readlines():
                click = log.split(',')
                if click[1] in algo:
                    if len(click[5])<0:
                        continue
                    if play_time.has_key(click[5]):
                        play_time[click[5]]+=float(click[0])
                    else:
                        play_time[click[5]]=float(click[0])
                    if click_count.has_key(click[5]):
                        click_count[click[5]]+=1.0
                    else:
                        click_count[click[5]]=1.0
            clickfile.close()

            expofile = open("ExpoPro" + self.expo_file_name[10:], 'r')
            for log in expofile.readlines():
                expo = log.split(',')
                if expo[0] in algo:
                    if len(expo[6])<0:
                        continue
                    if expo_count.has_key(expo[6]):
                        expo_count[expo[6]]+=1.0
                    else:
                        expo_count[expo[6]] = 1.0
            expofile.close()

            for key,value in expo_count.items():
                if click_count.has_key(key):
                    meanpt= float(play_time[key])/float(click_count[key])
                    ctr = float(click_count[key])/float(expo_count[key])
                    if topicname.has_key(key):
                        outputfile.write(algo+','+key+','+str(play_time[key])+','+str(click_count[key])+','+str(expo_count[key])+','+str(meanpt)+','+str(ctr)+','+topicname[key])
                        #self.content+=(algo+','+key+','+str(play_time[key])+','+str(click_count[key])+','+str(expo_count[key])+','+str(meanpt)+','+str(ctr)+','+topicname[key])
                    else:
                        outputfile.write(algo+','+key+','+str(play_time[key])+','+str(click_count[key])+','+str(expo_count[key])+','+str(meanpt) + ',' + str(ctr) + ',NoName,\n')
                        #self.content+=(algo+','+key+','+str(play_time[key])+','+str(click_count[key])+','+str(expo_count[key])+','+str(meanpt) + ',' + str(ctr) + ',NoName,\n')
            print(algo+"   finished")
        outputfile.close()
        print("all Finished")

if __name__ == "__main__":
    now=datetime.datetime.now()
    todaydate=now.strftime("%Y%m%d")
    content += str(todaydate) + "\n"
    action_file_name = "recom_feed_action"+todaydate+".txt"
    expo_file_name = "recom_feed_expo"+todaydate+".txt"
    header_file_name = "recom_feed_header"+todaydate+".txt"
    alg = Analysis(action_file_name, expo_file_name, header_file_name, [ALGORITHM_ANALYSIS_TYPE])
    #alg = Analysis(action_file_name, expo_file_name,header_file_name, [ALGORITHM_ANALYSIS_TYPE])
    #alg = Analysis(action_file_name, expo_file_name,header_file_name, [VERSION_ANALYSIS_TYPE])
    #alg = Analysis(action_file_name, expo_file_name,header_file_name, [ITEM_ANALYSIS_TYPE])
    alg.analysis()
    if os.path.isfile("ClickPro" + action_file_name[10:]):
        os.remove("ClickPro" + action_file_name[10:])
    if os.path.isfile("ExpoPro" + expo_file_name[10:]):
        os.remove("ExpoPro" + expo_file_name[10:])
    if os.path.isfile(action_file_name):
        os.remove(action_file_name)
    if os.path.isfile(expo_file_name):
        os.remove(expo_file_name)
    if os.path.isfile(header_file_name):
        os.remove(header_file_name)
    content += alg.content
    send_mail(mailto_list, "FeedDetail" + todaydate, content)
