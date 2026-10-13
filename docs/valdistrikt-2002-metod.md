# Valdistriktsgränser 2002 – metod och osäkerhet

## Status
Datasetet är en **rekonstruktion** och inte ett autentiskt GIS-original från valåret 2002. Originalgeometrierna kommer från Valmyndighetens officiella GIS-lager från 2006. Dessa har jämförts med officiella kartbilder från 2002.

## Dokumenterade kontroller i det ursprungliga arkivet
- 56 unika distrikt: 29 Norra, 27 Södra valkretsen.
- Namn enligt 2002 års distriktslistor.
- Visuell/topologisk jämförelse med de officiella kartbilderna på deras upplösningsnivå.
- Geometrivalidering och ingen parvis överlappning större än 1 m² enligt ursprungsdokumentationen.

Dessa punkter återger **tidigare dokumenterade kontroller**. De är inte en ny oberoende verifiering i detta repository.

## Koordinatsystem
- Källans RT90 2.5 gon V: äldre EPSG:2400, motsvarande normaliserad EPSG:3021.
- GeoPackage: EPSG:3021 och EPSG:3006 (SWEREF 99 TM).
- GeoJSON för webbkarta: EPSG:4326.
- Det ursprungliga `.prj` behålls för spårbarhet.

## Begränsningar
Officiella 2002-kartbilder har begränsad upplösning. Små förändringar mellan 2002 och 2006 kan inte uteslutas. Datasetet bör inte användas som juridiskt eller historiskt certifierad exakt gränsdata.

## Källor
- Valmyndighetens officiella valdistriktsgeometrier 2006.
- https://historik.val.se/val/val_02/kartor/25R/258001.jpg
- https://historik.val.se/val/val_02/kartor/25R/258002.jpg
- https://historik.val.se/val/val_02/slutresultat/25R/2580/2580.html
