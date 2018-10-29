pyOdorik
=====================

[Odorik]: http://www.odorik.cz

* Sources:                https://github.com/MarrekNozka/pyOdorik
* Bug reports and issues: https://github.com/MarrekNozka/pyOdorik/issues

User aplication for [Odorik][] VoIP.       
Uživatelská aplikace pro [Odorik][] VoIP.


Aplikace používá [Odorik API](https://www.odorik.cz/w/api).
Konfigurace je uložena v [~/.config/pyodorik.ini](pyodorik.ini).



Seznam kontaktů
----------------

    $ pyodorik list
    $ pyodoril search karel


Kredit
-------

    $ pyodorik
    $ pyodorik credit


Zpětné volání
--------------

    $ pyodorik 756 123 658
    $ pyodorik 123 456789 - 756123456
    $ pyodorik tonda


Pokud je zadáno jen jedno číslo, bere se číslo telefonu z kterého
chci volat z konfiguračního souboru. Na mezerách nezáleží. Při zadání dvou
čísel je oddělovačem pomlčka. Dvě telefonní čísla se zadávají v pořadí
`<odkud>` - `<kam>`

V konfiguračním souboru si pro každého hostitele můžu nastavit jiné výchozí
telefonní číslo. Hostitel se určuje voláním příkazu `hostname`. (Tato funkce
je zde proto, že si zrcadlím konfiguraci na více počítačů a chci, aby se to
například v práci chovalo jinak než doma.)

Pokud není uvedeno telefonní číslo, začne se vyhledávat řetězec v kontaktech.
Hledání probíhá bez diakritiky.

    $ pyodorik tonda
    $ pyodorik.home reditel
    $ pyodorik 'adam|eva'

Výpis a volba linky
--------------

    $ pyodolik lines

Volba linky se provádí pojmenování příkazu, kterým je program volán a sekcí
[lines] v konfiguračním souboru.

    $ cd ~/bin
    ~/bin $ ln -s pyodorik.py pyodolik
    ~/bin $ ln -s pyodorik.py pyodolik.home
    ~/bin $ ln -s pyodorik.py pyodolik.adam
    ~/bin $ ln -s pyodorik.py pyodolik.eva

    $ pyodorik.adam 777 555 444


Help
-------

    $ pyodorik help


