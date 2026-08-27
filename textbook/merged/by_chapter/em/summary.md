# 1
## 模块一：静电场基础（§1–§3）

### §1–§2 电荷、起电、守恒
**已掌握，跳过。** 你Q1对高斯定理的适用边界判断完全正确，说明电荷守恒和叠加原理的底层逻辑没有问题。

### §3 库仑定律与单位制

核心公式：
$$F = \frac{1}{4\pi\varepsilon_0}\frac{q_1 q_2}{r^2}\hat{\mathbf{r}}_{12}$$

**考试区分度不在公式本身，而在量纲和单位制。**

- $\varepsilon_0$ 的量纲：$[\varepsilon_0] = L^{-3}M^{-1}T^4I^2$。教材明确给出了这个推导：从 $F = kq_1q_2/r^2$ 反解 $\varepsilon_0$。
- CGSE单位制（静电单位制）中 $k=1$，电量单位定义为 $\text{e.s.u.}$。换算关系：$1\text{C} = 3.00\times10^9 \text{ e.s.u.}$。
- **易错陷阱**：如果题目同时出现CGSE和SI的量，或者让你做量纲分析，$\varepsilon_0$ 和 $\mu_0$ 的引入/遗漏是最常见的扣分点。你在Q1磁荷量纲推导中已经展示了这个能力，但要注意 $\mu_0$ 的量纲是 $[F]I^{-2} = MLT^{-2}I^{-2}$，与 $\varepsilon_0$ 的量纲互为"倒数结构"（差一个 $c^2$）。

---

## 模块二：磁学基础（§1–§4 磁学部分）

这是你明确说"不熟"的模块，我按最大颗粒度展开。

### §1 磁的库仑定律与磁场强度 $\mathbf{H}$

**物理图像**：
磁荷模型是一个**数学等效工具**，不是物理实在。它的目的是让磁学问题的形式与静电场完全平行，从而可以复用静电场的所有数学方法。

核心公式链：
$$F = \frac{1}{4\pi\mu_0}\frac{q_{m1}q_{m2}}{r^2} \quad \text{(磁的库仑定律)}$$
$$\mathbf{H} = \frac{\mathbf{F}}{q_{m0}} \quad \text{(磁场强度定义)}$$
$$\oint \mathbf{H}\cdot d\mathbf{l} = 0 \quad \text{(无自由电流时，H无旋)}$$
$$\mathbf{H} = -\nabla U_m \quad \text{(磁标势)}$$

**量纲**：
- $q_m$ 的量纲：$ML^2T^{-2}I^{-1}$（即韦伯 Wb）。
- $\mathbf{H}$ 的量纲：$[q_m]/([\mu_0]L^2) = IT^{-1}L^{-1}$（即 A/m）。

**磁偶极子**：
$$U_m = \frac{1}{4\pi\mu_0}\frac{\mathbf{p}_m\cdot\hat{\mathbf{r}}}{r^2}, \quad \mathbf{p}_m = q_m l$$
$$\mathbf{L} = \mathbf{p}_m \times \mathbf{H} \quad \text{(力矩)}$$

**易错陷阱**：
- $\mathbf{H}$ 不是"真实磁场"。真实磁场是 $\mathbf{B}$。$\mathbf{H}$ 是为了计算方便引入的辅助量。
- 磁标势 $U_m$ 只在 $\nabla\times\mathbf{H}=0$（即无自由电流）的区域有效。如果区域内有载流导线，$\mathbf{H}$ 有旋，不能引入标势。
- 磁荷 $q_m$ 是虚构的。不存在孤立的磁单极。

### §2 电流的磁效应与安培分子环流假说

**物理图像**：
奥斯特实验（1820）揭示了电流产生磁场。安培随后提出分子环流假说：磁铁的磁性来源于微观环形电流的定向排列。

**核心结论**：
- 无论传导电流还是磁铁，磁现象的本源都是**电荷的运动**。
- 磁相互作用通过**磁场**传递，是近距作用，不是超距作用。
- 静止电荷之间只有库仑力；运动电荷之间才有磁相互作用。

**考试区分度**：
- 螺线管的极性与电流方向的关系（右手定则）。
- 载流线圈等效为磁偶极子：$\mathbf{m} = IS\hat{\mathbf{n}}$（$\hat{\mathbf{n}}$ 由右手定则确定）。

### §3 安培定律（电流元相互作用）

**物理图像**：
安培定律是恒磁场的基本定律，类比于静电场的库仑定律。但电流元与点电荷有本质区别：**不存在孤立的恒定电流元**，电流元总是闭合回路的一部分。

核心公式：
$$d\mathbf{F}_{12} = \frac{\mu_0}{4\pi}\frac{I_1 I_2 \, d\mathbf{l}_2 \times (d\mathbf{l}_1 \times \hat{\mathbf{r}}_{12})}{r_{12}^2}$$

**这是整章最容易被符号滥用搞崩的公式。** 我拆成三层：

**第一层：大小**
$$dF_{12} \propto \frac{I_1 dl_1 \sin\theta_1 \cdot I_2 dl_2 \sin\theta_2}{r_{12}^2}$$
- $\theta_1$ 是 $d\mathbf{l}_1$ 与 $\hat{\mathbf{r}}_{12}$ 的夹角。
- $\theta_2$ 是 $d\mathbf{l}_2$ 与 $d\mathbf{l}_1\times\hat{\mathbf{r}}_{12}$（即两者所在平面的法线）的夹角。

**第二层：方向**
$d\mathbf{F}_{12}$ 在 $d\mathbf{l}_1$ 和 $\hat{\mathbf{r}}_{12}$ 组成的平面内，且垂直于 $d\mathbf{l}_2$。方向由双重叉积 $d\mathbf{l}_2\times(d\mathbf{l}_1\times\hat{\mathbf{r}}_{12})$ 的右手定则确定。

**第三层：牛顿第三定律失效**
- 电流元之间的力**不一定满足**牛顿第三定律：$d\mathbf{F}_{21} \neq -d\mathbf{F}_{12}$（一般情况下）。
- 但沿闭合回路积分后，总力满足牛顿第三定律。
- **物理原因**：电磁场本身携带动量和角动量。电流元不是封闭系统，它与电磁场交换动量。只有"电荷+电磁场"整体才满足动量守恒和角动量守恒。

**安培的四个实验（示零法）**：
这是教材中非常精彩但考试可能直接考的内容。四个实验的逻辑链：

| 实验 | 操作 | 结论 |
|:---|:---|:---|
| 实验一 | 对折导线，反平行电流，靠近无定向秤 | 电流反向时，作用力也反向 |
| 实验二 | 将一段换成绕另一段的螺旋线 | 电流元具有矢量性，合作用=矢量叠加 |
| 实验三 | 圆弧形导体绕圆心转动 | 作用在电流元上的力与电流元垂直 |
| 实验四 | 三个几何相似线圈，线度比 $1/n:1:n$ | 几何线度同倍放大时，作用力不变 |

加上一个**假设**：两电流元间作用力沿它们的联线。

由此推导出安培最初发表的公式（2.14）：
$$d\mathbf{F}_{12} = -kI_1I_2\mathbf{r}_{12}\left[\frac{2}{r_{12}^3}(d\mathbf{l}_1\cdot d\mathbf{l}_2) - \frac{3}{r_{12}^5}(d\mathbf{l}_1\cdot\mathbf{r}_{12})(d\mathbf{l}_2\cdot\mathbf{r}_{12})\right]$$

**关键辨析**：
- 安培原始公式（2.14）满足牛顿第三定律（$d\mathbf{F}_{21}=-d\mathbf{F}_{12}$），且力沿联线。
- 现代通用公式（2.12）一般不满足牛顿第三定律，力也不一定沿联线。
- 但两者对**闭合回路**的积分结果完全一致。
- 在恒定条件下，无法用实验区分哪个"正确"。但在非恒定条件下（如单个运动电荷），实验结果与（2.12）符合。

**易错陷阱**：
- 考试可能问"电流元之间的力是否满足牛顿第三定律"。答案：**不一定**。但闭合回路之间的总力一定满足。
- 如果题目给的是两个平行电流元（$\theta_1=\theta_2=\pi/2$），则 $d\mathbf{F}_{21}=-d\mathbf{F}_{12}$，看起来满足牛顿第三定律。但这只是特殊情况。
- 如果两个电流元共线（$\theta_1=\theta_2=0$），则 $d\mathbf{F}_{12}=0$ 但 $d\mathbf{F}_{21}\neq 0$。这是教材例题3的结论，非常反直觉，但完全正确。

### §4 电流单位安培的定义

**物理图像**：
安培是SI基本单位之一，其定义基于安培定律。

$$\mu_0 = 4\pi\times10^{-7} \text{ N/A}^2$$

这个数值是**定义出来的**，不是测量出来的。通过固定 $\mu_0$ 的值，反过来定义了安培。

**考试区分度**：
- 如果题目问"$\mu_0$ 是怎么确定的"，答案是"通过定义安培来确定"，而不是"通过实验测量"。
- 安培秤（天平）测量的是闭合回路之间的力，不是电流元之间的力。

---

## 模块三：电磁感应（§3 电磁感应部分）

### 法拉第电磁感应定律

核心公式：
$$\mathcal{E} = -\frac{d\Phi}{dt} \quad \text{(单匝)}$$
$$\mathcal{E} = -N\frac{d\Phi}{dt} \quad \text{(N匝，每匝磁通相同)}$$
$$\mathcal{E} = -\frac{d\Psi}{dt} \quad \text{(N匝，每匝磁通不同，}\Psi=\sum\Phi_i\text{)}$$

