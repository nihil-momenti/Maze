#include <Python.h>

static PyMethodDef FractalMapMethods[] = {
  {"value", value, METH_VARGS | METH_KEYWORDS, ""},
  {NULL, NULL, 0, NULL} /* Sentinel */
};

PyMODINIT_FUNC initfractal_map(void) {
  (void) Py_InitModule("fractal_map", FractalMapMethods);
}

static PyObject * value(PyObject *self, PyObject *args, PyObject *keywords) {
  const 


int main(int argc, char *argv[]) {
  /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initfractal_map();
}