import ctypes


class LinkedStack_double:
    def __init__(self):
        self.__stack = ctypes.cdll.LoadLibrary('./Libraries/LinkedStack_double')

    def init_stack(self):
        init_stack = self.__stack.init_stack
        init_stack.restype = ctypes.c_bool
        return init_stack()

    def destroy_stack(self):
        destroy_stack = self.__stack.destroy_stack
        destroy_stack()

    def clear_stack(self):
        clear_stack = self.__stack.clear_stack
        clear_stack()

    def stack_empty(self):
        stack_empty = self.__stack.stack_empty
        stack_empty.restype = ctypes.c_bool
        return stack_empty()

    def stack_length(self):
        stack_length = self.__stack.stack_length
        stack_length.restype = ctypes.c_int
        return stack_length()

    def get_top(self):
        get_top = self.__stack.get_top
        get_top.restype = ctypes.c_double
        return get_top()

    def push(self, elem):
        push = self.__stack.push
        push.argtypes = [ctypes.c_double]
        push.restype = ctypes.c_bool
        return push(elem)

    def pop(self):
        pop = self.__stack.pop
        pop.restype = ctypes.c_double
        return pop()

    def stack_traverse(self):
        stack_traverse = self.__stack.stack_traverse
        stack_traverse()
