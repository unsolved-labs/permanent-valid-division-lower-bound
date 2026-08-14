# Source and novelty audit

Audit date: **2026-08-14**.

## 1. Frozen public baseline

**OpenAI, _Ten Advances in Mathematics and Theoretical Computer Science_, updated 2026-08-06, Chapter 5, “Arithmetic circuit complexity.”**

Primary source: `https://cdn.openai.com/pdf/ten-proofs-oai.pdf`

Load-bearing statements checked against the current PDF:

- Theorem 1.1: for every `n >= 2^16`, division-free arithmetic circuits computing `per_n` have size at least
  `n^2/144 * (log_2 log_2 n - 3)`.
- Chapter 5 explicitly says the circuit theorem does **not** treat circuits with division.
- Lemma 4.1 uses a generic fibre with `e^k` distinct points, one quadratic equation per multiplication gate, and the affine Bézout inequality to obtain `e^k <= 2^q`.
- Lemma 4.2 constructs the projected gradient map used by Proposition 4.3.
- Proposition 7.1 and the proof of Theorem 1.1 establish `k >= n^2/48` and `log_2(d-1) >= log_2 log_2 n - 3`, producing the explicit denominator `144`.

The new proof uses the permanent-specific construction unchanged. Its only new work is the valid-division transfer.

## 2. Differentiation with division

**Walter Baur and Volker Strassen, “The complexity of partial derivatives,” _Theoretical Computer Science_ 22 (1983), 317–330.**

Primary-source scan used: `https://web.vu.lt/mif/s.jukna/tropical/Baur-Strassen.pdf`

At the start of the paper, `L` is defined as nonscalar multiplication/division complexity in a rational-function field, with additions/subtractions and scalar multiplications free. The main inequality is

`L(f, df/dx_1, ..., df/dx_n) <= 3 L(f)`.

The proof explicitly permits each nonlinear step to be either multiplication or division. Theorem 2 separately gives the refined operation counts and again assigns a factor of three to the nonscalar multiplication/division operations.

Therefore the factor `3s` used by the new transfer theorem is within the original Baur–Strassen model; no division-elimination theorem is invoked.

## 3. Affine Bézout dependency

**Joos Heintz, “Definability and fast quantifier elimination in algebraically closed fields,” _Theoretical Computer Science_ 24 (1983), 239–277.**

Primary publisher record: `https://www.sciencedirect.com/science/article/pii/0304397583900026`

The publisher abstract identifies the paper’s affine Bézout inequality for algebraic-complexity applications. More importantly for the exact formulation used here, the current OpenAI Chapter 5, Lemma 4.1 explicitly invokes Heintz’s affine Bézout inequality to bound the number of **isolated solutions** of `q` quadratic gate equations plus affine output equations by `2^q`.

The valid-division proof uses the same polynomial-system bound. Division changes only the graph equation from `v-AB=0` to `Bv-A=0`, which remains quadratic. Regular circuit points lift to isolated solutions; extraneous components on `B=0` do not invalidate an upper bound on isolated solutions.

## 4. Dimension of the pole-image dependency

**The Stacks Project, Lemma 33.20.4 (Tag 0B2L).**

Primary source: `https://stacks.math.columbia.edu/tag/0B2L`

For an irreducible source `X` and a morphism `f`, if `Z` is the closure of `f(X)`, the lemma writes

`dim(X) - dim(Z) = trdeg_{k(f(eta))} k(eta) >= 0`.

Thus `dim closure(f(X)) <= dim X`. Applied componentwise to the pole hypersurface gives

`dim closure(G_t(Z_t)) <= dim Z_t <= k-1`.

Hence the pole image is contained in a proper algebraic subset of `C^k` and cannot contain a Euclidean neighborhood of the target.

## 5. Root persistence dependency

The proof uses only the standard holomorphic implicit/inverse-function theorem: if the Jacobian of `G_0(u)-a_0` with respect to `u` is invertible at a solution, then that solution continues uniquely as a holomorphic local branch for small parameter changes. Because the initial fibre contains finitely many distinct simple roots, disjoint neighborhoods can be chosen and intersected to preserve all branches simultaneously.

No quantitative estimate is required.

## 6. Novelty boundary

A fresh search on 2026-08-14 checked the current OpenAI paper, arXiv results for 2026 arithmetic-circuit lower bounds, and the 2026 ECCC report index for a permanent lower bound covering valid division. No matching theorem was located.

The strongest audited primary-source boundary is the current OpenAI paper itself: it explicitly says its new permanent-specific `Omega(N log log N)` circuit bound is for division-free circuits and “does not ... treat circuits with division.”

This is a **search audit**, not a claim that unpublished or unindexed work cannot exist.
