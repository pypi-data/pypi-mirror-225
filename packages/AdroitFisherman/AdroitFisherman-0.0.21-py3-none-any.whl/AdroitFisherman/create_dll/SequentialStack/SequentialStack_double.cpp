#include "DataStorage.h"
#include <iostream>
#include "SequentialStack_double.h"
DataStorage::SequentialStack<double>STACK = DataStorage::SequentialStack<double>();
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
double get_top()
{
	return STACK.GetTop();
}
bool push(double elem)
{
	bool tag = STACK.Push(elem);
	return tag;
}
double pop()
{
	return STACK.Pop();
}
void stack_traverse()
{
	STACK.StackTraverse();
}