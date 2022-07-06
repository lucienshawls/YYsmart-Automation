import base
from base import *
BASE_DRIVER_OPTIONS = ["--no-sandbox","--disable-dev-shm-usage","--disable-gpu"]
HEADLESS_OPTIONS = ["--headless","window-size=1920x1080","blink-settings=imagesEnabled=false"]
SETTINGS = {
    "runtime":{
        "mode": "check"
    },
    "driver":{
        "browser": "chrome",
        "driver_path": "",
        "options": BASE_DRIVER_OPTIONS
    },
    "yysmart":{
        "resource_path": "",
        "user_profile_path": ""
    }
}

settings_file = MYDIR + '/settings.json'
if os.path.exists(settings_file):
    with open(settings_file,'r',encoding='utf-8') as f:
        SETTINGS = json.loads(f.read())
def myverify(stu_list,set_skip=False): # 确认学生信息是否正确
    incorrect = []
    skip = []
    if set_skip: # “验证信息正确”和“跳过某些学生记录不提交”代码逻辑相同，故整合
        notify = "，是否加入提交列表" # 设置提示语
    else:
        notify = "，请确认"
    for sinfo in stu_list:
        mytake = []
        notake = []
        for option in sinfo['options'].items():
            if(option[1]): # 修读
                mytake.append(CORRES[option[0]]) # 获取修读的课程中文名字，加入列表
            else:
                notake.append(CORRES[option[0]]) # 获取不修读的课程中文名字，加入列表
        if len(mytake) == 0:
            mytake = ['（无）']
        if len(notake) == 0:
            notake = ['（无）']
        confirm = input(sinfo['name'] + '同学（学号为：' + sinfo['accnt'][0] +  '）修读' + sinfo['period'] + '学时GMP课程，' + '修读以下课程：' + '、'.join(mytake) + '，不修读以下课程：' + '、'.join(notake) + notify)
        if confirm != 'y' and confirm != 'Y':
            incorrect.append(sinfo['name']) # 按N，验证不通过（将学生姓名加入列表）或跳过提交（不做任何事）
        else:
            skip.append(sinfo) # 按Y，验证通过（不做任何事）或不跳过提交（将学生信息字典加入提交的列表）
    if set_skip: # 根据不同的模式返回不一样的列表
        return skip # 这里存储的是不被跳过的学生信息列表
    else:
        return [not len(incorrect),incorrect] # 这里存储的是[是否完全验证通过,不通过的学生姓名名单（列表）]
def clear_screen():
    if os.name == 'nt':
        a = os.system('cls')
    else:
        a = os.system('clear')

def config_settings_browser_headless(last_msg):
    prompt_text = '''菜单列表-浏览器模式选择
    1. 使用无头模式（不显示浏览器窗口）
    2. 不使用无头模式（显示浏览器窗口）
    0. 返回上级菜单且不进行更改
    '''
    err_msg = ''
    while True:
        clear_screen()
        print(last_msg)
        print(err_msg)
        print(prompt_text)
        a = input('请选择（输入序号后按回车）:')
        if a == '1':
            SETTINGS['driver']['options'] = BASE_DRIVER_OPTIONS[:] + HEADLESS_OPTIONS[:]
        elif a == '2':
            SETTINGS['driver']['options'] = BASE_DRIVER_OPTIONS[:]
        elif a == '0':
            return
        else:
            err_msg = '==输入有误，请重新输入==\n'
            continue
        err_msg = ''
        break

def config_settings_browser_driver(last_msg):
    prompt_text = '''菜单列表-配置driver
    1. driver路径置空（请确保driver所在路径被写入PATH环境变量）
    2. 手动配置driver
        若准备选择此项，请先根据自己的浏览器版本下载对应的driver.
        如果使用chrome浏览器，请去搜索引擎搜索：chromedriver下载
        如果使用edge浏览器，请去搜索引擎搜索：msedgedriver下载
        若下载得到的是压缩文件，请解压成单个文件并将其置入本程序路径下，然后输入2并按回车。
        请确保已经选择了浏览器。如果未选择，请输入0先回到上一步进行选择。
    0. 返回上级菜单且不进行更改
    '''
    err_msg = ''
    while True:
        clear_screen()
        print(last_msg)
        print(err_msg)
        print(prompt_text)
        a = input('请选择（输入序号后按回车）:')
        if a == '1':
            SETTINGS['driver']['driver_path'] = ''
        elif a == '2':
            if os.path.exists(MYDIR + '\\chromedriver.exe'):
                SETTINGS['driver']['driver_path'] = MYDIR + '\\chromedriver.exe'
            elif os.path.exists(MYDIR + '\\msedgedriver.exe'):
                SETTINGS['driver']['driver_path'] = MYDIR + '\\msedgedriver.exe'
            elif os.path.exists(MYDIR + '/chromedriver'):
                SETTINGS['driver']['driver_path'] = MYDIR + '/chromedriver'
            elif os.path.exists(MYDIR + '/msedgedriver'):
                SETTINGS['driver']['driver_path'] = MYDIR + '/msedgedriver'
            else:
                err_msg = '==未检测到当前目录的driver, 请确保driver未被更名==\n'
                continue
        elif a == '0':
            return
        else:
            err_msg = '==输入有误，请重新输入==\n'
            continue
        err_msg = ''
        break

