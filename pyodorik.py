#!/usr/bin/env python3
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
import re
import unicodedata
from os.path import basename

############################################################################


class PyOdorik:
    root = "/api/v1"
    conffile = os.getenv("HOME") + "/.config/pyodorik.ini"
    hostname = subprocess.check_output(["hostname"]).strip().decode("ascii")

    def __init__(self):
        if not os.path.isfile(self.conffile):
            stderr.write(
                """
Konfigurační soubor {} neexistuje!
Příklad konfiguračního souboru najdeš na adrese:
https://github.com/MarrekNozka/pyOdorik/blob/master/pyodorik.ini

""".format(
                    self.conffile
                )
            )
            sys.exit(10)

        self.config = configparser.ConfigParser()
        self.config.read(self.conffile)
        if (
            "auth" in self.config
            and "user" in self.config["auth"]
            and "password" in self.config["auth"]
        ):
            self.auth = self.config["auth"]
        else:
            stderr.write(
                """
V konfiguračním souboru {} je třeba sekce

[auth]
password = topsecpass
user = abc123456

Příklad konfiguračního souboru najdeš na adrese:
https://github.com/MarrekNozka/pyOdorik/blob/master/pyodorik.ini

""".format(
                    self.conffile
                )
            )
            sys.exit(20)
        if (
            "default_caller" in self.config
            and self.hostname in self.config["default_caller"]
        ):
            self.caller = self.config["default_caller"][self.hostname]
        elif (
            "default_caller" in self.config
            and "default" in self.config["default_caller"]
        ):
            self.caller = self.config["default_caller"]["default"]
        else:
            stderr.write(
                """
V konfiguračním souboru {0} je třeba sekce

[default_caller]
default = 123 456 789
{1} = 5

Příklad konfiguračního souboru najdeš na adrese:
https://github.com/MarrekNozka/pyOdorik/blob/master/pyodorik.ini

""".format(
                    self.conffile, self.hostname
                )
            )
            sys.exit(21)
        self.recipient = self.caller

        if "lines" in self.config:
            self.lines = self.config["lines"]
            # print(list(self.lines.items()))
            if "default" in self.lines:
                self.line = self.lines["default"]
            else:
                self.line = None
            for line in self.lines:
                """Pokud je v názvu spustitelného souboru jméno linky,
                použije se."""
                if line in basename(sys.argv[0]):
                    self.line = self.lines[line]
        else:
            self.lines = []
            self.line = None

    def printHelp():
        print(
            """
  pyOdorik
=====================
Help, usage and sources: https://github.com/MarrekNozka/pyOdorik
Bug reports and issues:  https://github.com/MarrekNozka/pyOdorik/issues
"""
        )

    def getFromAPI(self, method, URL, **kwargs):
        params = dict(self.auth)
        params.update(kwargs)
        params = urllib.parse.urlencode(params)
        try:
            conn = http.client.HTTPSConnection("www.odorik.cz")
        except:
            stderr.write("chyba sítě.\n\n")
            sys.exit(30)
        if method == "POST":
            conn.request("POST", self.root + URL, params)
        elif method == "GET":
            conn.request("GET", self.root + URL + "?" + params)
        else:
            return False
        response = conn.getresponse()
        print(response.status, response.reason)
        data = response.read()
        conn.close()
        return data

    def getCredit(self):
        return self.getFromAPI("GET", "/balance").decode("ascii")

    def getContacts(self):
        contacts = self.getFromAPI("GET", "/speed_dials.json")
        contacts = json.loads(contacts)
        return contacts

    def getLines(self):
        lines = self.getFromAPI("GET", "/lines")
        return lines.decode("ascii").split(",")

    def make(self, args):
        "zpracuje telefonní čísla na příkazovém řádku"
        args.pop(0)
        numbers = "".join(args).split("-")  # 123 456 789 - 12 555 12 13
        if not all(numbers):
            stderr.write("Zadej jedno telefonní číslo \n")
            stderr.write("... nebo dvě čísla oddělená pomlčkou\n")
            exit(44)
        if len(numbers) > 0:
            self.recipient = numbers.pop()
        if len(numbers) > 0:
            self.caller = numbers.pop()
        if not re.search(r"^\d+$", self.caller):
            self.caller = self.findContact(self.caller)
        if not re.search(r"^\d+$", self.recipient):
            self.recipient = self.findContact(self.recipient)

    def findContact(self, exp):
        "najde kontakty odpovídající výrazu"
        "ten zmatek s unicodedata a .encode a .decode je tu proto"
        "aby vyhledávání probíhalo bez diakritiky"

        def match(item):
            exppp = (
                unicodedata.normalize("NFD", exp)
                .upper()
                .encode("ascii", "ignore")
                .decode("ascii")
            )
            return re.search(
                exppp,
                unicodedata.normalize("NFD", item["name"])
                .upper()
                .encode("ascii", "ignore")
                .decode("ascii"),
                re.I,
            )

        print("\nHLEDÁM", exp)
        calllist = self.getContacts()
        calllist = list(filter(match, calllist))
        if len(calllist) == 0:  # nic jsem nenašel
            return 0
        elif len(calllist) == 1:  # přesně jeden odpovídá
            print(
                "    ",
                calllist[0]["shortcut"],
                calllist[0]["name"],
                calllist[0]["number"],
            )
            choice = input(" pokračujeme? [A/n]> ")
            if choice == "" or choice.upper() == "A" or choice.upper() == "Y":
                return calllist[0]["shortcut"]
            else:
                return 0
        else:  # odpovídajících kontaktů je víc
            for i, contact in enumerate(calllist, start=1):
                print(
                    " ",
                    i,
                    ":",
                    contact["shortcut"],
                    contact["name"],
                    contact["number"],
                )
            choice = input(" zvol si číslo (0 znamená odchod)[1]> ")
            if choice == "":
                return calllist[0]["shortcut"]
            while 1:
                try:
                    choice = int(choice)
                    if choice == 0:
                        return 0
                    return calllist[choice - 1]["shortcut"]
                except ValueError:
                    print("CHYBA: Zadej číslo!")
                except IndexError:
                    print("CHYBA: Zadej správné číslo!!")
                choice = input(" zvol si číslo (0 znamená odchod)[1]> ")
            return

    def call(self):
        kwargs = {}
        if self.line:
            kwargs.update({"line": self.line})
        if self.caller and self.recipient:
            return self.getFromAPI(
                "POST",
                "/callback",
                caller=self.caller,
                recipient=self.recipient,
                **kwargs
            )
        else:
            stderr.write(" Některé z čísel není zadáno správně.\n")
            exit(51)


##############################################################################


if __name__ == "__main__":
    try:
        pyodorik = PyOdorik()

        if len(sys.argv) == 1 or sys.argv[1] == "credit":
            print("Kredit: {} Kč".format(pyodorik.getCredit()))
            sys.exit(0)
        elif sys.argv[1] == "help":
            pyodorik.printHelp()
            sys.exit(0)
        elif sys.argv[1] == "lines":
            print(pyodorik.getLines())
            sys.exit(0)
        elif sys.argv[1] == "list":
            contacts = pyodorik.getContacts()
            for k in contacts:
                print(k["shortcut"], ":", k["name"], ":", k["number"])
            sys.exit(0)
        elif sys.argv[1] == "search":
            contacts = pyodorik.findContact(sys.argv[2])
            sys.exit(0)
        else:
            pyodorik.make(sys.argv)
            stdout.write("\nCaller: {}\n".format(pyodorik.caller))
            stdout.write("Recipient: {}\n".format(pyodorik.recipient))
            print(pyodorik.call())
            sys.exit(0)
    except KeyboardInterrupt:
        exit(1)
