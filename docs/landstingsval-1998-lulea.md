# Landstingsfullmäktigevalet 1998 – Luleås valkretsindelning

## Korrigering av tidigare antagande
I SCB:s *Allmänna valen 1998, del 2, Landstingsfullmäktige*, tabell 3 (forts.), tryckta sidor **277–278**, redovisas hela Luleå kommun inom **Norrbottens läns landstings femte valkrets**.

I avslutningen på sida 278 har raderna **Hela kommunen** och **Hela valkretsen – Samtliga röster** samma totalsiffror: **55 724 röstberättigade**, **44 742 röstande**, **43 817 giltiga valsedlar**. Därmed ska man inte förväxla detta landstingsvals valkrets med de **två kommunala valkretsar** som återfinns i rekonstruerade valdistriktsdata från 2002.

Källa: https://share.scb.se/ov9993/data/historisk%20statistik/SOS%201911-%2FValstatistiken%2FAllm%C3%A4nna%20valen%20%28SOS%29%201970-1998%2FValstatistik-Allmanna-valen-1998-Del-2-Landstingsfullmaktige.pdf

## Luleås distriktsnamn i detta dokument
Tabellen på sidorna 277–278 omfattar bland andra:
Avvik, Antnäs, Avan, Bensbyn, Bergnäsets 1–3, Björkskatans 1–2, Brändön, Bälinge, Ersnäs, Gammelstad, Hertsön 1, Hertsön 3–4, Jämtön, Klöverträsk, Lerbäcken, Luleå 1–11, Luleå 13–22, Melderstein, Måttsund, Niemisel, Porsön 1–3, Rutvik, Råneå 1–2, Stadsön 1–3, Sunderbyns 1–2 och Vittå.

*Förteckningen ovan är en partiell transkription för orientering, inte en verifierad komplett distriktslista.* Kontrollera originaltabellen före inläsning av fullständigt distriktsregister.

## Datamodell
En relation för valkretsmedlemskap ska alltid innehålla minst:
`valar,valtyp,valkrets_id,valkrets_namn,kommun_id,geografisk_niva,kall_id,kallsida,gransstatus`.

För 1998 års landstingsval gäller:
`1998,region,5,5:e valkretsen,2580,kommun,SCB_SOS_1998_D2,277-278,dokumenterad_tabell`.

Valdistriktsmedlemskap byggs från varje distrikt i källtabellen och kan skilja sig från kommunvalets och riksdagsvalets valkretsindelningar.

Inga individuella röster eller distriktsgränser för 1998 har ännu importerats.

## Poströster som inte räknades i vallokal

SCB:s originalrapport (Allmänna valen 1998, del 2, s. 5 och tabell 3 s. 278) förklarar att merparten av poströsterna redan ingår i valdistriktsresultaten, medan övriga poströster ingår på kommunnivå. De utgörs enligt SCB huvudsakligen av röster avgivna under valsöndagen. Uppgiften visar **inte** att samtliga har avgetts i en annan kommun.

För Luleå 2580 är skillnaden mellan kommuntotal och summan av 56 valdistrikt exakt 304 röstande och 290 giltiga valsedlar. Fördelningen av de 290 giltiga rösterna: m 51, c 11, fp 21, kd 16, mp 17, s 90, v 60, övriga 24. Summan är 290.

**Redovisningsregel:** Behåll kategorin `i_vallokal_ej_raknade_postroster` som en separat kommunövergripande restpost utan valdistriktsgeometri. Addera inte den till något enskilt valdistrikt. Hela kommunens röster = summan av distriktens lokalt räknade röster + denna restpost. Undvik den obestyrkta etiketten `röster avgivna i andra kommuner`.
