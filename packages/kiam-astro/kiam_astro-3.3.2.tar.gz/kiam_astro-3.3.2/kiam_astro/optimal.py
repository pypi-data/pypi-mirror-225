"""
This Python module is a part of the KIAM Astrodynamics Toolbox developed in
Keldysh Institute of Applied Mathematics (KIAM), Moscow, Russia.

The module provides routines to solve optimal control problems.

The toolbox is licensed under the MIT License.

For more information see GitHub page of the project:
https://github.com/shmaxg/KIAMToolbox
"""

import kiam
from scipy.optimize import minimize
from numpy.linalg import norm
import numpy
from numpy import sqrt
from typing import Callable, Any

# r2bp_pontr_energy_irm_u_rv problem
def solve_r2bp_pontr_energy_irm_u_rv(x0: numpy.ndarray, x1: numpy.ndarray, tof: float, nrevs: int, disp_iter: bool = True, atol_in: float = 1e-12, rtol_in: float = 1e-12, atol_ex: float = 1e-10, rtol_ex: float = 1e-10):
    """
    Solve standard energy-optimal control problem by Pontryagin principle in two-body problem,
    position-velocity variables in ideally-regulated engine model, using control acceleration as control variable.

    Parameters:
    -----------

    `x0` : numpy.ndarray, shape (6,)

    Initial phase state. Stucture: [x, y, z, vx, vy, vz]. Dimensionless, mu = 1.0.

    `x1` : numpy.ndarray, shape (6,)

    Target phase state. Stucture: [x, y, z, vx, vy, vz]. Dimensionless, mu = 1.0.

    `tof` : float

    The time of flight.

    `nrevs` : int

    The number of revolutions.

    `disp_iter` : bool

    Whether to display iterations of the differential continuation method. Default: True.

    `atol_in` : float

    Absolute tolerance when integrating the internal equations (equations of motion). Default is 1e-12.

    `rtol_in` : float

    Relative tolerance when integrating the internal equations (equations of motion). Default is 1e-12.

    `atol_ex` : float

    Absolute tolerance when integrating the external equations (equations of differential continuation). Default is 1e-10.

    `rtol_ex` : float

    Relative tolerance when integrating the internal equations (equations of differential continuation). Default is 1e-10.

    Returns:
    --------

    `zopt` : numpy.ndarray, shape (6,)

    The optimized vector of initial conjugate variables. Structure: [lamx, lamy, lamz, lamvx, lamvy, lamvz].
    The optimization is done by using a Newton method with adaptive step.

    `zend` : numpy.ndarray, shape (6,)

    The non-optimized vector of initial conjugate variables obtained by differential correction procedure. Structure: [lamx, lamy, lamz, lamvx, lamvy, lamvz].

    `res` : numpy.ndarray, shape (6,)

    The residue between the target position and velocity and obtained by using `zopt` conjugate variables.

    `jac` : numpy.ndarray, shape (6, 6)

    The Jacobian of the residue function at `zopt`.

    Examples:
    ---------
    ```
    x0 = numpy.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])

    x1 = numpy.array([1.5, 0.0, 0.0, 0.0, numpy.sqrt(1.5), 0.0])

    tof = 3 * numpy.pi

    nrevs = 1

    zopt, zend, res, jac = optimal.solve_r2bp_pontr_energy_irm_u_rv(x0, x1, tof, nrevs)
    ```
    """
    kiam.FKIAMToolbox.optimalcontrol.atol_in = atol_in
    kiam.FKIAMToolbox.optimalcontrol.rtol_in = rtol_in
    kiam.FKIAMToolbox.optimalcontrol.atol_ex = atol_ex
    kiam.FKIAMToolbox.optimalcontrol.rtol_ex = rtol_ex
    kiam.FKIAMToolbox.optimalcontrol.display_iterations = disp_iter
    zopt, zend, res, jac = kiam.FKIAMToolbox.optimalcontrol.solve_energy_optimal_problem(x0, x1, tof, nrevs)
    return zopt, zend, res, jac
