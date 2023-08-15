from setuptools import setup
import os

class build_extension:
    def __init__(self):
        os.chdir("./AdroitFisherman/includes")
        os.system("del *.dll")
        os.chdir("../../")
        os.chdir("./AdroitFisherman/create_dll")
        self.data_structures = os.listdir()
        os.chdir("../")
        with open("descriptor.txt", "w+") as fe:
            for data_s in self.data_structures:
                fe.write("%s," % data_s)
        fe.close()
        os.chdir("../")
        self.data_types = ["int", "char", "float", "double", "string"]

    def build(self):
        for data_structure in self.data_structures:
            for data_type in self.data_types:
                os.system(
                    f"g++ -shared -static -I ./AdroitFisherman/create_dll/ -fpic -o ./AdroitFisherman/includes/{data_structure}_{data_type}.dll ./AdroitFisherman/create_dll/{data_structure}/{data_structure}_{data_type}.cpp")


builder = build_extension()
builder.build()
read_me = open('README.md', 'r')
setup(
    name="AdroitFisherman",
    version="0.0.20",
    author="adroit_fisherman",
    author_email="1295284735@qq.com",
    platforms="Windows",
    description="This is a simple package about Data Structure packed by C/C++ language.",
    long_description_content_type="text/markdown",
    long_description=read_me.read(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities"
    ],
    include_package_data=True
)
read_me.close()
