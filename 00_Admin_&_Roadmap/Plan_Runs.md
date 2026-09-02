# Plan de runs — sujet v2

**Budget réel :** 3 semaines × 30 h de quota Kaggle hebdomadaire = **90 h**, sessions plafonnées à **9 h**.
**Coût mesuré** (2026-09-03, run `04-filtre3-faisabilite`, statut `COMPLETE`) : **9,76 h par bras** — SFT 5,55 h à 56,8 s/pas, DPO 4,21 h à 109,8 s/pas. Deux bras sur trois graines : **58,6 h sur 90**, marge ~30 h. Détail dans `03_Experiments/Estimation_Compute.md`.

**⚠️ Un bras ne tient PAS dans une session.** 9,76 h contre un plafond de 9 h. C'est la contrainte qui structure le plan, et elle impose de découper : SFT et DPO en deux soumissions séparées, le second reprenant l'adaptateur produit par le premier.

---

## 1. Les runs à produire

Chaque bras se découpe en **deux soumissions**, puisqu'il dépasse le plafond de session.

| # | Run | Contenu | Coût mesuré | Dépend de |
| :---- | :---- | :---- | ---: | :---- |
| R0 | **A0 + A1**, évaluation seule | aucun entraînement | ~0,5 h | rien |
| R1a | **A2** (Qwen-Base), graine 42 | SFT | 5,55 h | R0 pour la métrique |
| R1b | A2, graine 42 | DPO depuis l'adaptateur R1a | 4,21 h | R1a |
| R2a | **A3** (AfriqueQwen), graine 42 | SFT | 5,55 h | — |
| R2b | A3, graine 42 | DPO depuis l'adaptateur R2a | 4,21 h | R2a |
| R3a/b … R6a/b | graines 43 et 44 | idem | 9,76 h par bras | la graine précédente réussie |

**Point technique à régler avant R1a :** le DPO doit repartir de l'adaptateur LoRA produit par le SFT, non du modèle de base. `run_dpo` accepte déjà un `model_path` ; il faut lui passer le checkpoint SFT et vérifier que PEFT recharge correctement l'adaptateur.

**R0 en premier, et sans discussion.** Il ne coûte presque rien, ne dépend d'aucune décision encore ouverte, et produit la première ligne du tableau de résultats. Si la chaîne d'évaluation a un défaut, il vaut mieux le découvrir sur un run d'une demi-heure que sur un run de six.

---

## 2. Séquencement journalier

Le principe : **une paire A2/A3 par jour, sur la même graine**. Jamais deux graines différentes le même jour, pour que si une journée est perdue, ce soit une graine complète et non un demi-appariement.

| Jour | Runs | Ce qu'on regarde le soir |
| :---- | :---- | :---- |
| **J1** | R0 | La chaîne d'évaluation fonctionne-t-elle bout en bout ? Les scores de A0 et A1 sont-ils au-dessus du plancher ? |
| **J2** | R1 puis R2 | Le SFT converge-t-il ? Le temps réel par pas confirme-t-il l'estimation ? |
| **J3** | R3 puis R4 | Deuxième graine. L'écart A3−A2 va-t-il dans le même sens qu'à la graine 42 ? |
| **J4** | R5 puis R6 | Troisième graine. Le signe de l'écart est-il stable sur les trois ? |
| **J5** | analyse | McNemar apparié, ventilation Honest/Harmless, tableau de résultats |

Deux runs de 5 h dans une journée tiennent : ils sont soumis en batch et n'occupent pas la machine locale.

---

## 3. Colab en second canal

Colab sert ce que Kaggle fait mal, pas la même chose en double.

| | Kaggle batch | Colab + colab-mcp |
| :---- | :---- | :---- |
| **Pour** | les six runs d'entraînement | itération, débogage, préparation de données |
| **Durée** | jusqu'à 9 h, sans surveillance | session navigateur à garder ouverte |
| **Qui pilote** | soumission fire-and-forget | pilotage direct, sortie immédiate |

Concrètement : si un run échoue à J2, on ne repousse pas six fois sur Kaggle en attendant vingt minutes à chaque essai. On reproduit sur 50 exemples dans Colab, on corrige en direct, et on ne repart sur Kaggle qu'une fois le problème réglé.

C'est le canal qui manquait aujourd'hui : neuf versions du même notebook, chacune coûtant un aller-retour complet pour découvrir une erreur de configuration.

---

## 4. Règles de conduite

**Une seule variable change entre R1 et R2.** Même graine, mêmes données, même recette, même longueur de séquence. Seul le backbone diffère. C'est ce qui rend l'écart attribuable.

**Toutes les graines sont notées, y compris celles dérivées.** `training.seed` et la graine du découpage (`seed`, `seed + 1`).

**Un run échoué est documenté, pas effacé.** Le contrat le demande explicitement, et les neuf échecs d'aujourd'hui ont chacun enseigné quelque chose.

**Ne jamais republier le dataset données.** Il ne change pas. Seul `dataset code` est repoussé à chaque itération — 0,1 Mo contre 31 Mo.

**Vérifier que `dataset code` réussit avant de pousser le kernel.** Rien dans la sortie du push ne signale que le code attaché est périmé ; c'est déjà arrivé, et le run a tourné sur l'ancienne version.

---

## 5. Le seuil d'abandon

Si à J3 le signe de l'écart A3−A2 s'inverse entre les graines 42 et 43, ce n'est pas un bug à corriger : c'est un résultat. Il indique que l'écart est du bruit, et la troisième graine sert alors à le confirmer plutôt qu'à espérer un renversement.

Ce cas est prévu, et il reste publiable — un résultat négatif sur une question que la revue systématique déclare ouverte a de la valeur. Ce qui ne serait pas publiable, c'est de relancer jusqu'à obtenir le signe voulu.
