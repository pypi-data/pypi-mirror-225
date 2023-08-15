#include "DataStorage.h"
#include <iostream>
#include "SequentialStack_char.h"
DataStorage::SequentialStack<char>STACK = DataStorage::SequentialStack<char>();
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
	bool tag=STACK.StackEmpty();
	return tag;
}
int stack_length()
{
	return STACK.StackLength();
}
char get_top()
{
	return STACK.GetTop();
}
bool push(char elem)
{
	bool tag = STACK.Push(elem);
	return tag;
}
char pop()
{
	return STACK.Pop();
}
void stack_traverse()
{
	STACK.StackTraverse();
}