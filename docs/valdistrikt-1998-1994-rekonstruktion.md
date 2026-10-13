# Rekonstruktion av valdistriktsgränser 1998 och 1994 — Luleå

## Källäge och säkerhetsnivå

**Primärkälla:** Luleå kommun, kommunfullmäktige, protokoll 2001-10-29 § 140, *Ändring av valdistriktsindelning*, s. 286–287, bilaga 1 (fastighetsförteckning) och bifogad karta. Originalet är uppladdat i projektkonversationen. Denna notering utgör källtolkning, **inte en färdig eller officiellt fastställd GIS-geometri för 1998 eller 1994**.

Enligt § 140 beslöt kommunfullmäktige att **hos länsstyrelsen hemställa om fastställelse** av föreslagen ändring. Dokumentet är alltså kommunfullmäktiges hemställan, **inte ett bevis på länsstyrelsens slutliga fastställelse eller exakt ikraftträdandedatum**.

## Dokumenterad föreslagen ändring inför valet 2002

Berörda distrikt: **Björkskatans 1:a valdistrikt** och **Björkskatans 2:a valdistrikt**. Bilaga 1 föreslår att väljare boende på följande fastigheter ska flyttas **från 2:a till 1:a valdistriktet**:

- Björkskatan 1:292–1:322
- Björkskatan 1:359
- Björkskatan 1:442–1:459
- Björkskatan 1:478
- Björkskatan 1:594–1:612
- Björkskatan 1:642
- Björkskatan 1:729–1:731

Motivet var ojämn röstberättigad befolkning till följd av nybyggnation. Den 1 mars 2001 redovisades 2 013 röstberättigade i Björkskatans 2:a valdistrikt och 1 144 i det 1:a. Efter föreslagen ändring beräknades cirka 1 686 respektive 1 471 röstberättigade.

Sista sidan i dokumentet innehåller en karta i skala **1:6500** med förslag till ny valdistrictsgräns markerad jämte den äldre gränsen. Kartan måste georefereras mot kända fastighetsgränser; dess linjer bör **inte automatiskt digitaliseras som exakta originalkoordinater** utan fastighets-/förrättningsunderlag.

## Försiktig GIS-metod

1. Säkra **länsstyrelsens beslut** som fastställde ändringen och kontrollera giltighet före valet 2002.
2. Identifiera de sju grupperna fastighetsbeteckningar i **historisk fastighetsgeometri omkring 2001** (nuvarande fastighetsgränser kan ha ändrats).
3. Om ändringen faktiskt trädde i kraft, bygg en **historisk 1998-kandidat** genom att återföra berörd yta från Björkskatans 1:a till Björkskatans 2:a, **förutsatt att valdistriktens övriga gränser 1998–2002 är identiska**.
4. 2002 års lager i webbplatsen är i sig **en rekonstruktion byggd från 2006 års GIS-data**, inte officiellt 2002-original; kontrollera därför också ändringar **2002–2006** före bakåträkning.
5. Jämför 1998 års distriktsnamn och koder med valstatistik, samt hitta belägg för att **1994 och 1998 hade samma indelning**. Uppgiften är tills vidare en hypotes, inte fastställd av detta beslut.
6. Exportera först därefter separata lager märkta **rekonstruerad 1998 / rekonstruerad 1994**, med osäkerhetsmarkering, källkedja och polygonkontroller.

**Viktigt:** Det är endast en **föreslagen gränsändring mellan två namngivna distrikt** som dokumentet belägger. Det säger inte att alla andra valdistrikt i kommunen var oförändrade mellan 1994, 1998, 2002 och 2006.

## Kartans referensyta

Webbplatsens kommungräns kommer från `Lulea-statistik/BR-brottsstatistik/docs/data/municipalities.geojson` och har kopierats till `docs/data/lulea_kommungrans_2580.geojson`. Den används enbart för **stabil geografisk kartinramning**, inte som historiskt verifierad land-/havsyta för något visst valår.

## Geografisk referens från karta och kommunens kartportal (13 oktober 2026)

Användaren har tillhandahållit en förstoring av bilagekartan från 2001 och en modern kartbild över **Bodskataudden, Stormvägen, Vinternäsets förskola och Björkskataskolan**, samt en koordinat **SWEREF 99 TM N 7296378, E 829939** som ligger **inne i det berörda området**.

Transformering EPSG:3006 → EPSG:4326 (för kartvisning) ger ungefär **65,619750° N, 22,175423° E**. Detta är en **orienteringspunkt**, inte en digitaliserad brytpunkt eller en uppmätt punkt på valdistriktsgränsen. Webbkartan har därför en särskild knapp **Visa Björkskatan (gränsändring 2001)** som zoomar dit och visar referenspunkten.

Kartutdragets legend: **streckad linje = nuvarande gräns (före föreslagen ändring år 2001)**, **heldragen linje = föreslagen gräns**. Därför är den streckade linjen den relevanta historiska gränskandidaten för 1998, medan den heldragna linjen endast visar föreslagen 2002-indelning. Den senare får inte behandlas som fastställd utan länsstyrelsens beslut. Skanningen har kartskala 1:6500 men kan ha skal-/rotationsförvrängning; fysisk georeferering kräver flera oberoende kontrollpunkter (exempelvis igenkännbara gatukorsningar och äldre fastighetsgränser), inte bara den tillhandahållna koordinaten.

Varken en historisk polygon för 1998 eller en identisk indelning 1994 har ännu fastställts av en sådan koordinat.
