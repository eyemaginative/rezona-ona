# Exchange Fairness Add‑On (FSE + FFB)

**Goal.** Make centralized deposit/withdraw flows *deterministic, transparent, and economically honest* when they touch the chain. This add‑on defines two pieces any venue can implement and any wallet can verify:

- **FSE — Fair‑Settlement Envelope.** A rolling, *commit→reveal* log of the exact order of **deposit credits** and **withdraw broadcasts**, bound to objective **deadlines** and backed by a *service bond*.
- **FFB — Fair‑Flow Badge.** A non‑transferable on‑chain badge (soulbound) proving a venue’s clean operating history. Computed from the FSE stream and used to *gate perks and bridges*.

This spec is chain‑agnostic and plugs into ONA as a **runtime pallet** or smart‑contract module.

---

## At‑a‑glance

| Field | Value |
|---|---|
| **Scope** | Deposits (crediting) and withdrawals (broadcasting) when they interface with L1 chains |
| **Actors** | Users, Venues (CEX/bridge), Auditors/Watchers, Wallets |
| **Clocking** | `Δt` commit interval (e.g., 10–30s); reveals follow each commit |
| **Deadline policy (DCW)** | Per asset: `N_conf` confirmations **or** `T_max` seconds since submit — whichever is later |
| **What is committed** | Merkle root of a strictly ordered batch with `venue_seq` monotonic |
| **On‑chain state** | Service **bond**, rolling **badge** (grade A–F), policy registry (DCW) |
| **Slashable** | Late or missing items vs deadline; malformed sequence; bad proofs |
| **Compensation (opt.)** | Price‑Move Compensation (PMC), bounded by policy |
| **User UX** | *Credit by* time, batch proofs, venue badge chip |
| **Interfaces** | `bond`, `set_dcw`, `commit_root`, `reveal_batch`, `slash_if_late`, `withdraw_intent`, `get_badge`, `get_stats` |

---

## 1) Deterministic envelopes (FSE)

### 1.1 Items
Two canonical event types are recorded in sequence:
```json
{
  "type": "deposit_credit | withdraw_broadcast",
  "venue": "example-cex-1",
  "venue_seq": 123456,
  "uid": "evt-123456",
  "asset": "DOGE",
  "amount": "100.0",
  "account": "hash-of-user-or-account",
  "dest_addr": "Dxyz...",            
  "source_txid": "DOGE-txid",        
  "chain_id": "doge | eth | ona",
  "deadline": 1725491800,            
  "ts_planned": 1725491790,          
  "risk_flag": null,                 
  "sig": "venue-signature"
}
```

### 1.2 Policy surface (per asset, per venue)
```
N_conf   — confirmations to recognize a deposit on origin chain
T_max    — hard cap in seconds since user submitted (whichever later)
```
**Deadline:** `deadline = max(t_conf_N , t_submit + T_max)`

### 1.3 Commit → reveal
- **Commit**: every Δt seconds the venue publishes `commit_root(venue, root, tick)`,
  where `root = Merkle(batch)` of items since last tick.
- **Reveal**: `reveal_batch(venue, tick, batch_blob)` presents all items and proofs.
- **Rules**:
  - `venue_seq` must strictly increase.
  - Any **deposit_credit** whose `deadline ≤ now()` must appear no later than the next commit tick.
  - Any **withdraw_broadcast** must correspond to a prior **withdraw_intent** (see Fair Gateway).

### 1.4 Bond & penalties
- `bond(venue, asset, amount)` posts a service bond sized to deter abuse.
- `slash_if_late(venue, uid)` slashes when deadlines are missed.
- Optional **Price‑Move Compensation (PMC)**: a capped formula compensates late credits against reference prices.

---

## 2) Fair‑Flow Badge (FFB)

A venue’s public, non‑transferable badge reflects objective performance over a sliding window **K**:

```
lateness_rate    = late_items / total_items
missing_rate     = missing_items / total_items
median_lateness  = median(max(0, t_observed - deadline))
commit_uptime    = commits_ok / commits_expected
badge_score      = f(lateness_rate, missing_rate, median_lateness, commit_uptime)
grade ∈ {A, B, C, D, F} from thresholds
```

- Badge is updated automatically from the FSE stream.
- Badge cannot be transferred and resets if the venue key rotates without a hand‑over proof.
- Consumers (DEX aggregators, wallets, bridges) **gate perks** by grade:
  - Example: Only **A/B** venues can use the fast bridge; **C/D** pay a higher fee and face per‑batch caps.

---

## 3) Runtime / contract interface (suggested)

```
bond(venue, asset, amount)
set_dcw(venue, asset, N_conf, T_max)
commit_root(venue, root, tick)
reveal_batch(venue, tick, blob)
slash_if_late(venue, uid)
withdraw_intent(venue, payload)   // from Fair Gateway
get_badge(venue) -> { grade, score, window }
get_stats(venue) -> { counts, lateness, uptime }
```

**Events**: `Arrival`, `Committed`, `Revealed`, `Slashed`, `BadgeUpdated`.

---

## 4) Verification & UX

- Wallets show **“Credit by HH:MM:SS”** once PoA confirms + DCW known.
- The *Activity* panel shows commits/reveals with links to the on‑chain proof.
- If an item is late or missing, the UI flags it and links to `slash_if_late`.
- A **Fair‑Flow badge** chip appears next to venue names across the app/bridge.

---

## 5) Security notes

- **Clock skew**: use chain time; venue may publish signed NTP offset.
- **Origin chain stalls**: `N_conf` dominates `T_max`.
- **Privacy**: store only hashes of account ids; never PII.
- **DoS**: bound batch size; enforce minimum bond; commit interval Δt.
- **Auditors**: independent watchers can reconstruct the queue and prove misbehavior.

---

## 6) Example thresholds (informative)

```
Grade A: lateness_rate < 0.5%, missing_rate = 0, commit_uptime ≥ 99.5%
Grade B: lateness_rate < 1.0%, missing_rate ≤ 0.1%, commit_uptime ≥ 99.0%
Grade C: lateness_rate < 2.0%, missing_rate ≤ 0.5%, commit_uptime ≥ 98.0%
Grade D: worse than C
Grade F: chronic missing or bond exhausted → badge revoked
```

---

## 7) Integration checklist for venues

1. Post a **bond** and publish **DCW** policy.
2. Emit **PoA** when `N_conf` reached and start the **deadline** clock.
3. Publish **commit_root** every Δt and **reveal_batch** afterward.
4. Handle **withdraw_intent** and include **withdraw_broadcast** by deadline.
5. Maintain grade **A/B** to access fast bridge & reduced fees.

---

*This specification is part of the REZONA (ONA) documentation set and is designed to work with the Fair Gateway spec.*
