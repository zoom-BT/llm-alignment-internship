# Semaine 5 — Synthèse pour la supervision

**Période :** 24–28 août 2026 · **Sujet :** alignement de sécurité par DPO sur modèles de fondation multilingues africains
**Proposal de référence :** `04_Weekly_Reports/Week_04_Research_Proposal.md`, approuvé le 25 août 2026

Document de présentation. Le journal de travail détaillé, avec les vérifications ligne à ligne, est dans `03_Experiments/Week5_Deviations_From_Proposal.md` (déviations D1 à D9).

---

## 1. En une page

La semaine devait produire une baseline. Elle a produit autre chose : la démonstration que la baseline prévue aurait été fausse.

Neuf problèmes ont été identifiés en confrontant le proposal aux données réelles. Six relèvent des données ou de l'exécution et se corrigent. **Trois modifient le proposal approuvé** et demandent une validation.

Le point saillant : **trois des problèmes techniques auraient produit des résultats plausibles et faux**. Aucun n'aurait provoqué d'erreur. Les entraînements auraient tourné, affiché des courbes crédibles et rempli un tableau de résultats — sur un signal détruit. C'est ce qui justifie d'avoir consacré la semaine à la vérification plutôt qu'à l'exécution.

Les modèles, le protocole expérimental et le budget compute restent inchangés.

---

## 2. Les trois changements à valider

### 2.1 — Le claim principal passe de H1 à H2

