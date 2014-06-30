from __future__ import print_function
import numpy as np

lim_map = {'x': 0, 'y': 1, 'z': 2}
atom_map = {'x': 2, 'y': 3, 'z': 4}


def histo2d(data, nbins, dim1, dim2, lo1=None, hi1=None, lo2=None, hi2=None):
    idim1_lim = lim_map[dim1]
    idim2_lim = lim_map[dim2]
    idim1_atom = atom_map[dim1]
    idim2_atom = atom_map[dim2]

    flag = 0
    while True:
        which, time, flag = data.iterator(flag)
        if flag == -1:
            break

        time, box, atoms, bonds, tris, lines = data.viz(which)

        los, his = box[:3], box[3:]
        if lo1 is None:
            lo1 = los[idim1_lim]
        if hi1 is None:
            hi1 = his[idim1_lim]
        if lo2 is None:
            lo2 = los[idim2_lim]
        if hi2 is None:
            hi2 = his[idim2_lim]

        r = np.array(atoms)
        r_1 = r[:, idim1_atom]
        r_2 = r[:, idim2_atom]

        lims = [[lo1, hi1], [lo2, hi2]]
        h, xe, ye = np.histogram2d(r_1, r_2, bins=nbins, range=lims)
        try:
            h_tot += h
        except UnboundLocalError:
            h_tot = h
    return h_tot, xe, ye
