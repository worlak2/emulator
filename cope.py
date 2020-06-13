# -*- coding: utf-8 -*-

from pathlib import Path
from queue import Queue
from sys import exit

from flask import Flask, request
from requests import get

app = Flask(__name__)
queue = Queue()
reroute_host = "http://shopsmsbot.com"


class SystemWork:
    hosts_path = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
    rename_host = "sms-activate.ru"

    def get_numbers(self):
        with open(Path("numbers.txt")) as read_number:
            for i in read_number.readlines():
                queue.put(i.rstrip())

    def find_hosts(self):
        text = ''
        for i in open(r'C:\\Windows\\System32\\drivers\\etc\\hosts').readlines():
            if self.rename_host in i:
                return text
            else:
                text = text + i

    def get_options(self, argument_action):
        if argument_action == '1':
            if self.rename_host not in open(self.hosts_path).read():
                ip = '127.0.0.1'
                open(self.hosts_path, 'a').write('\n{0} {1} \n'.format(ip, self.rename_host))
        elif argument_action == '2':
            if self.rename_host in open(self.hosts_path).read():
                newtext = self.find_hosts()
                open(self.hosts_path, 'w').write(
                    newtext)
                print('Чисто')
                exit()
            else:
                print('Чисто')
                exit()


def acsess_cancel(status, apikey):
    response = ""
    if status == '8':
        response = "ACCESS_CANCEL"
    elif status == '1':
        response = "ACCESS_READY"
    elif status == '6':
        response = "ACCESS_ACTIVATION"
    return response


def balance_return():
    return "ACCESS_BALANCE:1000.11"


def number_return():
    if not queue.empty():
        response = "ACCESS_NUMBER:{0}:{0}".format(queue.get_nowait())
    else:
        response = "NO_NUMBERS"
    return response


def result_return(apikey, status):
    url_path = "{0}/getsms?token={1}".format(reroute_host, apikey)
    response = get(url=url_path).text
    if "Not Sms" not in response:
        result = "STATUS_OK:{0}".format(response.split("code:")[1])
    else:
        result = "STATUS_WAIT_CODE"
    return result


def action_check(status_check, **kwargs):
    list_status = {"setStatus": acsess_cancel(**kwargs), "getBalance": balance_return(), "getNumber": number_return(),
                   "getStatus": result_return(**kwargs)}
    return list_status.get(status_check)


@app.route('/stubs/handler_api.php', methods=['GET'])
def handler():
    action = request.args.get('action')
    apikey = request.args.get('api_key')
    status = request.args.get('status')
    result = action_check(action, status=status, apikey=apikey)
    if result:
        return result
    return get(url="{0}/stubs/handler_api.php".format(reroute_host), params=request.args).text


if __name__ == '__main__':
    options = SystemWork()
    print("1. Обновить конфигурацию. \n2. Вернуть стандартную")
    options.get_options(str(input()))
    options.get_numbers()
    app.run(host='0.0.0.0', port='80', debug=False)
