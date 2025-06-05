# Technisch Rapport voor Superpy Implementatie
Dit rapport beschrijft drie opvallende technische elementen van de implementatie van de Superpy CLI-tool, met uitleg over de problemen die ze oplossen en waarom ze op deze manier zijn geïmplementeerd.
## 1. Datumbeheer met `set_date` en `advance_time`
De functies `set_date` en `advance_time` beheren de systeemtijd via een `current_time.txt` bestand. Dit lost het probleem op van het handhaven van een consistente, manipuleerbare datum voor het volgen van aankopen, verkopen en rapportages. Door de datum extern op te slaan, kan het systeem flexibel schakelen tussen huidige, historische of toekomstige datums zonder afhankelijkheid van de systeemtijd. De keuze voor een tekstbestand vereenvoudigt persistentie en debugging, terwijl regex-validatie (`r'^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$'`) zorgt voor een correct datumformaat. Dit ontwerp biedt robuustheid en eenvoud.
```python
if re.match(r'^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$', date):
    new_date = datetime.strptime(date, "%Y-%m-%d").date()
```
## 2. FIFO-aanpak in `sell_product`
De `sell_product` functie implementeert een First-In-First-Out (FIFO) strategie door batches te sorteren op vervaldatum. Dit lost het probleem op van het verkopen van producten die het eerst vervallen, waardoor verspilling wordt geminimaliseerd. Door beschikbare batches te berekenen (`available = original_count - sold_count`) en te sorteren op vervaldatum, wordt de oudste voorraad eerst verkocht. Deze aanpak is efficiënt en realistisch voor voorraadbeheer in een winkelcontext.

```python
available_batches.sort(key=lambda x: datetime.strptime(x['expiration_date'], "%Y-%m-%d"))
```
## 3. Flexibele rapportage in report
De `report` functie ondersteunt meerdere rapporttypes (`inventory`, `revenue`, `profit`) met flexibele datumfilters (`now`, `yesterday`, `--date`). Dit lost het probleem op van het genereren van gerichte financiële en voorraadrapporten. Door conditionele logica en CSV-verwerking worden rapporten dynamisch gefilterd en berekend. Dit ontwerp maakt de functie veelzijdig en herbruikbaar, terwijl het gebruik van `rich` voor console-uitvoer de leesbaarheid verbetert.

```python
if args.now is True:
    if current_date in row:
        print(row)
```

Deze implementaties balanceren functionaliteit, gebruiksvriendelijkheid en onderhoudbaarheid, passend bij de behoeften van een eenvoudige winkelbeheertool.