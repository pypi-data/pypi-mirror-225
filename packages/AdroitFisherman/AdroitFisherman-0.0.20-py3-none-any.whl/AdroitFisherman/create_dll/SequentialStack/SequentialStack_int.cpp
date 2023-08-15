#include "DataStorage.h"
#include <iostream>
#include "SequentialStack_int.h"
DataStorage::SequentialStack<int>STACK = DataStorage::SequentialStack<int>();
bool init_stack(int length)
{
	bool tag = STACK.InitStack(length);
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