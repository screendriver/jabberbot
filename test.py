class Oben(object):
    def foo(self):
        print('Oben')

class Unten(Oben):
    def foo(self):
        super(Unten, self).foo()

        print('Unten')

Unten().foo()
