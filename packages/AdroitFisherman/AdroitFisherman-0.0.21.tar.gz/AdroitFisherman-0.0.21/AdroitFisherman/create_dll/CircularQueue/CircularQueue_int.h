#ifndef CIRCULARQUEUE_INT
#define CIRCULARQUEUE_INT
#include "DataStorage.h"
#include "framework.h"
#include <iostream>
extern "C" __declspec(dllimport) void set_capacity(int size);
extern "C" __declspec(dllimport) bool init_queue();
extern "C" __declspec(dllimport) void destroy_queue();
extern "C" __declspec(dllimport) void clear_queue();
extern "C" __declspec(dllimport) bool queue_empty();
extern "C" __declspec(dllimport) int queue_length();
extern "C" __declspec(dllimport) int get_head();
extern "C" __declspec(dllimport) bool en_queue(int elem);
extern "C" __declspec(dllimport) int de_queue();
extern "C" __declspec(dllimport) void queue_traverse();
#endif // !CIRCULARQUEUE_INT