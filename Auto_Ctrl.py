#encoding:utf-8
# writer: MikeShine
# date: 2018-7-20
# This is the Auto_Ctrl Script for 
###################################
########## "Mike_Test " ###########
###################################

from appium import webdriver
from time import sleep
import time



class Action():
    def __init__(self):   # 构造函数
        # 初始化配置，设置Desired Capabilities参数
        self.desired_caps = {
        "platformName": "Android",
        "deviceName": "unknown-mike_test-192.168.194.101:5555",   # 根据设备名称更改  
        "udid":"192.168.194.101:5555",     # 这里的Udid才是真正能够辨识的模拟器的 indicator
        "appPackage": "com.ss.android.ugc.aweme",
        "appActivity": ".splash.SplashActivity"
        }
        # 指定Appium Server
        self.server = 'http://localhost:4723/wd/hub'    # 服务器的端口按照奇数向后排列
        # 新建一个Session
        self.driver = webdriver.Remote(self.server, self.desired_caps)
        # 设置滑动初始坐标和滑动距离
        self.start_x = 500
        self.start_y = 500
        self.distance = 500
        sleep(2)
        # app开启之后点击一次屏幕，确保页面的展示
        self.driver.tap([(500, 100)], 500)
        sleep(2)
        self.driver.tap([(500, 100)], 500)
        self.driver.swipe(365, 920, 365, 300)
        print("-----------------------------------初始化完成----------------------------------------")
        
    def scroll(self):
        sleep(2)
        self.driver.swipe(365, 920, 365, 300)
        
    
    def individual(self):
       
        if self.driver.find_elements_by_id("com.ss.android.ugc.aweme:id/aea"):   # 广告页面  
            self.scroll()
            localtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(localtime+"：跳过广告！")
            print()
            sleep(1)
            return
        
        else:  # 正常用户的作品    
            sleep(3)
            # self.driver.tap([(713,345)], 500)  # 通过tap()方法进入主页，这里包含了提醒信息的Debug

            self.driver.find_element_by_id("com.ss.android.ugc.aweme:id/aek").click()
            localtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print(localtime + "： 进入主页")
            sleep(2)  # 等主页加载
            
            element = self.driver.find_element_by_id("a04")  #  点赞数
            y_location = element.location['y'] + element.size['height'] + 50   #左上角的纵坐标 +  点赞的高度 + 50（固定差值34）        
            x_location = 300
            # 这个坐标取得不对
            self.driver.tap([(x_location, y_location)], 500)  # 确定点到作品中，这里是Debug有些音乐人的主页不同格式的问题。
            print("确认点击到作品")
            sleep(2)
            
            self.driver.tap([(161,975)], 500)  # 点第一个作品
            sleep(2)
            for i in range(3):   #  我们这里就只抓50个
                self.scroll()   
                sleep(1)
            self.driver.press_keycode(4)
            sleep(2)
            self.driver.press_keycode(4)
            sleep(2)


    def main(self):
        while True:
            self.individual()
            localtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print("*****************"+ localtime + "： 完成上一个用户主页爬取"+"******************")
            sleep(2)
            self.driver.tap([(500, 100)], 500)
            sleep(2)
            self.scroll()
            localtime = time.strftime("%Y-%m-%d %H:%M:%S")
            print("*****************"+localtime+ "： 向下一个用户进发"+ "*****************")
            sleep(2)
            
        
        
        
if __name__ == '__main__':
    action = Action()
    action.main()