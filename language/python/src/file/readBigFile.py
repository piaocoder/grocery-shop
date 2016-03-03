#!/usr/bin/python
#coding:utf8
import threading     #载入多线程模块
import time          #载入时间模块
import os            #载入os模块
import shutil        #载入shutil模块
import re            #载入re正则模块

fuhao=os.linesep     #换行符
start_time=int(time.strftime('%H%M%S'))  #执行程序开始时间
print start_time
def count_cpu_heshu():                      #统计cpu核数函数
    file=open('/proc/cpuinfo')
    cpu_sum=[]
    for line in file.readlines():
        cpu_he=re.findall('^processor',line)
        if len(cpu_he)==1:
           cpu_sum.append(cpu_he)
        else:
           continue
    file.close()
    return len(cpu_sum)                    #返回cpu函数

def count_memory_size():                   #统计系统内存大小函数
    mem_sum=int(os.popen("free -m|awk  '{print $2}'|sed -n '2p'").readline().strip())  #统计内存的shell
    return mem_sum                                                                     #返回内存大小

def nginx_log_fenge():                    #因nginx日志太大，需要按500M分割，建立此函数进行分割日志
    if os.path.exists('/data/logs/nginx_tmp/')!=True:       #分割日志的临时目录
       os.makedirs('/data/logs/nginx_tmp/')
    if os.path.exists('/data/logs/nginx_tmp_binfa/')!=True: #并发目录
       os.makedirs('/data/logs/nginx_tmp_binfa/')
    if os.path.exists('/data/logs/nginx_tmp_txt01/')!=True:  #time记录txt目录 
       os.makedirs('/data/logs/nginx_tmp_txt01/')
    if os.path.exists('/data/logs/nginx_tmp_txt02/')!=True:  #url记录txt目录 
       os.makedirs('/data/logs/nginx_tmp_txt02/')
    if os.path.exists('/data/logs/nginx_tmp_chuli/')!=True:  #处理所有txt目录
       os.makedirs('/data/logs/nginx_tmp_chuli/')
    nginx_log_name=os.listdir('/data/logs/nginx_log')[0].strip()  #切割日志名
    nginx_file='/data/logs/nginx_log/%s' %nginx_log_name           #切割日志名及路径
    file=open(nginx_file)                   #nginx日志文件路径
    sizehint=int(count_memory_size() / count_cpu_heshu() * 0.5 * 1024 * 1024)              #此数字是按字节进行计算，这里大小为内存除以cpu核数剩以0.5得到的结果为500M
    position=0                               #当前位置为0
    file_num=1                               #分割文件名默认加1
    while True:                             #当条件为真执行，为假退出。
          lines = file.readlines(sizehint)   #读文件
          file_name='/data/logs/nginx_tmp/dd_access%d' %file_num  #分割成功的文件名
          file01=open(file_name,'w')       #写文件
          file01.writelines(lines)         #把读取的单个1G文件写到文件名中
          if  file.tell() - position > 0: #如果分割的位置大于默认位置就继续执行，否则就退出。
              position = file.tell()      #替换位置
              file_num=file_num+1
              continue
          else:
              break
    file.close()
    file01.close()
    os.remove(file_name)
    time.sleep(300)

def nginx_log_time_count(file_name01):         #nginx分析日志函数
    file_name='/data/logs/nginx_tmp_binfa/%s' %file_name01    #并发日志名
    file_txt='/data/logs/nginx_tmp_txt01/%s.txt' %file_name01        #执行shell结果保存目录
    cmd="awk '{print $4}' %s|awk -F / '{print $NF}'|awk -F : '{print $2$3$4$5}'  2>/dev/null|sort 2>/dev/null|uniq -c 2>/dev/null|sort -nr 2>/dev/null|head -n 1 > %s" %(file_name,file_txt)  #分析脚本
    os.system(cmd)  #执行shell命令
    fuhao_cmd='%s' %fuhao
    f=open(file_txt)
    f1=open('/data/logs/nginx_tmp_chuli/time_sum.txt','a')
    for line in f.readlines():
         time_single_max= line.split()[0]   #单个文件连接数
         f1.writelines(time_single_max)
         f1.write(fuhao_cmd)
    f.close()
    f1.close()

def nginx_log_url_count(file_name01):         #nginx分析日志函数
    file_name='/data/logs/nginx_tmp_binfa/%s' %file_name01  #并发日志名
    file_txt='/data/logs/nginx_tmp_txt02/%s.txt' %file_name01   #执行shell结果保存目录
    cmd="awk '{print $7}' %s  2>/dev/null|sort 2>/dev/null|uniq -c 2>/dev/null|sort -rn 2>/dev/null|head -n 200 > %s " %(file_name,file_txt)  #分析脚本
    os.system(cmd)  #执行shell命令
    fuhao_cmd='%s' %fuhao
    f=open(file_txt)
    f1=open('/data/logs/nginx_tmp_chuli/url_sum.txt','a')
    for line in f.readlines():          #把url_status里面每一行值以列表方法增加到url_count列表里面
        f1.writelines(line.strip())
        f1.write(fuhao_cmd)
    f.close()
    f1.close()

def dxc_call_time_count():                       #多线程调用分析日志函数
    file_name_read=[]                        #文件名读取列表
    f=os.listdir('/data/logs/nginx_tmp_binfa/')   #显示data/logs/nginx_tmp/目录下所有文件
    for read_filename in f:
        filename_chuancan=read_filename.strip()  #单个文件名
        filename=threading.Thread(target=nginx_log_time_count,args=(filename_chuancan,))  #建立多线程
        file_name_read.append(filename)         #添加线程到file_name_read列表
    filename_sum=range(len(file_name_read))     #统计文件名数量
    for line in filename_sum:
        file_name_read[line].start()            #启动线程
    for line in filename_sum:
        file_name_read[line].join()             #等待多线程结束后，就结束进程。

