# 数据读取

regular_datapipeline.py

```python
class RegularDatapipeline(DatapipelineBase):
    def __getitem__(...):
        sampled_data = self.sampler[item]
        # 调用 TrackPairSampler.__getitem__
        for proc in self.pipeline:
            sample_data = proc(sampled_data)
            # 第一次：调用 RandomCropTransformer.__call__，得到裁剪后的图像像素，以及目标在裁剪后的图像中的边框。
            # 第二次：调用 DenseboxTarget.__call__
```

track_pair_sampler.py

```python
class TrackPairSampler:
    def __getitem__(...):
        data1, data2 = self._sample_track_pair()
        data1["image"] = load_image(data1["image"])
        data2["image"] = load_image(data2["image"])  # 读取像素值
        sampled_data = dict(
            data1=data1,  # 字典，'image'为像素值，'anno'为原始边框
            data2=data2,
            is_negative_pair=is_negative_pair,
        )
        return sampled_data
    def _sample_track_pair(...):
        sequence_data = self._sample_sequence_from_dataset(dataset)
        # 字典{'images':..., 'annos':...} 某段视频的所有帧的路径及原始边框
        data1, data2 = self._sample_track_pair_from_sequence(
                sequence_data, self._state["max_diffs"][dataset_idx])
        # 从整段视频中选择两幅图像，返回路径及原始边框
        return data1, data2
        
    def _sample_sequence_from_dataset(...):
        sequence_data = dataset[idx]
        # idx 表示got10k数据库中的第几段视频
        # 调用 GOT10kDataset.__getitem__
        return sequence_data  # 某段视频的所有帧的路径及原始边框
    
    def _sample_track_pair_from_sequence(...):
        data1 = {k: v[idx1] for k, v in sequence_data.items()}
		# 字典，包括一幅图片的路径及原始边框
        data2 = {k: v[idx2] for k, v in sequence_data.items()}
        return data1, data2
```

got10k.py

```python
class GOT10kDataset:
    def __getitem(...):
        img_files, anno = self._state["dataset"][item]
        # got10k数据库中第item段视频的所有帧的路径及对应边框。
        sequence_data = dict(image=img_files, anno=anno)
        # 将该段视频的图像路径名及边框表示成字典形式。
        return sequence_data
```

random_crop_transformer.py

```python
class RandomCropTransformer:
    def __call__(...):
        data1 = sampled_data["data1"]
        data2 = sampled_data["data2"]  # 字典，包括图像像素和原始边框
        im_temp, bbox_temp = data1["image"], data1["anno"]
        im_curr, bbox_curr = data2["image"], data2["anno"]
        # im_* 为图像像素，bbox_* 为目标在原始图像中的边框。
        im_z, bbox_z, im_x, bbox_x, _, _ = crop_track_pair(
            im_temp,
            bbox_temp,
            im_curr,
            bbox_curr,
            config=self._hyper_params,
            rng=self._state["rng"])
        # im_* 为裁剪后的图像像素，bbox_*为目标在裁剪后的图像中的边框。
        sampled_data["data1"] = dict(image=im_z, anno=bbox_z)
        sampled_data["data2"] = dict(image=im_x, anno=bbox_x)
		# dict, 'image': 裁剪后的图像像素，'anno'：目标在裁剪后的图像中的边框
        return sampled_data
```

crop_track_pair.py

```python
def crop_track_pair(...):
    context_amount = 0.5
    z_size = 127
    x_size = 289
    max_scale = 0.3
    max_shift = 0.4
    max_scale_temp = 0.0
    max_shift_temp = 0.0
    box_temp = xyxy2cxywh(bbox_temp)
    box_curr = xyxy2cxywh(bbox_curr)  # 转换边框格式，仍为原始边框
    
    wt, ht = box_temp[2:]  # 模板目标的原始宽高
    wt_ = wt + context_amount * (wt + ht)
    ht_ = ht + context_amount * (wt + ht)
    st_ = np.sqrt(wt_ * ht_)  # 模板目标+padding在原始图像中的尺寸（正方形边长）
    
    ...
    sc_ = np.sqrt(wc_ * hc_)  # 搜索目标+padding在原始图像中的尺寸（正方形边长）
    
    scale_temp_ = z_size / st_  # 若想让模板目标+padding的尺寸变为127，需对原始图像如何缩放
    scale_curr_ = z_size / sc_  # 若想让搜索目标+padding的尺寸变为127，需对原始图像如何缩放
    scale_rand = ...  # 搜索图像的尺度扰动
    scale_rand_temp = 1.0  # 模板图像不进行尺度扰动
    scale_curr = scale_curr_ / scale_rand  # 若想让搜索目标+padding的尺寸位于127附近，需对原始图像如何缩放
    scale_temp = scale_temp_ / scale_rand_temp
    s_curr = x_size / scale_curr  # bbox for cropping，相对于原始图像。
    s_temp = z_size / scale_temp  # bbox for cropping
    
    # calculate bbox for cropping，指在原始图像中，需要裁剪的边框。
    box_crop_temp = np.concatenate([
        box_temp[:2] - np.array([dx_temp, dy_temp]),
        np.array([s_temp, s_temp])
    ])  # box_temp 为原始边框。从目标中心进行裁剪。
    box_crop_curr = np.concatenate(
        [box_curr[:2] - np.array([dx, dy]),
         np.array([s_curr, s_curr])])
    
    # calculate new bbox 目标在裁剪出来的图像中的坐标
    box_z = np.array([(z_size - 1) / 2] * 2 + [0] * 2) + np.concatenate(
        [np.array([dx_temp, dy_temp]),
         np.array([wt, ht])]) * scale_temp
    box_x = np.array([(x_size - 1) / 2] * 2 + [0] * 2) + np.concatenate(
        [np.array([dx, dy]), np.array([wc, hc])]) * scale_curr
    bbox_z = cxywh2xyxy(box_z)
    bbox_x = cxywh2xyxy(box_x)
    
    im_z = get_subwindow_tracking(im_temp,
                                      box_crop_temp[:2],
                                      z_size,
                                      s_temp,
                                      avg_chans=avg_chans)
    im_x = get_subwindow_tracking(im_curr,
                                      box_crop_curr[:2],
                                      x_size,
                                      s_curr,
                                      avg_chans=avg_chans)

    return im_z, bbox_z, im_x, bbox_x, mask_z, mask_x
```





densebox_target.py

```python
class DenseboxTarget(TargetBase):
    def __call__(...):
        im_x, bbox_x = data_x["image"], data_x["anno"]
        # bbox_x: nd.array, shape=(4,), xyxy
        cls_label, ctr_label, box_label = make_densebox_target(
                    bbox_x.reshape(1, 4), self._hyper_params)
```

make_densebox_target.py

```python
def make_densebox_target(...):
    
```

