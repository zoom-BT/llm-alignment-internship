# Sujet v2 — Étape 1 : les gaps déclarés par la revue

**Source unique :** Lemofouet, V. D., Uzor, B. N., Anyanwu, P. C., Kapsa, D. B., Imam, S. H., Sahil, P. S., Oppong, A., Abdullahi, T., Siro, C., Abdulmumin, I., Yimam, S. M., & Muhammad, S. H. (2026). *LLM Safety Alignment in Low-Resource Languages: A Systematic Literature Review.* arXiv:2608.14626v1. Workshop LM4UC, IJCAI 2026. PRISMA 2020, ~1 500 papiers filtrés à 50.

**Méthode de cette étape.** Relecture directe des sections 7 (RQ4), 8 (Discussion) et 9 (Conclusion). Chaque gap est cité **verbatim** puis reformulé. **Aucun filtrage par faisabilité à ce stade** — c'est délibéré : filtrer trop tôt, c'est ce qui avait produit un sujet qu'il a fallu corriger neuf fois. Le croisement avec nos données disponibles est l'étape 2.

Traduction des citations en note ; l'original anglais fait foi.

---

## G1 — Le PEFT, la synthèse de données et le transfert cross-lingue ne sont pas validés sur les langues africaines

> « Methodologically speaking (RQ1 and RQ4), techniques like parameter-efficient fine-tuning, data synthesis, and cross-lingual transfer might be helpful, yet they are **poorly validated in the context of the African languages**. »

**Ce que ça dit.** Trois familles de méthodes sont couramment employées, et personne n'a établi qu'elles fonctionnent sur les langues africaines. Ce n'est pas « on ne sait pas si ça marche bien » — c'est « la validation n'a pas été faite ».

**Ce qui comblerait ce gap.** Une évaluation propre d'au moins une de ces trois familles sur des langues africaines, avec baseline et test statistique.

---

## G2 — La couverture au pré-entraînement est posée comme cause, jamais testée

> « As long as the pre-trained models lack coverage of these languages, the gains brought by such techniques are rather marginal. Partly because, at the pre-training stage, these models already under-represent the languages, which makes recovery of any kind of multilingual representation impossible. »

**Ce que ça dit.** C'est une **affirmation causale** : les techniques d'alignement plafonnent *parce que* le pré-entraînement sous-représente ces langues. Le mot « impossible » est fort et n'est appuyé par aucune expérience contrôlée dans la revue.

**Ce qui comblerait ce gap.** Comparer deux modèles identiques à la couverture de pré-entraînement près, et mesurer si l'écart d'alignement suit. C'était le sujet v1 — il reste valide sur le fond, c'est son cadrage et sa métrique qui avaient dérivé.

---

## G3 — Les risques sont rapportés mais presque jamais évalués

> « Issues such as cross-lingual jailbreak transfer, code-switching based vulnerabilities, and unintended safety degradation through benign fine-tuning into new languages have been reported, **but seldom evaluated**. »

**Ce que ça dit.** Trois risques concrets circulent comme des observations ponctuelles, sans mesure systématique. Le troisième est le plus frappant : **un fine-tuning bénin dégraderait la sécurité**, ce qui concerne toute équipe adaptant un modèle à une nouvelle langue.

**Ce qui comblerait ce gap.** Une mesure systématique de l'un des trois, avec un protocole reproductible plutôt qu'une anecdote.

---

## G4 — Les risques culturellement spécifiques sont absents des benchmarks

> « Furthermore, culturally specific risks, such as those reported in Hausa (Inuwa-Dutse, 2025), are **almost completely neglected in benchmarks designed with English-centric assumptions**. »

**Ce que ça dit.** Les benchmarks importent les catégories de préjudice anglophones. Les préjudices propres à un contexte africain n'y ont pas de case.

**Ce qui comblerait ce gap.** Un travail de construction ou d'audit de catégories de préjudice ancrées localement. Coûteux en expertise humaine.

---

## G5 — Le problème n'est pas seulement dans les modèles, il est dans les annotations

> « According to Vajjala (2025), however, such limitations do not apply exclusively to models; **annotation discrepancies and culturally biased benchmarks contribute to the inadequacy of evaluation measures**. »

**Ce que ça dit.** Les mesures d'évaluation sont elles-mêmes défaillantes — désaccords d'annotation, biais culturel des benchmarks. On évalue mal, donc on ne peut pas savoir où l'on en est.

**Ce qui comblerait ce gap.** Un audit de la qualité d'annotation d'un benchmark existant. Nous en avons déjà fait un embryon avec D5 sur UbuntuGuard.

---

## G6 — La traduction reste la méthode dominante, et elle abîme le sens

> « Translation is still the primary strategy used in the creation of datasets, although this methodology has **repeatedly demonstrated its ability to manipulate meanings and mislead safety annotations**. »

**Ce que ça dit.** Le domaine continue de construire ses jeux de données par traduction, tout en sachant que la traduction déforme le sens et fausse les annotations de sécurité.

**Note importante pour nous.** C'est le gap dont relevait H1 du sujet v1. La revue le déclare *connu*, pas ouvert — d'où l'abandon de H1. À ne pas reprendre tel quel.

---

## G7 — Le cycle qui se renforce lui-même

