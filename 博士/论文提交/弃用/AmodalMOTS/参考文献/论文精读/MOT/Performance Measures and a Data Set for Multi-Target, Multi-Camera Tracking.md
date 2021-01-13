# Performance Measures and a Data Set for Multi-Target, Multi-Camera Tracking

To compute the optimal truth-to-result match, we construct a **bipartite graph** $G = (V_{T}, V_{C}, E)$ as follows.

Vertex set $V_{T}$ has one **"regular" node** $\tau$ for each **true trajectory** and one "false positive" node $f_{\gamma}^{+}$ for each **computed trajectory** $\gamma$.

Vertex set $V_{C}$ has one **"regular" node** $\gamma$ for each computed trajectory and one "false nagative" node $f_{\tau}^{-}$, for each **true trajectory** $\tau$.

Two ragular nodes are connected with an edge $e \in E$ if their trajectories overlap in time.

Every regular **true node** $\tau$ is also connected to its corresponding $f_{\tau}^{-}$, and every regular computed node $\gamma$ is also connected to its corresponding $f_{\gamma}^{+}$.

The cost on an edge $(\tau, \gamma) \in E$ tallies the number of false negative and false positive frames that would be incurred if that match were chosen.

Specifically, let $\tau(t)$ be the sequence of detections for true trajectory $\tau$, one detection for each frame $t$ in the set $\mathcal{T}_{\tau}$ over which $\tau$ extends, and define $\gamma(t)$ for $t \in \mathcal{T}_{\gamma}$ similarly for computed trajectories.

The two simultaneous detections $\tau(t)$ and $\gamma(t)$ are a miss if they do not overlap in space, and we write
$$
m(\tau, \gamma, t, \mathit{\Delta}) = 1.
$$
Every $(\tau, \gamma)$ match is a True Positive ID $(IDTP)$. Every $(f_{\gamma}^{+}, \gamma)$ match is a False Positive ID $(IDFP)$. Every $(\tau, f_{\tau}^{-})$ match is a False Negative ID ($IDFN$). Every $(f_{\gamma}^{+}, f_{\tau}^{-})$ match is a  True Negative ID $(IDTN)$.

The sets
$$
MT = \{\tau|(\tau, \gamma) \in IDTP\} \text{ and } MC = \{\gamma|(\tau,\gamma) \in IDTP\}
$$

$$
IDFN = \sum_{\tau \in AT}\sum_{t \in \mathcal{T}_{\tau}}m(\tau, \gamma_{m}(\tau), t, 
\mathit{\Delta}),
$$
where $AT$ and $AC$ are all true and computed identities in $MT$ and $MC$.
$$
IDF_{1} = \frac{2IDTP}{2IDTP + IDFP + IDFN}
$$
放弃理解，直接看例子：https://zhuanlan.zhihu.com/p/35391826

![img](https://pic3.zhimg.com/80/v2-4a196b28e3752d9b40b6c05eaa76ef8e_1440w.jpg)

对于同一个例子，我们分别计算一下他们的IDF1值可以得到下图结果，这里就不展开计算。由于例子比较简单，所以一眼就可以看出来，Tracker只有2帧结果认为是同一个目标，而Tracker++有8帧结果认为是同一个目标的轨迹。可以得到他们的IDF1分别是0.2和0.8。这就是IDF1的作用，可以更好的表示出跟踪器判断轨迹是否是同一个目标的能力。

![img](https://pic1.zhimg.com/80/v2-482d3301dc78f538774b53b1bf64c3d0_1440w.jpg)