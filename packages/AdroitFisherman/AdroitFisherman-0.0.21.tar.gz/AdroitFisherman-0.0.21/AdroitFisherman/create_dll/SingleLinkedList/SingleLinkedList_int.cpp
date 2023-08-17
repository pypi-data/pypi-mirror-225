#include "SingleLinkedList_int.h"
#include <iostream>
#include "DataStorage.h"
DataStorage::SingleLinkedList <int>LIST = DataStorage::SingleLinkedList<int>();
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
int get_elem(int index)
{
	return LIST.GetElem(index);
}
int locate_elem(int elem)
{
	return LIST.LocateElem(elem);
}
int prior_elem(int elem)
{
	return LIST.PriorElem(elem);
}
int next_elem(int elem)
{
	return LIST.NextElem(elem);
}
bool add_first(int elem)
{
	bool tag = LIST.addFirst(elem);
	return tag;
}
bool add_after(int elem)
{
	bool tag = LIST.addAfter(elem);
	return tag;
}
bool list_insert(int index, int elem)
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