#encoding:utf-8
# writer: MikeShine
# date: 2018-7-20
# 这是用mitmdump -s script.py在终端运行命令来执行的
# 通过抓包获得视频地址来直接下载



# 还要考虑对userid做去重之类的操作。遇到重复的Id, 我们不下载，这里不能直接跳过，因为下载的脚本和控制的脚本是两个独立的部分


import requests
import re 
import os
import redis

r1 = redis.Redis(host='127.0.0.1', port=6379, db=1, decode_responses=True)

path_NOW = ""   # 写到全局变量先声明一下。
num = 0
tmp = ""
user_id = ""
video_List=[]   # 用户临时下载视频列表
id_List=[]    # 临时Id列表，用于确认是否变换了用户Id
path_delete = ""  # 用于文件删除的路径

# 文件路径
def getPath(user_id):
    path = 'D:/video/DouYin_Test/'
    real_path = path + str(user_id) + '/'
    if not os.path.isdir(real_path):
            os.makedirs(real_path)           # 路径不存在就创造路径
    return real_path

 
def response(flow):    # 函数名不能改哈
    global path_NOW
    global num 
    global tmp
    global user_id
    global video_List
    global id_List
    global path_delete

    target_urls = ['http://v1-dy.ixigua.com/', 'http://v1-dy-x.ixigua.com/','http://v1-dy-y.ixigua.com/','http://v1-dy-z.ixigua.com/',                   
                   'http://v3-dy.ixigua.com/','http://v3-dy-x.ixigua.com/','http://v3-dy-y.ixigua.com/','http://v3-dy-z.ixigua.com/',
                   'http://v6-dy.ixigua.com/','http://v6-dy-x.ixigua.com/','http://v6-dy-y.ixigua.com/','http://v6-dy-z.ixigua.com/',
                   'http://v9-dy.ixigua.com/','http://v9-dy-x.ixigua.com/','http://v9-dy-y.ixigua.com/','http://v9-dy-z.ixigua.com/']
    
    id_urls = ['https://api.amemv.com/aweme/v1/aweme/post/','https://aweme.snssdk.com/aweme/v1/aweme/post/']  
    
    
    # 这里是想要创建路径。
    for id_url in id_urls:
        if flow.request.url.startswith(id_url):
            print("**********这是包含UserId的地址*************")
            user_id_patn = re.compile(r'https://.*?/aweme/v1/aweme/post/\?.*?user_id=(.*?)&')
            user_id = re.findall(user_id_patn, flow.request.url)    
            
            path_NOW = getPath(user_id[0])   #当前工作执行路径
            print("*****************当前工作路径：%s********************" %path_NOW )
            # print(user_id[0])
            # print(id_List)


            if user_id[0] not in id_List:    
                id_List.append(user_id[0])

               

            if len(id_List)==2:   # 说明到了新的主页了
                # 这里删除最后那个文件
                file_list = os.listdir(path_delete)
                file_list.sort(key=lambda x:int(x[:-4]))    #倒数第四个字符排序
                print(file_list)  # 这里是空的
                del_path = path_delete + '/' + file_list[-1]
                os.remove(del_path)
                # 把相关的index清空
                num = 0
                video_List = []   

                #############################################################
                r1.sadd("DouYin_User",id_List[0])  # 把上一个Id添加到数据库里
                #############################################################

                id_List[0] = id_List[1]
                del id_List[1]
            return 



    # 下面是下载的部分
    if path_NOW != tmp:  # 工作路径改变才下载东西
        for url in target_urls:
            if flow.request.url.startswith(url): 

                ########################################################################
                if not sismember("DouYin_User",user_id[0]):  # 不在数据库中，才可以下载
                ########################################################################
                
                    if flow.request.url not in video_List:   # 避免下载重复视频的
                        filename = path_NOW +"/" + str(user_id[0]) +"_"+ str(num) + '.mp4'   
                        # 使用request获取视频url的内容
                        # stream=True作用是推迟下载响应体直到访问Response.content属性
                        res = requests.get(flow.request.url, stream=True)
                        # 将视频写入文件夹
                        with open(filename, 'ab') as f:
                            f.write(res.content)
                            f.flush()
                            print("****************" + filename + '下载完成' + "****************")
                        num += 1
                        video_List.append(flow.request.url)

                        path_delete = path_NOW   # 下载视频时候把当前工作路径保存下来 

                        return
       

