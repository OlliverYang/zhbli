$K$：视频最后一帧的编号。
$\phi(\cdot)$：用于计算亲和力（affinity）。
$\varphi(\cdot)$：用于计算 long-term affinity。
$\mathbb{O}^{k}$：第 $k$ 帧的候选目标集合。
$I_{k}$：第 $k$ 帧中的候选目标数。
$\mathbf{o}_{i_{k}}^{k}$：第 $k$ 帧的第 $i_{k}$ 个候选目标。
$\textbf{t}_{i_{0}:i_{K}}$：从第 $0$ 帧到第 $K$ 帧的一条假设的轨迹。
$c_{i_{0}:i_{K}}$：轨迹 $\textbf{t}_{i_{0}:i_{K}}$ 的亲和力。一个数。
$z_{i_{0}:i_{K}}$：轨迹 $\textbf{t}_{i_{0}:i_{K}}$ 是真或假。一个数。
$\mathcal{C}$：所有候选轨迹的亲和力向量。一个向量。
$\mathcal{Z}$：所有候选轨迹的真假。一个向量。

作者把MOT定义成了MDA（多维分配：Multi-dimensional assignment）问题。什么是多维分配呢？

与该文联系最紧密的、引用处最多的论文是《Rank-1 tensor approximation for high-order association in multi-target tracking》（IJCV2019）。所以为了更好地理解这一问题，有必要去看看这一篇论文。