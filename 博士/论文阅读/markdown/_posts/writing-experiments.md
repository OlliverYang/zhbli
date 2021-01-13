---
title: '[writing] experiments'
date: 2020-09-11 09:53:02
tags:
- writing
---

## OTB

- Table 2 gives the results of the attribute-based evaluation on OTB-2015. Our TLDCF tracker achieves the best performance on 8 out of 11 attributes and the second best on the remaining attributes.
- For further analyses on the tracking performance, we also demonstrate the advantages of our algorithm through the attribute-based comparison on sequences of the OTB-2013 dataset. The complete comparisons with 11 different attributes are illustrated in Figure 5 and Figure 6. Our CMKCF tracker achieves the best performance on all 11 attributes on Precision metric, and 10 attributes on Success metric, respectively.
- We also perform an attribute based analysis on our tracker. In OTB, each sequence is annotated with 11 different attributes, namely: fast motion, background clutter, motion blur, deformation, illumination variation, in-plane rotation, low resolution, occlusion, out-of-plane rotation, out-of-view and scale variation. It is interesting to find that K(MF) 2 JMT ranks the first on 7 out of 11 attributes **(see Fig. 2)**, especially on illumination variation, occlusion, out-of-plane rotation and scale variation. **This verifies the superiority of** K(MF) 2 JMT on target appearance representation and its capability on discovering reliable coherence from short-term memory.
- As shown in Figure 6, CTFT shows good performance on most of these attributes **which demonstrates its robustness in challenging tracking scenarios**.