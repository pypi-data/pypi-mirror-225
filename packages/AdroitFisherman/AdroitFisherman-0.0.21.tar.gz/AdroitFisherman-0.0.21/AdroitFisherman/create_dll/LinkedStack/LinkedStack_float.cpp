#include "DataStorage.h"
#include <iostream>
#include "LinkedStack_float.h"
DataStorage::LinkedStack<float> STACK = DataStorage::LinkedStack<float>();
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
float get_top()
{
	return STACK.GetTop();
}
bool push(float elem)
{
	bool tag = STACK.Push(elem);
	return tag;
}
float pop()
{
	return STACK.Pop();
}
void stack_traverse()
{
	STACK.StackTraverse();
}