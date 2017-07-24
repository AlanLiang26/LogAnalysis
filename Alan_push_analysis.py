# -*- coding: UTF-8 -*-
#!/usr/bin/python

from push_log import PushClick,PushExpo,PushData
from datetime import datetime
import datetime
import os
import smtplib
from email.mime.text import MIMEText

ALGORITHM_ANALYSIS_TYPE  = 1
HOUR_ANALYSIS_TYPE  = 2
ALGORITHM_HOUR_ANALYSIS_TYPE  = 3
CTR_ANALYSIS_TYPE =4
NETWORK_ANALYSIS_TYPE = 5
REPEAT_ANALYSIS_TYPE=6
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

class Analysis(object):
    def __init__(self, action_file_name,expo_file_name,video_name_file,type):
        push_data = PushData(action_file_name,expo_file_name)
        print ("Process file sucessed")
        self.action_file_name=action_file_name
        self.expo_file_name = expo_file_name
        self.video_name_file = video_name_file
        self.type = type
        self.content=""

    def analysis(self):
        if ALGORITHM_ANALYSIS_TYPE in self.type:
            resultfile = open("PushResult.txt", 'a')
            resultfile.write("Algorithm  Analysis:" + '\n')
            resultfile.close()
            self.content +=( "Algorithm  Analysis:" + '\n')
            self.algorithm_analysis()
        if HOUR_ANALYSIS_TYPE in self.type:
            resultfile = open("PushResult.txt", 'a')
            resultfile.write("Hour  Analysis:" + '\n')
            resultfile.close()
            self.content += ("Hour  Analysis:" + '\n')
            self.time_analysis()
        if ALGORITHM_HOUR_ANALYSIS_TYPE in self.type:
            resultfile = open("PushResult.txt", 'a')
            resultfile.write("Time and Algorithm  Analysis:" + '\n')
            resultfile.close()
            self.time_algorithm_analysis()
        if CTR_ANALYSIS_TYPE in self.type:
            self.ctr_analysis()
        if NETWORK_ANALYSIS_TYPE in self.type:
            resultfile = open("PushResult.txt", 'a')
            resultfile.write("Network Analysis:" + '\n')
            resultfile.close()
            self.content += ("Network Analysis:" + '\n')
            self.network_analysis()
        if REPEAT_ANALYSIS_TYPE in self.type:
            resultfile = open("PushResult.txt", 'a')
            resultfile.write("Repeat Analysis:" + '\n')
            resultfile.close()
            self.content += ("Repeat Analysis:" + '\n')
            self.repeat_analysis()

    def algorithm_analysis(self):
        all_total_click_count = 0.0
        all_total_expo_count = 0.0
        tempexpo={}
        tempclick={}
        outputfile = open("PushResult.txt", 'a')
        for algo in ["recomm","other","new"]:
            total_click_count = 0.0
            total_expo_count = 0.0
            clickfile= open("ProPush"+self.action_file_name[6:],'r')
            for info in clickfile.readlines():
                click = info.split(',')
                if algo in click[16]:
                    total_click_count += 1.0
                    all_total_click_count += 1.0
                    if tempclick.has_key(click[len(click)-2]):
                        tempclick[click[len(click)-2]]+=1.0
                    else:
                        tempclick[click[len(click)-2]]=1.0
            clickfile.close()
            expofile= open("ProPush"+self.expo_file_name[6:],'r')
            for info in expofile.readlines():
                expo = info.split(',')
                if algo in expo[16]:
                    total_expo_count += 1.0
                    all_total_expo_count += 1.0
                    if tempexpo.has_key(expo[len(expo)-2]):
                        tempexpo[expo[len(expo)-2]]+=1.0
                    else:
                        tempexpo[expo[len(expo)-2]]=1.0
            expofile.close()
            CTR = total_click_count/(total_expo_count + 1.0)
            print('Algo: {0}  ClickCount: {1:.1f} TotalExpoCount: {2:.1f} CTR: {3:.3f}'.format(
                        algo,
                        total_click_count,
                        total_expo_count,
                        CTR
                        ))
            outputfile.write(algo+','+str(total_click_count)+','+str(total_expo_count)+','+str(CTR)+',\n')
            self.content+=(algo+'  ,  '+str(total_click_count)+'  ,  '+str(total_expo_count)+'  ,  '+(str(CTR))[:6]+',\n')
        CTR=all_total_click_count/(all_total_expo_count + 1.0)
        print('Algo: {0}  ClickCount: {1:>4} TotalExpoCount: {2:>3}  CTR: {3:.3f}'.format(
                    "all",
                    all_total_click_count,
                    all_total_expo_count,
                    CTR
                    ))
        outputfile.write( 'all,' + str(all_total_click_count) + ',' + str(all_total_expo_count) + ',' + str(CTR) +',\n')
        self.content +=('all  ,' + str(all_total_click_count) + '  ,  ' + str(all_total_expo_count) + '  ,  ' + (str(CTR))[:6] +',\n')
        for key in tempexpo:
            if tempclick.has_key(key):
                print(key+',expo,'+str(tempexpo[key])+',click,'+str(tempclick[key]))
                outputfile.write(key + ',' + str(tempexpo[key]) + ',' + str(tempclick[key])  + '\n')
                self.content +=(key + '  ,  ' + str(tempexpo[key]) + '  ,  ' + (str(tempclick[key]))[:6]  + '\n')
            else:
                print(key + ',expo,' + str(tempexpo[key]) + ',click,0' )
                outputfile.write(key + '  ,  ' + str(tempexpo[key]) + '  ,  0\n')
                self.content += (key + '  ,  ' + str(tempexpo[key]) + '  ,  0\n')
        outputfile.close()

    def time_algorithm_analysis(self):
        time_click_merge = {}
        time_expo_merge = {}

        for hour in range(0,24):
            time_click_merge[hour] = {}
            time_expo_merge[hour] = {}
            for algo in ["cf","tb","other"]:
                time_click_merge[hour][algo] = []
                time_expo_merge[hour][algo] = []

        for click in self.clicks:
            time_click_merge[click.action_time.tm_hour][click.algorithm].append(click)

        for expo in self.expos:
            time_expo_merge[expo.action_time.tm_hour][expo.algorithm].append(expo)

        all_total_play_time = 0.0
        all_total_click_count = 0.0
        all_total_expo_count = 0.0
        for hour in range(0,24):
            for algo in ["cf","tb","other"]:
                total_play_time = 0.0
                total_click_count = 0.0
                total_expo_count = 0.0
                for click in time_click_merge[hour][algo]:
                    if click.play_time > 200:
                        continue
                    total_play_time  += click.play_time
                    total_click_count += 1.0

                    all_total_play_time += click.play_time
                    all_total_click_count += 1.0

                for expo in time_expo_merge[hour][algo]:
                    total_expo_count += 1.0
                    all_total_expo_count += 1.0
                print('Hour: {} Algo: {} PlayTime: {:.1f} ClickCount: {:>4} TotalExpoCount: {:>3} MeanPlayTime: {:.3f} CTR: {:.3f}'.format(
                    hour,
                    algo,
                    total_play_time,
                    total_click_count,
                    total_expo_count,
                    total_play_time/(total_click_count + 1.0),
                    total_click_count/(total_expo_count + 1.0)
                    ))

        print('Hour: {} Algo: {}  PlayTime: {:.1f} ClickCount: {:>4} TotalExpoCount: {:>3} MeanPlayTime: {:.3f} CTR: {:.3f}'.format(
            "all",
            algo,
            all_total_play_time,
            all_total_click_count,
            all_total_expo_count,
            all_total_play_time/(all_total_click_count + 1.0),
            all_total_click_count/(all_total_expo_count + 1.0)
            ))

    def time_analysis(self):
        all_total_click_count = 0.0
        all_total_expo_count = 0.0
        outputfile = open("PushResult.txt", 'a')
        for hour in range(0,24):
            total_click_count = 0.0
            total_expo_count = 0.0
            clickfile = open("ProPush" + self.action_file_name[6:], 'r')
            for info in clickfile.readlines():
                click = info.split(',')
                ch=click[7].split('=')
                if ch[1] == str(hour):
                    total_click_count += 1.0
                    all_total_click_count += 1.0
            clickfile.close()
            expofile = open("ProPush" + self.expo_file_name[6:], 'r')
            for info in expofile.readlines():
                expo = info.split(',')
                eh = expo[7].split('=')
                if  eh[1] == str(hour):
                    total_expo_count += 1.0
                    all_total_expo_count += 1.0
            expofile.close()
            CTR = total_click_count/(total_expo_count + 1.0)
            print('Hour: {0}  ClickCount: {1:>4} TotalExpoCount: {2:>3}  CTR: {3:.3f}'.format(
                        hour,
                        total_click_count,
                        total_expo_count,
                        CTR
                        ))
            outputfile.write(str(hour) + ',' + str(total_click_count) + ',' + str(total_expo_count) + ',' + str(CTR) + ',\n')
            self.content+=(str(hour) + '  ,  ' + str(total_click_count) + '  ,  ' + str(total_expo_count) + '  ,  ' + (str(CTR))[:6] + ',\n')
        CTR = all_total_click_count / (all_total_expo_count + 1.0)
        print('Hour: {0}  ClickCount: {1:>4} TotalExpoCount: {2:>3}  CTR: {3:.3f}'.format(
                    "all",
                    all_total_click_count,
                    all_total_expo_count,
                    CTR
                    ))
        outputfile.write('all,' + str(all_total_click_count) + ',' + str(all_total_expo_count) + ',' + str(CTR) + ',\n')
        self.content += ('all  ,  ' + str(all_total_click_count) + '  ,  ' + str(all_total_expo_count) + '  ,  ' + (str(CTR))[:6] + ',\n')
        outputfile.close()

    def ctr_analysis(self):
        ctr_profile = {}
        profile_style= ["general_aged", "general_men", "general_women", "general_child","general_and","general_ios"]
        for ctrprofile in  profile_style:
            ctr_profile[ctrprofile]=[]
        videoname={}    #get the wid,name
        expofile = open("ProPush" + self.expo_file_name[6:], 'r')
        for info in expofile.readlines():
            expo = info.split(',')
            if expo[3] in profile_style:
                find_expo = 0
                if len(expo[15])<1:
                    continue
                if len(ctr_profile[expo[3]])<1:
                    ctr_profile[expo[3]].append([expo[15],1.0,1.0])
                    videoname[expo[15]]="NotFoundName"
                    continue
                for ctr_m in ctr_profile[expo[3]]:
                    if expo[15] == ctr_m[0]:    #该视频唯一标识符已经在该profile中存在记录并修改该记录值
                        ctr_profile[expo[3]][ctr_profile[expo[3]].index(ctr_m)][1]+=1.0     #播放次数+1
                        find_expo = 1
                        break
                if find_expo == 0:
                    ctr_profile[expo[3]].append([expo[15],1.0,0.0])     #视频唯一标识符，播放次数，点击次数
                    videoname[expo[15]]="NotFoundName"
        expofile.close()
        clickfile = open("ProPush" + self.action_file_name[6:], 'r')
        for info in clickfile.readlines():
            click = info.split(',')
            if click[3] in profile_style:
                if len(click[15])<1:
                    continue
                find_click = 0
                for ctr_m in ctr_profile[click[3]]:
                    if click[15] == ctr_m[0]:
                        ctr_profile[click[3]][ctr_profile[click[3]].index(ctr_m)][2] += 1.0  # 点击次数+1
                        find_click = 1
                        break
                #if find_click == 0:
                #   ctr_profile[click.profile].append([click.v_id, 0.0, 1.0])
        clickfile.close()
        videoname_file=open(self.video_name_file,'r')
        for log in videoname_file.readlines():
            video=log.split(',')
            if videoname.has_key(video[0]):
                videoname[video[0]]=video[1]
        videoname_file.close()
        ctr_file = open('0Push_CtrAnalysis_'+action_file_name[6:] , 'w')  # +datetime.now().date().strftime('%Y%m%d')
        for profile2 in profile_style:
            for i in ctr_profile[profile2]:
                ctr_file.write(profile2+","+i[0]+","+videoname[i[0]]+','+str(i[1])+","+str(i[2])+","+str(i[2]/i[1])+"\n") #
        ctr_file.close()

    def network_analysis(self):
        total_click_count = 0.0
        total_expo_count = 0.0
        expo_count = {}
        expofile = open("ProPush" + self.expo_file_name[6:], 'r')
        for info in expofile.readlines():
            expo = info.split(',')
            if expo_count.has_key(expo[13]):
                expo_count[expo[13]][0] += 1.0
            else:
                expo_count[expo[13]] = [1.0, 0.0]
        expofile.close()
        clickfile = open("ProPush" + self.action_file_name[6:], 'r')
        for info in clickfile.readlines():
            click = info.split(',')
            if expo_count.has_key(click[13]):
                expo_count[click[13]][1]+=1.0
        clickfile.close()
        resultfile = open("PushResult.txt", 'a')
        for key in expo_count:
            total_expo_count+=expo_count[key][0]
            total_click_count+=expo_count[key][1]
            CTR = expo_count[key][1] / expo_count[key][0]
            print('Network: {0}  ClickCount: {1:.1f} TotalExpoCount: {2:.1f} CTR: {3:.3f}'.format(
                key,
                expo_count[key][1],
                expo_count[key][0],
                CTR
                ))
            resultfile.write(key+" "+str(expo_count[key][0])+" " + str(expo_count[key][1])+" "+str(CTR)+'\n')
            self.content+=(key+"   "+str(expo_count[key][0])+"    " + str(expo_count[key][1])+"    "+ (str(CTR))[:6]+'\n')
        CTR = total_click_count / (total_expo_count + 1.0)
        print('Network: {0}  ClickCount: {1:>4} TotalExpoCount: {2:>3}  CTR: {3:.3f}'.format(
            "all",
            total_click_count,
            total_expo_count,
            CTR
        ))
        resultfile.write("all " + str(total_click_count) + " " + str(total_expo_count) + " " + str(CTR)+'\n')
        self.content+=("all   " + str(total_click_count) + "    " + str(total_expo_count) + "    " + (str(CTR))[:6] +'\n')
        resultfile.close()

    def repeat_analysis(self):
        expofile=open("ProPush" + self.expo_file_name[6:],'r')
        outputfile = open("0PushRepeat"+self.expo_file_name[6:],'w')
        pushexpo={}
        expouser=0.0
        repeatuser=0.0
        for log in expofile.readlines():
            expo = log.split(',')
            hour=expo[7].split('=')
            minute= expo[8].split('=')
            if pushexpo.has_key(expo[0]):
                findwid=0
                for wid in pushexpo[expo[0]]:
                    if expo[15] in wid and hour[1] in wid[1] and minute[1] in wid[3]:
                        wid[2]+=1.0
                        findwid=1
                        break
                if findwid == 0:
                    pushexpo[expo[0]].append([expo[15],hour[1],1.0,minute[1]])
            else:
                pushexpo[expo[0]]=[[expo[15],hour[1],1.0,minute[1]]]
        for key in pushexpo:
            expouser+=1.0
            for wid in pushexpo[key]:
                counttemp=0
                if wid[2]>1:
                    outputfile.write(key+','+wid[0]+','+wid[1]+','+wid[3]+','+str(wid[1])+',\n')
                    if counttemp == 0:
                        repeatuser+=1.0
                        counttemp=1
        print('User,'+str(expouser)+' repeatuser,'+str(repeatuser) +'  percent,'+str(repeatuser/expouser))
        resultfile = open("PushResult.txt", 'a')
        resultfile.write('User,'+str(expouser)+' repeatuser,'+str(repeatuser) +'  percent,'+str(repeatuser/expouser) + '\n')
        self.content+=('User,'+str(expouser)+' repeatuser,'+str(repeatuser) +'  percent,'+str(repeatuser/expouser) + '\n')
        resultfile.close()
        outputfile.close()
        expofile.close()

