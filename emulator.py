# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import requests
import sys
import os
import socket

print("1. Обновить конфигурацию. \n2. Вернуть стандартную")
work = str(input())
app = Flask(__name__)


# def run_cmd():
#    return str(socket.gethostbyname(socket.gethostname()))


def find_hosts():
    text = ''
    newtext = open(r'C:\\Windows\\System32\\drivers\\etc\\hosts', ).readlines()
    for i in newtext:
        if (i.find('sms-activate.ru') != -1):
            return text
        else:
            text = text + i


if (work == '1'):
    if (open(r'C:\\Windows\\System32\\drivers\\etc\\hosts').read().find('sms-activate.ru') == -1):
        ip = '127.0.0.1'
        open(r'C:\\Windows\\System32\\drivers\\etc\\hosts', 'a').write('\n{0} sms-activate.ru \n'.format(ip))
if (work == '2'):
    if (open(r'C:\\Windows\\System32\\drivers\\etc\\hosts').read().find('sms-activate.ru') != -1):
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


@app.route('/stubs/handler_api.php', methods=['GET'])
def handler():
    action = request.args.get('action')
    apikey = request.args.get('api_key')
    service = request.args.get('service')
    status = request.args.get('status')
    # phone=request.args.get('phone')
    id = request.args.get('id')
    if (action == 'getBalance'):
        myresponse = requests.get('https://sms-off.com/api/?route=getBalance&apikey={1}'.format(action, apikey))
        return 'ACCESS_BALANCE:' + str(myresponse.json()['balance'])
    if (action == 'getNumbersStatus'):
        return jsonify(
            {"vk_0": "116", "ok_0": "120", "wa_0": "171", "vi_0": "198", "tg_0": "110", "wb_0": "30", "go_0": "200",
             "av_0": "30", "av_1": "0", "fb_0": "208", "tw_0": "29", "ot_1": "0", "ub_0": "12", "qw_0": "30",
             "gt_0": "29", "sn_0": "30", "ig_0": "120", "ss_0": "30", "ym_0": "30", "ym_1": "0", "ma_0": "30",
             "mm_0": "87", "uk_0": "29", "me_0": "87", "mb_0": "89", "we_0": "30", "bd_0": "30", "kp_0": "30",
             "dt_0": "30", "ya_0": "30", "ya_1": "0", "mt_0": "85", "oi_0": "82", "fd_0": "30", "zz_0": "30",
             "kt_0": "30", "pm_0": "30", "tn_0": "30", "ot_0": "0"})
    if (action == 'getNumber'):
        myresponse = requests.get(
            'https://sms-off.com/api/?route=getPhone&service={0}&apikey={1}'.format(service, apikey))
        return 'ACCESS_NUMBER:86{0}:86{0}'.format(str(myresponse.json()['phone']))
    if (action == 'getStatus'):
        myresponse = requests.get(
            'https://sms-off.com/api/?route=getMessage&apikey={0}&phone={1}'.format(apikey, id[2:]))
        if (str(myresponse.json()['message']).find('No sms found') != -1):
            return 'STATUS_WAIT_CODE'
        if (str(myresponse.json()['message']).find('Unknown error') != -1):
            return 'STATUS_WAIT_CODE'
        else:
            maybe = str(myresponse.json()['message'])
            clear = [int(s) for s in maybe if s.isdigit()]
            new = ''
            for i in clear:
                new = new + str(i)
            # return 'STATUS_OK:' + maybe[maybe.rfind(" ") + 1:]
            return 'STATUS_OK:' + new
    if (action == 'setStatus'):
        if (status == '1'):
            return 'ACCESS_READY'
        elif (status == '6'):
            return 'ACCESS_ACTIVATION'
        elif (status == '8'):
            requests.get(
                'https://smsoff.com/api/?api/?route=addBlacklist&apikey={0}&phone={1}'.format(apikey, id))
            return 'ACCESS_CANCEL'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80', debug=False)
