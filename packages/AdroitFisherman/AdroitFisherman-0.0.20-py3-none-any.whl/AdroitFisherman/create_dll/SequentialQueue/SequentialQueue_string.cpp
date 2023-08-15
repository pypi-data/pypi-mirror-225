#include "SequentialQueue_string.h"
#include <iostream>
#include "DataStorage.h"
DataStorage::SequentialQueue<char *> QUEUE = DataStorage::SequentialQueue<char *>();
void set_capacity(int length)
{
	QUEUE.SetCapacity(length);
}
bool init_queue()
{
	bool tag = QUEUE.InitQueue();
	return tag;
}
void destroy_queue()
{
	QUEUE.DestroyQueue();
}
void clear_queue()
{
	QUEUE.ClearQueue();
}
bool queue_empty()
{
	bool tag = QUEUE.QueueEmpty();
	return tag;
}
int queue_length()
{
	return QUEUE.QueueLength();
}
char * get_head()
{
	return QUEUE.GetHead();
}
bool en_queue(char * elem)
{
	bool tag = QUEUE.EnQueue(elem);
	return tag;
}
char * de_queue()
{
	return QUEUE.DeQueue();
}
void queue_traverse()
{
	QUEUE.QueueTraverse();
}