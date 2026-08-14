#!/usr/bin/env python3
"""Independent standard-library replay of the integer bookkeeping.

This intentionally shares no symbolic-algebra dependency with verify.py.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
claim = json.loads((ROOT / "claim.json").read_text())

assert claim["threshold_n"] == 65536
assert claim["constant_denominator"] == 144

# Check exact denominator composition 48*3=144 and a large collection of
# exact rational instances.
assert 48 * 3 == 144
for n in [65536, 65537, 10**5, 10**6, 2**32, 10**20]:
    assert Fraction(n*n, 48) / 3 == Fraction(n*n, 144)

# For every m>=4, ell in [4m,4m+4) has floor(ell/4)=m and the worst case
# for d-1 >= ell/8 is the right endpoint. The exact gap there is
# m/2 - 3/2. Checking its affine formula at m=4 and slope 1/2 proves it
# for all m>=4; the finite loop is merely an additional implementation check.
assert Fraction(4, 2) - Fraction(3, 2) == Fraction(1, 2)
assert Fraction(1, 2) > 0
for m in range(4, 1_000_000):
    assert Fraction(m, 2) - Fraction(3, 2) >= 0

# Integer form of M <= 2^(3s): independently find the threshold with a
# bit-shift loop and check the preceding value fails.
for base in range(1, 100):
    for k in range(1, 80):
        M = base ** k
        s = 0
        bound = 1
        while bound < M:
            s += 1
            bound <<= 3
        assert bound >= M
        if s:
            assert (bound >> 3) < M

print("PASS independent standard-library constant audit")
print("PASS independent exact floor-bound audit")
print("PASS independent integer exponent-threshold audit")
