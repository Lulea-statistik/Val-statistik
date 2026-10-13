# SCB:s original-PDF:er – Luleå-utdrag

För varje av de tre valtyperna och varje valår skapas en **oförändrad sidutdrag-PDF** för Luleås del av SCB:s SOS-volym (kommun 2580). Den länkas från webbsidan när den är kontrollgranskad. PDF-dokumenten från SCB är **primärkälla**; utdraget är en kopia av originalets relevanta sidor, inte självständig officiell publikation.

## Arbetsflöde
1. Hämta rätt SCB-volym enligt källregistret. Bevara hela originalfilen lokalt för spårbarhet.
2. Lokalisera Luleås kommunblock i PDF:en och kontrollera eventuella fortsättningssidor. Anteckna båda **tryckta sidnummer** och **PDF-sidindex**, vilka ofta skiljer sig.
3. Skapa utdrag med `scripts/extract_lulea_pdf.py` (bibliotek `pypdf`), t.ex.:

```bash
pip install pypdf
python scripts/extract_lulea_pdf.py scb_1998_landsting.pdf --year 1998 --election region --pages PDF_SIDINDEX_1-PDF_SIDINDEX_2 --printed-pages 277-278 --source-url "SCB_ORIGINAL_URL"
```

Ersätt platshållarna med **verifierade PDF-sidindex**. Sidnummer 277–278 är tryckta sidnummer, inte per automatik PDF-sidindex.

4. Granska utdragets första/sista rad visuellt, kontrollera att samtliga Luleådistrikt och kommunsumma medföljer. Sidor kan innehålla andra kommuner; behåll originalutseendet men **importera aldrig deras rösttal**.
5. Publicera PDF och dess JSON-manifest i `docs/pdf/lulea/` (GitHub Pages). Manifest anger källa, sha256, PDF- och tryckta sidnummer, samt granskningsstatus.
6. Visa endast färdiggranskade utdrag på webbsidan. Låt inte utdragna PDF-sidor ersätta CSV-transkription eller kontroller av röstsummor.

## Status 2026-10-13
SCB:s PDF-server kunde inte nås från körmiljön. Detta är en färdig förberedelse för sidutdrag; **inga nya PDF-utdrag har producerats eller publicerats**. Uppladdade SCB-original kan bearbetas med samma metod utan att servern behöver vara tillgänglig.

## Rättigheter
Kontrollera SCB:s återanvändningsvillkor innan stora delar av originalpublikationerna återpubliceras. Ange alltid titel, år, del, källa och sidintervall.
