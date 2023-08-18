import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="rest_fastapi",  # 模块名称
    version="0.1.2",  # 当前版本
    author="lxshen",  # 作者w
    author_email="lxshen613@163.com",  # 作者邮箱
    description="fastapi脚手架，封装了基本curd",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    url="https://gitee.com/ileona/falsework.git",  # 模块github地址
    # packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    packages=setuptools.find_namespace_packages(include=["rest_fastapi", "rest_fastapi.*"], ),
    include_package_data=True,

    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'fastapi==0.75.2',
        'pandas==1.3.0',
        'orjson==3.9.1',
        'redis==4.1.4',
        'sqlalchemy==1.4.49',
        'uvicorn==0.22.0',
        'setuptools==68.0.0',
        'pydantic==1.10.12',
        'starlette==0.17.1',
        'pymysql==0.9.3',
        'styleframe==4.1,',
    ],
    python_requires='>=3.8.15',
)
