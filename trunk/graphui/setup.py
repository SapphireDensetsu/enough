from distutils.core import setup, Extension

if __name__ == '__main__':
    from Pyrex.Compiler.Main import compile, default_options
    for pyrex_source in ['Lib/Point.pyx', 'Shapes/Ellipse.pyx']:
        print "Compiling", pyrex_source
        compile(pyrex_source, default_options)

    setup(ext_modules=[Extension("Lib.Point", ["Lib/Point.c"]),
                       Extension("Shapes.Ellipse", ["Shapes/Ellipse.c"])])