**Constat.** La question sous-jacente à H1 — *la qualité de traduction des données d'alignement affecte-t-elle le transfert de sécurité ?* — est déjà répondue dans la littérature. Une revue systématique récente (Lemofouet et al., arXiv:2608.14626, méthodologie PRISMA sur environ 1 500 papiers, acceptée au workshop LM4UC d'IJCAI) recense quatre travaux convergents : LionGuard 2 (« les données d'entraînement naïvement traduites dégradent la performance »), Paul et al. 2025 (40 k échantillons filtrés égalent 200 k non filtrés), Ge et al. 2025, CultureGuard.

Le repli envisagé — arguer que les *paires de préférence* se dégradent différemment des cibles SFT — ne tient pas non plus : le DPO multilingue de sécurité est un domaine actif (MPO, Lim et al. 2025, Paul et al. 2025).

**Ce que la même revue déclare non couvert**, textuellement : le *continued pre-training* n'y figure pas comme méthode, et ses perspectives appellent à valider « le fine-tuning à paramètres efficients, la synthèse de données et le transfert cross-lingue » spécifiquement « dans le contexte des langues africaines ».

Sa discussion pose même le blocage comme une prémisse : *« tant que les modèles pré-entraînés manquent de couverture de ces langues, les gains apportés par ces techniques restent marginaux »*.

**Proposition.** H2 devient le claim principal : *le pré-entraînement continu en langues africaines améliore-t-il la rétention de l'alignement de sécurité ?* AfriqueQwen3.5-4B-50Langs ne manque pas de cette couverture — 35,5 milliards de tokens africains. L'étude teste donc directement la relation causale sur laquelle la revue s'appuie, avec un modèle qui n'existait pas quand cette affirmation a été formulée.

**Conséquence.** Change le titre, la question de recherche (section 3) et la contribution C2. H1 devient un axe secondaire, ou est abandonnée.

### 2.2 — La métrique : UbuntuGuard n'est pas un benchmark de génération

**Constat.** Le script d'évaluation publié par les auteurs révèle la nature réelle de la tâche : le modèle évalué reçoit un couple `(politique, transcript)` et répond `PASS` ou `FAIL`. Il est **juge**, pas agent. Le score est une exactitude et un macro F1 contre les étiquettes du jeu.

L'inspection des exemples le confirme : **les réponses PASS ne sont pas des refus.** Ce sont des réponses conformes et utiles — elles traitent la question, corrigent l'erreur, citent l'autorité compétente. L'axe du benchmark est *conformité contre violation*, non *refus contre obtempération*.

**Conséquence.** Le Refusal Rate et l'Over-Refusal Rate (section 9) ne mesurent rien sur ces données. La métrique devient le **macro F1 du modèle gardien**, qui sert simultanément de score et de **précision déclarée du détecteur de conformité**.

**Deux garanties méthodologiques** attachées à ce choix :

- Le juge tourne sur le backbone de **contrôle** (Qwen3.5-4B-Base), pas sur le modèle cible. Un juge partageant son backbone avec l'agent qu'il note favoriserait cet agent — et comme H2 compare précisément un agent Qwen-Base à un agent AfriqueQwen, un juge AfriqueQwen gonflerait l'effet revendiqué. Tout biais d'affinité joue donc **contre** l'hypothèse : le test est conservateur.
- Découpage à trois voies (juge / agent / évaluation) sans question partagée, pour que le juge ne note jamais un transcript sur lequel il a été entraîné.

### 2.3 — L'axe d'étude : Honest plutôt que Harmless seul

**Constat.** Le sujet avait été cadré en semaine 4 sur l'axe *Harmless* uniquement. Le comptage du champ `theme` d'UbuntuGuard contredit ce cadrage :

| Thème | Lignes | Part | Axe |
| :---- | ---: | ---: | :---- |
| désinformation | 1 032 | 45 % | **Honest** |
| intérêt public | 463 | 20 % | ambigu |
| stéréotypes | 394 | 17 % | **Harmless** |
| conseil spécialisé | 241 | 10 % | **Honest** |
| discours haineux | 177 | 8 % | **Harmless** |

Traduit en paires exploitables, **Harmless seul ne laisse que 216 paires d'entraînement et 57 d'évaluation** réparties sur dix langues — avec le luganda à 5 paires au total et le nyanja à 6.

Les autres jeux ne peuvent pas combler ce côté : AfriHate ne fournit que des étiquettes sans réponses, TukaBench que des prompts sans réponses. Ni l'un ni l'autre ne donne de paires de préférence sans génération ni jugement supplémentaires. À l'inverse, Uhura-TruthfulQA fournit `best_answer` et `incorrect_answers`, donc des paires Honest immédiatement utilisables.

**Proposition.** Entraîner sur l'axe Honest, évaluer sur les deux.

La question devient : *le pré-entraînement africain améliore-t-il davantage l'alignement sur la véracité que sur l'évitement du préjudice ?* Avec un mécanisme derrière — les échecs Honest sont des échecs de **connaissance** (savoir ce que dit la loi ghanéenne, ce qu'est l'Asaro yoruba), ce que le pré-entraînement injecte ; les échecs Harmless sont des échecs de **comportement**, qui transfèrent plus facilement depuis l'alignement anglais. **Prédiction falsifiable : le CPT aide davantage sur Honest.**

**Point d'honnêteté.** Cela réintroduit l'axe Honest écarté en semaine 4. La différence : il avait été écarté comme *second corps de travail*. Ici c'est une **stratification d'un seul résultat** — mêmes données, mêmes modèles, mêmes entraînements, le champ `theme` servant à ventiler le compte rendu. Coût marginal quasi nul.

---

## 3. Problèmes de données

| Réf. | Constat | Traitement |
| :---- | :---- | :---- |
| **D1** | **Aucun split d'entraînement publié.** Vérifié sur l'historique git complet du dépôt : aucun fichier d'entraînement n'a jamais été committé. Le papier rapporte les tailles dans sa Table 3 mais ne s'engage nulle part explicitement à les publier | Découpage propre des données de test : **1 089 paires → 869 entraînement / 220 évaluation** |
| **D2** | Les fichiers `crosslingual` et `translated` ne constituent pas l'axe natif/traduit du proposal. Ils diffèrent **uniquement par la langue de la politique** — 2 307 lignes sur 2 307, zéro différence de transcript | Les volumes ne s'additionnent pas. Axe abandonné |
| **D3** | Licence CC BY 4.0 annoncée dans le papier, mais **aucun fichier LICENSE** dans le dépôt | Demande de confirmation à l'autrice correspondante, en cours |
| **D4** | Le contenu en langues africaines d'UbuntuGuard est lui-même **traduit automatiquement** (Google Translate). Même constat pour HealthBench-Africa (gpt-4o-mini) | Confirme que H1 était inopérante : deux traductions machine comparées entre elles |
| **D5** | Les étiquettes PASS/FAIL **n'ont jamais été validées par un humain** — générées par Llama-3.1-405B et Qwen3-235B, avec contrôles structurels automatiques uniquement. Le papier reconnaît un validateur unique pour 4 langues sur 10 | Limitation héritée, déclarée. Le juge mesure un **accord** avec ces étiquettes, pas une **justesse** |
| **D7** | Le pool d'évaluation avait été estimé à environ 1 900 prompts. **Réel : 192 prompts africains**, plus 337 questions de contrôle anglais | Impose le test apparié de McNemar au lieu de Fisher, et interdit toute conclusion par langue |

**Six jeux de données validés** contre leurs sources primaires plutôt que contre leurs fiches descriptives : UbuntuGuard, AfriHate, HealthBench-Africa, Uhura-TruthfulQA, IrokoBench, TukaBench. Des incohérences entre la prose des fiches et les données réelles ont été trouvées dans presque chacun — ce constat est en soi une contribution documentaire.

---

## 4. Problèmes techniques découverts à l'exécution

Aucun de ceux-ci ne figurait dans un document. Ils sont apparus en écrivant puis en lançant le code.

**Les trois premiers auraient produit des résultats plausibles et faux, sans jamais provoquer d'erreur.**

| Problème | Ce qu'il aurait produit |
| :---- | :---- |
| **Contamination cross-lingue.** 265 questions sur 566 existent dans plusieurs langues. Un découpage par identifiant de ligne mettait **54 % des questions d'évaluation dans l'entraînement**, sous une autre langue | De la mémorisation, présentée et publiée comme du transfert cross-lingue |
| **Troncature silencieuse.** Longueur de séquence fixée à 1 024, puis 2 048, alors que la tâche gardien culmine à 2 060 tokens | Des entraînements complets sur des verdicts coupés — courbe de loss crédible, signal détruit |
| **Extracteur de verdict biaisé.** La règle des auteurs renvoie FAIL dès que le mot apparaît, or les modèles raisonnent en prose avant de conclure | FAIL prédit 9 fois sur 10. Un score de parseur pris pour un score de modèle |
| Budget de génération à 64 tokens, insuffisant pour des modèles qui raisonnent | 100 % de sorties non exploitables, interprétées à tort comme un échec des modèles |
| `target_modules` non spécifié — PEFT n'a pas de correspondance pour l'architecture `qwen3_5` | Arrêt au lancement de l'entraînement |
| bf16 demandé sur GPU T4, qui ne le supporte pas — remontée silencieuse en fp32 | Mémoire doublée, dépassement mémoire |
| Vocabulaire de 248 044 tokens : les logits DPO occupent 2,5 Go par séquence, doublés pour chosen et rejected | Dépassement mémoire sur T4 |

---

## 5. Ce que la semaine a produit

**Livré**

- Fiche descriptive de six jeux de données, chacun vérifié contre sa source primaire
- Pipeline de traitement implémenté et testé — **88 tests**, exécutables sans GPU
- Découpage sans contamination, vérifié à zéro sur trois contrôles indépendants
- Script d'évaluation reproductible, avec protocole de validation du juge
- Notebook d'inspection des données, exécuté et versionné avec ses sorties
- Liste des modes d'échec : les neuf déviations

**Reporté en semaine 6** — les quatre tâches restantes dépendent d'une seule et même chose, une première session GPU : évaluation des modèles non modifiés, baseline, estimation compute, reprise sur checkpoint.

**Première mesure réelle obtenue** : sur la tâche gardien, Qwen3.5-4B-Base atteint un macro F1 de 0,537 contre un plancher de classe majoritaire à 0,333 — sans aucun entraînement. Le juge part d'une base non nulle.

---

## 6. Comment le juge sera validé sans lire les langues

Question méthodologique centrale, puisque l'équipe ne lit aucune des dix langues cibles.

Le juge n'est pas évalué sur la qualité de ses réponses mais sur **un mot**. Il produit `PASS` ou `FAIL`, comparé à l'étiquette du jeu. La comparaison est indépendante de la langue.

Quatre contrôles, tous réalisables sans locuteur natif :

1. **Contrôle anglais.** 337 questions existent dans le fichier anglais et dans **aucun** fichier africain — soit 555 exemples sur l'axe Honest. Elles sont lisibles, donc vérifiables à la main. L'écart entre le F1 anglais et le F1 africain **est lui-même un résultat** : c'est la dégradation cross-lingue, le phénomène que l'étude examine.
2. **Plancher.** Le jeu d'évaluation est presque équilibré ; répondre toujours PASS donne 0,333 de macro F1. Un juge à ce niveau n'a rien appris.
3. **F1 par langue.** Mesurable sans lire aucune langue, et détermine sur quelles langues des conclusions sont permises.
4. **Accord entre deux juges** entraînés avec des graines différentes, sans aucune étiquette de référence.

**Limite assumée :** rien ne permet d'établir que les étiquettes d'UbuntuGuard sont correctes (D5). Le juge mesure un accord. Une sonde partielle est envisagée — un locuteur natif sur une trentaine d'exemples dans une langue — décrite comme sonde et non comme validation.

**Règle permanente :** aucune affirmation dans les résultats ne sera énoncée avec plus de précision que la fiabilité mesurée du juge ne le permet.

---

## 7. Décisions demandées

1. **Validation du recentrage de H1 vers H2**, avec les conséquences sur le titre, la question de recherche et la contribution C2.
2. **Validation de la métrique gardien** en remplacement du Refusal Rate.
3. **Validation de l'orientation Honest** avec Harmless en axe de contraste, qui réintroduit un axe écarté en semaine 4.
4. **Avis sur la validation du juge** : les quatre contrôles décrits suffisent-ils, ou faut-il chercher une validation par locuteurs natifs avant d'aller plus loin ?
