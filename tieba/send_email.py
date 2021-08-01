import pymysql
import pandas as pd
import time, datetime
import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


# 连接数据库
def get_db_connection():
    host = 'localhost'
    port = 3306
    user = 'root'
    password = '1512007'
    database = 'test'
    conn = pymysql.connect(host=host,user=user,password=password,database=database,charset="utf8")
    print('数据库连接成功')
    return conn


# 查询SQL结果并生成execl
def get_execl(filepath):
    sql = 'select * from tieba_infor'
    conn = get_db_connection()
    # 直接使用pandas的read_sql即可转化成DataFrame
    df = pd.read_sql(sql,conn)
    print(df)
    df.to_excel(filepath)
    print(df.to_excel(filepath))
    print('已经生成Excel文件')


# 发送邮件
def sendmail(people,filepath):
    mail_msg = MIMEMultipart()
    mail_msg['Subject'] = '来李sir的一封信'
    mail_msg['From'] = 'm13520285560@163.com'
    smtp_addr = 'smtp.163.com'
    name = people + '@163.com', 'm13520285560@163.com'
    mail_msg['To'] = ','.join(name)
    password = 'MCHBBLZYVEJPNWRH'
    msg = '''
    <p>\n\t <h1>来自未来的信息!</h1></p>
    <p>\n\t <h3>请惠存！</h3></p>
    '''
    mail_msg.attach(MIMEText(msg, 'html', 'utf-8'))
    part1 = MIMEApplication(open(filepath, 'rb').read())
    part1.add_header('Content-Disposition', 'attachment', filename=('查询结果.xlsx'))
    mail_msg.attach(part1)
    try:
        s = smtplib.SMTP()
        s.connect(smtp_addr)
        s.login(mail_msg['From'], password)
        s.sendmail(mail_msg['From'], mail_msg['To'], mail_msg.as_string())
        s.quit()
    except Exception:
        print('error')
        print(traceback.format_exc())

def clean_database():
    engine_conn = 'mysql+pymysql://root:1512007@localhost:3306/tieba?charset=utf8'
    db = pymysql.connect("localhost", "root", "1512007", "test", charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    sql = 'truncate table tieba_infor'
    cursor.execute(sql)
    db.commit()
