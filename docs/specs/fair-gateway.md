# Fair Gateway for Deposits & Withdrawals (DCW · PoA · PoQ · WID)

**Goal:** Remove opaque timing and reordering from centralized deposit/withdraw queues by making them **deterministic, auditable, and penalizable** when these flows touch the chain.

This spec defines four interoperable pieces:

- **DCW — Deterministic Credit Window:** For each asset, a venue publishes "credit after N confirmations or T seconds (whichever later)" and posts a service bond. Missing the deadline is slashable.
- **PoA — Proof‑of‑Arrival:** A light proof that a deposit reached `N` confirmations on its origin chain (SPV for UTXO chains, header+receipt for EVM). Starts the DCW clock.
- **PoQ — Proof‑of‑Queue:** A rolling Merkle **commit→reveal** of the *exact order* of **deposit credits** and **withdraw broadcasts** with monotonic sequence numbers.
- **WID — Withdrawal Intent with Deadline:** When a user requests a withdrawal, the venue submits a signed intent including a **max broadcast time**. Missing it is slashable.

(Full spec continues with interfaces, schemas, rules, penalties, UX, and edge cases.)