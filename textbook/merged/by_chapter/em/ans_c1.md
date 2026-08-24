## Phase 1
### Q1.
1. 错误。点电荷不位于球心，因此体系不为球对称，无法得出球面上各点电场强度大小相等的结论。
2. 正确。高斯定理作为麦克斯韦方程组的一部分，始终成立。
3. 错误。这是1的直接推论。事实上由库仑定律和几何关系也可得到这一命题是错误的。
4. 正确。$\Phi_e=\frac{Q}{\varepsilon_0}$。
5. 错误。此时球面的总电通量为零，但是球面上个点电场强度不等，因此该命题不成立。同样地，也可由库仑定律和几何关系证伪这一命题。

### Q2.
1. 是的。
2. 不能。需要知道 $V$ 内一点的电势，从而确定电势零点。
3. 可以。
4. 名字忘了，总之这种时候电势也是可解的。

### Q3.
1. 正确。这是电流连续性方程的推论，其保证不存在随时间变化的电荷堆积。
2. 正确。这是电磁场边界条件。
3. 正确。这是因为导体交界面上有稳定面电荷堆积。
4. 正确。静电平衡导体没有电流，因此没有电场；恒定电流场，一般情况下存在电流，因此一般情况下存在电场。
5. 错误。这是因为导体交界面上有稳定面电荷堆积，因此 $D_{2n}=D_{1_n}+\sigma$。

### Q4.
1. 会。$q_\text{内}=-q$。可以通过画一个包括空腔的，导体壳内部的高斯面得到。
2. 会。$q_\text{外}=+q$。这是因为导体壳与地面绝缘，总电量始终保持为零。
3. 外表面电荷会变为 $q_\text{外}'=0$。可以通过对空腔外的空间使用唯一性定理得到。
4. 不会。这是静电屏蔽效应，可通过对空腔内部使用唯一性定理证明。
5. 都不会。可以通过对空腔外的空间使用唯一性定理得到。

## Phase 2
### EX A.
介质内部要满足的边界条件自然是法向电位移矢量连续和切向电场强度连续：$D_{1n}=D_{2n},\ \vec E_{1t}=\vec E_{2t}$。这是因为电介质的极化产生束缚电荷而非自由电荷，因此不会有自由面电荷。由此我们可以对每一块介质区域运用唯一性定理。但是我确实不清楚如何从这里推导出完整的唯一性定理，或许需要仿照一般的唯一性定理的证明过程。

### EX B.
$$
E_{1n}=\frac{J_n}{\sigma_1},\ E_{2n}=\frac{J_n}{\sigma_2}\\
D_{1n}=\varepsilon_1\frac{J_n}{\sigma_1},\ D_{2n}=\varepsilon_2\frac{J_n}{\sigma_2}\\
\sigma_f=D_{2n}-D_{1n}=\varepsilon_2\frac{J_n}{\sigma_2}-\varepsilon_1\frac{J_n}{\sigma_1}
$$

（此处不失一般性地假设 $J_n$ 方向为由1至2）

## Re: Phase 1
### Q1.
* 注：这块我不熟，你务必多讲讲
1. $[q_m]=[\mu_0Fr^2]^{1/2}=[Fr/{\varepsilon_0c^2}]^{1/2}=[\frac{Fr^2E}{\sigma c^2}]^{1/2}=[\frac{F^2r^4}{q^2c^2}]^{1/2}=MLT^{-2}\cdot L^2/(IT\cdot L/T)=ML^2T^{-2}I^{-1}$
   $[m]=[IS]=L^2I$，$q_ml=\mu_0m$
2. 类比电偶极子，$\vec H_{q_ml}=\frac{q_ml}{4\pi\mu_0r^3}(2\cos\theta\vec e_r+\sin\theta\vec e_\theta)$
   而由磁矩磁场，$\vec B_{IS}=\frac{\mu_0IS}{4\pi r^3}(2\cos\theta\vec e_r+\sin\theta\vec e_\theta)$
   故得 $q_ml=\mu_0m$
3. 磁荷法的等效结果为介质表面出现等效磁荷，而分子电流模型的等效结果为介质侧面出现绕行的磁化电流。二者是两条不同的研究方式，物理理解完全不同，相互独立，不能认为等效磁荷和磁化电流同时存在。

### Q2.
1. 这一跃变是由局部电荷产生的。通过一个沿局部面电荷的无穷薄的高斯面，可证明远处的电荷对近处的局部的电作用是匀变的，因此也就不存在电场强度的跃变。
2. 
   $$
   E_{in}=E'-\frac{\sigma}{2\varepsilon_0}=0,\ E_{in}=I_0
   $$
   $$
   E'=\frac{\sigma}{2\varepsilon_0},\ E_{out}=E'+\frac{\sigma}{2\varepsilon_0}=\frac{\sigma}{\varepsilon_0}
   $$
   导体内部总场为0，是因为静电学条件下导体内部 $j=0$，因此一定有 $E=0$。
3. $f=\sigma E$ 正确，但 $E=E_{out}$ 不正确。面电荷分布中不同位置的元电荷感受到的电场不同，介于 $0$ 与 $E_{out}$ 之间。

