import base
from base import *
import yycourse

def get_driver_options():
    with open(MYDIR + '/settings.yaml','r',encoding='utf-8') as f:
        settings = yaml.full_load(f.read())
    myoption = settings['driver'] # myoption这个字典就是settings['driver']这个字典
    return myoption

def init(myoption,exam_mode=False): # 初始化浏览器并导航至药育平台官网
    if myoption['browser'] == 'chrome':
        option = webdriver.ChromeOptions()
    elif myoption['browser'] == 'edge':
        option = webdriver.EdgeOptions()
    for i in myoption['options']:
        option.add_argument(i)
    # option.add_experimental_option('detach',True) # 程序结束后保留浏览器窗口
    option.add_experimental_option('excludeSwitches',['enable-logging']) # 关闭selenium控制台提示
    if myoption['driver_path'] == '':
        # 应用选项
        if myoption['browser'] == 'chrome':
            driver = webdriver.Chrome(options=option)
        elif myoption['browser'] == 'edge':
            driver = webdriver.Edge(options=option)
    else:
        driver_service = Service(myoption['driver_path'])
        if myoption['browser'] == 'chrome':
            driver = webdriver.Chrome(service=driver_service, options=option)
        elif myoption['browser'] == 'edge':
            driver = webdriver.Edge(service=driver_service, options=option)

    driver.implicitly_wait(20)
    driver.maximize_window() # 最大化
    driver.get('http://www.yysmart.cn') # 药育平台首页
    return driver
def login(_drivr,accnt):
    username=accnt[0]; password=accnt[1] # 获取用户名和密码
    _drivr.maximize_window() # 确认最大化
    Clickx(_drivr,'/html/body/div[3]/div[1]/div[2]/span[1]')    # 登录
    Enterx(_drivr,username,'/html/body/div[5]/div[2]/input[1]') # 用户名
    Enterx(_drivr,password,'/html/body/div[5]/div[2]/input[2]') # 密码
    Clickx(_drivr,'/html/body/div[5]/div[2]/div/p')             # 下拉
    time.sleep(0.5)                                             # 等待下拉列表加载
    Clickx(_drivr,'/html/body/div[5]/div[2]/div/ul/li[1]')      # 用户身份
    time.sleep(0.5)                                             # 等待下拉列表消失
    Clickx(_drivr,'/html/body/div[5]/div[2]/a[2]')              # 登录
def get_user_id(_drivr):
    cookies = _drivr.get_cookies()
    user_id = ''
    try:
        for cookie in cookies:
            if cookie['name'] == 'userId':
                user_id = cookie['value']
    except:
        pass
    return user_id

def fake_download(_drivr,user_id):
    with open(MYDIR + '/settings.yaml','r',encoding='utf-8') as f:
        settings = yaml.full_load(f.read())
    user_profile_dir = settings['yysmart']['user_profile_path']
    safety_education_ppt_url = 'yysmarturl://res:server=www.yysmart.cn&fid=Nb75816c6ad0f4ceeba361dbd358e908a&fext=ppt&fname=安全教育.ppt&logoid=Nc7904ab0ec9f4b27999f2b9850b42182&ftype=0&hashcode=ce2f6b8090f352c8c7c573a348d88a71'
    _drivr.get(safety_education_ppt_url)
    a = input('\t\t\t\t正在唤起示例资源链接，请在浏览器中点击打开yyamrt应用，接着点击否（不要下载），然后按回车继续')
    ## 如果userid文件夹不存在则创建
    ## 进入文件夹，将dat文件粘贴
    user_folder_name = '0'*(8-len(user_id)) + user_id
    filelist_storage_dir = user_profile_dir + '/' + user_folder_name
    isexist = os.path.exists(filelist_storage_dir)
    if not isexist:
        os.mkdir(filelist_storage_dir)
    with open(MYDIR + '/data/exam/filelist.dat','rb') as f:
        filelist_data = f.read()
    with open(filelist_storage_dir + '/filelist.dat', 'wb') as g:
        g.write(filelist_data)

def mysubmit(sinfo,check_only=False,exam_mode=False):
    # 读取课程信息
    course_list = mycsv(MYDIR + '/data/course_list/c' + sinfo['credit_hr'] +'.csv')
    myprint('Initiating browser...')
    driver = init(myoption=get_driver_options(),exam_mode=exam_mode) # 初始化浏览器并导航至药育平台官网
    myprint('Attempting login...')
    login(driver,sinfo['accnt']) # 登陆账户
    myprint('Handling: ' + sinfo['accnt'][0])
    time.sleep(1) # 等待登录后页面刷新
    user_id = get_user_id(driver)
    # 检测右上角显示的名字
    actual_name = driver.find_element(by=By.XPATH,value='/html/body/div[3]/div[1]/div[3]/div/h3').text
    if sinfo['name'] != actual_name: # 如果右上角显示的名字与本地记录不符（登记错误或者密码错误）
        if actual_name == '':
            myprint('\tIncorrect username or password!')
            result = {'res':False,'info':'Incorrect username or password','courses':{}}
        else:
            myprint('\tName mismatch! ' + sinfo['name'] + ' // ' + actual_name) # 报错并展示两个名字
            result = {'res':False,'info':'Name mismatch','courses':{}}
        driver.quit() # 退出浏览器
        return result
    result = {'res':True,'info':'No course','courses':{}}
    if exam_mode:
        a = input('\t请启动yysmart浏览助手并确认登陆账号为：' + sinfo['accnt'][0] + '输入y以显示密码')
        if a == 'y' or a =='Y':
            b = input('\t' + sinfo['accnt'][1])
        a = input('\t\t\t准备欺骗系统从而省略下载步骤（不保证一定能跳过），请按回车键继续，如仍需下载请按n')
        if a!='n' and a!='N':
            fake_download(driver,user_id)
        else:
            a = print('\t\t\t\t您可能需要等待下载')
    err = False # 初始状态为：没出错
    for i in range(TOTAL_COURSES): # 遍历每个课程
        try:
            # 课程列表中当前课程的简写拼音名字（如an）对应的学生信息字典中option下的选修课程情况为确实选修
            if sinfo['options'][course_list[i][2]]: 
                result['info'] = 'Complete!' # 如果有修读的课程，就覆盖“No course”的消息
                myprint('\tHandling: ' + course_list[i][0])
                cinfo = course_list[i][1:] # 获取课程信息。
                # course_list[i] = ['安','1187','an','1','1','0','18']

                yycourse.detail(driver,cinfo) # 进入课程详情页
                time.sleep(1) # 等待加载
                if not check_only: # 如果不是仅验证，那就开始完成课业
                    if exam_mode:
                        yycourse.exam(driver,cinfo,user_id) # 考核
                    else:
                        yycourse.prev(driver,cinfo) # 预习
                        yycourse.test(driver,cinfo) # 自测
                    time.sleep(1)
                res = yycourse.check_all(driver,cinfo,exam_mode,check_only) # 无论如何最后需要检测完成情况
                result['courses'][course_list[i][2]] = res[:] # [False,[prev_res, test_res, exam_res]]
        except:
            result['courses'][course_list[i][2]] = [False,['Fail','Fail','Fail']]
            err = True
            myprint('\t\tERROR!!!!!')
    for course in result['courses'].items():
        # course = ('an', [, [, , ]])
        if course[1][0] == False:
            result['res'] = False
            result['info'] = 'Incomplete!'
            break
    if err:
        result['info'] = 'ERROR!'
    driver.quit()
    return result
