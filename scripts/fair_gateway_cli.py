#!/usr/bin/env python3
# fair_gateway_cli.py — build/verify PoQ commits and reveals (stdlib-only)
import argparse, json, hashlib
from typing import List, Dict, Any

def sha256(b: bytes) -> bytes: return hashlib.sha256(b).digest()

def to_leaf(event: Dict[str, Any]) -> bytes:
    canon = json.dumps(event, sort_keys=True, separators=(',',':')).encode('utf-8')
    return sha256(canon)

def merkle_root(leaves: List[bytes]) -> bytes:
    if not leaves: return b'\x00' * 32
    level = leaves[:]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            a = level[i]; b = level[i+1] if i+1 < len(level) else level[i]
            nxt.append(sha256(a + b))
        level = nxt
    return level[0]

def build_proofs(leaves: List[bytes]) -> List[List[str]]:
    if not leaves: return []
    tree = [leaves[:]]
    while len(tree[-1]) > 1:
        cur = tree[-1]; nxt = []
        for i in range(0, len(cur), 2):
            a = cur[i]; b = cur[i+1] if i+1 < len(cur) else cur[i]
            nxt.append(sha256(a + b))
        tree.append(nxt)
    proofs = []
    for idx in range(len(leaves)):
        sibs = []; pos = idx
        for level in range(len(tree)-1):
            cur = tree[level]; pair = pos ^ 1
            sib = cur[pair] if pair < len(cur) else cur[pos]
            sibs.append(sib.hex()); pos //= 2
        proofs.append(sibs)
    return proofs

def verify_proof(leaf_hex: str, proof: List[str], root_hex: str, index: int) -> bool:
    node = bytes.fromhex(leaf_hex); idx = index
    for sib_hex in proof:
        sib = bytes.fromhex(sib_hex)
        node = sha256(node + sib) if idx % 2 == 0 else sha256(sib + node)
        idx //= 2
    return node.hex() == root_hex

def load_events(path: str) -> List[Dict[str, Any]]:
    with open(path, 'r', encoding='utf-8') as f: return json.load(f)

def cmd_commit(args):
    evs = load_events(args.events); leaves = [to_leaf(e) for e in evs]
    root = merkle_root(leaves).hex()
    print(json.dumps({"venue": evs[0].get("venue","unknown") if evs else "unknown",
                      "tick": int(args.tick), "root": root, "count": len(evs)}, indent=2))

def cmd_reveal(args):
    evs = load_events(args.events); leaves = [to_leaf(e) for e in evs]
    proofs = build_proofs(leaves)
    items = [{"event": e, "leaf": leaf.hex(), "index": i, "proof": proofs[i]}
             for i, (e, leaf) in enumerate(zip(evs, leaves))]
    print(json.dumps({"tick": int(args.tick), "root": args.root.lower(), "items": items}, indent=2))

def cmd_verify(args):
    with open(args.reveal, 'r', encoding='utf-8') as f: rev = json.load(f)
    root = rev["root"].lower(); ok_all = True
    for it in rev["items"]:
        ok = verify_proof(it["leaf"], it["proof"], root, it["index"])
        if not ok: ok_all = False; print(f"FAIL index={it['index']} uid={it['event'].get('uid')}")
    if ok_all: print("OK: all proofs verified against root", root)

def main():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="cmd", required=True)
    c = s.add_parser("commit"); c.add_argument("--events", required=True); c.add_argument("--tick", required=True); c.set_defaults(func=cmd_commit)
    r = s.add_parser("reveal"); r.add_argument("--events", required=True); r.add_argument("--tick", required=True); r.add_argument("--root", required=True); r.set_defaults(func=cmd_reveal)
    v = s.add_parser("verify"); v.add_argument("--reveal", required=True); v.add_argument("--root", required=True); v.set_defaults(func=cmd_verify)
    args = p.parse_args(); args.func(args)
if __name__ == "__main__": main()
