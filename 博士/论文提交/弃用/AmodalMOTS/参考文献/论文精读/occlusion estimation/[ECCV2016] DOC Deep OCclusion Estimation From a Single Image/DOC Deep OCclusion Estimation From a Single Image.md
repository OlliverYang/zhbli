# Abstract

ECCV 2016，引用 17。

In this paper, we propose a deep convolutional network architecture, called DOC, which detects object boundaries and **estimates the occlusion relationships** (i.e. **which side of the boundary is foreground  and which is background**).

Specifically, we first represent occlusion relations by a **binary edge indicator**, to indicate the object boundary, and an occlusion orientation variable whose direction specifies the occlusion relationships by a **left-hand rule ** (the left side of the arrows is foreground), see Fig. 1.

To train and test DOC,  we **construct a large-scale instance occlusion boundary dataset** using  PASCAL VOC images, which we call the PASCAL instance occlusion  dataset (PIOD). 能不能用虚拟数据构建类似的数据集？

# 1. Introduction

人类能够从单个图像中恢复物体的遮挡关系。长期以来，这已被认为是场景理解和感知的重要能力[15,4]。如图1左侧所示，我们可以使用遮挡关系来推断该人正握着狗，因为该人的手遮住了狗，而狗遮住了他的身体。电生理学[18]和功能磁共振成像[13]研究表明，遮挡关系最早在视觉区域 V2 出现。生物学研究[9]还表明，遮挡检测可能需要来自更高层皮质区域的反馈，这表明可能需要远程上下文和语义层知识。心理物理学研究表明，有很多线索可以遮挡，包括边缘凸度[23]，边缘连接，强度梯度和纹理[35]。

# 2. Related word

# 3. The DOC network

