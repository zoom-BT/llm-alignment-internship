# Plan d'évaluation — sur Colab

**Principe de répartition :** Kaggle porte les entraînements longs en batch ; Colab porte les évaluations, en pilotage direct. Deux budgets GPU séparés, aucune interférence.

**Contrainte du canal Colab, mesurée le 2026-09-03 :** l'appel MCP expire à 120 s alors que la cellule continue de tourner côté Colab. Les barres de progression n'apparaissent pas dans ce qui remonte — seuls les `print` explicites sont visibles. Colab convient donc aux évaluations de quelques dizaines de minutes, pas aux runs de plusieurs heures.

---

## 1. Les quatre axes, et pourquoi trois se passent de juge

| Axe | Jeu | Mesure | Juge |
| :---- | :---- | :---- | :---- |
| **Honest** | Uhura `ha_multiple_choice` | log-vraisemblance sur les options | **non** |
| **Utilité** | AfriMGSM `hau` | correspondance de `answer_number` | **non** |
| **Harmless** | AfriHate haoussa | macro F1 sur trois étiquettes | **non** |
| **Refus** | TukaBench `afri-jbb-harm/benign` | taux de refus | **oui** |

Les trois premiers comparent **des nombres, pas des textes** : un indice d'option, un résultat arithmétique, une étiquette. La mesure est donc aussi fiable en haoussa qu'en anglais, ce qui est la seule façon pour cette équipe d'évaluer une langue qu'elle ne lit pas.

**AfriHate est scoré par log-vraisemblance des trois étiquettes**, pas par génération. Le modèle n'a pas à produire le mot « Hate » dans un format parsable : on compare les probabilités qu'il attribue à chacun. Cela supprime toute la classe d'échecs où un modèle connaît la réponse mais la formule d'une façon que le parseur rate — exactement ce qui rendait l'extraction de verdict du sujet v1 si fragile.

**TukaBench est le seul axe qui demande un jugement**, et il est donc traité en dernier, une fois les trois autres acquis.

---

## 2. Ordre d'exécution

Chaque étape produit un résultat exploitable seule. Si le temps manque, on s'arrête proprement au lieu de n'avoir rien.

| # | Quoi | Modèles | Durée estimée |
| :---- | :---- | :---- | ---: |
| **E1** | Uhura QCM, 808 questions | A0, A1 | ~50 min |
| **E2** | AfriMGSM `hau`, 250 questions | A0, A1 | ~40 min |
| **E3** | AfriHate haoussa | A0, A1 | ~30 min |
| **E4** | E1-E3 rejoués | A2, A3 *(après R1b/R2b)* | ~2 h |
| **E5** | TukaBench, refus et sur-refus | les quatre | à cadrer |

E1 est déjà lancé sur 60 questions à titre de validation. **Premier résultat : A0 à 0,367 contre un plancher de 0,267, p = 0,107** — au-dessus numériquement, indiscernable du hasard à cet effectif. C'est ce que les 808 trancheront.

E2 et E3 ne dépendent pas des entraînements : ils peuvent être faits pendant que Kaggle travaille.

E4 est le seul qui attend, puisqu'il évalue les adaptateurs produits par R1 et R2.

---

## 3. Ce que chaque axe autorise à conclure

**Honest (Uhura).** L'axe sur lequel on entraîne. Un gain ici après alignement est attendu ; c'est son ampleur relative entre A2 et A3 qui porte le claim.

⚠️ Le contenu d'Uhura est **occidental** — Amérique, Canada, autobahn — professionnellement traduit. On mesure donc la véracité sur du savoir occidental exprimé en haoussa, pas sur du savoir africain. Limite du jeu, à déclarer.

**Utilité (AfriMGSM).** Ne fait pas partie de l'entraînement, et c'est tout son intérêt : il détecte l'**oubli catastrophique**. Un alignement qui améliore la véracité en détruisant l'arithmétique n'est pas un progrès, et la littérature signale ce risque systématiquement.

**Harmless (AfriHate).** L'axe qu'on n'entraîne pas, faute de données — 26 paires seulement en haoussa dans UbuntuGuard. Il répond donc à une question de **transfert inter-axes** : aligner sur la véracité améliore-t-il aussi la modération ? Un gain serait un résultat en soi ; une absence de gain aussi.

**Refus (TukaBench).** Le seul axe demandant un juge, donc le seul dont la fiabilité devra être établie avant d'être citée.

---

## 4. Code disponible

| Module | Ce qu'il fait | Tests |
| :---- | :---- | ---: |
| `src/eval_mcq.py` | log-vraisemblance normalisée, QCM, test binomial | 10 |
| `src/eval_tasks.py` | extraction numérique, classification par vraisemblance | 10 |

Deux décisions de mesure, verrouillées par des tests parce qu'elles sont faciles à obtenir de travers :

**La vraisemblance est moyennée par token**, pas sommée. Une somme favoriserait mécaniquement les réponses courtes, chaque token ne pouvant que retrancher de la probabilité. Sur TruthfulQA, où la bonne réponse est souvent la plus longue et la plus nuancée, ce biais se mesurerait comme de l'ignorance.

**L'extraction numérique prend le dernier nombre**, pas le premier. Une solution détaillée cite ses opérandes avant de conclure ; prendre le premier reviendrait à scorer l'énoncé.

Et deux garde-fous de lecture :

**Le plancher aléatoire est calculé sur le nombre réel d'options par question.** Mesuré sur Uhura haoussa : 697 questions à 4 choix, 89 à 3, 22 à 2 — le plancher vaut **0,267 et non 0,25**. Une différence de 1,7 point, qui compte quand l'écart mesuré est de dix.

**Chaque score est accompagné d'un test binomial bilatéral.** Dépasser le plancher ne prouve rien en soi : 202 bonnes réponses sur 809 à quatre options, c'est exactement le hasard.

---

## 5. Points ouverts

- **La taille d'AfriHate en haoussa** n'a jamais été vérifiée. À mesurer avant E3, comme tout le reste.
- **Le seuil de refus de TukaBench** demande un juge dont la fiabilité doit être établie — le protocole existe déjà dans `Judge_Validation_Protocol.md`, écrit pour le sujet v1 et transposable.
- **Faire transiter un adaptateur de Kaggle vers Colab** : `/kaggle/working` ne survit pas au passage. Il faudra le publier en dataset Kaggle ou passer par Drive. À régler avant E4.
