#!/usr/bin/env python3
"""Deterministic non-proof stress tests for one-variable rational circuits.

The proof does not depend on these tests. They target the failure mode that
motivated the new theorem: syntactic divisions, cancellations, and pole loci.
"""
from __future__ import annotations

import random
import sympy as sp

rng = random.Random(20260814)
x = sp.symbols("x")

# Each state stores a rational function achievable using exactly the nonlinear
# gates used so far. Free affine combinations are used to create operands.
def affine(states):
    coeffs = [rng.randint(-2, 2) for _ in range(len(states) + 2)]
    out = sp.Integer(coeffs[0]) + coeffs[1] * x
    for c, s in zip(coeffs[2:], states):
        out += c * s
    return sp.cancel(out)

checked_polynomial_outputs = 0
for q in range(1, 5):
    for _trial in range(20):
        states = []
        valid = True
        for _ in range(q):
            A = affine(states)
            B = affine(states)
            if rng.random() < 0.5:
                nxt = sp.cancel(A * B)
            else:
                if sp.cancel(B) == 0:
                    valid = False
                    break
                nxt = sp.cancel(A / B)
            states.append(nxt)
        if not valid or not states:
            continue

        # Use a free affine output combination. Retain only polynomial outputs,
        # matching the hypothesis of Lemma 1.
        G = affine(states)
        num, den = sp.fraction(sp.cancel(G))
        if sp.Poly(den, x).degree() != 0:
            continue
        G = sp.Poly(sp.cancel(num/den), x)
        if G.is_zero:
            continue
        checked_polynomial_outputs += 1

        # Every target fibre has at most degree(G) complex roots, and the
        # circuit-fibre lemma predicts degree(G) <= 2^q in this 1-D setting.
        # (Pointwise poles can only reduce the regular fibre.)
        assert G.degree() <= 2**q, (q, G.degree(), G.as_expr())

# Hand-built cancellation pathologies.
for h in [x, x-1, x**2+1, (x-2)*(x+3)]:
    f = x**4 + 2*x + 7
    expr = sp.cancel((f*h)/h)
    assert sp.cancel(expr-f) == 0

assert checked_polynomial_outputs >= 5
print(f"PASS rational-circuit stress suite ({checked_polynomial_outputs} polynomial outputs)")
print("NOTE stress suite is sanity evidence only; THEOREM.md carries the general argument")
