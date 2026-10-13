# Historiska val: källor och datamodell

## Valtyper
En separat serie för riksdagsval (`riksdag`), landstings-/regionfullmäktigeval (`region`) och kommunfullmäktigeval (`kommun`).

## Valår
1970, 1973, 1976, 1979, 1982, 1985, 1988, 1991, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022, 2026. 1994 är sista året i treårscykeln; från 1998 hålls ordinarie val vart fjärde år.

## SCB-serier
1970–1994: Allmänna valen del 1 (riksdag), del 2 (kommunala val, inkluderar landstingsval) och del 3 (specialundersökningar).

1998: del 1 (riksdag), del 2 (landstingsfullmäktige), del 3 (kommunfullmäktige), del 4 (specialundersökningar).

SCB:s samlingssida: https://www.scb.se/hitta-statistik/aldre-statistik/innehall/sveriges-officiella-statistik-sos/valstatistik-19091999/allmanna-valen-1970-1998/

## Tabellstruktur (planerad)
`results.csv`: valar, valtyp, geoniva, geo_id, geo_namn, parti_id, partinamn_original, roster, kalla_id, sida, tabell, kvalitetsstatus.

`turnout.csv`: valar, valtyp, geoniva, geo_id, rostberattigade, rostande, giltiga, ogiltiga, blanka, kalla_id, sida, tabell, kvalitetsstatus.

`sources.csv`: kalla_id, titel, url, dokumentets_sida, insamlingsdatum, kontrollmetod.

Geometriregister separat: valar + valdistriktskod + geometri + rekonstruktionsstatus + CRS.

## Kvalitet
- Kontrollera först att PDF faktiskt redovisar valdistriktsdata. Kommunvärden får inte felaktigt brytas ned till valdistrikt.
- Valdistriktskoder och gränser kan ändras mellan år; matcha historiskt per valår.
- Skilj historiska partinamn från harmoniserade partier.
- Håll de tre valtypernas röster, rösträtt och valdeltagande separata.
- Registrera källans tryckta sida, tabell och OCR/manuell verifiering.
- Avstäm summerade distriktsresultat mot originalets kommuntotaler och använd saknade värden, inte nollor, för obekräftad statistik.
- Ange tydligt att 2002 års gränser är rekonstruktion baserad på 2006 års kartdata.

Status: Ingen PDF-tabell har ännu extraherats till verifierad valstatistik.
