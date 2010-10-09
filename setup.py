from distutils.core import setup, Extension
setup(name="fractal_map", version="1.0", ext_modules=[Extension("fractal_map", ["fractal_map.c"])])