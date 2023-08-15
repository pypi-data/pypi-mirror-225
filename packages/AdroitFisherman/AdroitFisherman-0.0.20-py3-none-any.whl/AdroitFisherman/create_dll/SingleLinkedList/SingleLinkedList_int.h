#ifndef SINGLELINKEDLIST_FLOAT
#define SINGLELINKEDLIST_FLOAT
#include "framework.h"
#include "DataStorage.h"
#include <iostream>
extern "C" __declspec(dllimport) bool init_list();
extern "C" __declspec(dllimport) void destroy_list();
extern "C" __declspec(dllimport) void clear_list();
extern "C" __declspec(dllimport) bool list_empty();
extern "C" __declspec(dllimport) int list_length();
extern "C" __declspec(dllimport) int get_elem(int index);
extern "C" __declspec(dllimport) int locate_elem(int elem);
extern "C" __declspec(dllimport) int prior_elem(int elem);
extern "C" __declspec(dllimport) int next_elem(int elem);
extern "C" __declspec(dllimport) bool add_first(int elem);
extern "C" __declspec(dllimport) bool add_after(int elem);
extern "C" __declspec(dllimport) bool list_insert(int index, int elem);
extern "C" __declspec(dllimport) bool list_delete(int index);
extern "C" __declspec(dllimport) void traverse_list();
#endif // !SINGLELINKEDLIST_FLOAT
