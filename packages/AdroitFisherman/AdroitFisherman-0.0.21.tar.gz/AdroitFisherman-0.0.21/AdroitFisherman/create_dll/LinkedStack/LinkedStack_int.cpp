#include "DataStorage.h"
#include <iostream>
#include "LinkedStack_int.h"
DataStorage::LinkedStack<int> STACK = DataStorage::LinkedStack<int>();
bool init_stack()
{
	bool tag = STACK.InitStack();
	return tag;
}
void destroy_stack()
{
	STACK.DestroyStack();
}
void clear_stack()
{
	STACK.ClearStack();
}
bool stack_empty()
{
	bool tag = STACK.StackEmpty();
	return tag;
}
int stack_length()
{
	return STACK.StackLength();
}
int get_top()
{
	return STACK.GetTop();
}
bool push(int elem)
{
	bool tag = STACK.Push(elem);
	return tag;
}
int pop()
{
	return STACK.Pop();
}
void stack_traverse()
{
	STACK.StackTraverse();
}