# RESEARCH PROPOSAL

| RESEARCH PROPOSAL |  | PREPARED BY          Balbino Tchoutzine	 |
| :---- | :---- | ----: |
| 23/08/2026 |  | **Fabrique Ngousso** Yaoundé Cameroon |

# **Translated Safety Alignment vs. Native :** Direct Preference Optimisation on African Multi-Lingual Foundation Models

# 1\. Research Context 

Les grands modèles de langages (LLM) présentent une dégradation critique de leurs garde-fous de sécurité lorsqu'ils sont sollicités dans des langues à faibles ressources (*Yong et al., 2023 ; Abdullahi et al., 2026*). . La majorité des travaux actuels reposent sur des jeux de données de sécurité traduits automatiquement depuis l’anglais, qui manquent les risques culturellement ancrés et sous estiment les vulnérabilités aux attaques translangues.  
L'émergence récente de modèles de fondation bénéficiant d’un pré-entraînement continu (CPT) sur des corpus africains d’envergure, tel que AfriqueQwen3.5-4B-50Langs (35.5 milliards de tokens sur 50 langues), offre une base linguistique solide. Il constitue un cas d'étude idéal pour mesure l’impact direct d’un alignement DPO ciblé sans l’interférence d’un alignment anglophone antérieur (*Rafailov et al.,2023*)

# 2\. Related Work

La littérature scientifique récente sur l’alignement de sécurité des grands modèles de langage s’articule autour de trois axes fondamentaux pour ce projet :

1. Dégradation de la sécurité multilingue et failles des benchmarks traduits  
   Les travaux sur la sécurité multilingue démontrent que les garde-fous de sécurité des LLM s’effondrent lorsque les requêtes sont formulées dans des langues à faibles ressources (*Yong et al., 2023*). Une revue systématique récente de la littérature souligne que la majorité des évaluations reposent sur des jeux de données traduits automatiquement depuis l’anglais, un approche qui masque les risques culturellement ancrés et sous-estime les attaques par injection ou mélange de langues (code-switching). Pour pallier cette limite, des initiatives récentes ont introduit des benchmarks natif centrés sur des politiques de sécurité locales, à l’instar d’UbuntuGuard (*Abdullahi et al., 2026*), qui propose des scénarios de dialogue multi-tours élaborés par des experts africains.  
     
2. Pré-entraînement continu et modèles de fondation africains  
   Pour surmonter les biais de tokenisation et la mauvaise représentation géométrique des langues peu ressourcées dans l’espace latent des modèles, la communauté scientifique a développé des stratégies de pré–entraînement continu (CPT). La suite AfriqueLLM(*Yu et al., 2026*), et plus particulièrement le modèle AfriqueQwen3.5-4B-50Langs, représente l’état de l’art actuel en étendant le modèle de base Qwen3.5-4B sur plus de 35,5 milliards de tokens couvrant 50 langues africaines. Bien que ce modèle “Brut” n’ayant subi aucun alignement d'instruction ou de sécurité (*Yu et al.,2026*)

# 

# 3\. Research Question

Dans quelle mesure un alignement de sécurité par DPO (*Direct Preference Optimization*) basé sur des données natives en langues africaines améliore t-il le taux de refus des requêtes malveillantes sur le modèle AfriqueQwen3.5-4B-50Langs (*Yu et al.,2026*), par rapport à un alignement sur des données traduites, tout en maintenant la précision et l’unité du modèle sur des requêtes bénignes ?

# 4\. Hypotheses

**H1) Supériorité de l’alignement natif vs. traduit :**  
Un alignement DPO réalisé avec un jeu de données de sécurité natif (ex. *UbuntuGuard)* produit un taux de refus *(Refusal Rate)* des requêtes malveillantes en langues africaines significativement supérieur à celui obtenu par un alignement réalisé sur des données traduites automatiquement depuis l’anglais.

**H2) Rôle du backbone pré-entraîné CPT:**  
En raison de sa représentation vectorielle et linguistique enrichie sur 50 langues africaines, le modèle AfriqueQwen3.5-4B-50Langs (*Yu et al.,2026*) retient mieux les règles de sécurté après alignement DPO qu’un modèle de base standard non adapté (*Qwen3.5-4B-Base*).

**H3)  Préservation de lutilité et contrôle du sur-refus:**  
L’alignement DPO ciblé sur des données natives permet d’inverser la dégradation de sécurité sur les requêtes toxiques sans provoquer d’augmentation disproportionnée du taux de sur-refus (*Over-Refusal Rate*) sur des questions bénignes de santé et de culture locale.

