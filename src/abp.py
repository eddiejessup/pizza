from __future__ import print_function
import numpy as np
import matplotlib.pyplot as pp


def props(data, index=None, timestep=None):
    a = data.get_atom_data(index, timestep)
    r = np.array([a['x'], a['y'], a['z']]).T
    F = np.array([a['fx'], a['fy'], a['fz']]).T
    F_prop = np.array([a['v_f_prop_x'], a['v_f_prop_y'], a['v_f_prop_z']]).T
    F_cons = np.array([a['f_f_cons[1]'], a['f_f_cons[2]'], a['f_f_cons[3]']]).T
    F_lang = F - F_prop - F_cons
    return r, F, F_prop, F_cons, F_lang


def atom_torque(data, index=None, timestep=None):
    a = data.get_atom_data(index, timestep)
    tq = np.array([a['tqx'], a['tqy'], a['tqz']]).T
    return tq


def effective_force(F_prop, F_cons):
    u_F_propuls = F_prop / np.sum(np.square(F_prop), axis=-1)[:, np.newaxis]
    F_eff = np.sum((F_cons + F_prop) * u_F_propuls, axis=-1)
    return F_eff


def mean_F_eff(data, index=None, timestep=None):
    r, F, F_prop, F_cons, F_lang = props(data, index, timestep)
    F_eff = effective_force(F_prop, F_cons)
    return np.mean(F_eff)


def feff_hist(data, index=None, timestep=None, nbins=40):
    r, F, F_prop, F_cons, F_lang = props(data, index, timestep)
    F_eff = effective_force(F_prop, F_cons)

    # tq = atom_torque(data, index, timestep)
    # tq_mag = np.sqrt(np.sum(np.square(tq), axis=1))
    # pp.scatter(F_eff, tq_mag)
    # pp.show()

    # c = (F_eff - min(F_eff)) / max(F_eff - min(F_eff))
    # pp.scatter(r[:, 0], r[:, 1], c=c, s=10, lw=0, cmap='hot')

    h, xe, ye = np.histogram2d(
        r[:, 0], r[:, 1], bins=nbins, range=[[0.0, 150.0], [0.0, 150.0]])
    h[...] = 0.0
    ixs = np.digitize(r[:, 0], xe[1:-1])
    iys = np.digitize(r[:, 1], ye[1:-1])
    for ix, iy, ir in zip(ixs, iys, range(len(r))):
        h[ix, iy] += F_eff[ir]

    pp.imshow(h, interpolation='none', aspect='equal')
    pp.show()


def hist(data, index=None, timestep=None, nbins=40):
    r, F, F_prop, F_cons, F_lang = props(data, index, timestep)

    r = r[:, :2]

    h, xe, ye = np.histogram2d(
        r[:, 0], r[:, 1], bins=nbins, range=[[0.0, 150.0], [0.0, 150.0]])

    pp.imshow(h, interpolation=None)
    pp.show()

    f = np.fft.fft2(h)
    k = np.fft.fftfreq(nbins, xe[1] - xe[0])

    print(np.sum(np.square(np.abs(f))))
    Kx, Ky = np.meshgrid(k, k)
    K = np.sqrt(Kx ** 2 + Ky ** 2)
    k_mean = np.sum(np.abs(K) * np.square(np.abs(f))) / \
        np.sum(np.square(np.abs(f)))
    L_mean = (2.0 * np.pi) / k_mean
    print('L', L_mean)

    # pp.imshow(np.log(np.fft.fftshift(np.square(np.abs(f)))), interpolation='none', extent=(min(k), max(k), min(k), max(k)))
    # pp.show()


def structure_factor(data, index=None, timestep=None):
    r, F, F_prop, F_cons, F_lang = props(data, index, timestep)

    r = r[:, :2]

    L = 150.0

    for nx in np.linspace(0.5, 10, 10):
        for ny in np.linspace(0.5, 10, 10):
            kj = 1j * (2.0 * np.pi) / (L * np.array([nx, ny]))
            S = 0.0
            for r1 in r:
                S += np.sum(np.exp(-kj * (r1 - r)))
            S /= len(r) ** 2
            print(nx, ny, S.real)
