import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="minecraft_launch_p",
  version="0.0.1",
  author="JustRainy",
  author_email="18331719639@qq.com",
  description="A Minecraft Launcher Core",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/Blessing-Studio/minecraft-launch-p",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)