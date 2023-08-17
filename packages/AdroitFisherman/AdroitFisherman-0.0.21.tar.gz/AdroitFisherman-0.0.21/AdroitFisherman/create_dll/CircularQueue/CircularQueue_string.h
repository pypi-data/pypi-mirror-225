#ifndef CIRCULARQUEUE_STRING
#define CIRCULARQUEUE_STRING
#include "DataStorage.h"
#include "framework.h"
#include <iostream>
extern "C" __declspec(dllimport) void set_capacity(int size);
extern "C" __declspec(dllimport) bool init_queue();
extern "C" __declspec(dllimport) void destroy_queue();
extern "C" __declspec(dllimport) void clear_queue();
extern "C" __declspec(dllimport) bool queue_empty();
extern "C" __declspec(dllimport) int queue_length();
extern "C" __declspec(dllimport) char * get_head();
extern "C" __declspec(dllimport) bool en_queue(char * elem);
extern "C" __declspec(dllimport) char * de_queue();
extern "C" __declspec(dllimport) void queue_traverse();
#endif // !CIRCULARQUEUE_STRING