def propagate_r2bp_pontr_energy_irm_u_rv(tspan: numpy.ndarray,  y0: numpy.ndarray, mu: float = 1.0, mu0: float = 1.0, atol: float = 1e-12, rtol: float = 1e-12):
    """
    Propagate extended by conjugate variables equations of motion.
    Two-body problem, energy-optimal control, ideally-regulated engine model, thrust acceleration as control function, position and velocity as variables.

    Parameters:
    -----------

    `tspan` : numpy.ndarray, shape (n,)

    The times at which the solution should be obtained.

    `y0` : numpy.ndarray, shape (12,), (156,), (168,)

    The initial state.

    Structure options:

    1. [rvect, vvect, lamr, lamv]

    2. [rvect, vvect, lamr, lamv, stm]

    3. [rvect, vvect, lamr, lamv, stm, dxdtau]

    where stm is the state transition matrix and dxdtau is derivative of [rvect, vvect, lamr, lamv] with respect to continuation parameter tau (gravitational parameter mu = mu0 + (1 - mu0) * tau).

    `mu` : float

    Gravitational parameter of the central body. Default is 1.0.

    `mu0` : float

    Initial value of the gravitational parameter in differential continuation process.
    This parameter is required only if dxdtau is among the dependent variables (len(y0) == 168).
    Otherwise the value is ignored.

    `atol` : float

    Absolute tolerance when integrating the equations. Default is 1e-12.

    `rtol` : float

    Relative tolerance when integrating the equations. Default is 1e-12.

    Returns:
    --------

    `T` : numpy.ndarray, shape (n,)

    The times at which the solution is obtained. Equals to tspan.

    `Y` : numpy.ndarray, shape (m, n)

    The integrated solutions. Each column correspond to a vector y at the correspondent time t in T.

    Examples:
    ---------
    ```
    x0 = numpy.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])

    z0 = numpy.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])

    tof = 3 * numpy.pi

    T, Y = optimal.propagate_r2bp_pontr_energy_irm_u_rv(numpy.linspace(0.0, tof, 10000), numpy.concatenate((x0, z0)))
    ```
    """

    neq = len(y0)

    if neq == 12:
        stmreq, gradmureq = False, False
    elif neq == 156:
        stmreq = True
        gradmureq = False
    elif neq == 168:
        stmreq = True
        gradmureq = False
    else:
        raise Exception('Wrong number of dependent variables.')

    T, Y = kiam.FKIAMToolbox.propagationmodule.propagate_r2bp_pontr_eopt_irm_u_rv(tspan, y0, neq, atol, rtol, mu, mu0, stmreq, gradmureq)

    return T, Y

