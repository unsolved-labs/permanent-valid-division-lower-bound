# A valid-division transfer for the permanent circuit lower bound

## Theorem

Let `n >= 2^16`. Every valid arithmetic circuit over `C` computing the `n x n` permanent has nonscalar multiplication/division complexity

\[
s \ge \frac{n^2}{144}\bigl(\log_2\log_2 n-3\bigr).
\]

Here a division gate is valid when its divisor is a nonzero element of the rational-function field in the input variables. Additions, subtractions, and scalar operations are free in the nonscalar model. Consequently the same expression lower-bounds the ordinary total gate count.

The proof combines the permanent-specific polynomial map constructed in OpenAI (2026, Chapter 5) with the following transfer theorem.

---

## Lemma 1 — rational gate-fibre bound

Let `G:C^k -> C^k` be polynomial. Suppose a valid rational straight-line circuit `Gamma` computes `G` with `q` nonscalar multiplication/division gates. Let `U_Gamma` be the set of points where every syntactic division in `Gamma` is defined and has nonzero divisor. If, for some target `a`, the fibre `G^{-1}(a) ∩ U_Gamma` contains `M` distinct isolated points, then

\[
M\le 2^q.
\]

### Proof

Topologically order the nonlinear gates and introduce one variable `v_j` for the value at the `j`th nonlinear gate. Collapse all intervening additions, subtractions, and scalar operations. The two operands at gate `j` are therefore affine functions `A_j(u,v_{<j})` and `B_j(u,v_{<j})`.

For a multiplication gate impose

\[
v_j-A_jB_j=0,
\]

and for a division gate impose

\[
B_jv_j-A_j=0.
\]

Each equation has total degree at most two. Each circuit output is affine in the original inputs and nonlinear-gate outputs, so setting the `k` outputs equal to `a` adds `k` equations of degree at most one. Thus there are `q+k` polynomial equations in `q+k` variables with degree product at most `2^q`.

Take a point `u*` in the stated fibre and evaluate the circuit there. It has a unique lift `(u*,v*)`. At that lift every division operand `B_j` is nonzero. In a sufficiently small neighborhood, the gate equations can therefore be solved successively: multiplication gives `v_j=A_jB_j`, and division gives `v_j=A_j/B_j`. Locally the gate-equation variety is exactly the graph of the circuit evaluation over the equation `G(u)=a`. Hence an isolated regular fibre point lifts to an isolated solution of the polynomial system.

The affine Bézout inequality, in the isolated-solution form used in OpenAI Chapter 5, Lemma 4.1, bounds the number of isolated solutions by the product of equation degrees, at most `2^q`. The `M` lifted regular points are among those isolated solutions. Therefore `M <= 2^q`.

Extraneous solutions or positive-dimensional components lying on zero-divisor loci only add to the polynomial system; they do not remove the `M` regular isolated solutions and do not invalidate the isolated-solution Bézout bound. ∎

---

## Lemma 2 — pole-avoiding transfer

Let `f in C[x_1,...,x_N]`. Suppose there are linear maps

\[
B:C^k\to C^N,\qquad R:C^N\to C^k,
\]

a vector `c_0 in C^N`, and a target `a_0 in C^k` such that

\[
G_0(u)=R\nabla f(Bu+c_0)
\]

has `M` distinct simple solutions to `G_0(u)=a_0`.

If `f` is computed by a valid arithmetic circuit of nonscalar multiplication/division complexity `s`, then

\[
M\le 2^{3s}.
\]

### Proof

By Baur–Strassen in the rational-function model, `f` and all coordinates of `∇f` admit a valid rational circuit `Gamma` with at most `3s` nonscalar multiplication/division gates.

For every syntactic intermediate rational function of `Gamma`, choose its reduced numerator and denominator in `C[x_1,...,x_N]`. In addition, for every division gate record the reduced numerator of the rational function used as its divisor. Validity of `Gamma` makes every recorded polynomial nonzero. Let `P` be this finite set of nonzero polynomials.

For a translation vector `t in C^N`, put

\[
\lambda_t(u)=Bu+c_0+t.
\]

For `p in P` let

\[
E_p=\{t: p(Bu+c_0+t)\equiv0\text{ as a polynomial in }u\}.
\]

Writing `p(Bu+c_0+t)` as a polynomial in `u`, each coefficient is polynomial in `t`, so `E_p` is Zariski closed. It is proper: choose `x` with `p(x) != 0` and take `t=x-c_0`; then the restricted polynomial is already nonzero at `u=0`.

