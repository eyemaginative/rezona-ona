# REZONA (ONA)

**A Harmonic, MEV‑Resistant Blockchain with Oscillation‑Normalized Agreement**  
*Whitepaper v0.2r — Terminology update*

---

## Abstract
This document describes a standalone Substrate blockchain that introduces ONA consensus — Oscillation-Normalized Agreement, a commit→slot→reveal + harmonic sequencing design that makes MEV extraction uneconomic. ONA replaces competition for hardware (PoW) or capital (PoS) with information alignment: blocks are valid only if their transaction flow respects micro-slot ordering and achieves low Harmonic Loss (HL) derived from phase/PSD/SNR features. Rewards scale by exp(−HL), so honest, well-tuned blocks pay best.

---

## 0. Identity & Links
- **Protocol / Chain:** REZONA  
- **Ticker:** **ONA**  
- **Consensus:** **Oscillation‑Normalized Agreement (ONA)**  
- **Tagline:** *Stay in tune.*  
- **Official site:** https://eyemaginative.github.io/rezona-ona/  
- **X (Twitter):** `@rezonahub`

---

## ONA: Canonical Expansions (Family)
1) **Oscillation‑Normalized Agreement** — consensus predicate  
2) **Order‑Normalized Assembly** — deterministic micro‑slot building  
3) **Orchestrated Noise Attenuation** — anti‑MEV mempool & sequencing  
4) **Optimal Node Alignment** — validator reputation (RW)  
5) **Observational Network Attestation** — commit→slot→reveal integrity  
6) **Oscillator‑Native Accounting** — tokenomics/issuance breathing  
7) **Objective Nonlinear Analysis** — features for HL (phase/PSD/SNR)  
8) **Orthogonal Noise Annulling** — SNR spam filter  
9) **Open Network of Agents** — ecosystem of apps  
10) **On‑chain Network Autonomy** — governance/upgrades

---

## 1. Build Philosophy & Deployment Shape
- **Independence:** v1 is a **solo Substrate chain** (BABE VRF authoring + GRANDPA finality).  
- **Path later:** optional Polkadot parachain or bridges; ONA consensus lives in the runtime.  
- **Why solo:** faster iteration on parameters (W, Δ, ε, α/β/γ, τ) and economics.

---

## 2. Architecture Overview (ONA consensus)
**Pipeline:**
1) **Commit**: users submit `C = H(tx)` plus VRF ticket `π`.  
2) **Slot assignment**: with randomness `R_t`, map to micro‑slot `s = F(π, R_t) mod W` for block *t+1*.  
3) **Reveal**: open `tx`; validators check `H(tx)=C` and slot eligibility `(s ∈ ±ε)`.  
4) **Order‑Normalized Assembly**: builder sweeps slots in order `0..W−1`; no cross‑slot jumps.  
5) **Harmonic checks**: compute **HL** over phase/PSD/SNR.  
6) **Finalize & reward**: block valid iff `HL ≤ τ`; reward `= base · exp(−HL)`.

**Ordering is validity:** if a tx appears outside its slot window or the block’s HL exceeds `τ`, the block is invalid. Inside a slot, co‑eligible txs may be fee‑sorted with adjacency guards.

## 2.1 Notation (cheat sheet)

| **Symbol**    | **Meaning**                                            |
| --------- | -------------------------------------------------- |
| `W`       | Micro-slots per block (e.g., 256)                  |
| `ε`       | Grace window in slots (e.g., ±1)                   |
| `Δ`       | Commit→reveal delay in blocks (e.g., 1)            |
| `τ`       | Harmonic Loss validity threshold                   |
| `α, β, γ` | HL coefficients (phase, PSD, SNR)                  |
| `R_t`     | Block-level randomness for slot mapping            |
| `π`       | User VRF ticket included at commit                 |
| `s`       | Assigned micro-slot for a tx in block *t+1*        |
| `HL`      | Harmonic Loss for a candidate block                |
| `RW`      | Validator Resonance Weight (reputation multiplier) |

## 2.2 Validity & payout rules (normative)

A block MUST satisfy all of the following to be valid:

**Commit→Reveal binding**
Every revealed transaction tx MUST match a prior commitment C = H(tx) made at or before t−Δ.

**Slot eligibility**
Let s = F(π, R_t) mod W be the assigned micro-slot for tx. The block MUST place tx within the window s ± ε. Inclusion outside that window makes the block invalid.

**Order-Normalized Assembly**
The builder MUST sweep slots in ascending order 0..W−1. Cross-slot reorders (e.g., inserting a slot-8 tx while building slot-5) are invalid.

**Harmonic Loss bound**
Compute HL for the block. If HL > τ, the block is invalid.

**Commit integrity**
All commitments used in the block MUST be unique and referenced at most once.

**Payout shaping (applies after validity):**

**Author reward:**
reward = base · exp(−HL) · RW_author

**Resonance Weight update (EMA, clamped):**
RW_author ← clamp( RW_min,
                   RW_max,
                   (1−λ)·RW_author + λ·exp(−HL) )
with suggested λ = 0.1, RW_min=0.5, RW_max=1.2.

