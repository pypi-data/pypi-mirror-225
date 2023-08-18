"""
Module for signal processing related LazyLinearOps (work in progress).
"""
import numpy as np
import scipy as sp
from lazylinop import *


def kron_eye(shape, k, B, **kwargs):
    """
    Args:
        shape: tuple
        shape of the eye matrix
    """

    Ma, Na = shape[0], shape[1]
    Mb, Nb = B.shape

    # we use kronecker(A, B) @ x = A @ X @ B.T
    #                            = A @ (B @ X.T).T
    # where X is a reshape of the vector x = vec(X)
    # and A an eye matrix of shape (Ma, Na) with k the off-diagonal index
    def _1d(shape, k, B, op):
        if 'complex' in [op.dtype]:
            dtype = 'complex'
        elif 'float' in [op.dtype]:
            dtype = 'float'
        elif 'int' in [op.dtype]:
            dtype = 'int'
        else:
            raise ValueError("invalid dtype.")

        if k == 0:
            # shape of (B @ op.reshape(Na, Nb).T).T is (Na, Mb)
            Y = np.zeros((Ma, Mb), dtype=dtype)
            print("op", op.reshape(Na, Nb).shape)
            print("B", B.shape)
            print("B.T", B.T.shape)
            print(min(Ma, Na))
            mt = op.reshape(Na, Nb)
            print(B)
            print((B @ mt.T).T.shape)
            Y[:min(Ma, Na), :] = ((B @ op.reshape(Na, Nb).T).T)[:min(Ma, Na), :]
            # Y[:min(Ma, Na), :] = (op.reshape(Na, Nb) @ B.T)[:min(Ma, Na), :]
            return Y.ravel()
        elif k > 0:
            if k >= Na:
                raise ValueError("k >= Na.")
            Y = np.zeros((Ma, Mb), dtype=dtype)
            # last k rows disappear
            Y[:min(Ma, Na - k), :] = ((B @ op.reshape(Na, Nb).T).T)[k:, :]
            return Y.ravel()
        else:
            if k <= -Ma:
                raise ValueError("k <= -Ma.")
            Y = np.zeros((Ma, Mb), dtype=dtype)
            # first k rows disappear
            end = min(Ma, Na - k)
            Y[(-k):end, :] = ((B @ op.reshape(Na, Nb).T).T)[:(end - (-k)), :]
            return Y.ravel()

    def _2d(shape, k, B, op):
        if 'complex' in [op.dtype]:
            dtype = 'complex'
        elif 'float' in [op.dtype]:
            dtype = 'float'
        elif 'int' in [op.dtype]:
            dtype = 'int'
        else:
            raise ValueError("invalid dtype.")

        C = op.shape[1]
        Y = np.zeros((Ma * Mb, C), dtype=dtype)

        for c in range(C):
            Y[:, c] = _1d(shape, k, B, op[:, c])
        # if k == 0:
        #     for c in range(C):
        #         Y[:Ma, :Mb, c] = (((B @ op[:, c].reshape(Na, Nb).T).T)[:Ma, :Mb]).ravel()
        # elif k > 0:
        #     for c in range(C):
        #         Y[:(min(Ma, Na) - k), c] = (((B @ op[:, c].reshape(Na, Nb).T).T)[k:min(Ma, Na), :]).ravel()
        # else:
        #     for c in range(C):
        #         print(-k, min(Ma, Na),np.arange(min(Ma, Na) - (-k)))
        #         Y[(-k):min(Ma, Na), :Mb, c] = (((B @ op[:, c].reshape(Na, Nb).T).T)[:(min(Ma, Na) - (-k)), :]).ravel()
        return Y

    return LazyLinearOp(
        shape=(Ma * Mb, Na * Nb),
        matmat=lambda x: (
            _1d(shape, k, B, x) if x.ndim == 1
            else _2d(shape, k, B, x)
        ),
        rmatmat=lambda x : (
            _1d((N, M), -k, B.T.conj(), x) if x.ndim == 1
            else _2d((N, M), -k, B.T.conj(), x)
        )
    )


