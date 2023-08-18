from setuptools import find_packages, setup

setup(
    name="nonebot_plugin_smart_reply",
    version="0.05.114514",
    author="Special-Week",
    author_email="HuaMing27499@gmail.com",
    description="nonebot2的融合了openai, newbing, 词库的智障回复插件",
    python_requires=">=3.9.0",
    packages=find_packages(),
    long_description="reply插件",
    url="https://github.com/Special-Week/nonebot_plugin_smart_reply",
    package_data={
        "nonebot_plugin_smart_reply": ["resource/json/*", "resource/audio/*"]
    },
    # 设置依赖包
    install_requires=[
        "EdgeGPT==0.10.16",
        "revChatGPT",
        "pillow",
        "nonebot2",
        "nonebot-adapter-onebot",
        "httpx"
    ],
)
