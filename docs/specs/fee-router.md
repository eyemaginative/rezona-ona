# Fee Router (Multi-Asset Fees)

Goal: let users pay ONA-denominated fees with BTC/ETH/SOL. The router escrows the foreign asset, quotes `ona_needed`, settles ONA on-chain, and retains a tiny per-asset **reserve skim** for operations.

## Interfaces (suggested)
- `set_asset_params(asset, enabled, skim_bps)` — root
- `pay_fee_in(asset, max_in, call_hash)` — user
- `withdraw_reserve(asset, to, amount)` — root (ops only)
- `get_reserve(asset)` — view

## Events
`FeePaid { payer, asset, amount_in, ona_settled, skim }`, `AssetParamsSet`, `ReserveWithdrawn`.

## Notes
- Validators receive ONA; the router handles foreign assets.
- Reserves are operational, publicly visible, and capped by policy.
