from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from auth_data import username, password
import pandas as pd
import random
import time
import requests
import os


# Убрать браузер можно так: 
# Self.options = Options()
# Self.options.headless = True

class InstagramBot():
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(service=Service('chromedriver.exe'), options = webdriver.ChromeOptions())
        
    
    def close_browser(self):
        self.browser.close()
        self.browser.quit()
        
    
    def login(self):
        browser = self.browser
        browser.get('https://www.instagram.com/')
        time.sleep(random.randrange(3,5))
        
        username_input = browser.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(username)
        
        password_input = browser.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(password)
        
        password_input.send_keys(Keys.ENTER)
        
        time.sleep(random.randrange(8,10))
        
        
    
    def like_photo_by_hashtag(self, hashtag):
        browser= self.browser
        browser.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
        time.sleep(random.randrange(3,5))
        
        for i in range(1, 4):
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3,5))

        hrefs = browser.find_elements(By.TAG_NAME, 'a')
        posts_urls = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
        
        for url in posts_urls:
            try:
                browser.get(url)
                time.sleep(3)
                like_button = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()
                time.sleep(random.randrange(8,10))
                
            except Exception as ex:
                print(ex)
                self.close_browser()
                
    
    def xpath_exists(self, url):
        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist
            
            
    def put_exactly_like(self, userpost):
        browser = self.browser
        browser.get(userpost)
        time.sleep(4)
        
        wrong_userpage = '/html/body/div/div[1]/div/div/h2'
        
        if self.xpath_exists(wrong_userpage):
            print('There is no such post, check the "url"!')
            self.close_browser()
        else:
            print('The post has been found, we like it!')
            time.sleep(3)
            
            like_button = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button'
            browser.find_element(By.XPATH, like_button).click()
            time.sleep(3)
            
            print(f'This post was like!: {userpost}')
            self.close_browser()


    def get_all_posts(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        
        wrong_userpage = '/html/body/div/div[1]/div/div/h2'
        
        if self.xpath_exists(wrong_userpage):
            print('There is no such user, check the "url"!')
            self.close_browser()
        else:
            print('The user has been found, we like it!')
            time.sleep(3)
            posts_count = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[1]/div/span/span').text
            q = posts_count.split(",")
            if len(q) > 1:
                posts_count = q[0] + q[1]
            else:
                posts_count = q[0]
            posts_count = int(posts_count)
            loops_count = int(posts_count/12)
            print(loops_count)
            
            posts_urls = []
            for i in range(0,loops_count):
                hrefs = browser.find_elements(By.TAG_NAME, 'a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
                for href in hrefs:
                    posts_urls.append(href)
                
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2,4))
                print(f"Iteration: #{i}")
            
            file_name = userpage.split("/")[-2]
            if not os.path.exists(f'{file_name}'):
                os.mkdir(file_name)
            posts_urls = list(set(posts_urls))
            
            with open(f'{file_name}/posts.txt', 'w') as file:
                for post_url in posts_urls:
                    file.write(post_url + '\n')


    def put_many_likes(self, userpage):
        browser = self.browser
        self.get_all_posts(userpage)
        file_name = userpage.split("/")[-2]
        browser.get(userpage)
        time.sleep(4)
        
        with open(f'{file_name}/posts.txt') as file:
            urls_list = file.readlines()
            for post_url in urls_list:
                try:
                    browser.get(post_url)
                    time.sleep(2)
                    like_button = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button'
                    browser.find_element(By.XPATH, like_button).click()
                    time.sleep(3)
                    print(f'This post was like!: {post_url}')
                except Exception as ex:
                    print(ex)
        self.close_browser()


    def download_userpage_content(self, userpage):
        browser = self.browser
        self.get_all_posts(userpage)
        file_name = userpage.split("/")[-2]
        browser.get(userpage)
        time.sleep(4)
        
        
        img_and_video_src_list =[]
        with open(f'{file_name}/posts.txt') as file:
            urls_list = file.readlines()
            for post_url in urls_list:
                try:
                    browser.get(post_url)
                    time.sleep(4)
                    carousel_src = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div/div[1]/img'
                    basqasha_carousel_src = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[1]/div/div[1]/div[2]/div/div/div/ul/li[2]/div/div/div/div/div[1]/div[1]/img'
                    img_src = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[1]/div/div/div/div[1]/div[1]/img'
                    video_src = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[1]/div/div/div/div/div/div/div/video'
                    post_id = post_url.split('/')[-2]
                    
                    if self.xpath_exists(img_src):
                        img_src_url = browser.find_element(By.XPATH, img_src).get_attribute('src')
                        img_and_video_src_list.append(img_src_url)
                        print('photooo')
                        get_img = requests.get(img_src_url)
                        with open(f'{file_name}/{post_id}_img.jpg', "wb") as img_file:
                            img_file.write(get_img.content)
                            print('abraca')
                    elif self.xpath_exists(carousel_src):
                        i = 0
                        while True:
                            if browser.find_elements(By.CLASS_NAME, "_afxw"):
                                carousel_src_url = browser.find_element(By.XPATH, carousel_src).get_attribute('src')
                                print(f'src[{i}] = {carousel_src_url}')
                                img_and_video_src_list.append(carousel_src_url)
                                print('carousel')
                                get_img = requests.get(carousel_src_url)
                                with open(f'{file_name}/{post_id}_#{i}_img.jpg', "wb") as img_file:
                                    img_file.write(get_img.content)
                                    print('abracadabra')
                            
                                print('find element')
                                browser.find_element(By.CLASS_NAME, "_afxw").click()
                                time.sleep(2)
                                i +=1
                            else:
                                carousel_src_url = browser.find_element(By.XPATH, carousel_src).get_attribute('src')
                                print(carousel_src_url)
                                img_and_video_src_list.append(carousel_src_url)
                                print('carousel')
                                get_img = requests.get(carousel_src_url)
                                with open(f'{file_name}/{post_id}_#{i}_img.jpg', "wb") as img_file:
                                    img_file.write(get_img.content)
                                break
                    elif self.xpath_exists(basqasha_carousel_src):
                        i = 0
                        while True:
                            if browser.find_elements(By.CLASS_NAME, "_afxw"):
                                carousel_src_url = browser.find_element(By.XPATH, basqasha_carousel_src).get_attribute('src')
                                print(f'src[{i}] = {carousel_src_url}')
                                img_and_video_src_list.append(carousel_src_url)
                                print('carousel')
                                get_img = requests.get(carousel_src_url)
                                with open(f'{file_name}/{post_id}_#{i}_img.jpg', "wb") as img_file:
                                    img_file.write(get_img.content)
                                    print('abracadabra')
                            
                                print('yyyyyyyyyyyyy')
                                browser.find_element(By.CLASS_NAME, "_afxw").click()
                                time.sleep(2)
                                i +=1
                            else:
                                carousel_src_url = browser.find_element(By.XPATH, basqasha_carousel_src).get_attribute('src')
                                print(carousel_src_url)
                                img_and_video_src_list.append(carousel_src_url)
                                print('carousel')
                                get_img = requests.get(carousel_src_url)
                                with open(f'{file_name}/{post_id}_#{i}_img.jpg', "wb") as img_file:
                                    img_file.write(get_img.content)
                                break
                    elif self.xpath_exists(video_src):
                        video_src_url = browser.find_element(By.XPATH, video_src).get_attribute('src')
                        img_and_video_src_list.append(video_src_url)
                        print(post_url)
                        print('videoooo')
                        
                        get_video = requests.get(video_src_url, stream=True)
                        with open(f"{file_name}/{post_id}_video.mp4", "wb") as video_file:
                            for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    video_file.write(chunk)
                                    print('dabra')
                    else:
                        print('Oooops!')
                        img_and_video_src_list.append(f'{post_url}, doesn`t have a link')
                    print('vse skachano!')
                except Exception as ex:
                    print(ex)
        self.close_browser()
        
        with open(f'{file_name}/{file_name}_content.txt', 'a') as file:
            for i in img_and_video_src_list:
                file.write(i+ '\n')
                
                
    def parse_follows(self, choice, step = 0, deep: int = 1, follows: dict = {}, file_name: str = '', username: str =''):
        browser = self.browser
            
        if step == 0:
            while True: 
                if username == '':
                    username = input('Enter username: ')
                reference = f'https://www.instagram.com/{username}/'
                browser.get(reference)
                time.sleep(random.randrange(2,4))
                wrong_userpage = '/html/body/div/div[1]/div/div/h2'
                if self.xpath_exists(wrong_userpage):
                    print('There is no such user, check the "url"!')
                    self.close_browser()
                else:
                    if not os.path.exists(username):
                            os.mkdir(username)
                    break
                
            start_time = time.time()
            
            if len(follows) == 0:
                follows = {'Adamdar': [], 'Step': [], 'Reference':[]}
            
            follows['Adamdar'].append(username)
            follows['Step'].append(step)
            follows['Reference'].append(reference)
            follows_csv = pd.DataFrame(follows)
            file_name = f'{username}/{choice}_#deep-{deep}.csv'
            follows_csv.to_csv(f'{file_name}', index=False)
        
        private_acc = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/article/div[1]/div'
        self.xpath_exists(private_acc)
        fcount='' 
        if choice == 'followers':
            # razdel = browser.find_element((By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]'))
            # followers = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[1]/div/div/a'\
            #             '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a'
            # followers = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a'
            # followers = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/ul/li[2]/a'
            # followers = 'x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5yxav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz._a6hd'
            followers ='/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[2]/a'
            f = followers
            f_button = browser.find_element(By.XPATH, f)
            f_count_without = f_button.find_element(By.CLASS_NAME, '_ac2a')
            f_count = f_count_without.get_attribute('title')
        elif choice == 'following':
            following = '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[3]/a'
            f = following
            f_count = browser.find_element(By.XPATH, f)

        print((f_count))
        razdelitel =''
        durys_fcount=''
        for i in f_count:
            print(i)
            if i == ',':
                razdelitel = ','
                print("delim ','")
            elif i == ' ':
                razdelitel = ' '
                print("delim ' '")
            elif i == ' ':
                print("delim ' '")
            else:
                durys_fcount += i

        # print(f'razdelitel = {razdelitel}')
        # f_count = f_count.split(" ")
        # for i in f_count:
        #     fcount += i
        fcount = int(durys_fcount)
        print(f'fcount = {fcount}')
        
        browser.find_element(By.XPATH, f).click()
        # browser.get(f'https://www.instagram.com/{username}/{choice}')
        step += 1
        loops_count = int(fcount/12)
        print(f'Count of iteration: {loops_count}')
        
        time.sleep(random.randrange(3,4))
        # '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]'
        followers_ul = browser.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]')
        # for i in range(1, loops_count + 1):
        #     browser.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].scrollHeight;", followers_ul)
        #     time.sleep(random.randrange(1,2))
        #     print(f'Iteration #{i}')
            
        # users = followers_ul.find_elements(By.CSS_SELECTOR, 'a.notranslate')
        # count_of_users = len(users) 
        # print(count_of_users)     
        while True:
            i = 0
            j = 0
            while True:
                if i%11 == 0:
                    j += 1
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].scrollHeight;", followers_ul)
                    print(f'Iteration #{j}')
                    time.sleep(random.randrange(4,5))
                    users = followers_ul.find_elements(By.CSS_SELECTOR, 'a.notranslate')
                    # time.sleep(random.randrange(1,2))


                f_adam = users[i].text
                f_step = step
                f_ref = users[i].get_attribute('href')     
                # follows['Adamdar'].append(f_adam)
                # follows['Step'].append(f_step)
                # follows['Reference'].append(f_ref)           
                new_row = pd.DataFrame({'Adamdar': f_adam, 'Step': f_step, 'Reference':f_ref}, index=[0])
                new_row.to_csv(file_name, header=None, mode='a', index=False)
                
                if deep == step:
                    print(f'[{i}]. zdes`')
                    
                elif step < deep:
                    print(f'follows1 = {follows}')
                    browser.get(f_ref)
                    print(f'follows2 = {follows}')
                    time.sleep(random.randrange(4,6))
                    self.parse_follows(choice, step, follows, deep, file_name)
                    browser.back()
                    
                
                if i == fcount:
                    break
                i +=1
            browser.back()
            break
        step -= 1
        
        if step == 0:
            fs_count = len(pd.read_csv(file_name).index)
            end_time = time.time()
            print(f'Start time: {start_time} \nEnd_time: {end_time} \nProcess time: {round((end_time-start_time),2)} \nSpend for each account: {round(((end_time-start_time)/int(fs_count)),2)} seconds')
            # self.close_browser()
                        
                        
    def get_all_followers(self, userpage):
        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        file_name = userpage.split('/')[-2]
        
        wrong_userpage = '/html/body/div/div[1]/div/div/h2'
        if self.xpath_exists(wrong_userpage):
            print('There is no such user, check the "url"!')
            self.close_browser()
        else:
            print('The user has been found, we like it!')
            time.sleep(3)
            
            if not os.path.exists(file_name):
                print(f'Creating a user folder: {file_name}')
                os.mkdir(file_name)
            
            followers_button = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[2]/a')
            followers_count = int(followers_button.text.split(' ')[0])
            print(f'The count of followers {followers_count}')
            time.sleep(4)
            
            loops_count = int(followers_count/12)
            print(f'Count of iteration: {loops_count}')
            time.sleep(4)
            
            followers_button.click()
            time.sleep(4)
            
            # followers_ul = WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]')))
            followers_ul = browser.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]')

            try:
                followers_urls =[]
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].scrollHeight;", followers_ul)
                    time.sleep(random.randrange(2,4))
                    print(f'Iteration #{i}')
                    
                # all_urls_div = followers_ul.find_elements(By.XPATH, f'/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/')
                all_urls_div = followers_ul.find_elements(By.CSS_SELECTOR, 'a.notranslate')
                print(all_urls_div)
                for url in all_urls_div:
                    followers_urls.append(url.get_attribute('href'))
                print(followers_urls)
                with open(f'{file_name}/followers.txt', 'a') as text_file:
                    print('teper` zdes`!')
                    for link in followers_urls:
                        text_file.write(link + '\n')
                        
                with open(f'{file_name}/followers.txt') as text_file:
                    users_urls = text_file.readlines()
                    
                    for user in users_urls:
                        try:
                            try:
                                with open(f'{file_name}/subscribe_list.txt', 'r') as subscribe_list_file:
                                    lines = subscribe_list_file.readlines()
                                    if user in lines:
                                        print(f'We are already subscribed to this {user} account')
                                        continue
                            except Exception as ex:
                                print('The file with the links has not been created yet.')
                                #print(ex)

                            browser = self.browser
                            browser.get(userpage)                            
                            page_owner = userpage.split('/')[-2]
                            
                            if self.xpath_exists('/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/a'):
                                print('This page is your, skip iteration')
                            elif self.xpath_exists('/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button'):
                                print(f'You are already subscribed to {page_owner}, skip iteration')
                            else:
                                time.sleep(random.randrange(4,8))
                                
                                if self.xpath_exists('/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/article/div[1]/div/h2'):
                                    try:
                                        follow_button = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div/button').click()
                                        print(f'A closed account. Requested a subscription to the user {page_owner}.')
                                    except Exception as ex:
                                        print(ex)
                                    
                                else:
                                    try:
                                        if self.xpath_exists('/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button'):
                                            follow_button = browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/div[1]/div[1]/div/div[1]/button').click()
                                            print(f'Public account. You are subscribing to {page_owner}')
                                        else:
                                            print('Can`t found!')
                                            
                                    except Exception as ex:
                                        print(ex)

                                with open(f'{file_name}/subscribe_list.txt', 'a') as subscribe_list_file:
                                    subscribe_list_file.write(user)
                                    
                                time.sleep(random.randrange(7, 15))
                    
                        except Exception as ex:
                            print(ex)
                            self.close_browser()
                
            except Exception as ex:
                print(ex)
                self.close_browser()
            
            
        self.close_browser()
        

        
                
        

