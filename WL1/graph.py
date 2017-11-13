from collections import defaultdict
import pandas as pd
import numpy as np
import itertools
import sys
import bisect
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as cl
import matplotlib.pyplot as pl
import matplotlib.patches as mpatches


def color_maker(count, map='gnuplot2', min=0.100, max=0.900):
     assert(min >= 0.000 and max <= 1.000 and max > min)
     gran=100000.0
     maker = cmx.ScalarMappable(norm=cl.Normalize(vmin=0, vmax=int(gran)), cmap=pl.get_cmap(map))

     r = [min*gran]
     if count > 1:
         r = [min*gran + gran*x*(max-min)/float(count-1) for x in range(0, count)]

     return [maker.to_rgba(t) for t in r]


def add_line(ax, xpos, ypos):
    line = plt.Line2D([xpos, xpos], [ypos + .1, ypos - .1], transform=ax.transAxes, linewidth=1.2, color='black')
    line.set_clip_on(False)
    ax.add_line(line)

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%.2f'%float(height))

#WL1
##user1           = userobj.UserInfo(2500, 43,'PPBBCC','user1')
##list_users.append(user1)
##
##user2       = userobj.UserInfo(1200, 40,'EEFF', 'user2')
##list_users.append(user2)
##
##user3       = userobj.UserInfo(1900, 35,'DDBBCC', 'user3')
##list_users.append(user3)
##
##user4       = userobj.UserInfo(1300, 74,'GGDDEEFF', 'user4')
##list_users.append(user4)
parse_files = [  'ed.txt',  'swd.txt',  'tt-1.txt',  'tt-30.txt', 'tt-50.txt',  'tt-dynbatch.txt', 'gs.txt' ]
xticks = ['Equal \n Division', 'Static Weighted \n Division', 'Time Trader \n no batch',  'Time Trader \n batchsize 30',  'Time Trader \n batchsize 50',  'Time Trader \n dynamic batch', 'GrandSlam']
ylim=6000

final_list = []
final_list2 = []
final_err_list2 = []
for fl in parse_files:
    print fl
    avg_list = []
    tail_list = []

    list_1  = []
    list_12 = []
    list_2  = []
    list_23 = []
    list_3  = []
    list_34  = []
    list_err  = []
    fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/isca-results/5.stacked-bar/grand-slam-sla/WL1/%s' %fl).readlines()]
    max_tail = 0
    data = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
    data_1 = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
    data_12 = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
    data_2 = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
    data_23 = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
    data_3 = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
    data_34 = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
    for item in fList:
        if 'PP' in item and 'user1' in item:
            list_1.append(float(item.split()[4]))
            list_12.append(float(item.split()[5]))
            data[item.split()[0]][item.split()[1]][item.split()[2]]= item.split()[7]
        if 'BB' in item  and 'user1' in item:
            list_2.append(float(item.split()[4]))
            list_23.append(float(item.split()[5]))
            data[item.split()[0]][item.split()[1]][item.split()[2]]= item.split()[7]
        if 'CC' in item and 'user1' in item:
            list_3.append(float(item.split()[4]))
            list_34.append(float(item.split()[5]))
            list_err.append(float(item.split()[7]))
            data[item.split()[0]][item.split()[1]][item.split()[2]]= item.split()[7]

    for item in data:
        if 'CC' in item:
            temp_list = []
            temp_idx = []
            for idx, ele in enumerate(data[item]['user1']):
                temp_list.append(float(data[item]['user1'][ele]))
                temp_idx.append(ele)
            #print max(temp_list), temp_list.index(max(temp_list))
            #print data[item]['user1'][temp_idx[temp_list.index(max(temp_list))]]
            a = item
            b = 'user1'
            c = temp_idx[temp_list.index(max(temp_list))]

    tail_list.append(list_12[int(c)-1])
    tail_list.append(list_1[int(c)-1])
    tail_list.append(list_23[int(c)-1])
    tail_list.append(list_2[int(c)-1])
    tail_list.append(list_34[int(c)-1])
    tail_list.append(list_3[int(c)-1])

    #print list_err
    #print np.std(list_err)
    final_err_list2.append(np.std(list_err))
    avg_list.append(np.mean(list_12))
    avg_list.append(np.mean(list_1))
    avg_list.append(np.mean(list_23))
    avg_list.append(np.mean(list_2))
    avg_list.append(np.mean(list_34))
    avg_list.append(np.mean(list_3))


    #print avg_list
    #print tail_list
    final_list.append(avg_list)
    final_list2.append(tail_list)
