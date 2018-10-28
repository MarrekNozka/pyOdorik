#!/usr/bin/env python3
# -*- coding: utf8 -*-
# Soubor:  pyodorik.py
# Datum:   14.03.2014 11:48
# Autor:   Marek Nožka, marek <@t> tlapicka <d.t> net
# Licence: GNU/GPL
# Úloha:   Jednoduché uživatelské rozhraní pro odorik.
############################################################################
import sys
import os
import subprocess
import http.client
import urllib.request
import urllib.parse
import urllib.error
import simplejson as json
import configparser
from sys import stdout, stderr
import os.path
############################################################################
root = '/api/v1'
conffile = os.getenv('HOME')+'/.config/pyodorik.ini'


def printHelp():
    print("""pyOdorik
=====================

Konfigurace je uložene v ~/.config/pyodorik.ini

Seznam kontaktů
----------------

$ pyodorik list

Kredit
-------

$ pyodorik credit

Zpětné volání
--------------

$ pyodorik call 756 123 658
$ pyodorik call 123 456 789 - 756 123 658

Pokud je zadáno jen jedno číslo na bere se číslo telefonu z kterého
chci volat z konfiguračního souboru.

V konfiguračním souboru si pro každého hostitele můžu nastavit jiné výchozí
telefoní číslo.


Help
-------

$ pyodorik
$ pyodorik help

""")


def getAuth():
    '''
    Funkce získá uživatelské jméno a heslo z konfiguračního souboru
    '''
    if not os.path.isfile(conffile):
        stderr.write('''
Konfigurační soubor {} neexistuje!
Příklad konfiguračního souboru najdeš na adrese:
https://github.com/MarrekNozka/pyOdorik/blob/master/pyodorik.ini

'''.format(conffile))
        sys.exit(10)

    config = configparser.ConfigParser()
    config.read(conffile)
    if 'auth' in config and \
            'user' in config['auth'] and 'password' in config['auth']:
        return config['auth']
    else:
        stderr.write('''
V konfiguračním souboru {} je třeba sekce

[auth]
password = topsecpass
user = abc123456

Příklad konfiguračního souboru najdeš na adrese:
https://github.com/MarrekNozka/pyOdorik/blob/master/pyodorik.ini

'''.format(conffile))
        sys.exit(20)


def getFromAPI(method, URL, **kwargs):
    auth = getAuth()
    auth.update(kwargs)
    params = urllib.parse.urlencode(auth)
    try:
        conn = http.client.HTTPSConnection("www.odorik.cz")
    except:
        stderr.write("chyba sítě.\n\n")
        sys.exit(30)
    if method == 'POST':
        conn.request('POST', root+URL, params)
    elif method == 'GET':
        conn.request('GET', root+URL+'?'+params)
    else:
        return False
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    conn.close()
    return data


##############################################################################


if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == 'help':
        printHelp()
        sys.exit(0)
    elif sys.argv[1] == 'list':
        contacts = getFromAPI("GET", '/speed_dials.json')
        contacts = json.loads(contacts)
        for k in contacts:
            print(k['shortcut'], k['name'])
        sys.exit(0)
    elif sys.argv[1] == 'credit':
        print('Kredit: {} Kč'.format(getFromAPI("GET",
                                                '/balance').decode('ascii')))
        sys.exit(0)
    elif sys.argv[1] == 'call':
        if len(sys.argv) == 4:
            caller = sys.argv[2]
            recipient = sys.argv[3]
        elif len(sys.argv) == 3:
            recipient = sys.argv[2]
            try:
                conf = open(conffile, 'r')
            except:
                stderr.write("Nemůžu otvřít soubor {}\n\n".format(conffile))
                sys.exit(10)
            try:
                default = json.load(conf)['default']
            except:
                stderr.write("V soubor {} je syntaktická"
                             "chyba.\n\n".format(conffile))
                sys.exit(20)
            conf.close()
            try:
                caller = default[subprocess.check_output(["hostname"]).strip()]
            except:
                caller = default['default']
        else:
            stderr.write('Zadejí číslo odkud voláš a kam\n\n')
            sys.exit(50)
        print("Volám z čísla "+caller)
        print("     na číslo "+recipient)
        print(getFromAPI("POST", '/callback', caller=caller, recipient=recipient))
        sys.exit(0)

    sys.exit(0)

while True:
    try:
        line = input('app>> ')
    except EOFError:
        exit(0)
    except KeyboardInterrupt:
        exit(1)
    except:
        stdout.write("ERROR\n")
