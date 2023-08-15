#ifndef PYFMATH
#define PYFMATH
#ifdef __cplusplus
extern "C" {
#endif
#include "Python.h"
#include "stdint.h"
#define add_name(func) #func, _##func
#define parse(arg) (*(int64_t*)_parse(PyFloat_AS_DOUBLE(arg)))
#define parsed parse(args)
#define _declare(func, value, ...) static PyObject * func(__VA_ARGS__) {return value;}
#define declare(func, operation, type) _declare(_##func, Py##type##_FromLong(operation), PyObject * self, PyObject * args)
const static int64_t one = 0x3FF0000000000000;
static void * _parse(double arg){return & arg;}
_declare(PyFloat_FromLong, PyFloat_FromDouble(*(double*)&x), int64_t x);
declare(abs, parsed & INT64_MAX, Float);
declare(sign, ~parsed >> 0x3F, Bool);
declare(sqrt, (parsed >> 1) + (one >> 1), Float);
_declare(_pow, PyFloat_FromLong((parse(args[0]) - one) * PyFloat_AS_DOUBLE(args[1]) + one), PyObject * self, PyObject *const *args, Py_ssize_t nargs);
static PyMethodDef fmath_methods[] = {
    {add_name(pow), METH_FASTCALL, "pow: return x to the power of y"},
    {add_name(abs), METH_O, "abs: return the absolute value of x"},
    {add_name(sign), METH_O, "sign: return True if x>=0 else False"},
    {add_name(sqrt), METH_O, "sqrt: return the square root of x"},
    {NULL, NULL, 0, NULL}
};
static struct PyModuleDef pyfmath_module = {PyModuleDef_HEAD_INIT, "fmath", NULL, -1, fmath_methods};
PyMODINIT_FUNC PyInit_fmath(void){return PyModule_Create(&pyfmath_module);}
#ifdef __cplusplus
}
#endif
#endif