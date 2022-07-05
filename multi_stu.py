import base
from base import *
import single_stu

def get_all_sinfo(filename,submit=False,verify=True):
    sl = mycsv.read(MYDIR + '/students/' + filename + '.csv') # 读取学生名单
    res = []
    for stu in sl:
        if stu[12] == 'exclude': # 被exclude标记的那一行被跳过
            continue # 直接看下一行
        sinfo = { # 单个学生信息
            'accnt':[stu[0],stu[1]],        # 账号密码
            'userid':'',                    # 内部账号
            'name':stu[11],                 # 学生姓名
            'credit_hr':stu[2],             # 课程学时
            'options':{                     # 修读选项
                'an':bool(int(stu[3])),     # 安
                'gu':bool(int(stu[4])),     # 固
                'vu':bool(int(stu[5])),     # 注
                'ds':bool(int(stu[6])),     # 冻
                'gs':bool(int(stu[7])),     # 公
                'ug':bool(int(stu[8])),     # 生
                'vsyc':bool(int(stu[9])),   # 中药
                'heig':bool(int(stu[10])),  # 合成
            }
        }
        res.append(sinfo) # 将单个学生信息加入总表，最后返回
    return res

def mysubmit(filenames, mode):
    stu_list = []
    for filename in filenames:
        if len(filename) == 0:
            continue
        stu_list += get_all_sinfo(filename) # 获得包含很多条记录的列表，每个记录是学生信息字典sinfo
    result = [] # 将会包含所有提交或仅验证的学生的课程验证结果

    for stu in stu_list:
        try:
            if mode == 'auto' or mode == 'exam': # 如果提交
                myprint('Completing the learning tasks...\n')
                if mode == 'exam':
                    myprint('Completing the simulation exams part...\n')
                    res = single_stu.mysubmit(stu,check_only=False,exam_mode=True)
                else: # mode == 'auto'
                    myprint('Completing the preview and test part...\n')
                    res = single_stu.mysubmit(stu,check_only=False,exam_mode=False) # 开始
            else: # 如果仅验证
                myprint('Checking for completion...\n')
                res = single_stu.mysubmit(stu,check_only=True,exam_mode=False) # 开始，但是仅验证
        except:
            ## 处理这个学生时发生错误，填写相关信息
            res = {
                'res': False,
                'info': 'An error occured',
                'courses':{}
            }
            pass
        finally:    
            myprint(res['info']) # 打印返回的消息
            for course in res['courses'].items(): # 详细写出预习、自测、仿真考核的完成情况
                myprint('\t' + CORRES[course[0]] + '：Prev: ' + course[1][1][0] + ', Test: ' + course[1][1][1] + ', Exam: ' + course[1][1][2])
            myprint('')
            # 将结果打包加入结果列表
            result.append({'name':stu['name'],'stuid':stu['accnt'][0],'info':res['info'],'courses':res['courses'].copy()})

    myprint('Overview: (Name, StuID, Prev, Test, Exam)')
    for stu in result: # 输出总览
        myprint('\t' + stu['name'] + stu['stuid'] + ': ' + stu['info'])
        for course in stu['courses'].items():
            myprint('\t\t' + CORRES[course[0]] + '：Prev: ' + str(course[1][1][0]) + ', Test: ' + str(course[1][1][1]) + ', Exam: ' + str(course[1][1][2]))
        myprint('')
    myprint('')

def main():
    with open(MYDIR + '/data_file_list.txt','r',encoding='utf-8') as f:
        # filenames = ['filename1', 'filename2', 'template',]
        filenames = f.read().strip().split('\n')
    ## mode: check, auto, exam
    with open(MYDIR + '/settings.json','r',encoding='utf-8') as g:
        settings = json.loads(g.read())
    mode = settings['runtime']['mode']
    mysubmit(filenames=filenames, mode = mode)

if __name__ == '__main__':
    st = datetime.datetime.now()
    myprint('='*30)
    myprint('= ' + str(st) + ' =')
    myprint('='*50)
    try:
        main()
    except:
        myprint('The program failed to run.')
    ed = datetime.datetime.now()
    myprint('='*50)
    myprint('==' + str(ed) + '==')
    myprint('='*30)
