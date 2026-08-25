Then

$$
\begin{array}{l} \gamma_ {n} = \sum_ {r = n} ^ {\infty} \delta_ {r} U _ {r - n} V _ {r + n} \\ = \sum_ {r = n} ^ {\infty} \frac {(\rho_ {1} ; q) _ {r} (\rho_ {2} ; q) _ {r} (q ^ {- N} ; q) _ {r} q ^ {r}}{(\rho_ {1} \rho_ {2} q ^ {- N} / a ; q) _ {r} (q ; q) _ {r - n} (a q ; q) _ {r + n}} \\ = \sum_ {r = 0} ^ {\infty} \frac {(\rho_ {1} ; q) _ {r + n} (\rho_ {2} ; q) _ {r + n} (q ^ {- N} ; q) _ {r + n} q ^ {r + n}}{(\rho_ {1} \rho_ {2} q ^ {- N} / a ; q) _ {r + n} (q ; q) _ {r} (a q ; q) _ {r + 2 n}} \\ = \frac {(\rho_ {1} ; q) _ {n} (\rho_ {2} ; q) _ {n} (q ^ {- N} ; q) _ {n} q ^ {n}}{(\rho_ {1} \rho_ {2} q ^ {- N} / a ; q) _ {n} (a q ; q) _ {2 n}} _ {3} \phi_ {2} \binom{\rho_ {1} q ^ {n}, \rho_ {2} q ^ {n}, q ^ {- (N - n)}; q, q}{\rho_ {1} \rho_ {2} q ^ {n - N} / a, a q ^ {2 n + 1}} \\ = \frac {(\rho_ {1} ; q) _ {n} (\rho_ {2} ; q) _ {n} (q ^ {- N} ; q) _ {n} q ^ {n} (a q ^ {n + 1} / \rho_ {1} ; q) _ {N - n} (a q ^ {n + 1} / \rho_ {2} ; q) _ {N - n}}{(\rho_ {1} \rho_ {2} q ^ {- N} / a ; q) _ {n} (a q ; q) _ {2 n} (a q ^ {2 n + 1} ; q) _ {N - n} (a q / \rho_ {1} \rho_ {2} ; q) _ {N - n}} \\ = \frac {(a q / \rho_ {1} ; q) _ {N} (a q / \rho_ {2} ; q) _ {N}}{(a q ; q) _ {N} (a q / \rho_ {1} \rho_ {2} ; q) _ {N}} \frac {(- 1) ^ {n} (\rho_ {1} ; q) _ {n} (\rho_ {2} ; q) _ {n} (q ^ {- N} ; q) _ {n}}{(a q / \rho_ {1} ; q) _ {n} (a q / \rho_ {2} ; q) _ {n} (a q ^ {N + 1} ; q) _ {n}} \\ \times (a q / \rho_ {1} \rho_ {2}) ^ {n} q ^ {n N - n (n - 1) / 2}. \end{array}
$$

We now turn to the proof of (12.2.3). Note that

$$
\begin{array}{l} \sum_ {r = 0} ^ {N} \frac {\alpha_ {r} ^ {\prime}}{(q ; q) _ {N - r} (a q ; q) _ {N + r}} \\ = \sum_ {r = 0} ^ {N} \frac {(\rho_ {1} ; q) _ {r} (\rho_ {2} ; q) _ {r} (a q / \rho_ {1} \rho_ {2}) ^ {r} \alpha_ {r}}{(a q / \rho_ {1} ; q) _ {r} (a q / \rho_ {2} ; q) _ {r} (q ; q) _ {N - r} (a q ; q) _ {N + r}} \\ = \sum_ {r = 0} ^ {N} \frac {(- 1) ^ {r} (\rho_ {1} ; q) _ {r} (\rho_ {2} ; q) _ {r} (q ^ {- N} ; q) _ {r}}{(a q / \rho_ {1} ; q) _ {r} (a q / \rho_ {2} ; q) _ {r} (a q ; q) _ {N + r}} (a q / \rho_ {1} \rho_ {2}) ^ {r} \cdot q ^ {r N - r (r - 1) / 2} \alpha_ {r} \\ = \frac {(a q / \rho_ {1} \rho_ {2} ; q) _ {N}}{(a q / \rho_ {1} ; q) _ {N} (a q / \rho_ {2} ; q) _ {N}} \sum_ {r = 0} ^ {N} \gamma_ {r} \alpha_ {r} \\ = \frac {(a q / \rho_ {1} \rho_ {2} ; q) _ {N}}{(a q / \rho_ {1} ; q) _ {N} (a q / \rho_ {2} ; q) _ {N}} \sum_ {r = 0} ^ {N} \beta_ {r} \delta_ {r} \quad \text {(by Lemma 12.2.2)} \\ = \frac {(a q / \rho_ {1} \rho_ {2} ; q) _ {N}}{(a q / \rho_ {1} ; q) _ {N} (a q / \rho_ {2} ; q) _ {N}} \sum_ {r = 0} ^ {N} \frac {(\rho_ {1} ; q) _ {r} (\rho_ {2} ; q) _ {r} (q ^ {- N} ; q) _ {r} q ^ {r} \beta_ {r}}{(\rho_ {1} \rho_ {2} q ^ {- N} / a ; q) _ {r}} \\ = \beta_ {N} ^ {\prime}, \end{array}
$$

where the last equation follows after an algebraic simplification that produces the expression given in (12.2.4). The theorem is proved.

Remark 12.2.1 The Weak Bailey Lemma (Lemma 12.2.1) follows from the full Bailey Lemma by letting $n, \rho_{1}, \rho_{2} \to \infty$ .

We call $(\alpha_{n}, \beta_{n})$ a Bailey pair if they are related as in Bailey's lemma. The power of the full Bailey Lemma is that, given a Bailey pair $(\alpha_{n}, \beta_{n})$ a new Bailey pair is produced. Consequently, from one such pair one can construct an infinite sequence $(\alpha_{n}, \beta_{n}) \to (\alpha_{n}^{\prime}, \beta_{n}^{\prime}) \to (\alpha_{n}^{\prime\prime}, \beta_{n}^{\prime\prime}) \to \cdots$ of Bailey pairs by successive application of Bailey's Lemma. This sequence is called a Bailey chain. The simplest conceivable chain starts with

$$
\beta_ {n} = \delta_ {n, 0} = \left\{ \begin{array}{l l} 1 & \text { if } n = 0, \\ 0 & \text { if } n > 0. \end{array} \right.\tag{12.2.5}
$$

It is an simple exercise to show that the corresponding $\alpha_{n}$ is

$$
\alpha_ {n} = \frac {(1 - a q ^ {2 n}) (a ; q) _ {n} (- 1) ^ {n} q ^ {\binom {n} {2}}}{(1 - a) (q ; q) _ {n}}.\tag{12.2.6}
$$

Remark 12.2.2 The fact that $(\alpha_{n}, \beta_{n})$ is a Bailey pair follows immediately from a formula of Agarwal [1953],

$$
\sum_ {j = 0} ^ {M} \frac {(1 - a q ^ {2 j}) (q ^ {- n} ; q) _ {j} (a ; q) _ {j} q ^ {n j}}{(1 - a) (a q ^ {n + 1} ; q) _ {j} (q ; q) _ {j}} = \frac {(a q ; q) _ {M} q ^ {n M} (q ^ {1 - n} ; q) _ {M}}{(q ; q) _ {M} (a q ^ {n + 1} ; q) _ {M}},\tag{12.2.7}
$$

a result that can be proved directly by induction on $M$ . Another way is to use the "inversion" formula: If $\beta_{n}$ is given by (12.2.1), then

$$
\alpha_ {n} = (1 - a q ^ {2 n}) \sum_ {j = 0} ^ {n} \frac {(a q ; q) _ {n + j - 1} (- 1) ^ {n - j} q ^ {\binom {n - j} {2}} \beta_ {j}}{(q ; q) _ {n - j}}.\tag{12.2.8}
$$

## 12.3 Watson's Transformation Formula

In this section we use the Bailey chain to derive some important formulas. In particular, we obtain a q-analog of Whipple's transformation due to Watson [1929]. This transforms a terminating very well poised $_{8}\phi_{7}$ to a terminating balanced $_{4}\phi_{3}$ . The phrase “very well poised” is defined below.

We start with a simpler result. Recall that $(\alpha_{n}, \beta_{n})$ in (12.2.5) and (12.2.6) form a Bailey pair. By Theorem 12.2.3, the next pair in the chain, namely $(\alpha_{n}^{\prime}, \beta_{n}^{\prime})$ , is given by

$$
\begin{array}{l} \beta_ {n} ^ {\prime} = \frac {(a q / \rho_ {1} \rho_ {2} ; q) _ {n}}{(q ; q) _ {n} (a q / \rho_ {1} ; q) _ {n} (a q / \rho_ {2} ; q) _ {n}}, \\ \alpha_ {n} ^ {\prime} = \frac {(\rho_ {1} ; q) _ {n} (\rho_ {2} ; q) _ {n} (a q / \rho_ {1} \rho_ {2}) ^ {n} (1 - a q ^ {2 n}) (a ; q) _ {n} (- 1) ^ {n} q ^ {\binom {n} {2}}}{(a q / \rho_ {1} ; q) _ {n} (a q / \rho_ {2} ; q) _ {n} (1 - a) (q ; q) _ {n}}. \end{array}
$$

And the relation

$$
\beta_ {n} ^ {\prime} = \sum_ {r = 0} ^ {n} \frac {\alpha_ {r} ^ {\prime}}{(q ; q) _ {n - r} (a q ; q) _ {n + r}},
$$

when written out in full, is

$$
\begin{array}{l} \frac {(a q / \rho_ {1} \rho_ {2}) _ {n}}{(q) _ {n} (a q / \rho_ {1}) _ {n} (a q / \rho_ {2}) _ {n}} \\ = \sum_ {r = 0} ^ {n} \frac {\left(\rho_ {1}\right) _ {r} \left(\rho_ {2}\right) _ {r} \left(a q / \rho_ {1} \rho_ {2}\right) ^ {r} \left(1 - a q ^ {2 r}\right) (a) _ {r} (- 1) ^ {r} q ^ {\binom {r} {2}}}{\left(q\right) _ {n - r} (a q) _ {n + r} \left(a q / \rho_ {1}\right) _ {r} \left(a q / \rho_ {2}\right) _ {r} (1 - a) (q) _ {r}}, \end{array}\tag{12.3.1}
$$

where $(x)_r = (x;q)_r$ . Note that

$$
\begin{array}{c} \frac {1 - a q ^ {2 r}}{1 - a} = \frac {(1 - \sqrt {a} q ^ {r}) (1 + \sqrt {a} q ^ {r})}{(1 - \sqrt {a}) (1 + \sqrt {a})} = \frac {(\sqrt {a} q ; q) _ {r} (- \sqrt {a} q ; q) _ {r}}{(\sqrt {a} , q) _ {r} (- \sqrt {a} ; q) _ {r}}, \\ (q) _ {n - r} = \frac {(- 1) ^ {r} (q) _ {n}}{(q ^ {n}) _ {r} q ^ {r (2 n - r + 1) / 2}}, \end{array}
$$

and

$$
(a q) _ {n + r} = (a q) _ {n} (a q ^ {n + 1}) _ {r}.
$$

Thus (12.3.1) is equivalent to the formula

$$
{ } _ { 6 } \phi _ { 5 } \left( \begin{array} { c } a , q \sqrt { a } , - q \sqrt { a } , \rho _ { 1 } , \rho _ { 2 } , q ^ { - n } \\ \sqrt { a } , - \sqrt { a } , a q / \rho _ { 1 } , a q / \rho _ { 2 } , a q ^ { n + 1 } \end{array} ; q , \frac { a q ^ { n + 1 } } { \rho _ { 1 } \rho _ { 2 } } \right) = \frac { ( a q ) _ { n } ( a q / \rho _ { 1 } \rho _ { 2 } ) _ { n } } { ( a q / \rho _ { 1 } ) _ { n } ( a q / \rho _ { 2 } ) _ { n } } .\tag{12.3.2}
$$

The $_{6}\phi_{5}$ is well poised because the product of a numerator parameter with the corresponding denominator parameter is aq. Additionally, the presence of the factor $(1 - aq^{2r})/(1 - a)$ now makes it a very well poised $_{6}\phi_{5}$ .

Watson's transformation is obtained by moving up the Bailey chain to $(\alpha_{n}^{\prime \prime},\beta_{n}^{\prime \prime})$ . The relation

$$
\sum_ {r = 0} ^ {n} \frac {\alpha_ {r} ^ {\prime \prime}}{(q) _ {n - r} (a q) _ {n + r}} = \beta_ {n} ^ {\prime \prime}
$$

is seen to be equivalent to

$$
\begin{array}{l} \sum_ {r = 0} ^ {n} \frac {\left(\lambda_ {1}\right) _ {r} \left(\lambda_ {2}\right) _ {r} \left(a q / \lambda_ {1} \lambda_ {2}\right) ^ {r} \left(\rho_ {1}\right) _ {r} \left(\rho_ {2}\right) _ {r} \left(a q / \rho_ {1} \rho_ {2}\right) ^ {r} \left(1 - a q ^ {2 r}\right) \left(a\right) _ {r} (- 1) ^ {r} q ^ {\binom {r} {2}})}{\left(a q / \lambda_ {q}\right) _ {r} \left(a q / \lambda_ {2}\right) _ {r} \left(a q / \rho_ {1}\right) _ {r} \left(a q / \rho_ {2}\right) _ {r} (1 - a) (q) _ {r} (q) _ {n - r} (a q) _ {n + r}} \\ = \sum_ {j \geq 0} \frac {\left(\lambda_ {1}\right) _ {j} \left(\lambda_ {2}\right) _ {j} \left(a q / \lambda_ {1} \lambda_ {2}\right) _ {n - j} \left(a q / \lambda_ {1} \lambda_ {2}\right) ^ {j} \left(a q / \rho_ {1} \rho_ {2}\right) _ {j}}{\left(q\right) _ {n - j} \left(a q / \lambda_ {1}\right) _ {j} \left(a q / \lambda_ {2}\right) _ {j} (q) _ {j} \left(a q / \rho_ {1}\right) _ {j} \left(a q / \rho_ {2}\right) _ {j}}. \end{array} \tag {12.3}\tag{12.3.3}
$$

By the formulas used to obtain (12.3.2), it is easy to show that (12.3.3) can be written as follows:

$$
\begin{array}{l} _ {8} \phi_ {7} \binom {a, q \sqrt {a}, - q \sqrt {a}, \lambda_ {1}, \lambda_ {2}, \rho_ {1}, \rho_ {2}, q ^ {- n}} {\sqrt {a}, - \sqrt {a}, a q / \lambda_ {1}, a q / \lambda_ {2}, a q / \rho_ {1}, a q / \rho_ {2}, a q ^ {n + 1}; q, \frac {a ^ {2} q ^ {n + 2}}{\lambda_ {1} \lambda_ {2} \rho_ {1} \rho_ {2}}} \\ = \frac {(a q) _ {n} (a q / \rho_ {1} \rho_ {2}) _ {n}}{(a q / \rho_ {1}) _ {n} (a q / \rho_ {2}) _ {n}} _ {4} \phi_ {3} \binom {a q / \lambda_ {1} \lambda_ {2}, \rho_ {1}, \rho_ {2}, q ^ {- n}} {a q / \lambda_ {1}, a q / \lambda_ {2}, \rho_ {1} \rho_ {2} q ^ {- n} / a}; q, q). \end{array} \tag {1}\tag{12.3.4}
$$

This is Watson's formula. When $aq / \lambda_1\lambda_2 = \rho_1\rho_2q^{-n} / a$ , the $_4\phi_3$ becomes a balanced $_3\phi_2$ , which can be summed by the $q$ -Pfaff–Saalschütz formula (10.11.3). The result in this case is the $q$ -analog of Dougall's formula due to Jackson [1921]:

$$
\begin{array}{l} _ {8} \phi_ {7} \binom {a, q \sqrt {a}, - q \sqrt {a}, \lambda_ {1}, \lambda_ {2}, \rho_ {1}, \rho_ {2}, q ^ {- n}} {\sqrt {a}, - \sqrt {a}, a q / \lambda_ {1}, a q / \lambda_ {2}, a q / \rho_ {1}, a q / \rho_ {2}, a q ^ {n + 1}; q, q} \\ = \frac {(a q) _ {n} (a q / \rho_ {1} \rho_ {2}) _ {n} (a q / \lambda_ {1} \rho_ {1}) _ {n} (a q / \lambda_ {1} \lambda_ {2}) _ {n}}{(a q / \lambda_ {1}) _ {n} (a q / \lambda_ {2}) _ {n} (a q / \rho_ {1}) _ {n} (a q / \lambda_ {1} \lambda_ {2} \rho_ {1}) _ {n}}, \quad \text {when} a ^ {2} q = \lambda_ {1} \lambda_ {2} \rho_ {1} \rho_ {2} q ^ {- n}. \end{array}\tag{12.3.5}
$$

Let $n\to \infty$ in (12.3.5). This gives

$$
\begin{array}{c} _ {6} \phi_ {5} \left( \begin{array}{c} a, q \sqrt {a}, - q \sqrt {a}, \lambda_ {1}, \lambda_ {2}, \rho_ {1} \\ \sqrt {a}, - \sqrt {a}, a q / \lambda_ {1}, a q / \lambda_ {2}, a q / \rho_ {1} \end{array} ; q, \frac {a q}{\lambda_ {1} \lambda_ {2} \rho_ {1}}\right) \\ = \frac {(a q) _ {\infty} (a q / \rho_ {1} \rho_ {2}) _ {\infty} (a q / \lambda_ {1} \rho_ {1}) _ {\infty} (a q / \lambda_ {1} \lambda_ {2}) _ {\infty}}{(a q / \lambda_ {1}) _ {\infty} (a q / \lambda_ {2}) _ {\infty} (a q / \rho_ {1}) _ {\infty} (a q / \lambda_ {1} \lambda_ {2} \rho_ {1}) _ {\infty}}. \end{array}\tag{12.3.6}
$$

This is a nonterminating form of (12.3.2).

Now observe that the $_{8}\phi_{7}$ in (12.3.4) is symmetric in $\lambda_{1}, \lambda_{2}, \rho_{1}, \rho_{2}$ and hence

$$
\begin{array}{l} \frac {(a q / \rho_ {1} \rho_ {2}) _ {n}}{(a q / \rho_ {1}) _ {n} (a q / \rho_ {2}) _ {n}} _ {4} \phi_ {3} \binom {a q / \lambda_ {1} \lambda_ {2}, \rho_ {1}, \rho_ {2}, q ^ {- n}} {a q / \lambda_ {1}, a q / \lambda_ {2}, \rho_ {1} \rho_ {2} q ^ {- n} / a}; q, q \\ = \frac {(a q / \lambda_ {1} \lambda_ {2}) _ {n}}{(a q / \lambda_ {1}) _ {n} (a q / \lambda_ {2}) _ {n}} _ {4} \phi_ {3} \binom {a q / \rho_ {1} \rho_ {2}, \lambda_ {1}, \lambda_ {2}, q ^ {- n}} {a q / \rho_ {1}, a q / \rho_ {2}, \lambda_ {1} \lambda_ {2} q ^ {- n} / a}; q, q. \end{array}\tag{12.3.7}
$$

A $q$ -analog of Dixon's formula for a well-poised ${}_{3}F_{2}$ is obtained by setting $\rho_{1} = \sqrt{a}$ in (12.3.6):

$$
\begin{array}{l} _ {4} \phi_ {3} \left( \begin{array}{c} a, - q \sqrt {a}, \lambda_ {1}, \lambda_ {2} \\ - \sqrt {a}, a q / \lambda_ {1}, a q / \lambda_ {2} \end{array} ; q, \frac {q \sqrt {a}}{\lambda_ {1} \lambda_ {2}}\right) \\ = \frac {(a q) _ {\infty} (a q / \lambda_ {1} \lambda_ {2}) _ {\infty} (q \sqrt {a} / \lambda_ {1}) _ {\infty} (q \sqrt {a} / \lambda_ {2}) _ {\infty}}{(a q / \lambda_ {1}) _ {\infty} (a q / \lambda_ {2}) _ {\infty} (q \sqrt {a}) _ {\infty} (q \sqrt {a} / \lambda_ {1} \lambda_ {2}) _ {\infty}}. \end{array}
$$

The two Rogers–Ramanujan formulas can also be derived from Watson's transformation (12.3.4). Let $\lambda_{1}, \lambda_{2}, \rho_{1}, \rho_{2} \to \infty$ to get

$$
\begin{array}{l} \sum_ {j = 0} ^ {n} \frac {(a ; q) _ {j} (1 - a q ^ {2 j}) (q ^ {- n} ; q) _ {j} (a ^ {2} q ^ {n + 2 j}) ^ {j}}{(q ; q) _ {j} (1 - a) (a q ^ {n + 1} ; q) _ {j}} \\ = (a q; q) _ {n} \sum_ {j = 0} ^ {n} \frac {(- 1) ^ {j} (q ^ {- n} ; q) _ {j}}{(q ; q) _ {j}} (a q ^ {n + 1 + (j - 1) / 2}) ^ {j}. \end{array}
$$

Now let $n \to \infty$ and apply the dominated convergence theorem. After simplification, the result is

$$
1 + \sum_ {j = 1} ^ {\infty} \frac {(a q ; q) _ {j - 1} (1 - a q ^ {2 j})}{(q ; q) _ {j}} (- 1) ^ {j} a ^ {2 j} q ^ {j (5 j - 1) / 2} = (a q; q) _ {\infty} \sum_ {j = 0} ^ {\infty} \frac {a ^ {j} q ^ {j ^ {2}}}{(q ; q) _ {J}}.
$$

For $a = 1$ , this is the first Rogers-Ramanujan identity and for $a = q$ it is the second one.

If one wants to generalize a q-series identity that has quadratic powers in it, it is natural to try to replace each $q^{\binom{k}{2}}$ with $(a;q)_{k}$ times something else that will give $q^{\binom{k}{2}}$ using

$$
\lim _ {a \to \infty} (a; q) _ {k} / (- a) ^ {k} = q ^ {\binom {k} {2}}.
$$

Since there are two Rogers–Ramanujan identities and five factors $q^{(\frac{k}{2})}$ , the minimum extension of the Rogers–Ramanujan identities of this type should have six free parameters. Formula (12.3.4) is this extension.

## 12.4 Other Applications

The summation formula for a very well poised $_{6}\phi_{5}$ and Watson's transformation were fairly straightforward consequences of Bailey's Lemma. Further interesting results are possible by starting with the Bailey pair (12.2.5) and (12.2.6) and moving further along the chain. For example,

$$
\sum_{n_{1}\geq n_{2}\geq \dots \geq n_{k}\geq 0}\frac{q^{n_{1}^{2} + n_{2}^{2} + \cdots n_{k}^{2}}}{(q)_{n_{1} - n_{2}}(q)_{n_{2} - n_{3}}\cdots(q)_{n_{k - 1} - n_{k}}(q)_{n_{k}}}\\ = \prod_{\substack{n = 1\\ n\not\equiv 0,\pm (k + 1)(\mathrm{mod} 2k + 3)}}^{\infty}\frac{1}{1 - q^{n}}.
$$

This identity reduces to the first Rogers–Ramanujan identity when k = 1. As noted before, it can be proved by examining $(\alpha_{n}^{(k+1)}, \beta_{n}^{(k+1)})$ in the Bailey chain starting with the pair (12.2.5) and (12.2.6).

It should be stressed that this is not the only Bailey chain of interest. In a totally different context, another of Ramanujan's series,

$$
S (q) := \sum_ {n = 0} ^ {\infty} \frac {q ^ {\binom {n + 1} {2}}}{(- q ; q) _ {n}} =: \sum_ {n = 0} ^ {\infty} s _ {n} q ^ {n},
$$

was studied. The relevant Bailey pair is

$$
\beta_ {n} = \frac {(- q) ^ {n}}{(q ^ {2} ; q ^ {2}) _ {n}}
$$

and

$$
\alpha_ {n} = q ^ {n ^ {2} + n} \sum_ {j = - n} ^ {n} (- 1) ^ {j} q ^ {- j ^ {2}}.
$$

From

$$
\beta_ {n} ^ {\prime} = \sum_ {r = 0} ^ {n} \frac {\alpha_ {r} ^ {\prime}}{(q ; q) _ {n - r} (q ; q) _ {n + r}},
$$

we can deduce

$$
S(q) = \sum_{\substack{n\geq 0\\ |j|\leq n}}(-1)^{n + j}q^{n(3n + 1) / 2 - j^{2}}(1 - q^{2n + 1}).
$$

From this result it can be shown that almost all $s_{n}$ equal zero and that for any integer M (positive, negative, or zero), there exist infinitely many n so that $s_{n} = M$ . For details, see Andrews, Dyson, and Hickerson [1988]. This paper also contains references to the work of Slater and Bressoud in Exercises 3, 4, and 5.

## Exercises

1. Obtain the second Rogers–Ramanujan identity (12.1.2) from the weak Bailey Lemma 12.2.1.

2. Prove Agarwal's formula (12.2.7), namely

$$
\sum_ {j = 0} ^ {M} \frac {(1 - a q ^ {2 j}) (q ^ {- n} ; q) _ {j} (a ; q) _ {m} q ^ {n j}}{(1 - a) (a q ^ {n + 1} ; q) _ {j} (q ; q) _ {j}} = \frac {(a q ; q) _ {M} q ^ {n M} (q ^ {1 - n} ; q) _ {M}}{(q ; q) _ {M} (a q ^ {n + 1} ; q) _ {M}}.
$$

3. Show that the $(\alpha_{n},\beta_{n})$ defined below is a Bailey pair with $a = 1$ :

