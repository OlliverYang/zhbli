# 训练

```bash
python run_training transt transt
```

# 测试

utils/setup.py
```python
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

setup(
    ext_modules = cythonize([Extension("region", ["region.pyx", "src/region.c"])]),
)
```

```bash
从 https://pan.baidu.com/s/1js0Qhykqqur7_lNRtle1tA#list/path=%2F 下载 GOT-10k.json

cd utils
python setup.py build_ext --inplace

specify the path of the model and dataset in the test.py.
net_path = '/path_to_model' #Absolute path of the model
dataset_root= '/path_to_datasets' #Absolute path of the datasets

python -u pysot_toolkit/test.py --dataset GOT-10k --name 'transt'

python pysot_toolkit/eval.py --tracker_path results/ --dataset GOT-10k --num 1 --tracker_prefix 'transt'
```