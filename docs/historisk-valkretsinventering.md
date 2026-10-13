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