5\. Expected Contribution  
**C1) Alignement de sécurité ciblé sur un backbone CPT africain (~~le premier~~):**  .  
Une ~~première~~ évaluation et implémentation empirique de l’alignement de sécurité par DPO sur le modèle de fondation AfrqueQwen3.5-4B-50Langs (*Yu et al.,2026),* testant l’hypothèse selon laquelle un pré-entrainement continu multilingue améliore la rétention des consignes de sécurité.  
**C2) Preuve expérimentale Natif vs. Traduit:**   
Une analyse comparative quantifiée démontrant les limites des données de sécurité traduites et l’efficacité des jeux de données d’alignement nativement ancrés dans le contexte socioculturel africain (*Abdullahi et al., 2026*)  
**C3) Pipeline d’alignement frugal et reproductible:**  
La mise à disposition d’un code open-source permettant d'évaluer et d’aligner des LLM multilingues sous contraintes de calcul légères (exécutable sur GPU NVIDIA T4 en moins de 2 heures via QLoRA+DPO).

6\. Selected Models  
L’étude s’appuiera sur deux modèles de 4 milliards de paramètres afin d’isoler l’impact du pré-entraînement continu (*Continued Pre-Training-CPT*) multilingue sur la rétention des consignes de sécurité:  
**M1) Modèle CPT Africain Cible :** *AfriqueQwen3.5-4B-50Langs  Juin26*  
Modèle de fondation développé par l’équipe McGill-NLP (Yu et al.,2026), étendu à partir de l’architecture Qwen3.5 via un pré-entrainement continu sur 35,5 milliards de tokens couvrant 50 langues africaines. Il servira à vérifier si un espace latent riche en langues locales améliore l’efficacité des garde-fous de sécurité.  
**M2) Modèle de Référence (Baseline architecture):** *Qwen3.5-4B-Base de Mars26*  
Modèle de base standard d’origine (non adapté aux langues africaines via CPT). Il sera utilisé pour mesurer l’écart de performance de sécurité entre un backbone généraliste anglophone/multilingue standard et un backbone spécifiquement adapté aux langues africaines( validation de **H2**).

7\. Datasets

Les jeux de données sont structurés selon leur rôle dans le pipeline expérimental (entraînement DPO vs. évaluation):  
 **D1) Données d’Alignement (Entrainment DPO)**

- Dataset DPO Natif

 Extrait directement du **split *training* d’UbuntuGuard** (Abdullahi et al., 2026 — licence CC BY 4.0), qui fournit déjà des paires de préférence complètes en langue locale, sans écriture manuelle requise (1 171 à 13 532 exemples selon la langue, sur 10 langues africaines dont Haoussa, Yoruba, Swahili). Chaque instance comprend:  
**Prompt**: Requête toxique ou sensible, dérivée des 8 091 requêtes anglaises originales et traduite par les auteurs du benchmark dans la langue cible.  
**Chosen (PASS)**: Réponse conforme à la politique de sécurité contextuelle (5-8 règles générées par GPT-5), générée par Llama-3.1-405B ou Qwen3-235B.  
**Rejected (FAIL)**: Réponse violant une ou plusieurs règles de la même politique, générée par les mêmes modèles.  
*Limite à noter (cf. section 13):* PASS/FAIL proviennent de modèles tiers et non d’AfriqueQwen-Brut lui-même — ces paires sont donc hors-politique (*off-policy*) pour le modèle cible, comme c’est le cas pour la plupart des jeux de préférence publics (ex. UltraFeedback).

- Dataset DPO Traduit 

Pour isoler la variable "qualité/nativité de la traduction" plutôt que le contenu, ce dataset réutilise le **même contenu source anglais d’UbuntuGuard** (mêmes paires PASS/FAIL) mais traduit automatiquement (NLLB/Google Translate) vers les langues cibles, au lieu des traductions par les auteurs du benchmark. H1 compare ainsi deux versions du même contenu de sécurité — traduction native/experte vs. traduction automatique — à volume et contenu égaux.

**D2) Datasets d'Évaluation de la Sécurité & Refus**

- **UbutuGuard** (Abdullahi et al.,): Benchmark natif de politiques de sécurité couvrant 10 langues africaines sur des scénarios multi-tours sensibles (santé, finance, éducation, gouvernement). Utilisé pour mesurer le taux de refus (Refusal Rate).  
- **AfriHate:** Corpus annoté par des locuteur natifs couvrant 15 langues africaines pour tester la détection du discours de haine et du langage abusif.

