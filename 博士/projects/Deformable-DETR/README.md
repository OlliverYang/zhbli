# 训练参数

GPUS_PER_NODE=7 ./tools/run_dist_launch.sh 7 ./configs/r50_deformable_detr_single_scale.sh --coco_path /data/COCO2017 --batch_size 4

我们的 batch size = 28，作者代码中提及的 batch size = 32

# 测试数据集 

可能是 coco-2017-val

# 测试精度

IoU metric: bbox                                                                
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.390 
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.597 
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.417 
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.204 
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.427
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.551
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.324
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.530
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.567
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.319
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.621
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.798

# 作者的代码中提及的精度

AP	    APS	    APM	    APL
39.4	20.6	43.0	55.5

# 训练时间

1 day, 6:36:26（训练过程中进行了多次val，不过每次val仅需要一分多钟） 

也就是说，7 卡 50 轮 耗时 30:36:26。

共训练 50 轮。

Epoch: [49] Total time: 0:35:19 (0.5018 s / it) 每轮半个多小时

# 收敛情况

Epoch: [49]  [4223/4224]  eta: 0:00:00  lr: 0.000020  class_error: 10.76  grad_norm: 64.63  loss: 7.5466 (7.4440)  loss_bbox: 0.2249 (0.2250)  loss_bbox_0: 0.2630 (0.2604)  loss_bbox_1: 0.2333 (0.2400)  loss_bbox_2: 0.2285 (0.2327)  loss_bbox_3: 0.2272 (0.2286)  loss_bbox_4: 0.2241 (0.2261)  loss_ce: 0.3865 (0.3952)  loss_ce_0: 0.4603 (0.4728)  loss_ce_1: 0.4278 (0.4295)  loss_ce_2: 0.4093 (0.4112)  loss_ce_3: 0.3989 (0.4010)  loss_ce_4: 0.3858 (0.3961)  loss_giou: 0.5654 (0.5697)  loss_giou_0: 0.6187 (0.6305)  loss_giou_1: 0.5890 (0.5945)  loss_giou_2: 0.5729 (0.5828)  loss_giou_3: 0.5650 (0.5762)  loss_giou_4: 0.5732 (0.5717)  cardinality_error_unscaled: 292.3214 (292.1922)  cardinality_error_0_unscaled: 292.2143 (292.5620)  cardinality_error_1_unscaled: 292.2143 (292.2490)  cardinality_error_2_unscaled: 292.2500 (292.2910)  cardinality_error_3_unscaled: 292.3929 (292.4365)  cardinality_error_4_unscaled: 292.3214 (292.4059)  class_error_unscaled: 9.4849 (8.2481)  loss_bbox_unscaled: 0.0450 (0.0450)  loss_bbox_0_unscaled: 0.0526 (0.0521)
loss_bbox_1_unscaled: 0.0467 (0.0480)  loss_bbox_2_unscaled: 0.0457 (0.0465)  loss_bbox_3_unscaled: 0.0454 (0.0457)  
loss_bbox_4_unscaled: 0.0448 (0.0452)  loss_ce_unscaled: 0.1933 (0.1976)  loss_ce_0_unscaled: 0.2301 (0.2364)  
loss_ce_1_unscaled: 0.2139 (0.2147)  loss_ce_2_unscaled: 0.2046 (0.2056)  loss_ce_3_unscaled: 0.1994 (0.2005)  
loss_ce_4_unscaled: 0.1929 (0.1980)  loss_giou_unscaled: 0.2827 (0.2849)  loss_giou_0_unscaled: 0.3094 (0.3152)  
loss_giou_1_unscaled: 0.2945 (0.2973)  loss_giou_2_unscaled: 0.2865 (0.2914)  loss_giou_3_unscaled: 0.2825 (0.2881)  
loss_giou_4_unscaled: 0.2866 (0.2858)  time: 0.5107  data: 0.0000  max mem: 5297                                                                 
                                                                  

# 结论

可复现