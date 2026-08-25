### **Problem:** 

**Background:** The energy-energy correlator (EEC) in a heavy state probes how energy is distributed on the celestial sphere after acting on the vacuum with a local operator of large scaling dimension. A central physical point is that heavy states exhibit two regimes: a small-angle regime controlled by the light-ray OPE and a broader-angle regime where the energy correlation becomes comparatively flat, reflecting the large number of particles produced by the heavy source.

In planar $\mathcal{N}=4$ SYM, an especially useful choice of heavy source and sink is a pair of half-BPS operators $\mathcal{O}_p$. In the Mellin-space representation, one may write the EEC as
$$
\frac{8 \pi^2}{q^2 \sigma_0} \int d^4x_{13} \, e^{i q\cdot x_{13}} \langle \mathcal{O}_p (x_1) \mathcal{E}(n_2) \mathcal{E}(n_4) \mathcal{O}_p (x_3) \rangle
= \frac{(q^2)^3}{2(q{\cdot}n_2)^3 (q{\cdot}n_4)^3} \int^{i \infty}_{-i \infty} \frac{ds \, dt}{(2\pi i)^2} \mathcal{M}_p(s, t) \mathcal{K}_p(t; \xi),
$$
where the detector kernel is
$$
\mathcal{K}_p (t; \xi) = \sum_{k=0}^2 (-1)^k \binom{2}{k} \xi^{\frac{t}{2}-k}
\frac{\pi^2 \, t (t-2) (t+2-2k) (t+4-2k) \Gamma (p-1) \Gamma (p)  \Gamma \left(p - \frac{t}{2}\right)}{128 \sin^2\left(\frac{\pi t}{2}\right) \Gamma\left(-2-\frac{t}{2}\right) \Gamma\left(p+k-2-\frac{t}{2}\right) \Gamma\left(p-k+3+\frac{t}{2}\right)}
\, {}_2F_1\left(3-k+\frac{t}{2}, 3-k+\frac{t}{2}, p+3-k+\frac{t}{2}; \xi\right).
$$
Because this kernel is built from a hypergeometric-Gamma contour integrand, it is natural to introduce the function basis $I_{m,p}(\xi)$ obtained from the same $t$-integral structure. Evaluating these basis functions is an important intermediate step in deriving explicit heavy-state EEC expressions, which leads to the following problem.

**Problem:** 
In the context of the heavy-state Energy-Energy Correlator (EEC), consider the source and sink to be half-BPS operators representing the heavy states. The relevant function basis $I_{m,p}(\xi)$ can be written as the following integral. Calculate
$$
 I_{m,p}(\xi)=\int_{1/2-i \infty}^{1/2+i \infty} \frac{d t}{2 \pi i}t^{m} \sum_{k=0}^2  (-1)^k \binom{2}{k} \xi^{\frac{t}{2}-k}  {}_2F_1\left(-k+\frac{t}{2}+3,-k+\frac{t}{2}+3;-k+p+\frac{t}{2}+3;\xi\right)  \\
 \times \frac{\pi  t (t-2) (-2 k+t+2) (-2 k+t+4) \Gamma (p-1) \Gamma (p) \Gamma \left(p-\frac{t}{2}\right)}{128 \sin ^2\left(\frac{\pi  t}{2}\right) \Gamma \left(-\frac{t}{2}-2\right) \Gamma \left(k+p-\frac{t}{2}-2\right) \Gamma \left(-k+p+\frac{t}{2}+3\right)}  $$
 for $I_{5,10}(\xi)$.
