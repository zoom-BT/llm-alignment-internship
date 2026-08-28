# Pipeline — schéma complet

État au 2026-08-28. Reflète les déviations D1 à D9 : claim recentré sur H2, métrique gardien
plutôt que RR%, axe Honest à l'entraînement, découpage au niveau `base_stem`.

```mermaid
flowchart TB

%% ─────────────────────────── 1. SOURCES ───────────────────────────
subgraph SRC["1 · Sources de données"]
  direction LR
  UG["<b>UbuntuGuard</b><br/>3 fichiers JSONL · CC BY 4.0<br/>versionnés dans le dépôt"]
  UH["<b>Uhura-TruthfulQA</b><br/>6 langues + en · MIT<br/>traduction humaine"]
  AH["<b>AfriHate</b><br/>15 langues · Apache-2.0"]
  TK["<b>TukaBench</b><br/>8 langues · CC-BY-NC"]
end

UG --> CL["<b>crosslingual</b><br/>2 307 lignes · 851 row_id<br/>politique EN"]
UG --> TR["<b>translated</b><br/>mêmes dialogues<br/>politique locale"]
UG --> EN["<b>english_only</b><br/>2 449 lignes · 903 row_id"]

CL -. "diffèrent<br/>UNIQUEMENT<br/>par policy" .- TR

%% ─────────────────────────── 2. CONSTRUCTION ───────────────────────────
subgraph BUILD["2 · Construction — src/data.py"]
  direction TB
  PARSE["<b>parse_transcript</b><br/>marqueurs User: / Agent:<br/>metadata = repr Python, pas JSON"]
  GP["<b>build_guardian_pairs</b><br/>juger politique+transcript<br/>chosen = vrai verdict<br/><b>2 307 exemples</b>"]
  PP["<b>build_preference_pairs</b><br/>coupe au 1er tour divergent<br/>839/843 = 1re réponse agent<br/><b>1 089 paires</b>"]
  UP["<b>build_uhura_pairs</b><br/>best_answer vs incorrect<br/>aucune génération requise"]
end

CL --> PARSE --> GP
PARSE --> PP
UH --> UP

%% ─────────────────────────── 3. AXE + SPLIT ───────────────────────────
subgraph SPLIT["3 · Axe HHH et découpage"]
  direction TB
  AXIS["<b>filter_by_axis</b><br/>Honest = désinfo + conseil expert · 45%<br/>Harmless = stéréotypes + haine · 25%<br/>public interest exclu des deux"]
  S3["<b>split_three_way</b><br/>groupé sur <b>base_stem</b>"]
  GUARD["🛡️ <b>Anti-contamination</b><br/>265/566 questions existent<br/>en plusieurs langues<br/>un split par row_id fuitait 54%"]
end

GP --> AXIS --> S3
PP --> AXIS
S3 -.- GUARD

S3 --> DJ["<b>juge</b><br/>461 ex."]
S3 --> DA["<b>agent</b><br/>1 373 ex."]
S3 --> DE["<b>éval</b><br/>473 · 267 sur axe Honest"]

%% ─────────────────────────── 4. ENTRAÎNEMENT ───────────────────────────
subgraph TRAIN["4 · Entraînement — QLoRA + DPO"]
  direction TB
  JUDGE["<b>JUGE</b> = Qwen3.5-4B-Base<br/>⚠️ backbone de CONTRÔLE, pas la cible<br/>tout biais d'affinité joue<br/>CONTRE notre hypothèse"]
  B3["<b>B3</b> Qwen-Base + DPO"]
  B4["<b>B4</b> AfriqueQwen + DPO"]
end

DJ --> JUDGE
DA --> B3
DA --> B4
UP -.-> B3
UP -.-> B4

M1["McGill-NLP/<br/>AfriqueQwen3.5-4B-50Langs"] --> B4
M2["Qwen/Qwen3.5-4B-Base"] --> B3
M2 --> JUDGE

M1 -. "même tokenizer<br/>248 044 tokens<br/>→ tokenisation contrôlée" .- M2

%% ─────────────────────────── 5. ÉVALUATION ───────────────────────────
subgraph EVAL["5 · Évaluation — run_guardian_eval.py"]
  direction TB
  B1["<b>B1</b> AfriqueQwen brut<br/>aucun entraînement"]
  GEN["génération gloutonne<br/>512 tokens — les modèles<br/>raisonnent avant de conclure"]
  EX["<b>extract_verdict</b><br/>dernier verdict, pas le premier<br/>2 modes : strict / loose<br/>l'écart = artefact de parseur"]
end

DE --> GEN
B1 --> GEN
B3 --> GEN
B4 --> GEN
JUDGE --> GEN
GEN --> EX

ENCTRL["<b>contrôle anglais</b><br/>337 questions → 555 ex. Honest<br/>absentes de TOUT fichier africain<br/>✅ lisibles à la main"] --> GEN
EN --> ENCTRL

%% ─────────────────────────── 6. ANALYSE ───────────────────────────
subgraph ANA["6 · Analyse — src/metrics.py"]
  direction TB
  MF1["<b>macro F1</b><br/>+ plancher classe majoritaire 0,333"]
  PERL["par langue et par thème<br/>&lt;20 ex. → 'ne pas citer'"]
  MCN["<b>McNemar</b> apparié<br/>tous les bras voient<br/>les MÊMES prompts"]
  GAPL["écart anglais ↔ africain<br/>= dégradation cross-lingue<br/><i>c'est un résultat, pas un défaut</i>"]
end

EX --> MF1 --> MCN
MF1 --> PERL
MF1 --> GAPL

%% ─────────────────────────── 7. HYPOTHÈSES ───────────────────────────
MCN --> H2["<b>H2</b> · claim principal<br/>B4 − B3<br/>le CPT africain améliore-t-il<br/>la rétention de l'alignement ?"]
PERL --> H2B["<b>H2 stratifié</b><br/>Honest vs Harmless<br/>prédiction : le CPT aide plus<br/>sur le savoir que sur le comportement"]
AH --> H3["<b>H3</b> · utilité<br/>F1 modération"]
TK --> H3

classDef src fill:#1e3a5f,stroke:#4a90d9,color:#fff
classDef proc fill:#2d4a3e,stroke:#5cb85c,color:#fff
classDef model fill:#4a3728,stroke:#d9a441,color:#fff
classDef warn fill:#5a2d2d,stroke:#d9534f,color:#fff
classDef res fill:#3d2d5a,stroke:#9b59b6,color:#fff

class UG,UH,AH,TK,CL,TR,EN src
class PARSE,GP,PP,UP,AXIS,S3,GEN,EX proc
class M1,M2,JUDGE,B1,B3,B4 model
class GUARD,ENCTRL warn
class MF1,PERL,MCN,GAPL,H2,H2B,H3 res
```

## Les quatre garde-fous du schéma

| Garde-fou | Ce qu'il empêche |
| :---- | :---- |
| Découpage sur `base_stem` | qu'une question vue en swahili à l'entraînement soit évaluée en haoussa — 54% de fuite avec un découpage par `row_id` |
| Juge sur le backbone de **contrôle** | qu'un juge partageant son backbone avec l'agent qu'il note gonfle l'effet mesuré |
| Contrôle anglais hors de tout fichier africain | qu'on ne puisse pas vérifier le juge à la main, faute de lire les langues cibles |
| Double extracteur strict/loose | qu'un score de parseur soit pris pour un score de modèle |

## Ce qui a été retiré du schéma, et pourquoi

- **Bras Translated-DPO / NLLB** — H1 rétrogradée, sa question est déjà répondue dans la littérature (D6).
- **RR% et Over-RR%** — UbuntuGuard n'est pas un benchmark de génération, ses réponses PASS ne sont pas des refus (D8).
- **`translated`** reste en source mais n'alimente aucun entraînement : il ne diffère de `crosslingual` que par la langue de la politique, donc les volumes ne s'additionnent pas (D2).
