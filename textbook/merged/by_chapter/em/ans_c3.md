## Phase 1
### 1.
1. $\Epsilon=\displaystyle\oint(\vec v\times\vec B)\cdot\mathrm d\vec l$
2. 不完整。涡旋电场仅为非静电力部分，回路内还有电荷重新分布导致的静电力。只有前者驱动电流。
3. 并非。这是因为连接电压表两端和回路的导线上也会存在电磁感应电动势。

## P2

1.
$$ m\frac{v^2(t)}{R} = e v(t) B(R,t) $$
$$ m\frac{dv(t)}{dt} = e E_{涡} $$
$$ 2\pi R E_{涡} = \frac{d}{dt}\int_0^R 2\pi r B_z(r,t)\,dr $$
$$ \Rightarrow\ m\frac{dv}{dt} = \frac{e}{R}\int_0^R r\frac{\partial B_z}{\partial t}dr,\qquad \frac{dv}{dt} = e\frac{dA}{dt} $$

2.
$$ v(t) = \frac{eR}{m}B(R,t) $$
$$ \Rightarrow\ R^2\frac{\partial B_z}{\partial t}\Big|_{r=R} = \int_0^R r\frac{\partial B_z}{\partial t}dr $$
$$ R^2\frac{\partial B_z}{\partial t}\Big|_{r=R} = \frac{1}{2}R^2\frac{d}{dt}\bar{B} $$
$$ \frac{\partial B_z}{\partial t}\Big|_{r=R} = \frac{1}{2}\frac{d\bar{B}}{dt} $$

造成电子加速的本质原因是 $R$ 内区域磁场变化带来的在 $r=R$ 上的涡旋电场，$r=R$ 处的 $B$ 仅负责提供向心力。

3.
$$ \vec{P} = \vec{p} - e\vec{A},\quad \frac{d\vec{P}}{dt} = \frac{d\vec{p}}{dt} - e\frac{d\vec{A}}{dt} = -e\vec{v}\times\vec{B} + e\frac{\partial\vec{A}}{\partial t} - e\frac{\partial\vec{A}}{\partial t} - e\vec{v}\cdot\nabla\vec{A} = 0 $$
$$ mv = eA(R,t) + C_0 = eRB(R,t) $$
$$ \frac{d}{dt}\big(A(R,t) - RB(R,t)\big) = 0 $$

$\vec{P}$ 是辅助量，在纯电磁力下守恒。

## P3

1. 是的。粒子运动过程和受外力情况与规范无关。

2.
$$ \vec{F_{12}} = I_2 d\vec{l_2}\times\left(\frac{\mu_0}{4\pi}\frac{I_1 d\vec{l_1}\times\vec{r}}{r^3}\right),\quad \vec{F_{21}} = I_1 d\vec{l_1}\times\left(\frac{\mu_0}{4\pi}\frac{I_2 d\vec{l_2}\times\vec{r}}{r^3}\right) $$
$$ \vec{F_{12}}+\vec{F_{21}}=0 \Leftrightarrow d\vec{l_2}\times(d\vec{l_1}\times\vec{r}) = d\vec{l_1}\times(d\vec{l_2}\times\vec{r}) $$
$$ \Leftrightarrow (d\vec{l_2}\cdot\vec{r})d\vec{l_1} - (d\vec{l_1}\cdot d\vec{l_2})\vec{r} = (d\vec{l_1}\cdot\vec{r})d\vec{l_2} - (d\vec{l_2}\cdot d\vec{l_1})\vec{r} $$
即要求 $d\vec{l_1}\parallel d\vec{l_2}$。

缺失的动量进入了电磁场，以电磁场动量的形式在空间中传播。

前者为正则动量，属于粒子，表现其与场作用的效果；后者属于场本身。

## P4

$\gamma = \dfrac{1}{\sqrt{1-v^2/c^2}}$

