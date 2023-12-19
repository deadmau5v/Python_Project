# 安装依赖
```shell
conda create -n pp python=3.11

conda install cudatoolkit=11.7

conda install cudnn

# GPU
python3 -m pip install paddlepaddle-gpu -i https://mirror.baidu.com/pypi/simple
# CPU 
python3 -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple

pip install PyMuPDF

pip install "paddleocr>=2.0.1"
```
> 对于Windows环境用户：直接通过pip安装的shapely库可能出现[winRrror 126] 找不到指定模块的问题。建议从[这里](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely)下载shapely安装包完成安装。

# Todo