$$
\alpha_ {m} = \left\{ \begin{array}{l l} - q ^ {6 n ^ {2} - 5 n + 1}, & m = 3 n - 1 > 0, \\ q ^ {6 n ^ {2} - n} + q ^ {6 n ^ {2} + n}, & m = 3 n > 0, \\ - q ^ {6 n ^ {2} + 5 n + 1}, & m = 3 n + 1 > 0, \\ 1, & m = 0, \end{array} \right.
$$

$$
\beta_ {n} = 1 / (q; q) _ {2 n}.\tag{Slater}
$$

4. Suppose

$$
\alpha_ {m} = \left\{ \begin{array}{l l} - q ^ {6 n ^ {2} - 2 n}, & m = 3 n - 1 > 0, \\ q ^ {6 n ^ {2} - 2 n} + q ^ {6 n ^ {2} + 2 n}, & m = 3 n > 0, \\ - q ^ {6 n ^ {2} + 2 n}, & m = 3 n + 1 > 0, \\ 1, & m = 0, \end{array} \right.
$$

and

$$
\beta_ {n} = q ^ {n} / (q; q) _ {2 n}.
$$

Prove that $(\alpha_{n},\beta_{n})$ is a Bailey pair with $a = 1$ .

(Slater)

5. Prove that

$$
\alpha_ {n} = \left\{ \begin{array}{l l} (- 1) ^ {m} (q ^ {m (5 m + 1) / 2} + q ^ {m (5 m - 1) / 2}), & n = 2 n, \\ 1, & n = 0, \\ 0, & n = \text {odd}, \end{array} \right.
$$

$$
\beta_ {n} = \frac {1}{(q ; q) _ {2 n}} \sum_ {j = 0} ^ {n} \left[ \begin{array}{c} n \\ j \end{array} \right] _ {q} q ^ {j ^ {2}}
$$

is a Bailey pair with $a = 1$ .

(Bressoud)

6. Apply (12.3.8), Exercises 10.37 and 10.39, and Jacobi's triple product formula to obtain the following six identities of Rogers:

(a)

$$
1 + \sum_ {n = 1} ^ {\infty} \frac {q ^ {n ^ {2}}}{(q ; q) _ {2 n}} = 1 / [ (q; q ^ {2}) _ {\infty} (q ^ {4}; q ^ {2 0}) _ {\infty} (q ^ {1 6}; q ^ {2 0}) _ {\infty} ].\tag{b}
$$

$$
1 + \sum_ {n = 1} ^ {\infty} \frac {q ^ {n ^ {2} + 2 n}}{(q ; q) _ {2 n + 1}} = 1 / [ (q; q ^ {2}) _ {\infty} (q ^ {8}; q ^ {2 0}) _ {\infty} (q ^ {1 2}; q ^ {2 0}) _ {\infty} ].\tag{c}
$$

$$
1 + \sum_ {n = 1} ^ {\infty} \frac {q ^ {n ^ {2} + n}}{(q ; q) _ {2 n}} = \prod_ {\substack {n = 1 \\ n \not \equiv \pm 1, \pm 8, \pm 9, 10 (\mathrm{mod} 20)}} ^ {\infty} (1 - q ^ {n}) ^ {- 1}.\tag{d}
$$

$$
1 + \sum_{n = 1}^{\infty}\frac{q^{n^{2} + n}}{(q;q)_{2n + 1}} = \prod_{\substack{n = 1\\ n\not\equiv \pm 3,\pm 4,\pm 7,10(\mathrm{mod} 20)}}^{\infty}(1 - q^{n})^{-1}.\tag{e}
$$

$$
(- q ^ {2}; q ^ {2}) _ {\infty} \sum_ {n = 0} ^ {\infty} \frac {q ^ {n ^ {2}}}{(q ^ {4} ; q ^ {4}) _ {n}} = \prod_ {n = 0} ^ {\infty} \frac {1}{(1 - q ^ {5 n + 1}) (1 - q ^ {5 n + 4})}.\tag{f}
$$

$$
(- q ^ {2}; q ^ {2}) _ {\infty} \sum_ {n = 0} ^ {\infty} \frac {q ^ {n ^ {2} + 2 n}}{(q ^ {4} ; q ^ {4}) _ {n}} = \prod_ {n = 0} ^ {\infty} \frac {1}{(1 - q ^ {5 n + 2}) (q - q ^ {5 n + 3})}.
$$

Whipple's $_7F_6$ transformation was obtained in Chapter 7 as a byproduct of the solution of the connection coefficient problem for Jacobi polynomials. There are several $q$ -analogs of the Jacobi polynomials. The next set of four problems shows how the little $q$ -Jacobi polynomials can be used to derive Watson's $_8\phi_7$ transformation. See Andrews and Askey [1977].

7. Define the little $q$ -Jacobi polynomials by

$$
p _ {n} (x; \alpha , \beta : q) = _ {2} \phi_ {1} \binom{q ^ {- n}, \alpha \beta q ^ {n + 1};}{\alpha q}; q, q x).
$$

(a) Show that

$$
\lim _ {q \rightarrow 1 ^ {-}} p _ {n} (x; q ^ {\alpha}, q ^ {\beta}: q) = P _ {n} ^ {(\alpha , \beta)} (1 - 2 x) / P _ {n} ^ {\alpha , \beta} (1).
$$

(b) Derive the orthogonality relation

$$
\begin{array}{l l} \sum_ {i = 0} ^ {\infty} \frac {\alpha^ {i} q ^ {i} (q ^ {i + 1} ; q) _ {\infty}}{(\beta q ^ {i + 1} ; q) _ {\infty}} p _ {n} (q ^ {i}; \alpha , \beta : q) p _ {m} (q ^ {i}; \alpha , \beta : q) \\ = \left\{ \begin{array}{l l} 0 & \text {if m\neq n}, \\ \frac {\alpha^ {n} q ^ {n} (q ; q) _ {\infty} (\alpha \beta q ^ {n + 1} ; q) _ {\infty} (q ; q) _ {n}}{(\beta q ^ {n + 1} ; q) _ {\infty} (\alpha q ; q) _ {\infty} (\alpha q ; q) _ {n} (1 - \alpha \beta q ^ {2 n + 1})} & \text {if m = n}. \end{array} \right. \end{array}
$$

[Hint: First obtain the following identity:

$$
\begin{array}{l l} \sum_ {i = 0} ^ {\infty} \frac {\alpha^ {i} q ^ {i} (q ^ {i + 1} ; q) _ {\infty}}{(\beta q ^ {i + 1} ; q) _ {\infty}} p _ {n} (q ^ {i}; \alpha , \beta : q) q ^ {i m} \\ = \left\{ \begin{array}{l l} 0 & \text { if } 0 \leq m <   n, \\ \frac {(- \alpha) ^ {n} q ^ {n (n + 1) / 2} (q ; q) _ {\infty} (\alpha \beta q ^ {2 n + 2} ; q) _ {\infty} (q ; q) _ {n}}{(\beta q ^ {n + 1} ; q) _ {\infty} (\alpha q ; q) _ {\infty}} & \text { if } m = n. ] \end{array} \right. \end{array}
$$

8. Suppose that

$$
p _ {n} (x; \gamma , \delta : q) = \sum_ {k = 0} ^ {n} a _ {k n} p _ {k} (x; \alpha , \beta : q).
$$

Show that

$$
\begin{array}{c} a _ {k n} = \frac {(- 1) ^ {k} q ^ {k (k + 1) / 2} (\gamma \delta q ^ {n + 1} ; q) _ {k} (q ^ {- n} ; q) _ {k} (\alpha q ; q) _ {k}}{(\alpha \beta q ^ {k + 1} ; q) _ {k} (q ; q) _ {k} (\gamma q ; q) _ {k}} \\ \cdot {} _ {3} \phi_ {2} \bigg ( \begin{array}{c} q ^ {- n + k}, \gamma \delta q ^ {n + k + 1}, \alpha q ^ {k + 1} \\ \gamma q ^ {k + 1}, \alpha \beta q ^ {2 k + 2} \end{array} ; q, q \bigg). \end{array}
$$

9. Note that the identity in Exercise 8 is a polynomial identity in $x$ . Deduce that with the same $a_{kn}$ , we have

$$
\begin{array}{l} _ {r + 2} \phi_ {r + 1} \binom{q ^ {- n}, \gamma \delta q ^ {n + 1}, a _ {1}, \ldots , a _ {r}}{\gamma q, b _ {1}, \ldots , b _ {r}}; q, q x \\ = \sum_ {k = 0} ^ {n} a  \phi_ {r + 1} \binom{q ^ {- k}, \alpha \beta q ^ {k + 1}, a _ {1}, \ldots , a _ {r}}{\alpha q, b _ {1}, \ldots b _ {r}}; q, q x. \end{array}
$$

10. Take $r = 2, \beta = \delta, a_1 = \alpha q, x = 1$ , and $b_2 = q^2 \alpha \delta a_2 / b_1$ in the previous exercise. Observe that the ${}_3\phi_2$ in $a_{kn}$ becomes balanced and may be computed

by (10.10.3). Deduce that

$$
\begin{array}{l} _ {4} \phi_ {3} \left( \begin{array}{c} q ^ {- n}, \gamma \delta q ^ {n + 1}, \alpha q, a _ {2} \\ \gamma q, b _ {1}, q ^ {2} \alpha \delta a _ {2} / b _ {1} \end{array} ; q, q\right) = \frac {\alpha^ {n} q ^ {n} (\delta q ; q) _ {n} (\gamma / \alpha ; q) _ {n}}{(\alpha \delta q ^ {2} ; q) _ {n} (\gamma q ; q) _ {n}} \\ \cdot {} _ {8} \phi_ {7} \left( \begin{array}{c} q ^ {- n}, q \sqrt {\alpha \delta q}, - q \sqrt {\alpha \delta q}, \alpha \delta q, \alpha q, \alpha \delta q ^ {2} / b _ {1}, \gamma \delta q ^ {n + 1}, b _ {1} / a _ {2} \\ \sqrt {\alpha \delta q}, - \sqrt {\alpha \delta q}, \delta q, b _ {1}, \alpha q ^ {- n + 1} / \gamma , \alpha \delta a _ {2} q ^ {2} / b _ {1}, \alpha \delta q ^ {n + 2} \end{array} ; q, a _ {2} / \gamma\right). \end{array}
$$

The standard form of Watson's transformation is obtained from this formula after proper identification.

11. The big q-Jacobi polynomials are defined by

$$
\begin{array}{l} P _ {n} ^ {(\alpha , \beta)} (x; c, d: q) = c ^ {n} \frac {q ^ {- (\alpha + 1) n} (q ^ {\alpha + 1} ; q) _ {n} (- q ^ {\alpha + 1} d / c ; q) _ {n}}{(q ; q) _ {n} (- q ; q) _ {n}} \\ \cdot {} _ {3} \phi_ {2} \left( \begin{array}{c} q ^ {- n}, q ^ {n + \alpha + \beta + 1}, x q ^ {\alpha + 1} d / c \\ q ^ {\alpha + 1}, - q ^ {\alpha + 1} d / c \end{array} ; q, q\right). \end{array}
$$

Prove that the orthogonality relation is

$$
\begin{array}{l} \int_ {- d} ^ {c} P _ {n} ^ {(\alpha , \beta)} (x; c, d: q) P _ {m} ^ {(\alpha , \beta)} (x: c, d: q) \frac {(q x / c ; q) _ {\infty} (- q x / d ; q) _ {\infty} d _ {q} x}{(q ^ {\alpha + 1} x / c ; q) _ {\infty} (- q ^ {\beta + 1} x / d ; q) _ {\infty}} \\ = \left\{ \begin{array}{l l} 0 & m \neq n, \\ \frac {(c d) ^ {n} q ^ {n (n - 1) / 2} (q ^ {\alpha + 1} ; q) _ {n} (q ^ {\beta + 1} ; q) _ {n}}{(q ^ {\alpha + \beta + 1} ; q) (q ; q) _ {n} (1 - q ^ {2 n + \alpha + \beta + 1})} \\ \cdot \frac {(- q ^ {\beta + 1} c / d ; q) _ {n} (- q ^ {\alpha + 1} d / c ; q) _ {n} (1 - q ^ {\alpha + \beta + 1}) M}{(- q ; q) _ {n} (- q ; q) _ {n}}, & m = n, \end{array} \right. \end{array}
$$

where

$$
M = \frac {c d (1 - q) (q ; q) _ {\infty} (q ^ {\alpha + \beta + 2} ; q) _ {\infty} (- d / c ; q) _ {\infty} (- c / d ; q) _ {\infty}}{(c + d) (q ^ {\alpha + 1} ; q) _ {\infty} (q ^ {\beta + 1} ; q) _ {\infty} (- q ^ {\alpha + 1} d / c ; q) _ {\infty} (- q ^ {\beta + 1} c / d ; q) _ {\infty}}.
$$

Note that when $c = d = 1$ , the weight function in the $q$ -integral tends to $(1 - x)^{\alpha}(1 + x)^{\beta}$ as $q \to 1^{-}$ .

12. A set of q-Laguerre polynomials is defined by

$$
L _ {n} ^ {(\alpha)} (x; q) = \frac {(q ^ {\alpha + 1} ; q) _ {n}}{(q ; q) _ {n}} \sum_ {k = 0} ^ {n} \frac {(q ^ {- n} ; q) _ {k} q ^ {\binom {k} {2}} (1 - q) ^ {k} (q ^ {n + \alpha + 1} x) ^ {k}}{(q ^ {\alpha + 1} ; q) _ {k} (q ; q) _ {k}}.
$$

(a) Replace $x$ with $-(1 - q)q^{-(\beta + 1)}x$ and let $\beta \to -\infty$ in the little $q$ -Jacobi polynomial of degree $n$ . Show that the result is

$$
\frac {(q ; q) _ {n}}{(q ^ {\alpha + 1} ; q) _ {n}} L _ {n} ^ {(\alpha)} (x; q).
$$

(b) Prove that $\lim_{q\to 1^{-}}L_n^{(\alpha)}(x;q) = L_n^\alpha (x)$ .

(c) Prove the discrete orthogonality relation

$$
\begin{array}{l} \sum_ {k = - \infty} ^ {\infty} L _ {n} ^ {(\alpha)} (q ^ {k}; q) L _ {m} ^ {(\alpha)} (q ^ {k}; q) \frac {q ^ {k \alpha + k}}{(- (1 - q) q ^ {k} ; q) _ {\infty}} \\ = \left\{ \begin{array}{l l} 0, & m \neq n, \\ \frac {(q ^ {\alpha + 1} ; q) _ {n}}{q ^ {n} (q ; q) _ {n}} \sum_ {k = - \infty} ^ {\infty} \frac {q ^ {k \alpha + k}}{(- (1 - q) q ^ {k} ; q) _ {\infty}} & m = n. \end{array} \right. \end{array}
$$

(Use Ramanujan's $_{1}\psi_{1}$ sum.)

(d) Prove the continuous orthogonality relation

$$
\begin{array}{l} \int_ {0} ^ {\infty} L _ {m} ^ {(\alpha)} (x; q) L _ {n} ^ {(\alpha)} (x; q) \frac {x ^ {\alpha}}{(- (1 - q) x ; q) _ {\infty}} d x \\ = \left\{ \begin{array}{l l} 0, & m \neq n, \\ \frac {\Gamma (\alpha + 1) \Gamma (- \alpha) (q ^ {n + 1} , q) _ {n}}{\Gamma_ {q} (- \alpha) (q ; q) _ {n} q ^ {n}}, & m = n. \end{array} \right. \end{array}\tag{Moak}
$$

13. A multiplicative shift of the variable $x$ in Exercise 12 gives a set of $q$ -Laguerre polynomials defined by

$$
L _ {n} ^ {\alpha} (x; q) = \sum_ {k = 0} ^ {n} \frac {(q ^ {- n} ; q) _ {k} q ^ {n k + (\alpha - \beta) k + k (k + 1) / 2} x ^ {k}}{(q ^ {\alpha + 1} ; q) _ {k} (q ; q) _ {k}}.
$$

(a) Show that

$$
\begin{array}{l} \int_ {0} ^ {\infty} \frac {L _ {n} ^ {\alpha} (x ; q) L _ {m} ^ {\alpha} (x ; q) x ^ {\alpha - \beta} (- q ^ {\beta + 1} x ^ {- 1} ; q) _ {\infty}}{(- x ; q) _ {\infty} (- q x ^ {- 1} ; q) _ {\infty}} d x \\ = \left\{ \begin{array}{l l} \frac {q ^ {- n} (q ; q) _ {n} (q ; q) _ {\infty}}{(q ^ {\alpha + 1} ; q) _ {n} (q ^ {\alpha + 1} ; q) _ {n}} \frac {\Gamma (\alpha + 1 - \beta) \Gamma (\beta - \alpha)}{\Gamma_ {q} (\alpha + 1 - \beta) \Gamma_ {q} (\beta - \alpha)}, & m = n, \\ 0, & m \neq n. \end{array} \right. \end{array}
$$

(b) Set $\alpha - \beta = c$ (fixed $c$ ) and let $\alpha \to \infty$ in $L_n^\alpha(x; q)$ . Show that the result is the Stieltjes-Wigert polynomial

$$
S _ {n} (x; q) = \sum_ {k = 0} ^ {n} \frac {q ^ {k ^ {2}} (- q ^ {c} x) ^ {k}}{(q ; q) _ {k} (q ; q) _ {n - k}}.
$$

(c) Prove that a weight function for the Stieltjes–Wigert polynomials is

$$
\omega (x) = \frac {x ^ {c}}{(- x ; q) _ {\infty} (- q / x ; q) _ {\infty}}.
$$

For Exercises 12 and 13, see Gasper and Rahman [1990, Chapter 7].

# Infinite Products

## A.1 Infinite Products

For readers unfamiliar with infinite products, a brief introduction is given here.

Definition A.1.1 Let $p_{n,k} = \prod_{m=k}^{n}(1 + a_{m})$ . If there is a k for which $p_{n,k}$ converges to a nonzero value p as $n \to \infty$ , then we say that the infinite product $\prod_{n=1}^{\infty}(1 + a_{n})$ converges. We write it as $p = \prod_{n=k}^{\infty}(1 + a_{n})$ . The reason for not taking k = 1 is to allow an finite number of zero factors. The convergence of the product is said to be absolute if $\prod_{n=1}^{\infty}(1 + |a_{n}|)$ converges.

The following basic theorem reduces the problem of convergence of a product to that of a series. For simplicity, assume that $Re a_{n} > -1$ , $n = 1, 2, \ldots$ . If not, start the product after this holds.

Theorem A.1.2 The product $\prod_{n=1}^{\infty}(1 + a_n)$ converges if and only if the series $\sum_{n=1}^{\infty}\log(1 + a_n)$ converges.

Proof. Suppose that $S_{n} = \sum_{m=1}^{n} \log(1 + a_{m})$ converges to $S$ . Since exp is a continuous function,

$$
\prod_ {m = 1} ^ {n} \left(1 + a _ {m}\right) = \exp \left(S _ {n}\right) \quad \text { converges   to } e ^ {S} = \prod_ {n = 1} ^ {\infty} \left(1 + a _ {n}\right).
$$

To prove the converse, let $1 + a_{m} = A_{m}e^{i\theta_{m}}$ and $\prod_{m=1}^{n}(1 + a_{m}) = B_{n}e^{i\phi_{n}}$ . The convergence of $\Pi(1 + a_{n})$ implies $a_{m} \to 0$ so that $\theta_{m} \to 0$ and $\phi_{n}$ can be chosen so that, say, $\phi_{n} \to \phi$ . We also have

$$
\theta_ {1} + \theta_ {2} + \dots + \theta_ {n} = \phi_ {n} + 2 \pi k _ {n},
$$

where $k_{n}$ is an integer. Therefore,

$$
\theta_ {n + 1} = \phi_ {n + 1} - \phi_ {n} + 2 \pi (k _ {n + 1} - k _ {n}).
$$

Since $k_{n+1}-k_{n}$ is an integer, $\theta_{n+1}\to0$ , and since $\phi_{n+1}-\phi_{n}\to0$ , we must have $k_{n}=k$ , a constant for sufficiently large n. Thus, for sufficiently large n,

$$
S _ {n} = \log p _ {n} + 2 \pi k i.
$$

Let $n\to \infty$ to get

$$
S = \log p + 2 \pi k i.
$$

This proves the theorem. For absolute convergence the condition is simpler and is contained in the next theorem. ■

Theorem A.1.3 The product $\prod_{n=1}^{\infty}(1+a_{n})$ converges absolutely if and only if $\sum_{n=1}^{\infty}a_{n}$ converges absolutely.

Proof. Convergence of the series or the product implies that $a_{n} \rightarrow 0$ . For sufficiently large n we must have $|a_{n}| \leq 1/2$ . Suppose $a_{n} \neq 0$ and n large. Then

$$
\begin{array}{r l} \left| 1 - \frac {\log (1 + a _ {n})}{a _ {n}} \right| & = \left| \frac {a _ {n}}{2} - \frac {a _ {n} ^ {2}}{3} + \dots \right| \\ & \leq \frac {1}{2} [ | a _ {n} | + | a _ {n} | ^ {2} + \dots ] \\ & = \frac {1}{2} \frac {| a _ {n} |}{1 - | a _ {n} |} \leq \frac {1}{2}. \end{array}
$$

So

$$
- \frac {1}{2} \leq \left| \frac {\log (1 + a _ {n})}{a _ {n}} \right| - 1 \leq \frac {1}{2}
$$

or

$$
\frac {1}{2} | a _ {n} | \leq | \log (1 + a _ {n}) | \leq \frac {3}{2} | a _ {n} |.
$$

These inequalities together with Theorem A.1.2 imply the result and also the fact that absolute convergence of a product implies its convergence. ■

Definition A.1.4 The infinite product

$$
\prod_ {n = 1} ^ {\infty} (1 + a _ {n} (x)),
$$

where x is a real or complex variable in a domain, is uniformly convergent if

$$
p _ {n} (x) = \prod_ {m = k} ^ {n} (1 + a _ {m} (x))
$$

converges uniformly in that domain, for each k.

Theorem A.1.5 If the series $\sum_{n=1}^{\infty}|a_n(x)|$ converges uniformly in some region, then the product $\prod_{n=1}^{\infty}(1 + a_n(x))$ also converges uniformly in that region.

The proof of this result is left to the reader.

Corollary A.1.6 If $a_{n}(x)$ is analytic in some region of the complex plane and $\Pi(1+a_{n}(x))$ converges uniformly in that region, then the infinite product represents an analytic function in that region.

## Exercises

1. Prove directly from the definition that the product $(1-\frac{1}{2})(1+\frac{1}{3})(1-\frac{1}{4})\cdots$ is convergent.

2. Prove that an absolutely convergence product is convergent.

3. Show that if $\Sigma a_{n}, \Sigma a_{n}^{2}, \ldots, \Sigma a_{n}^{k-1}, \Sigma |a_{n}|^{k}$ are all convergent, then $\Pi(1 + a_{n})$ is convergent.

$$
\prod_ {n = 1} ^ {\infty} \left\{\left(1 + \frac {1}{n}\right) ^ {x} \left(1 - \frac {x}{n}\right) \right\}.
$$

4. Discuss the convergence of the product

# Summability and Fractional Integration

## B.1 Abel and Cesàro Means

The following theorem, the first part of which was proved by Abel, is often encountered in a first course in real analysis.

Theorem B.1.1 Suppose that the series $\sum_{n=0}^{\infty} b_{n}$ converges to B. Then $\sum_{n=0}^{\infty} b_{n} x^{n}$ converges uniformly on [0, 1], and in particular

$$
\lim _ {x \rightarrow 1 ^ {-}} \sum_ {n = 0} ^ {\infty} b _ {n} x ^ {n} = B.\tag{B.1.1}
$$

Moreover, if $B_{n} = \sum_{k=0}^{n} b_{k}$ , then

$$
\lim _ {n \rightarrow \infty} \frac {B _ {0} + B _ {1} + \cdots + B _ {n}}{n + 1} = B.\tag{B.1.2}
$$

The example of the series $1 - 1 + 1 - \cdots$ shows that the limits in (B.1.1) and (B.1.2) may exist even when the series does not converge. Thus (B.1.1) and (B.1.2) may be used to assign a sum to divergent series.

The series $\sum_{n=0}^{\infty} b_n$ is Abel summable or summable $A$ to $B$ if (B.1.1) holds; and it is Cesàro summable or summable $(C, 1)$ to $B$ if (B.1.2) holds. We also speak of (B.1.1) as the Abel mean and (B.1.2) as the Cesàro mean of the series $\sum_{n=0}^{\infty} b_n$ .

The Abel and Cesàro means of the series $1 - 1 + 1 - \cdots$ are both 1/2. The next theorem shows that Cesàro summability is a stronger requirement than Abel summability.

Theorem B.1.2 If the series $\sum_{n=0}^{\infty} b_n$ is $(C, 1)$ summable to $B$ , then it is $A$ summable to $B$ .

Proof. Use summation by parts to get

$$
\begin{array}{r l} \sum_ {n = 0} ^ {\infty} b _ {n} x ^ {n} - B & = (1 - x) \sum_ {n = 0} ^ {\infty} B _ {n} x ^ {n} - B \left(\text {where} B _ {n} = \sum_ {k = 0} ^ {n} b _ {k}\right) \\ & = (1 - x) ^ {2} \sum_ {n = 0} ^ {\infty} (B _ {0} + \dots + B _ {n}) x ^ {n} - B \\ & = (1 - x) ^ {2} \sum_ {n = 0} ^ {\infty} \{(B _ {0} + \dots + B _ {n}) - (n + 1) B \} x ^ {n}. \end{array}\tag{B.1.3}
$$

Now (B.1.2) implies that, for $\epsilon > 0$ , there exists an integer $N$ such that

$$
\left| \left(B _ {0} + \dots + B _ {n}\right) - (n + 1) B \right| <   \epsilon (n + 1) \quad \text { for } n \geq N.
$$

Use this in (B.1.3) to arrive at the necessary result. ■

The example of the series $1 - 2 + 3 - \cdots$ shows that the Abel mean may exist (in this case it is 1/4) but the Cesàro mean may not. The Abel and Cesàro means, together with other summability methods, are very useful in analysis and analytic number theory. As an elementary example, consider the following theorem of Abel on the product of two series:

Theorem B.1.3 Suppose $\sum_{n=0}^{\infty} a_n$ and $\sum_{n=0}^{\infty} b_n$ are convergent series. Let $c_n = \sum_{k=0}^{n} a_k b_{n-k}$ and suppose that $\sum_{n=0}^{\infty} c_n$ is convergent. Then

$$
\sum_ {n = 0} ^ {\infty} c _ {n} = \sum_ {n = 0} ^ {\infty} a _ {n} \sum_ {n = 0} ^ {\infty} b _ {n}.\tag{B.1.4}
$$

Proof. Since

$$
c _ {n} = \sum_ {k = 0} ^ {n} a _ {n - k} b _ {k},
$$

$$
\sum_ {k = 0} ^ {\infty} c _ {n} r ^ {n} = \sum_ {j = 0} ^ {\infty} a _ {j} r ^ {j} \sum_ {k = 0} ^ {\infty} b _ {k} r ^ {k}
$$

and Theorem B.1.1 completes the proof.

The Cesàro and Abel means play a very significant role in the theory of Fourier series and transforms. We take a very brief look at how they appear in Fourier series since these ideas will play a role elsewhere in the book.

Suppose $f(x)$ is an integrable function of period $2\pi$ . Let $\sum_{-\infty}^{\infty} a_n e^{inx}$ be its Fourier series. An important question is: When does the Fourier series of a function converge to the function? Once again it is easier to deal with the Cesàro mean or the Abel mean. The Abel sum is given by

$$
\sum_ {- \infty} ^ {\infty} a _ {n} r ^ {| n |} e ^ {i n x}, \quad | r | <   1.\tag{B.1.5}
$$

Since

$$
a _ {n} = \frac {1}{2 \pi} \int_ {0} ^ {2 \pi} f (t) e ^ {- i n t} d t,
$$

the sum in (B.1.5) is equal to

$$
\frac {1}{2 \pi} \int_ {0} ^ {2 \pi} f (t) \sum_ {- \infty} ^ {\infty} r ^ {| n |} e ^ {i n (x - t)} d t.
$$

The sum inside the integral is called the Poisson kernel and it is a straightforward calculation to show that it is equal to

$$
\frac {1 - r ^ {2}}{1 - 2 r \cos (x - t) + r ^ {2}} \equiv P _ {r} (x - t).\tag{B.1.6}
$$

The following properties of $P_{r}(x)$ are worth noting:

(i) $P_{r}(x)\geq 0$

(ii) $\frac{1}{2\pi}\int_0^{2\pi}P_r(x)dx = 1$ , and

(iii) for $\delta > 0$ , $\max_{\delta \leq x \leq 2\pi - \delta} P_r(x) \to 0$ as $r \to 1^{-}$ .

These properties can be used to give a proof of the following theorem:

Theorem B.1.4 If f is periodic and integrable on $(0,2\pi)$ then the Abel means of the Fourier series converge to $\frac{1}{2}\{f(x_{0}+) + f(x_{0}-)\}$ at every point $x_{0}$ where the right and left limits $f(x_{0}\pm)$ exist.

A similar result exists for Cesàro means. The nth partial sum of the Fourier series is given by

$$
s _ {n} (x) = \sum_ {k = - n} ^ {n} a _ {k} e ^ {i k x} = \frac {1}{2 \pi} \int_ {0} ^ {2 \pi} \sum_ {k = - n} ^ {n} e ^ {i k (x - t)} f (t) d t.
$$

The sum inside the integral is

$$
1 + 2 \sum_ {k = 0} ^ {n} \cos k (x - t) = \frac {\sin (n + 1 / 2) (x - t)}{\sin ((x - t) / 2)}.\tag{B.1.7}
$$

This expression is called the Dirichlet kernel. One drawback of the Dirichlet kernel is that it is not always positive. However, if we take the $(C, 1)$ mean of the Fourier

series, then we get

$$
\begin{array}{l} \sigma_ {n} (x) = \frac {s _ {0} (x) + s _ {1} (x) + \cdots + s _ {n} (x)}{n + 1} \\ = \frac {1}{2 \pi (n + 1)} \int_ {0} ^ {2 \pi} f (t) \sum_ {k = 0} ^ {n} \frac {\sin \left(n + \frac {1}{2}\right) (x - t)}{\sin ((x - t) / 2)} d t. \end{array}
$$

The sum in the integral denoted by $K_{n}(x - t)$ is called the Fejér kernel. The sum is equal to

$$
\left\{\frac {\sin \frac {1}{2} (n + 1) (x - t)}{\sin \frac {1}{2} (x - t)} \right\} ^ {2} \geq 0.\tag{B.1.8}
$$

The Fejér kernel has the three properties of the Poisson kernel mentioned above. One may then deduce the following theorem:

Theorem B.1.5 For $f$ as in Theorem B.1.4, the Cesàro means of the Fourier series of $f$ converge to $\frac{1}{2}\{f(x_0+) + f(x_0-)\}$ at every point $x_0$ where the right and left limits $f(x_0 \pm)$ exist.

If we assume $f$ to be continuous on $[0, 2\pi]$ , then the Abel and Cesàro means converge to $f$ . An important consequence of Theorem B.1.5 is the following corollary:

Corollary B.1.6 A continuous function on $[0, 2\pi]$ can be uniformly approximated by trigonometric polynomials, that is, polynomials of the form $\sum_{-n}^{n} a_{k} e^{ikx}$ .

Since $e^{ikx}$ is uniformly approximated on $[0, 2\pi]$ by partial sums of its Taylor series, we get another proof (see Exercise 1.40) of the Weierstrass approximation theorem.

## B.2 Cesàro Means (C, α)

In the previous section, we saw that the $(C, 1)$ means do not assign a value to the sum $1 - 2 + 3 - 4 + \cdots$ . To handle this and some other situations, we define Cesàro means of higher order.

For the series $\sum_0^\infty b_n$ , set

$$
B _ {n} ^ {(0)} = B _ {0} + B _ {1} + \dots + B _ {n},
$$

where

$$
B _ {n} = \sum_ {k = 0} ^ {n} b _ {k}.
$$

The limit of the sequence $\{\frac{B_n^{(0)}}{n + 1}\}$ gives the $(C,1)$ mean. Now, set

$$
B _ {n} ^ {(1)} = B _ {0} ^ {(0)} + B _ {1} ^ {(0)} + \dots + B _ {n} ^ {(0)}\tag{B.2.1}
$$

and

$$
E _ {n} ^ {(1)} = 1 + 2 + \dots + n + 1 = \frac {(n + 1) (n + 2)}{2}.
$$

The limit of the sequence $\{\frac{B_n^{(1)}}{E_n^{(1)}}\}$ is the $(C,2)$ mean of the series $\sum_0^\infty b_n$ . Similarly,

$$
B _ {n} ^ {(2)} = B _ {0} ^ {(1)} + B _ {1} ^ {(1)} + \dots + B _ {n} ^ {(1)}
$$

and

$$
E _ {n} ^ {(2)} = 1 + 3 + \dots + \frac {(n + 1) (n + 2)}{2} = \frac {(n + 1) (n + 2) (n + 3)}{3 !}.
$$

Thus, the $(C,3)$ mean is given by

$$
\lim _ {n \to \infty} \left(B _ {n} ^ {(2)} / E _ {n} ^ {(2)}\right).
$$

Define $B_{n}^{(k)}$ and $E_{n}^{(k)}$ inductively by

$$
B _ {n} ^ {(k)} = B _ {0} ^ {(k - 1)} + B _ {1} ^ {(k - 1)} + \dots + B _ {n} ^ {(k - 1)}
$$

and

$$
E _ {n} ^ {(k)} = E _ {0} ^ {(k - 1)} + E _ {1} ^ {(k - 1)} + \dots + E _ {n} ^ {(k - 1)}.
$$

It is possible to express $B_{n}^{(k)}$ explicitly in terms of $b_{n}$ as follows. Note that

$$
\sum_ {n = 0} ^ {\infty} B _ {n} ^ {(k)} x ^ {n} = (1 - x) ^ {- 1} \sum_ {n = 0} ^ {\infty} B _ {n} ^ {(k - 1)} x ^ {n} = \dots = (1 - x) ^ {- (k + 1)} \sum_ {0} ^ {\infty} b _ {n} x ^ {n}
$$

and

$$
\sum_ {n = 0} ^ {\infty} E _ {n} ^ {(k)} x ^ {n} = (1 - x) ^ {- (k + 1)}.
$$

So

$$
B _ {n} ^ {(k)} = \sum_ {\ell = 0} ^ {n} \left(\frac {(k + 1) _ {\ell}}{\ell !}\right) b _ {n - \ell}\tag{B.2.2}
$$

and

$$
E _ {n} ^ {(k)} = \frac {(k + 1) _ {n}}{n !}.\tag{B.2.3}
$$

We define the $(C, k)$ mean of $\sum_{0}^{\infty} b_{n}$ as the limit of the $B_{n}^{(k)} / E_{n}^{(k)}$ as $n \to \infty$ . Note that these quotients are meaningful even when k is not a positive integer. We take k to be real and greater than -1.

Definition B.2.1 The series $\sum_0^\infty b_n$ is $(C,\alpha)$ summable to $B$ (for $\alpha > - 1$ ) if

$$
\lim _ {n \rightarrow \infty} \frac {n !}{(\alpha + 1) _ {n}} \sum_ {\ell = 0} ^ {n} \frac {(\alpha + 1) _ {k}}{\ell !} b _ {n - \ell} = B.\tag{B.2.4}
$$

Remark B.2.1 Note that the limit in (B.2.4) is equal to

$$
\lim _ {n \rightarrow \infty} \frac {\Gamma (\alpha + 1)}{n ^ {\alpha}} B _ {n} ^ {(\alpha)}.
$$

## B.3 Fractional Integrals

It is possible to extend the summability definitions to integrals. Suppose $f(t)$ is integrable on finite intervals $(0, x)$ . We say, for example, that f is Abel integrable, that is, $\int_{0}^{\infty} f(t) dt$ exists in the Abel sense, if

$$
\lim _ {\lambda \rightarrow 0 ^ {+}} \int_ {0} ^ {\infty} e ^ {- \lambda t} f (t) d t \quad \text { exists. }
$$

We also write this as

$$
\int_ {0} ^ {\infty} f (t) d t = \lim _ {\lambda \rightarrow 0 ^ {+}} \int_ {0} ^ {\infty} e ^ {- \lambda t} f (t) d t \quad (\text { Abel }).
$$

To define Cesàro integrability $(C, k)$ , where $k$ is an integer, we first have the integral analog of $B_{n}^{(k)}$ (see (B.2.2)) as

$$
f _ {(k)} (x) = \int_ {0} ^ {x} f _ {(k - 1)} (t) d t = \int_ {0} ^ {x} (x - t) f _ {(k - 2)} (t) d t = \dots = \frac {1}{k !} \int_ {0} ^ {x} (x - t) ^ {k} f (t) d t.\tag{B.3.1}
$$

Following the remark after (B.2.4) we say that $\int_0^\infty f(t)dt$ is $(C,k)$ integrable if

$$
\lim _ {x \rightarrow \infty} \frac {\Gamma (k + 1)}{x ^ {k}} f _ {k} (x) = \lim _ {x \rightarrow \infty} \int_ {0} ^ {x} \left(1 - \frac {t}{x}\right) ^ {k} f (t) d t \quad \text { exists. }
$$

Observe that the final expression for $f_{k}(x)$ in (B.3.1) is meaningful for all real k > -1. Thus we have a definition of $(C, \alpha)$ integrability for $\alpha > -1$ .

Note also that the formula for $f_{(k)}$ in (B.3.1) expresses $f_{(k)}$ as a $(k+1)$ -fold integral of f. Thus, we define $I_{\alpha}f$ , the $\alpha$ -fold integral of f for Re $\alpha > 0$ , by the formula

$$
I _ {\alpha} f (x) = \frac {1}{\Gamma (\alpha)} \int_ {0} ^ {x} (x - t) ^ {\alpha - 1} f (t) d t.\tag{B.3.2}
$$

It is easy to check that the operator $I_{\alpha}$ satisfies the relation

$$
I _ {\alpha} I _ {\beta} = I _ {\alpha + \beta}, \quad \operatorname{Re} (\alpha , \beta) > 0.
$$

The operator $I_{\alpha}$ is called a fractional integral of order $\alpha$ . Euler's integral expression for the ${}_2F_1$ hypergeometric series can now be interpreted as a fractional integral. Write the formula as

$$
\begin{array}{r l} _ {2} F _ {1} \binom {a, b} {c}; x & = \frac {\Gamma (c) x ^ {1 - c}}{\Gamma (b) \Gamma (c - b)} \int_ {0} ^ {x} t ^ {b - 1} (x - t) ^ {c - b - 1} (1 - t) ^ {- a} d t \\ & = \frac {\Gamma (c)}{\Gamma (b)} x ^ {1 - c} (I _ {c - b} f) (x), \end{array}
$$

where $f(t) = t^{b - 1}(1 - t)^{-a}$ .

Remark B.3.1 Abel and Cesàro integrability can be used to study Fourier integrals just as the corresponding summability is used to study Fourier series.

## B.4 Historical Remarks

Euler had used Abel means and other methods for associating a sum to a divergent series. In particular, he obtained the functional equation of the zeta function in the form

$$
\frac {1 - 2 ^ {s - 1} + 3 ^ {s - 1} - \cdots}{1 - 2 ^ {- s} + 3 ^ {- s} - \cdots} = - \frac {(s - 1) ! (2 ^ {s} - 1)}{(2 ^ {s - 1} - 1) \pi^ {s}} \cos \frac {1}{2} s \pi .
$$

When Re s > 1, the series in the denominator converges but the series in the numerator is interpreted in the Abelian sense. It can be proved that

$$
\lim _ {x \rightarrow 1 ^ {-}} \sum_ {1} ^ {\infty} (- 1) ^ {n - 1} n ^ {s - 1} x ^ {n} = \zeta (1 - s) \left(2 ^ {s} - 1\right);
$$

thus Euler had the functional equation correct. He verified it only for integer values of $s$ and for $s = \frac{1}{2}$ and $\frac{3}{2}$ . Abel's name is attached to this method of summation since he proved formula (B.1.1).

Leibniz used $(C,1)$ means to evaluate $1-1+1-\cdots$ and somewhat later D. Bernoulli employed the same method to consider the more general series $\sum_{n=0}^{\infty}b_{n}$ , where $b_{n+p}=b_{n}$ for all n and $\sum_{0}^{p-1}b_{k}=0$ . Neither Leibniz nor Bernoulli explicitly stated that he was giving a new definition of convergence. This was done by Cesàro. For more on the history of Abel and Cesàro means the reader should consult the very interesting treatment given in Hardy [1949].

Abel was apparently the first mathematician to use fractional calculus, though the concept had been considered by others before him. Abel used fractional calculus in his solution to the problem of finding the tautochrone - the curve down which a particle slides freely under gravity with zero initial velocity and reaches the bottom in the same amount of time regardless of the starting point, provided that the starting and lowest points are distinct. This problem had already been solved by Huygens; the motivation was the construction of a clock in which the period of oscillation does not depend on the amplitude of the pendulum.

Suppose that the particle slides down from the point $(a, b)$ and that the bottom of the curve is the origin of coordinates. If s is the length measured from the origin, then conservation of energy implies that

$$
\text { velocity } = v = d s / d t = \sqrt {2 g (b - y)}
$$

at a point on the curve with ordinate y. Set ds/dy = f(y) to see that the time taken to reach the bottom is given by

$$
T (b) = \frac {1}{\sqrt {2 g}} \int_ {0} ^ {b} \frac {f (y)}{\sqrt {b - y}} d y.
$$

Abel observed that

$$
T (b) = \sqrt {\frac {\pi}{2 g}} (I _ {1 / 2} f) (b).
$$

Since $T(b)$ is independent of $b$ , use (B.3.2) to get

$$
I _ {1 / 2} \left(I _ {1 / 2} f\right) (b) = \frac {\sqrt {2 g} T}{\pi} \int_ {0} ^ {b} \frac {d y}{\sqrt {b - y}} = \frac {2 T}{\pi} \sqrt {2 g b}.
$$

Now take the derivative of both sides to obtain

$$
f (b) = \frac {T}{\pi} \sqrt {\frac {2 g}{b}}.
$$

Since

$$
f (y) = \frac {d s}{d y} = \left[ 1 + \left(\frac {d x}{d y}\right) ^ {2} \right] ^ {1 / 2},
$$

we get a differential equation that can be solved. The tautochrone curve turns out to be a cycloid. An English translation of Abel's [1826] paper on this topic is also available.

The above calculations suggest that the concept of a fractional derivative would also be useful. For smooth enough functions, in particular analytic functions, it is possible to define fractional derivatives as follows:

$$
D _ {\alpha} f (x) = \frac {d ^ {n}}{d x ^ {n}} I _ {n - \alpha} f (x),\tag{B.4.1}
$$

where $0 < \operatorname{Re} \alpha < n$ , and $n$ is an integer. Observe that we took the integral first and then the derivative. If the calculations are done in the opposite order, a different function arises since the first n - 1 terms are removed by the nth derivative. For an analytic function

$$
f (x) = \sum_ {0} ^ {\infty} a _ {k} x ^ {k}
$$

the fractional integral has the form

$$
I _ {\alpha} f (x) = \sum_ {0} ^ {\infty} \frac {k !}{\Gamma (k + \alpha + 1)} a _ {k} x ^ {k + \alpha},
$$

as is easily verified. This shows that the value of n in (B.4.1) may be arbitrarily chosen as long as $n > Re \alpha$ . In fact,

$$
D _ {k} I _ {\alpha} = D _ {n} I _ {\alpha + n - k}.
$$

However, the inclusion of fractional derivatives with fractional integrals does not give a group, for although

$$
D _ {\alpha} D _ {\beta} = D _ {\alpha + \beta}
$$

when $\alpha, \beta$ and $\alpha + \beta$ are not integers,

$$
D _ {1 / 2} D \neq D _ {3 / 2}
$$

for the reason mentioned above.

## Exercises

1. Prove Theorem B.1.1.

2. With the notation of Theorem B.1.3, prove that if $\sum_0^\infty a_n$ converges absolutely and $\sum_0^\infty b_n$ converges, then $\sum_0^\infty c_n$ converges.

3. Prove that if the series $\sum_0^\infty b_n$ is $(C, \alpha)$ summable to $B$ , and $\beta > \alpha$ , then the series is $(C, \beta)$ summable to $B$ .

4. Prove the following extension of Theorem B.1.2: If the series $\sum_{0}^{\infty} b_n$ is $(C, \alpha)$ summable to $B$ , then it is Abel summable to $B$ .

5. Show that

$$
\sum_ {n = 1} ^ {\infty} (- 1) ^ {n - 1} n ^ {m} e ^ {- n y} = (- 1) ^ {m} \frac {d ^ {m}}{d y ^ {m}} (1 + e ^ {y}) ^ {- 1}.
$$

Deduce that

$$
1 - 2 ^ {2 k} + 3 ^ {2 k} = \dots = 0,
$$

$$
1 - 2 ^ {2 k - 1} + 3 ^ {2 k - 1} - \dots = (- 1) ^ {k - 1} \frac {2 ^ {2 k} - 1}{2 k} B _ {k}
$$

in the sense of Abel summability. This result is due to Euler. See the historical introduction in Hardy [1949].

6. A sequence $\mathbf{S}_n$ converges to $\mathbf{S}$ in the sense of Borel if

$$
\lim _ {t \rightarrow \infty} e ^ {- t} \sum_ {n = 0} ^ {\infty} \frac {\mathsf {S} _ {n}}{n !} t ^ {n} = \mathsf {S}.
$$

Show that if $S_{n}$ converges to S then $S_{n} \rightarrow S$ in the Borel sense. Also prove that if $\mathbf{S}_{n}(x) = 1 + x + \cdots + x^{n}$ , then $\mathbf{S}_{n}(x) \rightarrow 1/(1 - x)$ in the Borel sense for Re x < 1.

7. Show that if $\beta \geq \alpha \geq -1$ and the $(C, \beta)$ means of $\Sigma a_n$ are nonnegative, then the $(C, \alpha)$ means of $\Sigma a_n r^n$ are nonnegative for $0 \leq r \leq (\alpha + 1) / (\beta + 1)$ . Hint: Observe that

$$
(1 - \omega) ^ {- \alpha - 1} \Sigma a _ {n} r ^ {n} \omega^ {n} = (1 - \omega) ^ {- \alpha - 1} (1 - r w) ^ {\beta + 1} (1 - r w) ^ {- \beta - 1} \Sigma a _ {n} r ^ {n} \omega^ {n}
$$

and show that the power series coefficients of $(1 - \omega)^{-\alpha - 1}(1 - rw)^{\beta + 1}$ and those of $(1 - rw)^{-\beta - 1}\Sigma a_n r^n \omega^n$ are nonnegative. This proof is due to Bustoz [1974].

8. A series $\sum_{1}^{\infty} a_n$ is summable (L) (Lambert summable) to S if

$$
\lim _ {x \rightarrow 1 ^ {-}} (1 - x) \sum_ {1} ^ {\infty} \frac {n a _ {n} x ^ {n}}{1 - x ^ {n}} = \mathsf {S}.
$$

Prove that if $\Sigma a_{n} = \mathbb{S}(C,\alpha)$ , for some $\alpha$ , then $\Sigma a_{n} = \mathbb{S}(L)$ .

9. Prove Dirichlet's theorem that if $\chi$ is a quadratic Dirichlet character, then $L(1, \chi) = \sum_{n=1}^{\infty} \chi(n)/n \neq 0$ as follows:

(a) Show that $\sum_{d|n} \chi(d) \geq 0$ .

(b) Show that

$$
\lim _ {x \rightarrow 1 ^ {-}} \sum_ {n = 1} ^ {\infty} \frac {\chi (n) x ^ {n}}{1 - x ^ {n}} = \lim _ {x \rightarrow 1 ^ {-}} \sum_ {n = 1} ^ {\infty} \left(\sum_ {d | n} \chi (d)\right) x ^ {n} = \infty .
$$

(c) Let

$$
f (x) = \sum_ {n = 1} ^ {\infty} \left(\frac {\chi (n)}{n (1 - x)} - \frac {\chi (n) x ^ {n}}{1 - x ^ {n}}\right) =: \sum_ {n = 1} ^ {\infty} \frac {\chi (n)}{1 - x} b _ {n}.
$$

Show that $b_{1} \geq b_{2} \geq \cdots \geq b_{n} \geq b_{n+1} \geq \cdots$ .

(d) Note that $|\sum_{n=1}^{m} \chi(n)| \leq M$ , where $M$ is a constant that does not depend on $m$ . Use summation by parts to prove that $f(x) \leq \frac{Mb_1}{1 - x} = M$ .

(e) Deduce that $L(1, \chi) \neq 0$ .

This proof is taken from Monsky [1994].

10. Prove the following theorem of Hardy and Littlewood: If $a_{n} \geq 0$ and

$$
\lim _ {x \rightarrow 1 ^ {-}} (1 - x) \sum_ {n = 0} ^ {\infty} a _ {n} x ^ {n} = 1,
$$

then

$$
\lim _ {n \rightarrow \infty} \frac {1}{n} \sum_ {k = 0} ^ {n} a _ {k} = 1.
$$

Karamata's proof is sketched below.

(a) Show that

$$
\lim _ {x \rightarrow 1 ^ {-}} (1 - x) \sum_ {n = 0} ^ {\infty} a _ {n} x ^ {n} g \left(x ^ {n}\right) = \int_ {0} ^ {1} g (t) d t,
$$

when $g(t)$

(i) is a polynomial,

(ii) is a continuous function, or

(iii) has a discontinuity of the first kind.

(b) Take $g(t) = 0$ ( $0 \leq t < 1/e$ ) = $1/t(1/e \leq t \leq 1)$ and complete the proof of the theorem.

# Asymptotic Expansions

## C.1 Asymptotic Expansion

Let x be a real or complex variable in an unbounded region D and let $\sum_{0}^{\infty}a_{n}x^{-n}$ be a formal power series that may be convergent or divergent.

Definition C.1.1 The series $\sum_0^\infty a_n x^{-n}$ is an asymptotic expansion of a function $f(x)$ if

$$
f (x) = \sum_ {0} ^ {n - 1} a _ {k} x ^ {- k} + R _ {n} (x),\tag{C.1.1}
$$

where $R_{n}(x) = 0(x^{-n})$ as $x \to \infty$ in $D$ . Usually (C.1.1) is written as

$$
f (x) \sim a _ {0} + a _ {1} x ^ {- 1} + a _ {2} x ^ {- 2} + \dots \quad a s x \rightarrow \infty i n D.\tag{C.1.2}
$$

This definition is due to Poincaré [1886]. As a simple example we have the following asymptotic expansion of $(1 + x)^{-1}$ :

$$
\frac {1}{1 + x} \sim \frac {1}{x} - \frac {1}{x ^ {2}} + \frac {1}{x ^ {3}} - \dots \quad \text { as } x \to \infty .\tag{C.1.3}
$$

In this case the series is convergent. The more interesting situation occurs when the series is divergent. Consider the complementary error function of a real variable $x \geq 0$ ,

$$
\operatorname{erfc} x = \frac {2}{\sqrt {\pi}} \int_ {x} ^ {\infty} e ^ {- t ^ {2}} d t.\tag{C.1.4}
$$

Successive integration by parts gives

$$
\begin{array}{r l} \operatorname{erfc} x & = \frac {2}{\sqrt {\pi}} \left[ \frac {e ^ {- x ^ {2}}}{2 x} - \int_ {x} ^ {\infty} \frac {e ^ {- t ^ {2}}}{2 t ^ {2}} d t \right] \\ & = \frac {e ^ {- x ^ {2}}}{\sqrt {\pi} x} \left[ 1 + \sum_ {k = 1} ^ {n} (- 1) ^ {k} \frac {1 \cdots 3 \cdot (2 k - 1)}{(2 x ^ {2}) ^ {k}} + R _ {n} (x) \right], \end{array}
$$

where

$$
R _ {n} (x) = (- 1) ^ {n + 1} \frac {1 \cdot 3 \cdots (2 n + 1)}{2 ^ {n}} x e ^ {x ^ {2}} \int_ {x} ^ {\infty} \frac {e ^ {- t ^ {2}}}{t ^ {2 n + 2}} d t.
$$

It is easy to see that

$$
\left| R _ {n} (x) \right| \leq \frac {1 \cdot 3 \cdots (2 n + 1)}{(2 x ^ {2}) ^ {n + 1}}.\tag{C.1.5}
$$

Hence

$$
\frac {e ^ {- x ^ {2}}}{\sqrt {\pi} x} \left[ 1 + \sum_ {k = 1} ^ {\infty} (- 1) ^ {k} \frac {1 \cdot 3 \cdots (2 k - 1)}{(2 x ^ {2}) ^ {k}} \right]
$$

is an asymptotic expansion of the complementary error function. It is clear that the series diverges for all x > 0. However, if a fixed number of terms is taken, then for large enough x a good approximation of erfc x is obtained. On the other hand, for a given x, taking more and more terms of the series does not improve the approximation, since the series diverges.

## C.2 Properties of Asymptotic Expansions

The following theorem follows almost immediately from the definition.

Theorem C.2.1 A function $f(x)$ has an asymptotic expansion $\Sigma a_{n}x^{-n}$ if and only if for each $n$ ,

$$
x ^ {n} \left[ f (x) - \sum_ {k = 0} ^ {n - 1} a _ {k} x ^ {- k} \right]\rightarrow a _ {n} \quad a s x \rightarrow \infty i n D,\tag{C.2.1}
$$

uniformly with respect to arg x when x is complex.

Proof. It is easy to see that (C.2.1) implies (C.1.2). To reason in the other direction, observe that

$$
x ^ {n} R _ {n} (x) = x ^ {n} \left[ a _ {n} x ^ {- n} + R _ {n + 1} (x) \right]\rightarrow a _ {n} \quad \text { as } x \rightarrow \infty ,
$$

and the theorem is proved.

A consequence of this theorem is that a function has at most one asymptotic expansion in D. In a different unbounded region the asymptotic expansion may be different. However, two different functions may have the same asymptotic expansion in some region. For example, the function $e^{-x}$ in $|\arg x| \leq \frac{1}{2}\pi - \delta < \frac{1}{2}\pi$ satisfies $x^{n}e^{-x} \to 0$ as $x \to \infty$ . By (C.2.1),

$$
e ^ {- x} \sim 0 + \frac {0}{x} + \frac {0}{x ^ {2}} + \dots \quad | \arg x | \leq \frac {1}{2} \pi - \delta , \quad x \rightarrow \infty .
$$

So the zero function and $e^{-x}$ have the same expansion in this region.

The next theorem gives some algebraic properties of asymptotic expansions.

Theorem C.2.2 Suppose that $f(x) \sim \Sigma a_n x^{-n}$ in $D_1$ and $g(x) \sim \Sigma b_n x^{-n}$ in $D_2$ . Then:

(i) For constants $\lambda$ and $\mu$

$$
\lambda f (x) + \mu g (x) \sim \Sigma (\lambda a _ {n} + \mu b _ {n}) x ^ {- n} i n D _ {1} \cap D _ {2}.
$$

(ii) $f(x)g(x)\sim \Sigma c_nx^{-n}$ in $D_{1}\cap D_{2},$ where

$$
c _ {n} = a _ {0} b _ {0} + a _ {1} b _ {n - 1} + \dots + a _ {n} b _ {0}.
$$

(iii) If $a_0 \neq 0$ , then

$$
\frac {1}{f (x)} = \sum_ {k = 0} ^ {n - 1} \frac {d _ {k}}{x ^ {k}} + O \left(x ^ {- n}\right) \quad a s x \rightarrow \infty i n D _ {1},
$$

where $a_0^{k + 1}d_k$ is a polynomial in $a_0, a_1, \ldots, a_k$ . The $d_k$ can be obtained from the relations

$$
a _ {0} d _ {0} = 1, \quad a _ {0} d _ {k} = - \left(a _ {1} d _ {k - 1} + a _ {2} d _ {k - 2} + \dots + a _ {k} d _ {0}\right), \quad k = 1, 2, \dots .
$$

The proof of this theorem is left to the reader.

Asymptotic series can be integrated over the interval $x \leq t < \infty$ , if $a_0 = a_1 = 0$ . In this case

$$
f (x) \sim \frac {a _ {2}}{x ^ {2}} + \frac {a _ {3}}{x ^ {3}} + \dots , \quad x \rightarrow \infty ,
$$

and

$$
\int_ {x} ^ {\infty} f (t) d t \sim \frac {a _ {2}}{x} + \frac {a _ {3}}{2 x ^ {2}} + \dots , \quad x \rightarrow \infty .
$$

Integration is possible here because $f(t) = a_{2}t^{-2} + O(t^{-2})$ for t large. If $a_{0}$ and $a_{1}$ are not zero, then

$$
\int_ {x} ^ {\infty} [ f (t) - a _ {0} - a _ {1} t ^ {- 1} ] d t \sim \frac {a _ {2}}{x} + \frac {a _ {3}}{2 x ^ {3}} + \dots , \quad x \rightarrow \infty .
$$

Differentiation of an asymptotic expansion may not always be valid. A standard example where differentiation fails is $f(x) = e^{-x} \sin e^{x}$ where x > 0. The derivative $f'(x) = \cos e^{x} - e^{-x} \sin e^{x}$ oscillates as $x \to \infty$ and hence does not have an asymptotic expansion by Theorem C.2.1. But

$$
f (x) \sim 0 + \frac {0}{x} + \frac {0}{x ^ {2}} + \dots , \quad x \rightarrow \infty .
$$

If $f'(x)$ is continuous and has an asymptotic expansion, then it can be obtained from term-by-term differentiation of the expansion for $f(x)$ . This follows from the result on integration and uniqueness of the asymptotic expansion.

## C.3 Watson's Lemma

In this section, we discuss a method of obtaining the asymptotic expansion in some region of a function expressible as a Laplace integral. Section 1 has an example of an integral whose asymptotic expansion was obtained using integration by parts. The failure of this method in one case was discussed in Chapter 2. Also see Wong [1989, p. 18].

The next theorem, called Watson's lemma, gives the asymptotic expansion of $\int_0^\infty e^{-xt}f(t)dt$ . See Watson [1918].

Theorem C.3.1 Let $f(t)$ be analytic in $|t| \leq a + \delta$ , where $a > 0$ , $\delta > 0$ , except possibly for a branch point at 0; and let

$$
f (t) = \sum_ {m = 1} ^ {\infty} a _ {m} t ^ {(m / r) - 1},\tag{C.3.1}
$$

when $|t| \leq a$ and $r > 0$ . Suppose also that $|f(t)| < \kappa e^{bt}$ , where $\kappa$ and $b$ are positive numbers independent of $t$ , when $t \geq a$ . Then

$$
\int_ {0} ^ {\infty} e ^ {- x t} f (t) d t \sim \sum_ {m = 1} ^ {\infty} a _ {m} \Gamma (m / r) x ^ {- m / r} \quad a s x \rightarrow \infty\tag{C.3.2}
$$

for $|\arg x| \leq \frac{1}{2}\pi - \delta < \frac{1}{2}\pi$ .

Proof. It is clear that for any fixed integer $M$ , a constant $C$ can be found such that for $t \geq 0$

$$
\left| f (t) - \sum_ {m = 1} ^ {M - 1} a _ {m} t ^ {(m / r) - 1} \right| \leq C t ^ {(M / r) - 1} e ^ {b t}.
$$

Hence

$$
\begin{array}{r l} \int_ {0} ^ {\infty} e ^ {- x t} f (t) d t & = \sum_ {m = 1} ^ {M - 1} \int_ {0} ^ {\infty} e ^ {- x t} a _ {m} t ^ {(m / r) - 1} d t + R _ {M} \\ & = \sum_ {m = 1} ^ {M - 1} a _ {m} \Gamma (m / r) x ^ {- m / r} + R _ {M}, \end{array}
$$

where

$$
\begin{array}{l} | R _ {M} | \leq \int_ {0} ^ {\infty} | e ^ {- x t} | C t ^ {(M / r) - 1} e ^ {b t} d t \\ = C \Gamma (M / r) / [ \operatorname{Re} x - b ] ^ {M / r}, \end{array}
$$

provided $\operatorname{Re} x > b$ . Since $|\arg x| \leq \frac{1}{2}\pi - \delta$ , it follows that $\operatorname{Re} x > b$ if $|x| > b$ $\csc \delta$ . Thus,

$$
\left| x ^ {M / r} R _ {M} \right| <   \frac {C \Gamma (M / r) | x | ^ {M / r}}{(| x | \sin \delta - b) ^ {M / r}} = O (1).
$$

This proves the theorem.

Watson's lemma can be generalized to the case in which the integral in (C.3.2) is a contour integral, $\int_{\infty}^{(0 +)}e^{-xt}f(t)dt$ and (C.3.1) is replaced by an asymptotic expansion for $f(t)$ . See Olver [1974, pp. 112-115] and Wong [1989, p. 22].

## C.4 The Ratio of Two Gamma Functions

We give an application of Watson's lemma to obtain the asymptotic expansion of a ratio of gamma functions. This expansion is due to Tricomi and Erdélyi [1951].

Observe that for $\operatorname{Re}(x + a) > 0$ and $\operatorname{Re}(b - a) > 0$ , we have

$$
\frac {\Gamma (x + a)}{\Gamma (x + b)} = \frac {1}{\Gamma (b - a)} \int_ {0} ^ {\infty} e ^ {- x t} e ^ {- a t} (1 - e ^ {- t}) ^ {b - a - 1} d t.\tag{C.4.1}
$$

Define the generalized Bernoulli polynomials $B_{n}^{\sigma}(u)$ by

$$
\frac {t ^ {\sigma} e ^ {u t}}{(e ^ {t} - 1) ^ {\sigma}} = \sum_ {n = 0} ^ {\infty} B _ {n} ^ {\sigma} (u) \frac {t ^ {n}}{n !}, \quad | t | <   2 \pi .\tag{C.4.2}
$$

Then for $\sigma = a + 1 - b$ ,

$$
\frac {e ^ {- a t}}{(1 - e ^ {- t}) ^ {\sigma}} = \sum_ {n = 0} ^ {\infty} \frac {(- 1) ^ {n}}{n !} B _ {n} ^ {\sigma} (a) t ^ {n - \sigma}, \quad | t | <   2 \pi .
$$

Watson's lemma now implies that

$$
\begin{array}{l}\frac {\Gamma (x + a)}{\Gamma (x + b)} \sim \sum_ {n = 0} ^ {\infty} \frac {(- 1) ^ {n}}{n !} B _ {n} ^ {\sigma} (a) \frac {\Gamma (b - a + n)}{\Gamma (b - a)} \frac {1}{x ^ {b - a + n}},\\| \arg x | \leq \frac {1}{2} \pi - \delta , \quad | x | \rightarrow \infty .\end{array}\tag{C.4.3}
$$

If instead of the integral representation (C.4.1), one were to use

$$
\frac {\Gamma (x + a)}{\Gamma (x + b)} = \frac {\Gamma (1 + a - b)}{2 \pi i} \int_ {- \infty \cdot e ^ {i \alpha}} ^ {(0 +)} e ^ {(x + a) t} (e ^ {t} - 1) ^ {b - a - 1} d t,\tag{C.4.4}
$$

$\operatorname{Re}[(x + a)e^{i\alpha}] > 0, |\alpha| < \pi / 2$ , and for small $|t|$ ,

$$
\alpha - \pi \leq \arg (e ^ {t} - 1) \leq \alpha + \pi ;
$$

then one could extend (C.4.3) to $|\arg x| \leq \pi - \delta$ .

There is an improvement of (C.4.3) from the computational standpoint due to Fields [1964]. Note that if $u$ is replaced by $\sigma - u$ in (C.4.2), then $B_k^\sigma (\sigma - u) = (-1)^k B_k^\sigma (u)$ . This implies that $B_{2k + 1}^\sigma (\sigma / 2) \equiv 0$ . Now write the integrand in

(C.4.1) as

$$
\begin{array}{c} e ^ {- (x + a - \sigma / 2) t} e ^ {- \sigma t / 2} (1 - e ^ {- t}) ^ {- \sigma} = e ^ {- (x + a - \sigma / 2) t} \sum_ {n = 0} ^ {\infty} \frac {(- 1) ^ {n}}{n !} B _ {n} ^ {\sigma} (\sigma / 2) t ^ {n - \sigma} \\ = e ^ {- (x + a - \sigma / 2) t} \sum_ {n = 0} ^ {\infty} \frac {B _ {2 n} ^ {\sigma} (\sigma / 2)}{(2 n) !} t ^ {2 n - \sigma}. \end{array}
$$

This implies

$$
\frac {\Gamma (x + a)}{\Gamma (x + b)} \sim \sum_ {n = 0} ^ {\infty} \frac {B _ {2 n} ^ {\sigma} (\sigma / 2)}{(2 n) !} \cdot \frac {\Gamma (b - a + 2 n)}{\Gamma (b - a)} \frac {1}{(x + a - \sigma / 2) ^ {2 n + b - a}}
$$

for $|\arg (x + a)|\leq \frac{1}{2}\pi -\delta ,|x|\to \infty .$

## Exercises

1. Let $\operatorname{Re} x \geq 0$ . Show that as $x \to 0$ ,

$$
\int_ {0} ^ {\infty} \frac {e ^ {- t}}{1 + x t} d t \sim \sum_ {n = 0} ^ {\infty} (- 1) ^ {n} n! x ^ {n}
$$

by two methods: (a) Expand $1 / (1 + xt)$ as a series. (b) Integrate by parts repeatedly.

2. Suppose that

$$
F (x) = \int_ {0} ^ {\infty} e ^ {- x t} f (t) d t
$$

converges for some $x = x_0$ and $f$ has continuous derivatives of all orders in $0 \leq t \leq a$ . Show that

$$
F (x) \sim \Sigma f ^ {(n)} (0) x ^ {- n - 1}
$$

uniformly in $\arg x$ , as $x \to \infty$ in $|\arg x| < \pi / 2 - \epsilon$ for $\epsilon > 0$ .

3. Show that

$$
x ^ {- a} e ^ {x} \int_ {x} ^ {\infty} e ^ {- x} x ^ {a - 1} d x \sim \frac {1}{x} + \frac {a - 1}{x ^ {2}} + \frac {(a - 1) (a - 2)}{x ^ {3}} + \dots .
$$

4. Suppose $\theta_{n}$ is defined by

$$
1 + \frac {n}{1 !} + \frac {n ^ {2}}{2 !} + \dots + \frac {n ^ {n - 1}}{(n - 1) !} + \frac {n ^ {n}}{n !} \theta_ {n} = \frac {1}{2} e ^ {n}.
$$

Show that

$$
\theta_ {n} = 1 + \frac {n}{2} \left(\int_ {0} ^ {1} (x e ^ {1 - x}) ^ {n} d x - \int_ {1} ^ {\infty} (x e ^ {1 - x}) ^ {n} d x\right)
$$

and hence

$$
\theta_ {n} \sim \frac {1}{3} + \frac {4}{1 3 5 n} - \frac {8}{2 8 3 5 n ^ {2}} + \dots \quad \text { as } n \rightarrow \infty .
$$

For a discussion of this result of Ramanujan, see Berndt [1989, pp. 181–184].

5. Prove Theorem C.2.2.

# Euler–Maclaurin Summation Formula

## D.1 Introduction

Some consequences of the close connection between series and integrals are brought out even in a first course in calculus. The integral test, for example, states that for a decreasing continuous function on $[1,\infty)$ the series $\sum_{1}^{\infty}f(n)$ and integral $\int_{1}^{\infty}f(x)dx$ converge or diverge together. In the derivation of Stirling's approximation for $\Gamma(x)$ given in Chapter 1, we saw that for finite sums the function f need not be decreasing for the integral to provide a good approximation. The Euler–Mclaurin summation formula makes the connection between the sum and the integral explicit for sufficiently smooth functions. In this appendix we give a statement and proof of the formula and a few applications.

Start with a differentiable function defined on a set that contains the interval $[m, n]$ , where m and n are integers. Let $m \leq j < n$ , where j is an integer. As a first approximation we consider

$$
\int_ {j} ^ {j + 1} f (x) d x \approx \frac {1}{2} (f (j) + f (j + 1)).\tag{D.1.1}
$$

It is possible to express the error in this approximation as an integral. Observe that

$$
\begin{array}{c} \frac {1}{2} (f (j) + f (j + 1)) = \int_ {j} ^ {j + 1} \frac {d}{d x} \left[ \left(x - j - \frac {1}{2}\right) f (x) \right] d x \\ = \int_ {j} ^ {j + 1} f (x) d x + \int_ {j} ^ {j + 1} \left(x - j - \frac {1}{2}\right) f ^ {\prime} (x) d x. \end{array}\tag{D.1.2}
$$

Set $j = m, m + 1, \ldots, n - 1$ to get

$$
\frac {1}{2} (f (m) + f (m + 1)) = \int_ {m} ^ {m + 1} f (x) d x + \int_ {m} ^ {m + 1} \left(x - m - \frac {1}{2}\right) f ^ {\prime} (x) d x,
$$

$$
\begin{array}{c} \frac {1}{2} (f (m + 1) + f (m + 2)) = \int_ {m + 1} ^ {m + 2} f (x) d x + \int_ {m + 1} ^ {m + 2} \left(x - (m + 1) - \frac {1}{2}\right) f ^ {\prime} (x) d x, \\ \frac {1}{2} (f (n - 1) + f (n)) = \int_ {n - 1} ^ {n} f (x) d x + \int_ {n - 1} ^ {n} \left(x - (n - 1) - \frac {1}{2}\right) f ^ {\prime} (x) d x. \end{array}
$$

The second integrals on the right can be added together if we note that the integrand can be written as $(x - [x] - \frac{1}{2})f'(x)$ . Addition gives

$$
\sum_ {m + 1} ^ {n - 1} f (k) + \frac {1}{2} (f (m) + f (n)) = \int_ {m} ^ {n} f (x) d x + \int_ {m} ^ {n} \left(x - [ x ] - \frac {1}{2}\right) f ^ {\prime} (x) d x.\tag{D.1.3}
$$

This is a particular case of the Euler–Maclaurin formula. To put it in a slightly different form, set $B_{1}(x) = x - \frac{1}{2}$ , so that $B_{1}(x - [x]) = x - [x] - \frac{1}{2}$ . Also let $B_{1} = B_{1}(0) = -1/2$ . Now write (D.1.3) as

$$
\sum_ {m + 1} ^ {n} f (k) + B _ {1} \{f (n) - f (m) \} = \int_ {m} ^ {n} f (x) d x + \int_ {m} ^ {n} B _ {1} (x - [ x ]) f ^ {\prime} (x) d x.\tag{D.1.4}
$$

Recall that $B_{1}(x)$ is the first Bernoulli polynomial and $B_{1}$ the first Bernoulli number. As an application take $f(x) = \log x$ and $m = 1$ in (D.1.4) to get

$$
\log n! - \left(n + \frac {1}{2}\right) \log n + n = 1 + \int_ {1} ^ {n} \frac {B _ {1} (x - [ x ])}{x} d x.\tag{D.1.5}
$$

Since $B_{1}(x - [x])$ is periodic of period 1 and

$$
\int_ {0} ^ {1} B _ {1} (x - [ x ]) d x = \int_ {t} ^ {t + 1} B _ {1} (x - [ x ]) d x = 0\tag{D.1.6}
$$

for any $t \geq 0$ , we see that the limit as $n \to \infty$ in (D.1.5) exists and is equal to

$$
1 + \int_ {1} ^ {\infty} \frac {B _ {1} (x - [ x ])}{x} d x.\tag{D.1.7}
$$

This is exactly Stirling's approximation, if we can show that the expression (D.1.7) equals $\frac{1}{2}\log 2\pi$ . We prove this later by a method different from the one given in Chapter 1, which uses Wallis's formula.

Formula (D.1.4) was obtained by one integration by parts. With Stirling's formula in mind, it makes sense to repeat the process. This would give an expression with higher derivatives of $f(x)$ . If $f(x) = \log x$ , then $f'(x) = 1/x$ , $f''(x) = -1/x^2$ , and so on. These quantities get small for large x and so an extension of (D.1.4) would be useful.

## D.2 The Euler–Maclaurin Formula

Let $\tilde{B}_{2}(x)$ be a primitive (antiderivative) of $B_{1}(x - [x]) = \tilde{B}_{1}(x)$ . It follows from (D.1.6) that $\tilde{B}_{2}$ is periodic with period one. In particular, this implies that $\tilde{B}_{2}(0) = \tilde{B}_{2}(1) = \cdots = \tilde{B}_{2}(j) = \tilde{B}_{2}(j + 1) = \cdots$ . Now, integration by parts gives

$$
\int_ {j} ^ {j + 1} \tilde {B} _ {1} (x) f ^ {\prime} (x) d x = \tilde {B} _ {2} (0) \left(f ^ {\prime} (j + 1) - f ^ {\prime} (j)\right) - \int_ {j} ^ {j + 1} \tilde {B} _ {2} (x) f ^ {\prime \prime} (x) d x.
$$

We assume that $f$ has continuous derivatives of as high an order as necessary. Sum from $j = m$ to $j = n$ to get

$$
\int_ {m} ^ {n} \tilde {B} _ {1} (x) f ^ {\prime} (x) d x = \tilde {B} _ {2} (0) \left(f ^ {\prime} (n) - f ^ {\prime} (m)\right) - \int_ {m} ^ {n} \tilde {B} _ {2} (x) f ^ {\prime \prime} (x) d x.\tag{D.2.1}
$$

Note that it was the periodicity of $\tilde{B}_{2}(x)$ that gave us the simple expression on the right side of Equation (D.2.1). This suggests that we should choose the constant of integration in $\tilde{B}_{2}(x)$ such that

$$
\int_ {0} ^ {1} \tilde {B} _ {2} (x) d x = \int_ {t} ^ {t + 1} \tilde {B} _ {2} (x) d x = 0.\tag{D.2.2}
$$

Let $\frac{1}{2} B_2(x) = \tilde{B}_2(x)$ for $0 \leq x \leq 1$ , so that $\tilde{B}_2(x) = \frac{1}{2} B_2(x - [x])$ . From the definition of $\tilde{B}_2(x)$ , it follows that

$$
B _ {2} (x) = x ^ {2} - x + \frac {1}{6},
$$

which is the second Bernoulli polynomial. We state the general Euler–Maclaurin formula in the next theorem:

Theorem D.2.1 Suppose f has continuous derivatives up to order s. Then

$$
\begin{array}{l} \sum_ {m + 1} ^ {n} f (x) = \int_ {m} ^ {n} f (x) d x + \sum_ {\ell = 1} ^ {s} (- 1) ^ {\ell} \frac {B _ {\ell}}{\ell !} \big \{f ^ {(\ell - 1)} (n) - f ^ {(\ell - 1)} (m) \big \} \\ \qquad + \frac {(- 1) ^ {s - 1}}{s !} \int_ {m} ^ {n} B _ {s} (x - [ x ]) f ^ {(s)} (x) d x, \end{array}
$$

where $B_{s}(x)$ are the Bernoulli polynomials and $B_{\ell} = B_{\ell}(0)$ , the Bernoulli numbers.

Proof. As in the derivation of (D.2.1), apply integration by parts successively to obtain a sequence of periodic functions $\tilde{B}_{n}(x)$ such that $\tilde{B}_{n}^{\prime}(x)=\tilde{B}_{n-1}(x)$ (0<x<1, $n\geq1$ ) and $\int_{0}^{1}\tilde{B}_{n}(x)dx=0, n\geq1$ . With respect to these functions,

we obtain the formula

$$
\begin{array}{c} \sum_ {m + 1} ^ {n} f (k) = \int_ {m} ^ {n} f (x) d x + \sum_ {\ell = 1} ^ {s} (- 1) ^ {\ell} \tilde {B} _ {\ell} (0) \bigl \{f ^ {(\ell - 1)} (n) - f ^ {(\ell - 1)} (m) \bigr \} \\ + (- 1) ^ {s - 1} \int_ {m} ^ {n} \tilde {B} _ {s} (x) f ^ {(s)} (x) d x. \end{array}
$$

To show the relation of $\tilde{B}_{\ell}(x)$ to Bernoulli polynomials, consider the generating function

$$
G (x, t) := \sum_ {0} ^ {\infty} \tilde {B} _ {n} (x) t ^ {n}, \quad \text { where } \tilde {B} _ {0} (x) = 1,\tag{D.2.3}
$$

of the sequence $\{\tilde{B}_{\ell}(x)\}$ . Observe that for $0 < x < 1$ ,

$$
\frac {\partial G}{\partial x} = \sum_ {n = 1} ^ {\infty} \tilde {B} _ {n} ^ {\prime} (x) t ^ {n} = \sum_ {n = 1} ^ {\infty} \tilde {B} _ {n - 1} (x) t ^ {n} = t \sum_ {n = 0} ^ {\infty} \tilde {B} _ {n} (x) t ^ {n} = t G.
$$

We then have

$$
G (x, t) = A (t) e ^ {x t}.\tag{D.2.4}
$$

Use $\int_0^1\tilde{B}_n(x)dx = 0$ in (D.2.3) and (D.2.4) to obtain

$$
1 = A (t) \frac {e ^ {t} - 1}{t} \quad \text {or} \quad A (t) = \frac {t}{e ^ {t} - 1}.
$$

Thus

$$
G (x, t) = \frac {t e ^ {x t}}{e ^ {t} - 1} = \sum_ {0} ^ {\infty} B _ {n} (x) \frac {t ^ {n}}{n !},\tag{D.2.5}
$$

and

$$
\tilde {B} _ {n} (x) = \frac {B _ {n} (x)}{n !} \quad \text { for } 0 <   x <   1.
$$

By the periodicity of $\tilde{B}_n(x)$ we arrive at

$$
\tilde {B} _ {n} (x) = \frac {1}{n !} B _ {n} (x - [ x ]) \quad \text { for   all } x.
$$

Although this formal argument has not been justified, it can be done easily since the generating function (D.2.5) is analytic in the disk $|t| < 2\pi$ . This proves the theorem. ■

## D.3 Applications

Take $f(x) = x^{-s} \log x, m = 1$ , and $n = N$ in (D.1.3) to get

$$
\begin{array}{l} \sum_ {n = 2} ^ {N} \frac {\log n}{n ^ {s}} = \frac {N ^ {1 - s} \log N}{1 - s} + \frac {1}{(s - 1) ^ {2}} - \frac {N ^ {1 - s}}{(s - 1) ^ {2}} \\ \qquad + \frac {1}{2} (N ^ {- s} \log N) + \int_ {1} ^ {N} \frac {x - [ x ] - \frac {1}{2}}{x ^ {s + 1}} (1 - s \log x) d x. \end{array}
$$

Let $\operatorname{Re}s > 1$ and $N \to \infty$ to obtain

$$
\zeta^ {\prime} (s) = \frac {- 1}{(s - 1) ^ {2}} - \int_ {1} ^ {\infty} \frac {x - [ x ] - \frac {1}{2}}{x ^ {s + 1}} (1 - s \log x) d x.
$$

The integral on the right side of the equality converges for $\operatorname{Re} s > -1$ by Abel's test. So

$$
\zeta^ {\prime} (0) = - 1 - \int_ {1} ^ {\infty} \frac {x - [ x ] - \frac {1}{2}}{x} d x.\tag{D.3.1}
$$

By Corollary 1.3.3 we have $\zeta'(0) = -\frac{1}{2} \log 2\pi$ . Thus the constant (D.1.7) in Stirling's formula is $\frac{1}{2} \log 2\pi$ .

As another application, we prove the following useful theorem on the order of $\zeta(s)$ and $\zeta'(s)$ for large $\operatorname{Im} s$ .

Theorem D.3.1 Let $s = \sigma + it$ . For $1 - \frac{A}{\log |t|} \leq \sigma \leq 2$ , where A is any positive constant, and $|t|$ large enough,

$$
\zeta (s) = O (\log | t |)
$$

and

$$
\zeta^ {\prime} (s) = O (\log^ {2} | t |).
$$

Proof. In (D.1.3), set $f(x) = x^{-s}$ , $m = N$ , and let $n \to \infty$ to arrive at

$$
\zeta (s) = \sum_ {n = 1} ^ {N} \frac {1}{n ^ {s}} + \frac {N ^ {1 - s}}{s - 1} - \frac {1}{2} N ^ {- s} - s \int_ {N} ^ {\infty} \frac {x - [ x ] - \frac {1}{2}}{x ^ {s + 1}} d x.
$$

The integral is $O(|t| / \sigma N^{\sigma})$ . Note that

$$
\left| n ^ {- s} \right| = n ^ {- \sigma} \leq n ^ {- (1 - A / \log | t |)} = O (1 / n),
$$

where the last equality holds for $n \leq |t|$ . Thus, take $N = [|t|]$ to get

$$
\zeta (s) = \sum_ {n = 1} ^ {N} O \left(\frac {1}{n}\right) + O (1) = O (\log | t |).
$$

To derive the result for $\zeta'(s)$ , take $f(x) = x^{-s} \log x$ and do a similar calculation. See Rademacher [1973, p. 100], if necessary.

We complete this section with a proof of the following theorem stated in Chapter 1.

Theorem D.3.2 Let $z \in \mathbb{C} - (-\infty, 0]$ . Then

$$
\begin{array}{l} \log \Gamma (z) = \left(z - \frac {1}{2}\right) \log z - z + \sum_ {j = 1} ^ {m} \frac {B _ {2 j}}{2 j (2 j - 1)} \frac {1}{z ^ {2 j - 1}} \\ \qquad + \frac {1}{2} \log 2 \pi - \frac {1}{2 m} \int_ {0} ^ {\infty} \frac {B _ {2 m} (x - [ x ])}{(x + z) ^ {2 m}} d x. \end{array}
$$

Proof. Start with the following expression of the gamma function:

$$
\Gamma (z) = \lim _ {n \rightarrow \infty} \prod_ {\ell = 1} ^ {n} \frac {\ell}{z + \ell - 1} \left(\frac {\ell + 1}{\ell}\right) ^ {z - 1}.
$$

Then

$$
\log \Gamma (z) = \lim _ {n \rightarrow \infty} \left[ (z - 1) \log (n + 1) - \sum_ {\ell = 1} ^ {n} \log \frac {z + \ell - 1}{\ell} \right],\tag{D.3.2}
$$

where the principal branch of the log function in $\mathbb{C} - (-\infty, 0]$ is chosen. In Theorem D.2.1, take

$$
f (x) = \log {\frac {x + z - 1}{x}} = \log (x + z - 1) - \log x
$$

to get

$$
\begin{array}{l} \sum_ {\ell = 1} ^ {n} \log \frac {z + \ell - 1}{\ell} = \log z + \sum_ {\ell = 2} ^ {n} \log \frac {z + \ell - 1}{\ell} \\ \qquad = \log z + \int_ {1} ^ {n} [ \log (x + z - 1) - \log x ] d x \\ \qquad + \sum_ {j = 1} ^ {m} \frac {B _ {2 j}}{2 j (2 j - 1)} \left[ \frac {1}{(n + z - 1) ^ {2 j - 1}} - \frac {1}{n ^ {2 j - 1}} - \frac {1}{z ^ {2 j - 1}} + 1 \right] \\ \qquad + \frac {1}{2} [ \log (n + z - 1) - \log n - \log z ] \\ \qquad + \frac {1}{2 m} \int_ {0} ^ {n} B _ {2 m} (x - [ x ]) \left[ \frac {1}{(z + x - 1) ^ {2 m}} - \frac {1}{x ^ {2 m}} \right] d x. \end{array}
$$

Here we have used the fact that $B_{1} = -1/2$ and $B_{2j+1} = 0$ for $j \geq 1$ . Compute the first of the above integrals and observe that after some cancellation the terms

that involve $n$ are

$$
\begin{array}{l} (n + z - 1) \log (n + z - 1) - n \log n + \frac {1}{2} \log \frac {n + z - 1}{n} \\ + \sum_ {j = 1} ^ {m} \frac {B _ {2 j}}{2 j (2 j - 1)} \left[ \frac {1}{(n + z - 1) ^ {2 j - 1}} - \frac {1}{n ^ {2 j - 1}} \right]. \end{array}
$$

Subtract this from $(z - 1)\log (n + 1)$ and let $n\to \infty$ to compute the limit in (D.3.2). The result is

$$
\begin{array}{l} \log \Gamma (z) = \left(z - \frac {1}{2}\right) \log z - z + 1 + \sum_ {j = 1} ^ {m} \frac {B _ {2 j}}{2 j (2 j - 1)} \left(\frac {1}{z ^ {2 j - 1}} - 1\right) \\ - \frac {1}{2 m} \int_ {1} ^ {\infty} B _ {2 m} (x - [ x ]) \left[ \frac {1}{(x + z - 1) ^ {2 m}} - \frac {1}{x ^ {2 m}} \right] d x. \end{array} \tag {（7）}\tag{D.3.3}
$$

From (D.1.5) and (D.3.1) we know that

$$
\lim _ {z \rightarrow \infty} [ \log \Gamma (z) - (z - 1 / 2) \log z + z ] = \frac {1}{2} \log 2 \pi .
$$

So let $z \to \infty$ in (D.3.3) to see that

$$
1 - \sum_ {j = 1} ^ {m} \frac {B _ {2 j}}{2 j (2 j - 1)} + \frac {1}{2 m} \int_ {1} ^ {\infty} \frac {B _ {2 m} (x - [ x ])}{x ^ {2 m}} d x = \frac {1}{2} \log 2 \pi .
$$

This result combined with (D.3.3) gives the formula in Theorem D.3.2.

## D.4 The Poisson Summation Formula

In this section we state and prove an important and useful formula from the theory of Fourier series. This is the Poisson summation formula. It has numerous applications though we mention only a few. One consequence of Poisson's formula is the Euler–Maclaurin summation formula.

Start with a result on Fourier series attributed to Jordan. Recall that a function $f(x)$ is said to be of bounded variation on an interval $[a, b]$ (which may be infinite), if there is a constant C > 0 such that for any set of points $x_{0} < x_{1} < \cdots < x_{n}$ in the interval

$$
\sum_ {k = 1} ^ {n} | f (x _ {i}) - f (x _ {i - 1}) | <   C.
$$

If the interval is the whole real line, then we say that f is of bounded total variation. An important though easily proved result is that if f is of bounded variation on $[a, b]$ , then f = g - h, where g and h are increasing functions on $[a, b]$ .

Jordan's theorem is the following: Suppose $f$ is integrable on $[0, 1]$ and periodic with period one. If $f$ is of bounded variation on $[0, 1]$ , then

$$
\frac {f (x +) + f (x -)}{2} = \lim _ {N \rightarrow \infty} \sum_ {| n | \leq N} \left(\int_ {0} ^ {1} f (t) e ^ {- 2 \pi i n t} d t\right) e ^ {2 \pi i n x}.
$$

Poisson's summation formula is contained in the next theorem.

Theorem D.4.1 Suppose g is integrable on $(-\infty, \infty)$ and of bounded total variation. Suppose h is an even, positive, integrable function that is decreasing on $[0, \infty)$ and such that $|g(x)| \leq h(x)$ . Then

$$
\sum_ {n = - \infty} ^ {\infty} \frac {g (x + n +) + g (x + n -)}{2} = \lim _ {N \rightarrow \infty} \sum_ {| n | \leq N} \int_ {- \infty} ^ {\infty} g (t) e ^ {- 2 \pi i n t} d t e ^ {2 \pi i n x}.\tag{D.4.1}
$$

Proof. The inequality

$$
\sum_ {n = - M} ^ {N - 1} | g (x + n) | \leq | g (x) | + \int_ {- M} ^ {N} h (x + t) d t
$$

implies that $\sum_{-\infty}^{\infty} g(x + n)$ is an absolutely convergent series and defines a periodic function $f(x)$ with period one. Moreover, since $g$ is of bounded total variation, $f$ is of bounded variation on $[0, 1]$ . By Jordan's theorem

$$
\frac {f (x +) + f (x -)}{2} = \lim _ {N \rightarrow \infty} \sum_ {| n | \leq N} \int_ {0} ^ {1} f (t) e ^ {- 2 \pi i n t} d t e ^ {2 \pi i n x}.
$$

Now

$$
\begin{array}{l} \int_ {0} ^ {1} f (t) e ^ {- 2 \pi i n t} d t = \int_ {0} ^ {1} \sum_ {- \infty} ^ {\infty} g (m + t) e ^ {- 2 \pi i n t} d t \\ \qquad = \sum_ {- \infty} ^ {\infty} \int_ {0} ^ {1} g (m + t) e ^ {- 2 \pi i n t} d t \\ \qquad = \sum_ {- \infty} ^ {\infty} \int_ {m} ^ {m + 1} g (u) e ^ {- 2 \pi i n u} d u \\ \qquad = \int_ {- \infty} ^ {\infty} g (u) e ^ {- 2 \pi i n u} d u. \end{array}
$$

The summation in the second line can be taken outside the integral by the dominated convergence theorem. ■

Remark D.4.1 If the series on the right-hand side in Theorem D.4.1 is absolutely convergent, then we can write

$$
\sum_ {n = - \infty} ^ {\infty} \frac {g (x + n +) + g (x + n -)}{2} = \sum_ {n = - \infty} ^ {\infty} \left(\int_ {- \infty} ^ {\infty} g (t) e ^ {- 2 \pi i n t} d t e ^ {2 \pi i n x}\right).
$$

An interesting example of Poisson's formula connects the Poisson kernel for the upper half plane given by $g(x) = y / (x^2 + y^2)$ , $y > 0$ , with the kernel for the unit disk given by $(1 - r^2) / (1 - 2r\cos x + r^2)$ . Observe that with $g$ as defined here,

$$
\hat {g} (t) = \int_ {- \infty} ^ {\infty} \frac {y e ^ {- 2 \pi i t x}}{x ^ {2} + y ^ {2}} d x = \pi e ^ {- 2 \pi y | t |}.
$$

The reader may verify this by contour integration or by other means. Substitution of this in Theorem D.4.1 gives

$$
\sum_ {n = - \infty} ^ {\infty} \frac {y}{y ^ {2} + (x + n) ^ {2}} = \sum_ {n = - \infty} ^ {\infty} e ^ {- 2 \pi y | n |} e ^ {2 \pi i n x} = \frac {1 - e ^ {- 4 \pi y}}{1 - 2 e ^ {- 2 \pi y} \cos 2 \pi x + e ^ {- 4 \pi y}}.
$$

The partial fraction expansions for the trigonometric functions can also be derived from Theorem D.4.1. Take s > 0 and set

$$
g (t) = \left\{ \begin{array}{l l} e ^ {- s t}, & t \geq 0, \\ 0, & t <   0. \end{array} \right.
$$

The left side of Poisson's formula becomes

$$
\sum_ {n > - x} e ^ {- s (n + x)} + \left\{ \begin{array}{l l} 1 / 2, & x \text {   integer }, \\ 0, & \text { otherwise }. \end{array} \right.
$$

The right-hand side is given by

$$
\sum_ {n = - \infty} ^ {\infty} \frac {e ^ {2 \pi i n x}}{s + 2 \pi i n}.
$$

When $x = 0$ , we get

$$
\frac {e ^ {s} + 1}{e ^ {s} - 1} = \frac {1}{s} + \sum_ {n = 1} ^ {\infty} \left(\frac {2}{s + 2 \pi i n} + \frac {1}{s - 2 \pi i n}\right).
$$

By analytic continuation, we can take $s = 2\pi iy$ . The result is

$$
\pi \cot \pi y = \frac {1}{y} + \sum_ {n = 1} ^ {\infty} \left(\frac {1}{y + n} + \frac {1}{y - n}\right).
$$

When $x = 1 / 2$ , we obtain

$$
{\frac {e ^ {s / 2}}{e ^ {s} - 1}} = {\frac {1}{s}} + \sum_ {n = 1} ^ {\infty} \left({\frac {(- 1) ^ {n}}{s + 2 \pi i n}} + {\frac {(- 1) ^ {n}}{s - 2 \pi i n}}\right).
$$

This time, $s = 2\pi iy$ gives

$$
\pi \csc \pi y = \frac {1}{y} + \sum_ {n = 1} ^ {\infty} (- 1) ^ {n} \left(\frac {1}{y + n} + \frac {1}{y - n}\right).
$$

An important transformation formula for theta functions follows from the Poisson summation formula by taking $g(x) = e^{-s\pi x^{2}}$ . The formula is

$$
\sum_ {n = - \infty} ^ {\infty} e ^ {- s \pi (n + x) ^ {2}} = s ^ {- 1 / 2} \sum_ {n = - \infty} ^ {\infty} e ^ {- \pi n ^ {2} / s} e ^ {2 \pi i n x}.\tag{D.4.2}
$$

The Euler–Maclaurin formula follows from the Poisson summation formula by taking

$$
g (x) = \left\{ \begin{array}{l l} f (x), & \text { for } a \leq x \leq b, \\ 0, & \text { otherwise }. \end{array} \right.
$$

Here a and b are assumed to be nonnegative integers and $f(x)$ is continuously differentiable in $[a, b]$ . This implies that f is of bounded variation on $[a, b]$ and hence $g(x)$ is of bounded total variation. Use this $g(x)$ in (D.4.1). The result is

$$
\begin{array}{c} \frac {1}{2} (f (a) + f (b)) + \sum_ {k = a + 1} ^ {b - 1} f (k) = \lim _ {N \to \infty} \sum_ {| n | \leq N} \int_ {a} ^ {b} f (t) e ^ {- 2 \pi i n t} d t \\ = \int_ {a} ^ {b} f (t) d t + 2 \sum_ {n = 1} ^ {\infty} \int_ {a} ^ {b} f (t) \cos 2 \pi n t d t. \end{array}\tag{D.4.3}
$$

Integration by parts gives

$$
\int_ {a} ^ {b} f (t) \cos 2 \pi n t d t = - \int_ {a} ^ {b} f ^ {\prime} (t) \frac {\sin 2 n \pi t}{2 n \pi} d t.
$$

Also,

$$
2 \sum_ {n = 1} ^ {\infty} \frac {\sin 2 n \pi x}{2 n \pi} = - B _ {1} (x - [ x ]),
$$

except when $x$ is an integer (see Exercise 44 in Chapter 1). Thus, by the dominated convergence theorem, we can write (D.4.2) as

$$
\sum_ {a <   n \leq b} f (n) = \int_ {a} ^ {b} f (t) d t - B _ {1} (f (b) - f (a)) + \int_ {a} ^ {b} f ^ {\prime} (x) B _ {1} (x - [ x ]) d x.
$$

If we assume that $f^{(m)}(x)$ is continuously differentiable, then the application of

$$
\frac {d B _ {n} (x)}{d x} = n B _ {n - 1} (x), \quad 0 <   x <   1,
$$

and successive integration by parts gives Theorem D.2.1. For other applications and extensions of the summation formulas studied here, see Berndt [1975].

## Exercises

1. Prove that with the notation and conditions of Theorem D.3.1 $\zeta'(s) = O(\log^2 |t|)$ .

2. Define $\Delta f(0) = f(1) - f(0)$ . Show that if $f(x)$ is a polynomial of degree $m$ , then

$$
f (0) = \int_ {0} ^ {1} f (x) d x + \sum_ {j = 1} ^ {m} \frac {B _ {j}}{j} \Delta f ^ {(j - 1)} (0).
$$

3. Use the Euler–Maclaurin formula to obtain the relation

$$
\sum_ {k = 1} ^ {n} \frac {1}{k} = \log n + \gamma + \frac {1}{2 n} - \sum_ {k = 1} ^ {p - 1} \frac {B _ {2 k}}{2 k n ^ {2 k}} - \frac {\theta B _ {2 p}}{2 p n ^ {2 p}},
$$

where $0 < \theta < 1$ and $\gamma$ is Euler's constant.

4. Show that there is a constant $C$ such that

$$
\sum_ {2 \leq n \leq x} \frac {1}{n \log n} = \log \log x + C + O \left(\frac {1}{x \log x}\right).
$$

5. Use the Poisson summation formula to prove that

$$
\sum_ {- \infty} ^ {\infty} e ^ {- s (n + x) ^ {2}} = \frac {1}{\sqrt {s}} \sum_ {- \infty} ^ {\infty} e ^ {- \pi n ^ {2} / s} e ^ {2 \pi i n x}.
$$

6. Use Poisson summation to obtain the following theorem of Lipschitz: Suppose $\operatorname{Re} x > 0, 0 < \alpha \leq 1$ , and $\operatorname{Re} s > 1$ . Then

$$
\frac {(2 \pi) ^ {s}}{\Gamma (s)} \sum_ {n = 0} ^ {\infty} (n + \alpha) ^ {s - 1} e ^ {- 2 \pi x (n + \alpha)} = \sum_ {n = - \infty} ^ {\infty} \frac {e ^ {2 \pi i n \alpha}}{(x + n i) ^ {s}}.
$$

(For a different proof where $\alpha = 1$ , see Exercise 37 in Chapter 2.)

7. Suppose $a, b$ , and $c$ are integers such that $ac + b$ is even. Use Poisson summation to prove the reciprocity for Gaussian sums

$$
\sum_ {n = 0} ^ {| c | - 1} e ^ {\pi i (a n ^ {2} + b n) / c} = \sqrt {\left| \frac {c}{a} \right|} e ^ {\pi i (| a c | - b ^ {2}) / (4 a c)} \sum_ {n = 0} ^ {| a | - 1} e ^ {- \pi i (c n ^ {2} + b n) / a}.
$$

# Lagrange Inversion Formula

## E.1 Reversion of Series

There are situations in analysis in which one knows a series expansion for $y(x)$ but would like to obtain the series for x in terms of y. Newton, for example, encountered such a problem when he had the series for $\sin^{-1}x$ by integrating the expansion of $(1-x^{2})^{-1/2}$ term by term and he wanted the series for $\sin x$ . Some results of Newton on reversion of series can be found in Newton [1960, p. 147].

Suppose a series for $x$ in powers of $y$ is required when $x = y\phi(x)$ . Assume that $\phi$ is analytic in a neighborhood of $x = 0$ with $\phi(0) \neq 0$ . Then

$$
y = x / \phi (x) = \sum_ {n = 1} ^ {\infty} a _ {n} x ^ {n}, \quad a _ {1} \neq 0.\tag{E.1.1}
$$

We shall see below that Lagrange's inversion formula gives

$$
x = \sum_ {n = 1} ^ {\infty} b _ {n} y ^ {n},
$$

where

$$
b _ {n} = \frac {1}{n !} \frac {d ^ {n - 1}}{d x ^ {n - 1}} [ \phi (x) ^ {n} ] _ {x = 0}.
$$

This means that $nb_{n}$ is the coefficient of $x^{n-1}$ in the expansion of $\phi^{n}(x)$ or the coefficient of $x^{-1}$ in the expansion of $1/y^{n}$ .

More generally, suppose that (E.1.1) holds and that $f(x)$ is an analytic function in a neighborhood of $x = 0$ . Then Lagrange's formula is

$$
f (x) = f (0) + \sum_ {n = 1} ^ {\infty} \frac {y ^ {n}}{n !} \left[ \frac {d ^ {n - 1}}{d x ^ {n - 1}} \left(f ^ {\prime} (x) \phi^ {n} (x)\right) \right] _ {x = 0}.\tag{E.1.2}
$$

## E.2 A Basic Lemma

The proof of Lagrange's formula (E.1.2) depends on a simple lemma given below. The treatment here follows that of Gessel and Stanton [1982], which is based on the work of Jacobi [1830]. See also Bromwich [1926]. An extension of Lagrange inversion to several variables is in Good [1960] and $q$ -analogs are discussed in Stanton [1988]. A history of this formula can be found in W. Johnson's unpublished manuscript, Notes on the Lagrange inversion formula.

Define the residue of a formal Laurent series $f(x) = \sum_{j=-m}^{\infty} a_j x^j$ by $\text{Res}[f(x)] = a_{-1}$ . The next lemma states that the residue does not change under a certain change of variables.

Lemma E.2.1 Let $G(x) = \sum_{j=-m}^{\infty} a_j x^j$ and $h(x) = \sum_{i=1}^{\infty} b_i x^i$ , where $b_1 \neq 0$ . Then $\operatorname{Res}[G(h(x))h'(x)] = \operatorname{Res}[G(x)]$ .

Proof. Since both sides of the equation are linear in G, it is sufficient to prove it for $G(x) = x^{m}$ . Since $\operatorname{Res}[g'(x)] = 0$ for any Laurent series $g(x)$ , it follows that, for $m \neq -1$ ,

$$
\operatorname{Res} \left[ h ^ {m} (x) h ^ {\prime} (x) \right] = \frac {1}{m + 1} \operatorname{Res} \left[ \left\{h ^ {m + 1} (x) \right\} ^ {\prime} \right] = 0.
$$

For $m = -1$ , let $h(x) = b_{1}xf(x)$ . Then

$$
\operatorname{Res} \left[ \frac {h ^ {\prime} (x)}{h (x)} \right] = \operatorname{Res} \left[ \frac {1}{x} + \frac {f ^ {\prime} (x)}{f (x)} \right] = 1 + \operatorname{Res} [ \{\log f (x) \} ^ {\prime} ] = 1.
$$

The lemma is proved.

To prove (E.1.2) note that $y = a_{1}x + a_{2}x^{2} + \cdots$ (x a complex variable) is conformal in a neighborhood of 0, because $a_{1} \neq 0$ , and so x can be expanded in powers of y. Since $f(x)$ is analytic, it can be expanded in powers of y. Suppose that

$$
f (x) = f (0) + \sum_ {n = 1} ^ {\infty} c _ {n} y ^ {n}.
$$

Then

$$
f ^ {\prime} (x) = \sum_ {n = 1} ^ {\infty} n c _ {n} y ^ {n - 1} \frac {d y}{d x}.
$$

Let $G(x) = \sum_{n=1}^{\infty} n c_n x^{n-1}$ . By Lemma E.2.1,

$$
\operatorname{Res} \left[ \frac {f ^ {\prime} (x) \phi^ {r} (x)}{x ^ {r}} \right] = \operatorname{Res} \left[ \frac {f ^ {\prime} (x)}{y ^ {r}} \right] = \operatorname{Res} \left[ \frac {G (y) d y / d x}{y ^ {r}} \right] = \operatorname{Res} \left[ \frac {G (x)}{x ^ {r}} \right] = r c _ {r}.
$$

But the Taylor series of $f'(x)\phi^r (x)$ is

$$
\sum_ {n = 0} ^ {\infty} \frac {x ^ {n}}{n !} \left[ \frac {d ^ {n}}{d x ^ {n}} (f ^ {\prime} (x) \phi^ {r} (x)) \right] _ {x = 0},
$$

and so

$$
\operatorname{Res} \left[ \frac {f ^ {\prime} (x) \phi^ {r} (x)}{x ^ {r}} \right] = \frac {1}{(r - 1) !} \left[ \frac {d ^ {r - 1}}{d x ^ {r - 1}} \left(f ^ {\prime} (x) \phi^ {r} (x)\right) \right] _ {x = 0}.
$$

Thus

$$
c _ {r} = \frac {1}{r !} \left[ \frac {d ^ {r - 1}}{d x ^ {r - 1}} (f ^ {\prime} (x) \phi^ {r} (x)) \right] _ {x = 0},
$$

which proves Lagrange's formula (E.1.2).

A variant of (E.1.2) is the formula

$$
\frac {f (x)}{1 - y \phi^ {\prime} (x)} = \sum_ {n = 0} ^ {\infty} \frac {y ^ {n}}{n !} \left[ \frac {d ^ {n}}{d x ^ {n}} (f (x) \phi^ {n} (x)) \right] _ {x = 0},\tag{E.2.1}
$$

where $y$ is defined by (E.1.1). To prove (E.2.1), note that since $x - y\phi(x) = 0$ , we have

$$
1 - \phi (x) \frac {d y}{d x} - y \phi^ {\prime} (x) = 0,
$$

or

$$
{\frac {d y}{d x}} = {\frac {1 - y \phi^ {\prime} (x)}{\phi (x)}}.\tag{E.2.2}
$$

Take the derivative of (E.1.2) with respect to $x$ and use (E.2.2) to get

$$
\frac {f ^ {\prime} (x) \phi (x)}{1 - y \phi^ {\prime} (x)} = \sum_ {n = 0} ^ {\infty} \frac {y ^ {n}}{n !} \left[ \frac {d ^ {n}}{d x ^ {n}} \left(f ^ {\prime} (x) \phi (x) \phi^ {n} (x)\right) \right] _ {x = 0}.
$$

Set $F(x) = f'(x)\phi(x)$ to obtain (E.2.1).

## E.3 Lambert's Identity

Lagrange's inversion formula can be used to obtain a number of interesting series expansions for specific functions. A few examples are given in the exercises. Here we derive an identity of Lambert. This is given by

$$
(1 + x) ^ {\alpha} = 1 + \sum_ {n = 1} ^ {\infty} \frac {\alpha}{\alpha + n \beta} \binom {\alpha + \beta n} {n} y ^ {n},\tag{E.3.1}
$$

where $y = x(1 + x)^{-\beta}$ . Take $f(x) = (1 + x)^{\alpha}$ and $\phi(x) = (1 + x)^{\beta}$ in (E.1.2). Then

$$
(1 + x) ^ {\alpha} = 1 + \sum_ {n = 1} ^ {\infty} \frac {y ^ {n}}{n !} \left[ \frac {d ^ {n - 1}}{d x ^ {n - 1}} (\alpha (1 + x) ^ {n \beta + \alpha - 1}) \right] _ {x = 0}.
$$

The expression in square brackets equals

$$
\alpha (n \beta + \alpha - 1) \dots (n \beta + \alpha - n + 1) = \alpha (n - 1)! \binom {\alpha + n \beta - 1} {n - 1},
$$

and this gives (E.3.1). The identity corresponding to (E.2.1) is

$$
\frac {(1 + x) ^ {\alpha + 1}}{1 + x (1 - \beta)} = 1 + \sum_ {n = 1} ^ {\infty} \binom {\alpha + \beta n} {n} y ^ {n}.\tag{E.3.2}
$$

An interesting binomial identity comes from (E.3.1) and (E.3.2). Equate the coefficient of $y^{n}$ on both sides of

$$
(1 + x) ^ {\gamma} \frac {(1 + x) ^ {\alpha + 1}}{1 + x (1 - \beta)} = \frac {(1 + x) ^ {\alpha + \gamma + 1}}{1 + x (1 - \beta)}.
$$

The result is

$$
\sum_ {k = 0} ^ {n} \frac {\gamma}{\gamma + \beta k} \binom {\gamma + \beta k} {k} \binom {\alpha + \beta (n - k)} {n - k} = \binom {\alpha + \gamma + \beta n} {n}.\tag{E.3.3}
$$

## E.4 Whipple's Transformation

Gessel and Stanton showed how to derive Whipple's transformation, which we obtained in different ways in Chapters 3 and 7, from Lemma E.2.1.

Theorem E.4.1 Suppose $A(x)$ , $B(x)$ , $C(x)$ , and $D(x)$ are power series whose coefficients of $x^{k}$ are $A_{k}$ , $B_{k}$ , $C_{k}$ , and $D_{k}$ respectively. Suppose

$$
(1 - x) ^ {- \alpha} A (x / (1 - x) ^ {\beta + 1}) = B (x),\tag{E.4.1}
$$

$$
(1 + \beta x) (1 - x) ^ {- \gamma} C (x / (1 - x) ^ {\beta + 1}) = D (x).\tag{E.4.2}
$$

If $n(\beta + 1) = 1 - \alpha - \gamma$ , then

$$
\sum_ {k = 0} ^ {n} B _ {k} D _ {n - k} = \sum_ {k = 0} ^ {n} A _ {k} C _ {n - k}.
$$

Proof. First note that

$$
\operatorname{Res} \left[ \frac {B (x) D (x)}{x ^ {n + 1}} \right] = \text { coefficient   of } x ^ {n} \text { in } B (x) D (x) = \sum_ {k = 0} ^ {n} B _ {k} D _ {n - k}.
$$

Now write $h(x) = x(1 - x)^{-\beta - 1}$ so that $h'(x) = (1 + \beta x)(1 - x)^{-\beta - 2}$ and

$$
\begin{array}{r l} \frac {B (x) D (x)}{x ^ {n + 1}} & = \frac {(1 + \beta x) (1 - x) ^ {- \alpha - \gamma} A (x / (1 - x) ^ {\beta + 1}) C (x / (1 - x) ^ {\beta + 1})}{x ^ {n + 1}} \\ & = \frac {(1 + \beta x) (1 - x) ^ {n (\beta + 1) - 1} A (h (x)) C (h (x))}{x ^ {n + 1}} \\ & = \frac {A (h (x)) C (h (x)) h ^ {\prime} (x)}{[ h (x) ] ^ {n + 1}}. \end{array}
$$

By Lemma E.2.1,

$$
\operatorname{Res} \left[ \frac {B (x) D (x)}{x ^ {n + 1}} \right] = \operatorname{Res} \left[ \frac {A (x) C (x)}{x ^ {n + 1}} \right].
$$

By the remark at the beginning of the proof, this implies that

$$
\sum_ {k = 0} ^ {n} B _ {k} D _ {n - k} = \sum_ {k = 0} ^ {n} A _ {k} C _ {n - k}.
$$

This proves the theorem.

To derive Whipple's transformation for a $_{7}F_{6}$ , recall Whipple's quadratic transformation noted in Chapter 2, namely,

$$
\begin{array}{l} (1 - x) ^ {- a} _ {3} F _ {2} \binom {a / 2, (1 + a) / 2, 1 + a - b - c} {1 + a - b, 1 + a - c}; - \frac {4 x}{(1 - x) ^ {2}} \\ = _ {3} F _ {2} \binom {a, b, c} {1 + a - b, 1 + a - c}; x. \end{array}\tag{E.4.3}
$$

This corresponds to (E.4.1) with $\alpha = a$ and $\beta = 1$ . The transformation corresponding to (E.4.3) is a result of Bailey [1929]:

$$
\begin{array}{l} (1 + x) (1 - x) ^ {- a - 1} _ {3} F _ {2} \left[ \begin{array}{c} (a + 1) / 2, 1 + a / 2, a + 1 - b - c \\ 1 + a - b, 1 + a - c \end{array} ; - \frac {4 x}{(1 - x) ^ {2}} \right] \\ = _ {4} F _ {3} \left[ \begin{array}{c} a, 1 + a / 2, b, c \\ a / 2, 1 + a - b, 1 + a - c \end{array} ; x \right]. \end{array} \tag {E.4}\tag{E.4.4}
$$

This can be obtained from (E.4.3) by differentiation or directly by equating the coefficients of $x^{n}$ . To apply Theorem E.4.1, note that from (E.4.3),

$$
\begin{array}{l} A _ {k} = (a / 2) _ {k} ((1 + a) / 2) _ {k} (1 + a - b - c) _ {k} (- 4) ^ {k} / [ k! (1 + a - b) _ {k} (1 + a - c) _ {k} ], \\ B _ {k} = (a) _ {k} (b) _ {k} (c) _ {k} / [ k! (1 + a - b) _ {k} (1 + a - c) _ {k} ], \end{array}
$$

and from (E.4.4) after renaming the parameters,

$$
\begin{array}{r l} & C _ {k} = ((1 + d) / 2) _ {k} ((2 + d) / 2) _ {k} (1 + d - e - f) _ {k} (- 4) ^ {k} / \\ & \qquad [ k! (1 + d - e) _ {k} (1 + d - f) _ {k} ], \\ & D _ {k} = (d) _ {k} (1 + d / 2) _ {k} (e) _ {k} (f) _ {k} / [ k! (d / 2) _ {k} (1 + d - e) _ {k} (1 + d - f) _ {k} ]. \end{array}
$$

So

$$
\begin{array}{l} \sum_ {k = 0} ^ {n} A _ {k} C _ {n - k} \\ = \frac {(- 4) ^ {n} ((1 + d) / 2) _ {n} ((2 + d) / 2) _ {n} (1 + d - e - f) _ {n}}{n ! (1 + d - e) _ {n} (1 + D - f) _ {n}} \\ \cdot \sum_ {k = 0} ^ {n} \frac {(a / 2) _ {k} ((1 + a) / 2) _ {k} (1 + a - b - c) _ {k} (- n) _ {k} (e - d - n) _ {k} (f - d - n) _ {k}}{k ! (1 + a - b) _ {k} (1 + a - c) _ {k} ((1 - d) / 2 - n) _ {k} (- n - d / 2) _ {k} (e + f - n - d) _ {k}}. \end{array}
$$

Theorem E.4.1 is applicable when 2n = -a - d. This simplifies the expression in the sum. For example, -n - d/2 = a/2, and the terms involving these expressions cancel. After simplification the sum becomes

$$
{ } _ { 4 } F _ { 3 } \bigg ( \begin{array} { c } - n , 1 + a - b - c , e + a + n , f + a + n \\ 1 + a - b , 1 + a - c , e + f + a + n \end{array} ; 1 \bigg ) .
$$

The sum $\sum_{k=0}^{n} B_k D_{n-k}$ leads to a $7F_6$ and the equality

$$
\sum_ {k = 0} ^ {n} B _ {k} D _ {n - k} = \sum_ {k = 0} ^ {n} A _ {k} C _ {n - k}
$$

results in Whipple's theorem

$$
\begin{array}{r l} _ {7} F _ {6} & \binom {a, 1 + a / 2, b, c, e + a + n, f + a + n, - n} {a / 2, 1 + a - b, 1 + a - c, 1 - e - n, 1 - f - n, 1 + a + n}; 1 \\ & = \frac {(a + 1) _ {n} (a + c + f + n) _ {n}}{(e) _ {n} (f) _ {n}} \\ & \times {} _ {4} F _ {3} \binom {1 + a - b - c, e + a + n, f + a + n, - n} {1 + a - b, 1 + a - c, e + f + a + n}; 1 \end{array}
$$

## Exercises

1. Show that

$$
e ^ {\alpha x} = \sum_ {n = 0} ^ {\infty} \frac {\alpha (\alpha + b n) ^ {n - 1}}{n !} (x e ^ {- b x}) ^ {n}
$$

and that

$$
x = \sum_ {n = 1} ^ {\infty} \frac {n ^ {n - 1}}{n !} (x e ^ {- x}) ^ {n}.
$$

2. Show formally that

$$
f (x + a) = \sum_ {n = 0} ^ {\infty} \frac {f ^ {(n)} (a - n b)}{n !} x (x + n b) ^ {n - 1}.
$$

Give sufficient conditions for this to be correct.

3. Show that

$$
(a + x) ^ {\alpha} = \sum_ {k = 0} ^ {\infty} x (x - k b) ^ {k - 1} \frac {(- \alpha) _ {k}}{k !} (- 1) ^ {k} (a + k b) ^ {\alpha - k}.
$$

4. Show that if $f^{-1}(x)$ is the inverse of $f(x)$ and $f(0) = 0$ , then assuming the necessary analyticity of the functions,

$$
f ^ {- 1} (x) = x \left(\frac {x}{f (x)}\right) _ {x = 0} + \frac {x ^ {2}}{2 !} \left(\frac {d}{d x} \left(\frac {x ^ {2}}{f (x)}\right)\right) _ {x = 0} + \dots .
$$

5. Show that

$$
\log (1 + x) = \sum_ {n = 1} ^ {\infty} \binom {n \beta - 1} {n - 1} \frac {y ^ {n}}{n}
$$

when $y = x(1 + x)^{-\beta}$ .

6. Suppose that $x^{m + 1} + ax - b = 0$ . Show that

$$
x = \frac {b}{a} - \frac {b ^ {m + 1}}{a ^ {m + 2}} + \frac {2 m + 2}{2 !} \frac {b ^ {2 m + 1}}{a ^ {2 m + 3}} - \frac {(3 m + 2) (3 m + 3)}{3 !} \frac {b ^ {3 m + 1}}{a ^ {3 m + 4}} + \dots .
$$

Use this formula to find a solution of $x^5 + 4x + 2 = 0$ to four decimal places of accuracy. When $m = 0$ , this series reduces to the geometric series. Write this sum as a hypergeometric series.

7. Use the Lagrange inversion formula to derive the generating function for Laguerre polynomials.

# Series Solutions of Differential Equations

## F.1 Ordinary Points

For readers not familiar with series solutions of differential equations, we give a few basic definitions so that the discussions of the hypergeometric equation in Chapter 2 and of the confluent and Bessel's equations in Chapter 4 are intelligible.

Consider the differential equation

$$
a (x) \frac {d ^ {2} y}{d x ^ {2}} + b (x) \frac {d y}{d x} + c (x) y = 0\tag{F.1.1}
$$

with $a(x), b(x)$ , and $c(x)$ analytic in the neighborhood of $x = x_0$ . We take $x$ to be a complex variable in this discussion. The simplest situation occurs when $a(x_0) \neq 0$ . In this case, $x_0$ is called an ordinary point of the Equation (F.1.1).

It is not difficult to show that if $x_{0}$ is an ordinary point of (F.1.1), then (F.1.1) has a unique solution $f(x)$ analytic in a neighborhood of $x_{0}$ with prescribed values $f(x_{0}) = f_{0}$ and $f'(x_{0}) = f_{1}$ . This implies that there are exactly two linearly independent solutions in a neighborhood of $x_{0}$ . To prove this result, it is convenient to divide (F.1.1) by $a(x)$ and rewrite the equation as

$$
y ^ {\prime \prime} = B (x) y ^ {\prime} + C (x) y.\tag{F.1.2}
$$

Again for convenience, take $x_0 = 0$ . Then

$$
B (x) = \sum_ {n = 0} ^ {\infty} b _ {n} x ^ {n} \quad \text { and } \quad C (x) = \sum_ {n = 0} ^ {\infty} c _ {n} x ^ {n}.
$$

Suppose that (F.1.2) has an analytic solution $f(x)$ with

$$
f (x _ {0}) = f _ {0}, \quad f ^ {\prime} (x _ {0}) = f _ {1}.
$$

Then

$$
f (x) = \sum_ {n = 0} ^ {\infty} f _ {n} x ^ {n}.\tag{F.1.3}
$$

Substitute this series and the series for $B(x)$ and $C(x)$ in (F.1.2); equate the coefficients of $x^n$ . The result is

$$
(n + 2) (n + 1) f _ {n + 2} = \sum_ {k = 0} ^ {n} (n + 1 - k) f _ {n + 1 - k} b _ {k} + \sum_ {k = 0} ^ {n} f _ {n - k} c _ {k},\tag{F.1.4}
$$

$n = 0, 1, 2, \ldots$ . This shows that $f_{0}$ and $f_{1}$ uniquely determine $f_{n}$ for $n \geq 2$ . It is now enough to prove that the series (F.1.3) has a positive radius of convergence. Since the series for $B(x)$ and $C(x)$ have a positive radius of convergence, there exist constants M and R such that

$$
\left| b _ {n} \right| \leq M / R ^ {n} \quad \text { and } \quad \left| c _ {n} \right| \leq M / R ^ {n}.
$$

We show by induction that there exist suitable positive numbers $M_{1}$ and r such that

$$
\left| f _ {n} \right| \leq M _ {1} / r ^ {n}.\tag{F.1.5}
$$

This implies the needed result. Take $M_{1}$ such that $|f_{1}| \leq M_{1}$ and choose r such that r < R, $|f_{1}| \leq M_{1}/r$ , and $M(r/2 + r^{2}) \leq 1$ . Suppose $n \geq 2$ and assume (F.1.5) true up to n - 1. By (F.1.4), the inequality (F.1.5) follows after a small calculation.

## F.2 Singular Points

When $a(x_0) = 0$ and $b(x_0)$ and/or $c(x_0)$ is not zero, then $x = x_0$ is called a singular point of (F.1.1). Divide (F.1.1) by $a(x)$ and write it as

$$
y ^ {\prime \prime} + d (x) y ^ {\prime} + e (x) y = 0.\tag{F.2.1}
$$

Consider first the simplest case where $x_{0}$ is a singular point and $a(x)$ has a simple zero at $x_{0}$ . Then $d(x)$ and $e(x)$ have at most simple poles. Take $x_{0}=0$ . Then

$$
d (x) = \sum_ {n = - 1} ^ {\infty} d _ {n} x ^ {n} \quad \text { and } \quad e (x) = \sum_ {n = - 1} ^ {\infty} e _ {n} x ^ {n}.\tag{F.2.2}
$$

Substitute the series (F.1.3) in (F.2.1) and equate coefficients as before. The reader may check that in this case we get only one solution, since the value of $f_{0}$ determines $f_{n}$ for $n \geq 1$ . Moreover, if $d_{-1}$ is a nonnegative integer, then this method may fail to produce a solution.

Now consider the case where $d(x)$ has at most a simple pole and $e(x)$ at most a double pole. The simplest special case of (F.1.1) that leads to this is when

$$
a (x) = a _ {2} (x - x _ {0}) ^ {2}, \quad b (x) = b _ {1} (x - x _ {0}), \quad c (x) = c _ {0}.\tag{F.2.3}
$$

Two linearly independent solutions exist, at least one of the form $y = (x - x_{0})^{\mu}$ . To determine $\mu$ , substitute this expression for y in (F.1.1) to get

$$
a _ {2} \mu (\mu - 1) + b _ {1} \mu + c _ {0} = 0.\tag{F.2.4}
$$

If this quadratic has two unequal roots, these roots give two independent solutions of (F.1.1). If the two roots equal $\mu_{1}$ (say), then we have the solution $(x - x_{0})^{\mu_{1}}$ . To find the other independent solution, set $y = (x - x_{0})^{\mu_{1}}w$ . The differential equation for w has $\log(x - x_{0})$ as a solution. Thus the second independent solution is $(x - x_{0})^{\mu_{1}}\log(x - x_{0})$ .

## F.3 Regular Singular Points

A point $x = x_0$ is called a regular singular point of (F.1.1) if

$$
\lim _ {x \rightarrow x _ {0}} \frac {(x - x _ {0}) b (x)}{a (x)} \quad \text { and } \quad \lim _ {x \rightarrow x _ {0}} \frac {(x - x _ {0}) ^ {2} c (x)}{a (x)}
$$

both exist. If one of these limits does not exist, the singular point is irregular.

To see the difference between a regular and an irregular singular point, the easiest case to consider is the first-order analog of (F.1.1). A regular singular point occurs when

$$
b (x) y ^ {\prime} + c (x) y = 0\tag{F.3.1}
$$

with $b(x)$ and $c(x)$ analytic in a neighborhood of $x = x_0$ , and

$$
\lim _ {x \to x _ {0}} (x - x _ {0}) c (x) / b (x)
$$

exists.

When $b(x) = (x - x_0)^2$ and $c(x) = c_0$ , then

$$
y (x) = A e ^ {- c _ {0} / (x - x _ {0})}
$$

is the solution, and it has an essential singularity at $x = x_0$ .

The simple case considered in the previous section, where $a(x)$ , $b(x)$ , $c(x)$ are as in (F.2.3), shows that, at a regular singular point, solutions may involve noninteger powers of $x - x_{0}$ . Moreover, the second solution may have a logarithmic singularity.

Now suppose that $x_0$ is a regular singular point of (F.1.1) such that $a(x)$ has a double zero at $x_0$ . Then

$$
a (x) = \sum_ {n = 2} ^ {\infty} a _ {n} (x - x _ {0}) ^ {n}, \quad b (x) = \sum_ {n = 1} ^ {\infty} b _ {n} (x - x _ {0}) ^ {n}, \quad \text { and } \quad c (x) = \sum_ {n = 0} ^ {\infty} c _ {n} (x - x _ {0}) ^ {n}.
$$

Suppose $y = (x - x_0)^{\mu}f(x)$ is a solution of (F.1.1). The equation for $f(x)$ can be seen to be

$$
\begin{array}{l} a (x) f ^ {\prime \prime} + \left(2 \mu \sum_ {n = 1} ^ {\infty} a _ {n + 1} (x - x _ {0}) ^ {n} + b (x)\right) f ^ {\prime} \\ \qquad + \left(c (x) + \mu \sum_ {n = 0} ^ {\infty} b _ {n + 1} (x - x _ {0}) ^ {n} + \mu (\mu - 1) \sum_ {n = 0} ^ {\infty} a _ {n + 2} (x - x _ {0}) ^ {n}\right) f = 0. \end{array}\tag{F.3.2}
$$

Now if $\mu$ is chosen so that

$$
\mu (\mu - 1) a _ {2} + \mu b _ {1} + c _ {0} = 0,\tag{F.3.3}
$$

then (F.3.1) is an equation of the same type as the one considered at the beginning of Section F.2. In that case a solution of the form $f(x) = \sum_{n=0}^{\infty} f_n(x - x_0)^n$ is always possible provided $2\mu + b_1/a_2$ is not a nonnegative integer.

Note that the quadratic (F.3.2) has two solutions $\mu_{1}$ and $\mu_{2}$ . Thus it may be possible to obtain two solutions of the form $(x - x_{0})^{\mu} f(x)$ . It follows from (F.3.2) that

$$
\begin{array}{r} \mu_ {1} - \mu_ {2} = 2 \mu_ {1} - (\mu_ {1} + \mu_ {2}) \\ = 2 \mu_ {1} - (1 - b _ {1} / a _ {2}) \\ = 2 \mu_ {1} + b _ {1} / a _ {2} - 1. \end{array}
$$

The remarks in the previous paragraph now imply that if the difference of the two roots of (F.3.2) is not an integer, then (F.1.1) has two independent solutions of the form $\sum_{n=0}^{\infty} f_n(x - x_0)^{n+\mu}$ . However, if $\mu_1 - \mu_2 \geq 0$ is an integer, then a solution of this form with $\mu = \mu_1$ exists. The other solution may involve a logarithmic singularity.

Equation (F.3.2) is called the indicial equation. In practice it is obtained by substituting the series $\Sigma f_{n}(x - x_{0})^{n+\mu}$ in (F.1.1) and equating the coefficients of the lowest power of $x - x_{0}$ .

For the hypergeometric equation (2.3.5), there are three regular singular points 0, 1, and infinity. For the confluent equation (4.1.3) and the Bessel equation (4.5.1), 0 is a regular singular point, and infinity is an irregular singular point.

Abel, N. H. [1826]. Auflösung einer mechanischen Aufgabe, J. Reine Ang. Math., 1, 153–157. English translation in Source Book in Mathematics, D. E. Smith, ed., McGraw-Hill, New York, 656–662.

Adams, J. C. [1877]. On the expression of the product of any two Legendre coefficients by means of a series of Legendre's coefficients, Proc. R. Soc. London, 27, 63–71.

Agarwal, R. P. [1953]. On the partial sums of series of hypergeometric type, Proc. Cambridge Phil. Soc., 49, 441–445.

Ahern, P. and Rudin, W. [1996]. Geometric properties of the gamma function, Am. Math. Monthly, 103, 678–681.

Al-Salam, W. A. and Ismail, M. E. H. [1988]. q-Beta integrals and the q-Hermite polynomials, Pac. J. Math., 209–221.

Amend, B. [1996]. Fox Trot, Comic strip, June 2.

Anastassiadis, J. [1964]. Définition des Fonctions Eulériennes par des Équations Functionnelles, Gauthier-Villars, Paris.

Anderson, G. W. [1990]. The evaluation of Selberg sums, Comp. Rend. Acad. Sci., Paris, 311, Série 1, 469–472.

Anderson, G. W. [1991]. A short proof of Selberg's generalized beta formula, Forum Math., 3, 415–417.

Andrews, G. E. [1976]. The Theory of Partitions, Addison-Wesley, Reading, MA.

Andrews, G. E. [1986]. q-Series: Their Development and Application in Analysis, Number Theory, Combinatorics, Physics, and Computer Algebra, Amer. Math. Soc., Providence, RI.

Andrews, G. E. [1994]. The death of proof? Semi-rigorous mathematics? You've got to be kidding!, Math. Intelligencer, 16 (4), 16–18.

Andrews, G. E. and Askey, R. [1977]. Enumeration of partitions: The role of Eulerian series and q-orthogonal polynomials, in Higher Combinatorics, M. Aigner, ed., Reidel, Dordrecht, 3–26.

Andrews, G. E. and Burge, W. H. [1993]. Determinant identities, Pac. J. Math., 158, 1–14.

Andrews, G. E., Dyson, F. J., and Hickerson, D. [1988]. Partitions and indefinite quadratic forms, Invent. Math., 91, 391-407.

Anno, M. and Mori, T. [1986]. Socrates and the Three Little Pigs, Philomel Books, New York.

Aomoto, K. [1987]. Jacobi polynomials associated with Selberg integrals, SIAM J. Math. Anal., 18, 545–549.

Artin, E. [1964]. The Gamma Function, Holt, Rinehart and Winston, New York.

Askey, R. [1970]. Orthogonal polynomials and positivity, Studies in Applied Mathematics 6, in Wave Propagation and Special Functions, D. Ludwig and F. W. J. Olver, eds., SIAM, Philadelphia, 68–85.

Askey, R. [1975]. Orthogonal Polynomials and Special Functions, SIAM, Philadelphia.

Askey, R. [1987]. Ramanujan's $\psi_{1}$ and formal Laurent series, Indian J. Math., 19, 101–105.

Askey, R. [1988]. Beta integrals and q-extensions, Papers of the Ramanujan Centennial International Conference, Ramanujan Math. Soc., 1987, 85–102.

Askey, R. [1994]. A look at the Bateman project, Contemporary Math., 169, 29–43.

Askey, R. and Gasper, G. [1971]. Jacobi polynomial expansions of Jacobi polynomials with non-negative coefficients, Proc. Cambridge Phil. Soc., 70, 243–255.

Askey, R. and Gasper, G. [1977]. Convolution structures for Laguerre polynomials, J. Analyse Math., 31, 48–68.

Askey, R., Gasper, G., and Ismail, M. [1975]. A positive sum from summability theory, J. Approx. Theory, 13, 413–420.

Askey, R., Koornwinder, T., and Rahman, M. [1986]. An integral of products of ultraspherical functions and a q-extension, J. London Math. Soc., 33 (2), 133–148.

Askey, R. and Steinig, J. [1974]. Some positive trigonometric sums, Trans. Am. Math. Soc., 187, 295–307.

Askey, R. and Wilson, J. A. [1984]. A recurrence relation generalizing those of Apéry, J. Austral. Math. Soc. (Series A) 36, 267–278.

Askey, R. and Wilson, J. A. [1985]. Some Basic Hypergeometric Orthogonal Polynomials that Generalize Jacobi Polynomials, Am. Math. Soc., Providence, RI.

Auslander, L. and Tolimieri, R. [1979]. Is computing with finite Fourier transform pure or applied mathematics?, Bull. Am. Math. Soc. (New Series), 11, 847–897.

Azor, R., Gillis, J., and Victor, J. D. [1982]. Combinatorial applications of Hermite polynomials, SIAM J. Math. Anal., 13, 879–890.

Baernstein II, A., Drasin, D., Duren, P., and Marden, A. [1986]. The Bieberbach Conjecture, Amer. Math. Soc. Surveys and Monographs No. 21, Providence, RI.

Bailey, W. N. [1929]. Some identities involving generalized hypergeometric series, Proc. London Math. Soc., 26 (2), 503–516.

Bailey, W. N. [1931]. The partial sum of the coefficients of the hypergeometric series, J. London Math. Soc., 6, 40–41.

Bailey, W. N. [1932]. On one of Ramanujan's theorems, J. London Math. Soc., 7, 34–36.

Bailey, W. N. [1933]. On the product of two Legendre polynomials, Proc. Cambridge Phil. Soc., 29, 173–177.

Bailey, W. N. [1935]. Generalized Hypergeometric Series, Cambridge University Press, Reprinted by Hafner Pub. Co., New York, 1972.

Bailey, W. N. [1938]. The generating function of Jacobi polynomials, J. London Math. Soc., 13, 8–11.

Bailey, W. N. [1941]. A note on certain q-identities, Quart. J. Math. (Oxford), 18, 157–166.

Bailey, W. N. [1949]. Identities of the Rogers–Ramanujan type, Proc. London Math. Soc., 50 (2), 1–10.

Bailey, W. N. [1954]. Contiguous hypergeometric functions of the type $_{3}F_{2}(1)$ , Proc. Glasgow Math. Assoc., 2, 62–65.

Bak, J. and Newman, D. J. [1982]. Complex Analysis, Springer-Verlag, New York.

Barnes, E. W. [1908]. A new development of the theory of the hypergeometric functions, Proc. London Math. Soc., 6 (2), 141–177.

Barnes, E. W. [1910]. A transformation of generalized hypergeometric series, Quart. J. Math., 41, 136–140.

Bateman, H. [1909]. The solution of linear differential equations by means of definite integrals, Trans. Cambridge Phil. Soc., 21, 171–196.

Bateman, H. [1932]. Partial Differential Equations of Mathematical Physics, Cambridge University Press, Cambridge, UK.

Bellman, R. [1961]. A Brief Introduction to Theta Functions, Holt, Rinehart, and Winston, Inc., New York.

Berggren, L., Borwein, J., and Borwein, P. [1997]. Pi: A Source Book, Springer-Verlag, New York.

Berndt, B. [1975]. Periodic Bernoulli numbers, summation formulas and applications, in Theory and Application of Special Functions, R. Askey, ed., Academic Press, New York.

Berndt, B. [1985]. Ramanujan's Notebooks, Part I, Springer-Verlag, New York.

Berndt, B. [1989]. Ramanujan's Notebooks, Part II, Springer-Verlag, New York.

Beukers, F. [1979]. A note on the irrationality of $\zeta(2)$ and $\zeta(3)$ , Bull. London Math. Soc., 11, 2268-2272.

Boas, R. P. [1954]. Entire Functions, Academic Press, New York.

Bochner, S. [1952]. Remarks on Gaussian sums and Tauberian theorems, J. Indian Math. Soc., 15, 99–106.

Bochner, S. [1955]. Harmonic Analysis and the Theory of Probability, University of California Press, Berkeley.

Bochner, S. [1979]. Review of Gesammelte Schriften by Gustav Herglotz, Bull. Am. Math. Soc. (New Series), 1, 1020–1022.

Bohr, H. and Mollerup, J. [1922]. Laerebog i Matematisk Analyse, Vol. III, J. Gjellerup, Kopenhagen.

Borwein, J. and Borwein, P. [1987]. Pi and the AGM, Wiley, New York.

Boyarsky, M. [1980]. p-adic gamma functions and Dwork cohomology, Trans. Am. Math. Soc., 257, 359–369.

Brafman, F. [1951]. Generating functions of Jacobi and related polynomials, Proc. Am. Math. Soc., 2, 924–949.

Brent, R. P. [1976]. Fast multiple-precision evaluation of elementary functions, J. Assoc. Comp. Mech., 23, 242–251.

Bressoud, D. M. [1987]. Almost poised basic hypergeometric series, Proc. Indian Acad. Sci. (Math./Sci.), 97, 61–66.

Bromwich, T. J. I'A. [1926]. An Introduction to the Theory of Infinite Series, 2nd ed., Macmillan, London.

Brown, G. and Hewitt, E. [1984]. A class of positive trigonometric sums, Math. Ann., 268, 91–122.

Brown, M. and Ismail, M. E. H. [1995]. A right inverse of the Askey–Wilson operator, Proc. Amer. Math. Soc., 123, 2071–2079.

Brualdi, R. A. and Ryser, H. J. [1991]. Combinatorial Matrix Theory, Cambridge University Press, New York.

Bustoz, J. [1974]. Note on “Positive Cesàro means of numerical series,” Proc. Amer. Math. Soc., 45, 69.

Caratheodory, C. [1954]. Funktionentheorie, English translation, Theory of Functions, Vols. I and II, [1958, 1960], Chelsea, New York.

Cartier, P. and Foata, D. [1969]. Problèmes Combinatoires de Commutation et Réarrangements, Lecture Notes in Math., No. 85, Springer-Verlag, Berlin.

Cauchy, A.-L. [1843]. Mémoire sur les fonctions dont plusieurs valeurs . . . , C.R. Acad. Sci. Paris, 17, 523, reprinted in Oeuvres de Cauchy, [1893], Ser. 1, 8, 42–50.

Cauchy, A.-L. [1843a]. Deuxième Mémoire sur les fonctions dont plusieurs valeurs . . . , C.R. Acad. Sci. Paris, reprinted in Oeuvres de Cauchy, [1893], 8, 50–55.

Chebyshev, P. L. [1870]. Sur les fonctions analogues à celles de Legendre, in Oeuvres de P. L. Tchebychef, Vol. 2, A. Markoff and N. Sonin, eds., St. Petersburg [1907], 61–68, reprinted Chelsea, New York [1961].

Chihara, J. S. [1978]. An Introduction to Orthogonal Polynomials, Gordon & Breach, New York.

Clausen, T. [1828]. Ueber die Fälle, wenn die Reihe von der Form  \( y = 1 + \frac{\alpha}{1} \cdot \frac{\beta}{\gamma} x + \frac{\alpha \cdot \alpha + 1}{1 \cdot 2} \cdot \frac{\beta \cdot \beta + 1}{\gamma \cdot \gamma + 1} x^{2} + \text{etc. ein quadrat von der Form } z = 1 + \frac{\alpha'}{1} \cdot \frac{\beta'}{\gamma'} \cdot \frac{\delta'}{\epsilon'} x + \frac{\alpha' \cdot \alpha' + 1}{1 \cdot 2} \cdot \frac{\beta' \cdot \beta' + 1}{\gamma' \cdot \gamma' + 1} \cdot \frac{\delta' \cdot \delta' + 1}{\epsilon' \cdot \epsilon' + 1} x^{2} + \text{etc. hat, J. Reine Ang. Math., 3, 89–91.}

Cooley, J. W. and Tukey, J. W. [1965]. An algorithm for the machine calculation of complex Fourier series, Math. Comp., 19, 297–301.

Copson, E. T. [1935]. Theory of Functions of a Complex Variable, Oxford Univ. Press, London.

Cox, D. [1984]. The arithmetic-geometric mean of Gauss, Enseign. Math., 30, 270–330.

Davenport, H. and Hasse, H. [1934]. Die Nullstellen der Kongruenzzetafunktion in gewissen zyklischen Fällen, J. Reine Ang. Math., 172, 151–182.

de Boor, C. [1980]. FFT as nested multiplication, with a twist, SIAM J. Sci. Stat. Comp., 1, 173–178.

de Branges, L. [1972]. Gauss spaces of entire functions, J. Math. Anal. Appl., 37, 1-41.

de Branges, L. [1972a]. Tensor product spaces, J. Math. Anal. App., 38, 109–148.

de Branges, L. [1985]. A proof of the Bieberbach conjecture, Acta Math., 154, 137-152.

de Bruijn, N. G. [1967]. Uncertainty principles in Fourier analysis, in Inequalities, O. Shisha, ed., Academic Press, New York.

de Bruijn, N. G., Saff, E. B., and Varga, R. S. [1981]. On the zeros of generalized Bessel polynomials, Proc. K. Ned. Akad. Wet., Series A, 84 (1), 1–25.

de Moivre, A. [1730]. Miscellanea Analytica de Seriebus et Quadraturis, Tonson and Watts, London.

Dedekind, R. [1853]. Über ein Eulersches Integral, J. Reine Ang. Math.

DeSainte-Catherine, M. and Viennot, G. [1983]. Combinatorial interpretation of integrals of products of Hermite, Laguerre and Tchebycheff polynomials, Polynômes Orthogonaux et Applications, C. Brezinski et al., eds., Lecture Notes in Math. 1171, Springer-Verlag, 120–128.

Din, A. M. [1981]. Lett. Math. Phys., 5, 207.

Dixon, A. C. [1903]. Summation of a certain series, Proc. London Math. Soc., 35 (1), 285–289.

Dougall, J. [1907]. On Vandermonde's theorem and some more general expansions, Proc. Edinburgh Math. Soc., 25, 114–132.

Dougall, J. [1919]. A theorem of Sonine in Bessel functions, with two extensions to spherical harmonics, Proc. Edinburgh Math. Soc., 37, 33–47.

Edwards, C. H. [1979]. The Historical Development of Calculus, Springer-Verlag, New York.

Edwards, A. W. F. [1987]. Pascal's Arithmetical Triangle, Charles Griffin and Co., London.

Eisenstein, G. [1847]. Genaue Untersuchung der unendlichen Doppelprodukte, J. Reine Ang. Math., 35, 153–274.

Elliot, E. B. [1904]. A formula including Legendre's $E K' + K E' - K K' = \frac{1}{2} \pi$ , Messenger of Math., 33, 31-40.

Erdélyi, A. [1937]. Der Zusammenhang zwischen verschiedenen Integraldarstellungen hypergeometrischer Funktionen, Quart. J. Math. (Oxford), 8, 200–213.

Erdélyi, A. [1938]. Note on the transformation of Eulerian hypergeometric functions, Quart. J. Math. (Oxford), 9, 129–134.

Erdélyi, A. [1939]. Transformation of hypergeometric integrals by means of fractional integration by parts, Quart. J. Math. (Oxford), 9, 176–189.

Erdélyi, A. [1953]. Higher Transcendental Functions, Vols. I, II, III, A. Erdélyi, ed., McGraw-Hill. Reprinted by Krieger Publishing Co., Malabar, FL [1981].

Erdélyi, A. [1956]. Asymptotic Expansions, Dover, New York.

Erdélyi, A. [1960]. Asymptotic solutions of differential equations with transition points or singularities, J. Mathematical Phys., 1, 16–26.

Euler, L. [1730]. De progressionibus transcendentibus sen quaroum termini generales algebrare dari nequeunt, Comm. Acad. Sci. Petropolitanae, 5, 36–57.

Euler, L. [1739]. De productis ex infinitis factoribus ortis, Comm. Acad. Sci. Petropolitanae, 11, 3–31. Reprinted in Opera Omnia, 14 [1924], 260–290.

Euler, L. [1748]. Introductio in Analysin Infinitorum, Marcum-Michaelem Bousquet, Lausannae. English translation published by Springer-Verlag, [1988].

Euler, L. [1769]. Institutiones Calculi Integralis, II, Opera Omnia, Ser. 1, Vols. 11–13.

Euler, L. [1794]. Specimen transformationis singularis serierum, Nova Acta Acad. Sci. Petropolitanae, 12, 58–70. Reprinted in Opera Omnia, Ser. 1, Vol. 16, Part 2, 41–55.

Evans, R. [1981]. Identities for Gauss sums over finite fields, Enseign. Math., 27 (2), 197–209.

Evans, R. [1991]. The evaluation of Selberg character sums, Enseign. Math., 37 (2), 235–248.

Fejér, L. [1925]. Abschätzungen für die Legendreschen und verwandte Polynome, Math. Zeit., 24, 267–284.

Feldheim, E. [1941]. Contribution à la théorie des polynomes de Jacobi (Hungarian, French summary), Mat. Fiz. Lapik, 48, 453–504.

Feldheim, E. [1941a]. Sur les polynomes généralisés de Legendre, Izv. Akad. Nauk. SSSR Ser. Math., 5, 241–248.

Feldheim, E. [1943]. Contributi alla teoria della funzioni ipergeometriche di più variabili, Annali della Scuola Norm. Super. di Pisa, Ser. II, 12, 17–60.

Feldheim, E. [1963]. Appendix by G. Szegö. On the positivity of certain sums of ultraspherical polynomials, J. Anal. Math., 11, 275–284.

Ferrers, N. M. [1877]. An Elementary Treatise on Spherical Harmonics and Subjects Connected with Them, Macmillan, London.

Fields, J. L. [1964]. A note on the asymptotic expansion of a ratio of gamma functions, Proc. Edinburgh Math. Soc., 15, 43–45.

Fine, N. J. [1988]. Basic Hypergeometric Series and Applications, Amer. Math. Soc., Providence, RI.

Foata, D. [1965]. Etude algébrique de certains problèmes d'analyse combinatoire et du calcul des probabilités, Publ. Inst. Stat. Univ. Paris, 14, 81–241.

Forrester, P. J. and Rogers, J. B. [1986]. Electrostatics and the zeros of the classical polynomials, SIAM J. Math. Anal., 17, 461–468.

Frobenius, F. G. [1871]. Über die Entwicklung analytischer Functionen in Reihen, die nach gegebenen Functionen fortschreiten, J. Reine Ang. Math., 73, 1–30. Reprinted in Gesammelte Abhandlungen, Band I, Springer-Verlag, [1968], 35–64.

Funk, P. [1916]. Beiträge zur Theorie der Kugelfunktionen, Math. Ann., 77, 136–152.

Fuss, N. [1843]. Correspondance Mathématique et Physique de Quelques Célèbres Géomètres du XVIIIème siècle, 1, Saint-Pétersbourg.

Gasper, G. [1975]. Positive integrals of Bessel functions, SIAM J. Math. Anal., 6, 868–881.

Gasper, G. [1977]. Positive sums of the classical orthogonal polynomials, SIAM J. Math. Anal., (8), 423–447.

Gasper, G. [1985]. Rogers' linearization formula for the continuous $q$ -ultraspherical polynomials and quadratic transformation formulas, SIAM J. Math. Anal., 16, 1061-1071.

Gasper, G. and Rahman, M. [1990]. Basic Hypergeometric Series, Cambridge University Press, Cambridge, UK.

Gauss, C. F. [1808]. Summatio quarumdam serierum singularium, Commen. Soc. Reg. Sci. Götting. Rec., vol. I. German translation in Arithmetische Untersuchungen, Chelsea, New York [1981].

Gauss, C. F. [1812]. Disquisitiones generales circa seriem infinitam, Comm. Soc. Reg Gött. II, Werke, 3, 123–162.

Gauss, C. F. [1866]. Zur Theorie der neuen Transscendenten, II, Werke, 3, 436–445.

Gauss, C. F. [1866a]. Hundert Theoreme über die neuen Transscendenten, Werke, 3, 461–469.

Gauss, C. F. [1866b]. Arithmetisch Geometrisches Mittel, Werke, vol. 3, 361–403.

Gautschi, W. [1967]. Computational aspects of three-term recurrence relations, SIAM Review, 9, 24–82.

Gegenbauer, L. [1875]. Ueber einige Bestimmte Integrale, Sitz. Math. Natur. Klasse Akad. Wiss. Wien, 70, 433–443.

Gessel, I. and Stanton, D. [1982]. Strange evaluations of hypergeometric series, SIAM J. Math. Anal., 11, 295–308.

Godsil, C. D. [1981]. Hermite polynomials and a duality relation for the matching polynomial, Combinatorica, 1, 257–262.

Godsil, C. D. [1993]. Algebraic Combinatorics, Chapman and Hall, New York.

Good, I. J. [1960]. Generalization to severable variables of Lagrange's expansion, with applications to stochastic processes, Proc. Cambridge Phil. Soc., 56, 367–380.

Good, I. J. [1962]. A short proof of MacMahon's "master theorem," Proc. Cambridge Phil. Soc., 58, 160.

Good, I. J. [1970]. Short proof of a conjecture of Dyson, J. Math. Phys., 11, 1884.

Gosper, R. W., Jr. [1978]. Decision procedure for indefinite hypergeometric summation, Proc. Natl. Acad. Sci. USA, 75, 40–42.

Gould, H. W. and Hsu, L. C. [1973]. Some new inverse series relations, Duke Math. J., 40, 885–891.

Gray, J. [1986]. Linear Differential Equations and Group Theory from Riemann to Poincaré, Birkhäuser, Boston.

Gronwall, T. H. [1912]. Ueber die Gibbssche Erscheinung und die trigonometrischen Summen $\sin x + 1/2 \sin 2x + 1/3 \sin 3x + \cdots + 1/n \sin nx$ , Math. Ann., 72, 228–243.

Gross, B. and Koblitz, N. [1979]. Gauss sums and the p-adic gamma function, Ann. Math., 109, 569–581.

Halmos, P. [1950]. Measure Theory, Van Nostrand, Princeton.

Hamburger, H. [1922]. Ueber einige Beziehungen, die mit der Funktionalgleichung der Riemannschen $\zeta$ -Funktion aequivalent sind, Math. Ann., 85, 129-140.

Hankel, H. [1875]. Bestimmte Integrale mit Cylinderfunctionen, Math. Ann., 8, 453–470.

Hardy, G. H. [1922]. A new proof of the functional equation for the zeta function, Mat. Tidsskrift, B, 71–73.

Hardy, G. H. [1933]. A theorem concerning Fourier transforms, J. London Math. Soc., 8, 227–231.

Hardy, G. H. [1940]. Ramanujan, Cambridge University Press, Cambridge, UK.

Hardy, G. H. [1949]. Divergent Series, Cambridge University Press, Cambridge, UK.

Hecke, E. [1918]. Ueber orthogonal-invariante Integralgleichungen, Math. Ann., 78, 398–404.

Heckman, G. and Schlicktkrull, H. [1994]. Harmonic Analysis and Special Functions on Symmetric Spaces, Academic Press, San Diego.

Heine, E. [1847]. Untersuchungen über die Reihe..., J. Reine Ang. Math., 34, 285–328.

Helversen-Pasotto, A. [1978]. L'identité de Barnes pour les corps finis, C. R. Acad. Sci. Paris, Sér. A–B, 286, A297–A300.

Helversen-Pasotto, A. and Solé, P. [1993]. Barnes' first lemma and its finite analogue, Canadian Math. Bull., 36, 273–282.

Hermite, C. [1890]. Sur les Polynomes de Legendre, Rend. Circ. Mat. Palermo, IV, 146–152. Reprinted in Oeuvres, 4, 314–320.

Hewitt, E. [1954]. Remark on orthonormal sets in $L_{2}(a,b)$ , Amer. Math. Monthly, 61, 249-250.

Hill, M. J. M. [1908]. On a formula for the sum of a finite number of terms of the hypergeometric series when the fourth element is equal to unity, Proc. London Math. Soc., (2), 6, 339–348.

Hille, E. [1962]. Analytic Function Theory, Vol. II, Ginn and Co., Republished, Chelsea, New York [1977].

Hölder, O. [1889]. Über einen Mittelwertsatz, Goettinger Nach., 38–47.

Hsü, H.-Y. [1938]. Certain integrals and infinite series involving ultraspherical polynomials and Bessel functions, Duke Math. J., 4, 374–383.

Hylleraas, E. [1962]. Linearization of products of Jacobi polynomials, Math. Scand., 10, 189–200.

Ingham, A. E. [1932]. The Distribution of Prime Numbers, Cambridge University Press, London.

Ireland, K. and Rosen, M. [1991]. A Classical Introduction to Modern Number Theory, 2nd Ed., Springer-Verlag, New York.

Ismail, M. E. H. [1977]. A simple proof of Ramanujan's $_{1}\psi_{1}$ sum, Proc. Amer. Math. Soc., 63, 185–186.

Ismail, M. E. H. and Stanton, D. [1988], On the Askey–Wilson and Rogers polynomials, Canadian J. Math., 40, 1025–1045.

Ismail, M. E. H. and Tamhankar, M. V. [1979]. A combinatorial approach to some positivity problems, SIAM J. Math. Anal., 10, 478–485.

Jackson, D. [1911]. Ueber eine trigonometrische Summe, Rend. Circ. Mat. Palermo, 32, 257–262.

Jackson, F. H. [1910]. On $q$ -definite integrals, Quart. J. Pure Appl. Math., 41, 193-203.

Jackson, F. H. [1921]. Summation of a $q$ -hypergeometric series, Messenger of Math., 50, 101-112.

Jacobi, C. G. [1826]. Über Gauss' neue Methode, die Werthe der Integrale näherungsweise zu finden, J. Reine Ang. Math., 1, 301–308.

Jacobi, C. G. [1829]. Fundamenta Nova, Regiomontis, fratrum Borntraeger. Reprinted in Werke, Vol. 1, Chelsea, New York [1969], 49–239.

Jacobi, C. G. [1830]. De resolutione aequationum per series infinitam, J. Reine Ang. Math., 6, 257–286.

Jacobi, C. G. [1834]. Demonstratio Formulae..., J. Reine Ang. Math., 11, 307.

Jacobi, C. G. [1859]. Untersuchung über die Differentialgleichung der hypergeometrischen Reihe, J. Reine Ang. Math., 56, 149–165.

Jensen, J. L. W. V. [1915-1916]. An elementary exposition of the theory of the gamma function, Ann. Math., 17, 124-166.

John, F. [1938]. Special solutions of certain difference equations, Acta Math., 71, 175–189.

Karlin, S. and McGregor, J. L. [1957]. The differential equations of birth-and-death processes, Trans. Amer. Math. Soc., 85, 489–546.

Kirillov, A. N. [1994]. Dilogarithm Identities, Preprint Series, Dept. of Math. Sci., University of Tokyo.

Klein, F. [1894]. Vorlesungen über die Hypergeometrische Funktion, Göttingen.

Knopp, M. [1971]. Modular Forms and Analytic Number Theory, Markham, New York.

Koblitz, N. [1977]. P-Adic Numbers, p-adic Analysis, and Zeta-Functions, Springer-Verlag, New York.

Koblitz, N. [1984]. Introduction to Elliptic Curves and Modular Forms, Springer-Verlag, New York.

Koekoek, R. and Swarttouw, R. F. [1994]. The Askey-scheme of hypergeometric orthogonal polynomials and its q-analogue, Reports of the Faculty of Technical Mathematics and Informatics, no. 98–117, Delft.

Kogbetliantz, E. [1924]. Recherches sur la sommabilité des séries ultrasphériques par la méthode des moyennes arithmetiques, J. Math. Pures Appl., (9), 3, 107–187.

Kolberg, O. [1957]. Some identities involving the partition functions, Math. Scand., 5, 77–92.

Koornwinder, T. H. [1972]. The addition formula for Jacobi polynomials, I, Summary of results, Indag. Math., 34, 188–191.

Koornwinder, T. H. [1974]. Jacobi polynomials, II. An analytic proof of the product formula, SIAM J. Math. Anal., 5, 125–137.

Koornwinder, T. H. [1975]. Jacobi polynomials, III. An analytic proof of the addition formula, SIAM J. Math. Anal., 6, 533–543.

Koornwinder, T. H. [1978]. Positivity proofs for linearization and connection coefficients of orthogonal polynomials satisfying an addition formula, J. London Math. Soc. (2), 18, 101–114.

Koornwinder, T. H. [1990]. Jacobi functions as limit cases of q-ultraspherical polynomials, J. Math. Anal. Appl., 148, 44–54.

Kummer, E. [1836]. Ueber die hypergeometrische Reihe, J. Reine Ang. Math., 15, 39–83, 127–172.

Kummer, E. [1847]. Beitrag zur Theorie der Function $\Gamma(x)$ , J. Reine Ang. Math., 35, 1-4. Lang, S. [1980]. Cyclotomic Fields II, Springer-Verlag, New York.

Lanzewizky, I. L. [1941]. Ueber die Orthogonalität der Fejér-Szegöschen Polynome, C. R. (Dokl.) Acad. Sci. USSR, 31, 199–200.

Lewin, L. [1981]. Polylogarithms and Associated Functions, North-Holland, New York.

Lewin, L. [1981a]. Structural Properties of Polylogarithms, Amer. Math. Soc., Providence, RI.

Liouville, J. [1839]. Sur quelques intégrales définies, J. Math. Pures Appl., Sér. 1, 4, 229–235.

Liouville, J. [1855]. Sur un théorème relatif à 1' intégrale eulérienne de seconde espèce, J. Math. Pure Appl., Sér. 1, 20, 157–160.

Littlewood, J. E. [1986]. Littlewood's Miscellany (B. Bollobás, ed.), Cambridge University Press, Cambridge, UK.

Lorch, L., Muldoon, M. E., and Szego, P. [1970]. Higher monotonicity properties of certain Sturm–Liouville functions, III, Canadian J. Math., 22, 1238–1265.

Lorch, L., Muldoon, M. E., and Szego, P. [1972]. Higher monotonicity properties of certain Sturm–Liouville functions, IV, Canadian J. Math., 24, 349–368.

Lorch, L. and Szego, P. [1963]. Higher monotonicity properties of certain Sturm–Liouville functions, Acta Math., 109, 55–73.

Lorentz, G. G. and Zeller, K. [1964]. Abschnittlimitierbarkeit und der Satz von Hardy–Bohr, Arch. Math. (Basel), 15, 208–213.

Lorentzen, L. and Waadeland, H. [1992]. Continued Fractions with Applications, North-Holland, Amsterdam.

Macdonald, I. G. [1995]. Symmetric Functions and Hall Polynomials, 2nd ed., Oxford University Press, Oxford.

MacMahon, P. A. [1917–1918]. Combinatory Analysis, Cambridge University Press, Cambridge, UK. Reprinted by Chelsea, New York [1984].

Magnus, A. [1988]. Associated Askey–Wilson polynomials as Laguerre–Hahn orthogonal polynomials, in Orthogonal Polynomials and Their Applications (Segovia, 1986), M. Alfaro et al., eds., Lecture Notes in Math. no. 1329, Springer-Verlag, New York, 261–378.

Makai, E. [1974]. An integral inequality satisfied by Bessel functions, Acta Math. Acad. Sci. Hungaricae, 25, 387–390.

Mehta, M. L. [1991]. Random Matrices, 2nd Ed., Academic Press, Boston.

Miller, W., Jr. [1972]. Symmetry Groups and Their Applications, Academic Press, New York.

Milne, S. C. [1988]. Multiple q-series and $U(n)$ generalizations of Ramanujan's $_{1}\psi_{1}$ sum, in Ramanujan Revisited, G. Andrews et al., eds., Academic Press, New York, 473–524.

Milne, S. C. and Lilly, G. M. [1995]. Consequences of the $A_{\ell}$ and $C_{\ell}$ Bailey transform and Bailey lemma, Discrete Math., 139, 319–346.

Moak, D. S. [1980]. The q-gamma function for q > 1, Aequat. Math., 20, 278–285.

Monsky, P. [1994]. Simplifying the proof of Dirichlet's theorem, Amer. Math. Monthly, 100, 861–862.

Morita, Y. [1975]. A p-adic analog of the $\Gamma$ -function, J. Fac. Sci. Tokyo, Sec. 1A, 22, 255–266.

Morris, W. G. [1984]. Constant term identities for finite and affine root systems: Conjectures and theorems, Ph.D. Thesis, University of Wisconsin–Madison.

Müller, C. [1966]. Spherical Harmonics, Lecture Notes in Mathematics, 7, Springer-Verlag, New York.

Murphy, R. [1835]. Second memoir on the inverse method of definite integrals, Trans. Cambridge Phil. Soc., 5, 113–148.

Nassarallah, B. and Rahman, M. [1985]. Projection formulas, a reproducing kernel and a generating function for $q$ -Wilson polynomials, SIAM J. Math. Anal., 16, 186-197.

Natanson, I. P. [1965]. Constructive Function Theory, Vol. III, Frederick Ungar Publishing Co., New York.

Nemes, I., Petkovšek, M., Wilf, H., and Zeilberger, D. [1997]. How to do Monthly Problems with your computer, Amer. Math. Monthly, 104, 505–519.

Nevai, P. [1979]. Orthogonal Polynomials, Amer. Math. Soc., Providence, RI.

Nevai, P. [1990]. Orthogonal Polynomials: Theory and Practice, P. Nevai, ed., Kluwer Academic Publishers, Dordrecht.

Newton, I. [1960]. The Correspondence of Isaac Newton, 2, 1676–1687, Cambridge University Press, Cambridge, UK.

Nielsen, N. [1906]. Handbuch der Theorie der Gamma Funktion, B. B. Teubner, Leipzig.

Olver, F. W. J. [1974]. Asymptotics and Special Functions, Academic Press, New York.

Papperitz, E. [1889]. Ueber die Darstellung der hypergeometrischen Transcendenten durch eindeutige Functionen, Math. Ann., 34, 247–296.

Petkovšek, M., Wilf, H., and Zeilberger, D. [1996]. A = B, A. K. Peters, Wellesley, MA. Pfaff, J. F. [1797]. Disquisitiones Analyticae, I, Helmstadt.

Pfaff, J. F. [1797a]. Observationes analyticae ad L. Euleri Institutiones Calculi Integralis, Vol. IV, Supplem. II et IV, Historie de 1793, Nova Acata Acad. Scie. Petropolitanae, XI, 38–57. (Note: The history section is paged separately from the scientific section of this journal.)

Poincaré, H. [1886]. Sur les intégrales irrégulières des équations linéares, Acta Math., 8, 295–344.

Poisson, S. D. [1823]. Suite du Mémoire sur les intégrales définies et sur la sommation des séries, Paris Jour. de l'École Polytechnique, 19, 404–509, especially, pp. 477–478.

Pólya, G. [1984]. Collected Papers, Vols. I–IV, MIT Press, Cambridge, MA.

Pólya, G. and Szegö, G. [1972]. Problems and Theorems in Analysis, Vols. I and II, Springer-Verlag, New York.

Rademacher, H. [1955]. On the transformation of $\log \eta(\tau)$ , J. Indian Math. Soc., 19, 25–30.

Rademacher, H. [1973]. Topics in Analytic Number Theory, Springer-Verlag, New York.

Rahman, M. [1981]. A non-negative representation of the linearization coefficients of the product of Jacobi polynomials, Canadian J. Math., 33, 915–928.

Rahman, M. [1986]. q-Wilson functions of the second kind, SIAM J. Math. Anal., 17, 1280–1286.

Ramanujan, S. [1927]. Collected Papers, Cambridge University Press. Reprinted by Chelsea, New York [1962].

Ramanujan, S. [1988]. The Lost Notebook, Narosa Publishing House, New Delhi.

Raynal, J. [1979]. On the definition and properties of generalized 6-j symbols, J. Math. Phys., 20, 2398–2415.

Riemann, B. [1857]. Beiträge zur Theorie der durch Gauss'sche Reihe $F(\alpha, \beta, \gamma, x)$ darstellbaren Functionen, K. Gess. Wiss. Göttingen, 7, 1–24.

Riemann, B. [1859]. Über die Anzahl der Primzahlen unter einer gegebene Grösse, Monatsb. Berliner Akad., 671–680. Reprinted in Gesammelte Mathematische Werke, paper 7, Springer-Verlag, [1990].

Rogers, L. J. [1888]. An extension of a certain theorem in inequalities, Messenger of Math., 17, 145–150.

Rogers, L. J. [1894]. Second memoir on the expansion of certain infinite products, Proc. London Math. Soc., 25, 318–343.

Rogers, L. J. [1895]. Third memoir on the expansion of certain infinite products, Proc. London Math. Soc., 26, 15–32.

Rogers, L. J. [1907]. On function sum theorems connected with the series $\sum_{n=1}^{\infty} x^n / n^2$ , Proc. London Math. Soc., 4, 169-189.

Rogers, L. J. [1917]. On two theorems of combinatory analysis and allied identities, Proc. London Math. Soc., (2), 16, 315–336.

Roosenraad, C. T. [1969]. Inequalities with orthogonal polynomials, Ph.D. Thesis, University of Wisconsin–Madison.

Rothe, H. A. [1811]. Systematisches Lehrbuch der Arithmetic, Leipzig.

Roy, R. [1990]. The discovery of the series formula for $\pi$ by Leibniz, Gregory and Nilakantha, Math. Mag., 63, 291-306.

Roy, R. [1993]. The work of Chebyshev on orthogonal polynomials, in Topics in Polynomials of One and Several Variables and Their Applications, Th. Rassias, H. M. Srivastava, A. Yanushauskas, eds., World Scientific, Singapore, 495–512.

Rudin, W. [1976]. Principles of Mathematical Analysis, 3rd ed., McGraw-Hill, New York.

Saalschütz, L. [1890]. Eine Summationsformel, Zeitschrift Math. Phys., 35, 186–188.

Saff, E. B. and Varga, R. S. [1976]. Zero-free parabolic regions for sequences of polynomials, SIAM J. Math. Anal., 7, 344–357.

Salamin, E. [1976]. Computation of $\pi$ using arithmetic-geometric mean, Math. Comput., 30, 565-570.

Sápiro, R. L. [1968]. Special functions related to representations of the group $SU(n)$ , of class I with respect to $SU(n-1)$ ( $n \geq 3$ ), Izv. Vyssh. Uchebn. Zaved. Matematika, 71 (4), 97–107 (in Russian).

Sarmanov, I. O. [1968]. A generalized symmetric gamma correlation, Dokl. Akad. Nauk SSSR, 179, 1276–1278; Soviet Math. Dokl., 9, 547–550.

Scharlau, W. and Opolka, H. [1985]. From Fermat to Minkowski, Springer-Verlag, New York.

Schiff, L. I. [1947]. Quantum Mechanics, Addison-Wesley, New York.

Schur, I. [1918]. Über die Verteilung der Wurzeln bei gewissen algebraischen Gleichungen mit ganzzahligen Koeffizienten, Math. Zeit., 1, 377–402.

Schur, I. [1921]. Über die Gaussschen Summen, Nach. Gessel. Göttingen, Math-Phys. Klasse, 147–153.

Schützenberger, M.-P. [1953]. Une interprétation de certaines solutions de l'équation fonctionnelle: $F(x + y) = F(x)F(y)$ , C. R. Acad. Sci. Paris, 236, 352-353.

Sears, D. B. [1951]. Transformations of basic hypergeometric functions of special type, Proc. London Math. Soc., (2), 53, 138–157.

Selberg, A. [1944]. Bemerkninger om et multipelt integral, Norske Mat. Tidsskr., 26, 71–78.

Sheppard, W. F. [1912]. Summation of the coefficients of some terminating hypergeometric series, Proc. London Math. Soc., (2), 10, 469–478.

Siegel, C. L. [1945]. The trace of totally positive and real algebraic integers, Ann. Math., 46, 302-313.

Siegel, C. L. [1954]. A simple proof of $\eta(-1/\tau) = \eta(\tau)\sqrt{\tau/2}$ , Mathematica, 1, 4.

Simpson, T. [1759]. The invention of a general method for determining the sum of every second, third, fourth, or fifth, etc. term of a series, taken in order; the sum of the whole series being known, Phil. Trans. Royal Soc. London, 50, 757–769.

Smith, H. J. S. [1859–1865]. Report on the Theory of Numbers, Reprinted by Chelsea, New York [1965].

Stanton, D. [1988]. Recent results for the q-Lagrange inversion formula, in Ramanujan Revisited, G. E. Andrews, R. Askey, B. Berndt, K. G. Ramanathan, and R. A. Rankin, eds., Academic Press, San Diego, 525–536.

Stieltjes, T. J. [1993]. Collected Papers, Vols. I and II, Springer-Verlag, New York. Stirling, J. [1730]. Methodus Differentialis, London.

Stone, M. H. [1962]. A generalized Weierstrass approximation theorem, in Studies in Modern Analysis, R. C. Buck, ed., Math. Assoc. America,

Sylvester, J. J. [1853]. On Mr. Cayley's impromptu demonstration of the rule for determining at sight the degree of any symmetrical function of the roots of an equation expressed in terms of the coefficients, Phil. Mag., 5, 199–202. Collected Papers, Vol. 1, 594–598.

Sylvester, J. J. [1883]. Note on the graphical method in partitions of n, Proc. Cambridge Phil. Soc., 19, 207–210.

Sylvester, J. J. [1886]. Lectures on the theory of reciprocants, Amer. J. Math., 8, 196–260; 9, 1–37, 113–11661, 297–352; 10, 1–116.

Szász, O. [1950]. On the relative extrema of ultraspherical polynomials, Bollettino della Unione Matematica Italiana, 5 (3), 125–127.

Szász, O. [1951]. On the relative extrema of the Hermite orthogonal functions, J. Indian Math. Soc., 25, 1340–1345.

Szegö, G. [1933]. Ueber gewisse Potenzreihen mit lauter positiven Koeffizienten, Math. Zeit., 37, 674–688.

Szegö, G. [1936]. Inequalities for the zeros of Legendre polynomials and related functions, Trans. Amer. Math. Soc., 39, 1–17.

Szegö, G. [1948]. On an inequality of Turán concerning Legendre polynomials, Bull. Amer. Math. Soc., 54, 401–405.

Szegö, G. [1950]. On the relative extrema of Legendre polynomials, Bollettino della Unione Matematica Italiana, 5 (4), 120–121.

Szegö, G. [1975]. Orthogonal Polynomials, Amer. Math. Soc., Providence, RI.

Szwarc, R. [1992]. Orthogonal polynomials and a discrete boundary value problem II, SIAM J. Math. Anal., 23, 965–969.

Takács, L. [1973]. On an identity of Shih-Chieh Chu, Acta Sci. Math., (Szeged), 34, 383–391.

Thomae, J. [1869]. Beiträge zur Theorie der durch die Heinesche Reihe..., J. Reine Ang. Math., 70, 258–281.

Thomae, J. [1879]. Über die Funktionen welche durch Reihen von der Form dargestellt werden: $1 + \frac{pp'p''}{1q'q''} + \cdots$ , Journal Math., 87, 26–73.

Titchmarsh, E. C. [1937]. Introduction to the Theory of Fourier Integrals, Oxford University Press, London.

Todd, J. [1950]. On the relative extrema of Laguerre orthogonal functions, Bollettino della Unione Matematica Italiana, 5 (3), 120–125.

Tricomi, F. G. and Erdélyi, A. [1951]. The asymptotic expansion of a ratio of gamma functions, Pac. J. Math., 1, 133–142.

Turán, P. [1952]. On a trigonometrical sum, Ann. Soc. Polonaise Math., 25, 155–161.

Tweddle, I. [1988]. James Stirling, Scottish Academic Press, Edinburgh.

van der Poorten, A. [1979]. A proof that Euler missed. . .Apéry's proof of the irrationality of $\zeta(3)$ , Math. Intelligencer, 2, 195–203.

Van Loan, C. [1992]. Computational Frameworks for the Fast Fourier Transform, SIAM, Philadelphia.

Viennot, G. [1983]. Une Theorie Combinatoire des Polynômes Orthogonaux Généraux, Lecture Notes, UQAM.

Vietoris, L. [1958]. Ueber das Vorzeichen gewisser trigonometrischer Summen, Sitzungsber. Oest. Akad. Wiss., 167, 125–135.

Vietoris, L. [1959]. Ueber das Vorzeichen gewisser trigonometrischer Summen, II, Sitzungsber. Oest. Akad. Wiss., 167, 192–193.

Vilenkin, N. J. [1958]. Some relations for Gegenbauer functions, Uspekhi Matem. Nauk (N.S.), 13 (3), 167–172.

Vilenkin, N. J. [1968]. Special Functions and the Theory of Group Representations, Translations of Math. Monographs 22, Amer. Math. Soc., Providence, RI.

Vilenkin, N. J. and Klimyk, A. [1992]. Representation of Lie Groups, Special Functions and Integral Transforms, Kluwer Academic, Amsterdam.

Wallis, J. [1656]. Arithmetica Infinitorum, Oxford.

Wang, Z. X. and Guo, D. R. [1989]. Special Functions, World Scientific, Singapore.

Watson, G. N. [1918]. Asymptotic expansions of Hypergeometric functions, Trans. Cambridge Phil. Soc., 22, 277–308.

Watson, G. N. [1925]. A note on generalized hypergeometric series, Proc. London Math. Soc., (2), 23, xiii–xv (Records for 8 Nov. 1923).

Watson, G. N. [1929]. A new proof of the Rogers–Ramanujan identities, J. London Math. Soc., 4, 4–9.

Watson, G. N. [1944]. A Treatise on the Theory of Bessel Functions, 2nd Ed., Cambridge University Press, Cambridge, UK.

Weil, A. [1949]. Number of solutions of equations in a finite field, Bull. Amer. Math. Soc., 55, 497–508.

Weil, A. [1968]. Sur une formule classique, J. Math. Soc. Japan, 20, 400–402.

Weil, A. [1974]. Two lectures on number theory, past and present, Collected Papers, Vol. III, Springer-Verlag, New York.

Weil, A. [1976]. Elliptic Functions According to Eisenstein and Kronecker, Springer-Verlag, New York.

Weil, A. [1983]. Number Theory, from Hammurabi to Legendre, Birkhäuser, Boston.

Whipple, F. J. W. [1926]. On well-poised series, generalized hypergeometric series having parameters in pairs each pair with the same sum, Proc. London Math. Soc., (2), 24, 247–263.

Whittaker, E. T. [1904]. An expression of certain known functions as generalized hypergeometric series, Bull. Amer. Math. Soc., 10, 125–134.

Whittaker, E. T. and Watson, G. N. [1940]. A Course of Modern Analysis, 4th Ed., Cambridge University Press, London.

Wiener, N. [1933]. The Fourier Integral and Certain of Its Applications, Cambridge. Reprinted by Dover, New York [1958].

Wilkins, J. E. [1948]. Nicholson's integral for $J_{n}^{2}(z) + Y_{n}^{2}(z)$ , Bull. Amer. Math. Soc., 54, 232-234.

Wilson, J. A. [1977]. Three-term contiguous relations and some new orthogonal polynomials, Padé and Rational Approximations, E. B. Saff and R. S. Varga, eds., Academic Press, New York.

Wilson, J. A. [1978]. Hypergeometric series, recurrence relations and some new orthogonal polynomials, Ph.D. Thesis, University of Wisconsin, Madison.

Wilson, J. A. [1991]. Orthogonal functions for Gram determinants, SIAM J. Math. Anal., 22, 1147–1155.

Wong, R. [1989]. Asymptotic Approximations of Integrals, Academic Press, New York.

Zagier, D. [1989]. The dilogarithm in geometry and number theory, in Number Theory and Related Topics, R. Askey et al., eds., Oxford University Press, Oxford, UK, 231–249.

Zeilberger, D. [1982]. Sister Celine's technique and its generalizations, J. Math. Anal. Appl., 85, 114–145.

Zeilberger, D. [1994]. Theorems for a price: Tomorrow's semi-rigorous mathematical culture, The Math. Intelligencer, 16 (4), 11–14.

Abel, N. H., 14, 106, 600, 605

Adams, J. C., 320

Agarwal, R. P., 586

Ahern, P., 36

Airy, G. B., 201

Al-Salam, W. A., 532

Amend, B., 61

Anastassiadis, J., 36

Anderson, G. W., 401, 402, 411, 430

Andrews, G. E., 171, 175, 574, 590, 592

Anno, M., 450

Aomoto, K., 401, 402, 406, 407, 428, 440

Apéry, R., 355

Archimedes, 485

Artin, E., 34, 36, 53

Askey, R. A., 67, 185, 314, 322, 363, 369, 391, 394, 505, 519, 575, 592

Auslander, L., 43

Azor, R., 328

Baernstein, A., 355

Bailey, W. N., 93, 124, 143, 144, 147, 150, 152, 154, 170, 173, 174, 181, 182, 184, 185, 277, 319, 386, 398, 400

Bak, J., 306

Barnes, E. W., 61

Bateman, H., 277, 313, 314, 475

Baxter, R. J., xv

Bellman, R., 535, 542

Berggren, L., 139

Berndt, B., 532, 627

Bernoulli, D., 2

Bernoulli, J., 605, 615, 619

Bessel, F. W., 187, 200, 202, 203, 222, 225, 228, 230, 231, 288, 321, 464, 475

Beukers, F., 355

Bieberbach, L., 355, 362, 382

Binet, J. P. M., 28, 29

Boas, R. P., 410

Bochner, S., 464, 542

Bohr, H., 363, 494

Borel, E., 608

Borwein, J., 139

Borwein, P., 139

Brafman, F., 400

Brent, R. P., 138

Bressoud, D. M., 401, 429, 590, 591

Bromwich, T. J., 630

Brown, G., 376

Brown, M., 552

Brualdi, R. A., 371

Burge, W. H., 171

Bustoz, J., 608

Butlewski, Z., 238

Carathéodory, C., 49

Carlson, F., 109

Cartier, P., 371

Cauchy, A. L., 263, 442, 491, 497, 523, 541, 542, 548

Cayley, A., 268

Cesàro, E., 355, 599, 604, 605

Charlier, C. V. L., 349

Chebyshev, P. L., 117

Christoffel, E. B., 240, 261, 272, 373

Chu, S.-C., 67

Clausen, T., 116

Connor, W. G., 576

Cooley, J. W., 43

Cooper, S., 409

Copson, E. T., 463

Cox, D., 134

Darboux, J. G., 240, 243, 271, 272

Davenport, H., 430, 432

de Boor, C., 43

de Branges, L., 152, 355, 382, 520

de Bruin, N. G., 234, 282

de Moivre, A., 18

Dedekind, R., 1

DeSainte-Catherine, M., 330

Hahn, W., 331, 332

Din, A. M., 322

Halmos, P., 468

Dirichlet, P. L., 1, 2, 401, 413, 434, 463, 532, 601

Dixon, A. C., 72, 239

Hamburger, H., 536

Hamilton, W. R., 268

Dougall, J., 71, 143, 147, 182, 183

Durfee, W. P., 567

Hankel, H., 121, 289–291

Hardy, G. H., 363, 410, 532, 572, 578, 608

Dwork, B., 46

Dyson, F. J., 410, 426, 427, 590

Hasse, H., 430, 432, 436

Hecke, E., 445, 458

Heine, E., 274, 491, 520–523

Edwards, A. W. F., 243, 485

Heisenberg, W., 282

Edwards, C. H., 485

Helversen-Pasotto, A., 93

Eisenstein, F. G. M., 12, 42

Herglotz, G., 1

Elliot, E. B., 138

Hermite, C., 100, 198, 266, 269, 271, 273, 299, 531

Erdélyi, A., 68, 111, 615

Euler, L., 1, 2, 4, 469, 471, 490, 493, 497, 501, 508, 521, 523, 524, 553, 564, 627

Hewitt, E., 306, 376

Hickerson, D., 590

Evans, R., 415

Hill, M. J. M., 63

Hille, E., 226, 496

Favard, J., 245, 248

Hölder, O., 647

Fejér, L., 269, 272, 313, 334, 355, 371, 372, 388, 602

Hsü, H.-Y., 321

Hsu, L. C., 186

Feldheim, E., 278, 291, 315, 382, 390

Hurwitz, A., 1, 226

Fermat, P., 1, 485, 486

Hylleraas, E., 322

Ferrers, N. M., 320, 565, 566

Fields, J. L., 615

Ingham, A. E., 394

Fine, N. J., 506

Ireland, K., 432

Foata, D., 371

Ismail, M. E. H., 363, 370, 504, 532, 552

Forrester, P. J., 426, 441

Ivory, J., 99

Fourier, J., 445, 464, 466, 540, 600, 602, 623

Friedrichs, K., 365

Jackson, D., 372, 375, 380

Funk, P., 445, 458

Jackson, F. H., 485, 486, 588

Fuss, N., 2

Jacobi, C. G., 240, 277, 297, 298, 401, 411, 485, 496, 500, 501, 508–510, 548, 591, 592

Gasper, G., 355, 363, 369, 382, 390, 523, 530, 545

Jensen, J. L. W. V., 14

Jimbo, M., xv

John, F., 544

Gauss, C. F., 1, 61, 63, 67, 78, 94, 95, 240, 254, 262, 355, 411, 431, 491, 496, 497, 499, 500, 508, 521, 523

Johnson, W., 542, 630

Jordan, C., 623

Gautschi, W., 212

Gegenbauer, L., 187, 204, 302, 316, 318, 334, 464, 475, 478

Karamata, J., 609

Karlin, S., 396

Gelfond, A., 410

Kenko, T., 183

Gessel, I., 630

Kirillov, A. N., 102

Gillis, J., 328

Klein, F., 65

Godsil, C. D., 266, 277, 328

Goldbach, C., 2

Klimyk, A., xiii

Good, I. J., 371, 427, 630

Knopp, M., 573

Koblitz, N., 540

Gordon, B., 576

Koekoek, R., 331

Gosper, R. W., 116

Kogbetliantz, E., 388

Gould, H. W., 186

Kolberg, O., 573

Graf, J. H., 239, 475

Koornwinder, T. H., 322, 369, 371, 475, 491

Guo, D. R., 29

Gram, J.-P., 277

Gray, J., 84

Kummer, E., 1, 63, 73, 124, 144, 154, 191, 522, 526

Gronwall, T. H., 372, 380

Gross, B., 45

Laguerre, E. N., 266, 273, 282, 290, 292, 306, 330, 363, 368, 370, 418, 635

Lambert, J. H., 608

Landen, J., 103

Olver, F. W. J., 312, 615

Landsberg, M., 542

Opolka, H., 55

Lang, S., 46

Orr, M. McF., 184

Lanzewizky, I. L., 278

Laplace, P. S., 100

Popperitz E., 73

Laurent, P. A., 426, 496, 497

Parseval, M. A., 265

Lebesgue, H., 6, 69, 311

Pascal, B., 482, 485

Legendre, A. M., 132, 136, 162, 199, 240, 252, 277, 311, 334, 496, 535

Petkovšek, M., 166

Pfaff, J. F., 63

Leibniz, G. W., 283, 485, 605

Phragmén, E., 539

Lerch, M., 17

Plana, G. A., 55

Lewin, L., 102

Poincaré, H., 649

Lewy, H., 365

Poisson, S. D., 401, 446, 531, 601, 602, 623, 625, 627

Lilly, G. M., xv

Lindelöf, E., 539

Pollaczek, F., 349

Liouville, J., 82, 99, 307

Lipschitz, R. O., 121

Rademacher, H., 622

Littlewood, J. E., xvi, 648

Rahman, M., xvi, 322, 519, 523, 545

Lorch, L., 188, 229, 231

Lorentz, G. G., 363

Ramanujan, S., 182, 485, 501, 505, 506, 509, 532, 550, 563, 569, 577, 589

Lorentzen, L., 98

Raynal, J., 124

Riemann, B., 1, 63, 65, 73, 160, 497, 532, 536

Maclaurin, C., 618, 626

MacMohan, P. A., 369, 553, 555, 565, 569, 572

Rodrigues, O., 99

Rogers, J. B., 426, 441

Madhava, 59

Rogers, L. J., 72, 319, 530, 575, 577, 579, 582

Magnus, A., 552

Makai, E., 391

Rosen, M., 432

Markov, A., 240, 254, 255, 259, 275

Rothe, H. A., 490, 491, 497

Maxwell, J. C., 479

Roy, R., 59, 100, 183

McGregor, J. L., 396

Rudin, W., 10, 61

Mehler, F. G., 313

Ryser, H. J., 371

Mehta, M. L., 410, 411, 425

Saff, E. B., 188, 231

Meixner, J., 349

Mellin, R. H., 61

Salamin, E., 138

Miller Jr., W., 445

Săpiro, R. L., 475

Milne, S. C., xv, 649

Sarmanov, I. O., 368

Moak, D. S., 544

Schützenberger, M.-P., 485

Mollerup, J., 494

Schafheitlin, P., 236

Monsky, P., 608

Scharlau, W., 55

Schiff, L. I., 199

Mori, T., 450

Schlömilch, O., 4

Morita, Y., 45

Morris, W. G., 428, 442

Schur, I., 401, 423, 578

Sears, D. B., 524

Muldoon, M. E., 231

Selberg, A., 110, 401, 402, 410, 417, 428

Müller, C., 445

Murphy, R., 240

Sheppard, W. F., 141

Siegel, C. L., 401, 419, 423

Nassarallah, B., 519

Simpson, T., 14

Slater, D., 590

Natanson, I. P., 252, 269

Smith, H. J. S., 542

Nemes, I., 166

Solé, P., 93

Neumann, C. G., 235

Sonine, N. J., 236, 291, 292, 466

Nevai, P., 277, 312, 334

Spence, W., 106

Newman, D. J., 306

Stanton, D., 630

Newman, F. W., 4

Steinig, J., 381

Newton, I., 248, 534

Nicholson, J. W., 187, 224

Stieltjes, T. J., 240, 254, 259, 401, 416, 419, 425, 496, 594

Nielsen, N., 4

Stirling, J., 356, 496, 617, 618

Stokes, G., 223

Stone, M. H., 265

Subbarow, M. V., 574

Swarttouw, R. F., 331

Sylvester, J. J., 566

Szász, O., 306

Szegö, G., 238, 245, 274, 304, 312, 313, 342, 365, 368, 380, 390, 419

Szego, P., 188, 229, 231

Szwarc, R., 323

Takács, L., 70

Tamhankar, M. V., 370

Tannery, J., 72

Thiruvenkatachar, V. R., 569

Thomae, J., 142, 485, 521

Titchmarsh, E. C., 89

Todd, J., 304

Tolimieri, R., 43

Tricomi, F. G., 615

Tukey, J. W., 43

Turán, P., 342, 343, 384

Tweddle, I., 18, 652

van der Poorten, A., 394

Van Loan, C., 43

Vandermonde, A., 70

Varga, R. S., 188, 231

Venkatachaliengar, K., 569

## Index

Victor, J. D., 328

Viennot, G., 277, 330

Viéte, F., 243

Vietoris, L., 355, 375, 377, 380, 398

Vilenkin, N. J., 315, 382, 445

Vitali, G., 496

von Staudt, C., 57

Waadelund, H., 98

Wallis, J., 4

Wang, Z. X., 29

Watson, G. N., 149, 179, 227, 237, 385, 512, 547, 548, 587, 614

Weierstrass, C., 4, 463

Weil, A., 501, 538

Whipple, F. J. W., 124, 130, 141, 143, 144, 146, 181, 355, 362, 632–634

Whittaker, E. T., 187, 195, 198, 512

Wiener, N., 289

Wiles, A., 509

Wilf, H., 125

Wilkins, J. E., 224

Wilson, J. A., 124, 152, 154, 157, 184, 277, 293, 331

Wong, R., 614

Zagier, D., 102

Zeilberger, D., 125

Zeller, K., 363

Abel summability, 599  
absolutely monotonic series, 389  
adjacency matrix, 266  
arithmetic-geometric mean, 134  
associated Legendre function, 456  
asymptotic expansion, 611  

Bailey chain, 586  
Bailey pair, 586  
Bailey's $9F_{8}$ transformation, 182  
Bailey's lemma, 584  
Barnes's beta integral, 90  
basic hypergeometric series, 523  
k-balanced, 524  
well-poised, 524  
Bernoulli numbers, 12  
Bernoulli polynomials, 20, 615  
generalized, 615  

Bessel functions, 200, 204–206, 212  
Bessel's formula, 212  
Gegenbauer's formula, 205  
generating function, 212  
Hankel's formula, 206  
Poisson integral, 204  
second kind, 200  

Bessel's equation, 200  
Bessel's inequality, 264  
beta integral, 4  

Carlson's theorem, 110  
Cesàro summability, 599  
characters, 38, 57  
additive, 38  
even, 58  
multiplicative, 38  
odd, 58  
primitive, 79  

Charlier polynomials, 347  
Chebyshev polynomials, 101, 102  
first kind, 101  
fourth kind, 102

second kind, 101
third kind, 102
Christoffel–Darboux formula, 246
Chu–Vandermonde identity, 67
Clausen's identity, 116
confluent hypergeometric equation, 188, 190, 194
asymptotic solutions, 190
recessive solutions, 194
contiguous $_{4}F_{3}$ , 155
cosine integral, 235
Coulomb wave function, 199

Darboux's method, 310
Dedekind η-function, 538
digamma function, 13
dilogarithm, 102
Dirichlet L-function, 58, 59
functional equation, 60
Dirichlet problem, 463
discriminant, 418
Dougall's $_{7}F_{6}$ formula, 147, 152
Bailey's $_{7}F_{6}$ integral analog, 152
Dougall's bilateral sum, 110
Dougall's identity, 71
Dyson's integral, 426

elliptic functions, 508
elliptic integrals, 132, 136
first kind, 132
second kind, 136
Erdélyi's formula, 113
error function, 196
Euler's angles, 469
Euler's reflection formula, 9
Euler's transformation, 69
Euler–Maclaurin summation formula, 18
Eulerian integral, 6
first kind, 6
second kind, 6

Fermat measure, 486
finite-dimensional representation of a group, 466, 467, 469
irreducible representation, 469
isomorphism of, 467
subrepresentation, 469
unitary representation, 467
fractional integral, 605
fractional integration, 111
Fresnel integrals, 235
Funk–Hecke formula, 459

gamma function, 3, 6, 23, 44
Gauss's multiplication formula, 23
integral representation, 6
p-adic, 44
product representation, 3
Gauss quadrature formula, 250
Gauss sums, 38, 627
reciprocity, 627
Gauss's summation formula, 67, 90
integral analog, 90
Gegenbauer polynomials, 302
Gegenbauer's addition formula, 215
Gegenbauer's product formula, 478
Gibbs phenomenon, 372
Gosper's algorithm, 163
Graf's formula, 215

Harr measure, 468
Hahn polynomials, 331, 345, 346
continuous, 331
continuous dual, 331
dual Hahn, 346
Hankel functions, 208
Hankel pair, 216, 290
Hankel transforms, 216, 289
harmonic polynomial, 446
Hasse–Davenport relation, 432
Heine's transformation formula, 520
Hermite polynomials, 278–280, 318, 419
discriminant, 419
generating function, 279
linearization formula, 318
orthogonality, 278
Poisson kernel, 280
Hurwitz zeta function, 15
hypergeometric differential equation, 75
hypergeometric functions, 64, 65, 87, 88, 94, 97, 125, 130
asymptotic expansion, 88
Barnes's integral, 87
contiguous relations, 94
continued fraction, 97
cubic transformations, 130
integral representation, 65
quadratic transformations, 125

hypergeometric series, 61, 70, 140, 146
balanced, 70
k-balanced, 140
nearly poised, 140
very well poised, 146
well-poised, 140
hypergeometric term, 163

incomplete gamma function, 197

Jackson's formula, 587
Jacobi elliptic functions, 510
Jacobi polynomials, 99, 298, 475, 476
generating function, 298
Koornwinder's product formula, 476
Laplace-type integral, 475
Poisson kernel, 385
Jacobi sums, 39

kernel polynomial, 260
Krawtchouk polynomials, 347
Kummer's first transformation, 191
Kummer's second transformation, 191

L-function, 434
Lagrange interpolation, 249
Lagrange inversion formula, 629
Laguerre polynomials, 283, 288, 418
discriminant, 418
generating-function, 283
Poisson kernel, 288
Lambert summable, 608
Landen's transformation, 103
Laplace equation, 198
Laplace transforms, 536
Legendre polynomials, 252
Legendre's differential equation, 162
Legendre's duplication formula, 22
Legendre–Féjer polynomials, 334
Lerch's theorem, 18
logarithmic convexity, 34
logarithmic integral, 197

MacMahon's Master Theorem, 369
Markov–Stieltjes inequalities, 254
matching polynomials, 324
Meixner polynomials, 346
Meixner–Pollaczek polynomials, 348
Mellin transforms, 85, 534
Miller's algorithm, 211
modified Bessel functions, 222
modular forms, 540
modular group, 540

Nicholson's formula, 224
noncommutative binomial theorem, 48 orthogonal matrix, 452
orthogonal polynomials, 452

parabolic cylinder functions, 198
Parseval's formula, 264
partition analysis, 555
partitions, 553, 559, 566–569
congruences, 569
conjugate, 567
Durfee square, 567
Ferrers graph, 566
Frobenius symbol, 568
generating functions, 559
pentagonal number
theorem, 501
Pfaff's transformation, 69
Pfaff–Saalschütz identity, 69, 91, 92
integral analog, 91
nonterminating form, 92
Poisson summation formula, 623

q-beta integrals, 514
q-binomial coefficients, 483
q-binomial theorem, 488
q-difference operator, 488
q-Dixon formula, 588
q-Dougall formula, 588
q-gamma function, 493
q-Gauss summation formula, 521
q-Hermite polynomials, 530, 531
generating function, 532
linearization formula, 532
Poisson kernel, 532
q-integral, 486
q-Jacobi polynomials, 592, 593
big, 593
little, 592
q-Kummer sum, 522
q-Laguerre polynomials, 593
q-Pfaff–Saalschütz identity, 524
q-ultraspherical polynomials, 527, 530
connection coefficient formula, 531
linearization formula, 531
quadratic reciprocity law, 53
quintuple product identity, 545

Racah polynomials, 344
radial functions, 464
Ramanujan's $_{1}\psi_{1}$ formula, 505
reciprocal polynomials, 150
resultant, 414

Riemann zeta function, 15, 16
functional relation, 16
Rogers–Ramanujan identities, 565, 578
partition theoretic interpretation, 565

Schrödinger equation, 199
Schur's inequality, 423
Sears transformation, 524
Selberg sum, 435
Selberg's integral formula, 402
Aomoto's extension, 402
shifted factorial, 2
Siegel's inequality, 420
sine integral, 235
Sonine's integrals, 218
spherical harmonics, 451, 456
addition theorem, 456
Stieltjes's problem, 415
Stieltjes–Wigert polynomials, 594
Stirling numbers, 356
Stirling's formula, 18
Sturm's comparison theorem, 227

theta functions, 509
triple product identity, 497
Turán's inequality, 342

ultraspherical polynomials, 302, 303, 316, 319, 462
addition formula, 462
generating function, 302
Laplace integral, 316
linearization formula, 319
Rodrigues's formula, 303

Vietoris's inequalities, 377

W–Z method, 167
Watson's $_{8}\phi_{7}$ transformation, 587
Watson's lemma, 614
Weber's equation, 198
Whipple's $_{4}F_{3}$ transformation, 140
Whipple's $_{7}F_{6}$ transformation, 143
Whittaker functions, 195
Whittaker's equation, 195
Wilson polynomials, 158
orthogonality, 158
Wilson's integral, 151
Wronskian, 136

zonal harmonics, 455

<table><tr><td>(a)n, 2</td><td>Iα(x), 222</td></tr><tr><td>(a; q)k, 487</td><td>J(χ, η), 39</td></tr><tr><td>B(x, y), 4</td><td>Jα(x), 200</td></tr><tr><td>Bn, 12</td><td>Jn, 325</td></tr><tr><td>Bn(x), 20</td><td>K(k), 132</td></tr><tr><td>Bq(α, β), 494</td><td>Kα(x), 223</td></tr><tr><td>C(x), 235</td><td>Kn(x; p, N), 347</td></tr><tr><td>Ci(x), 235</td><td>L(λ, t), 433</td></tr><tr><td>cn(u, k), 511</td><td>li, 197</td></tr><tr><td>Cλn(x), 302</td><td>Li2(x), 102</td></tr><tr><td>Cn(x; β | q), 527</td><td>Llmx, 106</td></tr><tr><td>Cn(x; a), 347</td><td>Lnα(x), 283</td></tr><tr><td>C*, 37</td><td>Lnα(x; q), 594</td></tr><tr><td>di,j(n), 506</td><td>Ln(α)(x; q), 593</td></tr><tr><td>dn(u, k), 511</td><td>M(a, b), 134</td></tr><tr><td>Dλn(x), 322</td><td>Mn(x; b, c), 346</td></tr><tr><td>Dn(x), 198</td><td>Mk,m(x), 195</td></tr><tr><td>Dq f, 529</td><td>NFs/F, 430</td></tr><tr><td>E(k), 136</td><td>P{α, β, γ} {a1, b1, c1, x} {a2, b2, c2}</td></tr><tr><td>eq(x), 492</td><td>p(N, M, n), 561</td></tr><tr><td>erf, 196</td><td>p(m, n), 562</td></tr><tr><td>erfc, 196</td><td>pA(n), 554</td></tr><tr><td>Eq(x), 492</td><td>pA(s)(n), 554</td></tr><tr><td>F(a+), 96</td><td>pO(n) = pN(1)(n), 554</td></tr><tr><td>pFq(a1, ..., ap; b1, ..., bq; x), 62</td><td>pm(j, n), 560</td></tr><tr><td>pFq(a1, ..., ap; x), 62</td><td>pn(x; a, b, c, d), 331</td></tr><tr><td>pFq(b1, ..., bq); x)</td><td>pn(x; α, β; q), 592</td></tr><tr><td>pFq, 62</td><td>pn^λ(x; φ), 348</td></tr><tr><td>g(χ), 38</td><td>Pk(x), 457</td></tr><tr><td>g(χ^α), g(α), 435</td><td>Pn(α,β)(x; c, d; q), 593</td></tr><tr><td>g(φ, θ, ψ), 470</td><td>Pn(α,β)(x), 99</td></tr><tr><td>g*(α), 435</td><td>Jn(x), 326</td></tr><tr><td>GL(V), 466</td><td>Q(N, M, n), 561</td></tr><tr><td>h(x, a), 516</td><td>Qm(n), 559</td></tr><tr><td>Hα(1)(x), 208</td><td>Qm(j, n), 560</td></tr><tr><td>Hα(2)(x), 208</td><td>Qm(k,l)(n), 559</td></tr><tr><td>Hε, 472</td><td>Qn(x; α, β, N), 345</td></tr><tr><td>Hm(x), 446</td><td></td></tr><tr><td>Hn(x), 278</td><td></td></tr><tr><td>Hn(x | q), 530</td><td></td></tr><tr><td>Hem(x), 324 $Q_p, 45$ </td><td> $\mathbb{Z}(p), 37$ </td></tr><tr><td> $R(F, G), 414$ </td><td> $\mathbb{Z}(p)^*, 38$ </td></tr><tr><td> $r_s(n), 506$ </td><td> $\int f(x)d_qx, 486$ </td></tr><tr><td> $R_n(\lambda(x)), 346$ </td><td> $\langle x, y \rangle, 467$ </td></tr><tr><td> $R_n(\lambda(x); \gamma, \delta, N), 344$ </td><td> $[{}_k^n]q, 483$ </td></tr><tr><td> $S(x), 235$ </td><td> $\lfloor q/2 \rfloor, 15$ </td></tr><tr><td> $\text{sn}(u, k), 510$ </td><td> $(\alpha, k), 209$ </td></tr><tr><td> $\text{Si}(x), 235$ </td><td> $\alpha(G), 324$ </td></tr><tr><td> $SL_2(\mathbb{C}), 471$ </td><td> $\gamma, 3$ </td></tr><tr><td> $SO(3), 476$ </td><td> $\gamma(a, x), 197$ </td></tr><tr><td> $SU(2), 466$ </td><td> $\Gamma(a, x), 197$ </td></tr><tr><td> $S_k(\xi), 458$ </td><td> $\Gamma(x), 3$ </td></tr><tr><td> $S_n(x; q), 594$ </td><td> $\Gamma_p(x), 45$ </td></tr><tr><td> $S_n(x^2; a, b, c), 331$ </td><td> $\Gamma_q(x), 493$ </td></tr><tr><td> $t_{mn}^\ell(g), 473$ </td><td> $\Delta_qf, 488$ </td></tr><tr><td> $T_\ell, T_\ell(g), 472$ </td><td> $\zeta(s), 15$ </td></tr><tr><td> $T_n(x), 101$ </td><td> $\zeta(x, s), 15$ </td></tr><tr><td> $Tr_{F_s/F}, 430$ </td><td> $\eta(\tau), 538$ </td></tr><tr><td> $U_n(x), 101$ </td><td> $\theta_i(z, q), i = 1, \dots, 4, 510$ </td></tr><tr><td> $V_n(\cos\theta), 102$ </td><td> $\Pi(x), 3$ </td></tr><tr><td> $W(y_1, y_2), 136$ </td><td> $_r\phi_s, 523$ </td></tr><tr><td> $W_n(\cos\theta), 102$ </td><td> $\psi(x), 13$ </td></tr><tr><td> $W_{k,m}(x), 196$ </td><td> $_1\psi_1, 505$ </td></tr><tr><td> $Y_\alpha(x), 200$ </td><td> $\Omega_\geq, 556$ </td></tr><tr><td> $Z_p, 45$ </td><td> $\theta_i(z, q), i = 1, \dots, 4, 509$ </td></tr></table>