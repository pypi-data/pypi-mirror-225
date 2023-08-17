#include "DoubleLinkedListWithoutHeadNode_float.h"
#include <iostream>
#include "DataStorage.h"
DataStorage::DoubleLinkedListWithoutHeadNode<float>LIST = DataStorage::DoubleLinkedListWithoutHeadNode<float>();
void init_list()
{
	LIST.InitList();
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
float get_elem(int index)
{
	return LIST.GetElem(index);
}
int locate_elem(float elem)
{
	return LIST.LocateElem(elem);
}
float prior_elem(float elem)
{
	return LIST.PriorElem(elem);
}
float next_elem(float elem)
{
	return LIST.NextElem(elem);
}
bool add_first(float elem)
{
	bool tag = LIST.addFirst(elem);
	return tag;
}
bool add_after(float elem)
{
	bool tag = LIST.addAfter(elem);
	return tag;
}
bool list_insert(int index, float elem)
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
void traverse_list_by_reverse_order()
{
    LIST.TraverseListByReverseOrder();
}