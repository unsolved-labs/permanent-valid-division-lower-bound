# Permanent lower bound with valid division

Canonical research artifact for **Unsolved Labs R014**.

## Result

For every integer \(n\ge 2^{16}\), every valid arithmetic circuit over \(\mathbb C\) computing the \(n\times n\) permanent has nonscalar multiplication/division complexity \(s\) satisfying

\[
s\ge \frac{n^2}{144}\bigl(\log_2\log_2 n-3\bigr).
\]

A division gate is valid when its divisor is a nonzero rational function in the input function field. Additions, subtractions, and scalar operations are free in the nonscalar model, so the same expression also lower-bounds ordinary total arithmetic-gate count.

The complete proof is in [`THEOREM.md`](THEOREM.md). The frozen statement and scope are recorded in [`claim.json`](claim.json), and the dependency ledger is in [`proof_obligations.json`](proof_obligations.json).

## Reproduce

Python 3.12 is used in CI.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python verify.py
python verify_independent.py
python stress_rational_circuits.py
```

Every command must exit with status zero and print `PASS`.

The principal verifier checks the frozen claim schema, multiplication/division gate-equation degree, exact exponent transfer, the explicit \(1/144\) constant, the floor/log inequality, and an adversarial denominator-annihilation example. A second implementation independently replays the integer bookkeeping using only the Python standard library. The stress suite targets cancellation and pole pathologies and is sanity evidence rather than part of the proof.

## Trust boundary

The theorem is a deductive proof, not a finite computational certificate. The executable replay verifies the machine-reducible portion and statement alignment. The external mathematical dependencies—Baur–Strassen differentiation, affine Bézout for isolated solutions, the holomorphic implicit/inverse-function theorem, and dimension of polynomial images—are isolated in [`SOURCE_AUDIT.md`](SOURCE_AUDIT.md) and [`proof_obligations.json`](proof_obligations.json).

No Lean or Coq formalization is claimed. Independent specialist review is pending.

## Files

- [`THEOREM.md`](THEOREM.md) — statement and complete proof.
- [`SOURCE_AUDIT.md`](SOURCE_AUDIT.md) — baseline, novelty, and primary-source dependency audit.
- [`claim.json`](claim.json) — machine-readable frozen claim and circuit model.
- [`proof_obligations.json`](proof_obligations.json) — complete proof-obligation ledger.
- [`verify.py`](verify.py) — principal machine-reducible replay.
- [`verify_independent.py`](verify_independent.py) — dependency-free independent arithmetic replay.
- [`stress_rational_circuits.py`](stress_rational_circuits.py) — deterministic pole/cancellation stress suite.
- [`requirements.txt`](requirements.txt) — pinned verifier dependency.
- [`.github/workflows/verify.yml`](.github/workflows/verify.yml) — clean-checkout CI replay.

## Public baseline

OpenAI's updated 2026 arithmetic-circuit result proves, for the permanent, the same explicit lower bound for **division-free** general arithmetic circuits. The paper states that its permanent-specific \(\Omega(N\log\log N)\) circuit theorem does not treat circuits with division:

- OpenAI, *Ten Advances in Mathematics and Theoretical Computer Science*, Chapter 5, updated August 6, 2026: https://cdn.openai.com/pdf/ten-proofs-oai.pdf

The transfer uses the rational-function differentiation theorem of Baur and Strassen, whose nonscalar model counts multiplication and division:

- Walter Baur and Volker Strassen, *The complexity of partial derivatives*, Theoretical Computer Science 22 (1983), 317–330: https://doi.org/10.1016/0304-3975(83)90110-X

A targeted literature audit through August 14, 2026 found no prior theorem matching this valid-division extension. This is a literature-search boundary, not a claim about unpublished or unindexed work.

## Scope

The theorem is over \(\mathbb C\) and uses rational-function validity: a divisor must be nonzero as an element of the function field, not nonzero at every numerical input. It does not address determinant circuits, does not improve the explicit division-free constant, and does not claim the lower bound is optimal.
