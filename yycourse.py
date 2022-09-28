import base
from base import *

COURSE_TABS      = '/html/body/div[2]/div/div[2]/div[1]/ul'
COURSE_TABS_PREV = '/html/body/div[2]/div/div[2]/div[1]/ul/li[2]'
COURSE_TABS_TEST = '/html/body/div[2]/div/div[2]/div[1]/ul/li[3]'
COURSE_TABS_EXAM = '/html/body/div[2]/div/div[2]/div[1]/ul/li[4]'
COURSE_TABS_STAT = '/html/body/div[2]/div/div[2]/div[1]/ul/li[7]'

COURSE_TABS_PREV_CONTENT = '/html/body/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/ul'
COURSE_TABS_TEST_CONTENT = '/html/body/div[2]/div/div[2]/div[2]/div[3]/ul'
COURSE_TABS_EXAM_CONTENT = '/html/body/div[2]/div/div[2]/div[2]/div[4]/ul'
COURSE_TABS_STAT_CONTENT = '/html/body/div[2]/div/div[2]/div[2]/div[7]/div[2]'

COURSE_TABS_PREV_CONTENT_DELTA_IMG  = '/div[1]/a/img'
COURSE_TABS_TEST_CONTENT_DELTA_TEST = '/p[3]/a'
COURSE_TABS_EXAM_CONTENT_DELTA_IMG  = '/div[1]/a/img'
COURSE_TABS_STAT_CONTENT_DELTA_STAT = '/span[3]/label'

COURSE_TEST_PAGE_CONTENT = '/html/body/div[2]'

def detail(_drivr,cinfo): # [id,simp_nm,p,t,e,credit_hr]
    # 详情页
    COURSE_URL = 'http://www.yysmart.cn/class-detail.html?id='
    curl = COURSE_URL + cinfo[0]
    _drivr.get(curl)

def prev_check(_drivr,cinfo): # returns [,[list(starts from 1)]]
    # 检测是否完成该课程预习
    num = int(cinfo[2]) # 预习资料个数
    tot_completed = 0
    res = []
    Clickx(_drivr,COURSE_TABS_STAT) # 点击学习概况
    time.sleep(0.5) # 等待学习概况加载
    for i in range(1,num+1): # 逐个看学习状况中的每个预习完成情况（序号从1开始）
        spot = COURSE_TABS_STAT_CONTENT + '/div[' + str(i) + ']' + COURSE_TABS_STAT_CONTENT_DELTA_STAT
        if _drivr.find_element(by=By.XPATH,value=spot).text == '未学习':
            res.append(i) # 将未学习的预习资源序号加入结果列表
        else:
            tot_completed += 1
    return [not bool(len(res)), res, str(tot_completed) + '/' + str(num)] # [是否学完,[未完成的学习资源序号], 完成百分比]

def prev(_drivr,cinfo): # 预习
    num = int(cinfo[2]) # 预习资料个数
    trials = 0 # 尝试次数
    myprint('\t\tHandling: '+ '预习')
    check_res = prev_check(_drivr,cinfo) # 检查完成情况，得到还没完成的序号
    while not check_res[0]: # 没有学完
        Clickx(_drivr,COURSE_TABS_PREV) # 点击预习页
        time.sleep(0.5) # 等待预习页加载
        for i in check_res[1]: # 遍历每个没完成的序号
            spot = COURSE_TABS_PREV_CONTENT + '/li[' + str(i) + ']' + COURSE_TABS_PREV_CONTENT_DELTA_IMG
            Clickx(_drivr,spot) # 点击序号对应的资源就算预习
            time.sleep(0.8*(trials+1)) # 越往后尝试，间隔越长
            myprint('\t\t\t' + str(i) + '/' + str(num) + '(' + str(trials) + ')')
        trials += 1
        if trials >= 7: # 尝试次数太多，先放弃，往下继续
            myprint('\t\t\tToo many trials.')
            break
        check_res = prev_check(_drivr,cinfo) # 点完一遍以后重新检查，因为可能服务器反应不过来点击