color_list = color_maker(10, map="afmhot")
#print final_err_list2

avg_list = []
tail_list = []

avg_list =  map(list, zip(*final_list))
tail_list =  map(list, zip(*final_list2))

print map(sum, zip(*avg_list))
print map(sum, zip(*tail_list))

#15735.267799605968, 13849.623439140854, 13897.656152319147
#22731.295585588367, 18826.555013618367, 18826.555013618367

#print final_list
fig  = plt.figure(figsize=(12, 3))
ax = fig.add_subplot(1,1,1)
width=0.25

plt.text(-0.05, 6300, r'15735', rotation='0', fontsize=8)
plt.text(0.28, 6300, r'22731', rotation='0', fontsize=8)


plt.text(0.97, 6300, r'13849',  rotation='0', fontsize=8)
plt.text(1.28, 6300, r'18826',  rotation='0', fontsize=8)

plt.text(1.97, 6300, r'13897',  rotation='0', fontsize=8)
plt.text(2.28, 6300, r'18826',  rotation='0', fontsize=8)

#print tail_list
ax1 = plt.bar(np.arange(len(avg_list[0])),avg_list[0] , width, color=color_list[0])
ax2 = plt.bar(width+np.arange(len(tail_list[0])),tail_list[0] , width, color=color_list[0])

ax1 = plt.bar(np.arange(len(avg_list[1])),avg_list[1] ,  width, bottom=map(sum, zip(avg_list[0])), color=color_list[5])
ax2 = plt.bar(width+np.arange(len(tail_list[1])), tail_list[1] ,  width, bottom=map(sum, zip(tail_list[0])), color=color_list[5])

ax1 = plt.bar(np.arange(len(avg_list[2])),avg_list[2] ,  width, bottom=map(sum, zip(avg_list[0], \
        avg_list[1])), color=color_list[2])
ax2 = plt.bar(width+np.arange(len(tail_list[1])),tail_list[1] ,  width, bottom=map(sum, zip(tail_list[0])), color=color_list[5])

ax1 = plt.bar(np.arange(len(avg_list[3])),avg_list[3] ,  width, bottom=map(sum, zip(avg_list[0],\
        avg_list[1], avg_list[2] )), color=color_list[7])
ax2 = plt.bar(width+np.arange(len(tail_list[3])),tail_list[3] ,  width, bottom=map(sum, zip(tail_list[0],\
       tail_list[1], tail_list[2] )), color=color_list[7])

ax1 = plt.bar(np.arange(len(avg_list[4])),avg_list[4] ,  width, bottom=map(sum, zip(avg_list[0],\
        avg_list[1], avg_list[2], avg_list[3])), color=color_list[3])
ax2 = plt.bar(width+np.arange(len(tail_list[4])),tail_list[4] ,  width, bottom=map(sum, zip(tail_list[0],\
       tail_list[1], tail_list[2], tail_list[3])), color=color_list[3])

ax5 = plt.bar(np.arange(len(avg_list[5])),avg_list[5] ,  width, bottom=map(sum, zip(avg_list[0],\
        avg_list[1], avg_list[2], avg_list[3], avg_list[4])), color=color_list[8], yerr=final_err_list2)