**符号约定（这是考试最容易扣分的地方）**：
- 先标定回路绕行方向。
- 用右手定则确定法线 $\mathbf{n}$ 方向（四指弯曲=绕行方向，拇指=法线方向）。
- $\Phi = \iint \mathbf{B}\cdot d\mathbf{S}$：若 $\mathbf{B}$ 与 $\mathbf{n}$ 夹角为锐角，$\Phi>0$；钝角，$\Phi<0$。
- $\mathcal{E}>0$ 表示电动势方向与标定绕行方向一致；$\mathcal{E}<0$ 表示相反。
- 负号的物理意义：$\mathcal{E}$ 的正负总是与 $d\Phi/dt$ 的正负**相反**。

**易错陷阱**：
- 感应电动势比感应电流更本质。即使回路不闭合（断路），感应电动势依然存在，只是没有感应电流。
- "磁通量变化"包括三种情况：$\mathbf{B}$ 变化、回路面积变化、回路与 $\mathbf{B}$ 的夹角变化。不能只想到 $\mathbf{B}$ 变化。
- 多匝线圈中，如果每匝磁通不同，不能直接写 $\mathcal{E}=-Nd\Phi/dt$，必须写 $\mathcal{E}=-d\Psi/dt$。

### 楞次定律

**物理图像**：
感应电流的方向总是使得它激发的磁场**阻碍**引起感应电流的磁通量变化。

更一般的表述：感应电流的**效果**总是反抗引起感应电流的**原因**。
- "原因"可以是磁通量变化，也可以是相对运动或回路形变。
- "效果"可以是感应电流激发的磁场，也可以是机械力。

**能量守恒的体现**：
如果感应电流的效果不反抗原因，就会出现"既对外做功又释放焦耳热"的永动机，违反能量守恒。

**易错陷阱**：
- "阻碍变化"≠"阻碍磁场"。如果磁通量在减小，感应电流激发的磁场与原磁场**同向**（试图阻止减小），而不是反向。
- 楞次定律和法拉第定律（负号）是等价的，但楞次定律在判断**机械效果**时更方便。

### 涡电流与电磁阻尼

**物理图像**：
大块金属在变化磁场中或相对磁场运动时，内部产生闭合的感应电流，流线呈涡旋状。

**核心应用**：
- 高频感应电炉（利用涡流热效应）
- 叠片铁芯减小涡流损耗（硅钢片平面平行于磁感应线，片间绝缘）
- 电磁阻尼（楞次定律的机械效果）
- 电磁驱动（异步电动机原理，圆盘转速总小于磁铁转速）

**易错陷阱**：
- 叠片铁芯的原理不是"增大电阻"这么简单，而是"把涡流限制在各薄片内"。硅钢片本身的电阻率较大是次要因素，主要因素是片间绝缘层切断了涡流的大回路。
- 电磁驱动是**异步**的：如果圆盘转速等于磁铁转速，相对运动为零，磁通量不变化，感应电流为零，驱动力为零。所以圆盘转速必须小于磁铁转速。

---

## 模块四：电介质（§4）

### §1 极化的宏观表现

**物理图像**：
电介质插入电容器后，电容增大。原因是极化电荷产生的附加场 $E'$ 削弱了总场 $E$，从而降低了电压 $U=Ed$。

**与导体的关键区别**：
- 导体：自由电荷重新分布，感应电荷可以**完全抵消**内部电场（$E_{in}=0$）。
- 电介质：束缚电荷微小位移，极化电荷只能**部分削弱**内部电场（$E_{in}\neq 0$）。

### §2 极化的微观机制

**两种极化机制**：

| 机制 | 适用对象 | 微观过程 | 频率响应 |
|:---|:---|:---|:---|
| 位移极化 | 无极分子（$H_2, N_2, CCl_4$） | 正负电荷重心在外场下错开 | 高频仍有效（电子惯性小） |
| 取向极化 | 有极分子（$H_2O$） | 固有电矩在外场下转向 | 高频失效（分子惯性大） |

**易错陷阱**：
- 有极分子介质中，取向极化比位移极化强约一个数量级，取向极化是主要的。
- 但在高频电场下，取向极化跟不上外场变化，只剩位移极化。
- 所以高频下所有介质的极化机制都退化为位移极化。

### §3 极化强度 $\mathbf{P}$ 与极化电荷

核心公式：
$$\mathbf{P} = \frac{\sum \mathbf{p}_{\text{分子}}}{\Delta V} \quad \text{(定义)}$$
$$\oiint \mathbf{P}\cdot d\mathbf{S} = -\sum q' \quad \text{(极化电荷与P的通量关系)}$$
$$\sigma_e' = \mathbf{P}\cdot\mathbf{n} = P_n \quad \text{(表面极化电荷面密度)}$$

**易错陷阱**：
- 均匀电介质内部 $\rho_e'=0$（极化电荷只在表面）。但**非均匀**电介质内部可以有 $\rho_e'\neq 0$。
- $\sigma_e' = \mathbf{P}\cdot\mathbf{n}$ 中的 $\mathbf{n}$ 是介质表面的**外法向**。如果 $\mathbf{P}$ 与 $\mathbf{n}$ 夹角为锐角，$\sigma_e'>0$（正极化电荷）；钝角，$\sigma_e'<0$。
- 极化电荷是**束缚电荷**，不能离开介质转移到其他导体上。这是与导体上感应电荷的本质区别。

### §4 退极化场

核心公式：
$$\mathbf{E} = \mathbf{E}_0 + \mathbf{E}' \quad \text{(总场=外场+极化电荷的场)}$$

退极化场 $\mathbf{E}'$ 在介质内部与外场 $\mathbf{E}_0$ 方向相反，起减弱极化的作用。

**形状依赖（这是考试高频考点）**：

| 几何形状 | 退极化场 | 备注 |
|:---|:---|:---|
| 无限大平板（$\mathbf{P}\perp$ 板面） | $E' = P/\varepsilon_0$ | 最强 |
| 均匀极化球 | $E' = P/(3\varepsilon_0)$ | 球的1/3因子 |
| 细长棒（沿轴极化） | $E' \approx 0$ | 可忽略 |

**物理直觉**：纵向尺度越大、横向尺度越小，退极化场越弱。

**易错陷阱**：
- 退极化场的大小与几何形状密切相关。不能把球的结论套用到棒上。
- 平行板电容器中电介质的退极化场最强（$E'=P/\varepsilon_0$），这是因为极化电荷均匀分布在两个平行平面上。

### §5 极化率与线性介质

核心公式：
$$\mathbf{P} = \chi_e \varepsilon_0 \mathbf{E} \quad \text{(各向同性线性介质)}$$

其中 $\chi_e$ 是极化率，与场强无关，是材料属性。

**自洽逻辑链（这是考试推导题的核心）**：
$$\mathbf{P} \xrightarrow{\text{决定}} \sigma_e' \xrightarrow{\text{决定}} \mathbf{E}' \xrightarrow{\text{决定}} \mathbf{E}=\mathbf{E}_0+\mathbf{E}' \xrightarrow{\text{决定}} \mathbf{P}$$

这四个量互相依赖、互相制约。计算任何一个，都必须联立所有关系。

**例题：介质球在均匀外场中**
$$\mathbf{E} = \mathbf{E}_0 - \frac{\mathbf{P}}{3\varepsilon_0} = \mathbf{E}_0 - \frac{\chi_e\mathbf{E}}{3}$$
$$\Rightarrow \mathbf{E} = \frac{\mathbf{E}_0}{1+\chi_e/3}$$

**例题：平行板电容器充满介质**
$$E = \frac{E_0}{1+\chi_e} = \frac{\sigma_{e0}}{(1+\chi_e)\varepsilon_0}$$
$$C = (1+\chi_e)C_0 = \varepsilon C_0$$

### §6 电位移矢量 $\mathbf{D}$ 与介质中的高斯定理

核心公式：
$$\mathbf{D} = \varepsilon_0\mathbf{E} + \mathbf{P} \quad \text{(定义)}$$
$$\oiint \mathbf{D}\cdot d\mathbf{S} = \sum q_0 \quad \text{(介质中的高斯定理)}$$
$$\mathbf{D} = \varepsilon\varepsilon_0\mathbf{E} \quad \text{(线性各向同性介质)}$$

其中 $\varepsilon = 1+\chi_e$ 是相对介电常量。

**$\mathbf{D}$ 的物理意义**：
$\mathbf{D}$ 是一个辅助量，引入它的目的是**消去极化电荷**，使得高斯定理只包含自由电荷。

**最关键的易错点（教材明确强调但学生经常忽略）**：

$$D = \varepsilon_0 E_0 \quad \text{这个关系式是有条件的！}$$

**成立条件**：均匀电介质充满电场所在的全部空间，或者均匀电介质的表面是等势面。

**不成立时**：$D \neq \varepsilon_0 E_0$，$E \neq E_0/\varepsilon$。

**反例**：沿轴均匀极化的介质细棒，中点退极化场 $E'\approx 0$，所以 $E\approx E_0$，$D = \varepsilon\varepsilon_0 E \approx \varepsilon\varepsilon_0 E_0 \neq \varepsilon_0 E_0$。

**为什么 $D$ 和 $\varepsilon_0 E_0$ 满足同一形式的高斯定理但不相等？**
因为高斯定理只反映矢量场的一个侧面（散度），不能完全确定矢量场。反映另一个侧面（旋度）的是环路定理：
- $\oint \mathbf{E}_0\cdot d\mathbf{l} = 0$（真空场无旋）
- $\oint \mathbf{D}\cdot d\mathbf{l} \neq 0$（一般情况下 $\mathbf{D}$ 有旋！）

