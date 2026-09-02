# Sujet v2 — Étape 3 : sélection des sources

**Décision de conception :** le résultat principal ne repose que sur des sources à **licence explicite et permissive**. Les sources à licence absente ou non confirmée servent de supplément déclaré, jamais de socle. Si une licence se révèle problématique en semaine 8, le papier tient toujours debout.

Langue principale : **haoussa**. Le swahili est gardé en réserve comme test de généralisation, pas comme second bras d'entraînement.

---

## 1. Le socle — licences propres, résultat principal

| Rôle | Source | Haoussa | Licence | Provenance |
| :---- | :---- | ---: | :---- | :---- |
| **SFT** | `CohereLabs/aya_dataset` | **3 512** | **Apache-2.0** | nativement rédigé par des locuteurs, validation humaine documentée |
| **DPO — Honest** | Uhura-TruthfulQA `ha_generation` | **799** | **MIT** | traduction professionnelle humaine |
| **DPO — Harmless** | UbuntuGuard, tranche haoussa | **26** ⚠️ | CC BY 4.0 *(papier, à confirmer)* | contenu ancré en contexte africain |

**Total DPO du socle : 919 paires**, mesuré au notebook `03_sources_haoussa.ipynb` (Uhura 791 + UbuntuGuard 128). ConsistentGuard publie sur 1 000 exemples ; on est dans le même ordre de grandeur, et c'est à déclarer comme tel plutôt qu'à masquer.

**⚠️ Correction (2026-09-02) — l'axe Harmless est bien plus mince qu'annoncé ici.** Une version antérieure comptait les 128 paires haoussa d'UbuntuGuard comme apport Harmless. C'est faux : ventilées par thème, elles se décomposent en **95 Honest** (désinformation, conseil spécialisé) et **26 Harmless** (stéréotypes 20, discours haineux 6), plus 7 en intérêt public, écartées des deux axes.

À 26 paires, **l'axe Harmless n'est plus entraînable** — il devient évaluable seulement, via AfriHate et TukaBench. Conséquence directe sur le dispositif : le DPO du socle porte en pratique sur l'axe Honest (791 Uhura + 95 UbuntuGuard = 886 paires), et le Harmless passe entièrement du côté évaluation. C'est cohérent avec D9 du sujet v1, qui était arrivé à la même conclusion sur les dix langues réunies ; le haoussa seul la rend encore plus nette.

Même ventilation en yoruba, pour comparaison : 68 paires au total, 53 Honest, 14 Harmless.

**⚠️ Le haoussa n'est pas la langue africaine la mieux dotée dans Aya.** Mesuré : il arrive **21ᵉ sur 71 langues**, et le **yoruba y compte 11 758 exemples contre 3 512** — 3,3 fois plus. Ce point contredit partiellement le choix de langue et doit être posé plutôt qu'omis.

Le haoussa reste retenu, mais l'arbitrage est plus serré qu'annoncé :

| | Haoussa | Yoruba |
| :---- | ---: | ---: |
| Aya (SFT) | 3 512 | **11 758** |
| afrisynt (DPO) | **6 290** | 2 779 |
| UbuntuGuard (DPO) | **128** | 68 |
| LSR, TukaBench, AfriMGSM, AfriHate | oui | oui |
| Locuteur natif joignable depuis l'ENSPY | **oui** | non |

Le yoruba gagne sur le SFT, le haoussa sur les deux sources DPO et sur la vérifiabilité humaine. Comme le DPO est le cœur du dispositif et que la validation par locuteur natif est la seule réponse à la limite héritée de D5, le haoussa tient — mais le yoruba est un repli documenté si le SFT s'avère insuffisant.

**Aya est la pièce maîtresse.** 3 512 exemples haoussa *nativement rédigés* — pas traduits — sous Apache-2.0, avec 18 570 téléchargements mensuels. C'est la meilleure source trouvée depuis le début du projet, tous critères confondus : provenance, licence, validation. Le rapport de recherche l'annonçait à 1 200-1 500 ; la mesure directe donne 3 512.

---

## 2. Les suppléments — volume contre provenance

| Source | Haoussa | Licence | Ce qu'elle apporte | Ce qui la disqualifie comme socle |
| :---- | ---: | :---- | :---- | :---- |
| `afrisynt/dpo` | **6 290** | **aucune** | axe Helpful, adhérence linguistique | pas de licence, entièrement synthétique, zéro validation humaine |
| `saillab/alpaca-hausa-cleaned` | 52 002 | **aucune** | volume SFT | pas de licence, traduction automatique non éditée |

**Usage prévu :** un bras supplémentaire, exécuté et rapporté séparément, pour répondre à la question « le volume compense-t-il la provenance ? ». Jamais mélangé au socle sans le dire.

`afrisynt/dpo` mérite une mention particulière : il ne mesure pas la sécurité mais **l'adhérence linguistique** — le modèle répond-il vraiment dans la langue demandée, ou retombe-t-il en anglais ? C'est l'axe *Helpful* des trois H, et c'est le plus directement lié à ce que le CPT est censé apporter.

---

## 3. L'évaluation — tenue à l'écart, et sans juge autant que possible

Aucune source d'entraînement ne sert à l'évaluation. Aucune source d'évaluation ne sert à l'entraînement.

