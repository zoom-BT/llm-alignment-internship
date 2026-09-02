# Estimation des ressources de calcul

**Livrable contractuel** (Annexe A, semaine 5 — verbatim) : *« estimate the computing time, memory requirements, and financial cost where applicable »* et *« a computing-resource estimate »*. Reporté depuis la semaine 5 faute de session GPU ; établi le 2026-09-03 sur **mesure réelle**, pas sur estimation.

**Source :** run `balbinotchoutzine/04-filtre3-faisabilite`, statut `COMPLETE`, mesuré sur 8 pas de SFT puis 8 pas de DPO, extrapolé au nombre de pas d'une run complète.

---

## 1. Matériel

| | |
| :---- | :---- |
| GPU | Tesla T4 (Kaggle, accélérateur « T4 x2 ») |
| VRAM par appareil | 15,64 Go |
| Appareils visibles | 2, mais **un seul utilisé** — voir §4 |
| Quota | 30 h/semaine, sessions plafonnées à 9 h |
| Coût financier | **nul** — Kaggle gratuit, aucun service payant |

---

## 2. Mesures

| Phase | s/pas | VRAM crête | Pas d'une run complète | Durée |
| :---- | ---: | ---: | ---: | ---: |
| **SFT** (Aya, 2 810 exemples, 2 époques) | **56,8** | **7,51 Go** | 352 | **5,55 h** |
| **DPO** (Uhura + UbuntuGuard, 735 paires, 3 époques) | **109,8** | **11,95 Go** | 138 | **4,21 h** |
| **Un bras complet** | | | 490 | **9,76 h** |

Le DPO coûte **1,93 fois** le SFT par pas — cohérent avec ce qu'il fait : un passage avant sur le modèle de référence figé en plus du modèle entraîné, sur `chosen` **et** `rejected`.

La libération mémoire entre les deux phases est propre : 0,02 Go résiduels.

---

## 3. Budget du dispositif

| | Heures |
| :---- | ---: |
| Un bras (A2 ou A3) | 9,76 |
| Deux bras, une graine | 19,5 |
| **Deux bras, trois graines** | **58,6** |
| A0 et A1 (évaluation seule, sans entraînement) | ~1 |
| **Total prévu** | **~60** |
| Budget disponible (3 semaines × 30 h) | 90 |
| **Marge** | **~30 h** |

**Les trois graines tiennent.** La marge de 30 h couvre les échecs, les reprises et les évaluations intermédiaires.

**Contrainte de session, plus structurante que le quota :** 9 h par session contre 9,76 h pour un bras complet. Un bras ne tient donc **pas** dans une seule session — il faut soit soumettre SFT et DPO séparément, soit reprendre depuis le checkpoint SFT. C'est le point à régler avant de lancer les runs réels.

---

## 4. Ce qui a rendu ces chiffres atteignables

Dix-huit versions du notebook ont été nécessaires. Quatre décisions expliquent l'écart entre l'échec et la mesure.

**`chunked_nll` — le facteur décisif.** Le vocabulaire d'AfriqueQwen compte **248 044 tokens**, si bien que les logits de la fonction de perte — `batch × seq × 248 044` — dominent la mémoire, loin devant les poids. Trois runs consécutifs ont échoué sur ce seul tenseur. TRL découpe cette cross-entropy par défaut ; la désactiver était une erreur, corrigée. VRAM du SFT : **13,06 Go → 7,51 Go**.

**Le `gradient_checkpointing` n'y peut rien.** Il recalcule les activations intermédiaires ; les logits de la perte sont matérialisés d'un bloc et lui échappent entièrement. C'est le raisonnement qui a coûté deux runs.

**Un seul GPU visible.** `Trainer` active DataParallel dès qu'il en voit plusieurs, doublant silencieusement le nombre de séquences par pas — `per_device_train_batch_size=2` en traitait 4. `CUDA_VISIBLE_DEVICES=0` supprime l'ambiguïté.

**Longueurs de séquence mesurées, non héritées.** Le `max_seq_length: 2560` venait de la tâche gardien du sujet v1, qui embarquait des transcripts entiers. Mesuré sur les vraies données haoussa : Aya a une médiane de **46 tokens**, les paires DPO plafonnent à **974**. `1024` ne tronque rien côté DPO et 2,5 % côté SFT, sur des valeurs extrêmes.

---

## 5. Leviers non exploités

Consignés sans être activés : la configuration actuelle fonctionne et le budget tient, il serait imprudent d'y toucher maintenant.

| Levier | Gain attendu | Risque |
| :---- | :---- | :---- |
| Batch plus large | le DPO plafonne à 11,95 Go sur 15,64, le SFT à 7,51 — il reste de la place | remonte le mur mémoire, quatre fois rencontré |
| fp16 plutôt que bf16 | `torch.cuda.is_bf16_supported()` renvoie `True` sur T4, mais Turing n'a pas de tensor cores bf16 natifs : possible émulation | à mesurer, gain incertain |
| Le second GPU | inutilisé | `device_map="auto"` est incompatible avec `chunked_nll`, qui vaut plus cher |

---

## 6. Comparaison à l'estimation du proposal

Le proposal (section 12) annonçait *« une expérience initiale complète en moins de 2 heures »* et *« moins de 12 h par expérience »*.

**Un bras coûte 9,76 h.** Le second chiffre tient ; le premier était optimiste d'un facteur cinq. L'écart s'explique : le proposal supposait 1 000 paires DPO et n'anticipait ni le SFT — indispensable puisque les deux backbones sont des checkpoints base — ni le coût d'un vocabulaire de 248 044 tokens.

À déclarer tel quel dans le rapport plutôt qu'à ajuster rétrospectivement.