# r2bp_pontr_time_bnd_f_rv problem
def solve_r2bp_pontr_time_bnd_f_rv(x0: numpy.ndarray, x1: numpy.ndarray, fmax: float, vex: float, mass0: float, z0: numpy.ndarray, mu: float = 1.0, method: str = 'trust-constr', atol: float = 1e-12, rtol: float = 1e-12):
    """
    Solve time-optimal control problem by Pontryagin principle in two-body problem,
    position-velocity variables for thrust-bounded engine model with fixed exhaust velocity, using thrust force as control variable

    Parameters:
    -----------

    `x0` : numpy.ndarray, shape (6,)

    Initial phase state. Stucture: [x, y, z, vx, vy, vz].

    `x1` : numpy.ndarray, shape (6,)

    Target phase state. Stucture: [x, y, z, vx, vy, vz].

    `fmax` : float

    The maximal thrust force of the engine.

    `vex` : float

    The exhaust velocity.

    `mass0` : float

    The initial mass of spacecraft.

    `z0` : numpy.ndarray, shape(7,)

    The initial guess for the optimization variables. Structure: [px, py, pz, pvx, pvy, pvz, tof], where
    px, py, pz -- conjugate to x, y, z variables, pvx, pvy, pvz -- conjugate to vx, vy, vz variables,
    tof -- time of flight.

    `mu` : float

    Gravitational parameter. Default: 1.0.

    `method` : str

    Optimization method. Options: `'trust-constr'` (default), `'nelder-mead'`.

    `atol` : float

    The absolute integration tolerance. Default: 1e-12.

    `rtol` : float

    The relative integration tolerance. Default: 1e-12.

    Returns:
    --------

    `zopt` : numpy.ndarray, shape (7,)

    The optimal optimization variables. Sturcture: [px, py, pz, pvx, pvy, pvz, tof], where
    px, py, pz -- conjugate to x, y, z variables, pvx, pvy, pvz -- conjugate to vx, vy, vz variables,
    tof -- time of flight.

    `res` : numpy.ndarray, shape (7,)

    The optimal residue. Structure: [r(tend) - r1, v(tend) - v1, H(tend) - 0], where tend -- final time,
    r(tend) -- the final integrated position, v(tend) -- the final integrated velocity,
    r1 -- the target position, v1 -- the target velocity, H(tend) -- the Hamiltonian at final time.

    `jac` : numpy.ndarray, shape (7, 7)

    The Jacobian of res, i.e. the derivative matrix of res wrt optimization variables.

    Examples:
    ---------
    ```
    units = kiam.units('sun')

    x0 = numpy.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])

    x1 = numpy.array([1.5, 0.0, 0.0, 0.0, 1 / numpy.sqrt(1.5), 0.0])

    fmax = 14.8e-03 / units['AccUnit']

    vex = 9.3 / units['VelUnit']

    mass0 = 80

    z0 = numpy.zeros(7, )

    z0[0:3] = numpy.array([-5.0, -2.0, 0.0])

    z0[3:6] = numpy.array([-2.0, -7.0, 0.0])

    z0[6] = optimal.estimate_tof(x0, x1, fmax / mass0, 1.0)

    zopt, res, jac = optimal.solve_r2bp_pontr_time_bnd_f_rv(x0, x1, fmax, vex, mass0, z0, 1.0, method='trust-constr', atol=1e-10, rtol=1e-10)

    T, Y = optimal.propagate_r2bp_pontr_time_bnd_f_rv(numpy.linspace(0.0, zopt[6], 10000), numpy.concatenate((x0, zopt[0:6])), fmax, vex, mass0)

    fig = kiam.plot(Y[0, :], Y[1, :], None, 'x', 'y', axis_equal=True)

    fig.show()

    mass = mass0 - fmax / vex * zopt[-1]

    print(f'Начальное приближение для времени полета: {z0[-1] * units["TimeUnit"]:.2f} дней')

    print(f'Оптимальное время полета: {zopt[-1] * units["TimeUnit"]:.2f} дней')

    print(f'Масса: {mass0:.2f} ---> {mass:.2f}, затрачивается {(1 - mass / mass0) * 100:.2f}%')

    print(f'Начальное ускорение: {fmax / mass0 * units["AccUnit"] * 1000} мм/с2')
    ```
    """

    if method == 'nelder-mead':

        options = {
            'disp': True,
            'maxiter': 10000,
            'return_all': False,
            'xatol': 1e-10,
            'fatol': 1e-10,
        }

        def objective(z):
            residue_norm, _ = objective_r2bp_pontr_time_bnd_f_rv(z, x0, x1, fmax, vex, mass0, mu, atol, rtol)
            return norm(residue_norm)

        result = minimize(objective,
                          z0,
                          method='Nelder-Mead',
                          options=options,
                          callback=callback_nelder_mead)

        f, jac = residue_r2bp_pontr_time_bnd_f_rv(result.x, x0, x1, fmax, vex, mass0, mu, atol, rtol)

        return result.x, f, jac

    if method == 'trust-constr':

        options = {
            'disp': True,
            'maxiter': 10000,
            'gtol': 1e-10,
            'xtol': 1e-10,
        }

        def objective(z):
            residue_norm, jacobian = objective_r2bp_pontr_time_bnd_f_rv(z, x0, x1, fmax, vex, mass0, mu, atol, rtol)
            return norm(residue_norm), jacobian

        result = minimize(objective,
                          z0,
                          jac=True,
                          method='trust-constr',
                          options=options,
                          callback=callback_trust_constr)

        f, jac = residue_r2bp_pontr_time_bnd_f_rv(result.x, x0, x1, fmax, vex, mass0, mu, atol, rtol)

        return result.x, f, jac