ax6 = plt.bar(width++np.arange(len(tail_list[5])),tail_list[5] ,  width, bottom=map(sum, zip(tail_list[0],\
        tail_list[1], tail_list[2], tail_list[3], tail_list[4])), color=color_list[8], yerr=final_err_list2)






m1, = ax.plot([], [], c=color_list[2] , marker='s', markersize=20,
                      fillstyle='left', linestyle='none')

m2, = ax.plot([], [], c=color_list[0] , marker='s', markersize=20,
                       linestyle='right')

#---- Define Second Legend Entry ----

m3, = ax.plot([], [], c=color_list[5] , marker='s', markersize=20,
                      fillstyle='left', linestyle='none')

m4, = ax.plot([], [], c=color_list[7] , marker='s', markersize=20,
                      fillstyle='right', linestyle='none')

m5, = ax.plot([], [], c=color_list[8] , marker='s', markersize=20,
                      fillstyle='bottom', linestyle='none')

m6, = ax.plot([], [], c=color_list[3] , marker='s', markersize=20,
                      fillstyle='bottom', linestyle='none')

#---- Plot Legend ----

ax.legend(((m1,m2,m6), (m3, m4, m5)), ('Queuing Delay', 'Compute Delay'), numpoints=1, labelspacing=2,
                  loc='upper right', fontsize=14, ncol=2)
plt.axhline(y=2500.0, color='k', ls='--')
plt.ylabel('Latency (ms)')
plt.xticks(np.arange(len(xticks))+width, xticks, fontsize=10, ha='center')
plt.ylim(0,ylim)
plt.savefig('done2.png', bbox_inches='tight',  dpi=125)

#p1 = plt.bar(np.arange(len(avg_list[0])),avg_list[0] , width, color='r')
#p2 = plt.bar(np.arange(len(avg_list[1])),avg_list[1] ,  width, bottom=avg_list[0],color='y')
#p3 = plt.bar(np.arange(len(avg_list[2])),avg_list[2] ,  width, bottom=map(sum, zip(avg_list[0], avg_list[1])),color='g')
#p4 = plt.bar(np.arange(len(avg_list[3])),avg_list[3] ,  width, bottom=avg_list[2],color=color_list[7])
#p5 = plt.bar(np.arange(len(avg_list[4])),avg_list[4] ,  width, bottom=avg_list[3],color=color_list[3])
#p6 = plt.bar(np.arange(len(avg_list[5])),avg_list[5] ,  width, bottom=avg_list[4],color=color_list[8], yerr=final_err_list2)



### data = defaultdict(list )
### WL = ['WL1', 'WL2', 'WL3', 'WL4', 'WL5']
### for item in fList:
###     if 'wl' in item:
###         wlid = item
###     else:
###         data[wlid].append([float(x) for x in item.split(',')])
###
### #for item in data:
### #    #print item
### #    for item2 in data[item]:
### #        print item2
### #        for item3 in item2:
### #            print item3
### #            print float(item3)
###
### xaxis = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5' ]
### print len(data['wl1'][0])
### print len(data['wl1'][1])
### print len(data['wl1'][2])
### print len(data['wl1'][3])
### print len(data['wl1'][4])
###
### a = len(data['wl1'][0])
### print np.arange(a)
### b = np.arange(6,10,1)
### print b
### c = np.arange(11,17,1)
### d = np.arange(18,24,1)
### e = np.arange(25,30,1)
###
###