def eye_test(m: int, n: int=None, k: int=0):

    if k > 0 and n <= k:
        raise ValueError("k > 0 and n <= k")

    if k < 0 and m <= (-k):
        raise ValueError("k < 0 and m <= (-k)")

    if n is None:
        n = m

    def _matmat(x, m, n, k):
        from lazylinop.wip.signal import pad
        mx, nx = x.shape
        if isLazyLinearOp(x):
            if k == 0:
                if m < mx:
                    return x[:m, :]
                else:
                    return pad(x.shape, (0, m - mx)) @ x
            elif k > 0:
                if m < mx:
                    return x[k:, :]
                else:
                    return pad(x.shape, (0, m - mx)) @ x[k:, :]
            else:
                if m < mx:
                    return pad(x.shape, (-k, 0)) @ x[k:m, :]
                else:
                    return pad(x.shape, (-k, m - mx)) @ x[k:m, :]
        else:
            if k == 0:
                if min(m, n) < mx:
                    print("1 k == 0", m, mx)
                    return np.pad(x[:min(m, n), :], ((0, max(0, m - n)), (0, 0)))
                else:
                    print("2 k == 0", m, mx)
                    print(m, x.shape[1], np.pad(x[:min(m, n), :], ((0, m - min(m, n)), (0, 0))).shape)
                    return np.pad(x[:min(m, n), :], ((0, m - min(m, n)), (0, 0)))
            elif k > 0:
                # first k rows disappear
                print("k > 0")
                if m < mx:
                    return x[k:(k + m), :]
                else:
                    return np.pad(x[k:(k + m), :], (0, m - mx))
            else:
                # first k rows disappear
                print("k < 0")
                end = min(m, n - k)
                if m < mx:
                    return np.pad(x[:(end - (-k)), :], ((-k, 0), (0, 0)))
                else:
                    return np.pad(x[:(end - (-k)), :], ((-k, m - mx), (0, 0)))

    return LazyLinearOp(
        shape=(m, n),
        matmat=lambda x: _matmat(x, m, n, k),
        rmatmat=lambda x: _matmat(x, n, m, -k)
    )


def kron_test(A, B, **kwargs):
    """Constructs a Kronecker product lazy linear operator K.
    Kronecker product between matrix A and matrix B is given by:
    .. math::
        \mathbf{A}\bigotimes\mathbf{B} = \begin{pmatrix}
        a_{11}\mathbf{B} & \cdots & a_{1N_A}\mathbf{B}\\
        \vdots & \cdots & \vdots\\
        a_{M_a1}\mathbf{B} & \cdots & a_{M_AN_A}\mathbf{B}\\
        \end{pmatrix}
    If we apply K to a 2d NumPy array, K @ x, it returns
    Kronecker product per column.

    Args:
        A: first matrix
        B: second matrix
        kwargs:
            use_numba: bool
            if yes, use Numba decorator

    Returns:
        LazyLinearOp

    Raises:

    Examples:

    References:
        See also `pylops.Kronecker <https://pylops.readthedocs.io/en/stable/api/generated/pylops.Kronecker.html>`_.
    """

    Ma, Na = A.shape[0], A.shape[1]
    Mb, Nb = B.shape[0], B.shape[1]
    shape = (A.shape[0] * B.shape[0], A.shape[1] * B.shape[1])

    if 'use_numba' in kwargs.keys():
        use_njit = bool(kwargs['use_numba'] == True)
    else:
        use_njit = False

    if use_njit:
        import numba as nb
        from numba import prange, set_num_threads

        @nb.jit(nopython=True, cache=True)
        def _matmul1(A, B):
            Ma, Na = A.shape[0], A.shape[1]
            Mb, Nb = B.shape[0], B.shape[1]
            C = np.full((Ma, Nb), 0.0 * (A[0, 0] + B[0, 0]))
            assert Na == Mb
            for i in range(Ma):
                for j in range(Nb):
                    for k in range(Na):
                        C[i, j] += A[i, k] * B[k, j]
            return C

        @nb.jit(nopython=True, cache=True)
        def _matmul2(A, b):
            # use B such that b = vec(B)
            Ma, Na = A.shape[0], A.shape[1]
            L = b.shape[0]
            assert (L % Na) == 0
            # _matmul2 is A @ mat(b)
            Mb, Nb = Na, L // Na
            C = np.full((Ma, Nb), 0.0 * (A[0, 0] + b[0]))
            for i in range(Ma):
                for j in range(Nb):
                    for k in range(Na):
                        C[i, j] += A[i, k] * b[k * Nb + j]
            return C

        @nb.jit(nopython=True, cache=True)
        def _matmul3(A, b):
            # use B such that b = vec(B)
            Ma, Na = A.shape[0], A.shape[1]
            L = b.shape[0]
            assert (L % Na) == 0
            # _matmul3 is A @ mat(b).T
            Mb, Nb = L // Na, Na
            assert Na == Nb
            C = np.full((Ma, Mb), 0.0 * (A[0, 0] + b[0]))
            for i in range(Ma):
                for j in range(Mb):
                    for k in range(Na):
                        C[i, j] += A[i, k] * b[j * Nb + k]
            return C

        T = nb.config.NUMBA_NUM_THREADS
        O = Na * Mb * Nb + Ma * Na * Mb
        while T > 1 and (O / T) < 100000:
            T -= 1
        T = 1
        use_parallel = bool(T > 1)
        nb.set_num_threads(T)
        # print(Ma, Na, Mb, Nb, nb.get_num_threads(), T, "operations=", O)
        # Numba wants to know if it returns 1d or 2d array ...
        # @nb.jit(nopython=True, parallel=use_parallel, cache=True)
        def _1d(A, B, op):
            Ma, Na = A.shape[0], A.shape[1]
            Mb, Nb = B.shape[0], B.shape[1]
            # we use kronecker(A, B) @ x = A @ X @ B.T
            #                            = A @ (B @ X.T).T
            # where X is a reshape of the vector x = vec(X)
            # return _matmul1(A, _matmul1(B, op.reshape(Na, Nb).T).T).ravel()
            return _matmul1(A, _matmul3(B, op).T).ravel()

        @nb.jit(nopython=True, parallel=use_parallel, cache=True)
        def _2d(A, B, op):
            Ma, Na = A.shape[0], A.shape[1]
            Mb, Nb = B.shape[0], B.shape[1]
            P, Q = op.shape
            output = np.full((Ma * Mb, Q), 0.0 * op[0, 0])
            for q in prange(Q):
                # _matmul3 computes B @ mat(v).T and return a matrix
                output[:, q] = _matmul1(A, _matmul3(B, op[:, q]).T).ravel()
            return output

        return LazyLinearOp(
            shape=shape,
            matmat=lambda x: (
                _1d(A, B, x) if x.ndim == 1
                else _2d(A, B, x)
            ),
            rmatmat=lambda x : (
                _1d(A.T.conj(), B.T.conj(), x) if x.ndim == 1
                else _2d(A.T.conj(), B.T.conj(), x)
            )
        )
    else:
        # we use kronecker(A, B) @ x = A @ X @ B.T
        #                            = A @ (B @ X.T).T
        # where X is a reshape of the vector x = vec(X)
        def _1d(A, B, shape, op):
            Y = A @ (B @ op.reshape(A.shape[1], B.shape[1]).T).T
            return Y.ravel()

        def _2d(A, B, shape, op):
            Y = np.zeros(op.shape)
            for c in range(op.shape[1]):
                Y[:, c] = (A @ (op[:, c].reshape(A.shape[1], B.shape[1]) @ B.T)).ravel()
            return Y

        return LazyLinearOp(
            shape=shape,
            matmat=lambda x: (
                _1d(A, B, shape, x) if x.ndim == 1
                else _2d(A, B, shape, x)
            ),
            rmatmat=lambda x : (
                _1d(A.T.conj(), B.T.conj(), (shape[1], shape[0]), x) if x.ndim == 1
                else _2d(A.T.conj(), B.T.conj(), (shape[1], shape[0]), x)
            )
        )

