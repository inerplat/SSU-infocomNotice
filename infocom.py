import requests
from bs4 import BeautifulSoup
import string
import smtplib
from email.mime.text import MIMEText
import time
import csv
recent=0

#time.sleep(60)
while (1):
    req = requests.get('http://infocom.ssu.ac.kr/rb/?c=2/38')
    html = req.text
    header = req.headers
    status = req.status_code
    is_ok = req.ok

    soup = BeautifulSoup(req.content,'html.parser', from_encoding='utf-8')


    number = soup.select('#bbslist > a')
    tmpmax=recent

    print(recent)
    if recent==0 :
        recent=int(number[0]['name'][1:])
        continue

    for now in number:
        nowNum=int(now['name'][1:])
        if nowNum>recent:
            if tmpmax<nowNum :
                tmpmax=nowNum
                print(tmpmax)
            print("new info")

            req2 = requests.get('http://infocom.ssu.ac.kr/rb/?c=2/38&uid='+str(nowNum))
            html2 = req2.text
            header2 = req2.headers
            status2 = req2.status_code
            is_ok2 = req2.ok
            soup2 = BeautifulSoup(req2.content,'html.parser', from_encoding='utf-8')
            title = soup2.select('#bbsview > div > div.subject > h1')
            #print(title[0].text)
            print(title)
            smtp = smtplib.SMTP('smtp.gmail.com', 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.login('inerplat.mailer@gmail.com', 'inerplat')

            content = soup2.select('#vContent')
            msg = MIMEText(content[0].text+'\n\n\n자세한 사항은 '+'http://infocom.ssu.ac.kr/rb/?c=2/38&uid='+str(nowNum)+'를 참고하시기 바랍니다.')
            msg['Subject'] = '[SSU-infocom] '+title[0].text
            
            cf = csv.reader(open('mailingList.csv','r',encoding='utf-8'))
            next(cf)
            for user in cf:
                msg['To'] = user[1]
                smtp.sendmail('notice',user[1], msg.as_string())

            smtp.quit()
    recent=tmpmax
    time.sleep(1800);


