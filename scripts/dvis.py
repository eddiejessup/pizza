#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as pp
import sys

t, s = np.loadtxt(sys.argv[1], unpack=True)

e = 100

alphas = []
for i in np.arange(0, len(t), e):
    lt = np.log(t[i:i+e])
    ls = np.log(s[i:i+e])

    alpha, lgamma = np.polyfit(lt, ls, 1)
    alphas.append(alpha)
    print(np.exp(lgamma))

pp.plot(t[::e], alphas)

pp.show()