### down=int(0)
### up = int(300)
### dashes = [5, 3, 5, 3]
###
### line1, = ax.plot( [5.25,5.25,5.25], [down,8,up], 'k--', linewidth=1.2)
### line1.set_dashes(dashes)
### line2, = ax.plot( [10.5, 10.5,10.5], [down,8,up], 'k-', linewidth=1.2)
### line2.set_dashes(dashes)
### line2, = ax.plot( [17.4, 17.4,17.4], [down,8,up], 'k-', linewidth=1.2)
### line2.set_dashes(dashes)
### line2, = ax.plot( [24.45, 24.45, 24.45], [down,8,up], 'k-', linewidth=1.2)
### line2.set_dashes(dashes)
###
###
###
###
### dashes = [10, 5, 10, 5]
### line1, = ax.plot( [0,5.25], [225,225], 'r--', linewidth=2)
### line1.set_dashes(dashes)
### line2, = ax.plot( [5.25, 10.5], [200,200], 'r--', linewidth=2)
### line2.set_dashes(dashes)
### line2, = ax.plot( [10.5, 17.4], [170, 170], 'r-', linewidth=2)
### line2.set_dashes(dashes)
### line2, = ax.plot( [17.4, 24.45], [200,200], 'r-', linewidth=2)
### line2.set_dashes(dashes)
### line2, = ax.plot( [24.45, 30], [160,160], 'r-', linewidth=2)
### line2.set_dashes(dashes)
###
### p1 = plt.bar(np.arange(len(data['wl1'][0])),  data['wl1'][0], width, color=color_list[0])
### p2 = plt.bar(np.arange(len(data['wl1'][1])),  data['wl1'][1], width, bottom=data['wl1'][0], color=color_list[5], label='Queuing Delay')
### p3 = plt.bar(np.arange(len(data['wl1'][2])),  data['wl1'][2], width, bottom=list(map(sum, zip(data['wl1'][0], data['wl1'][1]))), color=color_list[1])
### p4 = plt.bar(np.arange(len(data['wl1'][3])),  data['wl1'][3], width, bottom=list(map(sum, zip(data['wl1'][0], data['wl1'][1],data['wl1'][2]))), color=color_list[5])
### p5 = plt.bar(np.arange(len(data['wl1'][4])),  data['wl1'][4], width, bottom=list(map(sum, zip(data['wl1'][0],data['wl1'][1],data['wl1'][2], data['wl1'][3] ))), color=color_list[2])
###
### p6 = plt.bar(b, data['wl2'][0], width, color=color_list[0])
### p7 = plt.bar(b, data['wl2'][1], width, bottom=data['wl2'][0], color=color_list[5])
### p8 = plt.bar(b, data['wl2'][2], width, bottom=list(map(sum, zip(data['wl2'][0], data['wl2'][1]))), color=color_list[1])
###
###
### p1 = plt.bar(c,  data['wl3'][0], width, color=color_list[0])
### p2 = plt.bar(c,  data['wl3'][1], width, bottom=data['wl3'][0], color=color_list[5])
### p3 = plt.bar(c,  data['wl3'][2], width, bottom=list(map(sum, zip(data['wl3'][0], data['wl3'][1]))), color=color_list[1])
### p4 = plt.bar(c,  data['wl3'][3], width, bottom=list(map(sum, zip(data['wl3'][0], data['wl3'][1],data['wl3'][2]))), color=color_list[5])
### p5 = plt.bar(c,  data['wl3'][4], width, bottom=list(map(sum, zip(data['wl3'][0],data['wl3'][1],data['wl3'][2], data['wl3'][3] ))), color=color_list[2])
### p6 = plt.bar(c,  data['wl3'][5], width, bottom=list(map(sum, zip(data['wl3'][0],data['wl3'][1],data['wl3'][2], data['wl3'][3],data['wl3'][4]))), color='m')
###
### p1 = plt.bar(d,  data['wl4'][0], width, color=color_list[0])
### p2 = plt.bar(d,  data['wl4'][1], width, bottom=data['wl4'][0], color=color_list[5])
### p3 = plt.bar(d,  data['wl4'][2], width, bottom=list(map(sum, zip(data['wl4'][0], data['wl4'][1]))), color=color_list[1])
### p4 = plt.bar(d,  data['wl4'][3], width, bottom=list(map(sum, zip(data['wl4'][0], data['wl4'][1],data['wl4'][2]))), color=color_list[5])
### p5 = plt.bar(d,  data['wl4'][4], width, bottom=list(map(sum, zip(data['wl4'][0],data['wl4'][1],data['wl4'][2], data['wl4'][3] ))), color=color_list[2])
### #p6 = plt.bar(d,  data['wl4'][5],width,  bottom=list(map(sum, zip(data['wl4'][0],data['wl4'][1],data['wl4'][2], data['wl4'][3],data['wl4'][4]))), color='m')
###
###
###
### p1 = plt.bar(e,  data['wl5'][0], width, color=color_list[0])
### p2 = plt.bar(e,  data['wl5'][1], width, bottom=data['wl5'][0], color=color_list[5])
### p3 = plt.bar(e,  data['wl5'][2], width, bottom=list(map(sum, zip(data['wl5'][0], data['wl5'][1]))), color=color_list[1])
### p4 = plt.bar(e,  data['wl5'][3], width, bottom=list(map(sum, zip(data['wl5'][0], data['wl5'][1],data['wl5'][2]))), color=color_list[5])
### p5 = plt.bar(e,  data['wl5'][4], width, bottom=list(map(sum, zip(data['wl5'][0],data['wl5'][1],data['wl5'][2], data['wl5'][3] ))), color=color_list[2])
###
### plt.yticks([0,50,100,150,200,250,300], [0,500,1000,1500,2000,2500,3000], size='10')
### #plt.grid()
### #plt.xticks(np.arange(len(xaxis)), xaxis)
### ax.xaxis.set_major_formatter(plt.NullFormatter())
### add_line(ax, 0 * 1.0, -.1)
### add_line(ax, 1 * 0.175, -.1)
### add_line(ax, 1 * 0.35, -.1)
### add_line(ax, 1 * 0.58, -.1)
### add_line(ax, 1 * 0.815, -.1)
### add_line(ax, 1 * 1, -.1)
### ax.text(2, -50, r'WL1', fontsize=12)
### ax.text(6.5, -50, r'WL2', fontsize=12)
### ax.text(13.5, -50, r'WL3', fontsize=12)
### ax.text(20.5, -50, r'WL4', fontsize=12)
### ax.text(26.5, -50, r'WL5', fontsize=12)
### #plt.ylim(0,300)
### #p = mpatches.Patch(color=color_list[5], alpha=0.5, linewidth=1, ec=color_list[0])
### #p1 = mpatches.Patch(color=color_list[0], alpha=0.5, linewidth=1, ec=color_list[0])
### #p2 = mpatches.Patch(color=color_list[1], alpha=0.5, linewidth=1, ec=color_list[0])
### #plt.legend((p,), ('Queuing Delay',), (p1,p2,) ('blah'))
### m1, = ax.plot([], [], c='red' , marker='s', markersize=20,
###                       fillstyle='left', linestyle='none')
###
### m2, = ax.plot([], [], c=color_list[5] , marker='s', markersize=20,
###                        linestyle='none')
###
### #---- Define Second Legend Entry ----
###
### m3, = ax.plot([], [], c=color_list[0] , marker='s', markersize=20,
###                       fillstyle='left', linestyle='none')
###
### m4, = ax.plot([], [], c=color_list[1] , marker='s', markersize=20,
###                       fillstyle='right', linestyle='none')
###
### m5, = ax.plot([], [], c=color_list[2] , marker='s', markersize=20,
###                       fillstyle='bottom', linestyle='none')
###
### m6, = ax.plot([], [], c=color_list[3] , marker='s', markersize=20,
###                       fillstyle='right', linestyle='none')
###
### #---- Plot Legend ----
###
### ax.legend(((m2), (m3, m4, m5)), ('Queuing Delay', 'Compute Delay'), numpoints=1, labelspacing=2,
###                   loc='upper right', fontsize=16, ncol=2)
###
###
### plt.ylabel('Latency\nStage Wise')
### #plt.title('Scores by group and gender')
### plt.savefig('done2.png', bbox_inches='tight',  dpi=125)
