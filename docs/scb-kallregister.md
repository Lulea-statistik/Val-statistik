# SCB – källregister för historisk valstatistik

Alla åtta tabeller nedan ingår i källkatalogen. Tabellen beskriver *tillgängliga källor*, inte redan importerade valresultat.

| Tabell | Valtyp och innehåll | Valår | Geografi |
|---|---|---|---|
| [Kfmandat](https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__ME__ME0104__ME0104A/Kfmandat/) | Kommunfullmäktige: Mandat efter kommun och parti | 1973–2022 | kommun |
| [Kommunmed](https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__ME__ME0104__ME0104A/Kommunmed/) | Kommunfullmäktige: Röstberättigade efter region och medborgarskap | 1973–2022 | kommun/region |
| [ME0104T25](https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__ME__ME0104__ME0104A/ME0104T25/) | Kommunfullmäktige: Personröster efter kommun, parti och kön | 2002–2022 | kommun |
| [ME0104T1](https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__ME__ME0104__ME0104A/ME0104T1/) | Kommunfullmäktige: Valresultat efter region och parti | 1973–2022 | kommun/region |
| [ME0104T9](https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__ME__ME0104__ME0104A/ME0104T9/) | Kommunfullmäktige: Röstberättigade efter kön och medborgarskapsland | 2002–2022 | riket (ingen kommunvariabel) |
| [ME0104T6](https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__ME__ME0104__ME0104A/ME0104T6/) | Kommunfullmäktige: Röstberättigade efter kommun, medborgarskap och kön | 2002–2018 | kommun |
| [Ltmandat](https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__ME__ME0104__ME0104B/Ltmandat/) | Landstings-/regionfullmäktige: Mandat efter region och parti | 1973–2022 | landsting/region |
| [Riksdagsmandat](https://www.statistikdatabasen.scb.se/pxweb/sv/ssd/START__ME__ME0104__ME0104C/Riksdagsmandat/) | Riksdag: Mandat efter region och parti | 1973–2022 | riksdagsvalkrets/riket; ej kommunmandat |

## Viktiga avgränsningar

- De sex kommunfullmäktigetabellerna omfattar olika variabler och kan inte ersätta varandra.
- ME0104T9 avser medborgarskapsland och kön på riksnivå, inte uppgifter per Luleå kommun.
- ME0104T6 avslutas 2018. Utöka inte serien till 2022 med antagna värden.
- Mandat för landsting/region och riksdag får inte knytas till en enskild kommun som om de hade tilldelats kommunen.
- Alla dessa tabeller är aggregerade: distriktsvisa valresultat kräver andra primärkällor.
- Historiska valdistriktsgränser behöver kvalitetssäkras per valår.

**Nästa importsteg:** Läs in kommunspecifika röstresultat och röstberättigade för 1973–2022 via SCB, med Luleå kod 2580 där den geografiska nivån medger det. För 1970 och valdistriktsnivå används äldre SOS/Valmyndigheten separat. Lagra officiellt råvärde, käll-ID och valår innan någon omräkning.
