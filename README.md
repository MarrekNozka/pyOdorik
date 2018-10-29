pyOdorik
=====================

[Odorik]: http://www.odorik.cz

Uživatelská aplikace pro [Odorik][] VoIP.

Use aplication for [Odorik][] VoIP.

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
    $ pyodorik tonda
    $ pyodorik 123 456789 - 756123456


Pokud je zadáno jen jedno číslo, bere se číslo telefonu z kterého
chci volat z konfiguračního souboru. Na mezerách nezáleží. Při zadání dvou
čísel je oddělovačem pomlčka. Dvě telefoní čísla se zadávají v pořadí
<odkud> - <kam>

V konfiguračním souboru si pro každého hostitele můžu nastavit jiné výchozí
telefonní číslo.

Pokud není uvedeno telefonní číslo, začne se vyhledávat řetězec v kontaktech.
Hledání probíhá bez diakritiky.


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


