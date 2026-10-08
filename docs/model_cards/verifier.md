# Vision-language verifier model card

**Model:** Qwen3-VL-8B-Instruct, used as a constrained weapon/not-weapon/uncertain verifier. The model/prompt and veto policy were frozen. No checkpoint or external model code is redistributed.

V can veto only an explicit `not_weapon` answer below tau_hi. At or above tau_hi the frozen weapon rule bypasses V. This saves verification work but allows high-scoring look-alikes through. Uncertain answers are not treated as confident negative evidence.

At q2, 643/766 MEVA-test NEW notices and 166/197 NWPU NEW notices bypassed V; 610/159 respectively have saved `not_weapon` answers. The q1-to-q2 threshold change gains 33→36/48 weapon incidents. These **post-hoc, test-informed** observations use saved predictions. Cooldown changes prevent reconstructing a new policy by subtracting notices. A validation-only every-alert diagnostic reduced recall and was not adopted.

Greedy decoding can differ across hardware: one of 17 repeated validation inputs changed answer. One seed and finite coverage limit robustness claims. **Combined real-time test: not passed.** Running the verifier separately did not establish a passing combined configuration, and a reduced-feed attempt failed in its runtime.

Scores are model confidence, not probabilities. A language-model answer is not human confirmation or ground truth. Original weapon criterion NOT MET; revised ≤5 MET under **post-hoc revision**. See [results](../results.md), [weapon card](weapons.md) and [third-party terms](../../THIRD_PARTY_NOTICES.md).

**Public-release verification scope:** CPU rule/feature parity and stored-notice evaluation were checked. No model inference, pixel-to-notice runtime equivalence or optional inference-environment installation was tested during curation. Frozen research results do not certify a new hardware/software environment.
