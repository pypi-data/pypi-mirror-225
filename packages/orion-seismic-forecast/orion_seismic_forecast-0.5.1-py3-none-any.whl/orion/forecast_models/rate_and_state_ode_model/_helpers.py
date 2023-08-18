# ------------------------------------------------------------------------------------------------
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2020-, Lawrence Livermore National Security, LLC
# All rights reserved
#
# See top level LICENSE, COPYRIGHT, CONTRIBUTORS, NOTICE, and ACKNOWLEDGEMENTS files for details.
# ------------------------------------------------------------------------------------------------

import numpy as np

from ._common import jitted

_C = np.array(
    [
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [1.0 / 4.0, 0.0, 0.0, 0.0, 0.0],
        [3.0 / 32.0, 9.0 / 32.0, 0.0, 0.0, 0.0],
        [1932.0 / 2197.0, -7200.0 / 2197.0, 7296.0 / 2197.0, 0.0, 0.0],
        [439.0 / 216.0, -8.0, 3680.0 / 513.0, -845.0 / 4104.0, 0.0],
        [-8.0 / 27.0, 2.0, -3544.0 / 2565.0, 1859.0 / 4104.0, -11.0 / 40.0],
    ],
    dtype=np.float64,
)

_W = np.array(
    [
        [25.0 / 216.0, 0.0, 1408.0 / 2565.0, 2197.0 / 4101.0, -1.0 / 5.0, 0.0],
        [
            16.0 / 135.0,
            0.0,
            6656.0 / 12825.0,
            28561.0 / 56430.0,
            -9.0 / 50.0,
            2.0 / 55.0,
        ],
    ],
    dtype=np.float64,
)


@jitted
def rate(t, s, s0i, tci, tmax, dt, dtmax, dtfac, dt_reduce_max, rtol):
    """
    Solve rate-and-state ODE using Runge-Kutta-Fehlberg method.

    Note
    ----
    See <https://maths.cnam.fr/IMG/pdf/RungeKuttaFehlbergProof.pdf>.

    """
    nt = len(t)
    i, ti = 0, t[0]
    count, success = 0, True
    times, rates = [ti], [1.0]
    while ti < tmax:
        si = s[i] * s0i

        # Calculate derivatives
        r0 = rates[-1]
        k0 = dt * r0 * tci * (si - r0)
        r1 = rates[-1] + _C[1, 0] * k0
        k1 = dt * r1 * tci * (si - r1)
        r2 = rates[-1] + _C[2, 0] * k0 + _C[2, 1] * k1
        k2 = dt * r2 * tci * (si - r2)
        r3 = rates[-1] + _C[3, 0] * k0 + _C[3, 1] * k1 + _C[3, 2] * k2
        k3 = dt * r3 * tci * (si - r3)
        r4 = rates[-1] + _C[4, 0] * k0 + _C[4, 1] * k1 + _C[4, 2] * k2 + _C[4, 3] * k3
        k4 = dt * r4 * tci * (si - r4)
        r5 = (rates[-1] + _C[5, 0] * k0 + _C[5, 1] * k1 + _C[5, 2] * k2 + _C[5, 3] * k3 + _C[5, 4] * k4)
        k5 = dt * r5 * tci * (si - r5)

        # Calculate error
        ro4 = rates[-1] + _W[0, 0] * k0 + _W[0, 2] * k2 + _W[0, 3] * k3 + _W[0, 4] * k4
        ro5 = (rates[-1] + _W[1, 0] * k0 + _W[1, 2] * k2 + _W[1, 3] * k3 + _W[1, 4] * k4 + _W[1, 5] * k5)
        eps = max(np.abs(ro5 - ro4) / ro5, 1.0e-16)

        # Check convergence
        if eps > rtol:
            dt /= dtfac
            count += 1

            if count == dt_reduce_max + 1:
                success = False
                break

        else:
            rates.append(ro5)
            times.append(ti)
            ti += dt

            # Update step size
            dt *= 0.84 * (rtol / eps)**0.25
            dt = min(dt, dtmax, tmax - ti)
            count = 0

            # Check current stressing rate
            if i + 1 < nt:
                dti = t[i + 1] - ti
                if 0.0 < dti < dt:
                    dt = dti
                    i += 1

    return (np.interp(t, times, rates) if success else -np.ones_like(t))
