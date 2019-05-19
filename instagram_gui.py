
	
from tkinter import *
from tkinter.ttk import Progressbar #for progress bar
from tkinter import ttk # for progress bar
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



#-------------------------------------------------------------------------
# The main instagram bot


class InstaBot:
    def __init__(self,username,password):    # Our bot class has a username, password and a driver for web
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()


    def CloseBrowser(self):
        self.driver.close()


    def Login(self):
        driver = self.driver
        driver.get('https://www.instagram.com/') # open the web browser defined above and go to instagram.com
        time.sleep(3) # wait for 3 seconds to load all elements of webpage

        # so far the instagram page should be loaded in the webpage but, it's the signup page not the login page!
        # we should tell the bot to click the login button on the page by using XPATH ! https://www.guru99.com/xpath-selenium.html
        # The html tag for login button ==>  <a href="/accounts/login/?source=auth_switcher">Log in</a>
        # The XPATH equivalent of the tag is ==> "//a[@href='/accounts/login/?source=auth_switcher']"] 
        # xpath = //tagname[@attribute='value']

        login_btn = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_btn.click()                        
        time.sleep(3)
        # now we are in the login page and we have to fill the username and password
        username_element = driver.find_element_by_xpath("//input[@name='username']")
        username_element.clear() # clear the field
        username_element.send_keys(self.username) # put the defined username in this field
        password_element = driver.find_element_by_xpath("//input[@name='password']")
        password_element.clear()
        password_element.send_keys(self.password)
        # after filling the username and poassword we can either click login or press enter on keyboard
        password_element.send_keys(Keys.RETURN) # pressing enter
        # because i've activated 2 step verification, after pressing enter i have to enter a security code 
        # manually so i'll make the bot wait for 7 seconds ( so i can enter the security code ) and press enter after.
        time.sleep(7)
        verification_element = driver.find_element_by_xpath("//input[@name='verificationCode']")
        verification_element.send_keys(Keys.RETURN)
        time.sleep(3)

    def Like_photos(self):
        driver = self.driver
        hashtags = [str(hash1_input.get()),str(hash2_input.get()),str(hash3_input.get())]
        for hash in hashtags:
            driver.get('https://www.instagram.com/explore/tags/'+hash+'/') # open the page of desired hashtag
            time.sleep(3)
            # in the hashtag page, instagram will not load more pictures until you scroll the page down
            # so we have to simulate the scroll action with the bot
            for i in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                hrefs = driver.find_elements_by_tag_name('a') # in this line we are finding elementS insted of element ! so we have a list
                pic_hrefs = [item.get_attribute('href') for item in hrefs]
                pic_hrefs = pic_hrefs[0:len(pic_hrefs)-14] # getting rid of useless hrefs (SEE SOLVED PROBLEMS BELOW)
                # pic_hrefs = [href for href in pic_hrefs if hashtag in href] #### this is not working anymore because hashtag is not in the href anymore.
                print(hash + ' photos : ' + str(len(pic_hrefs)))

                for pic_href in pic_hrefs:
                    driver.get(pic_href)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    driver.find_element_by_xpath("//span[@aria-label='Like']").click()
                    time.sleep(5)

#--------------------------------------------------------------------
# The GUI intercation with the main Code
def user_exit():
    exit()

def add_data():
    shahinBot = InstaBot(account_input.get(),pass_input.get())
    shahinBot.Login()
    shahinBot.Like_photos()
    

#----------------------------------------------------------------------
# The GUI

#the window(frame)
window = Tk()
window.title("Instagram Bot")
window.geometry('400x400')

#handling the menu
menu = Menu(window)
new_item = Menu(menu)
new_item.add_command(label='Exit',command = user_exit)
menu.add_cascade(label='File', menu=new_item)
window.config(menu=menu)


#handling the labels
top_label = Label(window,text = "Instagram Bot",font=16)
top_label.place(x=140)
account_label = Label(window,text = "Instagram Account : ")
account_label.place(x=10,y=100)
pass_label = Label(window,text = "Instagram Password : ")
pass_label.place(x=10,y=130)
hash1_label = Label(window,text = "Hashtag #1 : ")
hash1_label.place(x=10,y=160)
hash2_label = Label(window,text = "Hashtag #2 : ")
hash2_label.place(x=10,y=190)
hash3_label = Label(window,text = "Hashtag #3 : ")
hash3_label.place(x=10,y=220)

#handling the input texts
account_input = Entry(window,width=25)
account_input.place(x=150,y=100)
pass_input = Entry(window,show='*',width=24)
pass_input.place(x=157,y=130 )
hash1_input = Entry(window,width=25)
hash1_input.place(x=105,y=160)
hash2_input = Entry(window,width=25)
hash2_input.place(x=105,y=190)
hash3_input = Entry(window,width=25)
hash3_input.place(x=105,y=220)


#handling button
btn = Button(window, text="Add Data & Start", command=add_data)
btn.place(x=120,y= 250)


window.mainloop()

