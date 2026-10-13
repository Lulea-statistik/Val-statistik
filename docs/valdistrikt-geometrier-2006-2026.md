# Valdistriktsgeometrier 2006–2026 – Luleå kommun 2580

**Aktivt arbetsområde:** geografier/valdistrikt. PDF-transkriberingen avslutas tills vidare. Det historiska valresultatet är oförändrat.

## Verifierade källsidor

| År | Källa | Leverans | Status |
|---|---|---|---|
| 2006 | https://historik.val.se/val/val2006/slutlig_ovrigt/statistik/kartor/index.html | GIS-shape: riksdagsvalet 2006 i valdistrikt, även resultatdata | Länk identifierad, binär originalfil ännu inte importerad |
| 2010 | https://historik.val.se/val/val2010/statistik/index.html | GIS → alla valdistrikt (shapefile) | Länk identifierad, import återstår |
| 2014 | https://historik.val.se/val/val2014/statistik/ | GIS → alla valdistrikt (shapefile) | Länk identifierad, import återstår |
| 2018 | https://historik.val.se/val/val2018/statistik/ | 2018_valgeografi_valdistrikt.zip (shapefile) | Länk identifierad, import återstår |
| 2022 | https://www.val.se/valresultat-och-statistik/statistik-och-data/radata-fran-val-2002-2022 | GIS Norrbottens län ZIP (JSON, SWEREF99 TM) | Länk identifierad, import återstår |
| 2026 | https://www.val.se/valresultat-och-statistik/statistik-och-data/radata-val-2026 | GIS Norrbottens län ZIP (JSON, SWEREF99 TM) | Länk identifierad, import återstår |

SCB hänvisar till Valmyndigheten för valdistriktsgränser: https://www.scb.se/vara-tjanster/bestall-data-och-statistik/bestall-statistiktabeller/geografiska-indelningar-och-digitala-granser/

## Principer

1. En separat årsgeometri per valår, begränsad till Luleå kommun (2580). Endast polygoner / multipolygoner.
2. Läs metadata, samtliga ursprungliga attribut och original-CRS innan bearbetning; använd PRJ eller explicit officiell metadata. **Härled aldrig CRS enbart från koordinattal.**
3. Exportera original-CRS som GeoPackage eller GeoJSON efter reell transformation till EPSG:4326. Behåll geometrins ursprung, förändra inte topologin i onödan.
4. Registrera geometristatus, filnamn, källa, nedladdningstid, SHA256, antal distrikt, identiteter, original-CRS och metod för urval av kod 2580. Utan verifierat kommunfält/kod ska importen misslyckas.
5. Kontrollera varje års distriktsidentiteter, överlapp, hål/gap samt polygoners giltighet. Äldre års gränser får inte ersättas med senare års geometri.
6. Kontrollera separat jämförbarhet år-för-år. 2018→2022 har Valmyndigheten en särskild jämförbarhetsfil; samma valdistriktsnamn innebär inte nödvändigtvis samma geometri.
7. Geografierna för 2002 är **rekonstruktion**, även om de utgår från ett officiellt 2006-lager. De får inte användas som originalgeometri för 2006 utan jämförelse mot källan.
8. För webbvisning används uttryckligen EPSG:4326; EPSG:3857-karta kan kräva reprojektion av eventuella raster, men här hanteras enbart vektorpolygoner.

## Datakatalog efter genomförd import

`docs/data/valdistrikt/{YEAR}/lulea_2580_valdistrikt_{YEAR}_epsg4326.geojson`

`data/geodata/kallregister_valdistrikt_2006_2026.csv`

`data/geodata/kontroll_{YEAR}.json`

### Publiceringsgräns

År ska inte markeras **färdigt/verifierat** förrän faktisk originalfil har laddats ned, schema och CRS kontrollerats samt kommunfilter, antal och topologi har validerats. Listan över källor innebär inte att geometrier redan finns publicerade.

## Kontrolluppdatering 2026-10-13

**2018**: Valmyndighetens ursprungliga statistikportal bekräftar direktarkivet `https://historik.val.se/val/val2018/statistik/2018_valgeografi_valdistrikt.zip` under *GIS och valgeografi* samt SWEREF99 TM (EPSG:3006). GeoJSON får först skapas efter kontroll mot faktiskt nedladdat ZIP-arkiv och dess PRJ. Även 2014–2018 års mappningsfil finns på samma källsida.

**Hämtstatus:** Den direkta ZIP-hämtningen från den aktuella arbetsmiljön stoppades av DNS-/nätverksbegränsning. GitHub Actions-status kunde inte avläsas från den anslutna GitHub-åtgärden. Ingen ny årgång markeras importerad eller geografiskt kvalitetssäkrad med denna kontrolluppdatering.

**Kritiskt:** Importskriptet är fail-closed vid saknat CRS. De ZIP-format som endast ger extern uppgift om EPSG måste granskas innan användaren eller arbetsflödet anger detta explicit. Om en årsfil innehåller flera shapefiler måste rätt originaldistriktslager identifieras, inte väljas godtyckligt.
