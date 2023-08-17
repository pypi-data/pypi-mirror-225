#ifndef DOUBLELINKEDLISTWITHOUTHEADNODE_FLOAT
#define DOUBLELINKEDLISTWITHOUTHEADNODE_FLOAT
#include "framework.h"
#include "DataStorage.h"
#include <iostream>
extern "C" __declspec(dllimport) void init_list();
extern "C" __declspec(dllimport) void destroy_list();
extern "C" __declspec(dllimport) void clear_list();
extern "C" __declspec(dllimport) bool list_empty();
extern "C" __declspec(dllimport) int list_length();
extern "C" __declspec(dllimport) float get_elem(int index);
extern "C" __declspec(dllimport) int locate_elem(float elem);
extern "C" __declspec(dllimport) float prior_elem(float elem);
extern "C" __declspec(dllimport) float next_elem(float elem);
extern "C" __declspec(dllimport) bool add_first(float elem);
extern "C" __declspec(dllimport) bool add_after(float elem);
extern "C" __declspec(dllimport) bool list_insert(int index, float elem);
extern "C" __declspec(dllimport) bool list_delete(int index);
extern "C" __declspec(dllimport) void traverse_list();
extern "C" __declspec(dllimport) void traverse_list_by_reverse_order();
#endif // !DOUBLELINKEDLISTWITHOUTHEADNODE_FLOAT
