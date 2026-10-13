# Systematisk genomgång av valdistrikt och valkretsar

Målet är att för varje ordinarie valår 1970–2026 dokumentera **tre separata val**: riksdag, landsting/region och kommun. Det ger **51 kontrollposter**. All historisk information måste verifieras per valår och valtyp.

## Viktig skillnad
Ett valdistrikt är inte samma sak som en valkrets. Ett valdistrikt kan tillhöra olika valkretsindelningar beroende på vilken valtyp och vilket år det handlar om. En valkrets kan dessutom omfatta fler kommuner eller en del av en kommun.

## Avprickning
- [x] 2002 kommun: 56 distriktsrelationer inlagda utifrån befintlig, uttryckligen **rekonstruerad** GIS. Inte oberoende historiskt verifierat mot kommunvalets originaltabell.
- [x] 1998 landsting/region: SCB s. 277–278 visar att Luleå kommun redovisas under **femte valkretsen**, där kommunens och valkretsens totalsiffror är lika. Distriktsrad för varje distrikt återstår att transkribera och verifiera.
- [ ] 1998 riksdag och kommun: individuella distriktslistor och valkretstillhörighet.
- [ ] 1994: undersök uppgiften om **två** valkretsar i respektive valtyp, utan att förutsätta att det stämmer.
- [ ] Resterande år och valtyper enligt arbetsregistret.

Se [arbetsregistret](../data/valkretsar/arbetsregister_1970_2026.csv) för hela matrisen och [distriktsrelationerna 2002](../data/valkretsar/2002_kommun_valdistrikt.csv).

## Arbetsmetod
1. Identifiera respektive års **officiella** volym/PDF för varje valtyp. Före 1998 omfattar SCB del 2 både landstings- och kommunalval; leta rätt tabellavsnitt.
2. Notera **tryckt sida, PDF-sida, tabellnummer, valkretsnamn/kod, kommun, valdistrikt och ursprunglig distriktsbeteckning**.
3. Importera en distriktsrad per valtyp, år och valkrets (ingen hopslagning mellan olika val).
4. Lägg röstberättigade, röstande och röster per parti i separata normaliserade tabeller; kontrollera partisummor, kommun- och valkretssummor.
5. Kontrollera om valdistriktsnamnet kan kopplas till geometri. Behåll källnamnet och flagga tvetydigheter, sammanslagningar och gränsändringar.
6. Publicera bara valkretskopplingar med dokumenterad källa. Skilj `verifierat_original`, `rekonstruktion`, `preliminar` och `saknas`.

## Granskning av 1994
Uppgiften att Luleå hade två valkretsar 1994 **är inte verifierad** och ska inte ärvas från GIS för 2002. Särskilt måste man skilja landstingsvalkrets från kommunvalkrets och riksdagsvalkrets.

## GitHub Pages
För närvarande ligger Pages på **main/docs**. Därför finns `docs/index.html` som startsida; den läser GeoJSON från `../data/`, vilket fungerar under GitHub Pages för detta repo även när HTML-filen ligger i `docs/`. Om GitHub Pages endast publicerar `docs/` kan dock filer utanför den mappen **inte** hämtas som webbresurser. Webbdatan måste därför också publiceras under `docs/data/` eller Pages-källan bytas till repositoryroten. Kontrollera detta innan kartan betraktas som färdig.

SCB:s äldre publikationer: https://www.scb.se/hitta-statistik/aldre-statistik/innehall/sveriges-officiella-statistik-sos/valstatistik-19091999/allmanna-valen-1970-1998/

## Publikationsinventering påbörjad 13 oktober 2026

[Inventeringen 1970–2026](../data/kallor/publikationsinventering_1970_2026.csv) har 51 separata poster för de tre valtyperna under 17 valår. Det är inte 51 verifierade PDF-filer. För åren 1970–1994 är SCB:s del 2 en gemensam publikation för landstings- och kommunfullmäktigeval, vilket innebär att två registerposter kan referera till samma volym. För 1998 har landstingsvalets del 2 en känd direktlänk; övriga direktlänkar ska identifieras och testas före datainläsning.

Först läses källans innehållsförteckning och distriktsvisa tabellsidor. Alla distriktsvärden kontrolleras mot kommun- och valkretstotaler; inga preliminära numeriska värden behandlas som verifierade.

## Publicering

GitHub Pages är inställt på `main/docs` enligt användarens skärmbild och innehåller nu både `docs/index.html` och `docs/data/lulea_valdistrikt_2002.geojson`. Den offentliga sidans tillgänglighet har inte kunnat verifieras genom extern HTTP-kontroll i denna session.

## Källhierarki (fastställd 2026-10-13)

1. **Primärkälla:** SCB:s *Allmänna valen* (SOS) 1970–1998, originalpublicerad PDF för respektive valår och valtyp. För 2002 och senare används officiella SCB-/Valmyndighetspublikationer och dokumenterat valresultat.
2. **Kontroll:** SCB:s statistikdatabastabeller och kommun-/valkretstotaler för att stämma av historiska värden, med rätt geografisk nivå.
3. **Oberoende dubbelkontroll:** SND/Researchdata, där åtkomliga data finns. Dessa får inte ersätta SCB som källa för publicerade slutliga värden och distrikts-/valkretskopplingar.

**Publikationsdelar:** SCB bekräftar att 1970–1994 har del 1 riksdag och del 2 *Kommunala valen* (både kommun- och landstingsval). **1998** har del 1 riksdag, del 2 landstingsfullmäktige, del 3 kommunfullmäktige. Antagandet att del 2 alltid är kommunval är därför fel. Primär hänvisning: https://www.scb.se/hitta-statistik/aldre-statistik/innehall/sveriges-officiella-statistik-sos/valstatistik-19091999/allmanna-valen-1970-1998/

Ingen distriktsrad ska markeras verifierad enbart för att en PDF-adress verkar rimlig; kontrollera dokumentets titel och rätt tabell/sida.

## Avgränsning och tillkomna originalvolymer, 13 oktober 2026

**Specialundersökningar ingår inte i projektet.** Granskningen omfattar enbart riksdagsval, landstings-/regionfullmäktigeval och kommunfullmäktigeval. Hänvisningar till specialundersökningar i äldre beskrivningar av SCB:s publikationsserie avser bara bibliografisk kontext och ska inte behandlas som arbetsposter.

Ytterligare tre direktlänkar som användaren tillhandahållit finns nu i [källregistret](../data/kallor/scb_sos_kompletterande_pdf.csv): 1970 del 1 (riksdag), 1970 del 2 (kommunala val) och 1998 del 3 (kommunfullmäktige). Dessa är registrerade som primärkällor men deras tabeller/sidor har ännu inte blivit individuellt extraherade eller avstämda. Direkt hämtning misslyckades vid kontroll, så länkarna kan ännu inte markeras som tekniskt verifierade.

1998 års publikation ska behandlas uttryckligen annorlunda: del 1 riksdag, del 2 landstingsfullmäktige, del 3 kommunfullmäktige. I 1970 års del 2 måste tabeller för både kommun- och landstingsval identifieras separat.
