# Copyright 2012 Luis Pedro Coelho <luis@luispedro.org>
# License: MIT

from abc import ABCMeta, abstractmethod
from contextlib import contextmanager

@contextmanager
def scopedimage(im):
    '''
    with scopedimage(im):
        ...
    '''
    yield im
    im.unload()

class Image(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def has_channel(self, ch):
        pass

    @abstractmethod
    def get(self, ch):
        pass

    @abstractmethod
    def unload(self):
        pass

    @abstractmethod
    def channels(self):
        pass

    @abstractmethod
    def __getstate__(self):
        pass

    @abstractmethod
    def __setstate__(self, state):
        pass

class FileImage(object):
    def __init__(self, files=None):
        super(FileImage, self).__init__()
        if files is None:
            files = {}
        self.files = files
        self.cache = {}

    def has_channel(self, ch):
        return ch in self.files

    def get(self, ch):
        if ch in self.cache:
            return self.cache[ch]
        data = self.open_file(self.files[ch])
        self.cache[ch] = data
        return data

    def unload(self):
        self.cache = {}

    def channels(self):
        return self.files.keys()

    def open_file(self, fname):
        from imread import imread
        return imread(fname)

    def composite(self, channels=('dna', 'protein', None)):
        import mahotas
        def g(ch):
            if ch is not None and \
                self.has_channel(ch): return self.get(ch)
        c0,c1,c2 = channels
        return mahotas.as_rgb(g(c0),g(c1),g(c2))

    def __getstate__(self):
        copy = self.__dict__.copy()
        del copy['cache']
        items = copy.items()
        items.sort(key=lambda it: it[0])
        return items

    def __setstate__(self, state):
        self.cache = {}
        for k,v in state:
            self.__dict__[k] = v

    def __repr__(self):
        '''Implement repr() operator'''
        return 'Image( %s )' % repr(self.files)


    def __eq__(self, other):
        return self.files == other.files

    def __ne__(self, other):
        return not (self == other)


    def show(self, **kwargs):
        '''
        Shows the image composite

        See composite.
        '''
        from pylab import imshow
        imshow(self.composite(**kwargs))


class StackFileImage(FileImage):
    def get(self, ch, plane=None):
        data = super(StackFileImage, self).get(ch)
        if plane is None:
            import numpy as np
            return np.array(data)
        if plane == 'max':
            return np.max(data, 0)
        return data[plane]

    def composite(self, channels=('dna', 'protein', None), plane='central'):
        import mahotas
        if plane == 'central':
            plane = len(self.files.values()[0])//2
        def g(ch):
            if ch is not None and self.has_channel(ch):
                return self.get(ch, plane)

        c0,c1,c2 = channels
        return mahotas.as_rgb(g(c0), g(c1), g(c2))

    def open_file(self, fname):
        from imread import imread_multi
        return imread_multi(fname)


class MultiFileImage(FileImage):
    '''
    These images have multiple files per channel, each one corresponding to a stack slice
    '''
    def __init__(self, files=None):
        super(MultiFileImage, self).__init__(files)

    def get(self, ch, plane=None):
        if plane is None:
            import numpy as np
            return np.array([self.get(ch, p) for p,_ in enumerate(self.files[ch])])
        if (ch,plane) in self.cache:
            return self.cache[ch, plane]
        data = self.open_file(self.files[ch][plane])
        self.cache[ch, plane] = data
        return data


    def composite(self, plane='central'):
        import mahotas
        if plane == 'central':
            plane = len(self.files.values()[0])//2
        def g(ch):
            if self.has_channel(ch):
                return self.get(ch, plane)
        return mahotas.as_rgb(g('dna'), g('protein'), None)