**这是考试极爱考的辨析题。** 很多学生看到 $\oiint \mathbf{D}\cdot d\mathbf{S} = \sum q_0 = \oiint \varepsilon_0\mathbf{E}_0\cdot d\mathbf{S}$，就直接写 $\mathbf{D}=\varepsilon_0\mathbf{E}_0$。这是错的。两个矢量散度相同不代表矢量本身相同。

---

## 模块五：恒定电流场（§5）

### §1 电源电动势、内阻与路端电压

**物理图像**：
电源内部存在非静电力 $\mathbf{K}$，它把正电荷从负极搬到正极，维持电势差。

**核心公式**：
$$\text{放电：} U = \mathcal{E} - Ir$$
$$\text{充电：} U = \mathcal{E} + Ir$$

**易错陷阱（符号滥用重灾区）**：
- 放电时，电流从负极流向正极（在电源内部），$U < \mathcal{E}$。
- 充电时，电流从正极流向负极（在电源内部），$U > \mathcal{E}$。
- 判断一个电源是充电还是放电，看电流在电源内部的方向：从负到正=放电，从正到负=充电。
- 在复杂电路中，不能一眼看出某个电源是充电还是放电。需要先假设方向，解方程后由电流正负判断。

**功率转化**：
$$\text{放电：} UI = \mathcal{E}I - I^2r \quad \text{(非静电能→外电路+焦耳热)}$$
$$\text{充电：} UI = \mathcal{E}I + I^2r \quad \text{(外电路输入→非静电能储存+焦耳热)}$$

**理想电压源**：$r=0$，则 $U=\mathcal{E}$ 恒成立，无论电流方向和大小。

### §2 化学电源（丹聂耳电池）

**物理图像**：
丹聂耳电池由锌极（负极）和铜极（正极）分别浸在硫酸锌和硫酸铜溶液中组成。

**非静电力的来源**：
- Zn极：化学亲和力使 $Zn^{2+}$ 溶解到溶液中，把负电荷留在Zn极板上。形成电偶极层。
- Cu极：化学亲和力使 $Cu^{2+}$ 从溶液淀积到Cu极板上，使Cu极带正电。形成电偶极层。

**电动势**：
$$\mathcal{E} = U_{AD} + U_{CB}$$
其中 $U_{AD}$ 是Cu极与溶液间的电势跃变，$U_{CB}$ 是溶液与Zn极间的电势跃变。

**放电时的路端电压**：
$$U_{AB} = U_{AD} + U_{CB} - U_{CD} = \mathcal{E} - Ir$$
其中 $U_{CD}$ 是溶液内部的电势降落（溶液电阻 $r$ 上的 $Ir$）。

**易错陷阱**：
- 电动势 $\mathcal{E}$ 是**非静电力**做功的度量，不是静电力。它等于两个电偶极层处电势跃变之和。
- 溶液内部有电阻，所以放电时溶液内部有电势降落 $Ir$。开路时溶液内部各处电势相等。

### §3 温差电效应

**三种效应的完整拆解**：

| 效应 | 条件 | 物理机制 | 可逆性 |
|:---|:---|:---|:---|
| 汤姆孙效应 | 同种金属，两端温度不同 | 自由电子热扩散→非静电力 | 可逆（电流反向，吸放热反转） |
| 佩尔捷效应 | 两种不同金属接触面 | 自由电子数密度不同→扩散 | 可逆（电流反向，吸放热反转） |
| 焦耳热 | 任何有电阻的导体 | 电流通过电阻 | **不可逆**（与电流方向无关） |

**汤姆孙电动势**：
$$\mathcal{E}(T_1,T_2) = \int_{T_1}^{T_2}\sigma(T)dT$$
其中 $\sigma(T)$ 是汤姆孙系数（注意：这里用 $\sigma$ 表示汤姆孙系数，不要与电导率 $\sigma$ 混淆！教材用的是同一个符号，但物理意义完全不同）。

**佩尔捷电动势**：
$$\Pi_{AB}(T)$$
表示金属A、B在温度 $T$ 接触时的佩尔捷电动势。
$$\Pi_{BA}(T) = -\Pi_{AB}(T)$$

**泽贝克电动势（温差电动势）**：
$$\mathcal{E}_{AB} = \Pi_{AB}(T_1) + \Pi_{BA}(T_2) + \int_{T_1}^{T_2}\sigma_A(T)dT + \int_{T_2}^{T_1}\sigma_B(T)dT$$

**关键结论（考试高频）**：
1. 同种金属闭合回路，即使两端温度不同，总汤姆孙电动势为零（两棒电动势大小相等、方向相反）。
2. 不同金属在**同一温度**下构成闭合回路，总佩尔捷电动势为零。
3. 要产生温差电流，必须**同时**存在温度梯度和电子数密度梯度（即两种不同金属+两端温度不同）。
4. 在A、B之间插入第三种金属C，只要C与A、B的两个连接点**温度相同**，总温差电动势不变。如果连接点温度不同，此定理不成立。

**易错陷阱**：
- 温差电动势很小，一般只有 mV 量级。
- 温差电效应是**可逆**的（扣除焦耳热和热传导后）。焦耳热是**不可逆**的。考试如果问"哪些过程可逆"，不能把焦耳热算进去。
- 汤姆孙系数 $\sigma(T)$ 和电导率 $\sigma$ 符号相同但物理意义完全不同。这是典型的"符号滥用"陷阱。

---

## 模块六：麦克斯韦理论（§6）

### §1 位移电流

**已在Phase 3中按最大颗粒度讲透，跳过。** 你已掌握：
- 全电流 $\mathbf{j}_{total} = \mathbf{j}_0 + \partial\mathbf{D}/\partial t$
- 位移电流拆解：$\partial\mathbf{D}/\partial t = \varepsilon_0\partial\mathbf{E}/\partial t + \partial\mathbf{P}/\partial t$
- 极化电流 $\mathbf{j}_P = \partial\mathbf{P}/\partial t$ 是真实电流
- 真空位移电流 $\varepsilon_0\partial\mathbf{E}/\partial t$ 无电荷运动
- 全电流线永远闭合
- 全电流是激发 $\mathbf{H}$ 的唯一源

### §2 麦克斯韦方程组

**积分形式**：
$$\text{(I)} \quad \oiint \mathbf{D}\cdot d\mathbf{S} = q_0$$
$$\text{(II)} \quad \oint \mathbf{E}\cdot d\mathbf{l} = -\iint \frac{\partial\mathbf{B}}{\partial t}\cdot d\mathbf{S}$$
$$\text{(III)} \quad \oiint \mathbf{B}\cdot d\mathbf{S} = 0$$
$$\text{(IV)} \quad \oint \mathbf{H}\cdot d\mathbf{l} = I_0 + \iint \frac{\partial\mathbf{D}}{\partial t}\cdot d\mathbf{S}$$

**微分形式**：
$$\text{(I)} \quad \nabla\cdot\mathbf{D} = \rho_{e0}$$
$$\text{(II)} \quad \nabla\times\mathbf{E} = -\frac{\partial\mathbf{B}}{\partial t}$$
$$\text{(III)} \quad \nabla\cdot\mathbf{B} = 0$$
$$\text{(IV)} \quad \nabla\times\mathbf{H} = \mathbf{j}_0 + \frac{\partial\mathbf{D}}{\partial t}$$

**介质方程（补充三个本构关系）**：
$$\text{(V)} \quad \mathbf{D} = \varepsilon\varepsilon_0\mathbf{E}$$
$$\text{(VI)} \quad \mathbf{B} = \mu\mu_0\mathbf{H}$$
$$\text{(VII)} \quad \mathbf{j}_0 = \sigma\mathbf{E}$$

**最基本形式（微观/真空）**：
$$\nabla\cdot\mathbf{E} = \rho_e/\varepsilon_0$$
$$\nabla\times\mathbf{E} = -\partial\mathbf{B}/\partial t$$
$$\nabla\cdot\mathbf{B} = 0$$
$$\nabla\times\mathbf{B} = \varepsilon_0\mu_0\frac{\partial\mathbf{E}}{\partial t} + \mu_0\mathbf{j}$$

**从微观到宏观的过渡**：
$$\rho_e = \rho_{e0} + \rho_e'$$
$$\mathbf{j} = \mathbf{j}_0 + \mathbf{j}' = \mathbf{j}_0 + \mathbf{j}_P + \mathbf{j}_M$$
其中 $\mathbf{j}_P = \partial\mathbf{P}/\partial t$（极化电流），$\mathbf{j}_M = \nabla\times\mathbf{M}$（磁化电流）。

引入辅助矢量 $\mathbf{D}=\varepsilon_0\mathbf{E}+\mathbf{P}$ 和 $\mathbf{H}=\mathbf{B}/\mu_0-\mathbf{M}$，消去 $\rho_e'$ 和 $\mathbf{j}'$，得到宏观形式。

**易错陷阱**：
- 宏观麦克斯韦方程组（I）–（IV）+ 介质方程（V）–（VII）才是完备的。只写四个方程不写介质方程，方程组不完备。
- 微观形式（6.12）中只包含 $\mathbf{E}$ 和 $\mathbf{B}$ 两个基本场矢量，$\rho_e$ 和 $\mathbf{j}$ 包含所有电荷和电流。
- 宏观形式中 $\rho_{e0}$ 只是自由电荷，$\mathbf{j}_0$ 只是传导电流。极化电荷和磁化电流被"吸收"进了 $\mathbf{D}$ 和 $\mathbf{H}$。