def propagate_r2bp_pontr_time_bnd_f_rv(tspan: numpy.ndarray, y0: numpy.ndarray, fmax: float, vex: float, mass0: float, mu: float = 1.0, atol: float = 1e-12, rtol: float = 1e-12):
    """
    Propagate extended by conjugate variables equations of motion.
    Two-body problem, position-velocity variables, thrust-bounded engine model with fixed exhaust velocity, thrust force as control variable.

    Parameters:
    -----------

    `tspan` : numpy.ndarray, shape (n,)

    The times at which the solution should be obtained.

    `y0` : numpy.ndarray, shape (12,), (156,)

    The initial state.

    Structure options:

    1. [rvect, vvect, lamr, lamv]

    2. [rvect, vvect, lamr, lamv, stm]

    where stm is the state transition matrix.

    `fmax` : float

    The maximal thrust force of the engine.

    `vex` : float

    The exhaust velocity.

    `mass0` : float

    The initial mass of spacecraft.

    `mu` : float

    Gravitational parameter. Default: 1.0.

    `atol` : float

    The absolute integration tolerance. Default: 1e-12.

    `rtol` : float

    The relative integration tolerance. Default: 1e-12.

    Returns:
    --------

    `T` : numpy.ndarray, shape (n,)

    The times at which the solution is obtained. Equals to tspan.

    `Y` : numpy.ndarray, shape (m, n)

    The integrated solutions. Each column correspond to a vector y at the correspondent time t in T.

    Examples:
    ---------
    ```
    units = kiam.units('sun')

    x0 = numpy.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])

    fmax = 14.8e-03 / units['AccUnit']

    vex = 9.3 / units['VelUnit']

    mass0 = 80

    z0 = numpy.array([0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 2 * numpy.pi])

    T, Y = optimal.propagate_r2bp_pontr_time_bnd_f_rv(numpy.linspace(0.0, z0[6], 10000), numpy.concatenate((x0, z0[0:6])), fmax, vex, mass0)

    fig = kiam.plot(Y[9, :], Y[10, :], None, 'px', 'py', axis_equal=True)

    fig.show()
    ```
    """
    neq = len(y0)
    if neq == 12:
        stmreq = False
    elif neq == 156:
        stmreq = True
    else:
        raise Exception('Wrong number of dependent variables.')
    T, Y = kiam.FKIAMToolbox.propagationmodule.propagate_r2bp_pontr_topt_bnd_f_rv(tspan, y0, neq, atol, rtol, mu, fmax, vex, mass0, stmreq)
    return T, Y
