from setuptools import find_packages, setup

setup(
    name="nonebot_plugin_impact",
    version="0.09.114514",
    author="Special-Week",
    author_email="HuaMing27499@gmail.com",
    description="让群友们眼前一黑的nonebot2淫趴插件",
    python_requires=">=3.8.0",
    packages=find_packages(),
    url="https://github.com/Special-Week/nonebot_plugin_impact",
    package_data={"nonebot_plugin_impact": ["fonts/*"]},
    # 设置依赖包
    install_requires=[
        "pillow",
        "nonebot2",
        "nonebot-adapter-onebot",
        "sqlalchemy",
        "nonebot-plugin-apscheduler",
    ],
)
