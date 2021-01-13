## 问题

有没有人在单目标领域这么做了。-> 没有。

- 1996 年的论文或许是做单目标跟踪的，但不确定。

为什么以前没人这么做过？-> 以前没法检测多个候选。

别人在 VOS 上做了，你再在单目标跟踪上做，还有意义吗？ -> 有，因为这是两个完全不同的领域。

这么做合不合理。

- 需要弄懂多假设。
- 靠实验说话。

鸡/毛毛虫/牛视频，能否正确跟踪？

对于消失后又重新出现的目标，怎么处理？

- MOT 中必然有消失后又重新出现的人。
- 问题的关键是，当目标重新出现后，你凭什么认为它是你需要跟踪的目标？

## 相关文献

VOS多假设 MHP-VOS: Multiple Hypotheses Propagation for Video Object Segmentation CVPR2019 https://github.com/shuangjiexu/MHP-VOS

- 没讲对于一个消失物体怎么找回的。

MOT多假设 Multiple hypothesis tracking revisited ICCV2015

最早文献 An efficient implementation of reid’s multiple hypothesis tracking algorithm and its evaluation for the purpose of visual tracking PAMI1996

## 合理性

现在的孪生网络可以检测多个候选了。

单目标跟踪的确有这种困难：有多个表观近似的目标，要跟哪一个？