if __name__ == "__main__":
    now = datetime.datetime.now()
    todaydate = now.strftime("%Y%m%d")
    content+= str(todaydate) + "\n"
    action_file_name = "push_action"+todaydate+".txt"
    expo_file_name = "push_expo"+todaydate+".txt"
    video_name_file = "video_name"+todaydate+".txt"
    #alg = Analysis(action_file_name, expo_file_name,video_name_file,[ALGORITHM_ANALYSIS_TYPE])
    resultfile=open("PushResult.txt",'a')
    resultfile.write(str(todaydate)+'\n')
    resultfile.close()
    alg  = Analysis(action_file_name,expo_file_name,video_name_file,[ALGORITHM_ANALYSIS_TYPE , HOUR_ANALYSIS_TYPE ,NETWORK_ANALYSIS_TYPE,REPEAT_ANALYSIS_TYPE, CTR_ANALYSIS_TYPE])
    #alg  = Analysis(action_file_name,expo_file_name,video_name_file,[ALGORITHM_ANALYSIS_TYPE , [ALGORITHM_HOUR_ANALYSIS_TYPE])
    alg.analysis()
    os.remove("ProPush" + action_file_name[6:])
    os.remove("ProPush" + expo_file_name[6:])
    if os.path.isfile(action_file_name):
        os.remove(action_file_name)
    if os.path.isfile(expo_file_name):
        os.remove(expo_file_name)
    if os.path.isfile(video_name_file):
        os.remove(video_name_file)
    content += alg.content
    send_mail(mailto_list ,"PushDetail"+todaydate , content)