### §3 边界条件（完整体系）

这是考试压轴题的高频考点。我按三组介质界面分别列出。

#### （1）磁介质界面

**法向**（由 $\nabla\cdot\mathbf{B}=0$）：
$$B_{2n} = B_{1n} \quad \text{(磁感应强度法向连续)}$$

**切向**（由 $\oint\mathbf{H}\cdot d\mathbf{l}=I_0$，界面无传导电流时）：
$$H_{2t} = H_{1t} \quad \text{(磁场强度切向连续)}$$

#### （2）电介质界面

**法向**（由 $\oiint\mathbf{D}\cdot d\mathbf{S}=q_0$，界面无自由电荷时）：
$$D_{2n} = D_{1n} \quad \text{(电位移法向连续)}$$

**切向**（由 $\oint\mathbf{E}\cdot d\mathbf{l}=0$）：
$$E_{2t} = E_{1t} \quad \text{(电场强度切向连续)}$$

#### （3）导体界面

**法向**（由 $\oiint\mathbf{D}\cdot d\mathbf{S}=q_0$，界面有自由电荷）：
$$D_{2n} - D_{1n} = \sigma_{e0} \quad \text{(电位移法向跃变=自由面电荷密度)}$$

**电流法向**（由电流连续方程）：
$$\text{非恒定：} (j_{02})_n - (j_{01})_n = -\frac{\partial\sigma_{e0}}{\partial t}$$
$$\text{恒定：} (j_{02})_n = (j_{01})_n \quad \text{(传导电流法向连续)}$$

**高频趋肤效应下的理想导体**：
$$\mathbf{n}\times\mathbf{H}_{\text{外}} = \mathbf{i}_0 \quad \text{(面电流密度)}$$

**易错陷阱**：
- 电介质界面 $D_n$ 连续的前提是**无自由面电荷**。如果有自由面电荷，$D_{2n}-D_{1n}=\sigma_{e0}$。
- 导体界面 $D_n$ 不连续（因为有自由面电荷），但 $E_t$ 仍然连续（$\oint\mathbf{E}\cdot d\mathbf{l}=0$ 对导体也适用）。
- 恒定条件下 $j_n$ 连续，但 $D_n$ 不一定连续。这两者不矛盾：$j_n$ 连续来自 $\nabla\cdot\mathbf{j}_0=0$，$D_n$ 跃变来自 $\nabla\cdot\mathbf{D}=\rho_{e0}$。
- 高频趋肤效应下，理想导体内部 $H_t=0$，边界条件变为 $\mathbf{n}\times\mathbf{H}_{\text{外}}=\mathbf{i}_0$，取代了 $H_t$ 连续。

---

# 2
## 0. 章节定位与核心主线

本章研究对象为**真空中的稳恒磁场**，即稳恒传导电流在真空中激发的恒定磁场 $\mathbf{B}$。

全章逻辑主线：

1. 从电流间相互作用出发，定义描述磁场的基本物理量 $\mathbf{B}$；
2. 给出电流产生磁场的局域叠加规律（毕奥-萨伐尔定律）；
3. 利用该定律计算典型电流系统的磁场分布；
4. 建立磁场自身满足的场方程（安培环路定理、磁场高斯定理）；
5. 研究磁场对电流与运动电荷的力学效应。

支配本章的核心场方程为：

$$
\nabla \cdot \mathbf{B} = 0, \quad \nabla \times \mathbf{B} = \mu_0 \mathbf{j}
$$

其中真空磁导率：

$$
\mu_0 = 4\pi \times 10^{-7}\ \mathrm{N/A^2}
$$

---

## 1. 磁感应强度矢量 $\mathbf{B}$ 的定义

### 1.1 从安培定律引入 $\mathbf{B}$

与静电场中库仑定律的地位相当，磁场的基本实验规律是安培定律。真空中两个电流元之间的相互作用力为：

$$
\mathrm{d}\boldsymbol{F}_{12} = \frac{\mu_0}{4\pi}\frac{I_2\,\mathrm{d}\boldsymbol{l}_2 \times (I_1\,\mathrm{d}\boldsymbol{l}_1 \times \hat{\boldsymbol{r}}_{12})}{r_{12}^2}
$$

仿照电场中将库仑定律拆分为"场源产生场"与"场对试探电荷施力"两步，将安培定律拆分：

$$
\mathrm{d}\boldsymbol{F}_2 = I_2\,\mathrm{d}\boldsymbol{l}_2 \times \boldsymbol{B}
$$

$$
\boldsymbol{B} = \frac{\mu_0}{4\pi}\oint_{(L_1)}\frac{I_1\,\mathrm{d}\boldsymbol{l}_1 \times \hat{\boldsymbol{r}}_{12}}{r_{12}^2}
$$

前式为 $\mathbf{B}$ 的定义式（安培力公式），后式为闭合回路 $L_1$ 产生磁场的计算公式。

### 1.2 $\mathbf{B}$ 的大小

将试探电流元 $I_2\,\mathrm{d}\boldsymbol{l}_2$ 放入磁场中，其受力大小为：

$$
\mathrm{d}F_2 = I_2\,\mathrm{d}l_2\,B\sin\theta
$$

其中 $\theta$ 为 $\mathbf{B}$ 与电流元的夹角。

- 当 $\theta = 0$ 或 $\pi$ 时，$\mathrm{d}F_2 = 0$，电流元不受力；
- 当 $\theta = \pi/2$ 时，$\mathrm{d}F_2$ 取最大值。

定义该点磁感应强度的大小为：

$$
B = \frac{(\mathrm{d}F_2)_{\max}}{I_2\,\mathrm{d}l_2}
$$

### 1.3 $\mathbf{B}$ 的方向

$\mathbf{B}$ 的方向沿试探电流元不受力时的取向。该取向给出 $\mathbf{B}$ 所在的直线，但存在两个彼此相反的指向。正反指向由矢积公式 $\mathrm{d}\boldsymbol{F} = I\,\mathrm{d}\boldsymbol{l}\times\boldsymbol{B}$ 按右手定则唯一确定。

具体操作：取 $\mathrm{d}F$ 取最大值时的一组 $\mathrm{d}\boldsymbol{l}$ 与 $\mathrm{d}\boldsymbol{F}$ 方向，由叉乘关系反解 $\mathbf{B}$ 的指向：

$$
\boldsymbol{B} = \frac{\mathrm{d}\boldsymbol{F}\times\mathrm{d}\boldsymbol{l}}{I\,\mathrm{d}l^2}
$$

### 1.4 单位

$$
1\ \mathrm{T} = 1\ \mathrm{N/(A\cdot m)}
$$

特斯拉（T）为 MKSA 制单位。另一常用单位为高斯（Gs）：

$$
1\ \mathrm{T} = 10^4\ \mathrm{Gs}, \quad 1\ \mathrm{Gs} = 10^{-4}\ \mathrm{T}
$$

---

## 2. 毕奥-萨伐尔定律

### 2.1 定律表述

任意闭合载流回路 $L$ 在空间某点产生的磁感应强度为：

$$
\boldsymbol{B} = \frac{\mu_0}{4\pi}\oint_{(L)}\frac{I\,\mathrm{d}\boldsymbol{l}\times\hat{\boldsymbol{r}}}{r^2}
$$

其中电流元 $I\,\mathrm{d}\boldsymbol{l}$ 产生的元磁场为：

$$
\mathrm{d}\boldsymbol{B} = \frac{\mu_0}{4\pi}\frac{I\,\mathrm{d}\boldsymbol{l}\times\hat{\boldsymbol{r}}}{r^2}
$$

物理内涵：

- $\mathrm{d}\boldsymbol{B}$ 垂直于 $\mathrm{d}\boldsymbol{l}$ 与 $\hat{\boldsymbol{r}}$ 确定的平面；
- 大小为 $\mathrm{d}B = \frac{\mu_0}{4\pi}\frac{I\,\mathrm{d}l\sin\theta}{r^2}$，其中 $\theta$ 为 $\mathrm{d}\boldsymbol{l}$ 与 $\hat{\boldsymbol{r}}$ 的夹角；
- 总磁场为所有电流元贡献的矢量叠加。

### 2.2 稳恒电流的闭合性

稳恒条件要求：

$$
\frac{\partial\rho}{\partial t} = 0 \implies \nabla\cdot\boldsymbol{j} = 0
$$

物理后果：

- 电流线不能中断，稳恒电流必须构成闭合回路；
- 不存在孤立的稳恒有限长电流元；
- 电流元 $I\,\mathrm{d}\boldsymbol{l}$ 仅为积分微元，不是独立物理源；
- 有限长直导线的磁场公式只能理解为闭合回路中一段的贡献，或回流路径足够远时的局部近似。

### 2.3 磁感应线

磁感应线（$\mathbf{B}$ 线）是描述磁场分布的有向曲线，其上每点的切线方向与该点 $\mathbf{B}$ 的方向一致。

基本性质：

- 磁感应线无头无尾，闭合或延伸至无穷远；
- 对载流直导线，磁感应线为围绕导线的同心圆；
- 对载流圆线圈，磁感应线为套在圆环上的闭合曲线；
- 对螺线管，内部磁感应线近似平行于轴线，外部在无限长极限下消失。

右手定则（圆线圈）：弯曲四指代表电流方向，伸直拇指沿轴线上 $\mathbf{B}$ 的方向。

---

## 3. 载流直导线的磁场

### 3.1 有限长直导线

设场点 $P$ 到直导线的垂直距离为 $r_0$，导线两端 $A_1,A_2$ 对应的角度为 $\theta_1,\theta_2$。由毕奥-萨伐尔定律积分：