> « Combined, these limitations create a **reinforcing cycle** whereby inadequate pre-training coverage translates into poor representation, which then limits the capabilities of the alignment methods, whereas poor benchmarks limit the ability to assess the deficiencies. »

**Ce que ça dit.** Trois défaillances s'alimentent : pré-entraînement insuffisant → représentations pauvres → alignement limité → et des benchmarks trop faibles pour mesurer quoi que ce soit. La revue appelle à progresser « sur tous les fronts simultanément ».

**Lecture.** C'est une thèse structurelle, pas une expérience. Elle indique surtout que **casser un seul maillon** est déjà une contribution — et que le maillon « benchmarks trop faibles pour mesurer » est le moins coûteux à attaquer.

---

## G8 — Les quatre perspectives explicites de la conclusion

> « Future research should focus on **native-language safety benchmarks**, **balanced multilingual pre-training**, **culturally aware evaluation methods**, and **participatory frameworks that actively involve African language communities** in defining AI safety standards and practices. »

Quatre directions nommées. Par ordre de coût croissant en ressources humaines :

| | Direction | Ce qu'elle exige |
| :---- | :---- | :---- |
| G8a | méthodes d'évaluation culturellement conscientes | conception + validation, expertise modérée |
| G8b | benchmarks de sécurité en langue native | locuteurs natifs, construction de données |
| G8c | pré-entraînement multilingue équilibré | compute hors de portée d'un stage |
| G8d | cadres participatifs avec les communautés | temps long, réseau, gouvernance |

---

## Mécanismes nommés dans la section 7 — des pistes, pas des gaps

La revue décrit des travaux qui *proposent* des mécanismes. Ce ne sont pas des trous à combler, mais des outils réutilisables ou des hypothèses à tester.

| Travail | Ce qu'il établit ou propose |
| :---- | :---- |
| Shen 2024 | l'alignement n'améliore la sécurité que dans les langues bien représentées |
| Verma & Bharadwaj 2025 | les traits de sécurité se regroupent dans les régions à haute ressource de l'espace latent |
| Upadhayay & Behzadan 2025 | introduire une langue nouvelle en fine-tuning perturbe la sécurité déjà apprise |
| — tokenisation | « morphologically rich languages and underrepresented scripts often suffer from **fragmented tokenization** and weaker semantic representations, reducing the reliability of safety reasoning and refusal behavior » |
| Liang 2026 (SWE) | édition parcimonieuse de poids, transformation linéaire en forme close, **sans gradient** |
| Shin & Hwang 2026 | identifier et remplacer les couches critiques pour la sécurité, **sans réentraînement** |
| Zhang 2026b | le comportement de sécurité cross-lingue dépendrait de **neurones de sécurité partagés**, ciblables |
| Wang 2026 | « a **shared directional structure** in refusal behavior across safety-aligned languages » — représentations latentes de sécurité partiellement universelles |
| Bansal & Mishra 2026 | un alignement appris sur un sous-ensemble bien choisi de langues généralise largement |
| Bu 2026 | objectif de cohérence multilingue imposant l'accord d'alignement entre langues |

**Ce que ce tableau suggère.** Une part importante des travaux récents ne passe **pas** par l'entraînement : édition de poids, transplantation de couches, ciblage de neurones, direction de refus. Ce sont des approches à faible coût compute — potentiellement décisif pour un stage sans GPU dédié.

---

## Trois benchmarks africains recensés par la revue

| Benchmark | Ce qu'il mesure |
| :---- | :---- |
| **LSR** (Faruna 2026, arXiv:2603.19273) | dégradation du refus cross-lingue — yoruba, haoussa, igbo, **igala** |
| **UbuntuGuard** (Abdullahi et al. 2026) | « the first African policy-based safety benchmark » |
| **Uhura** (Bayes et al. 2024) | véracité et contraintes de sécurité |

La revue elle-même conclut : « **African languages remain substantially under-represented compared with other multilingual benchmark ecosystems.** »

---

## Synthèse — les huit gaps

| Réf. | Gap | Statut |
| :---- | :---- | :---- |
| **G1** | PEFT / synthèse / transfert non validés sur langues africaines | ouvert |
| **G2** | La couverture au pré-entraînement posée comme cause, jamais testée | ouvert |
| **G3** | Jailbreak cross-lingue, code-switching, dégradation par fine-tuning bénin : rapportés, non évalués | ouvert |
| **G4** | Préjudices culturellement spécifiques absents des benchmarks | ouvert, coûteux |
| **G5** | Annotations et benchmarks eux-mêmes défaillants | ouvert |
| **G6** | La traduction abîme le sens | **connu, pas ouvert** — c'était H1 |
| **G7** | Cycle auto-renforçant des trois défaillances | thèse structurelle |
| **G8** | Benchmarks natifs, pré-entraînement équilibré, évaluation culturelle, cadres participatifs | ouvert, coûts très variables |

---

## Étape suivante

Croiser cette liste avec :

1. **ce que nos six jeux de données validés permettent réellement** — volumes, langues, licences, ce qui est déjà vérifié ;
2. **ce que notre infrastructure permet** — T4 Kaggle, deux backbones fonctionnels, pipeline testé ;
3. **la contrainte de temps** — trois semaines, dont une pour la rédaction.

L'intersection donnera les sujets candidats. Contrainte non négociable : **le sujet doit porter sur l'alignement**, pas sur la traduction ni sur la classification pure.
