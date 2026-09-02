# 🎯 Semaine 6 : Expériences principales

**Calendrier :** 2026-08-31 (lun) – 2026-09-04 (ven) selon le contrat.

**⚠️ Changement de sujet en cours de semaine.** Cette checklist a d'abord été écrite pour le sujet v1 — tâche gardien, juge de conformité, bras B1 à B4 sur UbuntuGuard. Ce sujet a été abandonné le 1ᵉʳ septembre après une pause délibérée, et reconstruit depuis la revue systématique. La version v1 reste dans l'historique git ; ce qui suit décrit le sujet réellement en cours.

**Sujet v2 : Instruct-CPT pour l'Afrique.** Voir `04_Weekly_Reports/Sujet_v2_02_Instruct_CPT.md` et `Sujet_v2_03_Selection_Sources.md`.

## 🎯 Objectif (contrat, Annexe A — verbatim)
> "WEEK 6: MAIN EXPERIMENTS — During Week 6, the Intern shall execute the central experiments required to test the research hypothesis. The Intern shall: modify only one major experimental variable at a time where reasonably possible; use consistent datasets and metrics across comparisons; record all random seeds; use multiple random seeds where computationally feasible; retain essential checkpoints and configuration files; document failed and interrupted experiments; inspect individual examples in addition to aggregate metrics; verify that any apparent improvement does not result from data leakage; compare the results with the base model and the selected baselines."

## 🧭 Le dispositif, en une ligne

Les modèles CPT africains sont des checkpoints **base** : capables, jamais alignés. On fait l'étape InstructGPT — SFT puis DPO — et on mesure si elle part de meilleures fondations sur un backbone CPT que sur sa base d'origine.

| Bras | Modèle | Traitement | Rôle |
| :---- | :---- | :---- | :---- |
| **A0** | Qwen3.5-4B-Base | aucun | point de départ |
| **A1** | AfriqueQwen3.5-4B-50Langs | aucun | point de départ après CPT |
| **A2** | Qwen3.5-4B-Base | SFT → DPO | contrôle aligné |
| **A3** | AfriqueQwen3.5-4B-50Langs | SFT → DPO | cible alignée |

**Le claim est A3 − A2**, à données, recette et graines identiques. Langue : haoussa.

## ✅ Tâches (contrat, verbatim) — appliquées à ce sujet
- [x] modify only one major experimental variable at a time where reasonably possible; — A2 et A3 ne diffèrent que par le **backbone**. Mêmes données, mêmes hyperparamètres, même graine. Et les deux partagent le tokenizer (248 044 tokens), donc la tokenisation est contrôlée : aucun écart mesuré ne peut lui être attribué
- [x] use consistent datasets and metrics across comparisons; — socle unique : Aya 3 512 (SFT), Uhura 791 + UbuntuGuard 128 (DPO). Toutes licences propres, Apache-2.0 et MIT
- [x] record all random seeds; — `config.yaml` `training.seed`, et les graines dérivées du découpage (`seed`, `seed + 1`)
- [ ] use multiple random seeds where computationally feasible; — **3 graines si le filtre 3 le permet.** Le claim est une différence entre deux bras ; une différence sur une graine unique ne se distingue pas du bruit d'initialisation
- [ ] retain essential checkpoints and configuration files; — adaptateurs LoRA seuls, quelques dizaines de Mo, plus le `config.yaml` exact de chaque run
- [x] document failed and interrupted experiments; — le sujet v1 tout entier en est un : neuf déviations, `Week5_Deviations_From_Proposal.md`. Continuer pour le v2
- [ ] inspect individual examples in addition to aggregate metrics; — lire les sorties haoussa avant et après alignement. Le contrôle anglais reste le seul lisible sans locuteur natif
- [x] verify that any apparent improvement does not result from data leakage; — découpage au niveau `base_stem`, vérifié à zéro au notebook 03, **y compris entre SFT et DPO** — sans quoi le DPO réoptimiserait ce que le SFT a déjà vu
- [ ] compare the results with the base model and the selected baselines. — A0 et A1 sont exactement ça : les deux points de départ non alignés

## 📥 Livrables (contrat, verbatim)
- [x] the experimental scripts; — `src/train.py` (`run_sft`, `run_dpo`), `src/data.py`, `src/metrics.py`, `scripts/kaggle_run.py`. 107 tests
- [x] the configuration files; — `config.yaml`, sections `sft` et `dpo` séparées
- [ ] the training and evaluation curves; — `save_training_curves` écrit PNG + historique JSON à chaque run
- [ ] the result tables;
- [ ] qualitative examples;
- [ ] the experiment log;
- [ ] a summary of the provisional conclusions.

## 📅 Déroulé réel de la semaine

| Jour | Ce qui s'est passé |
| :---- | :---- |
| lun 31 août – mar 1ᵉʳ sept | Pause délibérée. Décision de repartir de zéro sur le sujet, en s'appuyant sur la revue systématique |
| mar 1ᵉʳ sept | Étape 1 : extraction des huit gaps déclarés par la revue |
| mer 2 sept | Étapes 2 et 3 : sujet Instruct-CPT défini, sources vérifiées et sélectionnées, notebook d'inspection exécuté, `run_sft` écrit, chaîne Kaggle montée |
| jeu 3 – ven 4 sept | Filtre 3, puis les quatre bras si le budget le permet |

## ⏭️ Prochaine action, précise

```
python scripts/kaggle_run.py push notebooks/04_filtre3_faisabilite.ipynb --accelerator --timeout 3600
```

Le filtre 3 mesure le temps par pas et la VRAM crête sur 8 pas de SFT puis 8 pas de DPO, et extrapole. Il produit `results/compute_estimate.json` — **le livrable d'estimation compute reporté depuis la semaine 5**, avec des chiffres mesurés.

Son verdict décide de la suite : quatre bras avec 3 graines, ou une seule graine déclarée comme limitation.

## ⚠️ Risques connus à l'entrée

| Risque | Traitement |
| :---- | :---- |
| Le budget ne permet qu'une graine | déclarer la limitation, ne pas la masquer. Une différence sur une graine unique n'est pas une preuve |
| Volume haoussa modeste : 3 512 SFT, 919 paires DPO | ConsistentGuard publie sur 1 000 exemples. Comparable, à déclarer |
| Auto-mutilation et contenu sexuel sans couverture native | limite de l'écosystème documentée par arXiv:2608.13695, à citer dans les limitations |
| L'axe Harmless est trop mince pour l'entraînement (26 paires) | bascule entièrement en évaluation, via AfriHate et TukaBench |
| Étiquettes UbuntuGuard non validées humainement | limite héritée. Sonde par locuteur natif haoussa envisagée depuis l'ENSPY |
| Sessions Kaggle froides : ~5 min de téléchargement par run | soumission batch plutôt qu'interactive, quota consommé seulement pendant l'exécution |

## 👉 Vers la semaine 7

Semaine 7 (Robustesse, ablations, analyse) prendrait :
- l'ablation de volume SFT, pour savoir combien de démonstrations suffisent
- le bras supplémentaire `afrisynt` — le volume compense-t-il l'absence de licence et de validation ?
- la généralisation au swahili, où MultiJail et RTP-LX fournissent des évaluations humainement validées que le haoussa n'a pas
