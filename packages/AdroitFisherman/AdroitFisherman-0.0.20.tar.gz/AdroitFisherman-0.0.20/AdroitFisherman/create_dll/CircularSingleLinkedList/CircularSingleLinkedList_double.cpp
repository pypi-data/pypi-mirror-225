#include "CircularSingleLinkedList_double.h"
#include <iostream>
#include "DataStorage.h"
DataStorage::CircularSingleLinkedList<double>LIST = DataStorage::CircularSingleLinkedList<double>();
bool init_list()
{
	bool tag = LIST.InitList();
	return tag;
}
void destroy_list()
{
	LIST.DestroyList();
}
void clear_list()
{
	LIST.ClearList();
}
bool list_empty()
{
	bool tag = LIST.ListEmpty();
	return tag;
}
int list_length()
{
	return LIST.ListLength();
}
double get_elem(int index)
{
	return LIST.GetElem(index);
}
int locate_elem(double elem)
{
	return LIST.LocateElem(elem);
}
double prior_elem(double elem)
{
	return LIST.PriorElem(elem);
}
double next_elem(double elem)
{
	return LIST.NextElem(elem);
}
bool add_first(double elem)
{
	bool tag = LIST.addFirst(elem);
	return tag;
}
bool add_after(double elem)
{
	bool tag = LIST.addAfter(elem);
	return tag;
}
bool list_insert(int index, double elem)
{
	bool tag = LIST.ListInsert(index, elem);
	return tag;
}
bool list_delete(int index)
{
	bool tag = LIST.ListDelete(index);
	return tag;
}
void traverse_list()
{
	LIST.TraverseList();
}