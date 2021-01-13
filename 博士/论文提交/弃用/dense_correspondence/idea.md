### 可行性

传统跟踪算法未用相邻帧的对应关系, 而这是视频的基本属性. 如果能够得到相邻帧的每个空间位置的对应关系, 则可以辅助跟踪结果.

### 关键点

应该与现有的跟踪算法较好的整合.

以无监督形式(或者仅用跟踪框)进行训练.

是否显式表示测试时的对应关系 ? 或者仅是隐式学习 ?

如何保证密集对应算法, 如 cycle-time 是对的, 能够区分近似表观 ?

现有的跟踪器, 常常对于所跟踪的物体根本没有检测出来, 这时该怎么办 ? 或者密集对应是否能够缓解这一问题 ?

- 为什么没有检测出所需跟踪的物体 ? 因为学习的 embedding 不能适应物体表观的变化.
- 如果密集对应可以很好地工作, 则在目标处具有较高的响应, 这就弥补了现有算法的缺点.

- 理想情况下, 仅靠 cycle-time 就能执行目标跟踪. 把 cycle-time 算法简单应用到现有跟踪器中, 则无法判断何时采用  cycle-time 的结果, 何时使用跟踪器的结果. 因此不是说 cycle-time 算法没有用, 而是需要和现有跟踪算法整合到一起端到端训练, 自适应地决定最好的结果.

仅依赖表观就可以跟踪, 所以网络可能会选择忽略密集对应这一线索. 但是从另一个角度讲, 也许仅用密集对应就能预测, 说不定还会忽略target线索. 不过, 不管利用什么线索, 只要最终的跟踪结果是好的, 不就可以吗?

是不是**必须**要得到warped warped map? 目前来说是的.

将已经训好的密集对应的权重**直接**拿来用，是我们的算法的上界。因为根本无法保证我们能够训到更好的密集对应关系。

### 注意

密集对应任务在根据上一帧标签确定下一帧标签时, 不仅知道了两帧之间的密集对应关系, 还知道的上一帧中的标签的位置.

### 相似算法

**Know Your Surroundings: Exploiting Scene Information for Object Tracking**

- 将状态向量和基于表观的单通道相应图串接起来, 经过两个卷积层, 得到最终结果.
- 状态向量的作用 ?
- 这篇论文, 你真的看懂了吗 ?

**DMV Visual Object Tracking via Part-level Dense Memory and Voting-based Retrieval**

- 在每个空间位置都检索最好的向量.
- 这篇论文, 你真的看懂了 ?

**Learning Correspondence from the Cycle-consistency of Time**

- 这篇文章, 你真的看懂了吗 ?
- 关键是弄清, 怎么利用边框gt, 就学到了密集对应.
- 在学习过程中, 密集对应关系是未知的,  是在训练过程中逐渐学到的.

### 方案

输入为两帧图像a, b, 计算得到亲和矩阵, 利用亲矩阵得到仿射变换参数.

输入为以a中目标为中心的高斯a', 对其进行仿射变换. 得到新的高斯b'.

将新的高斯与b串接, 送入卷积层增强位置信息的重要性, 再与目标特征互相关得到最终结果.

**Q&A**

Q: 仅仅得到了一个高斯, 是不是太简单了?

A: 原来的算法中, 高斯窗是以上一个位置为中心的, 且需要调参来拟合测试集. 本文通过端到端训练.

A: 引文2中, 也仅仅是把 score map 和 8 通道的矩阵串接在了一起.

A: 引文3中, 也仅仅是把特征和score map串接在了一起.

Q: 如果背景没发生变化, 而是物体位置变了, 怎么办?

A: 还有表观信息可以利用. 而且对于局部搜索机制, 物体是会占主体的.

Q: 这和qw的空间attention有什么区别?

Q: 怎么期待有了高斯之后(如果不互相关的话)就能预测特定的目标了?

A: 这得参考文献3了.

A: 并不是将高斯直接相乘, 进行了隐式的编码.

### 参考文献

1. [CVPR2019] Learning Correspondence from the Cycle-consistency of Time
2. [arXiv2003] Know Your Surroundings: Exploiting Scene Information for Object Tracking
3. [arXiv2003] DMV Visual Object Tracking via Part-level Dense Memory and Voting-based Retrieval
4. [ECCV2018] Tracking Emerges by Colorizing Videos