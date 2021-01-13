---
title: '[coding] OTB使用说明'
date: 2020-09-09 09:17:06
tags:
- coding
---

## 概念介绍 

OPE/TRE/SRE：

- OPE 是一次成功率。（One Pass Evaluation）
- TRE（20次）和 SRE（12次）都是多次的。

## 目录树

```bash
anno
	视频标注信息。默认为 OTB2013 的视频序列。测试 OTB2015 是，需要进行替换。
figs
initOmit
perfMat
results
	results_OPE
	results_SRE
	results_TRE
	results_SRE_CVPR2013
		*.mat
	results_TRE_CVPR_2013
rstEval
trackers
util
	configTrackers.m 设置测试哪些跟踪器。
	configSeqs.m 设置在哪些视频上测试。
drawResultBB.m
genPerfMat.m
main_running.m 运行跟踪器，将跟踪结果保存在 results 文件夹中。
perfPlot.m
trackers.txt
```

## 运行方式

1. 清空 perfMat。
2. 确认 anno 文件夹中的标注信息对应的数据集是否正确。
3. 将跟踪结果保存在 results 文件夹。
4. 修改 perPlot.m，指定 OPE/TRE/SRE，指定生成成功率图还是精度图。
5. 运行 perfPlot.m 绘图。
6. 在 figs 中查看绘图结果。

## .mat 文件结构

![result](https://img-blog.csdn.net/20180420093636330?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RldmlsXzA4/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

上图中，由于 TRE 重复运行 20 次，所以是 1×20 的 cell，每个 cell 是 1×1 的 struct，表示一次运行的结果。

![result](https://img-blog.csdn.net/20180420093724253?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RldmlsXzA4/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

struct 中的 res 即为跟踪结果。725 是视频帧数，第一行就是初始帧的跟踪框。4列表示的是 (x, y ,w, h)，这里 x 和 y 表示的是目标位置的中心，w和h就是目标框的宽和高。anno 是人工标注的信息。

## 代码解读

### perfPlot.m

```matlab
evalTypeSet = {'SRE', 'TRE', 'OPE'};
rankingType = 'threshold';  % 可填 AUC 或 threshold。AUC 对应成功率（success）图，threshold 对应精度（precision）图。
```

