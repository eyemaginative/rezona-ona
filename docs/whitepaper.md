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
- **Official site:** [eyemaginative.github.io/rezona-ona](https://eyemaginative.github.io/rezona-ona/){target=_blank rel="noopener"}
- **X (Twitter):** [@rezonahub](https://x.com/rezonahub){target=_blank rel="noopener"}

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

### 4.1 Multi-Asset Fees & Operational Reserves

ONA remains the fee/bond unit; however, a **fee router** may accept BTC/ETH/SOL for user convenience:
- For each accepted asset `a`, the router takes `amount_in`, settles `ona_needed` to the chain, and retains a small `skim_a` as **operational reserve** (`0 ≤ skim_a ≤ 0.50%`, configurable).
- Reserves are **not** investment pools; they cover routing slippage, gas sponsorship, bridge float, and auditor costs.
- Validators are paid in ONA; only the router handles foreign-asset intake.


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

## 11. Compliance & Legal

Important: This whitepaper is for information only. It is not legal, financial, or tax advice. Building, running, or using the protocol may have legal implications that vary by jurisdiction and over time. Consult qualified counsel before taking any action. Nothing herein constitutes an offer to sell, a solicitation to buy, or a recommendation regarding any asset.

## 11.1 Nature and Purpose of ONA

ONA is the native unit of account used by the network to pay for compute and storage (gas/fees), to post bonds for certain actions (e.g., venue service bonds in the FSE/FFB spec), and to meter on-chain resources.

ONA does not represent equity, debt, revenue share, dividends, profit rights, or ownership in any entity. It confers no governance or control rights over any company or foundation by default.

The protocol’s aim is technical utility (secure, MEV-resistant transaction ordering). Any secondary market price is not intended, promised, or managed by the developers.

## 11.2 No Offering; No Expectation of Profit from Others’ Efforts

The project does not plan a public token sale or fundraising via the sale of ONA. Tokens are expected to enter circulation primarily through protocol issuance and rewards for running network infrastructure, and through usage-based fees/bonds.

Marketing, documentation, and community materials must avoid investment language (e.g., “returns,” “profits,” “moon,” “price targets,” “investment,” “pump/burn to raise price”). Do not suggest any buyer can expect profit from others’ efforts.

There is no promise of buybacks, revenue distributions, or price maintenance, and no promise of listing on any exchange.

## 11.3 Token Mechanics (Utility Only)

Fees/Gas: ONA is required to pay fees for transaction execution and storage, similar in spirit to how ETH is used on Ethereum to pay gas.

Base-fee burn & tips: If the protocol includes a base-fee burn (akin to EIP-1559), it is an algorithmic network rule, not an issuer action. Tips (priority fees) compensate block authors for inclusion.

Bonds & Slashing: Certain actions (e.g., FSE/FFB venue bonds) require ONA bonds that may be slashed on rule violations. Bonds are service guarantees, not investments.

No dividends or revenue rights: ONA does not entitle holders to dividends, profit shares, or cash flows from any entity.

## 11.4 Distribution, Allocations, and Supply

Issuance: Protocol-level issuance targets ~3.0% APR decaying to ~1.0% (see §4). This is an on-chain algorithm, not discretionary issuance.

Allocations (if any): Any future allocations (e.g., contributor grants) will be publicly disclosed, subject to use restrictions (e.g., for development, testing, or ecosystem grants), and not marketed as investments.

No implied rights: Holding ONA does not confer rights to governance, revenue, or services beyond what is implemented in the open-source protocol.

## 11.5 Secondary Markets and Listings

There is no commitment to seek, support, or maintain listings on centralized or decentralized exchanges.

If third parties list ONA, they do so independently. Users are responsible for complying with all laws when using any exchange, including KYC/AML requirements that may apply to the exchange.

## 11.6 US Regulatory Notes (High-Level)

Securities laws (SEC): Whether a digital asset is a “security” depends on facts and circumstances (e.g., Howey factors). ONA is intended for consumptive use (fees, bonds) and is not marketed for profit expectations. This is not a legal determination; obtain counsel.

Commodities/CFTC: Digital assets can be treated as commodities in some contexts; derivatives/trading products may invoke additional rules.

Money transmission/FinCEN: Publishing open-source software or validating a network generally is not money transmission, but custodial services or fiat/asset exchange can trigger MSB rules. The project does not operate a custodial wallet, exchange, or fiat on-ramp.

Sanctions/OFAC: Users and integrators must not engage with sanctioned jurisdictions/persons. Venues participating in FSE/FFB are expected to maintain their own sanctions compliance.

State law (Ohio): Ohio applies federal frameworks and may impose additional licensing for custodial activities and money transmission. Do not operate custody or exchange services without proper licensing.

## 11.7 Taxes

Using, earning, or disposing of ONA may be taxable. No tax advice is provided here. Users are responsible for their own reporting and compliance.

## 11.8 Forward-Looking Statements and Changes

Roadmaps and parameters (e.g., α, β, γ, τ, W) are subject to change through transparent, open-source development processes. There is no guarantee any feature will ship or persist.

The project may update protocol code and documentation; such updates do not constitute investment promises or inducements.

## 11.9 Trademarks, License, and No Warranty

“REZONA” and “ONA” may be used as project wordmarks. Proposed software license: Apache-2.0 (permissive, includes explicit patent grant) or MIT.

Software is provided “AS IS,” without warranties or conditions of any kind. See LICENSE for details.

ONA is used for fees/gas, bonds/slashing, and potentially staking/validator collateral if later enabled. These are technical functions, not investment contracts.

**Note on foreign assets:** Any BTC/ETH/SOL retained by the protocol are **operational reserves** for routing/bridge safety and auditor funding, not investment instruments and not marketed for profit.


## 12. Cross-Asset Liquidity & Utility-Driven Inflows

ONA’s design can attract BTC/ETH/SOL and other L1 assets **without** promising price or yield by making those assets *useful* inside the ecosystem.

### 12.1 Principles
- **Utility, not investment.** All mechanisms are framed as fees, bonds, credits, and service tiers.
- **Ordering as validity.** ONA’s inclusion rules + HL penalties make settlement predictable, which venues and market makers value.
- **Operational reserves.** Any retained foreign assets are earmarked for network operations (not an investment program).

### 12.2 Service Bonds in BTC/ETH/SOL (FSE + FFB)
Venues (CEXs, bridges, custodial wallets) post **service bonds** in top L1 assets to participate in FSE/FFB.
- **Why:** Higher badge grade (A/B) unlocks fee rebates, fast lanes, higher limits.
- **Flow:** Venue deposits → maintains grade → attracts flow → earns rebates.
- **Enforcement:** Bonds are slashed for objective violations (missed deadlines, missing credits).

### 12.3 Multi-Asset Gas & Fee Router
Users may pay ONA-denominated fees with BTC/ETH/SOL via a **router**:
- Escrow foreign asset → quote → settle ONA on chain → retain tiny **reserve skim** in the foreign asset for operations.
- Improves first-use UX; validators still receive ONA.

### 12.4 Canonical Wrapped Assets (wBTC/wETH/wSOL)
Audited bridges or light-client proofs mint canonical wrapped assets on ONA.
- **Why bridge:** Apps on ONA treat wraps as first-class with faster, fair settlement.
- **Fee:** Per-transfer fee in the origin asset; a slice funds **safety reserves** and auditors.

### 12.5 Protocol-Owned Liquidity via Utility Bonding
Accept BTC/ETH/SOL as **utility bonds** in exchange for **time-vested fee credits** (gas coupons, DA credits, bridge priority).
- Credits reduce operating cost for heavy users; no emissions, no APY language.

### 12.6 Blockspace Auctions (Any-Asset Settlement)
Sealed-bid auctions for priority blockspace or batch settlement; winners settle in BTC/ETH/SOL.
- Portion retained as operational reserve; rest routed to ONA via the fee router.

### 12.7 Routing Rebates with ve-ONA (No Yield Farming)
Lock ONA to steer **rebate budgets** toward routes/pools that deepen BTC/ETH/SOL liquidity.
- LPs earn **fee rebates/credits** (not emissions); improves execution quality.

### 12.8 Validator/AVS Multi-Asset Collateral (Advanced)
For specific services (e.g., ordering oracle), allow LSTs/LRTs as collateral with explicit **slashing**.
- Opt-in, narrowly scoped; publish conditions.

### 12.9 RFQ with Bonded Market Makers
MMs bond BTC/ETH/SOL to quote; failure → **slash**; success → **rebates** and preferred routing.

### 12.10 MVP (initial delivery)
1) **FSE/FFB venue bonds** (accept BTC/ETH/SOL; slashing; badge grades).  
2) **Multi-asset fee router** (pay fees in BTC/ETH/SOL; keep tiny reserve skim).  
3) **One canonical wrapped asset** (e.g., wETH) with fairness guarantees.

### 12.11 Accounting & Communications
- Tag all foreign-asset balances as **operational reserves** dedicated to fee routing, gas sponsorship, bridge float, and auditors.
- Public dashboards should show reserves, slashes, and badge grades.
- Avoid investment language (no “yield/returns/listings”).