**D3) Datasets d’Evaluation du Sur-Refus & l’Utilité (Over-Refusal & Utility)**

- HealthBench-Africa Extension: Scénarios et requets de conseils de santé bénins formulés en langues locales.  
- Uhura-TruthfulQA /  Subsets IrokoBench: Questions de culture, d’histoire et de savoirs locaux. Ils permettent de mesurer le taux de sur-refus(Over-Refusal Rate) et de vérifier que l’alignement DPO ne bloque pas abusivement les requêtes légitimes(validation de  **H3**)

8\.  Baselines  
L’expérimentation comparera quatre configurations de modèles pour isoler précisément les facteurs d’efficacité de l’alignement:  
**B1) AfriqueQwen-Brut**  
Le modèle AfriqueQwen3.5-4B-50Langs non aligné, il établit le niveau de refus spontané et de sécurité du backbone CPT.  
**B2) AfriqueQwen \+ Traduit-DPO**  
Le modèle AfriqueQwen3.5-4B-50Langs  aligné par DPO avec le jeu de données de sécurité traduit automatiquement depuis l’anglais (Traduit-DPO)  
**B3)** **Qwen-Base \+ Natif-DPO**  
Le modèle de base généraliste standard Qwen3.5-4B-Base aligné avec le jeu de données natif (Natif-DPO), permet de valider l’impact de la représentation linguistique du backbone (**H2).**  
**B4) AfriqueQwen \+ Natif-DPO**  
Le modèle cible combinant le pré-entraînement continu africain et alignement DPO sur données natives.

9\. Evaluation Metrics & Procedure  
L’évaluation s’appuie sur trois métriques quantitatives principales:

- Taux de Refus (RR%)  
  Proportion de requêtes malveillantes ou toxiques (issues d’UbuntuGuard) pour lesquelles le modèle génère un refus explicite et conforme à la politique de sécurité.  
    
- Taux de Sur-Refus (Over-RR %)  
  Proportion de requêtes légitimes et bénignes (santé, culture) bloquées à tort par le modèle (mesure de la préservation de l’utilité, **H3**)  
- F1-Score/ Précision de Modération:  
  Score F1 macro évalué sur le corpus AfriHate pour mesurer la capacité du modèle à classifier le discours de haine et les contenus abusifs.


Procédure d’évaluation: Les réponses générées sont classées de manière automatisée à l’aide de motifs d’inhibition linguistique et d’un classifieur de modération léger, avec une validation croisée manuelle sur un échantillon de 10% des réponses.

 10\. Experimental Protocol  
 **E1) Evaluation Infill**  
Inférence du modèle Brut AfriqueQwen3.5-4B-50Langs sur les jeux de données d’évaluation (UbuntuGuard, AfriHate, HealthBanch-Africa) pour extraire les métriques de départ.

**E2) Structuration des Datasets DPO**  
Formatage des paires PASS/FAIL du split *training* d’UbuntuGuard en ChatML pour Natif-DPO (aucune génération requise) ; traduction automatique (NLLB) des mêmes paires depuis l’anglais vers les langues cibles pour Traduit-DPO.

**E3) Entraînement DPO via QLoRA**  
Ajustement du modèle avec l’algorithme DPO (Rafailov et al.,2023) sous QLoRA 4-bbit (rank=16, Alpha=32, Lerning Rate=5\*10^-6) sur kaggle (2\* GPU T4).

**E4) Inférence comparative & Post-Évaluation**  
Ré-évaluation des modèles alignés sur les mêmes prompts pour mesurer le delta de la performance ( **delta RR et delta ORR).**

11\. Planned Ablation Studies

**A1) Volume de données d’alignement**  
Evaluation des performances du modèle aligné avec 250,500 eet 1000 exemples DPO afin de déterminer le seuil minimal de données de préférence nécessaire.

**A2) Impact de la diversité linguistique**  
Comparaison entre un alignement DPO monolingue (ex. Houssa uniquement) et un alignement DPO multilingue équilibré (Haoussa, Yoruba, Swahili, Pidgin) pour observer le transfert de sécurité interlingue.

12\. Estimates Computing Requirements (\<12h)

- **Inférence de Baselin (Colab T4)**

L’inférence sur 1000 prompts prend \~15 minutes avec l’optimisation vLLM/Hugging Face pipeline en 4-bit.

