from . import SequentialList
from . import SingleLinkedList
from . import SingleLinkedListWithOutHeadNode
from . import CircularSingleLinkedList
from . import DoubleLinkedList
from . import DoubleLinkedListWithoutHeadNode
from . import CircularDoubleLinkedList
from . import SequentialStack
from . import LinkedStack
from . import SequentialQueue
import os
run_plat="dll"
if not "Libraries" in os.listdir():
    os.mkdir("Libraries")
env_path=os.path.abspath(__file__).rstrip("__init__.py")
real_path=os.path.abspath("")
with open(f"{env_path}descriptor.txt",'r') as fe:
    file_msg=fe.read()
fe.close()
data_structures=file_msg.split(",")
data_types=["int","char","float","double","string"]
os.chdir("./Libraries")
for index in range(0,len(data_structures)-1,1):
    for data_type in data_types:
        if not f"{data_structures[index]}_{data_type}.{run_plat}" in os.listdir():
            print(f"copy {env_path}includes\\{data_structures[index]}_{data_type}.{run_plat} {real_path}\\Libraries")
            os.system(f"copy {env_path}includes\\{data_structures[index]}_{data_type}.{run_plat} {real_path}\\Libraries")
os.chdir("../")