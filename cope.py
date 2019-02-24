# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import requests
import sys

print("1. Обновить конфигурацию. \n2. Вернуть стандартную")
work = str(input())
app = Flask(__name__)


# def run_cmd():
#    return str(socket.gethostbyname(socket.gethostname()))


def find_hosts():
    text = ''
    newtext = open(r'C:\\Windows\\System32\\drivers\\etc\\hosts', ).readlines()
    for i in newtext:
        if (i.find('smsactivation.pro') != -1):
            return text
        else:
            text = text + i


if (work == '1'):
    if (open(r'C:\\Windows\\System32\\drivers\\etc\\hosts').read().find('smsactivation.pro') == -1):
        ip = '127.0.0.1'
        open(r'C:\\Windows\\System32\\drivers\\etc\\hosts', 'a').write('\n{0} smsactivation.pro \n'.format(ip))
if (work == '2'):
    if (open(r'C:\\Windows\\System32\\drivers\\etc\\hosts').read().find('smsactivation.pro') != -1):
        newtext = find_hosts()
        open(r'C:\\Windows\\System32\\drivers\\etc\\hosts', 'w').write(
            newtext)
        print('Чисто')
        sys.exit()
    else:
        print('Чисто')
        sys.exit()


# os.system(
#     'netsh interface portproxy add v4tov4 listenport=80 listenaddress={0} connectport=8080 connectaddress={0}'.format(run_cmd()))



@app.route('/get/money/<apikey>', methods=['GET'])
def money(apikey):
    # phone=request.args.get('phone')
    myresponse = requests.get('https://sms-off.com/api/?route=getBalance&apikey={0}'.format(str(apikey)))
    return  str(myresponse.json()['balance'])


@app.route('/get/number/<service>/<apikey>/cn', methods=['GET'])
def get_number(service,apikey):
    if(str(service)=='17'):
        service='vk'
    if(str(service)=='11'):
        service='OK'
    myresponse = requests.get(
        'https://sms-off.com/api/?route=getPhone&service={0}&apikey={1}'.format(str(service), str(apikey)))
    return '86{0}'.format(str(myresponse.json()['phone']))


@app.route('/get/sms/<number>/<apikey>/cn', methods=['GET'])
def sms_get(number, apikey):
    myresponse = requests.get(
        'https://sms-off.com/api/?route=getMessage&apikey={0}&phone={1}'.format(str(apikey), str(number[2:])))
    if (str(myresponse.json()['message']).find('No sms found') != -1):
        return 'Error|Not Receive'
    if (str(myresponse.json()['message']).find('Unknown error') != -1):
        return 'Error|Not Receive'
    else:
        maybe = str(myresponse.json()['message'])
        clear = [int(s) for s in maybe if s.isdigit()]
        new = ''
        for i in clear:
            new = new + str(i)
        # return 'STATUS_OK:' + maybe[maybe.rfind(" ") + 1:]
        return new




@app.route('/toblacklist/<number>/<apikey>/cn', methods=['GET'])
def black_list(number,apikey):
    response=requests.get(
        'http://sms-off.com/api/?route=addBlacklist&apikey={0}&phone={1}'.format(str(apikey), str(number[2:])))
    return 'Message|Had add black list'





if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=False)
