# REZONA (ONA)

**A Harmonic, MEV‑Resistant Blockchain with Oscillation‑Normalized Agreement**  
*Whitepaper v0.2r — Terminology update (replaces “QIH” with “ONA consensus”)*

---

## Abstract
This document describes a standalone Substrate blockchain that introduces **ONA consensus — Oscillation‑Normalized Agreement**, a commit→slot→reveal + harmonic sequencing design that makes **MEV extraction uneconomic**. ONA replaces competition for hardware (PoW) or capital (PoS) with **information alignment**: blocks are only valid if their transaction flow respects **micro‑slot ordering** and achieves low **Harmonic Loss (HL)** derived from phase/PSD/SNR features. Rewards scale by **`exp(−HL)`**, so honest, well‑tuned blocks pay best.

This revision removes all references to “QIH / Quantum Information Harmonics” as a protocol name. The underlying ideas are preserved and fully attributable to our own **ONA consensus** design.

---

## 0. Identity & Links
- **Protocol / Chain:** REZONA  
- **Ticker:** **ONA**  
- **Consensus:** **Oscillation‑Normalized Agreement (ONA)**  
- **Tagline:** *Stay in tune.*  
- **Official site:** `eyemaginative.github.io/rezona-ona/`  
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

---

## 3. Harmonic Loss (HL)
We model the per‑block transaction cadence as a signal and penalize manipulative patterns:
```
HL = α · Σ_s Σ_tx∈slot(s) ε_phase(tx,s)^2
   + β · ε_psd(block)^2
   + γ · (1 / SNR(block))
```
- **Phase error**: tx vs predicted slot‑phase curve φ.  
- **PSD distance**: Wasserstein/EMD of expected vs realized slot distribution.  
- **SNR penalty**: discourages spam/noise.

Two enforcement modes: **hard validity** (`HL>τ` → reject) and **reward shaping** (`reward *= exp(−HL)`).

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

---

## 8. Validators (Optimal Node Alignment)
- **RW (Resonance Weight):** EMA of `exp(−HL)` per validator; bounded effect on slot odds/payout.  
- **Sybil deterrence:** new identities reset RW; a small refundable admission bond deters churn.  
- **Censorship is costly:** skipped slots ↑HL and erode RW.

---

## 9. Implementation Plan
M1 Commit/Reveal → M2 Slot‑enforced assembly → M3 Harmonic Loss + telemetry → M4 Rewards/fees → M5 FSE/FFB pallets → M6 UX tooling.

---

## 10. Credits & Related Work
The term **“Quantum Information Harmonics”** has been used informally in the community to discuss harmonic‑style reasoning about information. We draw inspiration from that general theme, and we gratefully acknowledge **Jason Padgett** for popularizing geometric/harmonic visualizations that motivated aspects of our communication and branding. This project’s protocol, terminology, and consensus—**Oscillation‑Normalized Agreement (ONA)**—are original and specific to this chain.

---

## 11. Compliance
Experimental software; not investment advice.
