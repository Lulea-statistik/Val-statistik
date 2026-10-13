# Importpolicy: endast Luleå kommun (2580)

Primärkälla är SCB:s SOS-originaltabeller. **Importera samtliga kolumner och samtliga relevanta rader som avser Luleå kommun**, även rader med 0, streck, valdistrikt, delsummeringar, poströster och totalsummor. Bevara originalkolumnnamn i råtabell och normalisera dem separat.

## Geografisk gräns
- Förekomst av `2580 Luleå` eller uttrycklig Luleå-rubrik i originaltabellen startar Luleås kommunblock. Läs alla tillhörande distriktsrader till och med `Hela kommunen`.
- Om en valkrets består av flera kommuner ska **inte** hela valkretsens röster tillskrivas Luleå. Behåll `Hela valkretsen` i separat kontrolltabell med tydlig nivå och endast som relevant valkretskontext.
- Rader för andra kommuner får inte följa med, även om de förekommer på samma PDF-sida.
- För historiska distriktskoder, kontrollera kommuntillhörighet i respektive års källa. Tilldela aldrig `2580` enbart från ett liknande distriktsnamn.
- Bevara valkretsindelning per **valår och valtyp**. Luleå kan ha olika valkretskopplingar för olika valtyper.

## Förlustfri representation
Lagra en rad per originaltabellrad med `kalla_id`, `pdf_sida`, `tryckt_sida`, `tabell`, `valar`, `valtyp`, `kommunkod`, `valkrets`, `valdistrikt`, `radtyp`, `original_radnummer` och **alla numeriska kolumner från originalet**. Behåll även fullständig råtranskription eller en dokumenterad kolumnlista med ursprungliga rubriker. Använd särskilda poster för valkrets-, kommun- och distriktssummor och eventuell uppdelning vallokal/poströster. Inkludera inte dubbelräkning av hierarkiska summor i analytiska tabeller.

## Kvalitet och publicering
- De tre huvudkontrollerna är rösttotal = giltiga + ogiltiga; giltiga = summan av samtliga redovisade partiröster; valdeltagande = röstande / röstberättigade med källans avrundning.
- I vissa tabeller kan giltiga valsedlar och partiernas lokalt räknade röster ha annan avgränsning. Beräkna då separat på rätt radnivå och kontrollera poströster explicit, utan att blanda nivåer.
- Felaktiga eller ofullständiga rader ska inte ingå som godkända valresultat; behåll dem i granskningsunderlag med status och avvikelse.
- Årtal 1970 och framåt registreras bara när rätt originaltabell för Luleå har lokaliserats. Fyll inte på med uppgifter från andra kommuner eller uppskattningar.

Status: importpolicy, inte en färdig transkription av samtliga PDF-publikationer.