- **Entrainement DPO (Kaggle 2\* Tesla T4)**  
  Un entraînement DPO QLoRA sur 1000 paires de préférences (3 époques ) consomme environ 45 à 60 minutes et nécessite \< 6Go de vRAM par GPU.  
- **Validation du critère de faisabilité**  
  Une expérience initiale complète (Inférence \+ Entraînement \+ Ré-Inférence) s’exécute en moins de 2 heures, garantissant le respect de la contrainte budgétaire (\< 12 heures par expérience et \> 30 heures/semaines).


13\. Main Risks and Limitations

- **Risque d’Oubli Catastrophique**

  L’alignement DPO peut réduire la fluidité linguistique générale du modèle. Atténuation: Intégration de paires de conversion générales dans le jeu de données d’alignement.Risque d’Oubli Catastrophique

- **Portée Linguistique Restreinte**

  L’évaluation expérimentale se concentrera sur 4 à 5 langues majeures (Haoussa, Yoruba, Swahili, Pidgin Nigérian) parmi les 50 couvertes par le modèle.7

- **Absence d’Annotateurs Humains en Temps Réel**

  La validation s’appuie sur des benchmarks pré-annotés par des experts et des métriques automatisées.

- **Paires DPO Hors-Politique (*Off-Policy*)**

  Les réponses PASS/FAIL d’UbuntuGuard sont générées par des modèles tiers (Llama-3.1-405B, Qwen3-235B), pas par AfriqueQwen-Brut lui-même — limite standard des jeux de préférence publics (ex. UltraFeedback), mais qui peut réduire l’efficacité du signal DPO par rapport à des paires générées sur-politique.


14\. Schedule for Weeks 5 to 8

| Semaine  | Objectifs Principaux & Livrables Techniques |
| :---- | :---- |
| S1 | Validation du script d’inférence, extraction de la Baseline 1 et préparation des datasets DPO. |
| S2 | Entrainements DPO sur kaggle (Modèle Natif vs Modèle Traduit) et obtention des Baselines 2 et 3\. |
| S3 | Exécution des études d’ablation (volume de données, mix linguistique) et évaluation du sur-refus (ORR) |
| S4 | Synthèse des résultats, génération des graphiques comparatifs et rédaction du rapport final. |

   
 15\. Expected Figures and Tables  
**F1) Architecture du Pipeline**   
Diagramme illustrant le flux allant du modèle CPT AfriqueQwen jusqu’à l’alignement DPO (Natif vs Traduit) et l’évaluation double (Sécurité vs Sur-Refus).   
**F2) Graphique d’Efficacité du refus**  
Graphique en barres comparant le Taux de Refus (RR) par langue entre le modèle brut, l’alignement traduit et le l’alignement natif.  
**T1) Tableau Principal des Résultats**  
Synthèse comparative des métriques (RR, ORR, F1-AfriHate) sur l’ensemble des baselines.  
**T2) Résultats des Ablations**  
Évolution des scores selon la taille du dataset DPO (250, 500, 1000 exemples) et le degré de diversité linguistique.

# All\_Refs

Bibliographie complète et la liste des ressources open-source (modèles et jeux de données) pour le *Balbino* *Research Proposal*.

### **1\. Publications Scientifiques Fondatrices (Articles de Référence)**

* **AfriqueLLM & AfriqueQwen3.5 (Modèle CPT Africain) :**

* **Référence :** Yu, H., Xu, T., Hedderich, M. A., Hamidouche, W., Zamir, S. W., & Adelani, D. I. (2026). *AfriqueLLM: How Data Mixing and Model Architecture Impact Continued Pre-training for African Languages*. arXiv preprint arXiv:2601.06395.

