#ifndef SINGLELINKEDLISTWITHOUTHEADNODE_STRING
#define SINGLELINKEDLISTWITHOUTHEADNODE_STRING
#include "framework.h"
#include "DataStorage.h"
#include <iostream>
extern "C" __declspec(dllimport) void init_list();
extern "C" __declspec(dllimport) void destroy_list();
extern "C" __declspec(dllimport) void clear_list();
extern "C" __declspec(dllimport) bool list_empty();
extern "C" __declspec(dllimport) int list_length();
extern "C" __declspec(dllimport) char * get_elem(int index);
extern "C" __declspec(dllimport) int locate_elem(char * elem);
extern "C" __declspec(dllimport) char * prior_elem(char * elem);
extern "C" __declspec(dllimport) char * next_elem(char * elem);
extern "C" __declspec(dllimport) bool add_first(char * elem);
extern "C" __declspec(dllimport) bool add_after(char * elem);
extern "C" __declspec(dllimport) bool list_insert(int index, char * elem);
extern "C" __declspec(dllimport) bool list_delete(int index);
extern "C" __declspec(dllimport) void traverse_list();
#endif // !SINGLELINKEDLISTWITHOUTHEADNODE_STRING
