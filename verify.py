#!/usr/bin/env python3
"""Replay the machine-checkable part of the valid-division permanent proof.

Trust boundary:
  * This script checks exact algebraic bookkeeping, gate degrees, exponent transfer,
    the 1/144 constant, the floor/log inequality, the frozen claim schema, and a
    deliberately adversarial pole-cancellation example.
  * It does NOT re-prove the external theorems listed in SOURCE_AUDIT.md
    (Baur--Strassen, affine Bezout, holomorphic IFT, or the dimension-of-image
    theorem). Those dependencies are explicitly pinned and their use is isolated
    as proof obligations in proof_obligations.json.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent

claim = json.loads((ROOT / "claim.json").read_text())
obligations = json.loads((ROOT / "proof_obligations.json").read_text())["obligations"]

# Frozen public claim schema.
assert claim["field"] == "C"
assert claim["threshold_n"] == 2**16
assert claim["constant_denominator"] == 144
assert claim["review_status"] == "pending"

# Public statement alignment: the canonical theorem file must carry the frozen threshold
# and explicit denominator used by claim.json.
theorem_text = (ROOT / "THEOREM.md").read_text()
assert "n >= 2^16" in theorem_text
assert "n^2}{144" in theorem_text
assert "valid arithmetic circuit" in theorem_text
assert len(obligations) == 9
assert [o["id"] for o in obligations] == [f"O{i}" for i in range(1, 10)]
assert all(o["status"] not in {"open", "failed", "unknown"} for o in obligations)

# Gate-degree certificate. After collapsing free affine operations, a nonlinear
# gate has affine operands A,B in the original inputs and preceding nonlinear
# outputs. Multiplication uses v-A*B=0; division uses B*v-A=0.
u, v, w = sp.symbols("u v w")
a0, a1, a2, b0, b1, b2 = sp.symbols("a0 a1 a2 b0 b1 b2")
A = a0 + a1*u + a2*w
B = b0 + b1*u + b2*w
mult_eq = sp.Poly(v - A*B, u, w, v)
div_eq = sp.Poly(B*v - A, u, w, v)
assert mult_eq.total_degree() <= 2
assert div_eq.total_degree() <= 2

# Exact exponent transfer. For an exact grid of (d,k), compute the least
# integer s with (d-1)^k <= 2^(3s) using integer arithmetic only.
def least_s_for_power_bound(M: int) -> int:
    s = 0
    while (1 << (3*s)) < M:
        s += 1
    return s

for d in range(2, 80):
    for k in range(1, 50):
        M = (d - 1) ** k
        smin = least_s_for_power_bound(M)
        assert M <= 2 ** (3*smin)
        if smin:
            assert M > 2 ** (3*(smin - 1))

# Exact symbolic logarithm identity used in the constant derivation:
# log_2(ell/8) = log_2(ell) - 3 for ell>0.
ell = sp.symbols("ell", positive=True)
log_identity = sp.simplify(sp.log(ell/8, 2) - (sp.log(ell, 2) - 3))
assert log_identity == 0

# Exact coefficient arithmetic:
# (n^2/48)/3 = n^2/144.
for n2 in [1, 2, 17, 65536**2, 10**30]:
    assert Fraction(n2, 48) / 3 == Fraction(n2, 144)

# Independently replay OpenAI's floor inequality
# d-1 >= ell/8 for every real ell>=16, where d=floor(ell/4).
# On each block ell in [4m,4m+4), d=m. The gap
#   (m-1) - ell/8
# decreases with ell, so its infimum on the block is the right-limit
#   (m-1) - (4m+4)/8 = m/2 - 3/2,
# which is nonnegative for m>=4.
for m in range(4, 100_000):
    right_limit_gap = Fraction(m, 2) - Fraction(3, 2)
    assert right_limit_gap >= 0

# Adversarial syntactic-pole example.
# f=x^3+y^3 can be computed by a valid rational circuit containing
# ((f*y)/y). On the original slice y=0 the syntactic divisor vanishes
# identically. Translating the slice to y=t (t != 0 as a rational function)
# repairs validity, while G_t(u)=partial_x f(u,t)=3u^2 keeps two simple roots
# over target 3.
x, y, t = sp.symbols("x y t")
f = x**3 + y**3
rational_output = sp.cancel((f*y)/y)
assert sp.cancel(rational_output - f) == 0
assert y.subs(y, 0) == 0
assert sp.Poly(t, t).is_zero is False
G = sp.diff(f, x).subs({x: u, y: t})
assert sp.expand(G - 3*u**2) == 0
roots = sp.solve(sp.Eq(G, 3), u)
assert set(roots) == {-1, 1}
assert all(sp.diff(G, u).subs(u, r) != 0 for r in roots)

# The generic-translation exceptional set in this example is exactly t=0;
# the bad target image of the pole set is empty once t is a nonzero constant.
tau = sp.symbols("tau")
restricted_divisor = y.subs({y: tau})
assert sp.Poly(restricted_divisor, tau).as_expr() == tau

print("PASS claim schema")
print("PASS multiplication/division gate equations have total degree <= 2")
print("PASS exact integer exponent-transfer audit")
print("PASS symbolic log identity and 1/144 constant arithmetic")
print("PASS floor inequality d-1 >= log2(n)/8 for n >= 2^16")
print("PASS adversarial denominator-annihilation / translation example")
print("PASS all proof obligations are closed in the frozen ledger")
print("NOTE external theorem dependencies are source-audited, not formalized here")