1.
$$ E'_{\parallel} = E_{\parallel} $$
$$ \vec{E'_{\perp}} = \gamma(\vec{E_{\perp}} + \vec{v}\times\vec{B_{\perp}}) $$

图见附图

实验室系中的 $\vec{B}$ 可视作是点电荷静止系中的 $\vec{E}$ 经相对论性变换得到的。

$\vec{B}$ 在实验室系真实存在，能产生安培力。

2. 实验室系中存在 $\vec{B}$，对极板有洛仑兹力作用，其与静电力的总作用效果使转矩抵消。
即须同时考虑 $\vec{E}$ 和 $\vec{B}$ 的变化。

## P5

1. $-\varepsilon_2 = M_{12}\dot{I_1}$，$\varepsilon_2$ 与 $I_1$ 均沿正方向或反方向时 $M_{12}<0$，否则 $M_{12}>0$。

2. 
$$ -\varepsilon = (L_1\dot{I_1} \pm M\dot{I_2}) + (L_2\dot{I_2} \pm M\dot{I_1}) $$
$$ = (L_1 + L_2 \pm 2M)\dot{I} $$
相同 / 相反对应 $\pm$ 号。
从磁链的角度，若方向相同，磁场叠加相长，总磁链更大；反之则更小。
从能量的角度，若方向相同，磁场叠加相长，互能为正；反之磁场相消，互能为负。

3. 
这违反了楞次定律，会导致非平衡态无限放大，电磁能量无尽流出。这应该是无外部能源的前提失效。（其实我不太清楚你这里在问什么qwq）

你帮我多讲讲磁矢势和正则动量什么的那块吧，我全忘了（哭）

## Phase 3
### 配置I
1. 吸引。$q$ 形成的电流元沿 $+z$，与 $I$ 同向。
2. 
   $$
   \lambda_+'=\dfrac{\lambda_S}{\sqrt{1-v^2/c^2}}\\
   \lambda_{-0}=\sqrt{1-u^2/c^2}\lambda_S\\
   \lambda_{+}'=\dfrac{\lambda_{-0}}{\sqrt{1-(\frac{u+v}{1-uv/c^2})^2/c^2}}=
   $$
   设 $\frac uc=\th\gamma_1,\frac vc=\th\gamma_2$，则 $\lambda_+'=\ch\gamma_2,\ \lambda_-'=\dfrac{\ch(\gamma_1+\gamma_2)}{\ch\gamma_1}$
   $\ch(\gamma_1+\gamma_2)=\ch\gamma_1\ch\gamma_2+\sh\gamma_1\sh\gamma_2>\ch\gamma_1\ch\gamma_2,\ \lambda_->\lambda_+$，静带电量为负。
3. 
   $$
   \vec B_S=\frac{\mu_0I}{2\pi d}\vec e_\theta\\
   \vec B_{S'}=\frac{1}{\sqrt{1-v^2/c^2}}(\vec B_S-\frac{\vec v}{c^2}\times\vec E_S)=\frac{1}{\sqrt{1-v^2/c^2}}\frac{\mu_0I}{2\pi d}\vec e_\theta\\
   \vec E_{S'}=\frac{1}{\sqrt{1-v^2/c^2}}(\vec E_S-\vec v\times\vec B_S)=-\frac{1}{\sqrt{1-v^2/c^2}}\frac{\mu_0Iv}{2\pi d}\vec e_r\\
   \vec F_S=qv\vec e_z\times\vec B_S=-\frac{\mu_0qIv}{2\pi d}\vec e_r\\
   \vec F_{S'}=q\vec E_{S'}=-\frac{1}{\sqrt{1-v^2/c^2}}\frac{\mu_0qIv}{2\pi d}\vec e_r
   $$
   两力方向一致，$F_{S'}=\frac{1}{\sqrt{1-v^2/c^2}}F_S$。这也可以通过横向动量不变和钟慢效应直接得到。

### 配置II
1. $m\vec v$ 守恒。管外 $\vec B=0$，$\vec F=0$，$\frac{\mathrm dp}{\mathrm dt}=0$，守恒量为 $m\vec v=m\vec v_0$。
   同理，$\vec M=0$，$\frac{\mathrm dL_z}{\mathrm dt}=0$，$\vec L_z=m\vec v_0\times\vec r_0$
   由于机械动量守恒而电磁动量中的磁矢势会随着位置的移动而改变，显然有正则动量不守恒。
   正则角动量 $\vec r\times(m\vec v+q\vec A)$ 守恒。$\vec r\times(m\vec v+q\vec A)=\vec L_z+q\frac{\Phi}{2\pi}\vec e_z$。
   （话说，正则角动量有没有什么统一的符号啊。）
2. $\chi=c\phi$ 在空间中具有多值性，$\nabla\chi$ 定义不明确，无法做为合法的标量势。
   正则角动量始终守恒。$\Delta $