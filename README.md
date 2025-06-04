# Fyllingsgrad og nedbør

## Requirements

Installer avhengigheter med:

```bash
pip install -r requirements.txt
```
I tillegg må det opprettes en fil `creds.json` i working directory med følgende format

```
{"ID":"aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"}
```
`ID`-verdien er User ID fra frost.met.no

## Usage

### 1. Opprette database og view

```
python main.py
```

### 2. Generere figurer

```
python generateFigures.py
```



## Datastruktur og relasjoner


```
+-------------------------------------------------------------------------------------------------+
| VIEW: view_fyllingsgrad                                                                         |
|-------------------------------------------------------------------------------------------------|
| Valgte Kolonner:                                                                                |
|   f.fyllingsgrad, f.endring_fyllingsgrad, f.omrnr, f.omrType, f.iso_aar, f.iso_uke,             |
|   o.navn,                                                                                       |
|   m.minFyllingsgrad, m.medianFyllingsGrad, m.maxFyllingsgrad,                                   |
|   n.value                                                                                       |
+-------------------------------------------------------------------------------------------------+
     ^
     |
     | Henter data fra og defineres av:
     |
+----|--------------------------------------------------------------------------------------------+
| TABELL: fyllingsgrad (f)                                                                        |
|-------------------------------------------------------------------------------------------------|
| Relevante Kolonner:                                                                             |
|   - fyllingsgrad         (valgt)                                                                |
|   - endring_fyllingsgrad (valgt)                                                                |
|   - omrnr                (valgt, join-nøkkel)                                                   |
|   - omrType              (valgt, join-nøkkel)                                                   |
|   - iso_aar              (valgt, join-nøkkel)                                                   |
|   - iso_uke              (valgt, join-nøkkel)                                                   |
+-------------------------------------------------------------------------------------------------+
     |
     |---- LEFT JOIN ----> +----------------------------------------------------------------------+
     |                     | TABELL: omraader (o)                                                 |
     |                     |----------------------------------------------------------------------|
     |                     | Join på:                                                             |
     |                     |   f.omrType = o.omrType                                              |
     |                     |   f.omrnr = o.omrnr                                                  |
     |                     |----------------------------------------------------------------------|
     |                     | Relevante Kolonner:                                                  |
     |                     |   - omrType (join-nøkkel)                                            |
     |                     |   - omrnr   (join-nøkkel)                                            |
     |                     |   - navn    (valgt for view)                                         |
     |                     +----------------------------------------------------------------------+
     |
     |---- LEFT JOIN ----> +----------------------------------------------------------------------+
     |                     | TABELL: fyllingsgrad_maxmin (m)                                      |
     |                     |----------------------------------------------------------------------|
     |                     | Join på:                                                             |
     |                     |   f.omrType = m.omrType                                              |
     |                     |   f.omrnr = m.omrnr                                                  |
     |                     |   f.iso_uke = m.iso_uke                                              |
     |                     |----------------------------------------------------------------------|
     |                     | Relevante Kolonner:                                                  |
     |                     |   - omrType            (join-nøkkel)                                 |
     |                     |   - omrnr              (join-nøkkel)                                 |
     |                     |   - iso_uke            (join-nøkkel)                                 |
     |                     |   - minFyllingsgrad    (valgt for view)                              |
     |                     |   - medianFyllingsGrad (valgt for view)                              |
     |                     |   - maxFyllingsgrad    (valgt for view)                              |
     |                     +----------------------------------------------------------------------+
     |
     |---- LEFT JOIN ----> +----------------------------------------------------------------------+
                           | SUBQUERY: nedboer (n)                                                |
                           |   (SELECT * FROM nedboer WHERE referenceHour = 0 AND iso_dag = 1)    |
                           |----------------------------------------------------------------------|
                           | Join på:                                                             |
                           |   f.iso_aar = n.iso_aar                                              |
                           |   f.iso_uke = n.iso_uke                                              |
                           |   f.omrnr = n.omrnr                                                  |
                           |----------------------------------------------------------------------|
                           | Relevante Kolonner (fra subquery):                                   |
                           |   - iso_aar (join-nøkkel)                                            |
                           |   - iso_uke (join-nøkkel)                                            |
                           |   - omrnr   (join-nøkkel)                                            |
                           |   - value   (valgt for view)                                         |
                           +----------------------------------------------------------------------+


```