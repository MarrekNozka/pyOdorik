pyOdorik
========

[Odorik]: http://www.odorik.cz


Uživatelská aplikace pro [Odorik][] VoIP.

Use aplication for [Odorik][] VoIP.

Konfigurace
--------------

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