* **Lien :** [https://arxiv.org/abs/2601.06395](https://arxiv.org/abs/2601.06395)

  \[cite: 1\]

* **UbuntuGuard (Benchmark Natif de Politiques de Sécurité) :**

* **Référence :** Abdullahi, T., Mgonzo, M., Owodunni, A. T., Singh, R., & Eickhoff, C. (2026). *UbuntuGuard: A Culturally-Grounded Policy Benchmark for Equitable AI Safety in African Languages*. OpenReview / arXiv preprint arXiv:2601.12696.

* **Lien :** [https://openreview.net/pdf?id=uPSzx3SBdf](https://openreview.net/pdf?id=uPSzx3SBdf)

  \[cite: 2\]

* **AfriHate (Corpus de Discours de Haine en 15 Langues Africaines) :**

  - **Référence :** Muhammad, S. H., et al. (2025). *AfriHate: A Multilingual Collection of Hate Speech and Abusive Language Datasets for African Languages*. arXiv preprint arXiv:2501.08284.

  - **Lien :** [https://arxiv.org/abs/2501.08284](https://arxiv.org/abs/2501.08284)

    \[cite: 3\]

* **Faille de Sécurité Multilingue (*Jailbreak* par Langues à Faibles Ressources) :**

  - **Référence :** Yong, J. U., Menghini, C., & Bach, S. H. (2023). *Low-Resource Languages Jailbreak GPT-4*. arXiv preprint arXiv:2310.02446.

  - **Lien :** [https://arxiv.org/abs/2310.02446](https://arxiv.org/abs/2310.02446)

* **Direct Preference Optimization (DPO) :**

  - **Référence :** Rafailov, R., Sharma, A., Mitchell, E., Ermon, S., Manning, C. D., & Finn, C. (2023). *Direct Preference Optimization: Your Language Model is Secretly a Reward Model*. Advances in Neural Information Processing Systems (NeurIPS 2023).

  - **Lien :** [https://arxiv.org/abs/2305.18290](https://arxiv.org/abs/2305.18290)

* **QLoRA (Quantisation 4-bit et Adaptateurs LoRA) :**

  - **Référence :** Dettmers, T., Pagnoni, A., Holtzman, A., & Zettlemoyer, L. (2023). *QLoRA: Efficient Finetuning of Quantized LLMs*. Advances in Neural Information Processing Systems (NeurIPS 2023).

  - **Lien :** [https://arxiv.org/abs/2305.14314](https://arxiv.org/abs/2305.14314)

* **AfriStereo (Évaluation des Biais et Stéréotypes) :**

  - **Référence :** YUX Cultural AI Lab (2025). *AfriStereo: Benchmarking Socio-Cultural Stereotypes in African Contexts*. arXiv preprint arXiv:2511.22016.

  - **Lien :** [https://arxiv.org/abs/2511.22016](https://arxiv.org/abs/2511.22016)

    \[cite: \]

### **2\. Modèles Étudiés (Hugging Face)**

| Nom du Modèle | Role Expérimental | Lien Direct Hugging Face |
| :---- | :---- | :---- |
| **AfriqueQwen3.5-4B-50Langs** | Modèle CPT cible (McGill-NLP)  | [HuggingFace / McGill-NLP](https://huggingface.co/McGill-NLP)  \[cite: 1\]  |
| **Qwen3.5-4B-Base** | Modèle de contrôle (Qwen Team) | [HuggingFace / Qwen/Qwen3.5-4B-Base](https://huggingface.co/Qwen) |

### **3\. Datasets et Benchmarks D'Évaluation (Hugging Face & Repositories)**

| Nom du Dataset | Usage dans le Proposal | Lien / Dépôt Source |
| :---- | :---- | :---- |
| **UbuntuGuard** | Dataset de politiques de sécurité & refus  | [OpenReview Paper & Dataset](https://openreview.net/pdf?id=uPSzx3SBdf)  \[cite: 2\]  |
| **AfriHate** | Détection du discours de haine (15 langues)  | [HuggingFace: afrihate/afrihate](https://huggingface.co/datasets/afrihate/afrihate)  \[cite: 3\]  |
| **AfriStereo** | Paires stéréotype/anti-stéréotype  | [GitHub: Afri-Stereo Repository](https://github.com/YUX-Cultural-AI-Lab/Afri-Stereo)  \[cite: \]  |
| **CyberNaija** | Cyberharcèlement en Pidgin et Code-Switching  | [HuggingFace: cike-dev/CyberNaija](https://huggingface.co/datasets/cike-dev/CyberNaija)  \[cite: \]  |
| **IrokoBench** | Multi-tâches et compréhension de sécurité  | [HuggingFace Collection: masakhane/irokobench](https://huggingface.co/collections/masakhane/irokobench)  \[cite: \]  |
| **Uhura-TruthfulQA** | Factualité et ancrage culturel  | [HuggingFace: masakhane/uhura-truthfulqa](https://huggingface.co/datasets/masakhane/uhura-truthfulqa)  \[cite: \]  |
| **HealthBench-Africa** | Évaluation du sur-refus et conseils médicaux  | [HuggingFace: tonative/healthbench-africa-extension](https://huggingface.co/datasets/tonative/healthbench-africa-extension)  \[cite: \] |