$$
B = \frac{\mu_0}{4\pi}\int_{\theta_1}^{\theta_2}\frac{I\sin\theta\,\mathrm{d}\theta}{r_0}
$$

得：

$$
B = \frac{\mu_0 I}{4\pi r_0}(\cos\theta_1 - \cos\theta_2)
$$

方向：在 $P$ 点，所有电流元产生的 $\mathrm{d}\boldsymbol{B}$ 方向一致（垂直于 $P$ 点与导线构成的平面），故只需求代数和。

### 3.2 无限长直导线

当导线为无限长时，$\theta_1 = 0$，$\theta_2 = \pi$：

$$
\cos\theta_1 - \cos\theta_2 = 1 - (-1) = 2
$$

得到：

$$
B = \frac{\mu_0 I}{2\pi r_0}
$$

即 $B \propto 1/r_0$。

### 3.3 对称性来源与有限长偏离

无限长直导线的 $1/r$ 标度源于两个对称性：

- 绕导线的旋转对称性；
- 沿导线方向的平移对称性。

二者共同强制 $\mathbf{B} = B(r)\,\hat{\boldsymbol{\varphi}}$，再由安培环路定理锁定 $B = \mu_0 I/(2\pi r)$。

有限长直导线破坏了沿轴方向的全局平移对称性，引入新的长度尺度 $l$（导线长度）。端角 $\theta_1,\theta_2$ 随 $r_0/l$ 变化，$1/r$ 标度不再成立。仅在 $r_0 \ll l$ 且场点靠近导线中部时，近似回到 $1/r$。

### 3.4 毕奥-萨伐尔实验验证

毕奥和萨伐尔最初用磁棒平衡装置精确验证了直导线周围 $B \propto 1/r_0$ 的规律。该实验是毕奥-萨伐尔定律的实验基础之一。

---

## 4. 载流圆线圈轴线上的磁场

### 4.1 对称性与轴线场推导

设圆线圈半径为 $R$，电流为 $I$，场点 $P$ 在轴线上距圆心 $r_0$。

关键对称性论证：

- 圆线圈具有绕轴旋转对称性；
- 轴线上的场点位于旋转轴上，是旋转操作的不动点；
- 对于通过场点的任一直径，两端电流元 $A$ 与 $A'$ 产生的 $\mathrm{d}\boldsymbol{B}$ 与 $\mathrm{d}\boldsymbol{B}'$ 对称；
- 垂直于轴线的分量成对抵消，仅剩轴向分量。

因此只需计算轴向分量：

$$
B = \oint \mathrm{d}B\cos\alpha
$$

其中 $\alpha = \angle PAO$。由毕奥-萨伐尔定律：

$$
\mathrm{d}B = \frac{\mu_0}{4\pi}\frac{I\,\mathrm{d}l}{r_0^2}\sin^2\alpha
$$

代入 $\cos\alpha = R/\sqrt{R^2+r_0^2}$，$\sin\alpha = r_0/\sqrt{R^2+r_0^2}$，$\oint\mathrm{d}l = 2\pi R$，得：

$$
B = \frac{\mu_0 R^2 I}{2(R^2+r_0^2)^{3/2}}
$$

### 4.2 特殊情形

**圆心处**（$r_0 = 0$）：

$$
B = \frac{\mu_0 I}{2R}
$$

**远场**（$r_0 \gg R$）：

$$
B \approx \frac{\mu_0 R^2 I}{2r_0^3}
$$

远场按 $1/r_0^3$ 衰减，退化为磁偶极子场。定义磁矩 $m = I\pi R^2$，则：

$$
B \approx \frac{\mu_0}{2\pi}\frac{m}{r_0^3}
$$

### 4.3 离轴磁场的定性讨论

轴线以外磁场的精确计算较为复杂（涉及椭圆积分），但可给出定性结构：

- 保留的对称性：绕轴旋转对称，场量不依赖方位角 $\varphi$；
- 失去的约束：轴线点的"不动点"性质。离轴点绕轴旋转后被带到另一点，不再要求横向分量为零；
- 一般结构：$\mathbf{B} = B_\rho(\rho,z)\,\hat{\mathbf{e}}_\rho + B_z(\rho,z)\,\hat{\mathbf{e}}_z$，且 $B_\varphi = 0$。

离轴处 $B_\rho \neq 0$，不能将磁场化为单一轴向分量。

### 4.4 亥姆霍兹线圈

两个完全相同的共轴圆线圈，半径均为 $R$，电流同向，间距为 $a$。

总磁场（取中点为原点，轴线为 $x$ 轴）：

$$
B(x) = \frac{\mu_0 R^2 I}{2}\left\{\frac{1}{[R^2+(x+a/2)^2]^{3/2}} + \frac{1}{[R^2+(x-a/2)^2]^{3/2}}\right\}
$$

由于 $B(x) = B(-x)$（偶函数），在 $x=0$ 处 $\mathrm{d}B/\mathrm{d}x = 0$ 自动满足。

为使中点附近磁场最均匀，需令：

$$
\left.\frac{\mathrm{d}^2B}{\mathrm{d}x^2}\right|_{x=0} = 0
$$

解得：

$$
a = R
$$

即两线圈间距等于半径时，中点附近磁场均匀性最优。此时泰勒展开中 $x^2$ 项消失，$B(x) = B(0) + O(x^4)$，在较大范围内近似均匀。

该装置称为亥姆霍兹线圈，用于产生中等强度的均匀磁场。

---

## 5. 载有环向电流的圆筒与螺线管

### 5.1 螺线管的圆筒模型

密绕螺线管可等效为载有环向电流的导体圆筒：

- 导线很细且一匝挨一匝密绕；
- 忽略匝与匝间电流和磁场的波纹起伏；
- 忽略边绕边进时电流的纵向分量；
- 单位长度内的电流记为 $\iota$。

若螺线管单位长度匝数为 $n$，每匝电流为 $I$，则：

$$
\iota = nI
$$

### 5.2 轴线磁场的计算

设圆筒半径为 $R$，总长度为 $L$，取轴线为 $x$ 轴，中点为原点。长度 $\mathrm{d}l$ 内的电流 $\iota\,\mathrm{d}l$ 在场点 $P$（坐标 $x$）产生的元磁场利用圆线圈轴线公式：

$$
\mathrm{d}B = \frac{\mu_0 R^2 \iota}{2}\frac{\mathrm{d}l}{[R^2+(x-l)^2]^{3/2}}
$$

总磁场：

$$
B = \frac{\mu_0 R^2 \iota}{2}\int_{-L/2}^{L/2}\frac{\mathrm{d}l}{[R^2+(x-l)^2]^{3/2}}
$$

令 $r = \sqrt{R^2+(x-l)^2} = R/\sin\beta$，$x-l = r\cos\beta$，换元积分得：

$$
B = \frac{\mu_0\iota}{2}(\cos\beta_1 - \cos\beta_2)
$$

其中 $\beta_1,\beta_2$ 分别是场点看向圆筒两端所对应的角度：

$$
\cos\beta_1 = \frac{x+L/2}{\sqrt{R^2+(x+L/2)^2}}, \quad \cos\beta_2 = \frac{x-L/2}{\sqrt{R^2+(x-L/2)^2}}
$$

当 $L \gg R$ 时，中部大范围内磁场近于均匀，仅在端点附近显著下降。

### 5.3 无限长螺线管

$L \to \infty$ 时，$\beta_1 = 0$，$\beta_2 = \pi$：

$$
B = \mu_0\iota = \mu_0 nI
$$

该结论不仅适用于轴线上，在整个圆筒内部空间磁场均均匀，方向平行于轴线。

外部磁场：在 $L \to \infty$ 极限下，整个外部空间的磁感应强度为零。但必须明确：

- 仅凭"外部无电流"不能推出外场为零；
- 必须补充无穷远边界条件 $\mathbf{B} \to 0$（$r \to \infty$），或由有限长螺线管取物理极限；
- 无电流区域允许存在无源均匀背景场 $\mathbf{B} = B_0\hat{\mathbf{z}}$，需边界条件排除。

### 5.4 半无限长螺线管端部

在半无限长圆筒的一端：

$$
\beta_1 = 0,\ \beta_2 = \pi/2 \quad \text{或} \quad \beta_1 = \pi/2,\ \beta_2 = \pi
$$

无论哪种情形：

$$
B = \frac{\mu_0\iota}{2} = \frac{\mu_0 nI}{2}
$$

叠加解释：将一个无限长圆筒从任意截面截成两半，由对称性，每半对截面处总磁场 $\mu_0\iota$ 的贡献相等，各为 $\mu_0\iota/2$。半无限长圆筒端部场正是其中一半的贡献。

### 5.5 有限长螺线管近似

对于有限长螺线管，只要 $L \gg R$：

- 中部：$B \approx \mu_0 nI$；
- 端部：$B \approx \mu_0 nI/2$；
- 外部：磁场较弱，随 $L/R$ 增大而趋近于零。

### 5.6 多层螺线管

对于多层密绕螺线管（内半径 $R_1$，外半径 $R_2$，半长度 $l$，电流密度 $j$），中心处磁场为：

$$
B_0 = \mu_0 j l \ln\frac{R_2 + \sqrt{R_2^2+l^2}}{R_1 + \sqrt{R_1^2+l^2}}
$$

其中 $j = NI/[2l(R_2-R_1)]$ 为等效电流密度。该式由薄层叠加积分得到。

---

## 6. 安培环路定理与磁场高斯定理

### 6.1 安培环路定理

