# Källgranskning 1998, landstingsval – andra läsning

SCB original: *Allmänna valen 1998*, del 2, tabell 3, tryckta sidor 276–278 (PDF-sidor 278–280).
Kommun: **2580 Luleå**. Valkrets: **5:e valkretsen**.

## Kontroller genomförda
- Originalbilderna för alla tre sidor har öppnats och tabellblockets gränser verifierats.
- Visuell jämförelse av **sida 278:s 12 distriktsrader** (Porsöns 1–3, Rutvik, Råneå 1–2, Stadsöns 1–3, Sunderbyns 1–2, Vitå) med GitHub-transkriptionen. Samtliga tabellkolumner har jämförts: namn, röstberättigade, därav utländska medborgare, röstande, deltagande, giltiga samt m, c, fp, kd, mp, s, v, övriga. Inga avvikelser noterade.
- Kommuntotalens samtliga kvantitativa kolumner och posten *Därav i vallokal ej räknade poströster* på sida 278 jämfördes mot registrerade kontrollvärden. Aritmetiken stämmer.
- Sidfördelning: 6 distrikt s. 276, 38 s. 277 och 12 s. 278.

## Status och fortsatt arbete
Detta är en **andra visuell genomgång av sida 278**, inte en separat extern dubbelkodning av alla 56 distriktsrader. Resterande 44 distrikt (s. 276–277) behöver motsvarande systematisk kolumnvis motläsning innan hela datamängden märks verifierad. GitHub Actions-körningarnas resultat måste också följas upp.

En viktig källbegränsning: SCB:s rapport förklarar att vissa poströster ingår direkt i valdistriktsresultaten, medan andra bara räknats in i kommunsumman. Restposten är därmed *inte* liktydig med alla förtidsröster, och det går inte att härleda var de avgivits.

## Kontrollomgång 3 – tryckt sida 276

Original-PDF:s sida 278 (tryckt sida 276) har lästs visuellt på nytt i hög upplösning. Alla 14 numeriska källfält (inkl. valdeltagande och 8 partier) och distriktsnamnen har jämförts med registrerad CSV för **Avvik, Antnäs, Avan, Bensbyn, Bergnäsets 1, Bergnäsets 2**. Ingen skillnad upptäckt. Dessa sex rader har fått status `visuellt_motlast_s276` i CSV:n. De 12 raderna på tryckt sida 278 motlästes i föregående kontrollomgång men har ännu inte särskild status per rad i CSV:n. Återstående 38 distrikt på sida 277 behöver motsvarande visuell motläsning.

**Tolkning:** 6 rader med explicit radstatus och 12 tidigare dokumenterade som motlästa i protokoll, totalt 18 av 56. Aritmetisk samstämmighet för 56 rader är separat kontroll och ersätter inte visuell jämförelse.