def test_check(_drivr,cinfo): # [id,simp_nm,p,t,e,credit_hr]
    # 检查是否完成该课程自测
    num = int(cinfo[3]) #自测试题个数
    tot_completed = 0
    mybefore = int(cinfo[2]) # “自测”的完成情况在学习概况里显示在“预习”完成情况的后面
    res = []
    Clickx(_drivr,COURSE_TABS_STAT) # 点击学习概况
    time.sleep(0.5) # 等待学习概况加载
    for i in range(mybefore+1,mybefore+num+1): # 这个范围是学习概况中“自测”部分的始末位置
        spot = COURSE_TABS_STAT_CONTENT + '/div[' + str(i) + ']' + COURSE_TABS_STAT_CONTENT_DELTA_STAT
        if _drivr.find_element(by=By.XPATH,value=spot).text != '100分':
            res.append(i-mybefore) # 没拿到满分就把自测资源的内部序号加入列表
        else:
            tot_completed += 1
    return [not bool(len(res)), res, str(tot_completed) + '/' + str(num)] # [是否学完,[未完成的学习资源序号], 完成百分比]

def perform_test(_drivr,cinfo,cur): # 进行自测（选择题）
    # 打开答案文件
    with open(MYDIR + '/data/test/c' + cinfo[5] + '/' + cinfo[1] + '_' + str(cur) + '.txt',encoding='utf8') as answer:
        # 第一行是：题型种类数量，第一种题型下题目数量，第二种题型下题目数量，第三种题型下题目数量
        sub = list(map(int,answer.readline().strip('\n').split(' ')))
        for i in range(1,sub[0]+1):
            for j in range(1,sub[i]+1): # 遍历题型种类
                myanswer = answer.readline().strip('\n') # 读一行选项，如：ABD
                for choice in myanswer: # 对答案中的每一个选项（字符），计算其与字母A的unicode值之差，确定点击当前题目的第几个选项
                    spot = COURSE_TEST_PAGE_CONTENT + '/div[' + str(i) + ']/div[' + str(j) + ']/ul/li[' + str(ord(choice) - ord('A') + 1) + ']'
                    myprint('\t\t\t\t' + str(j) + '/' + str(sub[i]) + '||' + str(i) + '/' + str(sub[0]))
                    Clickx(_drivr,spot) # 点击某个选项
        time.sleep(0.5) # 全部选完后稍等
        Clickx(_drivr,COURSE_TEST_PAGE_CONTENT + '/a') # 提交
        Clickx(_drivr,'/html/body/div[6]/div/a') # 确认提交

def test(_drivr,cinfo): # 自测
    num = int(cinfo[3]) # 自测试卷数量
    trials = 0
    myprint('\t\tHandling: '+ '自测')
    check_res = test_check(_drivr,cinfo) # 检查当前自测分数
    while not check_res[0]: # 如果自测分数检查过后发现不是100
        Clickx(_drivr,COURSE_TABS_TEST) # 点击自测页
        time.sleep(0.5) # 等待自测页加载
        for i in check_res[1]: # 遍历没有做满分的自测题序号（从1开始）
            spot = COURSE_TABS_TEST_CONTENT + '/li[' + str(i) + ']' + COURSE_TABS_TEST_CONTENT_DELTA_TEST
            Clickx(_drivr,spot) # 点开一个测试卷
            myprint('\t\t\t' + str(i) + '/' + str(num) + '(' + str(trials) + ')')
            time.sleep(1) # 等待测试卷页面加载
            perform_test(_drivr,cinfo,i) # 填写答案
        detail(_drivr,cinfo) # 填完返回课程详情页
        time.sleep(1) # 等待课程详情页加载
        trials += 1
        if trials >= 2:
            myprint('\t\t\tToo many trials.')
            break
        check_res = test_check(_drivr,cinfo) # 做完题后检查是否满分

def exam_check(_drivr,cinfo): # [id,simp_nm,p,t,e,credit_hr]
    # 检查是否完成课程仿真考核
    num = int(cinfo[4]) # 仿真考核题目数量
    tot_completed = 0
    mybefore = int(cinfo[2]) + int(cinfo[3]) # “考核”的完成情况在学习概况里显示在“预习”和“自测”完成情况的后面
    res = []
    Clickx(_drivr,COURSE_TABS_STAT) # 点击学习概况
    time.sleep(0.5) # 等待学习概况加载
    for i in range(mybefore+1,mybefore+num+1): # 这个范围是学习概况中“仿真考核”部分的始末位置
        spot = COURSE_TABS_STAT_CONTENT + '/div[' + str(i) + ']' + COURSE_TABS_STAT_CONTENT_DELTA_STAT
        if _drivr.find_element(by=By.XPATH,value=spot).text != '100分':
            res.append(i-mybefore) # 没拿到满分就把自测资源的内部序号加入列表
        else:
            tot_completed += 1
    return [not bool(len(res)), res, str(tot_completed) + '/' + str(num)] # [是否学完,[未完成的学习资源序号], 完成百分比]

