# -*- coding: UTF-8 -*-
#!/usr/bin/python

from push_log import PushClick,PushExpo,PushData
from datetime import datetime
import time
import os

ALGORITHM_ANALYSIS_TYPE  = 1
HOUR_ANALYSIS_TYPE  = 2
ALGORITHM_HOUR_ANALYSIS_TYPE  = 3
CTR_ANALYSIS_TYPE =4
NETWORK_ANALYSIS_TYPE = 5
class Analysis(object):
    def __init__(self, action_file_name,expo_file_name,video_name_file,type):
        push_data = PushData(action_file_name,expo_file_name)
        print ("Process file sucessed")
        self.action_file_name=action_file_name
        self.expo_file_name = expo_file_name
        self.video_name_file = video_name_file
        self.type = type

    def analysis(self):
        if ALGORITHM_ANALYSIS_TYPE in self.type:
            print("Algorithm  Analysis:")
            self.algorithm_analysis()
        if HOUR_ANALYSIS_TYPE in self.type:
            print("Hour  Analysis:")
            self.time_analysis()
        if ALGORITHM_HOUR_ANALYSIS_TYPE in self.type:
            print("Time and Algorithm  Analysis:")
            self.time_algorithm_analysis()
        if CTR_ANALYSIS_TYPE in self.type:
            print("CTR  Analysis:")
            self.ctr_analysis()
        if NETWORK_ANALYSIS_TYPE in self.type:
            print("Network Analysis:")
            self.network_analysis()

    def algorithm_analysis(self):
        all_total_click_count = 0.0
        all_total_expo_count = 0.0
        tempexpo={}
        tempclick={}
        outputfile = open("0Push_AlgorithmAnalysis"+self.action_file_name[6:],'w')
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
        CTR=all_total_click_count/(all_total_expo_count + 1.0)
        print('Algo: {0}  ClickCount: {1:>4} TotalExpoCount: {2:>3}  CTR: {3:.3f}'.format(
                    "all",
                    all_total_click_count,
                    all_total_expo_count,
                    CTR
                    ))
        outputfile.write( 'all,' + str(all_total_click_count) + ',' + str(all_total_expo_count) + ',' + str(CTR) +',\n')
        outputfile.close()
        for key in tempexpo:
            if tempclick.has_key(key):
                print(key+',expo,'+str(tempexpo[key])+',click,'+str(tempclick[key]))
            else:
                print(key + ',expo,' + str(tempexpo[key]) + ',click,0' )

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
        outputfile = open("0Push_TimeAnalysis" + self.action_file_name[6:], 'w')
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
        CTR = all_total_click_count / (all_total_expo_count + 1.0)
        print('Hour: {0}  ClickCount: {1:>4} TotalExpoCount: {2:>3}  CTR: {3:.3f}'.format(
                    "all",
                    all_total_click_count,
                    all_total_expo_count,
                    CTR
                    ))
        outputfile.write('all,' + str(all_total_click_count) + ',' + str(all_total_expo_count) + ',' + str(CTR) + ',\n')
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
        CTR = total_click_count / (total_expo_count + 1.0)
        print('Network: {0}  ClickCount: {1:>4} TotalExpoCount: {2:>3}  CTR: {3:.3f}'.format(
            "all",
            total_click_count,
            total_expo_count,
            CTR
        ))

if __name__ == "__main__":
    action_file_name = "push_action20170703.txt"
    expo_file_name = "push_expo20170703.txt"
    video_name_file = "video_name20170703.txt"
    alg = Analysis(action_file_name, expo_file_name,video_name_file,[ALGORITHM_ANALYSIS_TYPE])
    #alg  = Analysis(action_file_name,expo_file_name,video_name_file,[ALGORITHM_ANALYSIS_TYPE , HOUR_ANALYSIS_TYPE ,NETWORK_ANALYSIS_TYPE, CTR_ANALYSIS_TYPE])
    #alg  = Analysis(action_file_name,expo_file_name,video_name_file,[ALGORITHM_ANALYSIS_TYPE , [ALGORITHM_HOUR_ANALYSIS_TYPE])
    alg.analysis()
    os.remove("ProPush" + action_file_name[6:])
    os.remove("ProPush" + expo_file_name[6:])
    if os.path.isfile("0Push_AlgorithmAnalysis"+action_file_name[6:]):
        os.remove("0Push_AlgorithmAnalysis"+action_file_name[6:])
    if os.path.isfile("0Push_TimeAnalysis" + action_file_name[6:]):
        os.remove("0Push_TimeAnalysis" + action_file_name[6:])