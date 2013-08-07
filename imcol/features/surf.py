# -*- coding: utf-8 -*-
# Copyright (C) 2011-2013 Luis Pedro Coelho <luis@luispedro.org>
# License: MIT

from __future__ import division, with_statement
import numpy as np
import mahotas.surf

def surf_ref(f, ref='dna', max_points=1024):
    '''
    features = surfref(im, ref='dna', max_points=1024)

    Compute SURF-ref as defined in


        Luis Pedro Coelho, Joshua D. Kangas, Armaghan Naik, Elvira
        Osuna-Highley, Estelle Glory-Afshar, Margaret Fuhrman, Ramanuja Simha,
        Peter B. Berget, Jonathan W. Jarvik, and Robert F.  Murphy,
        *Determining the subcellular location of new proteins from microscope
        images using local features* in Bioinformatics, 2013 [`DOI
        <http://dx.doi.org/10.1093/bioinformatics/btt392>`__]

    Parameters
    ----------
    im : image object
    ref : str, optional
        Reference channel, by default DNA
    max_points : int, optional
        Max number of points to compute (by default 1024)
    '''
    fi = mahotas.surf.integral(f.copy())
    points = mahotas.surf.interest_points(fi, 6, 24, 1, max_points=max_points, is_integral=True)
    descs = mahotas.surf.descriptors(fi, points, is_integral=True, descriptor_only=True)
    if ref is None:
        return descs
    ri = mahotas.surf.integral(ref.copy())
    descsref = mahotas.surf.descriptors(ri, points, is_integral=True, descriptor_only=True)
    return np.hstack( (descs, descsref) )

