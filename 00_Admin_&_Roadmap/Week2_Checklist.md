# 🎯 Week 2: Supervised Fine-Tuning and Instruction Tuning

## 📥 Deliverables Checklist (Due: Friday)
- [ ] Reading note on instruction tuning (InstructGPT — `06_Reading_Notes/`)
- [ ] Dataset / dataset-preparation script (reused: databricks-dolly-15k via `src/data.py` — no change needed, protocol requires it stays identical to Week 1)
- [ ] Supervised fine-tuning scripts (`src/train.py`, corrected: learning rate, LR schedule, early stopping, loss masking)
- [ ] Table of hyperparameters (Week 1 recipe vs. Week 2 corrected recipe, side by side)
- [ ] Training and validation curves (TensorBoard — this time with real `eval_loss` tracked during training, not just after)
- [ ] Comparison of the model before and after fine-tuning (baseline = 13.92; success = below 13.92, not "beat 75.41")
- [ ] Error analysis (qualitative review of ≥20 generated examples: failures, regressions, unexpected behaviors)

---

## 📚 Technical Concepts Matrix (Week 2)
- [ ] Pretraining vs. supervised fine-tuning
- [ ] Task-specific fine-tuning vs. instruction tuning
- [ ] The causal language-modeling loss
- [ ] Prompt-response datasets
- [ ] Multi-turn conversational datasets
- [ ] System, user, and assistant roles
- [ ] Masking the loss on prompt tokens
- [ ] Padding and truncation
- [ ] Sequence packing
- [ ] Maximum context length
- [ ] Data quality and diversity
- [ ] Data deduplication
- [ ] Training and evaluation contamination
- [ ] Overfitting
- [ ] Training and validation curves
- [ ] Perplexity and its limitations
- [ ] Automatic evaluation
- [ ] Human evaluation
- [ ] Memorizing examples vs. learning a response style vs. acquiring a new capability

---

## 🔧 Corrections carried over from Week 1 (priority order, per the intern's own analysis)
1. **Learning rate: `2e-4` → `2e-5`** — an order of magnitude; the leading suspect (Alpaca trains 3 epochs at 2e-5 without diverging, so LR is the primary culprit, not epoch count)
2. **Wire up the validation split** (`eval_strategy="steps"`, `eval_steps=100`, `load_best_model_at_end=True`, `metric_for_best_model="eval_loss"`, `EarlyStoppingCallback(patience=3)`) — methodologically the most important: turns a blind run into a monitorable one
3. **Full LR schedule** (`warmup_ratio=0.03`, `lr_scheduler_type="cosine"`) — protects the first steps from a too-aggressive start
4. **Let early stopping decide the stopping point**, rather than fixing epochs in advance (raise the epoch ceiling, trust the callback)

## 🔒 Protocol — do not touch
Same dataset, same split (seed=42), same `evaluate.py` code path as Week 1. Only the training recipe changes. Baseline reference stays **13.92**.

## 🔍 Investigation avenues (if time permits, in this order)
1. LR ablation (2e-5 / 5e-5 / 1e-4) on a 1,000-example subsample (~15 min each) — resolve the LR hypothesis empirically before spending another ~6h run
2. Loss masking on the response only (`labels=-100` on prompt tokens) — closer to the real task; currently the whole sequence (prompt included) is trained and evaluated on
3. Stratified split by Dolly's task categories — weak effect at 1,500 examples, but methodologically cleaner
4. Bootstrap confidence interval on perplexity (e.g. "13.92 ± 0.4") — matters more if Week 2's result ends up close to the baseline
5. A metric beyond perplexity (perplexity doesn't measure response usefulness) — open question for the Supervisor meeting

## 👉 Bridge to Week 3 (LoRA)
Same setup exactly, to compare full fine-tuning vs. PEFT properly. `learning_rate: 2e-4` becomes correct again there — it's LoRA's native context, not full fine-tuning's. Document `r`, `alpha`, `target_modules`.
