# Sujet v2 — Étape 2 : Instruct-CPT pour l'Afrique

**Statut :** candidat retenu à l'itération 2. Non figé.
**Étape précédente :** `Sujet_v2_01_Gaps_Revue.md` — les huit gaps déclarés par la revue systématique.

---

## 1. L'idée en une phrase

GPT-3 était un modèle base : capable, mais ne respectant pas les 3H. InstructGPT a comblé cet écart par SFT puis apprentissage à partir de préférences humaines.

**Les modèles CPT africains sont exactement dans la position de GPT-3.** AfriqueQwen3.5-4B-50Langs est un checkpoint base — vérifié sur sa fiche : *« Causal Language Model (Base/Pre-trained) »*, aucun instruction-tuning, aucun alignement, aucune mention de sécurité. Personne n'a franchi l'étape InstructGPT pour ces modèles.

> **Faire cette étape, et mesurer si elle part de meilleures fondations sur un backbone CPT africain que sur sa base d'origine.**

---

## 2. Ce qui rend la question ouverte

Trois sources indépendantes convergent, et aucune ne recouvre la question.

**La revue systématique** (arXiv:2608.14626) : le continued pre-training n'y figure pas comme méthode d'alignement, et ses perspectives appellent à valider le fine-tuning à paramètres efficients et le transfert cross-lingue « dans le contexte des langues africaines ». Sa discussion pose comme prémisse que les gains d'alignement plafonnent *parce que* le pré-entraînement sous-représente ces langues — une affirmation causale jamais testée.

**Le papier AfriqueLLM** (arXiv:2601.06395, ACL 2026) : produit les modèles, les évalue en capacité — maths, code, raisonnement, traduction longue — et **n'évalue jamais la sécurité, l'alignement, le refus ou la toxicité**.

**La licence Llama 3.1** : les langues hors des huit supportées sont déclarées *out-of-scope*, et la responsabilité de sécurité est explicitement transférée à qui adapte le modèle. AfriqueLlama-8B est un CPT de Llama 3.1 vers des langues africaines. L'obligation circule et n'est prise en charge par personne.

**Cadrage honnête.** La sécurité n'était pas l'objet d'AfriqueLLM ; leur travail est une étude de recette de CPT, correctement menée sur son propre terrain. Le problème est **systémique** : l'adaptation linguistique par CPT est devenue une pratique standard, et cette pratique produit des modèles publics dont personne ne caractérise la sécurité. Le papier ne doit pas attaquer une équipe.

---

## 3. Le dispositif

Quatre bras. **Une seule variable change entre les deux qui portent le claim : le backbone.**

| Bras | Modèle | Traitement | Rôle |
| :---- | :---- | :---- | :---- |
| **A0** | Qwen3.5-4B-Base | aucun | point de départ, base d'origine |
| **A1** | AfriqueQwen3.5-4B-50Langs | aucun | point de départ, après CPT |
| **A2** | Qwen3.5-4B-Base | SFT → DPO | contrôle aligné |
| **A3** | AfriqueQwen3.5-4B-50Langs | SFT → DPO | cible alignée |

**Le claim est A3 − A2**, à données, recette et graines identiques.
**A1 − A0** répond à une question secondaire mais réelle : le CPT change-t-il déjà quelque chose avant tout alignement ?

**Pourquoi SFT → DPO et non le pipeline InstructGPT complet.** InstructGPT enchaîne SFT, modèle de récompense et PPO. L'équivalent moderne et frugal est SFT puis DPO : une étape de moins, pas de modèle de récompense à entraîner, et une empreinte mémoire qui tient sur un T4. C'est aussi ce que notre infrastructure gère déjà.

**Pourquoi le SFT n'est pas optionnel ici.** Les deux backbones sont des modèles base. Ils ne suivent pas d'instructions. Le smoke test l'a montré : ils partent en raisonnement libre sans jamais produire le format demandé. Sans SFT, le DPO travaillerait sur un modèle incapable de répondre dans la forme attendue.

---

## 4. Le mur des données de v1 ne s'applique pas ici

Constat important, et c'est ce qui débloque le sujet.

H1 exigeait que les données possèdent une **propriété particulière** — être traduites nativement plutôt qu'automatiquement. Aucune source ne l'offrait, d'où l'impasse.

**Ce dispositif n'exige rien de tel.** Les deux bras reçoivent des données *identiques* ; seul le backbone diffère. Les défauts connus des données — traduction automatique (D4), étiquettes non validées humainement (D5), contenu occidental — **frappent A2 et A3 à l'identique et s'annulent dans la différence**.

Ce qui compte n'est pas que les données soient parfaites, mais qu'elles soient les mêmes. Les défauts limitent ce qu'on peut dire du *niveau absolu*, pas de l'*écart*.

---

## 5. Langue cible : le haoussa

Croisement des six jeux validés :

| Langue | UbuntuGuard | Uhura | AfriHate | TukaBench | AfriMGSM | LSR |
| :---- | ---: | :---: | :---: | :---: | :---: | :---: |
| Swahili | 207 paires | ✅ 813 | ✅ | ✅ | ✅ | — |
| **Haoussa** | 128 paires | ✅ 799 | ✅ | ✅ | ✅ | ✅ |
| Zulu | 152 | ✅ 761 | ✅ | — | ✅ | — |
| Yoruba | 68 | ✅ 815 | ✅ | ✅ | ✅ | ✅ |

**Haoussa retenu**, pour trois raisons qui ne sont pas des préférences :

