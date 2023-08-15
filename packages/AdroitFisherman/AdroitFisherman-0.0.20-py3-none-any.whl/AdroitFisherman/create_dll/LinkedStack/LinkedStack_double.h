#ifndef LINKEDSTACK_DOUBLE
#define LINKEDSTACK_DOUBLE
#include "framework.h"
#include "DataStorage.h"
#include <iostream>
extern "C" __declspec(dllimport) bool init_stack();
extern "C" __declspec(dllimport) void destroy_stack();
extern "C" __declspec(dllimport) void clear_stack();
extern "C" __declspec(dllimport) bool stack_empty();
extern "C" __declspec(dllimport) int stack_length();
extern "C" __declspec(dllimport) double get_top();
extern "C" __declspec(dllimport) bool push(double elem);
extern "C" __declspec(dllimport) double pop();
extern "C" __declspec(dllimport) void stack_traverse();
#endif // !LINKEDSTACK_DOUBLE
