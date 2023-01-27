# Replikasjonsprosjekt

Dette er et replikasjonsprosjekt for Institutt for Psykologi ved NTNU

## Dette trenger du

Du trenger Python 3 installert, samt R.
For å installere pakker til Python som kreves, kjør `pip install -r requirements.txt` i `Downloader`-mappen

## Finne artikler

For å finne artikler som tilhører Institutt for Psykologi, brukes Cristin APIet, implementert i `Downloader/cristin_api.py`

## Laste ned artikler

Denne funksjonaliteten er med vilje ikke lagt ved siden det kommer helt an på hvordan man har tilgang til artikler. Implementasjonen antar at man har en fil `Downloader/downloader.py` som har en funksjon `download_papers_from_doi_links` tar inn en liste med DOI-linker og en lokasjon for å lagre PDFer av artiklene, og deretter laster ned artiklene til det stedet. Som du kan se er `downloader.py` i `.gitignore`.

## Konvertering av PDF artikler

Når PDFene er lastet ned kan man kjøre CERMINE på artiklene for å konvertere dem til `.cermxml`. For enkelthetsskyld har jeg lagt ved et Python-skript `cermine_runner.py` for å kjøre CERMINE riktige fillokasjoner. Merk at man må ha en gyldig Java-installasjon for at CERMINE skal kjøre.

## Generering av grafer og uthenting av statistikk

Ved å kjøre R-filen `main.R` så vil man generere grafer og statistikker basert på uthentet statistikk fra artiklene.

## Lisens
Merk at CERMINE har sin egen lisens gitt i filen `CERMINE_LICENSE`. Resten av prosjektet har lisens gitt ved filen `LICENSE`.