### Q3.
1. 不妨电流沿 $-z$ 方向。$\vec j_c=-j_c\vec e_z$
   $$
   I_0=j_cS+\frac{\mathrm dq}{\mathrm dt},\ j_c=\gamma\cdot\frac{q}{\varepsilon_0\varepsilon_rS}\\q=\frac{\varepsilon_0\varepsilon_rI_0}{\gamma}e^{-\frac{\gamma}{\varepsilon_0\varepsilon_r}t},\ j_c=\frac{I_0}{S}(1-e^{-\frac{\gamma}{\varepsilon_0\varepsilon_r}t})\\\vec j_c=-\frac{I_0}{S}(1-e^{-\frac{\gamma}{\varepsilon_0\varepsilon_r}t})\vec e_z,\\\vec j_p=-\frac{\mathrm d\vec P}{\mathrm dt}=-\varepsilon_0(\varepsilon_r-1)\frac{\mathrm d\vec E}{\mathrm dt}=\varepsilon_0(\varepsilon_r-1)\frac{\mathrm dq}{\mathrm dt}/(\varepsilon_0\varepsilon_r)\vec e_z=(1-\frac{1}{\varepsilon_r})\frac{I_0}{S}e^{-\frac{\gamma}{\varepsilon_0\varepsilon_r}t}\vec e_z\\\vec j_\text{vac}=-\varepsilon_0\frac{\mathrm d\vec E}{\mathrm dt}=\vec j_p/(\varepsilon_r-1)=\frac{1}{\varepsilon_r}\frac{I_0}{S}e^{-\frac{\gamma}{\varepsilon_0\varepsilon_r}t}\vec e_z
   $$
2. 
   $$
   \vec D=+\frac{q}{S}\vec e_z=\frac{\varepsilon_0\varepsilon_rI_0}{\gamma S}e^{-\frac{\gamma}{\varepsilon_0\varepsilon_r}t}\vec e_z,\ \frac{\partial \vec D}{\partial t}=-\frac{I_0}{S}e^{-\frac{\gamma}{\varepsilon_0\varepsilon_r}t}\vec e_z\\\vec j_\text{total}=\vec j_c+\frac{\partial \vec D}{\partial t}=-\frac{I_0}{S}\vec e_z
   $$
3. $\displaystyle j_c/j_p=\frac{1}{\frac{1}{\varepsilon_r}-1}\cdot\frac{1-e^{-\frac{\gamma}{\varepsilon_0\varepsilon_r}t}}{e^{-\frac{\gamma}{\varepsilon_0\varepsilon_r}t}}=\frac{\varepsilon_r}{1-\varepsilon_r}(e^{\frac{\gamma}{\varepsilon_0\varepsilon_r}t}-1)$，$\displaystyle\lim_{t\to+\infty}\frac{j_c}{j_p}=-\infty$，即 $\displaystyle\lim_{t\to+\infty}\vec j_p=0$。这说明电容系统为电流的稳恒造成了弛豫，而 $\vec j_p$ 描述了弛豫过程，$\vec j_c$ 描述了末态过程。$t\ll\tau$ 时弛豫过程占主导，$j_p\gg j_c$；$t\gg\tau$ 时系统基本达到稳态，$j_p\ll j_c$。$\vec H$ 由 $\vec j_\text{total}$ 是麦克斯韦方程组的要求，而 $\vec E$ 的大小和弛豫过程有关，因而与 $\frac{j_c}{j_p}$ 有关。

## Phase 3
### 1.
$$
\vec P=(\varepsilon_r-1)\varepsilon_0\vec E=(\varepsilon_r-1)\varepsilon_0\alpha t\vec e_z\\
\vec j_p=\dfrac{\mathrm d\vec P}{\mathrm dt}=(\varepsilon_r-1)\varepsilon_0\alpha\vec e_z\\
\vec j_\text{vac}=\varepsilon_0\dfrac{\mathrm d\vec E}{\mathrm dt}=\varepsilon_0\alpha\vec e_z\\
\vec j_\text{total}=\vec j_p+\vec j_\text{vac}=\varepsilon_r\varepsilon_0\alpha\vec e_z
$$

### 2.
$$
2\pi rH_\text{in}=\pi r^2j_\text{total},\ \vec H_\text{in}=\frac{r}{2}\cdot\alpha\varepsilon_0\varepsilon_r\vec e_\theta,\ \vec B_\text{in}=\frac{r}{2}\cdot\mu_0\alpha\varepsilon_0\varepsilon_r\vec e_\theta\\
2\pi rH_\text{out}=\pi R^2j_\text{total},\ \vec H_\text{out}=\frac{R^2}{2r}\cdot\alpha\varepsilon_0\varepsilon_r\vec e_\theta,\ \vec B_\text{out}=\frac{R^2}{2r}\cdot\mu_0\alpha\varepsilon_0\varepsilon_r\vec e_\theta
$$

### 3.
全电流为 $I_\text{total}=\pi R^2j_\text{total}=\alpha\pi R^2\varepsilon_0\varepsilon_r$，由极化电流和位移电流组成。

从含介质麦克斯韦方程的角度讲，极化电流就是 $\vec D$ 的一部分，当然要参与 $\vec H,\ \vec B$ 的计算。如果漏掉极化电流会导致不同曲面（例如选择介质外导线的部分）算出的磁通量不一致。