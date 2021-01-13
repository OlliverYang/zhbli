---
title: '[coding] video_analyst'
date: 2020-09-09 15:57:03
tags:
- coding
---

test.py

```python
if __name__ == '__main__':
    tester.test()  # 调用 OTBTester.test
```

tester_impl/otb.py

```python
class OTBTester:
    def test:
        experiment = ExperimentOTB(...)
```

experiments/otb.py

```python
class ExperimentOTB:
    def __init__:
        pass
    def run:  # 在 OTB 数据集上运行跟踪器
        for s, (img_files, anno) in enumerate(self.dataste):
            record_file = os.path.join(self.result_dir, tracker.name, '%s.txt'%seq_name)
        	boxes, times = tracker.track(...)  # 调用 PipelineTraker.track
            self._record(record_file, boxes, times)
    def report(tracker_names):
        report_dir = os.path.join(self.report_dir, tracker_names[0])
        
```

got_benchmark_helper.py

```python
class PipelineTraker:
    def track(img_files, box):
        boxes = np.zeros((frame_num, 4))
        boxes[0] = box  # 用于保存跟踪结果。box调用1/2
        for f, img_file in enumerate(img_files):
            image = cv2.imread(img_file, cv2.IMREAD_COLOR)
            if f == 0:
                self.init(image, box)  # 调用 SiamFCppTracker.init. box调用2/2. box: xywh
            else:
                boxes[f, :] = self.update(image)
```

siamfcpp_track.py

```python
class SiamFCppTracker:
    def init:
        ...
```