微分形式：

$$
\nabla \times \mathbf{B} = \mu_0 \mathbf{j}
$$

积分形式：

$$
\oint_L \mathbf{B}\cdot\mathrm{d}\mathbf{l} = \mu_0 I_{\text{enc}}
$$

其中 $I_{\text{enc}}$ 为穿过以 $L$ 为边界的任意曲面的净传导电流。

核心要点：

- 该定理对任意闭合回路 $L$ 恒成立，与电流分布是否对称无关；
- 环流是全局约束，不能直接给出局域场值；
- 要从环流推出 $B$ 的局部值，必须依靠对称性保证 $\mathbf{B}$ 在环路上切向且大小恒定。

### 6.2 磁场高斯定理

微分形式：

$$
\nabla \cdot \mathbf{B} = 0
$$

积分形式：

$$
\oiint_S \mathbf{B}\cdot\mathrm{d}\mathbf{S} = 0
$$

物理内涵：

- 磁场是无源场，不存在磁单极子；
- 磁感应线无起点无终点，闭合或延伸至无穷远；
- 穿过任意闭合曲面的净磁通量恒为零。

### 6.3 对称性方法论

利用安培环路定理求解 $\mathbf{B}$ 的充分条件：

| 对称性类型 | 效果 | 典型系统 |
|:---|:---|:---|
| 平移对称 | 场量不依赖某坐标 | 无限长直导线、无限长螺线管 |
| 旋转对称 | 场量不依赖方位角 | 柱对称系统 |
| 反射对称 | 排除特定分量 | 圆线圈轴线、螺线管 |

反射对称性对轴矢量 $\mathbf{B}$ 的作用：

- $\mathbf{B}$ 是轴矢量（赝矢量），在镜像反射下变换行为与极矢量不同；
- 包含电流轴的平面反射可排除垂直于反射面的磁场分量；
- 轴线上的点在旋转操作下不动，横向矢量若存在会破坏旋转不变性，故必须为零。

### 6.4 边界条件与唯一性

场方程 $\nabla\times\mathbf{B} = \mu_0\mathbf{j}$ 只约束旋度。在无源区（$\mathbf{j}=0$）：

$$
\nabla\times\mathbf{B} = 0, \quad \nabla\cdot\mathbf{B} = 0
$$

该齐次方程组允许非零解，如均匀背景场 $\mathbf{B} = B_0\hat{\mathbf{z}}$。因此：

- "无电流"不能推出"无磁场"；
- "净电流为零"不能推出"外场处处为零"；
- 必须补充边界条件（如 $\mathbf{B}\to 0$ at infinity）才能排除齐次解，锁定唯一物理场。

面电流处的边界关系（真空）：

$$
\hat{\mathbf{n}}\cdot(\mathbf{B}_2 - \mathbf{B}_1) = 0
$$

$$
\hat{\mathbf{n}}\times(\mathbf{B}_2 - \mathbf{B}_1) = \mu_0\mathbf{K}
$$

其中 $\mathbf{K}$ 为面电流密度，$\hat{\mathbf{n}}$ 为从区域 1 指向区域 2 的单位法向。

---

## 7. 磁场对电流与运动电荷的作用

### 7.1 安培力

电流元在磁场中受力：

$$
\mathrm{d}\boldsymbol{F} = I\,\mathrm{d}\boldsymbol{l}\times\boldsymbol{B}
$$

对整段导线积分得总力。

### 7.2 闭合线圈在均匀场中的受力与力矩

**合力**：若 $\mathbf{B}$ 均匀，

$$
\mathbf{F} = I\left(\oint\mathrm{d}\mathbf{l}\right)\times\mathbf{B} = 0
$$

因为闭合回路 $\oint\mathrm{d}\mathbf{l} = 0$。此结论精确成立，不依赖线圈形状，无需偶极近似。

**力矩**：合力为零但力矩可不为零。定义磁矩 $\mathbf{m} = I\mathbf{S}$（$\mathbf{S}$ 为线圈面积矢量），则：

$$
\boldsymbol{\tau} = \mathbf{m}\times\mathbf{B}
$$

当 $\mathbf{m}\nparallel\mathbf{B}$ 时力矩非零。物理图像：各电流元所受安培力方向不同，合力为零但作用线不共线，构成力偶。

### 7.3 平行直导线间的相互作用

两根无限长平行直导线，电流 $I_1,I_2$，间距 $r$。导线 1 在导线 2 处产生：

$$
B_1 = \frac{\mu_0 I_1}{2\pi r}
$$

导线 2 单位长度受力：

$$
\frac{F}{l} = I_2 B_1 = \frac{\mu_0 I_1 I_2}{2\pi r}
$$

同向电流相吸，反向电流相斥。

### 7.4 洛伦兹力与动生电动势

运动电荷在磁场中受力：

$$
\mathbf{F} = q\mathbf{v}\times\mathbf{B}
$$

由于 $\mathbf{F}\perp\mathbf{v}$，磁场力对电荷不做功。

动生电动势的非静电力为洛伦兹力。设导体以速度 $\mathbf{v}$ 运动，电子另有相对导体的漂移速度 $\mathbf{u}$，则电子总速度为 $\mathbf{u}+\mathbf{v}$，总洛伦兹力：

$$
\mathbf{F}_{\text{总}} = -e(\mathbf{u}+\mathbf{v})\times\mathbf{B}
$$

拆为两项：

$$
\mathbf{F}_v = -e(\mathbf{v}\times\mathbf{B}), \quad \mathbf{F}_u = -e(\mathbf{u}\times\mathbf{B})
$$

- $\mathbf{F}_v$ 沿导体方向推动电荷，形成动生电动势，对漂移运动做正功；
- $\mathbf{F}_u$ 方向与 $\mathbf{v}$ 相反，阻碍导体运动，做负功；
- 两项功率代数和为零，总洛伦兹力不做功；
- 外力克服 $\mathbf{F}_u$ 做正功输入机械能，通过 $\mathbf{F}_v$ 转化为电能。洛伦兹力是能量传递媒介，不是能量源。

动生电动势公式：

$$
\mathcal{E} = \oint_L(\mathbf{v}\times\mathbf{B})\cdot\mathrm{d}\mathbf{l}
$$

---

## 8. 高频逻辑陷阱与防线清单

### 陷阱一：安培环路定理误用

$\oint\mathbf{B}\cdot\mathrm{d}\mathbf{l} = \mu_0 I$ 对任意回路恒成立，但不能直接给出 $B$ 的局域值。只有在对称性保证 $\mathbf{B}$ 沿环路切向且大小恒定时，才能提取 $B$。

### 陷阱二：孤立有限长电流源

稳恒电流必须闭合。有限长直导线公式仅为闭合回路中一段的贡献或局部近似，不能作为独立物理源。

### 陷阱三：轴线对称性误推广至离轴

圆线圈轴线上横向分量为零，源于场点位于旋转轴不动点集。离轴点无此约束，$B_\rho \neq 0$，不可将轴线结论推广。

### 陷阱四：无电流等同于无磁场

$\nabla\times\mathbf{B} = 0$ 允许无源均匀背景场。必须补边界条件或反射对称性才能断言场为零。

### 陷阱五：净电流为零等同于外场处处为零

净电流为零仅能推出某些环流分量为零（如 $B_\varphi = 0$），不能排除轴向均匀背景场。

### 陷阱六：偶极近似替代基础证明

均匀场中闭合线圈合力为零应直接用 $\oint\mathrm{d}\mathbf{l} = 0$ 证明。使用 $\mathbf{F} = \nabla(\mathbf{m}\cdot\mathbf{B})$ 是偶极近似，逻辑倒置。

### 陷阱七：洛伦兹力不做功的误读

总功为零不代表不能传递能量。分力一正一负，洛伦兹力充当机械能向电能转化的媒介。

---

## 9. 核心公式速查表

| 物理量/规律 | 公式 |
|:---|:---|
| $\mathbf{B}$ 大小定义 | $B = (\mathrm{d}F)_{\max}/(I\,\mathrm{d}l)$ |
| 安培力元 | $\mathrm{d}\mathbf{F} = I\,\mathrm{d}\mathbf{l}\times\mathbf{B}$ |
| 毕奥-萨伐尔定律 | $\mathrm{d}\mathbf{B} = \frac{\mu_0}{4\pi}\frac{I\,\mathrm{d}\mathbf{l}\times\hat{\mathbf{r}}}{r^2}$ |
| 有限长直导线 | $B = \frac{\mu_0 I}{4\pi r_0}(\cos\theta_1-\cos\theta_2)$ |
| 无限长直导线 | $B = \frac{\mu_0 I}{2\pi r_0}$ |
| 圆线圈轴线 | $B = \frac{\mu_0 R^2 I}{2(R^2+r_0^2)^{3/2}}$ |
| 圆线圈圆心 | $B = \frac{\mu_0 I}{2R}$ |
| 圆线圈远场 | $B \approx \frac{\mu_0 R^2 I}{2r_0^3}$ |
| 亥姆霍兹线圈间距 | $a = R$ |
| 螺线管轴线 | $B = \frac{\mu_0 nI}{2}(\cos\beta_1-\cos\beta_2)$ |
| 无限长螺线管内部 | $B = \mu_0 nI$ |
| 半无限长端部 | $B = \mu_0 nI/2$ |
| 磁场高斯定理 | $\oiint\mathbf{B}\cdot\mathrm{d}\mathbf{S} = 0$ |
| 安培环路定理 | $\oint\mathbf{B}\cdot\mathrm{d}\mathbf{l} = \mu_0 I_{\text{enc}}$ |
| 面电流边界 | $\hat{\mathbf{n}}\times(\mathbf{B}_2-\mathbf{B}_1) = \mu_0\mathbf{K}$ |
| 均匀场中闭合线圈合力 | $\mathbf{F} = 0$ |
| 线圈力矩 | $\boldsymbol{\tau} = \mathbf{m}\times\mathbf{B}$ |
| 磁矩 | $\mathbf{m} = I\mathbf{S}$ |
| 平行导线单位长度力 | $F/l = \frac{\mu_0 I_1 I_2}{2\pi r}$ |
| 动生电动势 | $\mathcal{E} = \oint(\mathbf{v}\times\mathbf{B})\cdot\mathrm{d}\mathbf{l}$ |

