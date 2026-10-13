# Import av historiska röstdata

Lägg filen `rostdata_v3.csv` här (UTF-8 med BOM, semikolonseparerad export av
Excel-fliken `Röstdata v3`, tabellen `röstdata`).

GitHub Actions-flödet `Import Röstdata v3` validerar 1 190 rader och skapar
`docs/data/roster/rostdata_v3.json`, som används av de två temakartorna.

Originalets svenska kolumnnamn bevaras. Tomma värden blir `null`, aldrig noll.
Kommuntotalen "Luleå" och `Uppsamlingsdistrikt` färgsätts inte som enskilda
valdistrikt. Datat omfattar riksdagsval (RS) och kommunfullmäktigeval (KF)
1985–2022; inga röstdata för 1970–1982 eller 2026 finns i denna tabell.

OBS: Denna katalog och importeraren är publicerade. Den faktiska CSV-filen
måste laddas upp här för att röststatistiken ska bli tillgänglig på kartan.
