# Val-statistik

Öppen samling för geografisk och statistisk analys av historiska val i Luleå kommun.

## Valdistrikt 2002 – rekonstruktion

Första datamängden omfattar **56 valdistrikt** (29 i Luleå Norra valkrets och 27 i Luleå Södra). Detta är **inte Valmyndighetens original-GIS från 2002**. Geometrierna är baserade på det officiella valdistriktslagret för 2006 och jämförda med Valmyndighetens kartbilder från 2002. Små gränsändringar 2002–2006 kan inte uteslutas.

Det ursprungliga arkivet `lulea_valdistrikt_2002_reconstructed_bundle.zip` har återfunnits och innehåller GeoPackage i EPSG:3006 respektive EPSG:3021, GeoJSON i EPSG:4326, en Shapefile-ZIP i EPSG:3006, distriktsförteckning (CSV), rekonstruktionsdokumentation och originalets PRJ. **Datafilerna är ännu inte publicerade i detta repository.** Publicering och automatisk kontroll återstår.

Se [metod och osäkerhet](docs/valdistrikt-2002-metod.md) och [importstatus](docs/importstatus.md).

## Källor
- [Valmyndigheten: Luleå 2002](https://historik.val.se/val/val_02/slutresultat/25R/2580/2580.html)
- [2002 års karta: Norra valkretsen](https://historik.val.se/val/val_02/kartor/25R/258001.jpg)
- [2002 års karta: Södra valkretsen](https://historik.val.se/val/val_02/kartor/25R/258002.jpg)

## Nästa steg
1. Importera och versionshantera originalarkivets sju filer under `data/valdistrikt/2002/`.
2. Kontrollera 56 unika distriktskoder, giltiga geometrier och CRS.
3. Bygg webbkarta och årsväljare när ytterligare år finns.

Licens för källdata ska granskas före vidare återpublicering.