def khatri_rao(A, B, column: bool=True, **kwargs):
    """Constructs a Khatri-Rao product lazy linear operator K.
    Khatri-Rao product is a column-wize Kronecker product we denotes c*
    while the row-wize product is r*.
    If A and B are two matrices then (A c* B)^T = A^T r* B^T.
    Therefore, we easily get the adjoint of the row-wize Kronecker product.

    Args:
        A: first matrix
        B: second matrix
        column: bool, optional
        compute Khatri-Rao product column-wize (True is default)
        kwargs:
            use_numba: bool
            if yes, use Numba decorator

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            number of rows differs.
        ValueError
            number of columns differs.

    Examples:

    References:
        See also `scipy.linalg.khatri_rao <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.khatri_rao.html>`_.
    """

    Ma, Na = A.shape[0], A.shape[1]
    Mb, Nb = B.shape[0], B.shape[1]

    if not column and Ma != Mb:
        raise ValueError("number of rows differs.")

    if column and Na != Nb:
        raise ValueError("number of columns differs.")

    if column:
        shape = (Ma * Mb, Na)
    else:
        shape = (Ma, Na * Nb)

    if 'use_numba' in kwargs.keys():
        use_njit = bool(kwargs['use_numba'] == True)
    else:
        use_njit = False

    def _1d(A, B, op, column):
        Ma, Na = A.shape[0], A.shape[1]
        Mb, Nb = B.shape[0], B.shape[1]
        if column:
            # we use (A c* B) @ x = vec(B @ diag(x) @ A^T)
            # and a ravel with order='F'
            Y = (B @ np.diag(op) @ A.T).ravel(order='F')
        else:
            # for each row compute product of Kronecker product with a vector
            Y = np.full(Ma, 0.0 * (A[0, 0] + B[0, 0] + op[0]))
            for r in range(Ma):
                Y[r] = A[r, :] @ (B[r, :] @ op.T).T
        return Y

    def _2d(A, B, op, column):
        Ma, Na = A.shape[0], A.shape[1]
        Mb, Nb = B.shape[0], B.shape[1]
        Y = np.full((Ma * Mb if column else Na * Nb, op.shape[1]), 0.0 * (A[0, 0] + B[0, 0] + op[0, 0]))
        if column:
            for i in range(op.shape[1]):
                Y[:, i] = (B @ np.diag(op[:, i]) @ A.T).ravel(order='F')
        else:
            for r in range(Ma):
                for i in range(op.shape[1]):
                    Y[r, i] = A[r, :] @ (B[r, :] @ op[:, i].T).T
        return Y

    # we use (A c* B)^T = A^T r* B^T to compute the adjoint.
    return LazyLinearOp(
        shape=shape,
        matmat=lambda x: (
            _1d(A, B, x, column) if x.ndim == 1
            else _2d(A, B, x, column)
        ),
        rmatmat=lambda x : (
            _1d(A.T.conj(), B.T.conj(), x, not column) if x.ndim == 1
            else _2d(A.T.conj(), B.T.conj(), x, not column)
        )
    )