1. Seule langue présente dans **les six** jeux, LSR compris — le benchmark de dégradation du refus.
2. La revue cite explicitement Inuwa-Dutse 2025 sur les **préjudices culturellement spécifiques en haoussa**, seul cas nommé pour une langue africaine (gap G4).
3. **Le haoussa est parlé dans le Nord-Cameroun.** Une validation par locuteur natif sur une trentaine d'exemples devient réaliste depuis l'ENSPY. C'est vrai d'aucune autre langue de la liste, et c'est la seule réponse crédible à la limite héritée de D5.

Le swahili est le second choix, à ajouter si le temps le permet — il testerait la généralisation à une deuxième langue.

---

## 6. Données d'entraînement

**Uhura-TruthfulQA `ha_generation`** — 799 lignes, traduction professionnelle humaine, licence MIT — alimente les **deux** étapes depuis une seule source :

- **SFT** : `question` → `best_answer`, une démonstration au sens InstructGPT
- **DPO** : `question`, chosen = `best_answer`, rejected = un `incorrect_answers`

**UbuntuGuard haoussa** — 128 paires de préférence, 278 exemples gardien — apporte l'axe sécurité, contenu ancré en contexte africain.

Découpage au niveau de la question, sans chevauchement, avec l'infrastructure déjà testée (`split_by_base_stem`).

---

## 7. Évaluation — et pourquoi elle échappe au problème du juge

C'est l'amélioration décisive par rapport à v1. **Trois axes sur quatre se mesurent sans aucun jugement de modèle.**

| Axe | Jeu | Mesure | Juge nécessaire ? |
| :---- | :---- | :---- | :---- |
| **Honest** | Uhura `ha_multiple_choice` | log-vraisemblance des 4 options, `mc1_targets` labels `[0,1,0,0]` | **non** |
| **Helpful** | AfriMGSM haoussa | correspondance de `answer_number` | **non** |
| **Harmless** | AfriHate haoussa | macro F1 de classification | **non** |
| **Harmless** | TukaBench `afri-jbb-harm` haoussa | taux de refus | oui, ou détection par motifs |
| **Sur-refus** | TukaBench `afri-jbb-benign` | refus sur requêtes légitimes | oui, ou motifs |

Vérifié sur données réelles : `ha_multiple_choice` renvoie bien 4 choix et des étiquettes binaires. Le scoring par log-vraisemblance est indépendant de la langue — on compare des nombres, pas des textes.

Seule la détection du refus sur TukaBench demande un jugement. C'est une surface bien plus petite qu'en v1, et le protocole de validation du juge déjà écrit s'y applique.

**Bonus de cadrage :** les trois H sont couverts à l'évaluation, alors que l'entraînement ne vise que Honest et Harmless. Cela permet de vérifier que l'alignement ne détruit pas l'utilité — l'oubli catastrophique que la littérature signale.

---

## 8. Ce qui est déjà construit et réutilisable

- Pipeline de données, 88 tests, sans GPU
- Découpage sans contamination, vérifié à zéro sur trois contrôles
- Métriques : macro F1, plancher de classe majoritaire, ventilation par groupe, McNemar apparié
- Deux backbones vérifiés sur Kaggle, contraintes mémoire mesurées
- Précision résolue automatiquement selon le GPU, `target_modules` LoRA nommés, longueur de séquence mesurée

**Une première mesure existe déjà** : Qwen3.5-4B-Base atteint 0,537 de macro F1 sur la tâche gardien, au-dessus du plancher à 0,333. Les modèles base ne partent pas de zéro — le récit ne doit pas reposer sur « ils vont s'effondrer », mais sur la mesure.

---

## 9. Risques identifiés

| Risque | Traitement |
| :---- | :---- |
| **« Aligner améliore » n'est pas un résultat** — établi depuis InstructGPT | C'est pourquoi A2 existe. Sans bras de comparaison, ce serait de l'ingénierie |
| Volume haoussa modeste : ~800 Uhura + 128 UbuntuGuard | ConsistentGuard publie sur 1 000 exemples. Comparable, à déclarer |
| Étiquettes UbuntuGuard non validées (D5) | Limitation héritée, déclarée. Sonde par locuteur natif haoussa envisagée |
| Oubli catastrophique après alignement | Mesuré explicitement via AfriMGSM |
| Coût compute : 4 bras × plusieurs graines | Une graine d'abord, graines supplémentaires si le temps le permet |
| Contenu occidental d'Uhura | S'annule entre les bras (section 4). Limite le propos sur le niveau absolu, pas sur l'écart |

---

## 10. Ce qui reste à trancher

1. **Vérifier que `masakhane/afrimgsm` expose bien une config haoussa** avec `answer_number` — la requête API a échoué, le nom de config est à confirmer.
2. **Vérifier si Gemma 3 et Qwen 3 portent la même clause de périmètre linguistique que Llama 3.1.** Si oui, l'argument de responsabilité transférée est systémique et non propre à Meta.
3. **Décider du volume SFT contre DPO** dans les ~800 lignes haoussa disponibles.
4. **Confirmer LSR** (arXiv:2603.19273) contre sa source avant de compter dessus.

---

## 11. Prochaine étape : filtre 3

Le filtre 1 (nouveauté) est passé. Le filtre 2 (données) est passé, à trois vérifications près listées ci-dessus.

Reste le **filtre 3 — exécutable** : un SFT puis un DPO sur un bras, en haoussa, sur T4, pour mesurer le temps réel et la mémoire. C'est ce qui dira si quatre bras tiennent dans le temps restant.