# 3

## §1 电磁感应定律的物理图景与数学表述

### 1.1 法拉第定律的普适形式
法拉第电磁感应定律揭示了时变磁场与电场的内在联系。其积分形式表述为：闭合回路 $L$ 中的感应电动势 $\mathcal{E}$ 等于穿过该回路所围曲面 $S$ 的磁通量 $\Phi$ 随时间变化率的负值。
$$ \mathcal{E} = -\frac{d\Phi}{dt} = -\frac{d}{dt} \iint_{S} \mathbf{B} \cdot d\mathbf{S} $$
微分形式（麦克斯韦-法拉第方程）则剥离了具体回路的几何依赖，揭示了空间各点场的局部属性：
$$ \nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t} $$
这表明，任何随时间变化的磁场必然在空间中激发有旋电场。

### 1.2 磁通量变化的全导数拆解
当回路 $L(t)$ 在空间中发生形变或运动时，磁通量的全导数必须使用流形上的莱布尼茨积分法则进行拆解：
$$ \frac{d\Phi}{dt} = \iint_{S} \frac{\partial \mathbf{B}}{\partial t} \cdot d\mathbf{S} + \oint_{L} (\mathbf{B} \times \mathbf{v}) \cdot d\mathbf{l} $$
- **第一项（感生项）**：源于磁场本身随时间的演化（$\partial_t \mathbf{B} \neq 0$），对应空间固定点处产生的涡旋电场。
- **第二项（动生项）**：源于回路边界 $L$ 以速度 $\mathbf{v}$ 扫掠空间非均匀磁场，对应洛伦兹力对回路中载流子的非静电力做功。
这两项在实验室系中是磁通变化的两个独立物理来源，但在不同惯性系中，它们可以通过洛伦兹变换相互转化。

### 1.3 楞次定律的力学与能量本质
楞次定律（感应电流的效果总是反抗引起感应电流的原因）并非独立的物理定律，而是**能量守恒定律在宏观电磁感应过程中的必然推论**。
若感应电流产生的磁场增强原磁通的变化，系统将自发获得无限的动能与电能，违反热力学第一定律。在力学层面，楞次定律表现为安培力对导体运动的阻碍作用（电磁阻尼），确保机械能向电能转化的单向性与守恒性。

### 1.4 电子感应加速器（Betatron）的轨道约束
在轴对称时变磁场 $B_z(r,t)$ 中，电子被约束在半径为 $R$ 的圆轨道上加速。系统需同时满足两个独立的动力学条件：
1. **径向约束（向心力）**：$p(t) = e R B(R,t)$
2. **切向加速（涡旋电场做功）**：$\frac{dp}{dt} = e E_\theta(R) = \frac{e R}{2} \frac{d\bar{B}(t)}{dt}$，其中 $\bar{B}$ 为轨道内的平均磁场。
两式联立求导，得到维持轨道半径恒定的**2:1法则**：
$$ \left. \frac{\partial B_z}{\partial t} \right|_{r=R} = \frac{1}{2} \frac{d\bar{B}}{dt} $$
该条件本质上反映了系统在轴对称性下的正则角动量守恒。

---

## §2 动生与感生电动势的微观与宏观机制

### 2.1 动生电动势与洛伦兹力的能量传递
在动生电动势中，非静电力是洛伦兹力的分量。设导体以宏观速度 $\mathbf{u}$ 运动，内部电子具有相对漂移速度 $\mathbf{v}_d$，电子总速度为 $\mathbf{V} = \mathbf{u} + \mathbf{v}_d$。
洛伦兹力 $\mathbf{F}_m = -e(\mathbf{V} \times \mathbf{B})$ 的总功率严格为零：
$$ P = \mathbf{F}_m \cdot \mathbf{V} = -e(\mathbf{V} \times \mathbf{B}) \cdot \mathbf{V} \equiv 0 $$
**物理图像**：洛伦兹力不做功，仅充当能量传递的媒介。
- 沿 $\mathbf{v}_d$ 方向的分力 $-e(\mathbf{u} \times \mathbf{B})$ 做正功，驱动电子形成电流（机械能转化为电能）。
- 沿 $\mathbf{u}$ 方向的分力 $-e(\mathbf{v}_d \times \mathbf{B})$ 做负功，宏观表现为安培力阻碍导体运动（消耗外部机械能）。
两者代数和为零，完美闭合能量守恒账目。

### 2.2 感生电动势与涡旋电场的拓扑性质
感生电动势由涡旋电场 $\mathbf{E}_{旋}$ 驱动。其核心拓扑性质为**无源有旋**：
$$ \nabla \cdot \mathbf{E}_{旋} = 0, \quad \nabla \times \mathbf{E}_{旋} = -\frac{\partial \mathbf{B}}{\partial t} $$
由于旋度不为零，$\oint \mathbf{E}_{旋} \cdot d\mathbf{l} \neq 0$，这意味着在包含时变磁场的区域内，**绝对不能引入单值的标量电势 $U$**。电场线在此区域内表现为闭合曲线，无头无尾。

### 2.3 导体内部的场分离与边界条件
在实际导体内部，总电场 $\mathbf{E}_{总} = \mathbf{E}_{旋} + \mathbf{E}_{静}$。
- **涡旋电场 $\mathbf{E}_{旋}$**：提供非静电力，其环路积分等于总电动势，负责能量的宏观注入。
- **静电场 $\mathbf{E}_{静}$**：由导体表面及内部电荷重排产生，满足 $\nabla \times \mathbf{E}_{静} = 0$。其环路积分为零，不贡献电动势，但在局部满足欧姆定律 $\mathbf{J} = \sigma \mathbf{E}_{总}$，负责将电流“导引”并约束在导线几何边界内。

### 2.4 涡电流与趋肤效应
大块导体处于时变磁场中时，内部激发的闭合感应电流称为涡电流。
- **电磁阻尼**：涡流在磁场中受安培力，其宏观力矩必然阻碍导体与磁场的相对运动。
- **趋肤效应**：高频交变磁场在导体内激发的涡流，其产生的反向磁场会削弱导体中心的净磁场与感应电场。这导致电流密度从表面向内部呈指数衰减，趋肤深度 $\delta = \sqrt{2 / (\omega \mu \sigma)}$。高频下电流被强制挤压在导体表面薄层。

---

## §3 磁矢势、正则动量与规范协变性

### 3.1 磁矢势的引入与规范自由度
由磁场的高斯定理 $\nabla \cdot \mathbf{B} = 0$，必然存在矢量场 $\mathbf{A}$ 使得 $\mathbf{B} = \nabla \times \mathbf{A}$，$\mathbf{A}$ 称为磁矢势。
$\mathbf{A}$ 具有**规范自由度**：对任意单值标量函数 $\chi(\mathbf{r}, t)$，作规范变换
$$ \mathbf{A}' = \mathbf{A} + \nabla \chi, \quad \phi' = \phi - \frac{\partial \chi}{\partial t} $$
变换后的势依然给出完全相同的物理场 $\mathbf{E}$ 和 $\mathbf{B}$。这表明 $\mathbf{A}$ 的局域值不具备直接的经典可观测量地位。

### 3.2 正则动量的动力学推导
带电粒子在电磁场中的拉格朗日量为 $L = \frac{1}{2}mv^2 - q\phi + q\mathbf{v}\cdot\mathbf{A}$。
由欧拉-拉格朗日方程 $\frac{d}{dt}\left(\frac{\partial L}{\partial \mathbf{v}}\right) - \frac{\partial L}{\partial \mathbf{r}} = 0$，定义**正则动量（共轭动量）**：
$$ \mathbf{p}_{can} = \frac{\partial L}{\partial \mathbf{v}} = m\mathbf{v} + q\mathbf{A} $$
其中 $m\mathbf{v}$ 为动力动量（机械动量），$q\mathbf{A}$ 为势动量。正则动量的时间演化满足：
$$ \frac{d\mathbf{p}_{can}}{dt} = -q\nabla(\phi - \mathbf{v}\cdot\mathbf{A}) $$
即正则动量的变化率等于广义势 $U_{eff} = q(\phi - \mathbf{v}\cdot\mathbf{A})$ 梯度的负值。

### 3.3 对称性与正则动量守恒
正则动量守恒的条件**不依赖于受力是否为纯电磁力**，而是严格依赖于**空间的几何对称性**。
若广义势 $U_{eff}$ 对某广义坐标 $q_i$ 的偏导数为零（即系统在该方向具有平移或旋转对称性），则对应的正则动量分量 $p_{can, i}$ 严格守恒。
**规范依赖性**：由于 $\mathbf{A}$ 在规范变换下会平移 $q\nabla\chi$，正则动量 $\mathbf{p}_{can}$ 的数值及其守恒陈述是**规范依赖**的。真正规范不变的物理内容是动力动量 $m\mathbf{v}$ 的运动轨迹，以及 $\mathbf{A}$ 的闭合环路积分（磁通量）。