def perform_exam(_drivr,cinfo,cur,user_id): # 进行仿真考核 # [id,simp_nm,p,t,e,credit_hr]
    spot = COURSE_TABS_EXAM_CONTENT + '/li[' + str(cur) + ']' + COURSE_TABS_EXAM_CONTENT_DELTA_IMG
    a = input('\t\t\t准备进行仿真考核，当前第' + str(cur) + '个，请按回车键继续')
    Clickx(_drivr,spot) # 点击仿真考核资源
    a = input('\t\t\t请在浏览器中点击确定，之后请等待考核界面加载；加载完毕后，请站在原地不动，直接点击接受任务、完成任务一直到底，出现日志后按回车键以继续')
    # 找到*.exam文件并覆盖内容
    with open(MYDIR + '/settings.yaml','r',encoding='utf-8') as f:
        settings = yaml.full_load(f.read())
    resource_dir = settings['yysmart']['resource_path']
    if resource_dir[-1] == '/' or resource_dir[-1] == '\\':
        resource_dir = resource_dir[:-1]
    with open(MYDIR + '/data/exam/c' + cinfo[5] + '/' + cinfo[1] + '_' + str(cur) + '.txt','r',encoding='utf8') as f:
        exam_filename = f.read().strip('\n')
    exam_full_filename = resource_dir + '/' + exam_filename + '.exam'
    isok = False
    while isok == False:
        with open(exam_full_filename,'r',encoding='utf-8') as f:
            exam_content = f.read().strip('\n')
        pos = exam_content.find('score')
        if exam_content.find('{') >= 0:
            isok = True
        else:
            a = input('\t\t\t请重试（请确认已弹出操作日志和错误日志），或按n强制跳过')
            if a == 'n' or a == 'N':
                return
    replacement = exam_content[0:pos+7] + '100,"answer":""}'
    with open(exam_full_filename,'w',encoding='utf-8') as f:
        f.write(replacement)

    a = input('\t\t\t文件替换完成，请点击仿真考核中的退出，按回车键继续')
    time.sleep(1)
    a = input('\t\t\t此仿真考核已完成，请按回车键继续')

def exam(_drivr,cinfo,user_id): # 仿真考核
    num = int(cinfo[4]) # 仿真考核资源数量
    trials = 0
    myprint('\t\tHandling: '+ '仿真考核')
    check_res = exam_check(_drivr,cinfo) # 先检查是否完成了仿真考核
    while not check_res[0]: # 没有完成
        Clickx(_drivr,COURSE_TABS_EXAM) # 点击仿真考核页
        time.sleep(0.5) # 等待仿真考核页加载
        for i in check_res[1]: # 遍历没有做满分的仿真考核题
            myprint('\t\t\t' + str(i) + '/' + str(num) + '(' + str(trials) + ')')
            try:
                perform_exam(_drivr,cinfo,i,user_id) # 进行仿真考核
            except:
                pass
            time.sleep(1) # 稍等，在安装了yysmart的情况下，浏览器可能弹出警告
        detail(_drivr,cinfo) # 回到课程详情
        time.sleep(1) # 等待课程详情页加载
        trials += 1
        if trials >= 2:
            myprint('\t\t\tToo many trials.')
            break
        check_res = exam_check(_drivr,cinfo) # 仿真考核结束后检查是否满分

def check_all(_drivr,cinfo,exam_mode=False,check_only=False): # 检查课程完成情况
    detail(_drivr,cinfo) # 详情页
    prev_res = prev_check(_drivr,cinfo) # 检查预习情况
    test_res = test_check(_drivr,cinfo) # 检查自测情况
    exam_res = exam_check(_drivr,cinfo) # 检查仿真考核情况
    res = [False]
    if check_only:
        if prev_res[0] and test_res[0] and exam_res[0]:
            res[0] = True
        else:
            res[0] = False
    else:
        if exam_mode:
            if exam_res[0]:
                res[0] = True
        else:
            if prev_res[0] and test_res[0]:
                res[0] = True
    res.append([prev_res[2], test_res[2], exam_res[2]])
    return res
