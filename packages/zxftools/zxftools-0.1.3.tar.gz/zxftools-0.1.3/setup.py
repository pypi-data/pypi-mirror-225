from distutils.core import setup

setup(name='zxftools',  # 包名
      version="0.1.3",  # 版本号
      author='zhaoxuefeng',  # 作者
      packages=['zxftools'],  # 包列表
      py_modules=[],
      description='工具包',
      )

# 建立build
# python3 setup_pls.py build
# 生成压缩包
# python3 setup_pls.py sdist
# 安装包
# tar -zxvf  DataDeal.tar
#
# python3 setup_pls.py install