def residue_r2bp_pontr_time_bnd_f_rv(z: numpy.ndarray, x0: numpy.ndarray, x1: numpy.ndarray, fmax: float, vex: float, mass0: float, mu: float = 1.0, atol: float = 1e-12, rtol: float = 1e-12):
    """
    Residue vector in boundary value problem derived for the time-optimal control problem.
    Two-body problem, bounded thrust force and fixed exhaust velocity, thrust force as control variable, position-velocity variables.

    Parameters:
    -----------

    `z` : numpy.ndarray, shape (7,)

    Optimization variables. Structure: [px, py, pz, pvx, pvy, pvz, tof], where
    px, py, pz -- conjugate to x, y, z variables, pvx, pvy, pvz -- conjugate to vx, vy, vz variables,
    tof -- time of flight.

    `x0` : numpy.ndarray, shape (6,)

    Initial phase state. Stucture: [x, y, z, vx, vy, vz].

    `x1` : numpy.ndarray, shape (6,)

    Target phase state. Stucture: [x, y, z, vx, vy, vz].

    `fmax` : float

    The maximal thrust force of the engine.

    `vex` : float

    The exhaust velocity.

    `mass0` : float

    The initial mass of spacecraft.

    `mu` : float

    Gravitational parameter. Default: 1.0.

    `atol` : float

    The absolute integration tolerance. Default: 1e-12.

    `rtol` : float

    The relative integration tolerance. Default: 1e-12.

    Returns:
    --------

    `res` : numpy.ndarray, shape (7,)

    The residue. Structure: [r(tend) - r1, v(tend) - v1, H(tend) - 0], where tend -- final time,
    r(tend) -- the final integrated position, v(tend) -- the final integrated velocity,
    r1 -- the target position, v1 -- the target velocity, H(tend) -- the Hamiltonian at final time.

    `jac` : numpy.ndarray, shape (7, 7)

    The Jacobian of res, i.e. the derivative matrix of res wrt optimization variables.

    Examples:
    ---------
    ```
    units = kiam.units('sun')

    x0 = numpy.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])

    x1 = numpy.array([1.5, 0.0, 0.0, 0.0, 1/numpy.sqrt(1.5), 0.0])

    fmax = 14.8e-03 / units['AccUnit']

    vex = 9.3 / units['VelUnit']

    mass0 = 80

    z = numpy.array([0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 2 * numpy.pi])

    res, jac = optimal.residue_r2bp_pontr_time_bnd_f_rv(z, x0, x1, fmax, vex, mass0)

    print(res, jac)
    ```
    """

    kiam.FKIAMToolbox.optimalcontrol.atol_in = atol
    kiam.FKIAMToolbox.optimalcontrol.rtol_in = rtol

    kiam.FKIAMToolbox.optimalcontrol.ext_r0 = x0[0:3]
    kiam.FKIAMToolbox.optimalcontrol.ext_v0 = x0[3:6]
    kiam.FKIAMToolbox.optimalcontrol.ext_r1 = x1[0:3]
    kiam.FKIAMToolbox.optimalcontrol.ext_v1 = x1[3:6]

    kiam.FKIAMToolbox.optimalcontrol.ext_topt_fmax = fmax
    kiam.FKIAMToolbox.optimalcontrol.ext_topt_mu = mu
    kiam.FKIAMToolbox.optimalcontrol.ext_topt_vex = vex
    kiam.FKIAMToolbox.optimalcontrol.ext_topt_mass0 = mass0

    kiam.FKIAMToolbox.equationsmodule.mu_kr2bp_pontr_topt_bnd_f_rv = mu
    kiam.FKIAMToolbox.equationsmodule.fmax_kr2bp_pontr_topt_bnd_f_rv = fmax
    kiam.FKIAMToolbox.equationsmodule.vex_kr2bp_pontr_topt_bnd_f_rv = vex
    kiam.FKIAMToolbox.equationsmodule.mass0_kr2bp_pontr_topt_bnd_f_rv = mass0
    kiam.FKIAMToolbox.equationsmodule.t0_kr2bp_pontr_topt_bnd_f_rv = 0.0

    f, jac = kiam.FKIAMToolbox.optimalcontrol.residue_topt(z, 7, 7)

    return f, jac