**Rationale:** making ordering part of validity plus reward curvature removes profitable MEV paths; honest sequencing dominates.

---

## 3. Harmonic Loss (HL)

**We model per-block transaction cadence as a signal and penalize manipulative patterns:**
HL = α · Σ_s Σ_{tx∈slot(s)} ε_phase(tx,s)^2
   + β · ε_psd(block)^2
   + γ · (1 / max(SNR(block), ε_snr))
**Phase error (ε_phase):** deviation from the predicted slot-phase trajectory φ(s) for eligible txs.

**PSD distance (ε_psd):** Wasserstein/EMD between expected vs realized per-slot distribution over a window K.

**SNR term:** suppresses spam/noise; ε_snr ≈ 1e−9 avoids division by zero.

**Enforcement modes:**

**Hard validity:** reject the block if HL > τ.

**Reward shaping:** for valid blocks, scale payout by exp(−HL).

---

## 4. Economics (Oscillator‑Native Accounting)
- **Issuance target:** ~**3.0% APR**, decaying 0.25%/yr → **1.0% floor**.  
- **Fee policy:** EIP‑1559‑style base fee; **50% burned**, tips to author.  
- **Rewards:** `reward = base · exp(−HL) · RW` where **RW** is a smoothed reputation (EMA of `exp(−HL)`), bounded (e.g., 0.5×–1.2×).  
- **Resonance Index (RI)** (narrow modulation): `issuance = base · (0.75 + 0.25 · RI)` with `RI∈[0,1]` from network‑wide HL.

---

## 5. Parameters (initial defaults)
- **Block time:** ~2s  
- **Micro‑slots per block (W):** 256  
- **Commit→reveal delay (Δ):** 1 block  
- **Grace window (ε):** ±1 slot  
- **HL coefficients:** α=1.0, β=0.5, γ=0.2  
- **HL threshold (τ):** 1.0 (tune on testnet)  
- **PSD window (K):** 128 blocks  
- **Decimals:** 9 (1 ONA = 1e9 plancks)  
- **SS58:** 42 (Substrate default)

## 5.1 Choosing parameters (testnet starting points)

W = 256, ε = 1, Δ = 1, τ = 1.0

α = 1.0, β = 0.5, γ = 0.2, K = 128

Block time ≈ 2s; tune τ to target ~95–99% acceptance for honest builders.

---

## 6. Threat Model & Defenses
| Threat | Manipulation | ONA Defense |
|---|---|---|
| Front‑run | Pull tx ahead of victim | Slot binding forbids cross‑slot jumps; phase check ↑HL |
| Sandwich | Bracket victim (pre+post) | Local discontinuity spikes HL; invalid or low reward |
| Back‑run bursts | Concentrated chase | PSD smoothing; bursts ↑HL |
| Spam/DoS | Flood mempool | SNR penalty + per‑slot caps + slow‑lane drain |
| Censorship | Skip eligible txs | Missing mass ↑HL; reputation drops (RW↓) |
| Collusion | Private reorder | Cross‑slot reorder invalid; honest builders out‑earn colluders |

---

## 7. Off‑Chain & CEX Interface
We can’t *ban* off‑chain trades, but we can make them **provably fair** when they touch the chain and **prefer** on‑chain flow.

**FSE — Fair‑Settlement Envelope**: commit/reveal logs for venues + non‑transferable **FFB — Fair‑Flow Badge**. See separate spec.

See Exchange Fairness Add-On (FSE + FFB) for the commit→reveal queue, deadlines, bond/slash, and venue badge rules. The chain can gate bridges and fee tiers by badge grade to prefer venues that honor on-chain time.

---

## 8. Validators (Optimal Node Alignment)
- **RW (Resonance Weight):** EMA of `exp(−HL)` per validator; bounded effect on slot odds/payout.  
- **Sybil deterrence:** new identities reset RW; a small refundable admission bond deters churn.  
- **Censorship is costly:** skipped slots ↑HL and erode RW.

---

## 9. Implementation Plan
M1 Commit/Reveal → M2 Slot‑enforced assembly → M3 Harmonic Loss + telemetry → M4 Rewards/fees → M5 FSE/FFB pallets → M6 UX tooling.

## 9.1 Security considerations

**Randomness & VRF:** R_t must be unbiased and unpredictable; verify VRF proofs on reveal.

**Clocking:** use chain time for deadlines; bound acceptable drift for external proofs.

**Spam bounds:** cap per-slot inclusions; SNR term discourages flood patterns.

**Censorship:** skipping eligible txs increases HL and erodes RW; multi-epoch reputation reduces cheap identity resets.

**Economic games:** sandwich/front-run require cross-slot distortions that violate validity or incur high HL, making them uneconomic.

---

## 10. Credits & Related Work
We acknowledge prior community discussions around harmonic-style reasoning about information and thank Jason Padgett for popularizing geometric/harmonic visualizations that influenced our communication and branding. The protocol and terminology presented here—Oscillation-Normalized Agreement (ONA)—are original to this project.

---

## 11. Compliance
Experimental software; not investment advice.
