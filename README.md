pyOdorik
========

[Odorik]: http://www.odorik.cz


Uživatelská aplikace pro [Odorik][] VoIP.

Use aplication for [Odorik][] VoIP.

Konfigurace
--------------

Konfigurace je uložene v `~/.config/pyodorik.json`

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

Pokud je zadáno jen jedno číslo bere se číslo telefonu z kterého 
chci volat z konfiguračního souboru.

V konfiguračním souboru si pro každého hostitele můžu nastavit jiné výchozí
telefonní číslo.


Help
-------

    $ pyodorik
    $ pyodorik help