| Axe | Source | Mesure | Juge nécessaire |
| :---- | :---- | :---- | :---- |
| **Honest** | Uhura `ha_multiple_choice` | log-vraisemblance sur 4 options | **non** |
| **Helpful / utilité** | AfriMGSM `hau` | correspondance de `answer_number` | **non** |
| **Harmless** | AfriHate, tranche haoussa | macro F1 de classification | **non** |
| **Harmless** | TukaBench `afri-jbb-harm` haoussa | taux de refus | oui |
| **Sur-refus** | TukaBench `afri-jbb-benign` haoussa | refus sur requêtes légitimes | oui |

**Trois axes sur cinq se mesurent sans aucun jugement de modèle.** C'est ce qui rend le projet évaluable par une équipe qui ne lit pas le haoussa.

AfriMGSM joue un rôle double : mesure d'utilité, et **détection de l'oubli catastrophique** après alignement — le risque que la littérature signale systématiquement.

⚠️ **Piège de nommage vérifié :** les configs AfriMGSM sont en ISO trois lettres — `hau`, `swa` — et non `ha`, `sw` comme l'annonce la carte. 19 configs, pas 17.

---

## 4. La méthode empruntée, sans les données

**LSR** (Faruna 2026, CC-BY-SA 4.0) apporte deux choses réutilisables et aucune donnée exploitable :

- le **protocole à double sonde** — même question en anglais et en langue cible, soumise au même modèle
- la métrique **Refusal Centroid Drift**, qui nomme l'écart entre les deux

Ses 14 sondes sont trop peu pour évaluer quoi que ce soit, et un seul modèle a été mesuré avec, fermé. Mais RCD donne un nom citable à ce que notre contrôle anglais mesurait déjà sans le nommer.

---

## 5. Écarté, et pourquoi

| Source | Motif |
| :---- | :---- |
| **Bactrian-X** | **aucun config haoussa** — 52 configs vérifiées, `sw` présent, `ha` absent. Le rapport annonçait 8 435 exemples haoussa ; ils n'existent pas |
| **AfriSpeech-Dialog** | `language: ['en']` — anglais à accent africain, tâche de reconnaissance vocale. Ce sont des accents, pas des langues |
| **MultiJail** | haoussa absent (10 langues, `sw` seul). Licence MIT, non Apache-2.0 comme annoncé. Réservé au swahili |
| **RTP-LX** | haoussa absent des 38 langues. Licence MIT confirmée côté Microsoft. Réservé au swahili |
| **Inkuba-Instruct** | dépôt *gated*, contenu invérifiable — et Aya fait mieux sur tous les critères |
| **HealthBench-Africa** | pas de couverture haoussa |
| **IrokoBench** (hors AfriMGSM) | AfriXNLI et AfriMMLU n'ajoutent rien que AfriMGSM ne couvre déjà pour l'utilité |

---

## 6. Ce que la littérature nous dispense de démontrer

**[Language-Specific Gaps in AI Safety Training Datasets](https://arxiv.org/abs/2608.13695)** — Onuoha, Sunu & Sikiru, août 2026. Audit de 21 ressources sur 25 tranches linguistiques, avec exactement trois paliers : **haoussa (bas), swahili (moyen), français (haut)**.

Trois conséquences directes :

1. **Notre motivation est établie par un tiers.** Nous n'avons plus à argumenter que le trou existe — un audit indépendant, sur nos deux langues, publié il y a trois semaines, le documente.
2. **Ils n'évaluent aucun modèle**, explicitement. Notre travail se place en aval du leur, sans recouvrement.
3. **Une limitation nous est imposée et doit être déclarée :** auto-mutilation et contenu sexuel n'ont *aucune* couverture en langue native dans les deux paliers africains. L'alignement produit aura donc des catégories de préjudice non couvertes — limite de l'écosystème, pas du travail, mais à écrire noir sur blanc avec cette citation.

Le dataset d'audit lui-même est disponible : `ChialukaOnuoha/safety-slice-audit`, CC BY 4.0.

---

## 7. Récapitulatif — qui fait quoi

```
SOCLE (licences propres)  -- tous les chiffres mesures, notebook 03
  SFT   ──► Aya haoussa, 3 512, Apache-2.0, natif      -> 2 810 train / 702 eval
  DPO   ──► Uhura ha_generation, 791, MIT              [Honest]
        └─► UbuntuGuard haoussa, 128 dont 95 Honest    [Honest surtout]
            (26 Harmless seulement : trop peu pour entrainer, bascule en evaluation)
            total DPO socle -> 735 train / 184 eval

SUPPLÉMENT (rapporté séparément)
  DPO   ──► afrisynt/dpo, 6 290, sans licence, synthétique         [Helpful]
  SFT   ──► alpaca-hausa, 52 002, sans licence, traduction machine

ÉVALUATION (jamais utilisée à l'entraînement)
  sans juge ──► Uhura ha_multiple_choice        [Honest]
            ──► AfriMGSM hau                    [utilité + oubli catastrophique]
            ──► AfriHate haoussa                [Harmless]
  avec juge ──► TukaBench harm / benign         [refus, sur-refus]

MÉTHODE (pas de données)
            ──► LSR : double sonde + métrique RCD
```

---

## 8. Ce qui reste à faire sur les sources

1. Confirmer la licence UbuntuGuard auprès de l'autrice — email rédigé, toujours pas envoyé
2. Vérifier la tranche haoussa d'AfriHate : volume exact et équilibre des classes
3. Télécharger le zip RTP-LX si le swahili entre dans le périmètre
4. Décider si `afrisynt/dpo` est utilisé, sachant qu'il n'a pas de licence — mon avis : oui, en supplément déclaré, jamais dans le socle
