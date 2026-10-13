# Obligatorisk aritmetisk kontroll av valresultat

Originalkälla: SCB:s SOS-volym och angiven tabell/sida. **Inga rader med felaktiga summeringar får publiceras som verifierade.** Kör:

```bash
python scripts/validate_election_csv.py data/qa/exempel_scb_1970_s134.csv
```

Tre huvudvillkor på varje geografisk nivå/valtyp:
1. Röstande = giltiga + ogiltiga.
2. Giltiga = summan av **samtliga** partiers rösttal (inklusive övriga).
3. Valdeltagande (%) = 100 × röstande / röstberättigade, med avrundning till en decimal där originalet visar en decimal.

Om vallokal- och poströster redovisas var för sig: kontrollera att deras summor motsvarar totalen. Denna kontroll gäller enbart när de två delmängderna bildar en fullständig, ömsesidigt uteslutande uppdelning enligt tabellens definition.

**Felhantering:** flagga rad, registrera SCB-volym, tryckt sida, tabell och granskarens korrigeringsanteckning; kontrollera visuellt mot original. Gissa inte eller förändra siffror för att få aritmetiken att gå ihop. Tomt värde är okänt, inte noll. Tryckta streck kontrolleras mot tabellförklaringen innan de blir numerisk nolla.

**Exempel (syntetiskt? NEJ: transkriberat från användarens visade SCB-tabell 2.2 s.134, Höör):** 5 701 + 14 = 5 715; summa åtta partikategorier = 5 701; 5 715 / 6 567 × 100 avrundat till en decimal = 87,0 %. Kontroll av separat redovisade röster: 5 053 + 662 = 5 715; 5 048 + 653 = 5 701.

Viktigt: denna kontroll garanterar **intern aritmetisk konsistens**, inte att siffrorna avlästs från rätt kommun, valkrets eller valtyp. Därefter krävs extern avstämning mot officiella kommun- och valkretstotaler. Exempelfilen är **QA-testdata från Höör**, inte valresultat från Luleå.
