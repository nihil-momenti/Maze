#include <Python.h>
#include "structmember.h"
#include <stdlib.h>

typedef struct {
  int small[6];
  int big1;
  int big2;
  int big3;
} Perlin;

typedef struct {
  PyObject_HEAD
  int octaves;
  float persistence;
  Perlin *perlins;
} FractalMap;



static PyObject * __getitem__(PyObject *self, PyObject *args) {
    return value(self, args);
}

static PyObject * value(PyObject *self, PyObject *args) {
  const int x, y, z, a, b, c; /* Currently max 6-dimensional values. */
  float output;
  x = y = z = a = b = c = 0;
  if (!PyArg_ParseTuple(args, "i|iiiii", &x, &y, &z, &a, &b, &c))
    return NULL;
  
  
  for octave in range(self.octaves):
    output += (self->persistence ** (self->octaves - octave - 1)) * interpolated(x, size, &self->perlins[octave])
    x /= 2; y /= 2; z /= 2; a /= 2; b /= 2; c /= 3;
  
  return Py_BuildValue("f", output)
}

Perlin new_perlin() {
  Perlin perlin = {
    {1, 11, 29, 43, 67, 89},
    rand() % 10000 + 10000,
    rand() % 250000 + 750000,
    rand() % 500000000 + 1000000000,
  };
  return perlin;
}
  
static float interpolated(int *x, int size, Perlin *settings) {
  int *fx,*cx, *y;
  fx = malloc(size * sizeof(int));
  cx = malloc(size * sizeof(int));
  y = malloc(size * sizeof(int));
  if (! (y && fx && cx)) {
    // Error
  }
  for (i = 0; i < size; i++) {
    fx[i] = floor(x[i]);
    cx[i] = fx[i] + 1;
  }
  value = int_f(y, x, fx, cx, size, 0, settings);
  free(fx); free(cx); free(y);
  return value;
}
    
static float int_f(int *y, int *x, int *fx, int *cx, int size, int depth, Perlin *settings) {
  float x1, x2;
  if (size - depth == 0)
    return smooth(y, size, settings)
  y[depth] = fx[depth]; x1 = int_f(y, x, fx, cx, size, depth + 1, settings);
  y[depth] = cx[depth]; x2 = int_f(y, x, fx, cx, size, depth + 1, settings);
  f = (1 - cos(pi*(x[0] - fx[0]))) / 2
  return x1 * (1 - f) + x2 * f
}

static float smooth(int *x, int size, Perlin *settings) {
    float value = 0.0;
    if (size == 1) {
      x[0] -= 1; value += noise(x, 1, settings);
      x[0] += 2; value += noise(x, 1, settings);
      value /= 2;
      x[0] -= 1; value += noise(x, 1, settings);
      value /= 2;
    }
    else if (size == 2) {
      x[0] -= 1; value += noise(x, 2, settings);
      x[0] += 2; value += noise(x, 2, settings);
      x[0] -= 1;
      x[1] -= 1; value += noise(x, 2, settings);
      x[1] += 2; value += noise(x, 2, settings);
      x[0] -= 1;
      value *= 3;
      x[1] -= 1;
      x[0] -= 1; value += noise(x, 2, settings);
      x[0] += 2; value += noise(x, 2, settings);
      x[1] += 2;
      x[0] -= 2; value += noise(x, 2, settings);
      x[0] += 2; value += noise(x, 2, settings);
      value /= 16
      x[0] -= 1; x[1] -= 1;
      value += noise(x, 2, settings);
      value /= 2;
    }
    else: {
      value = noise(x, size, settings);
    }
    return value;
  }

// Crap randomiser, need to find something with less repetition
// Works okay for fractal generation though
static float noise(int *x, int size, Perlin *settings) {
    int i;
    int n = 0;
    for (i = 0; i < size; i++) {
      n += x[i] * settings->small[i];
    }
    n = (n<<13) ^ n;
    return ( 1.0 - ( (n * (n * n * settings->big1 + settings->big2) + settings->big3) & 0x7fffffff) / 1073741824.0)
  }

  
static PyMethodDef FractalMap_methods[] = {
  {"value", value, METH_VARGS, ""},
  {NULL, NULL, 0, NULL} /* Sentinel */
};

static PyMemberDef FractalMap_members[] = {
  {"octaves", T_INT, offsetof(FractalMap, octaves), 0, "number of octaves"},
  {"persistence", T_FLOAT, offsetof(FractalMap, persistence), 0, "persistence"},
  {NULL}  /* Sentinel */
};

static void
FractalMap_dealloc(FractalMap* self)
{
  self->ob_type->tp_free((PyObject*)self);
}

static int
FractalMap_init(FractalMap *self, PyObject *args, PyObject *kwds)
{
  int i;
  Perlin* perlin;

  if (! PyArg_ParseTuple(args, "if", &self->octaves, &self->persistence))
    return -1;
  
  tmp = self->perlins;
  if (! self->perlins = malloc(self->octaves * sizeof(Perlin)))
    return -1;
  Py_INCREF(self->perlins);
  Py_XDECREF(tmp);
  
  for (i = 0; i < self->octaves; i++){
    self->perlins[i] = new_perlin();
  }
  
  return 0;
}



static PyTypeObject FractalMapType = {
  PyObject_HEAD_INIT(NULL)
  0,                         /*ob_size*/
  "fractal_map.FractalMap",             /*tp_name*/
  sizeof(FractalMap), /*tp_basicsize*/
  0,                         /*tp_itemsize*/
  (destructor)FractalMap_dealloc,                         /*tp_dealloc*/
  0,                         /*tp_print*/
  0,                         /*tp_getattr*/
  0,                         /*tp_setattr*/
  0,                         /*tp_compare*/
  0,                         /*tp_repr*/
  0,                         /*tp_as_number*/
  0,                         /*tp_as_sequence*/
  0,                         /*tp_as_mapping*/
  0,                         /*tp_hash */
  0,                         /*tp_call*/
  0,                         /*tp_str*/
  0,                         /*tp_getattro*/
  0,                         /*tp_setattro*/
  0,                         /*tp_as_buffer*/
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,        /*tp_flags*/
  "Fractal Map",           /* tp_doc */
  0,                   /* tp_traverse */
  0,                 /* tp_clear */
  0,                 /* tp_richcompare */
  0,                     /* tp_weaklistoffset */
  0,                 /* tp_iter */
  0,                 /* tp_iternext */
  FractalMap_methods,             /* tp_methods */
  FractalMap_members,             /* tp_members */
  0,                         /* tp_getset */
  0,                         /* tp_base */
  0,                         /* tp_dict */
  0,                         /* tp_descr_get */
  0,                         /* tp_descr_set */
  0,                         /* tp_dictoffset */
  (initproc)FractalMap_init,      /* tp_init */
  0,                         /* tp_alloc */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC
initFractalMap(void) {
  PyObject* m;

  FractalMapType.tp_new = PyType_GenericNew;
  if (PyType_Ready(&FractalMapType) < 0)
      return;

  m = Py_InitModule3("fractal_map", FractalMapMethods,"");

  Py_INCREF(&FractalMapType);
  PyModule_AddObject(m, "Noddy", (PyObject *)&FractalMapType);
}



int main(int argc, char *argv[]) {
  /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initFractalMap();
}