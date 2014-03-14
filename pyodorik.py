#!/usr/bin/python
# -*- coding: utf8 -*-
# Soubor:  pyodorik.py
# Datum:   14.03.2014 11:48
# Autor:   Marek Nožka, marek <@t> tlapicka <d.t> net
# Licence: GNU/GPL 
# Úloha:   Jednoduché uživatelské rozhraní pro odorik.
############################################################################
#from __future__ import unicode_literals

import sys, os, httplib, urllib
import simplejson as json
from sys import stdin, stdout, stderr
############################################################################

root='/api/v1'
conffile=os.getenv('HOME')+'/.config/pyodorik.json'

def printHelp():
    print """pyOdorik
=====================

Konfigurace je uložene v ~/.config/pyodorik.json 

Seznam kontaktů
----------------

$ pyodorik list

Kredit
-------

$ pyodorik credit

Zpětné volání
--------------

$ pyodorik call 756123658
$ pyodorik call 123456789 756123658

Pokud je zadáno jen jednočíslo na bere se číslo telefonu z kterého 
chci volat z konfiguračního souboru.

V konfiguračním souboru si pro každého hostitele můžu nastavit jiné telefoní 
číslo.


Help
-------

$ pyodorik
$ pyodorik help

"""

def getAuth():
    """Funkce získá uživatelské jméno a heslo z konfiguračního souboru
    """
    try:
        conf=open( conffile, 'r' )
    except:
        stderr.write("Nemůžu otvřít soubor {}\n\n".format(conffile))
        sys.exit(10)
    try:
        auth=json.load(conf)['auth']
    except:
        stderr.write("V soubor {} je syntaktická chyba.\n\n".format(conffile))
        sys.exit(20)
    conf.close()
    
    return auth


def getFromAPI(method,URL,**kwargs):
    auth=getAuth()
    auth.update(kwargs)
    params = urllib.urlencode(auth)
    if method=='POST':    
        try:
            conn=httplib.HTTPSConnection("www.odorik.cz")
        except:
            stderr.write("chyba sítě.\n\n")
            sys.exit(30)
        conn.request('POST',root+URL,params)
        response = conn.getresponse()
        print response.status, response.reason
        data = response.read()
        conn.close()
        return data
    elif method=='GET':
        response=urllib.urlopen("https://www.odorik.cz"+root+URL+"?"+params)
        return response.read()


##############################################################################
if len(sys.argv) == 1 or sys.argv[1]=='help':
    printHelp()
    sys.exit(0)
elif sys.argv[1]=='list':
    contacts = getFromAPI("GET" , '/speed_dials.json')
    contacts = json.loads(contacts)
    for k in contacts:
        print k['shortcut'], k['name']
    sys.exit(0)
elif sys.argv[1]=='credit':
    print getFromAPI("GET" , '/balance')
    sys.exit(0) 
elif sys.argv[1]=='call':
    if len(sys.argv) == 4:
        caller = sys.argv[2]
        recipient = sys.argv[3]
    elif len(sys.argv) == 3:
        caller = sys.argv[2]

        try:
            conf=open( conffile, 'r' )
        except:
            stderr.write("Nemůžu otvřít soubor {}\n\n".format(conffile))
            sys.exit(10)
        try:
            default=json.load(conf)['default']
        except:
            stderr.write("V soubor {} je syntaktická chyba.\n\n".format(conffile))
            sys.exit(20)
        conf.close()
        try:
            recipient=default[os.getenv('HOST')]
        except:
            recipient=default['default']
    else:
        stderr.write('Zadejí číslo odkud voláš a kam\n\n')
        sys.exit(50)

    print "Volám z čísla "+caller
    print "     na číslo "+recipient
    print getFromAPI("POST" , '/callback', caller=caller, recipient=recipient)
    sys.exit(0) 


sys.exit(0)

while True:
    try:
        line = raw_input('app>> ')    
    except EOFError:
        exit(0)
    except KeyboardInterrupt:
        exit(1)
    except:
        stdout.write("ERROR\n")