def config_settings_browser_choose(last_msg):
    prompt_text = '''菜单列表-浏览器选择
    1. 使用Microsoft Edge (推荐Windows用户使用)
    2. 使用Google Chrome (国内网络环境难以配置driver)
    0. 返回上级菜单且不进行更改
    '''
    err_msg = ''
    while True:
        clear_screen()
        print(last_msg)
        print(err_msg)
        print(prompt_text)
        a = input('请选择（输入序号后按回车）:')
        if a == '1':
            SETTINGS['driver']['browser'] = 'edge'
        elif a == '2':
            SETTINGS['driver']['browser'] = 'chrome'
        elif a == '0':
            return
        else:
            err_msg = '==输入有误，请重新输入==\n'
            continue
        err_msg = ''
        break

def config_settings_browser(last_msg):
    prompt_text = '''菜单列表-浏览器配置
    1. 选择浏览器
    2. 配置driver
    3. 是否开启无头模式
    0. 返回上级菜单
    '''
    err_msg = ''
    while True:
        clear_screen()
        print(last_msg)
        print(err_msg)
        print(prompt_text)
        a = input('请选择（输入序号后按回车）:')
        if a == '1':
            config_settings_browser_choose('选择浏览器')
        elif a == '2':
            config_settings_browser_driver('配置driver')
        elif a == '3':
            config_settings_browser_headless('选择是否使用无头模式')
        elif a == '0':
            return
        else:
            err_msg = '==输入有误，请重新输入==\n'
            continue
        err_msg = ''

def config_settings_mode(last_msg): # done
    prompt_text = '''菜单列表-模式选择
    1. 检查各课程任务完成情况（check）
    2. 自动完成预习和自测任务（auto）
    3. 半自动完成仿真考核任务（exam）
    0. 返回上级菜单且不进行更改
    '''
    err_msg = ''
    while True:
        clear_screen()
        print(last_msg)
        print(err_msg)
        print(prompt_text)
        a = input('请选择（输入序号后按回车）:')
        if a == '1':
            SETTINGS['runtime']['mode'] = 'check'
        elif a == '2':
            SETTINGS['runtime']['mode'] = 'auto'
        elif a == '3':
            if os.name != 'nt':
                err_msg = '==非Windows系统不可选择此项==\n'
                continue
            else:
                SETTINGS['runtime']['mode'] = 'exam'
        elif a == '0':
            return
        else:
            err_msg = '==输入有误，请重新输入==\n'
            continue
        err_msg = ''
        break

def config_settings(last_msg):
    prompt_text = '''菜单列表-配置设置
    1. 选择运行模式
    2. 配置浏览器和driver
    3. 设置药育平台软件相关路径
    4. 将设置写入文件（必须在此程序退出前写入，否则设置将丢失）
    0. 返回至主菜单
    '''
    err_msg = ''
    while True:
        clear_screen()
        print(last_msg)
        print(err_msg)
        print(prompt_text)
        a = input('请选择（输入序号后按回车）:')
        if a == '1':
            config_settings_mode('选择运行模式')
        elif a == '2':
            config_settings_browser('配置浏览器和driver')
        elif a == '3':
            pass
        elif a == '4':
            settings = str(SETTINGS).replace('\\','\\\\').replace("'",'"')
            with open(MYDIR + '/settings.json','w',encoding='utf-8') as f:
                f.write(settings)
        elif a == '0':
            return
        else:
            err_msg = '==输入有误，请重新输入==\n'
            continue
        err_msg = ''

def home(last_msg):
    prompt_text ='''菜单列表-主菜单
    1. 检查程序资源完整性
    2. 完成程序的基本配置
    3. 创建或修改学生信息
    4. 验证设置和学生信息
    0. 退出
    '''
    err_msg = ''
    while True:
        clear_screen()
        print(last_msg)
        print(err_msg)
        print(prompt_text)
        a = input('请选择（输入序号后按回车）:')
        if a == '1':
            return
        elif a == '2':
            config_settings('完成程序的基本配置')
        elif a == '3':
            pass
        elif a == '4':
            pass
        elif a == '0':
            return

        else:
            err_msg = '==输入有误，请重新输入==\n'
            continue
        err_msg = ''

def main():
    a = input('此辅助程序可帮助用户完成基本设置，按回车键继续...')
    home(last_msg='辅助程序')
    # print(SETTINGS)
if __name__ == '__main__':
    main()