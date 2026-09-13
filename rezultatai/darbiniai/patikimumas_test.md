# Rezultatu patikimumo patikros

Sugeneruota: `python -m src.eksperimentai.patikimumas`

| Nr. | Patikra | Busena | Pastabos |
|---|---|---|---|
| 1 | test neitakojo jokio sprendimo | **PRAEJO** | tau sutampa 4/4 modeliu · test eiluciu su val pora: 18/18 |
| 2 | train ir test nesikerta | **RADINYS** | 2a  39 stulpeliu (dedublikavimo erdve): 0 - protokolo garantija · 2b  36 pozymiu + etikete (modelio ivestis): 30 = 0.0082 % test aibes · priezastis: dedublikuota PRIES pozymiu salinima; vieno bito skirtumai pasalintuose stulpeliuose po to isnyksta |
| 3 | tikslumas neperzengia 99.78 % | **PRAEJO** | didziausias: 0.9436 (XGBoost, dvejetaine) · atsarga iki ribos: 5.42 p. p. |
| 4 | operacinis taskas persikelia i test | **RADINYS** | FPR santykis test/val: 0.95-1.13x · biudzeta virsija: Random Forest (suderintas) (1.02 %) |
| 5 | metrikos atkuriamos nepriklausomu keliu | **PRAEJO** | sugretinta 12 paleidimu · didziausias skirtumas: macro-F1 4.51e-06, tikslumas 4.69e-06 |
