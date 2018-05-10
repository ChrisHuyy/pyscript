# coding=utf-8
from __future__ import division
import pandas as pd

'''
基于原结论：“1/2新用户只播放第一个视频就退出” ---- 他们所面临的环境是怎样的？

对这些新用户在不同维度进行和活跃用户的对比

以下是数据分析

'''


df = pd.read_csv('new_user.csv')
dfg_utdid = df.groupby('utdid')
# df_videoids = df[['utdid','video_id']]
# print df_videoids.head(5)

def pd_concat(series):
	return ','.join(series)

# 把series转化成dataframe
def dfy(series,index_name,values_name):
	return pd.DataFrame({index_name:series.index, values_name:series.values})

# 把浮点数转化为百分比
def percentagefy(f):
	return '%.2f%%'%(f*100)

# 写报告
def file_write(content,file_name='report.txt'):
	with open(file_name,'a') as f:
		f.write(content)

# dfs = df_videoids.groupby('utdid').video_id.apply(pd_concat)
# new_df = dfy(dfs,index_name='utdid',values_name='video_ids')
# print type(new_df)
# print new_df.head(5)

# 初始化报告文件
with open('report.txt','w') as f:
	f.write('')

# 只看了一个视频的用户占比
s = dfg_utdid.action.count()
file_write("只看了一个视频的用户占比：%.2f%%\n" % (len(s[s==1])/len(s) * 100)) 
file_write("\n")

# 生成中间表 - 标记用户观看的视频数
df_video_watch_num = dfy(s,index_name='utdid',values_name='video_watch_num')
df_mark_vn = pd.merge(df,df_video_watch_num,how='left',on='utdid')


# 不同维度的占比输出
def separate(df_mark,dimension):
	file_write("========================== SEPARATE ====================================\n")
	file_write("维度：%s，与总样本什么差异:\n" % dimension) 
	df_1 = df_mark[df_mark['video_watch_num'] == 1][['utdid',dimension]].groupby(dimension).count().\
			rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
	df_2 = df_mark[df_mark['video_watch_num'] != 1][['utdid',dimension]].groupby(dimension).count().\
			rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)

	df_1['percentage'] = (df_1['Total_Numbers']/(df_1['Total_Numbers'].sum())).apply(percentagefy)
	df_2['percentage'] = (df_2['Total_Numbers']/(df_2['Total_Numbers'].sum())).apply(percentagefy)
	df_1 = df_1.drop(['Total_Numbers'], axis = 1)
	df_2 = df_2.drop(['Total_Numbers'], axis = 1)
	file_write("只看一个视频的用户\n")
	df_1.head().to_csv(r'report.txt', mode='a', sep='\t')
	file_write("\n")
	file_write("活跃用户\n")
	df_2.head().to_csv(r'report.txt', mode='a', sep='\t')
	file_write("\n")

separate(df_mark_vn,'tag')
separate(df_mark_vn,'way')
separate(df_mark_vn,'source_type')
separate(df_mark_vn,'net')
separate(df_mark_vn,'user_source')
separate(df_mark_vn,'refer')
separate(df_mark_vn,'app_id')
separate(df_mark_vn,'login')
separate(df_mark_vn,'app_ver')


# # 只看了一个视频的用户是怎么接触到视频，与总样本什么差异
# print "只看了一个视频的用户是怎么接触到视频，与总样本什么差异:".decode('utf-8')
# df_3 = df_mark_vn[df_mark_vn['video_watch_num'] == 1][['utdid','way']].groupby('way').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# df_4 = df_mark_vn[df_mark_vn['video_watch_num'] != 1][['utdid','way']].groupby('way').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# print df_3.head()
# print df_4.head()
# print '\n'

# # 只看了一个视频的用户是接触什么类型的视频，与总样本什么差异
# print "只看了一个视频的用户是接触什么类型的视频，与总样本什么差异:".decode('utf-8')
# df_5 = df_mark_vn[df_mark_vn['video_watch_num'] == 1][['utdid','source_type']].groupby('source_type').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# df_6 = df_mark_vn[df_mark_vn['video_watch_num'] != 1][['utdid','source_type']].groupby('source_type').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# print df_5.head()
# print df_6.head()
# print '\n'


# # 只看了一个视频的用户网络情况是怎样，与总样本什么差异
# print "只看了一个视频的用户网络情况是怎样，与总样本什么差异:".decode('utf-8')
# df_7 = df_mark_vn[df_mark_vn['video_watch_num'] == 1][['utdid','net']].groupby('net').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# df_8 = df_mark_vn[df_mark_vn['video_watch_num'] != 1][['utdid','net']].groupby('net').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# print df_7.head()
# print df_8.head()
# print '\n'

# # 只看了一个视频的用户看的是谁的视频，与总样本什么差异
# print "只看了一个视频的用户看的是谁的视频，与总样本什么差异:".decode('utf-8')
# df_9 = df_mark_vn[df_mark_vn['video_watch_num'] == 1][['utdid','user_source']].groupby('user_source').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# df_10 = df_mark_vn[df_mark_vn['video_watch_num'] != 1][['utdid','user_source']].groupby('user_source').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# print df_9.head()
# print df_10.head()
# print '\n'


# # 只看了一个视频的用户从哪里来，与总样本什么差异
# print "只看了一个视频的用户从哪里来，与总样本什么差异:".decode('utf-8')
# df_11 = df_mark_vn[df_mark_vn['video_watch_num'] == 1][['utdid','refer']].groupby('refer').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# df_12 = df_mark_vn[df_mark_vn['video_watch_num'] != 1][['utdid','refer']].groupby('refer').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# print df_11.head()
# print df_12.head()
# print '\n'



# # 只看了一个视频的用户安装渠道是什么，与总样本什么差异
# print "只看了一个视频的用户安装渠道是什么，与总样本什么差异:".decode('utf-8')
# df_13 = df_mark_vn[df_mark_vn['video_watch_num'] == 1][['utdid','app_id']].groupby('app_id').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# df_14 = df_mark_vn[df_mark_vn['video_watch_num'] != 1][['utdid','app_id']].groupby('app_id').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# print df_13.head()
# print df_14.head()
# print '\n'


# # 只看了一个视频的用户是否登录用户，与总样本什么差异
# print "只看了一个视频的用户是否登录用户，与总样本什么差异:".decode('utf-8')
# df_15 = df_mark_vn[df_mark_vn['video_watch_num'] == 1][['utdid','login']].groupby('login').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# df_16 = df_mark_vn[df_mark_vn['video_watch_num'] != 1][['utdid','login']].groupby('login').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# print df_15.head()
# print df_16.head()
# print '\n'

# # 只看了一个视频的用户是哪个版本的，与总样本什么差异
# print "只看了一个视频的用户是哪个版本的，与总样本什么差异:".decode('utf-8')
# df_17 = df_mark_vn[df_mark_vn['video_watch_num'] == 1][['utdid','app_ver']].groupby('app_ver').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# df_18 = df_mark_vn[df_mark_vn['video_watch_num'] != 1][['utdid','app_ver']].groupby('app_ver').count().\
# 		rename(columns={'utdid':'Total_Numbers'}).sort_values(by='Total_Numbers',ascending=False)
# print df_17.head()
# print df_18.head()
# print '\n'