insta = InstagramBot(username, password)
insta.login()
#insta.put_exactly_like('https://www.instagram.com/p/ClqmQmptbRz/?utm_source=ig_web_copy_link')
# insta.download_userpage_content('https://www.instagram.com/olzhvssy/')
# insta.get_all_followers('https://www.instagram.com/olzhvssy/')

while True:
    choice = input('What do you want to pars? \n[1]Followers\t[2]Followings\nEnter the number: ')
    if choice == '1':
        choice = 'followers'
        break
    
    elif choice == '2':
        choice = 'following'
        break
# f_count = browser.find_element(By.CSS_SELECTOR, 'span.title').text
deep = 1

while True:
    d = input('To what deapth do you want to parse?\nEnter a number: ')
    if int(d):
        d = int(d)
        deep = d
        break
    else:
        print('I humanly asked you to enter the number ;(')
# 'adikke', 'arman_sapiolda', 'abayomar',
acc_more_10k = ['yerkintatishev','vitaliybuzhan','kulanman','batyr_siyabek','moneyqen','sabi.beis','zhmeirbek','alibekov_beibit','rapmuzkz_kz','theflow.online','kyranstudents','qazphilosophy','interiordesigners','kuantr','finance_for_life','ruslan_berdenov','shoqansuits','aligee_investor','rahim_abdimanatt','qonandoyle','damir.amanzho1ov','g_e_class','sharipov_ulugbek','qazaqgrammar','nashi_v_mire','lifeofmedet','t.itayev','askhat_abu_muhammad','rapmuzkz','syrymbek_tau','clvdeex','forbes_kz','galymkaliakbarov','kyran_talapbek','hakimmukaram','nikiforov.standup','aqarys','we_project','give_my_oscar','nemcy.kz','nnnurdaylet','erkebulan_toktar','unknownkazak','mark_dixson','baha_puper','menenbarisuraid1','qazaqstories','saebiz_banda','flagman_kz','smotra_0ff','kabylbek_alipbaiuly','muftiyatkz','oljaskhan_','darkhanzholshybekuly','kimotashy','armanustaz.kz','oner_kyrandary_official','akbota__anuarbek','asq_flowers','outfit.kz','kex_group','territima','iman_ainasy_kz','serdos_m','kris.p.original','good_zhan','erbolat.gulnur','almatymarathon','darhanzholshybekov','erlan_synyqshy','tiktok.k7','rodnoiburger_shymkent','rodnoiburger_kyzylorda','suleimen.maralbai','auda_amar','khan_storre','azhikenov','saebiz_sila','qazaq_robin_hood','tarazkilem','burya_chopa','altynai__hanum','nomad.today','serkebayeva_resmi','meirambekmahambetov','mynbala_house','olzhas_suleimenov','ruslan__amir','baglantay','dakentiy_official','nartay_aralbayuli','espanov_n','farizatoreali']
# len(acc_more_10k)
# for i in acc_more_10k:
#     insta.parse_follows(choice=choice, deep=deep, username=i)
insta.parse_follows(choice=choice, deep=deep)