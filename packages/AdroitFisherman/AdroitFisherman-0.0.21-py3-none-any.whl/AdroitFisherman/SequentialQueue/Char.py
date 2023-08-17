import ctypes
class SequentialQueue_char:
    def __init__(self):
        self.__queue=ctypes.cdll.LoadLibrary('./Libraries/SequentialQueue_char')
    def set_capacity(self,length):
        set_capacity=self.__queue.set_capacity
        set_capacity.argtypes=[ctypes.c_int]
        set_capacity(length)
    def init_queue(self):
        init_queue=self.__queue.init_queue
        init_queue.restype=ctypes.c_bool
        return init_queue()
    def destroy_queue(self):
        destroy_queue=self.__queue.destroy_queue
        destroy_queue()
    def clear_queue(self):
        clear_queue=self.__queue.clear_queue
        clear_queue()
    def queue_empty(self):
        queue_empty=self.__queue.queue_empty
        queue_empty.restype=ctypes.c_bool
        return queue_empty()
    def queue_length(self):
        queue_length=self.__queue.queue_length
        queue_length.restype=ctypes.c_int
        return queue_length()
    def get_head(self):
        get_head=self.__queue.get_head
        get_head.restype=ctypes.c_char
        return ctypes.c_char(get_head()).value
    def en_queue(self,elem):
        en_queue=self.__queue.en_queue
        en_queue.argtypes=[ctypes.c_char]
        en_queue.restype=ctypes.c_bool
        return en_queue(ctypes.c_char(bytes(elem,encoding='utf-8')))
    def de_queue(self):
        de_queue=self.__queue.de_queue
        de_queue.restype=ctypes.c_char
        return ctypes.c_char(de_queue()).value
    def queue_traverse(self):
        queue_traverse=self.__queue.queue_traverse
        queue_traverse()