def objective_r2bp_pontr_time_bnd_f_rv(z: numpy.ndarray, x0: numpy.ndarray, x1: numpy.ndarray, fmax: float, vex: float, mass0: float, mu: float = 1.0, atol: float = 1e-12, rtol: float = 1e-12):
    """
    Scalar objective in boundary value problem derived for the time-optimal control problem.
    Two-body problem, bounded thrust force and fixed exhaust velocity, thrust force as control variable, position-velocity variables.

    Parameters:
    -----------

    `z` : numpy.ndarray, shape (7,)

    Optimization variables. Structure: [px, py, pz, pvx, pvy, pvz, tof], where
    px, py, pz -- conjugate to x, y, z variables, pvx, pvy, pvz -- conjugate to vx, vy, vz variables,
    tof -- time of flight.

    `x0` : numpy.ndarray, shape (6,)

    Initial phase state. Stucture: [x, y, z, vx, vy, vz].

    `x1` : numpy.ndarray, shape (6,)

    Target phase state. Stucture: [x, y, z, vx, vy, vz].

    `fmax` : float

    The maximal thrust force of the engine.

    `vex` : float

    The exhaust velocity.

    `mass0` : float

    The initial mass of spacecraft.

    `mu` : float

    Gravitational parameter. Default: 1.0.

    `atol` : float

    The absolute integration tolerance. Default: 1e-12.

    `rtol` : float

    The relative integration tolerance. Default: 1e-12.

    Returns:
    --------

    `obj` : float

    The squared norm of residue.

    `grad` : numpy.ndarray, shape (7,)

    The gradient of obj, i.e. the derivative of obj wrt optimization variables.

    Examples:
    ---------
    ```
    units = kiam.units('sun')

    x0 = numpy.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])

    x1 = numpy.array([1.5, 0.0, 0.0, 0.0, 1/numpy.sqrt(1.5), 0.0])

    fmax = 14.8e-03 / units['AccUnit']

    vex = 9.3 / units['VelUnit']

    mass0 = 80

    z = numpy.array([0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 2 * numpy.pi])

    obj, grad = optimal.objective_r2bp_pontr_time_bnd_f_rv(z, x0, x1, fmax, vex, mass0)

    print(obj, grad)
    ```
    """
    f, jac = residue_r2bp_pontr_time_bnd_f_rv(z, x0, x1, fmax, vex, mass0, mu, atol, rtol)
    return norm(f)**2, jac.T @ f

# Auxiliary functions
def callback_nelder_mead(x: numpy.ndarray, objective: Callable):
    """
    Auxiliary callback function for the scipy's Nelder-Mead routine.

    `x` : numpy.ndarray, shape (n,)

    Vector of optimization variables.

    `objective` : Callable

    Objective function.

    Returns:
    --------

    Prints the value of the objective funtion at x.

    """
    residue_norm = objective(x)
    print(f'{residue_norm}')
def callback_trust_constr(x: numpy.ndarray, state: Any):
    """
    Auxiliary callback function for the scipy's 'trust-constr' method.

    `x` : numpy.ndarray, shape (n,)

    Vector of optimization variables.

    `state` : Any

    Object that contains information about the current state of the optimization procedure.

    Returns:
    --------

    Prints the iteration number, objective value, constraints violation, and optimality value.

    """
    print('{0:4d}   {1: 3.6e}   {2: 3.6e}   {3: 3.6e}'.format(state.nit, state.fun, state.constr_violation, state.optimality))
def estimate_tof(x0: numpy.ndarray, x1: numpy.ndarray, umax: float, mu: float = 1.0):
    """
    Estimate the time of flight in the low-thrust control problem.

    `x0` : numpy.ndarray, shape (6,)

    Initial phase state. Stucture: [x, y, z, vx, vy, vz].

    `x1` : numpy.ndarray, shape (6,)

    Target phase state. Stucture: [x, y, z, vx, vy, vz].

    `umax` : float

    Maximal thrust control acceleration.

    `mu` : float

    Gravitational parameter. Default: 1.0.

    Returns:
    --------

    `tof` : float

    The estimated time of flight.

    Examples:
    ---------
    ```
    units = kiam.units('Sun')

    x0 = numpy.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])

    x1 = numpy.array([1.5, 0.0, 0.0, 0.0, 1 / numpy.sqrt(1.5), 0.0])

    fmax = 14.8e-03 / units['AccUnit']

    mass0 = 80

    tof = optimal.estimate_tof(x0, x1, fmax / mass0)
    ```
    """
    oe0 = kiam.rv2oe(x0, mu, False)
    oe1 = kiam.rv2oe(x1, mu, False)
    p0 = oe0[0] * (1 - oe0[1] ** 2)
    p1 = oe1[0] * (1 - oe1[1] ** 2)
    tof = (sqrt(mu / p0) - sqrt(mu / p1)) / umax
    return tof

