import ctypes


class SingleLinkedList_double():
    def __init__(self):
        self.__list = ctypes.cdll.LoadLibrary("./Libraries/SingleLinkedList_double.dll")

    def init_list(self):
        init_list = self.__list.init_list
        init_list.restype = ctypes.c_bool
        return init_list()

    def destroy_list(self):
        destroy_list = self.__list.destroy_list
        destroy_list()

    def clear_list(self):
        clear_list = self.__list.clear_list
        clear_list()

    def list_empty(self):
        list_empty = self.__list.list_empty
        list_empty.restype = ctypes.c_bool
        return list_empty()

    def list_length(self):
        list_length = self.__list.list_length
        list_length.restype = ctypes.c_int
        return list_length()

    def get_elem(self, index):
        get_elem = self.__list.get_elem
        get_elem.argtypes = [ctypes.c_int]
        get_elem.restype = ctypes.c_double
        return get_elem(index)

    def locate_elem(self, elem):
        locate_elem = self.__list.locate_elem
        locate_elem.restype = ctypes.c_int
        locate_elem.argtypes = [ctypes.c_double]
        return locate_elem(elem)

    def prior_elem(self, elem):
        prior_elem = self.__list.prior_elem
        prior_elem.restype = ctypes.c_double
        prior_elem.argtypes = [ctypes.c_double]
        return prior_elem(elem)

    def next_elem(self, elem):
        next_elem = self.__list.next_elem
        next_elem.restype = ctypes.c_double
        next_elem.argtypes = [ctypes.c_double]
        return next_elem(elem)

    def add_first(self, elem):
        add_first = self.__list.add_first
        add_first.restype = ctypes.c_bool
        add_first.argtypes = [ctypes.c_double]
        return add_first(elem)

    def add_after(self, elem):
        add_after = self.__list.add_after
        add_after.restype = ctypes.c_bool
        add_after.argtypes = [ctypes.c_double]
        return add_after(elem)

    def list_insert(self, index, elem):
        list_insert = self.__list.list_insert
        list_insert.argtypes = [ctypes.c_int, ctypes.c_double]
        list_insert.restype = ctypes.c_bool
        return list_insert(index, elem)

    def list_delete(self, index):
        list_delete = self.__list.list_delete
        list_delete.argtypes = [ctypes.c_int]
        list_delete.restype = ctypes.c_bool
        return list_delete(index)

    def traverse_list(self):
        self.__list.traverse_list()
