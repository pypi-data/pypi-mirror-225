#ifndef GRAPES_GRAPES_CGRAPH_HEAP_H_
#define GRAPES_GRAPES_CGRAPH_HEAP_H_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

typedef struct MinHeapNode MinHeapNode;
typedef struct MinHeap     MinHeap;

MinHeap   *MinHeap_alloc(Py_ssize_t max_size);
void       MinHeap_free(MinHeap *heap);
void       MinHeap_insert(MinHeap *heap, Py_ssize_t key, Py_ssize_t priority);
Py_ssize_t MinHeap_extract_min(MinHeap *heap);
int        MinHeap_is_empty(MinHeap *heap);
void MinHeap_siftdown(MinHeap *heap, Py_ssize_t startpos, Py_ssize_t pos);
void MinHeap_siftup(MinHeap *heap, Py_ssize_t pos);
void MinHeap_print(MinHeap *heap);

#endif  // GRAPES_GRAPES_CGRAPH_HEAP_H_