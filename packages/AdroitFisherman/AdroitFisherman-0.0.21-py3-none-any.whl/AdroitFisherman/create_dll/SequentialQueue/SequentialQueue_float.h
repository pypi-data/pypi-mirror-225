#ifndef SEQUENTIALQUEUE_FLOAT
#define SEQUENTIALQUEUE_FLOAT
#include <iostream>
#include "DataStorage.h"
#include "framework.h"
extern "C" __declspec(dllimport) void set_capacity(int length);
extern "C" __declspec(dllimport) bool init_queue();
extern "C" __declspec(dllimport) void destroy_queue();
extern "C" __declspec(dllimport) void clear_queue();
extern "C" __declspec(dllimport) bool queue_empty();
extern "C" __declspec(dllimport) int queue_length();
extern "C" __declspec(dllimport) float get_head();
extern "C" __declspec(dllimport) bool en_queue(float elem);
extern "C" __declspec(dllimport) float de_queue();
extern "C" __declspec(dllimport) void queue_traverse();
#endif // !SEQUENTIALQUEUE_FLOAT