The finite union of the `E_p` is therefore a proper Zariski-closed subset of `C^N`. Its complement is Euclidean dense. We may consequently choose `t` arbitrarily close to zero while avoiding every `E_p`.

Now define

\[
G_t(u)=R\nabla f(Bu+c_0+t).
\]

Each of the `M` solutions of `G_0(u)=a_0` is simple, so its `u`-Jacobian is invertible. By the holomorphic implicit-function theorem, after restricting `t` to a sufficiently small neighborhood of zero, all `M` roots persist as distinct simple local branches. Choose the preceding pole-avoiding `t` inside this neighborhood.

Because no recorded numerator or denominator restricts identically to zero, the specialized circuit is a valid rational circuit. Let `Q_t(u)` be the product of all specialized reduced denominators and all specialized reduced numerators of division operands. Every factor is a nonzero polynomial, so `Q_t` is nonzero. Set

\[
U_t=D(Q_t),\qquad Z_t=V(Q_t).
\]

On `U_t` every syntactic gate of the specialized circuit is regular, and the circuit computes the specialized gradient. If `Z_t` is nonempty, it is a hypersurface and has dimension at most `k-1` (if `Q_t` is constant, `Z_t` is empty and the next step is trivial).

For the fixed small `t`, choose pairwise disjoint neighborhoods around the `M` continued simple roots. The inverse-function theorem gives a common Euclidean neighborhood `O` of `a_0` such that every `a in O` has one simple preimage in each neighborhood, hence at least `M` distinct simple preimages under `G_t`.

For every irreducible component `Z_i` of `Z_t`, the dimension-of-image theorem gives

\[
\dim\overline{G_t(Z_i)}\le\dim Z_i\le k-1.
\]

Thus

\[
\dim\overline{G_t(Z_t)}\le k-1,
\]

so this closure is a proper algebraic subset of `C^k` and has empty Euclidean interior. Choose

\[
a\in O\setminus\overline{G_t(Z_t)}.
\]

None of the `M` local preimages of `a` lies in `Z_t`; all lie in the circuit regularity domain `U_t`.

Precomposing the gradient circuit by the affine map `lambda_t` and postcomposing by `R` costs no nonscalar operations. It therefore computes `G_t` with at most `3s` nonlinear gates. Lemma 1 now gives

\[
M\le2^{3s}.
\]

∎

---

## Application to the permanent

OpenAI Chapter 5 constructs, for its parameters `d,m,k`, an affine specialization

\[
P(x)=\gamma\,\operatorname{per}_n(M_0x+c_0)
\]

with `gamma != 0`, together with linear maps `W:C^k -> C^m` and `A:C^m -> C^k`, such that

\[
F_0(u)=A\nabla P(Wu)
\]

is homogeneous of degree `d-1` and `F_0^{-1}(0)={0}`. By OpenAI Lemma 4.1, a generic fibre of `F_0` contains exactly

\[
(d-1)^k
\]

distinct simple points.

The chain rule gives

\[
F_0(u)=\gamma A M_0^{\mathsf T}\nabla\operatorname{per}_n(M_0Wu+c_0).
\]

Apply Lemma 2 with

\[
B=M_0W,\qquad R=\gamma A M_0^{\mathsf T},\qquad f=\operatorname{per}_n,
\]

and `M=(d-1)^k`. If `s` is the nonscalar multiplication/division complexity of a valid circuit for the permanent, then

\[
(d-1)^k\le2^{3s},
\]

hence

\[
s\ge\frac{k\log_2(d-1)}3.
\]

OpenAI Proposition 7.1 and the proof of its Theorem 1.1 use, for `n>=2^16`,

\[
d=\left\lfloor\frac{\log_2 n}{4}\right\rfloor
\]

and prove

\[
k\ge\frac{n^2}{48},\qquad
\log_2(d-1)\ge\log_2\log_2 n-3.
\]

Therefore

\[
s\ge
\frac{1}{3}\frac{n^2}{48}
\bigl(\log_2\log_2n-3\bigr)
=
\frac{n^2}{144}
\bigl(\log_2\log_2n-3\bigr).
\]

This proves the theorem. ∎

## Scope

The theorem is over `C` and uses the same valid-division convention as the rational-function Baur–Strassen model: divisors must be nonzero rational functions, not globally nonvanishing functions on every numerical input. The result does not address determinant circuits and does not claim optimality of the constant `1/144`.