def dxc_call_url_count():                       #多线程调用分析日志函数
    file_name_read=[]                        #文件名读取列表
    f=os.listdir('/data/logs/nginx_tmp_binfa/')   #显示data/logs/nginx_tmp/目录下所有文件
    for read_filename in f:
        filename_chuancan=read_filename.strip()  #单个文件名
        filename=threading.Thread(target=nginx_log_url_count,args=(filename_chuancan,))  #建立多线程
        file_name_read.append(filename)         #添加线程到file_name_read列表
    filename_sum=range(len(file_name_read))     #统计文件名数量
    for line in filename_sum:
        file_name_read[line].start()            #启动线程
    for line in filename_sum:
        file_name_read[line].join()             #等待多线程结束后，就结束进程。

def time_count_chuli():                         #time处理函数
    f=open('/data/logs/nginx_tmp_chuli/time_sum.txt')
    time_max=[]
    for count in f:
       time_max.append(int(count.strip()))
    f.close()
    return max(time_max)

def url_count_chuli():                          #url处理函数
    f=open('/data/logs/nginx_tmp_chuli/url_sum.txt')
    url_max=[]
    for count in f:
        url_max.append(count.split())
    f.close()
    return url_max

def write_report_email():                       #写文件用来发email
    fuhao_cmd='%s' %fuhao
    time_max=time_count_chuli()                 #接受time处理函数返回的结果
    url_max=url_count_chuli()                   #接受url处理函数返回的结果
    file=open('/data/logs/nginx_log_email_tmp.txt','w')
    file.write("nginx单秒的最大请求数为:%d" %time_max)
    file.write(fuhao_cmd)
    file.write('nginx连接数TOP100排序')
    file.write(fuhao_cmd)
    new_dict={}                       #定义一字典用来统计连接重复数,得到字典结果为连接地址:连接重复数
    for i in url_max:                 #遍历url_max列表
         new_dict[i[1]] = new_dict.get(i[1],0) + int(i[0])    #i[1]表示连接地址,i[0]表示连接重复数,new_dict[i[1]]表示把列表中的地址重复数与地址连接交换,如果连接相同，就累加连接重复数.
    n_dict = {}                       #定义一字典用来恢复原来的连接重复数:连接地址
    for k in new_dict:                #遍历new_dict字典
         n_dict[new_dict[k]] = k      #k表示连接地址,new_dict[k]表示连接重复数,最后n_dict结果为连接重复数:连接地址
    url_count=sorted(n_dict.iteritems(),key=lambda dict1:dict1[0],reverse=True) #对字典进行排序
    for line in url_count:
        file.write('连接重复数:')
        file.write(str(line[0]))              #把连接重复数写到日志临时文件
        file.write('   ')
        file.write('http://d.m1905.com')      #写连接头文件
        file.write(str(line[1]))              #把连接地址写到日志临时文件
        file.write(fuhao_cmd)
    file.close()
    file=open('/data/logs/nginx_log_email_tmp.txt','r')   #读取日志临时文件
    row=0
    file01=open('/data/logs/nginx_log_email.txt','w')     #写文件
    for line in file.readlines():
        row=row+1                                         #row表示行数
        if row <= 102:                                    #读取文件到102行，大于102行就退出
           file01.write(line)
        else:
           break
    file.close()
    file01.close()
    os.remove('/data/logs/nginx_log_email_tmp.txt')       #删除日志临时文件  
    os.remove('/data/logs/nginx_tmp_chuli/time_sum.txt')       #删除time_sum文件 
    os.remove('/data/logs/nginx_tmp_chuli/url_sum.txt')       #删url_sum文件  

def rmdir_nginx_log_mulu():       #清空日志目录函数
    shutil.rmtree('/data/logs/nginx_tmp/')  #清空日志临时目录，供新日志存放
    os.mkdir('/data/logs/nginx_tmp/')
    shutil.rmtree('/data/logs/nginx_log/')  #清空日志目录，供新日志存放
    os.mkdir('/data/logs/nginx_log')

def main():
    shutil.rmtree('/data/logs/nginx_tmp_chuli')  #清空日志临时目录，供新日志存放
    os.mkdir('/data/logs/nginx_tmp_chuli')
    cpu_he=count_cpu_heshu()                                       #cpu核数
    while len(os.listdir('/data/logs/nginx_tmp/'))>0:   #动态统计分割日志文件个数
        f=os.listdir('/data/logs/nginx_tmp/')          #动态统计分割日志文件
        key=0                                                       #默认key为0
    while (key<=cpu_he-1 and key<len(f)):      #对cpu核数进行对比
        name = '/data/logs/nginx_tmp/%s' %f[key]    #日志文件名
        shutil.move(name,'/data/logs/nginx_tmp_binfa/')  #移动日志文件，为了减少负载太高
        key=key+1
        dxc_call_time_count()
        dxc_call_url_count() 
        shutil.rmtree('/data/logs/nginx_tmp_binfa/')
        os.mkdir('/data/logs/nginx_tmp_binfa/')
        shutil.rmtree('/data/logs/nginx_tmp_txt01/')
        os.mkdir('/data/logs/nginx_tmp_txt01/')
        shutil.rmtree('/data/logs/nginx_tmp_txt02/')
        os.mkdir('/data/logs/nginx_tmp_txt02/')
    write_report_email()
    rmdir_nginx_log_mulu() 

nginx_log_fenge()
main()
stop_time=int(time.strftime('%H%M%S'))
print stop_time
#os.system('/usr/bin/python /root/liu_shell/nginx_log/send_email.py')   #send_email.py把结果发邮件到开发人员
