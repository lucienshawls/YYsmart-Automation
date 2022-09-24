import base
from base import *
import codecs

def trans_codecs(mode=0):
    if mode != 0 and mode !=1:
        raise RuntimeError('输入错误')
    with open(MYDIR + '/students/data_file_list.txt','r',encoding='utf-8') as f:
        filenames = f.read().strip().split('\n')
    for filename in filenames:
        file_full_name = MYDIR + '/students/' + filename + '.csv'
        try :
            with open(file_full_name,'rb') as f:
                data = f.read()
                if data[:3] == codecs.BOM_UTF8:
                    myencode = 1
                else:
                    myencode = 0
            if myencode != mode:
                with open(file_full_name,'wb') as f:
                    if mode == 0:
                        f.write(data[3:])
                    else:
                        f.write(codecs.BOM_UTF8 + data)
        except:
            pass

def main():
    mystr = '''\
请选择：
0. 将students下相关文件统一为utf-8编码(不带BOM)
1. 将students下相关文件统一为utf-8-sig编码(带BOM)'''
    print(mystr)
    a = input('')
    trans_codecs(int(a))

if __name__ == '__main__':
    main()