### 3.4 牛顿第三定律的破产与电磁场动量
对于两个孤立的运动电荷（或非闭合电流元），其间的磁相互作用力一般不满足 $\mathbf{F}_{12} = -\mathbf{F}_{21}$，机械动量之和不守恒。
**物理本质**：孤立的非闭合电流元违反电荷守恒定律，物理上不存在。对于真实的运动电荷系统，缺失的机械动量被转移到了**电磁场**中。电磁场具有动量密度：
$$ \mathbf{g} = \epsilon_0 \mathbf{E} \times \mathbf{B} = \frac{\mathbf{S}}{c^2} $$
系统总动量（机械动量 + 场动量 + 势动量）在封闭系统内严格守恒。

### 3.5 阿哈罗诺夫-玻姆（AB）效应与拓扑相位
在 $\mathbf{B}=0$ 但 $\mathbf{A} \neq 0$ 的区域（如理想无限长螺线管外部），经典洛伦兹力为零，电子不受力。
但在量子力学中，电子波函数的相位受 $\mathbf{A}$ 调制。两束电子绕过螺线管后重新汇合，其相位差为：
$$ \Delta \varphi = \frac{q}{\hbar} \oint \mathbf{A} \cdot d\mathbf{l} = \frac{q\Phi}{\hbar} $$
AB效应证明了：磁矢势 $\mathbf{A}$ 并非纯粹的数学辅助量，其环路积分（拓扑性质）具有非局域的真实物理效应，且该相位差是严格规范不变的。

---

## §4 电磁场的相对论变换

### 4.1 电磁场张量与洛伦兹变换
电场 $\mathbf{E}$ 与磁场 $\mathbf{B}$ 并非独立的矢量，而是二阶反对称四维电磁场张量 $F^{\mu\nu}$ 的空间分量。
在惯性系 $S$ 到 $S'$（相对速度 $\mathbf{v}$）的洛伦兹变换下，电磁场按张量规则 $F'^{\mu\nu} = \Lambda^\mu_\alpha \Lambda^\nu_\beta F^{\alpha\beta}$ 变换。这从根本上统一了电与磁：磁场本质上是电场在相对论运动参考系中的表现。

### 4.2 电场与磁场的分量变换规则
将场分解为平行于相对运动速度 $\mathbf{v}$ 的分量（$\parallel$）和垂直分量（$\perp$）：
- **平行分量不变**：$E'_\parallel = E_\parallel$， $B'_\parallel = B_\parallel$
- **垂直分量混合**：
  $$ \mathbf{E}'_\perp = \gamma (\mathbf{E}_\perp + \mathbf{v} \times \mathbf{B}_\perp) $$
  $$ \mathbf{B}'_\perp = \gamma \left(\mathbf{B}_\perp - \frac{1}{c^2} \mathbf{v} \times \mathbf{E}_\perp \right) $$
这表明，在一个参考系中纯静电的场，在运动参考系中必然激发出磁场；反之亦然。

### 4.3 电磁场的洛伦兹不变量
无论参考系如何变换，电磁场张量构造的两个标量绝对不变：
1. $I_1 = \mathbf{B}^2 - \frac{1}{c^2}\mathbf{E}^2$
2. $I_2 = \mathbf{E} \cdot \mathbf{B}$
**物理推论**：
- 若某系中 $\mathbf{E} \perp \mathbf{B}$，则任何系中两者皆垂直。
- 若 $E > cB$，必存在一个参考系使 $\mathbf{B}'=0$（纯电场）。
- 若 $\mathbf{E} \cdot \mathbf{B} \neq 0$，则任何参考系中 $\mathbf{E}$ 和 $\mathbf{B}$ 均不为零，且绝不可能相互垂直。

### 4.4 运动电荷的电磁场与横向收缩
静止系中点电荷的电场各向同性（库仑场）。在实验室系中，由于垂直分量增强 $\gamma$ 倍，电场线在垂直于速度的方向上被“压缩”。
- **超相对论极限（$v \to c$）**：电场线极度集中在垂直于速度的平面内，形成横向的平面电磁脉冲（等效光子近似）。
- **磁场的起源**：实验室系中的磁场 $\mathbf{B} = \frac{1}{c^2} \mathbf{v} \times \mathbf{E}$ 纯粹是静止系电场经相对论变换的产物。磁场是真实的物理实体，携带动量与能量。

### 4.5 四维电流密度与源的对账
电磁场的变换必须与源的变换严格对账。电荷密度 $\rho$ 与电流密度 $\mathbf{J}$ 构成四维矢量 $J^\mu = (c\rho, \mathbf{J})$。
$$ \rho' = \gamma \left(\rho - \frac{v}{c^2} J_z \right) $$
**物理图像**：电中性（$\rho=0$）仅仅是特定参考系下的巧合。例如，载流导线在实验室系中电中性，但在运动电子的静止系中，由于正离子与电子的洛伦兹收缩比例不同，导线将表现出净电荷密度，从而产生纯粹的静电力。这正是“磁场力在运动系中表现为静电力”的微观机制。

### 4.6 特鲁顿-诺伯（Trouton-Noble）佯谬的协变破局
**佯谬**：静止系中带电电容器无力矩；Boost 后，由于极板间分离矢量（纵向收缩）与静电力（横向收缩）的缩放比例不一致，导致电磁力不共线，产生表观电磁转矩 $\tau_{em} \neq 0$。
**破局**：电容器并非自由极板，其机械支撑结构在静止系中存在应力。在相对论中，应力是能量-动量张量的空间分量。Boost 后，应力伴随宏观能流，产生**机械隐动量** $\mathbf{g}_{mech} = \mathbf{S}_{mech}/c^2$。
隐动量的角动量时间导数严格等于 $-\tau_{em}$。总力矩（电磁 + 机械）在任何惯性系下恒为零。协变表述：力矩是二阶反对称张量的分量，静止系为零，则全空间为零。

---

## §5 互感、自感与磁场能量

### 5.1 自感与互感的磁链定义
自感 $L$ 与互感 $M$ 是描述回路系统磁惯性的几何参数。
- **自感**：$L = \frac{\Psi_{self}}{I}$，表征回路自身电流激发磁场并链合自身的效率。
- **互感**：$M_{21} = \frac{\Psi_{21}}{I_1}$，表征回路 1 的电流激发磁场并链合回路 2 的效率。
它们仅取决于回路的几何形状、相对位置及周围介质的磁导率，与电流大小无关。

### 5.2 纽曼公式与互易性定理
对于真空中两个细导线回路 $L_1$ 和 $L_2$，互感可由纽曼公式（Neumann formula）严格计算：
$$ M_{12} = \frac{\mu_0}{4\pi} \oint_{L_1} \oint_{L_2} \frac{d\mathbf{l}_1 \cdot d\mathbf{l}_2}{|\mathbf{r}_1 - \mathbf{r}_2|} $$
**物理意义**：从积分核的对称性 $|\mathbf{r}_1 - \mathbf{r}_2| = |\mathbf{r}_2 - \mathbf{r}_1|$ 直接得出 $M_{12} = M_{21}$。这证明了互易性定理：回路 1 对回路 2 的互感，严格等于回路 2 对回路 1 的互感。互感是系统纯粹的拓扑与几何属性。

### 5.3 磁场能量与能量密度
建立电流系统需要克服感应电动势做功，这部分能量储存在磁场中。对于线性介质，磁场总能量为：
$$ W_m = \frac{1}{2} \iiint_V \mathbf{J} \cdot \mathbf{A} \, dV = \iiint_V \frac{B^2}{2\mu_0} \, dV $$
磁场能量密度 $w_m = \frac{B^2}{2\mu_0}$ 表明，磁场能量**定域于场分布的空间**中，而非仅仅依附于电流导线上。此公式严格依赖于介质的线性（$\mathbf{B} \propto \mathbf{H}$），对非线性铁磁质（存在磁滞损耗）失效。

### 5.4 耦合系统的磁能与交叉项
两个磁耦合线圈的总磁能包含自感能与互感能：
$$ W_m = \frac{1}{2} L_1 I_1^2 + \frac{1}{2} L_2 I_2^2 \pm M I_1 I_2 $$
**交叉项符号的物理判定**：
符号取决于两电流产生的磁场在空间中的**相对取向**。
- 若两磁场在耦合区相长（互磁通与自磁通同向），总场强增加，系统储能增加，互能项取 $+M I_1 I_2$。
- 若两磁场相消，总场强减弱，系统储能减少，互能项取 $-M I_1 I_2$。

### 5.5 串联合成电感与正定性底线
两线圈串联时，电流 $I$ 相同。总磁链为两自感磁链与两互感磁链的代数和。
- **顺接（磁场相长）**：$L_{eq} = L_1 + L_2 + 2M$
- **逆接（磁场相消）**：$L_{eq} = L_1 + L_2 - 2M$
**正定性底线（物理审查）**：
磁场能量本质是 $\int \frac{B^2}{2\mu_0} dV$，必然满足 $W_m \ge 0$。
这意味着对于任意给定的 $(I_1, I_2)$，磁能的二次型矩阵必须半正定。由此导出互感的绝对上限：
$$ M^2 \le L_1 L_2 \quad \text{或} \quad k = \frac{M}{\sqrt{L_1 L_2}} \le 1 $$
任何计算出 $M > \sqrt{L_1 L_2}$ 或等效电感 $L_{eq} < 0$ 的模型，均意味着假设了“漏磁为零（全耦合）”，这在物理上是不可能的，属于模型自相矛盾，无需检查后续计算。