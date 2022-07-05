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
