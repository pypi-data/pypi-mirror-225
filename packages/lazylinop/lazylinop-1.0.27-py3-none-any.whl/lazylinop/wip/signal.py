"""
Module for signal processing related LazyLinearOps (work in progress).
"""
import numpy as np
import scipy as sp
from lazylinop import *


def fft(n, backend='scipy', **kwargs):
    """
    Returns a LazyLinearOp for the DFT of size n.

    Args:
        backend:
             'scipy' (default) or 'pyfaust' for the underlying computation of the DFT.
        kwargs:
            any key-value pair arguments to pass to the scipy of pyfaust dft backend
            (https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft.html,
            https://faustgrp.gitlabpages.inria.fr/faust/last-doc/html/namespacepyfaust.html#a2695e35f9c270e8cb6b28b9b40458600).

    Example:
        >>> from lazylinop.wip.signal import fft
        >>> import numpy as np
        >>> F1 = fft(32, norm='ortho')
        >>> F2 = fft(32, backend='pyfaust')
        >>> x = np.random.rand(32)
        >>> np.allclose(F1 @ x, F2 @ x)
        True
        >>> y = F1 @ x
        >>> np.allclose(F1.H @ y, x)
        True
        >>> np.allclose(F2.H @ y, x)
        True

    """
    from scipy.fft import fft, ifft

    if backend == 'scipy':
        def scipy_scaling(kwargs):
            if 'norm' in kwargs:
                if kwargs['norm'] == 'ortho':
                    return 1
                elif kwargs['norm'] == 'forward':
                    return 1 / n
                elif kwargs['norm'] == 'backward':
                    return n
                else:
                    raise ValueError('Invalid norm value for scipy backend')
            else: # default is backward
                return n
        lfft = LazyLinearOp(matmat=lambda x: fft(x, axis=0, **kwargs),
                                  rmatmat=lambda x: ifft(x, axis=0, **kwargs) *
                                  scipy_scaling(kwargs), shape=(n, n))
    elif backend == 'pyfaust':
        from pyfaust import dft
        lfft = aslazylinearoperator(dft(n, **kwargs))
    else:
        raise ValueError('backend '+str(backend)+' is unknown')
    return lfft


def fft2(shape, backend='scipy', **kwargs):
    """Returns a LazyLinearOp for the 2D DFT of size n.

    Args:
        shape:
            the signal shape to apply the fft2.
        backend:
            'scipy' (default) or 'pyfaust' for the underlying computation of the 2D DFT.
        kwargs:
            any key-value pair arguments to pass to the `SciPy <https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft2.html>`_
            or `pyfaust <https://faustgrp.gitlabpages.inria.fr/faust/last-doc/html/namespacepyfaust.html#a2695e35f9c270e8cb6b28b9b40458600>`_
            dft backend.

    Example:
        >>> from lazylinop.wip.signal import fft2
        >>> import numpy as np
        >>> F_scipy = fft2((32, 32), norm='ortho')
        >>> F_pyfaust = fft2((32, 32), backend='pyfaust')
        >>> x = np.random.rand(32, 32)
        >>> np.allclose(F_scipy @ x.ravel(), F_pyfaust @ x.ravel())
        True
        >>> y = F_scipy @ x.ravel()
        >>> np.allclose(F_scipy.H @ y, x.ravel())
        True
        >>> np.allclose(F_pyfaust.H @ y, x.ravel())
        True
    """
    s = shape[0] * shape[1]
    if backend == 'scipy':
        from scipy.fft import fft2, ifft2
        return LazyLinearOp(
            (s, s),
            matvec=lambda x: fft2(x.reshape(shape), **kwargs).ravel(),
            rmatvec=lambda x: ifft2(x.reshape(shape), **kwargs).ravel()
        )
    elif backend == 'pyfaust':
        from pyfaust import dft
        K = kron(dft(shape[0], **kwargs), dft(shape[1], **kwargs))
        return LazyLinearOp((s, s), matvec=lambda x: K @ x,
                                  rmatvec=lambda x: K.H @ x)
    else:
        raise ValueError('backend '+str(backend)+' is unknown')


def _binary_dtype(A_dtype, B_dtype):
    if isinstance(A_dtype, str):
        A_dtype = np.dtype(A_dtype)
    if isinstance(B_dtype, str):
        B_dtype = np.dtype(B_dtype)
    if A_dtype is None:
        return B_dtype
    if B_dtype is None:
        return A_dtype
    if A_dtype is None and B_dtype is None:
        return None
    kinds = [A_dtype.kind, B_dtype.kind]
    if A_dtype.kind == B_dtype.kind:
        dtype = A_dtype if A_dtype.itemsize > B_dtype.itemsize else B_dtype
    elif 'c' in [A_dtype.kind, B_dtype.kind]:
        dtype = 'complex'
    elif 'f' in kinds:
        dtype = 'double'
    else:
        dtype = A_dtype
    return dtype

def _is_power_of_two(n: int) -> bool:
    """return True if integer 'n' is a power of two.

    Args:
        n: int

    Returns:
        bool
    """
    return ((n & (n - 1)) == 0) and n > 0


def flip(shape: tuple, start: int = 0, end: int = None, axis: int = 0):
    """Constructs a flip lazy linear operator.

    Args:
        shape: tuple
        shape of the input
        start: int, optional
        flip from start (default is 0)
        end: int, optional
        stop flip (not included, default is None)
        axis: int, optional
        if axis=0 (default) flip per column, if axis=1 flip per row
        it does not apply if shape[1] is None.

    Returns:
        The flip LazyLinearOp

    Raises:
        ValueError
            start is < 0.
        ValueError
            start is > number of elements along axis.
        ValueError
            end is < 1.
        ValueError
            end is > number of elements along axis.
        ValueError
            end is <= start.
        ValueError
            axis is either 0 or 1.
    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.signal import flip
        >>> x = np.arange(6)
        >>> x
        array([0, 1, 2, 3, 4, 5])
        >>> y = flip(x.shape, 0, 5) @ x
        >>> y
        array([4, 3, 2, 1, 0, 5])
        >>> z = flip(x.shape, 2, 4) @ x
        >>> z
        array([0, 1, 3, 2, 4, 5])
        >>> X = np.eye(5, M=5, k=0)
        >>> X
        array([[1., 0., 0., 0., 0.],
               [0., 1., 0., 0., 0.],
               [0., 0., 1., 0., 0.],
               [0., 0., 0., 1., 0.],
               [0., 0., 0., 0., 1.]])
        >>> flip(X.shape, 1, 4) @ X
        array([[1., 0., 0., 0., 0.],
               [0., 0., 0., 1., 0.],
               [0., 0., 1., 0., 0.],
               [0., 1., 0., 0., 0.],
               [0., 0., 0., 0., 1.]])
    """
    N = shape[0]
    A = N
    if len(shape) == 2:
        M = shape[1]
        if axis == 1:
            A = M

    if start < 0:
        raise ValueError("start is < 0.")
    if start > A:
        raise ValueError("start is > number of elements along axis.")
    if not end is None and end < 1:
        raise ValueError("end is < 1.")
    if not end is None and end > A:
        raise ValueError("end is > number of elements along axis.")
    if not end is None and end <= start:
        raise ValueError("end is <= start.")
    if axis != 0 and axis != 1:
        raise ValueError("axis is either 0 or 1.")

    def _matmat(x, start, end, axis):
        if x.ndim == 1:
            y = np.copy(x.reshape(x.shape[0], 1))
            x_is_1d = True
            y[start:end, 0] = x[end - 1 - (np.arange(start, end, 1) - start)]
            return y.ravel()
        else:
            y = np.copy(x)
            x_is_1d = False
            if axis == 0:
                y[start:end, :] = x[end - 1 - (np.arange(start, end, 1) - start), :]
            else:
                y[:, start:end] = x[:, end - 1 - (np.arange(start, end, 1) - start)]
            return y

    return LazyLinearOp(
        shape=(N, N),
        matmat=lambda x: _matmat(x, start, N if end is None else end, axis),
        rmatmat=lambda x: _matmat(x, start, N if end is None else end, axis)
    )


def decimate(shape: tuple, start: int = 0, end: int = None, every: int = 2, axis: int = 0):
    """Constructs a decimation lazy linear operator.
    If the shape of the input array is (N, M) and the axis=0 the operator
    has a shape = ((D + D % every) // every, N) where D = end - start.

    Args:
        shape: tuple
        shape (N, M) of the input
        start: int, optional
        first element to keep, default is 0
        end: int, optional
        stop decimation (not included), default is None
        every: int, optional
        keep element every this number, default is 2
        axis: int, optional
        if axis=0 (default) decimation per column, if axis=1 decimation per row.
        it does not apply if shape[1] is None.

    Returns:
        The decimation LazyLinearOp

    Raises:
        ValueError
            every is < 1.
        ValueError
            axis expects 0 or 1.
        ValueError
            start is < 0.
        ValueError
            end is <= start.
        ValueError
            start is > number of elements along axis.
        ValueError
            end is > number of elements along axis.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.signal import decimate
        >>> x = np.arange(10)
        >>> x
        array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        >>> y = decimate(x.shape, 0, 10, every=2) @ x
        >>> y
        array([0, 2, 4, 6, 8])
        >>> X = np.arange(30).reshape((10, 3))
        >>> X
        array([[ 0,  1,  2],
               [ 3,  4,  5],
               [ 6,  7,  8],
               [ 9, 10, 11],
               [12, 13, 14],
               [15, 16, 17],
               [18, 19, 20],
               [21, 22, 23],
               [24, 25, 26],
               [27, 28, 29]])
        >>> decimate(X.shape, 0, 10, every=2) @ X
        array([[ 0,  1,  2],
               [ 6,  7,  8],
               [12, 13, 14],
               [18, 19, 20],
               [24, 25, 26]])
    """
    if every < 1:
        raise ValueError("every is < 1.")
    if axis != 0 and axis != 1:
        raise ValueError("axis expects 0 or 1.")
    N = shape[0]
    if start < 0:
        raise ValueError("start is < 0.")
    M = 1 if len(shape) == 1 else shape[1]
    if start > (N if axis == 0 else M):
        raise ValueError("start is > number of elements along axis.")
    if not end is None:
        if end > (N if axis == 0 else M):
            raise ValueError("end is > number of elements along axis.")
    if not end is None and end <= start:
        raise ValueError("end is <= start.")

    def _matmat(x, start, end, every, axis):
        D = end - start
        # L = (D + D % every) // every
        L = int(np.ceil(D / every))
        if x.ndim == 1:
            y = np.zeros((L, 1), dtype=x.dtype)
            indices = np.arange(y.shape[0])
            y[indices, 0] = x[start + indices * every]
            return y.ravel()
        else:
            if axis == 0:
                # decimation per column
                y = np.zeros((L, x.shape[1]), dtype=x.dtype)
                indices = np.arange(y.shape[0])
                y[indices, :] = x[start + indices * every, :]
            else:
                # decimation per row
                y = np.zeros((x.shape[0], L), dtype=x.dtype)
                indices = np.arange(y.shape[1])
                # print(x.shape, start + indices * every)
                y[:, indices] = x[:, start + indices * every]
            return y

    def _rmatmat(x, start, end, every, axis):
        if x.ndim == 1:
            y = np.zeros(end, dtype=x.dtype)
            indices = np.arange(x.shape[0])
            y[start + indices * every] = x[indices]
            return y
        else:
            D = end - start
            if axis == 0:
                # decimation per column
                y = np.zeros((end, x.shape[1]), dtype=x.dtype)
                indices = np.arange(x.shape[0])
                y[start + indices * every, :] = x[indices, :]
            else:
                # decimation per row
                y = np.zeros((x.shape[0], end), dtype=x.dtype)
                indices = np.arange(y.shape[1])
                y[:, indices] = x[:, start + indices * every]
            return y

    last = (N if axis==0 else M) if end is None else end
    D = last - start
    # L = (D + D % every) // every
    L = int(np.ceil(D / every))
    return LazyLinearOp(
        shape=(L, N),
        matmat=lambda x: _matmat(x, start, last, every, axis),
        rmatmat=lambda x: _rmatmat(x, start, last, every, axis)
    )


def bc(shape: tuple, n: int=1, boundary='periodic'):
    """Constructs a periodic boundary condition lazy linear operator
    xN, ..., x2, x1 | x1, x2, ..., xN | xN, ..., x2, x1
    or constructs a symmetric boundary condition lazy linear operator.
    x1, x2, ..., xN | x1, x2, ..., xN | x1, x2, ..., xN

    Args:
        shape: tuple
        shape of the array
        n: int, optional
        duplicate signal this number of times on both side
        boundary: str, optional
        boundary condition 'periodic'/'wrap' (default) or 'symmetric'/'symm'

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            n has to be >= 1.
        ValueError
            boundary is either 'periodic' or 'symmetric'.

    Examples:
        >>> from lazylinop.wip.signal import bc
        >>> import numpy as np
        >>> x = np.arange(10)
        >>> x
        >>> LOP = bc(x.shape, n=1, boundary='periodic')
        >>> LOP @ x
        >>> X = np.arange(12).reshape(4, 3)
        >>> X
        >>> LOP = bc(X.shape, n=1, boundary='periodic')
        >>> LOP @ X
        >>> x = np.arange(5)
        >>> x
        array([0, 1, 2, 3, 4])
        >>> LOP = bc(x.shape, n=1, boundary='symmetric')
        >>> LOP @ x
        array([4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 4, 3, 2, 1, 0])
        >>> X = np.arange(12).reshape(4, 3)
        >>> X
        array([[0, 1, 2],
               [3, 4, 5]])
        >>> LOP = bc(X.shape, n=1, boundary='symmetric')
        >>> LOP @ X
        array([[3, 4, 5],
               [0, 1, 2],
               [0, 1, 2],
               [3, 4, 5],
               [3, 4, 5],
               [0, 1, 2]])
    """
    if n < 1:
        raise ValueError("n has to be >= 1.")

    if boundary == 'symmetric' or boundary == 'symm':
        def _matvec(x, n):
            shape = x.shape
            if len(shape) == 1:
                X, Y = shape[0], 1
                x = x.reshape(X, 1)
            else:
                X, Y = shape[0], shape[1]
            y = np.zeros(((n + 1 + n) * X, Y), dtype=x.dtype)
            y[(n * X):((n + 1) * X), :] = x[:X, :]
            for i in range(0, n, 2):
                y[((n - 1 - i) * X):((n - i) * X), :] = x[X - 1 - np.arange(X), :]
                y[((n + 1 + i) * X):((n + 2 + i) * X), :] = x[X - 1 - np.arange(X), :]
            for i in range(1, n, 2):
                y[((n - 1 - i) * X):((n - i) * X), :] = x[:X, :]
                y[((n + 1 + i) * X):((n + 2 + i) * X), :] = x[:X, :]
            if Y == 1:
                return y.ravel()
            else:
                return y

        def _rmatvec(x, n):
            shape = x.shape
            if len(shape) == 1:
                X, Y = shape[0], 1
                x = x.reshape(X, 1)
            else:
                X, Y = shape[0], shape[1]
            y = np.zeros((Y, (n + 1 + n) * X), dtype=x.dtype)
            y[:, (n * X):((n + 1) * X)] = x[:X, :]
            for i in range(0, n, 2):
                y[:, ((n - 1 - i) * X):((n - i) * X)] = x[X - 1 - np.arange(X), :]
                y[:, ((n + 1 + i) * X):((n + 2 + i) * X)] = x[X - 1 - np.arange(X), :]
            for i in range(1, n, 2):
                y[:, ((n - 1 - i) * X):((n - i) * X)] = x[:X, :]
                y[:, ((n + 1 + i) * X):((n + 2 + i) * X)] = x[:X, :]
            if Y == 1:
                return y.ravel()
            else:
                return y

    elif boundary == 'periodic' or boundary == 'wrap':
        def _matvec(x, n):
            shape = x.shape
            if len(shape) == 1:
                X, Y = shape[0], 1
                y = np.zeros(((n + 1 + n) * X, 1), dtype=x.dtype)
                for i in range(n + 1 + n):
                    y[(i * X):((i + 1) * X), 0] = x[:X]
                return y.ravel()
            else:
                X, Y = shape[0], shape[1]
                y = np.zeros(((n + 1 + n) * X, X), dtype=x.dtype)
                for i in range(n + 1 + n):
                    y[(i * X):((i + 1) * X), :] = x[:X]
                return y

        def _rmatvec(x, n):
            shape = x.shape
            if len(shape) == 1:
                X, Y = shape[0], 1
                y = np.zeros((1, (n + 1 + n) * X), dtype=x.dtype)
                for i in range(n + 1 + n):
                    y[0, (i * X):((i + 1) * X)] = x[:X]
                return y.ravel()
            else:
                X, Y = shape[0], shape[1]
                y = np.zeros((X, (n + 1 + n) * X), dtype=x.dtype)
                for i in range(n + 1 + n):
                    y[:, (i * X):((i + 1) * X)] = x[:X]
                return y

    else:
        raise ValueError("boundary is either 'periodic' ('wrap') or 'symmetric' (symm).")

    return LazyLinearOp(
        shape=((n + 1 + n) * shape[0], shape[0]),
        matvec=lambda x: _matvec(x, n),
        rmatvec=lambda x: _rmatvec(x, n)
    )


def _dwt(hfilter: np.ndarray, lfilter: np.ndarray, mode: str = 'zero', level: int = -1, **kwargs):
    """Constructs Discrete Wavelet Transform (DWT) as lazy linear operator.
    Because of the decomposition, the size of the data has to be a power of 2.

    Args:
        hfilter:
            np.ndarray, quadratic mirror high-pass filter
        lfilter:
            np.ndarray, quadratic mirror low-pass filter
        mode:
            str, optional, see pywavelet documentation for more details, zero is default
        level:
            int, decomposition level, by default (level < 0) return all
        kwargs:
            in1:
                np.ndarray, input array
            shape:
                tuple, shape of the input array
            implementation:
                int, 0 or anything


    Returns:
        The DWT LazyLinearOp.

    Raises:
        ValueError
            function expects in1 or shape argument but not both.
        ValueError
            function expects in1 or shape argument.
        ValueError
            first dimension of the input is not a power of two.
        ValueError
            second dimension of the input is not a power of two.
    """
    if 'in1' in kwargs.keys() and 'shape' in kwargs.keys():
        raise ValueError("function expects in1 or shape argument but not both.")
    if not ('in1' in kwargs.keys() or 'shape' in kwargs.keys()):
        raise ValueError("function expects in1 or shape argument.")
    use_1d, use_2d, implementation = False, False, 1
    for key, value in kwargs.items():
        if key == 'in1':
            shape = value.shape
            use_1d = bool(in1.ndim == 1)
            use_2d = bool(in1.ndim == 2)
        elif key == 'shape':
            shape = value
            use_1d = bool(not shape[0] is None and shape[1] is None)
            use_2d = bool(not shape[0] is None and not shape[1] is None)
        elif key == 'implementation':
            implementation = value
        else:
            pass
    N = shape[0]
    if not _is_power_of_two(N):
        raise ValueError("first dimension of the input is not a power of two.")
    if not shape[1] is None:
        if not _is_power_of_two(shape[1]):
            raise ValueError("second dimension of the input is not a power of two.")
    if use_1d:
        # because of the decomposition the size
        # of the input has to be a power of 2^k
        K = int(np.log2(N))
        # first iteration of hih-pass and low-pass filters + decimation
        # return vertical stack of high-pass and low-pass filters lazy linear operator
        D = K if level < 1 else min(K, level)
        A = eye(N, n=N, k = 0)
        M = [N]
        for i in range(D):
            # low-pass filter
            G = convolveND((M[i], ), lfilter, mode='same', boundary='fill', method='lazy.scipy.signal.convolve')
            # high-pass filter
            H = convolveND((M[i], ), hfilter, mode='same', boundary='fill', method='lazy.scipy.signal.convolve')
            # decimation and vertical stack (pywavelet starts from 1)
            if False:
                GH = vstack((G[1::2, :], H[1::2, :]))
            else:
                GH = vstack((decimation(G.shape, 1, None, 2) @ G, decimation(H.shape, 1, None, 2) @ H))
            if i == 0:
                # first level of decomposition
                # apply low and high-pass filters to the signal
                A = GH @ A
            else:
                # second and higher levels of decomposition
                # do not apply to the result of the high-pass filter
                tmp_eye = eye(N - M[i], n=N - M[i], k=0)
                # low-pass filter output goes through low-pass and high-pass filters
                # it corresponds to a lazy linear operator (second level of decomposition):
                # (GH 0) @ (G) @ input
                # (0 Id)   (H)
                A = block_diag(*[GH, tmp_eye], mt=True) @ A
            M.append(M[i] // 2)
        return A
    if use_2d:
        # TODO: does not work for decomposition level > 1.
        if implementation == 0:
            # image has been flattened (with img.flatten(order='C'))
            # the result is vec = (row1, row2, ..., rowR) with size = R * C
            # number of rows, columns
            R, C = shape[0], shape[1]
            # low-pass filter for each row + decimation
            # result is vec = (gdrow1, gdrow2, ..., gdrowR)
            G = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C, ), filters = "low"))
            # high-pass filter for each row + decimation
            # result is vec = (hdrow1, hdrow2, ..., hdrowR)
            H = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C, ), filters = "high"))
            # now we work on the columns
            # from 'C' order to 'F' order
            G = C_to_F_flatten((R, C // 2)) @ G
            H = C_to_F_flatten((R, C // 2)) @ H
            # low-pass for each column of the result of the previous low-pass filter
            GG = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C // 2, ), filters = "low")) @ G
            # high-pass for each column of the result of the previous low-pass filter
            HG = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C // 2, ), filters = "high")) @ G
            # low-pass for each column of the result of the previous high-pass filter
            GH = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C // 2, ), filters = "low")) @ H
            # high-pass for each column of the result of the previous high-pass filter
            HH = kron(eye(R, n=R, k=0), _dwt_qmf_decimation(hfilter, lfilter, (C // 2, ), filters = "high")) @ H
            # from 'F' order to 'C' order
            GG = C_to_F_flatten((C // 2, R // 2)) @ GG
            HG = C_to_F_flatten((C // 2, R // 2)) @ HG
            GH = C_to_F_flatten((C // 2, R // 2)) @ GH
            HH = C_to_F_flatten((C // 2, R // 2)) @ HH
        else:
            # image has been flattened (with img.flatten(order='C'))
            # the result is vec = (row1, row2, ..., rowR) with size = R * C
            # number of rows, columns
            R, C = shape[0], shape[1]
            # low-pass filter for each row + decimation
            # high-pass filter for each row + decimation
            # first work on the row ...
            G = _dwt_qmf_decimation(hfilter, lfilter, (C, ), filters = "low")
            H = _dwt_qmf_decimation(hfilter, lfilter, (C, ), filters = "high")
            GH = vstack((G, H))
            A = kron(GH, GH)
            print(A, R, C)
            # ... and then work on the column
            
        # do we need to do from 'F' order to 'C' order ?
        # return -------
        #        |GG|HG|
        #        -------
        #        |GH|HH|
        #        -------
        # return vstack((hstack((GG, HG)), hstack((GH, HH))))
        # return ----
        #        |GG|
        #        |HG|
        #        |GH|
        #        |HH|
        #        ----
        return vstack((vstack((GG, HG)), vstack((GH, HH))))


def dwt(in1, hfilter: np.ndarray, lfilter: np.ndarray, mode: str = 'zero', level: int = 1) -> list:
    """multiple levels DWT, see _dwt function for more details.
    If in1 is a tuple the function returns a lazy linear operator.
    If in1 is a Numpy array the function returns the result of the DWT.

    Args:
        in1:
            tuple or np.ndarray, shape or array of the input
        hfilter:
            np.ndarray, quadratic mirror high-pass filter
        lfilter:
            np.ndarray, quadratic mirror low-pass filter
        mode:
            str, optional, see pywavelet documentation for more details, zero is default
        level:
            int, optional, decomposition level >= 1, 1 is the default value
            consider only decomposition level <= log2(in1.shape[0])

    Returns:
        [cAn, cDn, cDn-1, ..., cD2, cD1]: list, approximation and detail coefficients

    Raises:
        ValueError
            decomposition level must greater or equal to 1.
        Exception
            in1 expects tuple or np.ndarray.
    """
    if level < 1:
        raise ValueError("decomposition level must be greater or equal to 1.")
    if type(in1) is tuple:
        return _dwt(hfilter, lfilter, mode, 1, shape=in1)
    elif type(in1) is np.ndarray:
        if in1.ndim == 1:
            N = in1.shape[0]
            if level == 1:
                cAcD = _dwt(hfilter, lfilter, mode, 1, N=N) @ in1
                return [cAcD[:(N // 2)], cAcD[(N // 2):]]
            else:
                cAD = _dwt(hfilter, lfilter, mode, level, N=N) @ in1
                # max decomposition level
                K = int(np.log2(N))
                # build list of approximaton and details coefficients
                M = N // np.power(2, level)
                list_cAD = [cAD[:M], cAD[M:(2 * M)]]
                start = 2 * M
                for k in range(min(K, level) - 1 - 1, -1, -1):
                    M *= 2
                    list_cAD.append(cAD[start:(start + M)])
                    start += M
                return list_cAD
        if in1.ndim == 2:
            X, Y = in1.shape
            F = X * Y
            result = _dwt(hfilter, lfilter, mode, 1, shape=in1.shape) @ in1.flatten()
            return (result[:(F // 4)], (result[(F // 4):(2 * F // 4)], result[(2 * F // 4):(3 * F // 4)], result[(3 * F // 4):]))
    else:
        raise Exception("in1 expects tuple or np.ndarray.")


def dwt1d(shape: tuple, hfilter: np.ndarray, lfilter: np.ndarray, boundary: str = 'zero', level: int = None):
    """Constructs a Discrete Wavelet Transform (DWT) lazy linear operator.
    Because of the decomposition, the size of the data has to be a multiple of 2.
    If the lazy linear operator is applied to a 1d array it returns the array [cA, cD]
    for the first decomposition level and the array [cAn, cDn, cDn-1, ..., cD2, cD1] for the nth levels.
    Of note, the function follows the format returned by Pywavelets module.
    You can extract the approximation and details coefficients with the `dwt1d_coeffs` function.

    Args:
        shape: tuple
        shape of the input array
        hfilter: np.ndarray
        quadrature mirror high-pass filter
        lfilter: np.ndarray
        quadrature mirror low-pass filter
        boundary: str, optional
        zero, signal is padded with zeros (default)
        symmetric, use mirroring to pad the signal
        periodic, signal is treated as periodic signal
        level: int, optional
        decomposition level, by default (None) return all

    Returns:
        The DWT LazyLinearOp.

    Raises:
        ValueError
            shape expects tuple.
        ValueError
            first dimension is not a multiple of 2.
        ValueError
            second dimension is not a multiple of 2.
        ValueError
            decomposition level must be greater or equal to 1.
        ValueError
            boundary is either 'zero', 'symmetric' or 'periodic'.
        ValueError
            level is greater than the maximum decomposition level.

    References:
        See also `Pywavelets module <https://pywavelets.readthedocs.io/en/latest/ref/dwt-discrete-wavelet-transform.html#pywt.wavedec>`_
    """
    if not type(shape) is tuple:
        raise ValueError("shape expects tuple.")
    if level < 1:
        raise ValueError("decomposition level must be greater or equal to 1.")
    if not boundary in ['zero', 'symmetric', 'periodic']:
        raise ValueError("boundary is either 'zero', 'symmetric' or 'periodic'.")

    if (shape[0] % 2) != 0:
        raise ValueError("first dimension is not a multiple of 2.")
    if len(shape) == 2:
        if (shape[1] % 2) != 0:
            raise ValueError("second dimension is not a multiple of 2.")

    # maximum decomposition level
    N = shape[0]
    bufferN, K = N, 0
    while (bufferN % 2) == 0:
        bufferN = bufferN // 2
        K += 1
    if level > K:
        raise ValueError("level is greater than the maximum decomposition level.")
    D = K if level is None else level

    # add X signal before and after
    X = 2

    # first iteration of hih-pass and low-pass filters + decimation
    # return vertical stack of high-pass and low-pass filters lazy linear operator
    if boundary == 'symmetric':
        # tmp_eye = eye(N, n=N, k=0)
        # tmp_flip = flip(shape, start=0, end=None)
        # A = vstack((tmp_flip, vstack((tmp_eye, tmp_flip))))
        A = bc((N, ), n=X, boundary='symmetric')
    elif boundary == 'periodic':
        # tmp_eye = eye(N, n=N, k=0)
        # A = vstack((tmp_eye, vstack((tmp_eye, tmp_eye))))
        A = bc((N, ), n=X, boundary='periodic')
    else:
        A = eye(N, n=N, k=0)
    Nm = A.shape[0]
    M = [Nm]
    for i in range(D):
        # low-pass filter
        G = convolve((M[i], ), lfilter, mode='same', method='lazylinop.scipy.signal.convolve')
        # high-pass filter
        H = convolve((M[i], ), hfilter, mode='same', method='lazylinop.scipy.signal.convolve')
        # decimation and vertical stack (pywavelet starts from 1)
        if False:
            GH = vstack((G[1::2, :], H[1::2, :]))
        else:
            GH = vstack((decimate(G.shape, 1, None, 2) @ G, decimate(H.shape, 1, None, 2) @ H))
        if i == 0:
            # first level of decomposition
            # apply low and high-pass filters to the signal
            A = GH @ A
        else:
            # second and higher levels of decomposition
            # do not apply to the result of the high-pass filter
            E = eye(Nm - M[i], n=Nm - M[i], k=0)
            # low-pass filter output goes through low-pass and high-pass filters
            # for second level of decomposition it corresponds to a lazy linear operator like:
            # (GH 0) @ (G) @ input
            # (0 Id)   (H)
            A = block_diag(*[GH, E], mt=True) @ A
        M.append(M[i] // 2)
    return A


def dwt1d_coeffs(in1: np.ndarray, boundary: str = 'zero', level: int = None):
    """Returns approximation and details coefficients of Discrete-Wavelet-Transform.
    first level: [cA, cD]
    nth level  : [cAn, cDn, cDn-1, ..., cD2, cD1]
    Of note, the function follows the format returned by Pywavelets module.

    Args:
        in1: np.ndarray
        input array (result of `dwt1d @ signal`)
        mode: str, optional
        zero, signal is padded with zeros (default)
        symmetric, use mirroring to pad the signal
        periodic, signal is treated as periodic signal
        level: int, optional
        decomposition level, by default (None) return all

    Returns:
        first level: list [cA, cD]
        nth level: list [cAn, cDn, cDn-1, ..., cD2, cD1] of approximation and detail coefficients
        TODO in1 is 2d input array:
        it follows Pywavelets format

    Raises:
        ValueError
            in1 expects np.ndarray.
        ValueError
            first dimension is not a multiple of 2.
        ValueError
            second dimension is not a multiple of 2.
        ValueError
            decomposition level must be greater or equal to 1.
        ValueError
            boundary is either 'zero', 'symmetric' or 'periodic'.
        ValueError
            level is greater than the maximum decomposition level.

    References:
        See also `Pywavelets module <https://pywavelets.readthedocs.io/en/latest/ref/dwt-discrete-wavelet-transform.html#pywt.wavedec>`_
    """
    if not type(in1) is np.ndarray:
        raise ValueError("in1 expects np.ndarray.")
    if level < 1:
        raise ValueError("decomposition level must be greater or equal to 1.")
    if not boundary in ['zero', 'symmetric', 'periodic']:
        raise ValueError("mode is either 'zero', 'symmetric' or 'periodic'.")

    shape = in1.shape

    if (shape[0] % 2) != 0:
        raise ValueError("first dimension is not a multiple of 2.")
    if len(shape) == 2:
        if (shape[1] % 2) != 0:
            raise ValueError("second dimension is not a multiple of 2.")

    # add X signal before and after
    if boundary == 'symmetric' or boundary == 'periodic':
        X = 2
        N = shape[0] // (2 * X + 1)
    else:
        X = 1
        N = shape[0]

    # maximum decomposition level
    bufferN, K = N, 0
    while (bufferN % 2) == 0:
        bufferN = bufferN // 2
        K += 1
    if level > K:
        raise ValueError("level is greater than the maximum decomposition level.")
    D = K if level is None else level

    # first iteration of hih-pass and low-pass filters + decimation
    # return vertical stack of high-pass and low-pass filters lazy linear operator
    if boundary == 'symmetric' or boundary == 'periodic':
        Nm = shape[0]
    else:
        Nm = N

    sm = Nm // 2
    if level == 1:
        return [in1[(sm - N // 2):sm], in1[sm:(sm + N // 2)]]
    else:
        # decomposition level > 1
        # list [cAn, cDn, cDn-1, ..., cD2, cD1] of approximaton and details coefficients
        cAD = [None] * (level + 1)
        M = N
        # list [cDn, cDn-1, ..., cD2, cD1] of details coefficients
        for k in range(level):
            cAD[level - k] = in1[sm:(sm + M // 2)]
            M = N // np.power(2, k + 1)
            sm = (Nm // 2) // np.power(2, k + 1)
        # add cAn at the beginning of the cAD list
        cAD[0] = in1[0:(N // np.power(2, level))]
        return cAD


def convToeplitz(c1: np.ndarray, r1: np.ndarray, K: int = None, **kwargs):
    """Constructs triangular Toeplitz matrix as lazy linear operator
    that will be used in the computation of the convolution of a kernel with a signal.
    Shape of the lazy linear operator is computed from c1 and r1.

    Args:
        c1: np.ndarray
        first column of the Toeplitz matrix, shape is (R, )
        r1: np.ndarray
        first row of the Toeplitz matrix, shape is (C, )
        if r1 is not zero considers c1 to be zero except first element c1[0] = r1[0]
        K: int, optional
        size of the kernel, if None (default) size is c1.shape[0]
        because of the padding, c1 might be larger than the size of the kernel.
        kwargs:
            use_numba: bool
                if yes, use Numba decorator

    Returns:
        The triangular Toeplitz LazyLinearOp
    """
    if 'use_numba' in kwargs.keys():
        _disable_numba = bool(kwargs['use_numba'] == False)
    else:
        _disable_numba = True

    import numba as nb
    from numba import prange, set_num_threads, threading_layer
    nz = max(np.count_nonzero(c1), np.count_nonzero(r1))
    T = nb.config.NUMBA_NUM_THREADS
    while T > 1 and (c1.shape[0] * nz) < (2 * T * 100000):
        T -= 1
    use_parallel = bool(T > 1)
    nb.config.DISABLE_JIT = int(_disable_numba)
    nb.config.THREADING_LAYER = 'omp'
    # print(T, nb.config.DISABLE_JIT, use_parallel)

    # matrix-vector product
    if _disable_numba:
        def _matvec(x, c1: np.ndarray, r1: np.ndarray) -> np.ndarray:
            # number of rows and columns (shape of Toeplitz matrix)
            R, C = c1.shape[0], r1.shape[0]
            nzr = np.count_nonzero(r1)
            if nzr > int(r1[0] != 0.0):
                # find the index 'sz' such that r1[i >= sz] = 0
                # all the elements with index greater or equal to 'sz' are zero
                if not K is None and K > 0:
                    sz = K
                else:
                    sz = 0
                    for c in range(C):
                        nzr -= int(r1[c] != 0.0)
                        if nzr == 0:
                            sz = c + 1
                            break
                # print(r1[sz - 1], r1[sz], r1[sz + 1])
                mv = np.full(R, 0.0 * r1[0])
                fr1 = r1[:sz]
                rmax = max(0, min(R, C - sz))
                L = min(R, C)
                if rmax > 0:
                    mv[:rmax] = x[np.arange(0, rmax, 1)[:, None] + np.arange(0, sz, 1)] @ fr1
                for r in range(rmax, L, 1):
                    end = 0 + sz - min(0, (C - sz) - r)
                    xend = min(x.shape[0], r + end - 0)
                    mv[r] = fr1[0:end] @ x[r:xend]
            else:
                # find the index 'sz' such that c1[i >= sz] = 0
                # all the elements with index greater or equal to 'sz' are zero
                if not K is None and K > 0:
                    sz = K
                else:
                    nzc = np.count_nonzero(c1)
                    sz = 0
                    for r in range(R):
                        nzc -= int(c1[r] != 0.0)
                        if nzc == 0:
                            sz = r + 1
                            break
                # print(R, sz, c1[sz - 1], c1[sz], c1[sz + 1])
                mv = np.full(R, 0.0 * c1[0])
                fc1 = np.flip(c1[:sz])
                # numpy broadcasting
                middle = min(R, C) - sz
                if middle > 0:
                    mv[sz:(sz + middle)] = x[np.arange(0, middle, 1)[:, None] + np.arange(1, sz + 1, 1)] @ fc1
                    l1 = list(range(sz)) + list(range(middle, min(R, sz + C - 1)))
                else:
                    l1 = np.arange(min(R, sz + C - 1))
                # no numpy broadcasting
                for r in l1:
                    start = max(0, (sz - 1) - r)
                    end = sz + min(0, C - (r + 1))
                    xend = min(C, r + 1)
                    xstart = max(0, xend - (end - start))
                    mv[r] = np.dot(fc1[start:end], x[xstart:xend])
            return mv
    else:
        @nb.jit(nopython=True, parallel=use_parallel, cache=True)
        def _matvec(x, c1: np.ndarray, r1: np.ndarray) -> np.ndarray:
            # number of rows and columns (shape of Toeplitz matrix)
            R, C = c1.shape[0], r1.shape[0]
            nzr = 0
            for c in range(C):
                nzr += int(r1[c] != 0.0)
            if nzr > int(r1[0] != 0.0):
                # find the index 'sz' such that r1[i >= sz] = 0
                # all the elements with index greater or equal to 'sz' are zero
                if not K is None and K > 0:
                    sz = K
                else:
                    sz = 0
                    for c in range(C):
                        nzr -= int(r1[c] != 0.0)
                        if nzr == 0:
                            sz = c + 1
                            break
                # print(r1[sz - 1], r1[sz], r1[sz + 1])
                mv = np.full(R, 0.0 * r1[0])
                fr1 = r1[:sz]
                rmax = max(0, min(R, C - sz))
                L = min(R, C)
                RperT = int(np.ceil(L / T))
                for t in prange(T):
                    for r in range(t * RperT, min(L, (t + 1) * RperT), 1):
                        for c in range(0, 0 + sz - min(0, (C - sz) - r), 1):
                            mv[r] += fr1[c] * x[r + c - 0]
            else:
                # find the index 'sz' such that c1[i >= sz] = 0
                # all the elements with index greater or equal to 'sz' are zero
                if not K is None and K > 0:
                    sz = K
                else:
                    nzc = 0
                    for r in range(R):
                        nzc += int(c1[r] != 0.0)
                    sz = 0
                    for r in range(R):
                        nzc -= int(c1[r] != 0.0)
                        if nzc == 0:
                            sz = r + 1
                            break
                # print(R, sz, c1[sz - 1], c1[sz], c1[sz + 1])
                mv = np.full(R, 0.0 * c1[0])
                fc1 = np.full(sz, 0.0 * c1[0])
                for r in range(sz):
                    fc1[r] = c1[sz - 1 - r]
                RperT = int(np.ceil(R / T))
                start = np.full(T, 0)
                end = np.full(T, 0)
                xstart = np.full(T, 0)
                xend = np.full(T, 0)
                for t in prange(T):
                    for r in range(t * RperT, min(R, (t + 1) * RperT), 1):
                        start[t] = max(0, (sz - 1) - r)
                        end[t] = sz + min(0, C - (r + 1))
                        xend[t] = min(C, r + 1)
                        xstart[t] = max(0, xend[t] - (end[t] - start[t]))
                        for c in range(start[t], end[t], 1):
                            mv[r] += fc1[c] * x[xstart[t] + c - start[t]]
            return mv

    return LazyLinearOp(
        shape=(c1.shape[0], r1.shape[0]),
        matvec=lambda x: _matvec(x, c1, r1),
        rmatvec=lambda x: _matvec(x, r1, c1)
    )


def fft_2radix(N: int, **kwargs):
    """Constructs a FFT lazy linear operator using radix-2 FFT algorithm.

    Args:
        N: int
        signal length (N = 2 ** k)
        kwargs:
            use_numba: bool
            if yes, use Numba decorator

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            signal length is not a power of 2.
    """
    if not _is_power_of_two(N):
        raise ValueError("signal length is not a power of 2.")

    if 'use_numba' in kwargs.keys():
        _disable_numba = bool(kwargs['use_numba'] == False)
    else:
        _disable_numba = True

    if N == 1:
        return LazyLinearOp(
            shape=(1, 1),
            matvec=lambda x: x,
            rmatvec=lambda x: x
        )
    else:
        # recursively compute FFT
        import numba as nb
        from numba import prange, set_num_threads, threading_layer
        nb.config.DISABLE_JIT = int(_disable_numba)
        nb.config.THREADING_LAYER = 'omp'
        if _disable_numba:
            nb.config.DISABLE_JIT = 1
        @nb.jit(nopython=True, parallel=True, cache=True)
        def _matvec(x, N):
            omegaN = np.exp(-2j * np.pi / N)
            omega = 1.0
            if len(x.shape) == 1:
                x_is_1d = True
                x = x.reshape(x.shape[0], 1)
            else:
                x_is_1d = False
            # decimate
            x_even = fft_2radix(x.shape[0] // 2) @ decimate(x.shape, 0, None, 2) @ x
            x_odd = fft_2radix(x.shape[0] // 2) @ decimate(x.shape, 1, None, 2) @ x
            # TODO: if len(x.shape) == 2
            output = np.full((N, x.shape[1]), 0j)
            T = 8
            NperT = int(np.ceil(N / T))
            if NperT > 1000:
                for t in prange(T):
                    for n in range(t * NperT, (t + 1) * NperT, 1):
                        if n >= N:
                            continue
                        nn = n % (N // 2)
                        output[n, :] = x_even[nn, :] + np.exp(-2j * np.pi * n / N) * x_odd[nn, :]
            else:
                # seq = np.arange(N)
                # mseq = np.mod(seq, N // 2)
                # output[seq, :] = np.add(x_even[mseq, :], np.exp(-2j * np.pi * seq / N).T @ x_odd[mseq, :])
                for n in range(0, N, 2):
                    nn = n % (N // 2)
                    output[n, :] = x_even[nn, :] + omega * x_odd[nn, :]
                    omega *= omegaN
                    nn = (n + 1) % (N // 2)
                    output[n + 1, :] = x_even[nn, :] + omega * x_odd[nn, :]
                    omega *= omegaN
            if x_is_1d:
                return output.ravel()
            else:
                return output
        @nb.jit(nopython=True, parallel=True, cache=True)
        def _rmatvec(x, N):
            omegaN = np.exp(2j * np.pi / N)
            omega = 1.0
            if len(x.shape) == 1:
                x_is_1d = True
                x = x.reshape(x.shape[0], 1)
            else:
                x_is_1d = False
            # decimate
            x_even = fft_2radix(x.shape[0] // 2).T.conj() @ decimate(x.shape, 0, None, 2) @ x
            x_odd = fft_2radix(x.shape[0] // 2).T.conj() @ decimate(x.shape, 1, None, 2) @ x
            # TODO: if len(x.shape) == 2
            output = np.full((N, x.shape[1]), 0j)
            T = 8
            NperT = int(np.ceil(N / T))
            if NperT > 1000:
                for t in prange(T):
                    for n in range(t * NperT, (t + 1) * NperT, 1):
                        if n >= N:
                            continue
                        nn = n % (N // 2)
                        output[n, :] = x_even[nn, :] + np.exp(2j * np.pi * n / N) * x_odd[nn, :]
            else:
                # seq = np.arange(N)
                # mseq = np.mod(seq, N // 2)
                # output[seq, :] = np.add(x_even[mseq, :], np.exp(2j * np.pi * seq / N).T @ x_odd[mseq, :])
                for n in range(0, N, 2):
                    nn = n % (N // 2)
                    output[n, :] = x_even[nn, :] + omega * x_odd[nn, :]
                    omega *= omegaN
                    nn = (n + 1) % (N // 2)
                    output[n + 1, :] = x_even[nn, :] + omega * x_odd[nn, :]
                    omega *= omegaN
            if x_is_1d:
                return output.ravel()
            else:
                return output
        return LazyLinearOp(
            shape=(N, N),
            matvec=lambda x: _matvec(x, N),
            rmatvec=lambda x: _rmatvec(x, N)
        )


def fwht(shape: tuple, normalize: bool = False, backend: str = 'lazylinop'):
    """Constructs a Fast-Walsh-Hadamard-Transform lazy linear operator.
    If shape of the input array is 2d (M, N), use Numba prange for
    parallel computation of the FWHT over the N columns.
    The size of the signal M=2^k has to be a power of two.

    Args:
        shape: tuple
        shape of the input array (M, N)
        normalize: tuple, optional
        normalize at each stage of the FWHT (default is False)
        backend: str, optional
        it can be 'lazylinop' (default), 'pytorch' (wip) or 'scipy'

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            The size of the signal M=2^k has to be a power of two.
        ValueError
            backend argument expects either 'lazylinop', 'pytorch' or 'scipy'.

    Examples:
    >>> import numpy as np
    >>> import scipy as sp
    >>> from lazylinop.wip.signal import fwht
    >>> x = np.random.rand(16)
    >>> y = fwht(x.shape) @ x
    >>> np.allclose(y, sp.linalg.hadamard(x.shape[0]))
    >>> X = np.random.rand(8, 4)
    >>> Y = fwht(X.shape) @ X
    >>> np.allclose(Y, sp.linalg.hadamard(X.shape[0]))
    """

    if len(shape) == 1:
        M, N = shape[0], 1
    else:
        M, N = shape[0], shape[1]

    if not _is_power_of_two(M):
        raise ValueError("The size of the signal M=2^k has to be a power of two.")

    if backend == 'scipy':
        return LazyLinearOp(
            shape=(M, M),
            matvec=lambda x: sp.linalg.hadamard(M) @ x,
            rmatvec=lambda x: sp.linalg.hadamard(M) @ x,
        )
    elif backend == 'pytorch':
        from math import log2, sqrt
        import torch
        def _matmat(x):
            output = torch.Tensor(x)
            xshape = x.shape
            if len(xshape) == 1:
                output = output.unsqueeze(0)
            batch_dim, L = output.shape
            D = int(log2(L))
            H, F = 2, 1
            for d in range(D):
                output = output.view(batch_dim, L // H, H)
                h1, h2 = output[:, :, :F], output[:, :, F:]
                output = torch.cat((h1 + h2, h1 - h2), dim=-1)
                H *= 2
                F = H // 2
            if normalize:
                return (output / pow(2.0, D / 2.0)).view(*xshape)
            else:
                return output.view(*xshape)

        return LazyLinearOp(
            shape=(M, M),
            matvec=lambda x: _matmat(x),
            rmatvec=lambda x: _matmat(x)
        )
    elif backend=='lazylinop':
        if N == 1:
            import numba as nb
            @nb.jit(nopython=True)
            def _matmat(x, M: int, N: int) -> np.ndarray:
                H = 1
                D = int(np.floor(np.log2(M)))
                x = x.reshape(x.size, 1)
                output = np.full(M, 0.0 * x[0, 0])
                for i in range(M):
                    output[i] = x[i, 0]
                for d in range(D):
                    for i in range(0, M, 2 * H):
                        for j in range(i, i + H):
                            tmp1, tmp2 = output[j], output[j + H]
                            output[j] = tmp1 + tmp2
                            output[j + H] = tmp1 - tmp2
                    H *= 2
                # normalization
                if normalize:
                    for i in range(M):
                        output[i] /= np.power(2.0, D / 2)
                return output
        else:
            import numba as nb
            from numba import prange, set_num_threads, threading_layer
            nb.config.DISABLE_JIT = int(N == 1)#int(_disable_numba)
            nb.config.THREADING_LAYER = 'omp'
            T = min(N, nb.config.NUMBA_NUM_THREADS)
            nb.set_num_threads(T)
            @nb.jit(nopython=True, parallel=True, cache=True)
            def _matmat(x, M: int, N: int) -> np.ndarray:
                Hs = np.full(N, 1)
                D = int(np.floor(np.log2(M)))
                output = np.full((M, N), 0.0 * x[0, 0])
                NperT = int(np.ceil(N // T))
                tmp1 = np.full(N, 0.0 * x[0, 0])
                tmp2 = np.full(N, 0.0 * x[0, 0])
                for t in prange(T):
                    for n in range(t * NperT, min(N, (t + 1) * NperT), 1):
                        for i in range(M):
                            output[i, n] = x[i, n]
                        for d in range(D):
                            for i in range(0, M, 2 * Hs[n]):
                                for j in range(i, i + Hs[n]):
                                    tmp1[n] = output[j, n]
                                    tmp2[n] = output[j + Hs[n], n]
                                    output[j, n] = tmp1[n] + tmp2[n]
                                    output[j + Hs[n], n] = tmp1[n] - tmp2[n]
                            Hs[n] *= 2
                # normalization
                if normalize:
                    for i in range(M):
                        output[i, n] /= np.power(2.0, D / 2)
                return output
    else:
        raise ValueError("backend argument expects either 'lazylinop', 'pytorch' or 'scipy'.")

    return LazyLinearOp(
        shape=(M, M),
        matmat=lambda x: _matmat(x, M, N),
        rmatmat=lambda x: _matmat(x, M, N)
    )


def convolve(in1, in2: np.ndarray, mode: str = 'full', method: str = 'lazylinop.scipy.signal.convolve', **kwargs):
    """If shape of the signal has been passed return a lazy linear
    operator that corresponds to the convolution with the kernel.
    If signal has been passed return the convolution result.

    Args:
        in1: tuple or np.ndarray
        shape or array of the input
        in2: np.ndarray
        1d kernel to convolve with the signal, shape is (K, )
        mode: str, optional
            'full' computes convolution (input + padding)
            'valid' computes 'full' mode and extract centered output that does not depend on the padding. 
            'same' computes 'full' mode and extract centered output that has the same shape that the input.
            'circ' computes circular convolution
        method: str, optional
            'auto' use lazy encapsulation of scipy.signal.convolve (optimization and benchmark in progress)
            'direct' direct computation using nested for loops (Numba implementation is work-in-progress)
            'lazylinop.scipy.signal.convolve' (default) to use lazy encapsulation of Scipy.signal convolve function
            'scipy.linalg.toeplitz' to use lazy encapsulation of Scipy implementation of Toeplitz matrix
            'pyfaust.toeplitz' to use pyfaust implementation of Toeplitz matrix
            'lazylinop.convToeplitz' to use Toeplitz for convolution optimization
            'oa' to use lazylinop implementation of overlap-add method
            'scipy.linalg.circulant' use Scipy implementation of circulant matrix (works with mode='circ')
            'scipy.fft.fft' use Scipy implementation of FFT to compute circular convolution (works with mode='circ')
            'pyfaust.circ' use pyfaust implementation of circulant matrix (works with mode='circ')
            'pyfaust.dft' use pyfaust implementation of DFT (works with mode='circ')
        kwargs:
            use_numba: bool
            if yes, use Numba decorator

    Returns:
        LazyLinearOp or np.ndarray

    Raises:
        ValueError
        number of dimensions of the signal and/or the kernel is greater than one.
        ValueError
        mode is either 'full' (default), 'valid', 'same' or 'circ'
        ValueError
        shape or input_array are expected
        ValueError
        size of the kernel is greater than the size of signal.
        ValueError
        method is not in:
             'auto',
             'direct',
             'lazylinop.scipy.signal.convolve',
             'scipy.linalg.toeplitz',
             'pyfaust.toeplitz',
             'lazylinop.convToeplitz',
             'oa',
             'scipy.linalg.circulant',
             'scipy.fft.fft',
             'pyfaust.circ',
             'pyfaust.dft'
        Exception
            in1 expects tuple or np.ndarray.
        ValueError
            method='scipy.linalg.circulant', 'pyfaust.circ', 'scipy.fft.fft' or 'pyfaust.dft' works only with mode='circ'.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.signal import convolve
        >>> import scipy as sp
        >>> signal = np.random.rand(1024)
        >>> kernel = np.random.rand(32)
        >>> c1 = convolve(signal.shape, kernel, mode='same', method='lazylinop.convToeplitz') @ signal
        >>> c2 = convolve(signal.shape, kernel, mode='same', method='pyfaust.toeplitz') @ signal
        >>> c3 = sp.signal.convolve(signal, kernel, mode='same', method='auto')
        >>> np.allclose(c1, c3)
        True
        >>> np.allclose(c2, c3)
        True
        >>> signal = np.random.rand(32768)
        >>> kernel = np.random.rand(48)
        >>> c1 = convolve(signal.shape, kernel, mode='circ', method='scipy.fft.fft') @ signal
        >>> c2 = convolve(signal.shape, kernel, mode='circ', method='pyfaust.dft') @ signal
        >>> c3 = convolve(signal, kernel, mode='same', method='scipy.fft.fft')
        >>> c4 = convolve(signal, kernel, mode='same', method='pyfaust.dft')
        >>> np.allclose(c1, c2)
        True
        >>> np.allclose(c1, c3)
        True
        >>> np.allclose(c1, c4)
        True
    """
    if not mode in ['full', 'valid', 'same', 'circ']:
        raise ValueError("mode is either 'full' (default), 'valid', 'same' or 'circ'.")

    if 'use_numba' in kwargs.keys():
        _disable_numba = bool(kwargs['use_numba'] == False)
    else:
        _disable_numba = True

    methods = [
        'auto',
        'direct',
        'lazylinop.scipy.signal.convolve',
        'scipy.linalg.toeplitz',
        'pyfaust.toeplitz',
        'lazylinop.convToeplitz',
        'oa',
        'scipy.linalg.circulant',
        'scipy.fft.fft',
        'pyfaust.circ',
        'pyfaust.dft'
    ]

    circmethods = [
        'auto',
        'direct',
        'scipy.linalg.circulant',
        'scipy.fft.fft',
        'pyfaust.circ',
        'pyfaust.dft'
    ]

    if mode == 'circ' and not method in circmethods:
        raise ValueError("mode 'circ' expects method to be in " + str(circmethods))

    if mode != 'circ' and (method == 'scipy.linalg.circulant' or method == 'pyfaust.circ' or method == 'scipy.fft.fft' or method == 'pyfaust.dft'):
        raise ValueError("method='scipy.linalg.circulant', 'pyfaust.circ', 'scipy.fft.fft' or 'pyfaust.dft' works only with mode='circ'.")

    # check if signal has been passed to the function
    # check if shape of the signal has been passed to the function
    if type(in1) is tuple:
        return_lazylinop = True
        shape = in1
    elif type(in1) is np.ndarray:
        return_lazylinop = False
        shape = in1.shape
    else:
        raise Exception("in1 expects tuple or np.ndarray.")

    if shape[0] <= 0 or in2.ndim != 1:
        raise ValueError("number of dimensions of the signal and/or the kernel is not equal to 1.")

    K = in2.shape[0]
    S = shape[0]
    if K > S:
        raise ValueError("size of the kernel is greater than the size of the signal.")

    if mode == 'circ':
        compute = 'circ.' + method
    else:
        compute = method

    ckernel = True#bool('complex' in in2.dtype.str)

    if method == 'auto':
        if K < np.log(S):
            compute = 'lazylinop.convToeplitz'
            # compute = 'direct'
        else:
            compute = 'lazylinop.scipy.signal.convolve'
    else:
        compute = method

    # lazy linear operator
    # check which method is asked for
    if compute == 'direct':
        import numba as nb
        from numba import prange, set_num_threads, threading_layer
        nb.config.DISABLE_JIT = int(_disable_numba)
        nb.config.THREADING_LAYER = 'omp'
        @nb.jit(nopython=True, parallel=True, cache=True)
        def _matvec(kernel, signal):
            K = kernel.shape[0]
            S = signal.shape[0]
            O = S + K - 1
            output = np.full(O, 0.0)
            # y[n] = sum(h[k] * s[n - k], k, 0, K - 1)
            T = nb.config.NUMBA_NUM_THREADS
            OperT = (O - O % T) // T + O % T
            if (OperT * K) > 100000:
                for t in prange(T):
                    # i - j >= 0
                    # j     <= i
                    # i - j < S
                    # j     > i - S
                    for i in range(t * OperT, min(O, (t + 1) * OperT), 1):
                        for j in range(
                                min(max(0, i - S + 1), min(K, i + 1)),
                                min(K, i + 1),
                                1
                        ):
                            output[i] += kernel[j] * signal[i - j]# if (i - j) < S else 0.0
            else:
                for i in range(O):
                    maxj = min(K, i + 1)
                    minj = min(max(0, i - S + 1), maxj)
                    for j in range(minj, maxj, 1):
                        output[i] += kernel[j] * signal[i - j]# if (i - j) < S else 0.0
            return output
        @nb.jit(nopython=True, parallel=True, cache=True)
        def _rmatvec(kernel, signal):
            K = kernel.shape[0]
            S = signal.shape[0]
            O = S + K - 1
            output = np.full(O, 0.0)
            # y[n] = sum(h[k] * s[k + n], k, 0, K - 1)
            T = nb.config.NUMBA_NUM_THREADS
            OperT = int(np.ceil(O / T))
            if (OperT * K) > 10000:
                for t in prange(T):
                    for i in range(t * OperT, min(O, (t + 1) * OperT), 1):
                        # j + i < S
                        # j     < S - i
                        for j in range(max(0, min(K, S - i))):
                            output[i] += kernel[j] * signal[j + i]
            else:
                for i in range(O):
                    for j in range(max(0, min(K, S - i))):
                        output[i] += kernel[j] * signal[j + i]
            return output
        LO = LazyLinearOp(
            shape=(S + K - 1, S),
            matvec=lambda x: _matvec(in2, x),
            rmatvec=lambda x: _rmatvec(in2, x)
        )
    elif compute == 'fft_2radix':
        # kernel length K <= signal length S
        Z = 2 * S
        while not _is_power_of_two(Z):
            Z += 1
        fft_kernel = fft_2radix(Z) @ eye(Z, n=K, k=0) @ in2
        tmp_LO = (diag(np.full(Z, 1.0 / Z), k=0) @ fft_2radix(Z).T.conj()) @ diag(fft_kernel, k=0) @ fft_2radix(Z) @ eye(Z, n=S, k=0)
        LO = LazyLinearOp(
            shape=(S + K - 1, S),
            matvec=lambda x: (
                tmp_LO[:(S + K - 1), :S] @ x if 'complex' in [in2.dtype.str, x.dtype.str]
                else np.real(tmp_LO[:(S + K - 1), :S] @ x)
            ),
            rmatvec=lambda x: (
                tmp_LO[:(S + K - 1), :S].T.conj() @ x if 'complex' in [in2.dtype.str, x.dtype.str]
                else np.real(tmp_LO[:(S + K - 1), :S].T.conj() @ x)
            )
        )
    elif compute == 'lazylinop.scipy.signal.convolve' or method == 'auto':
        LO = LazyLinearOp(
            shape=(S + K - 1, S),
            matvec=lambda x: sp.signal.convolve(x, in2, mode='full', method='auto'),
            rmatvec=lambda x: sp.signal.correlate(x, in2, mode='full', method='auto')
        )
    elif compute == 'scipy.linalg.toeplitz':
        LO = LazyLinearOp(
            shape=(S + K - 1, S),
            matvec=lambda x: sp.linalg.toeplitz(np.pad(in2, (0, S - 1)), np.pad([in2[0]], (0, S - 1))) @ x,
            rmatvec=lambda x: (
                sp.linalg.toeplitz(np.pad(in2, (0, S - 1)), np.pad([in2[0]], (0, S - 1))).T.conj() @ x if 'complex' in [x.dtype.str, in2.dtype.str]
                else np.real(sp.linalg.toeplitz(np.pad(in2, (0, S - 1)), np.pad([in2[0]], (0, S - 1))).T.conj() @ x)
            )
        )
    elif compute == 'pyfaust.toeplitz':
        from pyfaust import toeplitz
        iscomplex = 'complex' in in2.dtype.str
        LO = LazyLinearOp(
            shape=(S + K - 1, S),
            matvec=lambda x: (
                toeplitz(np.pad(in2, (0, S - 1)), np.pad([in2[0]], (0, S - 1)), diag_opt=False) @ x if iscomplex or 'complex' in x.dtype.str
                else np.real(toeplitz(np.pad(in2, (0, S - 1)), np.pad([in2[0]], (0, S - 1)), diag_opt=False) @ x)
            ),
            rmatvec=lambda x: (
                toeplitz(np.pad(in2, (0, S - 1)), np.pad([in2[0]], (0, S - 1)), diag_opt=False).T.conj() @ x if iscomplex or 'complex' in x.dtype.str
                else np.real(toeplitz(np.pad(in2, (0, S - 1)), np.pad([in2[0]], (0, S - 1)), diag_opt=False).T.conj() @ x)
            )
        )
    elif compute == 'lazylinop.convToeplitz':
        LO = convToeplitz(np.pad(in2, (0, S - 1)), np.pad([in2[0]], (0, S - 1)), K, **kwargs)
    elif compute == 'oa':
        LO = _oaconvolve(in2, 'full', shape=shape)
    elif 'circ.' in compute:
        tmp_method = method.replace('circ.', '')
        LO = _circconvolve(in2, tmp_method, shape=shape, **kwargs)
    else:
        raise ValueError("method is not in " + str(methods))

    # compute full mode and extract what we need
    dim = {}
    dim['full'] = S + K - 1
    dim['valid'] = S - K + 1
    dim['same'] = S
    dim['circ'] = S
    if mode == 'valid' or mode == 'same':
        # _circconvolve handles mode='circ': do not need to slice
        start = ((S + K - 1) - dim[mode]) // 2
        if return_lazylinop:
            return LO[start:(start + dim[mode]), :S]
        else:
            return LO[start:(start + dim[mode]), :S] @ in1
    else:
        if return_lazylinop:
            return LO
        else:
            return LO @ in1


def _circconvolve(kernel: np.ndarray, method: str = 'auto', **kwargs):
    """This function returns circular convolution.
    Length of the signal and length of the kernel must be the same.
    If shape of the signal has been passed return Lazy Linear Operator
    that corresponds to the convolution with the kernel.
    If signal has been passed return the convolution result.
    The function only considers the first dimension of both kernel and signal.

    Args:
        kernel: np.ndarray
        kernel to use for the convolution
        method: str, optional
            'auto' use lazy encapsulation of scipy.fft fft and ifft functions (optimization and benchmark in progress)
            'direct' direct computation using nested for loops (Numba implementation is work-in-progress)
            'scipy.linalg.circulant' use Scipy implementation of the circulant matrix
            'scipy.fft.fft' use Scipy implementation of the FFT
            'pyfaust.circ' use pyfaust implementation of circulant matrix
            'pyfaust.dft' use pyfaust implementation of DFT
        kwargs:
            shape: tuple
            shape of the signal to convolve with the kernel
            input_array: np.ndarray
            input array to convolve with the kernel
            use_numba: bool
            if yes, use Numba decorator

    Returns:
        LazyLinearOp or np.ndarray

    Raises:
        Exception
        kernel number of dimensions < 1.
        ValueError
        shape or input_array are expected.
        ValueError
        expect shape or input_array not both.
        ValueError
        method is not in ['auto', 'direct', 'scipy.linalg.circulant', 'scipy.fft.fft', 'pyfaust.circ', 'pyfaust.dft'].
        ValueError
        'scipy.fft.fft' and 'pyfaust.dft' methods expect the size of the signal to be a power of 2.
    """
    if not "shape" in kwargs.keys() and not "input_array" in kwargs.keys():
        raise ValueError("'shape' or 'input_array' are expected")
    if "shape" in kwargs.keys() and "input_array" in kwargs.keys():
        raise ValueError("expect 'shape' or 'input_array' not both")

    if 'use_numba' in kwargs.keys():
        _disable_numba = bool(kwargs['use_numba'] == False)
    else:
        _disable_numba = True

    # check if signal has been passed to the function
    # check if shape of the signal has been passed to the function
    return_lazylinop, B = True, 2
    for key, value in kwargs.items():
        if key == "shape":
            return_lazylinop = True
            shape = value
        elif key == "input_array":
            return_lazylinop = False
            shape = value.shape
        else:
            pass

    # keep only the first dimension of the kernel
    if kernel.ndim == 1:
        kernel1d = np.copy(kernel)
    elif kernel.ndim > 1:
        kernel1d = np.copy(kernel[:1])
    else:
        raise Exception("kernel number of dimensions < 1.")

    # size of the kernel
    K = kernel1d.size
    # size of the signal
    S = shape[0]
    # if K != S:
    #     raise ValueError("size of the kernel differs from the size of the signal.")
    if not _is_power_of_two(S) and (method == 'scipy.fft.fft' or method == 'pyfaust.dft'):
        raise ValueError("'scipy.fft.fft' and 'pyfaust.dft' methods expect the size of the signal to be a power of 2.")
    # size of the output
    O = S
    # pad the kernel
    if method == 'pyfaust.dft':
        P = O
        while not _is_power_of_two(P):
            P += 1
        pkernel = np.pad(kernel, (0, P - K), mode='constant', constant_values=0.0)
    else:
        pkernel = np.pad(kernel, (0, O - K), mode='constant', constant_values=0.0)

    if method == 'direct':
        if _disable_numba:
            def _matvec(kernel, signal):
                K = kernel.shape[0]
                S = signal.shape[0]
                O = S
                output = np.full(O, 0.0)
                # y[n] = sum(h[k] * s[n - k mod N], k, 0, K - 1)
                for i in range(O):
                    output[i] = np.dot(kernel, signal[np.mod(np.subtract(i, np.arange(K)), S)])
                return output
            def _rmatvec(kernel, signal):
                K = kernel.shape[0]
                S = signal.shape[0]
                O = S
                output = np.full(O, 0.0)
                # y[n] = sum(h[k] * s[n - k mod N], k, 0, K - 1)
                for i in range(O):
                    output[i] = np.dot(kernel, signal[np.mod(np.add(i, np.arange(K)), S)])
                return output
        else:
            import numba as nb
            from numba import prange, set_num_threads, threading_layer
            nb.config.DISABLE_JIT = int(_disable_numba)
            nb.config.THREADING_LAYER = 'omp'
            @nb.jit(nopython=True, parallel=True, cache=True)
            def _matvec(kernel, signal):
                K = kernel.shape[0]
                S = signal.shape[0]
                O = S
                output = np.full(O, 0.0)
                # y[n] = sum(h[k] * s[n - k mod N], k, 0, K - 1)
                T = nb.config.NUMBA_NUM_THREADS
                OperT = int(np.ceil(O / T))
                if (OperT * K) > 1000:
                    for t in prange(T):
                        for i in range(t * OperT, min(O, (t + 1) * OperT), 1):
                            for j in range(K):
                                output[i] += kernel[j] * signal[np.mod(i - j, S)]
                else:
                    for i in range(O):
                        for j in range(K):
                            output[i] += kernel[j] * signal[np.mod(i - j, S)]
                return output
            @nb.jit(nopython=True, parallel=True, cache=True)
            def _rmatvec(kernel, signal):
                K = kernel.shape[0]
                S = signal.shape[0]
                O = S
                output = np.full(O, 0.0)
                # y[n] = sum(h[k] * s[k + n mod N], k, 0, K - 1)
                T = nb.config.NUMBA_NUM_THREADS
                OperT = int(np.ceil(O / T))
                if (OperT * K) > 10000:
                    for t in prange(T):
                        for i in range(t * OperT, min(O, (t + 1) * OperT), 1):
                            for j in range(K):
                                output[i] += kernel[j] * signal[np.mod(i + j, S)]
                else:
                    for i in range(O):
                        for j in range(K):
                            output[i] += kernel[j] * signal[np.mod(i + j, S)]
                return output
        LO = LazyLinearOp(
            shape=(O, S),
            matvec=lambda x: _matvec(kernel1d, x),
            rmatvec=lambda x: _rmatvec(kernel1d, x)
        )
    elif method == 'scipy.linalg.circulant':
        LO = LazyLinearOp(
            shape=(O, S),
            matvec=lambda x: sp.linalg.circulant(np.pad(kernel, (0, O - K))) @ x,
            rmatvec=lambda x: sp.linalg.circulant(np.pad(kernel, (0, O - K))).T.conj() @ x
        )
    elif method == 'scipy.fft.fft' or method == 'auto':
        # Op @ signal
        # Op = FFT^-1 @ diag(FFT(kernel)) @ FFT
        # Op^H = FFT^H @ diag(FFT(kernel))^H @ (FFT^-1)^H
        # FFT^H equiv FFT^-1
        fft_kernel = sp.fft.fft(pkernel)
        ifft_kernel = sp.fft.ifft(pkernel)
        LO = LazyLinearOp(
            shape=(O, S),
            matvec=lambda x: (
                sp.fft.ifft(fft_kernel * sp.fft.fft(x)) if ckernel or 'complex' in x.dtype.str
                else np.real(sp.fft.ifft(fft_kernel * sp.fft.fft(x)))
            ),
            rmatvec=lambda x: (
                sp.fft.ifft(ifft_kernel * sp.fft.fft(x)) if ckernel or 'complex' in x.dtype.str
                else np.real(sp.fft.ifft(ifft_kernel * sp.fft.fft(x)))
            )
        )
    elif method == 'pyfaust.circ':
        from pyfaust import circ
        LO = LazyLinearOp(
            shape=(O, S),
            matvec=lambda x: (
                circ(pkernel) @ x if 'complex' in [pkernel.dtype.str, x.dtype.str]
                else np.real(circ(pkernel) @ x)
            ),
            rmatvec=lambda x: (
                circ(pkernel).T.conj() @ x if 'complex' in [pkernel.dtype.str, x.dtype.str]
                else np.real(circ(pkernel).T.conj() @ x)
            )
        )
    elif method == 'pyfaust.dft':
        from pyfaust import dft
        norm = False
        fft_kernel = dft(P, normed=norm) @ np.multiply(1.0 / P, pkernel)
        ifft_kernel = dft(P, normed=norm).T.conj() @ np.multiply(1.0 / P, pkernel)
        F = aslazylinearoperator(dft(P, normed=norm))
        LO = LazyLinearOp(
            shape=(P, S),
            matvec=lambda x: (
                F.T.conj() @ diag(fft_kernel) @ F @ eye(P, n=S, k=0) @ x if 'complex' in [pkernel.dtype.str, x.dtype.str]
                else np.real(F.T.conj() @ diag(fft_kernel) @ F @ eye(P, n=S, k=0) @ x)
            ),
            rmatvec=lambda x: (
                eye(P, n=S, k=0) @ F.T.conj() @ diag(fft_kernel).conj() @ F @ x if 'complex' in [pkernel.dtype.str, x.dtype.str]
                else np.real(eye(P, n=S, k=0) @ F.T.conj() @ diag(fft_kernel).conj() @ F @ x)
            )
        )[:O, :]
    else:
        raise ValueError("method is not in ['auto', 'direct', 'scipy.linalg.circulant', 'scipy.fft.fft', 'pyfaust.circ', 'pyfaust.dft']")

    # convolution
    if return_lazylinop:
        # return lazy linear operator
        # keep the middle of full mode (centered)
        start = O // 2 - S // 2
        return LO[start:(start + S), :]
    else:
        # return result of the convolution
        # keep the middle of full mode (centered)
        start = O // 2 - S // 2
        return (LO @ signal)[start:(start + S)]


def _oaconvolve(kernel: np.ndarray, mode: str = 'full', **kwargs):
    """This function implements overlap-add method for convolution.
    If shape of the signal has been passed return Lazy Linear Operator
    that corresponds to the convolution with the kernel.
    If signal has been passed return the convolution result.
    The function only considers the first dimension of both kernel and signal.

    Args:
        kernel: np.ndarray
        kernel to use for the convolution
        mode: str, optional
            'full' computes convolution (input + padding)
            'valid' computes 'full' mode and extract centered output that does not depend on the padding
            'same' computes 'full' mode and extract centered output that has the same shape that the input
            refer to Scipy documentation of scipy.signal.convolve function for more details
        kwargs:
            shape (tuple) of the signal to convolve with kernel
            input_array (np.ndarray) to convolve with kernel, shape is (S, )
            block_size (int) size of the block unit (a power of two)

    Returns:
        LazyLinearOp or np.ndarray

    Raises:
        Exception
        kernel number of dimensions < 1.
        ValueError
        mode is either 'full' (default), 'valid' or 'same'
        ValueError
        shape or input_array are expected
        ValueError
        expect shape or input_array not both.
        ValueError
        block_size argument expects a value that is a power of two.
        ValueError
        block_size must be greater than the kernel size.
        ValueError
        size of the kernel is greater than the size of the signal.
    """
    if not mode in ['full', 'valid', 'same']:
        raise ValueError("mode is either 'full' (default), 'valid' or 'same'")
    if not "shape" in kwargs.keys() and not "input_array" in kwargs.keys():
        raise ValueError("'shape' or 'input_array' are expected")
    if "shape" in kwargs.keys() and "input_array" in kwargs.keys():
        raise ValueError("expect 'shape' or 'input_array' not both.")

    # check if signal has been passed to the function
    # check if shape of the signal has been passed to the function
    return_lazylinop, B = True, 2
    for key, value in kwargs.items():
        if key == "shape":
            return_lazylinop = True
            shape = value
        elif key == "input_array":
            return_lazylinop = False
            shape = value.shape
        elif key == "block_size":
            B = value
            if B <= 0 or not _is_power_of_two(B):
                raise ValueError("block_size argument expects a value that is a power of two.")
        else:
            pass

    # keep only the first dimension of the kernel
    if kernel.ndim == 1:
        kernel1d = np.copy(kernel)
    elif kernel.ndim > 1:
        kernel1d = np.copy(kernel[:1])
    else:
        raise Exception("kernel number of dimensions < 1.")

    # size of the kernel
    K = kernel1d.size
    # size of the signal
    S = shape[0]
    if K > S:
        raise ValueError("size of the kernel is greater than the size of the signal.")
    # size of the output (full mode)
    O = S + K - 1

    # block size B, number of blocks X=S/B
    if not "block_size" in kwargs.keys():
        # no input for the block size: compute a value
        B = K
        while B < min(S, 2 * K) or not _is_power_of_two(B):
            B += 1
    else:
        if B < K:
            raise ValueError("block_size must be greater or equal to the kernel size.")
    # number of blocks
    R = S % B
    X = (S + R) // B

    # create linear operator LO that will be applied to all the blocks
    # LO = ifft(np.diag(fft(kernel)) @ fft(signal))
    # use Kronecker product between identity matrix and LO to apply to all the blocks
    # use pyfaust_multi_pad to pad each block
    # if the size of the signal is S the size of the result is 2*S
    if False:
        norm = False
        from pyfaust import dft
        fft_kernel = dft(2 * B, normed=norm) @ np.multiply(1.0 if norm else 1.0 / (2 * B), np.pad(kernel1d, ((0, 2 * B - K))))
        LO = overlap_add(B, 2 * X) @ kron(
            eye(X, n=X, k=0),
            aslazylinearoperator(dft(2 * B, normed=norm).T.conj()) @ diag(
                fft_kernel, k=0
            ) @ aslazylinearoperator(
                dft(2 * B, normed=norm)
            ) @ eye(2 * B, n=B, k=0)
        )
    else:
        def lazy_fft(N: int):
            LLOp = LazyLinearOp(
                shape=(N, N),
                matvec=lambda x: sp.fft.fft(x),
                rmatvec=lambda x: np.multiply(N, sp.fft.ifft(x))
            )
            return LLOp
        fft_kernel = np.multiply(1.0 / (2 * B), lazy_fft(2 * B) @ eye(2 * B, n=K, k=0) @ kernel1d)
        LO = overlap_add(B, 2 * X) @ kron(
            eye(X, n=X, k=0),
            lazy_fft(2 * B).H @ diag(fft_kernel, k=0) @ lazy_fft(2 * B)
        ) @ multi_pad(B, X)

    # convolution mode
    if mode == 'valid':
        # compute full mode, valid mode returns
        # elements that do not depend on the padding
        extract = S - K + 1
    elif mode == 'same':
        # keep the middle of full mode (centered)
        # and returns the same size that the signal size
        extract = S
        start = O // 2 - extract // 2
    else:
        # compute full mode
        start = 0
        extract = O

    indices = np.arange(start, start + extract, 1)

    if return_lazylinop:
        # return LazyLinearOp or convolution result
        iscomplex = 'complex' in kernel1d.dtype.str
        return LazyLinearOp(
            shape=(indices.size, S),
            matvec=lambda x: LO[indices, :] @ x if iscomplex or 'complex' in x.dtype.str
            else np.real(LO[indices, :] @ x),
            rmatvec=lambda x: LO[indices, :].T.conj() @ x if iscomplex  or 'complex' in x.dtype.str
            else np.real(LO[indices, :].T.conj() @ x)
        )
    else:
        # return result of the convolution
        iscomplex = 'complex' in kernel1d.dtype.str or 'complex' in signal.dtype.str
        return (
            LO[indices, :] @ eye(S + R, n=S, k=0) @ signal if iscomplex
            else np.real(LO[indices, :] @ eye(S + R, n=S, k=0) @ signal)
        )


def multi_pad(L: int, X: int, signal = None):
    """return a lazy linear operator or np.ndarray mp to pad each block of a signal.
    If you apply this operator to a vector of length L * X the output will have a length 2 * L * X.

    Args:
        L: int, block size
        X: int, number of blocks
        signal: np.ndarray, optional
        if signal is numpy array apply overlap-add linear operator (default is None).

    Returns:
        LazyLinearOp or np.ndarray

    Examples:
        >>> from lazylinop.wip.signal import multi_pad
        >>> import numpy as np
        >>> signal = np.full(5, 1.0)
        >>> signal
        array([1., 1., 1., 1., 1.])
        >>> y = multi_pad(1, 5) @ signal
        >>> y
        array([1., 0., 1., 0., 1., 0., 1., 0., 1., 0.])
    """
    mp = np.zeros((2 * X, X))
    indices = np.arange(0, 2 * X, 2)
    mp[indices, np.floor_divide(indices, 2)] = 1
    if type(signal) is np.ndarray:
        return kron(mp, eye(L, n=L, k=0)) @ signal
    else:
        return kron(mp, eye(L, n=L, k=0))


def overlap_add(L: int, X: int, signal = None):
    """return overlap-add linear operator or result of the overlap-add.
    If signal is a numpy array return the result of the matrix-vector product.
    The overlap-add linear operator adds block i > 0 (of size L) with
    block i + 1 (of size L). Of note, block i = 0 (of size L) does not change.

    Args:
        L: int
        block size
        X: int
        number of blocks
        signal: np.ndarray, optional
        if signal is numpy array apply overlap-add linear operator (default is None).

    Returns:
        LazyLinearOp or np.ndarray

    Raises:
        ValueError
        L is strictly positive.
        ValueError
        X is strictly positive.
        ValueError
        number of columns of the linear operator is not equal to the size of the signal.

    Examples:
        >>> from lazylinop.wip.signal import overlap_add
        >>> import numpy as np
        >>> signal = np.full(16, 1.0)
        >>> oa1 = overlap_add(1, 16, None) @ signal
        >>> oa2 = overlap_add(1, 16, signal)
        >>> np.allclose(oa1, oa2)
        True
        >>> oa1
        array([1., 2., 2., 2., 2., 2., 2., 2., 1., 0., 0., 0., 0., 0., 0., 0.])
        >>> oa1 = overlap_add(2, 8, None) @ signal
        >>> oa2 = overlap_add(2, 8, signal)
        >>> np.allclose(oa1, oa2)
        True
        >>> oa1
        array([1., 1., 2., 2., 2., 2., 2., 2., 1., 1., 0., 0., 0., 0., 0., 0.])
    """
    if L <= 0:
        raise ValueError("L is strictly positive.")
    if X <= 0:
        raise ValueError("X is strictly positive.")
    if (X % 2) != 0:
        raise ValueError("number of blocks is not a multiple of 2.")
    if type(signal) is np.ndarray and (X * L) != signal.size:
        raise ValueError("L * X is not equal to the size of the signal.")
    def _matmat(x, L, X):
        rnz = X // 2 + 1
        if x.ndim == 1:
            x_is_1d = True
            y = np.reshape(x, newshape=(x.size, 1))
        else:
            x_is_1d = False
            y = np.copy(x)
        mv = np.full((X, y.shape[1]), 0.0, dtype=y.dtype)
        mv[0, :] = y[0, :]
        # for i in range(1, rnz - 1):
        #     mv[i, :] = y[2 * (i - 1) + 1, :] + y[2 * (i - 1) + 2, :]
        indices = np.arange(1, rnz - 1, 1)
        mv[indices, :] = y[2 * indices - 1, :] + y[2 * indices, :]
        mv[rnz - 1, :] = y[2 * ((rnz - 1) - 1) + 1, :]
        if x_is_1d:
            return mv.ravel()
        else:
            return mv
    if type(signal) is np.ndarray:
        rnz = X // 2 + 1
        oa = np.full((X, X), 0.0)
        oa[0, 0] = 1
        indices = np.arange(1, rnz - 1, 1)
        oa[indices, 2 * indices - 1] = 1
        oa[indices, 2 * indices] = 1
        oa[rnz - 1, 2 * ((rnz - 1) - 1) + 1] = 1
        return aslazylinearoperator(
            kron(
                oa,
                eye(L, n=L, k=0)
            )
        ) @ signal
    else:
        return aslazylinearoperator(
            kron(
                LazyLinearOp(
                    (X, X),
                    matmat=lambda x: _matmat(x, L, X),
                    rmatmat=lambda x: _matmat(x, L, X).T.conj()
                ),
                eye(L, n=L, k=0)
            )
        )


def fft2(shape, backend='scipy', **kwargs):
    """Returns a LazyLinearOp for the 2D DFT of size n.

    Args:
        shape:
             the signal shape to apply the fft2 to.
        backend:
             'scipy' (default) or 'pyfaust' for the underlying computation of the 2D DFT.
        kwargs:
             any key-value pair arguments to pass to the scipy or pyfaust dft backend
                (https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft2.html,
                https://faustgrp.gitlabpages.inria.fr/faust/last-doc/html/namespacepyfaust.html#a2695e35f9c270e8cb6b28b9b40458600).

    Example:

        >>> from lazylinop.wip.signal import fft2
        >>> import numpy as np
        >>> F_scipy = fft2((32, 32), norm='ortho')
        >>> F_pyfaust = fft2((32, 32), backend='pyfaust')
        >>> x = np.random.rand(32, 32)
        >>> np.allclose(F_scipy @ x.ravel(), F_pyfaust @ x.ravel())
        True
        >>> y = F_scipy @ x.ravel()
        >>> np.allclose(F_scipy.H @ y, x.ravel())
        True
        >>> np.allclose(F_pyfaust.H @ y, x.ravel())
        True
    """
    s = shape[0] * shape[1]
    if backend == 'scipy':
        from scipy.fft import fft2, ifft2
        return LazyLinearOp(
            shape=(s, s),
            matvec=lambda x: fft2(x.reshape(shape), **kwargs).ravel(),
            rmatvec=lambda x: ifft2(x.reshape(shape), **kwargs).ravel()
        )
    elif backend == 'pyfaust':
        from pyfaust import dft
        K = kron(dft(shape[0], **kwargs), dft(shape[1], **kwargs))
        return LazyLinearOp(
            shape=(s, s),
            matvec=lambda x: K @ x,
            rmatvec=lambda x: K.H @ x
        )
    else:
        raise ValueError('backend '+str(backend)+' is unknown')


def _is_power_of_two(n: int) -> bool:
    """return True if integer 'n' is a power of two.

    Args:
        n: int

    Returns:
        bool
    """
    return ((n & (n - 1)) == 0) and n > 0


def bc(shape: tuple, n: int=1, boundary: str='periodic'):
    """Constructs a periodic or symmetric boundary condition lazy linear operator.
    If you apply the operator to a 2d array, it will work
    on each column and returns a 2d array.
    Symmetric boundary condition is something like:
    xN, ..., x2, x1 | x1, x2, ..., xN | xN, ..., x2, x1
    while a periodic boundary condition is something like:
    x1, x2, ..., xN | x1, x2, ..., xN | x1, x2, ..., xN

    Args:
        shape: tuple
        shape of the image
        n: int, optional
        duplicate signal this number of times on both side
        boundary: str, optional
        wrap/periodic (default) or symm/symmetric boundary condition

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            n has to be >= 1.
        ValueError
            boundary excepts 'wrap', 'periodic', 'symm' or 'symmetric'.

    Examples:
        >>> from lazylinop.wip.signal import bc
        >>> import numpy as np
        >>> x = np.arange(10)
        >>> x
        >>> LOP = bc(x.shape, n=1, boundary='periodic')
        >>> LOP @ x
        >>> X = np.arange(12).reshape(4, 3)
        >>> X
        >>> LOP = bc(X.shape, n=1, boundary='periodic')
        >>> LOP @ X
        >>> x = np.arange(5)
        >>> x
        array([0, 1, 2, 3, 4])
        >>> LOP = bc(x.shape, n=1, boundary='symmetric')
        >>> LOP @ x
        array([4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 4, 3, 2, 1, 0])
        >>> X = np.arange(12).reshape(4, 3)
        >>> X
        array([[0, 1, 2],
               [3, 4, 5]])
        >>> LOP = bc(X.shape, n=1, boundary='symmetric')
        >>> LOP @ X
        array([[3, 4, 5],
               [0, 1, 2],
               [0, 1, 2],
               [3, 4, 5],
               [3, 4, 5],
               [0, 1, 2]])
    """
    if n < 1:
        raise ValueError("n has to be >= 1.")

    if boundary == 'symmetric' or boundary == 'symm':
        def _matvec(x, n):
            shape = x.shape
            if len(shape) == 1:
                X, Y = shape[0], 1
                x = x.reshape(X, 1)
            else:
                X, Y = shape[0], shape[1]
            y = np.zeros(((n + 1 + n) * X, Y), dtype=x.dtype)
            y[(n * X):((n + 1) * X), :] = x[:X, :]
            for i in range(0, n, 2):
                y[((n - 1 - i) * X):((n - i) * X), :] = x[X - 1 - np.arange(X), :]
                y[((n + 1 + i) * X):((n + 2 + i) * X), :] = x[X - 1 - np.arange(X), :]
            for i in range(1, n, 2):
                y[((n - 1 - i) * X):((n - i) * X), :] = x[:X, :]
                y[((n + 1 + i) * X):((n + 2 + i) * X), :] = x[:X, :]
            if Y == 1:
                return y.ravel()
            else:
                return y

        def _rmatvec(x, n):
            shape = x.shape
            if len(shape) == 1:
                X, Y = shape[0], 1
                x = x.reshape(X, 1)
            else:
                X, Y = shape[0], shape[1]
            y = np.zeros((Y, (n + 1 + n) * X), dtype=x.dtype)
            y[:, (n * X):((n + 1) * X)] = x[:X, :]
            for i in range(0, n, 2):
                y[:, ((n - 1 - i) * X):((n - i) * X)] = x[X - 1 - np.arange(X), :]
                y[:, ((n + 1 + i) * X):((n + 2 + i) * X)] = x[X - 1 - np.arange(X), :]
            for i in range(1, n, 2):
                y[:, ((n - 1 - i) * X):((n - i) * X)] = x[:X, :]
                y[:, ((n + 1 + i) * X):((n + 2 + i) * X)] = x[:X, :]
            if Y == 1:
                return y.ravel()
            else:
                return y

    elif boundary == 'periodic' or boundary == 'wrap':
        def _matvec(x, n):
            shape = x.shape
            if len(shape) == 1:
                X, Y = shape[0], 1
                y = np.zeros(((n + 1 + n) * X, 1), dtype=x.dtype)
                for i in range(n + 1 + n):
                    y[(i * X):((i + 1) * X), 0] = x[:X]
                return y.ravel()
            else:
                X, Y = shape[0], shape[1]
                y = np.zeros(((n + 1 + n) * X, X), dtype=x.dtype)
                for i in range(n + 1 + n):
                    y[(i * X):((i + 1) * X), :] = x[:X]
                return y

        def _rmatvec(x, n):
            shape = x.shape
            if len(shape) == 1:
                X, Y = shape[0], 1
                y = np.zeros((1, (n + 1 + n) * X), dtype=x.dtype)
                for i in range(n + 1 + n):
                    y[0, (i * X):((i + 1) * X)] = x[:X]
                return y.ravel()
            else:
                X, Y = shape[0], shape[1]
                y = np.zeros((X, (n + 1 + n) * X), dtype=x.dtype)
                for i in range(n + 1 + n):
                    y[:, (i * X):((i + 1) * X)] = x[:X]
                return y

    else:
        raise ValueError("boundary is either 'periodic' ('wrap') or 'symmetric' (symm).")

    return LazyLinearOp(
        shape=((n + 1 + n) * shape[0], shape[0]),
        matvec=lambda x: _matvec(x, n),
        rmatvec=lambda x: _rmatvec(x, n)
    )


def bc2d(shape: tuple, n: int=1, boundary: str='periodic'):
    """Constructs a periodic or symmetric boundary condition lazy linear operator.
    It will be applied to a flattened image.
    It basically add image on bottom, left, top and right side.
    Symmetric boundary condition is something like (on both axis):
    xN, ..., x2, x1 | x1, x2, ..., xN | xN, ..., x2, x1
    while a periodic boundary condition is something like (on both axis):
    x1, x2, ..., xN | x1, x2, ..., xN | x1, x2, ..., xN

    Args:
        shape: tuple
        shape of the image
        n: int, optional
        duplicate signal this number of times on both side
        2 * n + 1 is the number of image along both axis.
        boundary: str, optional
        wrap/periodic (default) or symm/symmetric boundary condition

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            n has to be >= 1.
        ValueError
            shape expects tuple (R, C).
        ValueError
            boundary excepts 'wrap', 'periodic', 'symm' or 'symmetric'.

    Examples:
        >>> from lazylinop.wip.signal import bc2d
        >>> import numpy as np
        >>> X = np.arange(4).reshape(2, 2)
        >>> X
        >>> LOP = bc2d(X.shape, n=1, boundary='periodic')
        >>> LOP @ X
        >>> X = np.arange(12).reshape(4, 3)
        >>> X
        >>> LOP = bc(X.shape, n=1, boundary='symmetric')
        >>> LOP @ X
        >>> x = np.arange(5)
        >>> x
        array([0, 1, 2, 3, 4])
        >>> LOP = bc(x.shape, n=1, boundary='symmetric')
        >>> LOP @ x
        array([4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 4, 3, 2, 1, 0])
        >>> X = np.arange(12).reshape(4, 3)
        >>> X
        array([[0, 1, 2],
               [3, 4, 5]])
        >>> LOP = bc(X.shape, n=1, boundary='symmetric')
        >>> LOP @ X
        array([[3, 4, 5],
               [0, 1, 2],
               [0, 1, 2],
               [3, 4, 5],
               [3, 4, 5],
               [0, 1, 2]])
    """
    if n < 1:
        raise ValueError("n has to be >= 1.")
    if len(shape) != 2:
        raise ValueError("shape expects tuple (R, C).")

    # apply boundary condition and get X images
    X = 2 * n + 1

    if 'wrap' in boundary or boundary == 'periodic':
        # periodic boundary condition
        # work on rows and columns
        # use Kronecker product
        A1 = np.full((X, 1), 1.0)
        K1 = kron(A1, eye(shape[0], n=shape[0], k=0))
        A2 = np.full((1, X), 1.0)
        K2 = kron(A2, eye(shape[1], n=shape[1], k=0))
        # kron(K1, K2)^T = kron(K1^T, K2^T)
        # K1^T = kron(A1, E1)^T = kron(A1^T, E1^T)
        # K2^T = kron(A2, E2)^T = kron(A2^T, E2^T)
        # return kron(K1, K2.T)
        LLOp = kron(K1, K2.T)
    elif 'symm' in boundary or boundary == 'symmetric':
        from lazylinop.wip.signal import flip
        # flip along rows and columns
        # use Kronecker product
        # rows
        A1 = np.full((X, 1), 1.0)
        K1 = kron(A1, eye(shape[0], n=shape[0], k=0))
        # flip one image every two images
        # do not flip image at the center
        for i in range(0, (X - 1) // 2, 2):
            K1 = flip(K1.shape, (n - 1 - i) * shape[0], (n - i) * shape[0]) @ K1
            K1 = flip(K1.shape, (n + 1 + i) * shape[0], (n + 2 + i) * shape[0]) @ K1
        # columns
        A2 = np.full((X, 1), 1.0)
        K2 = kron(A2, eye(shape[1], n=shape[1], k=0))
        # flip one image every two images
        # do not flip image at the center
        for i in range(0, (X - 1) // 2, 2):
            K2 = flip(K2.shape, (n - 1 - i) * shape[1], (n - i) * shape[1]) @ K2
            K2 = flip(K2.shape, (n + 1 + i) * shape[1], (n + 2 + i) * shape[1]) @ K2
            # K2 = flip(K2.shape, 0, None) @ K2
            # K2 = flip(K2.shape, 0, None) @ K2
        # return kron(K1, K2)
        LLOp = kron(K1, K2)
    else:
        raise ValueError("boundary excepts either 'wrap', 'periodic', 'symm' or 'symmetric'.")

    return LazyLinearOp(
        shape=LLOp.shape,
        matvec=lambda x: (
            LLOp @ x if 'complex' in x.dtype.str
            else np.real(LLOp @ x)
        ),
        rmatvec=lambda x: (
            LLOp.T.conj() @ x if 'complex' in x.dtype.str
            else np.real(LLOp.T.conj() @ x)
        )
    )


def dwt2d(shape: tuple, hfilter: np.ndarray, lfilter: np.ndarray, boundary: str = 'zero', level: int = None) -> list:
    """Constructs a multiple levels DWT lazy linear operator.

    Args:
        shape: tuple
        shape of the input array (X, Y)
        hfilter: np.ndarray
        quadratic mirror high-pass filter
        lfilter: np.ndarray
        quadratic mirror low-pass filter
        boundary: str, optional
        'zero', signal is padded with zeros (default)
        'periodic', image is treated as periodic image
        'symmetric', use mirroring to pad the signal
        see Pywavelets documentation for more details
        level: int, optional
        if level is None compute full decomposition (default)

    Returns:
        LazyLinearOp

    Raises:
        Exception
            shape expects tuple.
        ValueError
            decomposition level must greater or equal to 1.
        ValueError
            decomposition level is greater than the maximum decomposition level.
        ValueError
            boundary is either 'zero', 'periodic' or 'symmetric'.

    References:
        See also `Pywavelets module <https://pywavelets.readthedocs.io/en/latest/ref/2d-dwt-and-idwt.html#ref-dwt2>`_
    """
    if not type(shape) is tuple:
        raise ValueError("shape expects tuple.")
    if not level is None and level < 1:
        raise ValueError("decomposition level must be greater or equal to 1.")
    
    # image has been flattened (with img.flatten(order='C'))
    # the result is vec = (row1, row2, ..., rowR) with size = X * Y
    # number of rows, columns
    X, Y = shape[0], shape[1]
    XY = X * Y
    # because of the decomposition the size
    # of the input has to be a power of 2
    # compute maximum decomposition level
    bufferX, bufferY = X, Y
    K = 0
    while (bufferX % 2) == 0 and (bufferY % 2) == 0:
        bufferX, bufferY = bufferX // 2, bufferY // 2
        K += 1
    if not level is None and level > K:
        raise ValueError("decomposition level is greater than the maximum decomposition level.")
    D = K if level < 1 else min(K, level)

    # boundary condition
    if boundary == 'zero':
        B = 1
        A = eye(XY, n=XY, k = 0)
    elif boundary == 'periodic':
        # add (B - 1) / 2 images on both sides
        B = 3
        A = bc2d((X, Y), n=(B - 1) // 2, boundary=boundary)
    elif boundary == 'symmetric':
        # add (B - 1) / 2 images on both sides
        B = 5
        A = bc2d((X, Y), n=(B - 1) // 2, boundary=boundary)
    else:
        raise ValueError("boundary is either 'zero', 'periodic' or 'symmetric'.")

    # loop over the decomposition level
    Xs, Ys = [B * X], [B * Y]
    for i in range(D):
        # low and high-pass filters + decimation
        # first work on the row ...
        # ... and then work on the column (use Kronecker product vec trick)
        GCx = convolve((Xs[i], ), lfilter, mode='same', method='lazylinop.scipy.signal.convolve')
        GCy = convolve((Ys[i], ), lfilter, mode='same', method='lazylinop.scipy.signal.convolve')
        HCx = convolve((Xs[i], ), hfilter, mode='same', method='lazylinop.scipy.signal.convolve')
        HCy = convolve((Ys[i], ), hfilter, mode='same', method='lazylinop.scipy.signal.convolve')
        Dx_Op = decimate(GCx.shape, 1, None, 2)
        Dy_Op = decimate(GCy.shape, 1, None, 2)
        # vertical stack
        GHx = vstack((Dx_Op @ GCx, Dx_Op @ HCx))
        GHy = vstack((Dy_Op @ GCy, Dy_Op @ HCy))
        # because we work on the rows and then on the columns we can write a Kronecker product that will be applied to the flatten image
        KGH = kron(GHx, GHy)
        # extract four sub-images
        # -------
        # |LL|HL|
        # -------
        # |LH|HH|
        # -------
        xy = (2 * Xs[i], 1)
        tmp_eye = eye(Ys[i] // 2, n=Ys[i] // 2, k=0)
        LL = kron(decimate(xy, 0, Xs[i], 2), tmp_eye)
        LH = kron(decimate(xy, 1, Xs[i], 2), tmp_eye)
        HL = kron(decimate(xy, Xs[i], 2 * Xs[i], 2), tmp_eye)
        HH = kron(decimate(xy, Xs[i] + 1, 2 * Xs[i], 2), tmp_eye)
        # vertical stack where LL is the first lazy linear operator
        # ----
        # |LL|
        # ----
        # |HL|
        # ----
        # |LH|
        # ----
        # |HH|
        # ----
        # V = eye(KGH.shape[0], n=KGH.shape[0], k=0)
        V = vstack((vstack((LL, HL)), vstack((LH, HH))))
        if i == 0:
            # first level of decomposition
            A = V @ KGH @ A
        else:
            # apply low and high-pass filters + decimation only to LL
            # because of lazy linear operator V, LL always comes first
            tmp_eye = eye(B ** 2 * XY - V.shape[0], n=(B ** 2 * XY - KGH.shape[1]), k=0)
            A = block_diag(*[V @ KGH, tmp_eye]) @ A
        Xs.append(Xs[i] // 2)
        Ys.append(Ys[i] // 2)
    return A


def dwt2d_coeffs(shape: tuple, in1: np.ndarray, boundary: str = 'zero', level: int = None) -> list:
    """Returns approximation, horizontal, vertical and details coefficients of 2d Discrete-Wavelet-Transform.

    Args:
        shape: tuple
        shape of the image (X, Y)
        in1: np.ndarray
        result of dwt2d @ image.flatten()
        boundary: str, optional
        'zero', signal is padded with zeros (default)
        'periodic', image is treated as periodic image
        'symmetric', use mirroring to pad the signal
        see Pywavelets documentation for more details
        level: int, optional
        if level is None compute full decomposition (default)

    Returns:
        [cAn, (cHn, cVn, cDn), ..., (cH1, cV1, cD1)]: list
        approximation, horizontal, vertical and detail coefficients, it follows Pywavelets format.

    Raises:
        Exception
            shape expects tuple (X, Y).
        Exception
            in1 expects np.ndarray.
        ValueError
            decomposition level must greater or equal to 1.
        ValueError
            decomposition level is greater than the maximum decomposition level.
        ValueError
            boundary is either 'zero', 'periodic' or 'symmetric'.

    References:
        See also `Pywavelets module <https://pywavelets.readthedocs.io/en/latest/ref/2d-dwt-and-idwt.html#ref-dwt2>`_
    """
    if not type(shape) is tuple:
        raise Exception("shape expects tuple (X, Y).")
    if not type(in1) is np.ndarray:
        raise Exception("in1 expects np.ndarray.")
    if not level is None and level < 1:
        raise ValueError("decomposition level must be greater or equal to 1.")

    # image has been flattened (with img.flatten(order='C'))
    # the result is vec = (row1, row2, ..., rowR) with size = X * Y
    # number of rows, columns
    X, Y = shape[0], shape[1]
    XY = X * Y
    # because of the decomposition the size
    # of the input has to be a power of 2
    # compute maximum decomposition level
    bufferX, bufferY = X, Y
    K = 0
    while (bufferX % 2) == 0 and (bufferY % 2) == 0:
        bufferX, bufferY = bufferX // 2, bufferY // 2
        K += 1
    if not level is None and level > K:
        raise ValueError("decomposition level is greater than the maximum decomposition level.")
    D = K if level is None else level

    # boundary condition
    if boundary == 'zero':
        B = 1
    elif boundary == 'periodic':
        B = 3
    elif boundary == 'symmetric':
        B = 5
    else:
        raise ValueError("boundary is either 'zero', 'periodic' or 'symmetric'.")

    # np.set_printoptions(edgeitems=10, linewidth=300)
    # print(in1.reshape(B * X, B * Y))
    for i in range(level, 0, -1):
        L = np.power(2, i)
        xx, yy = X // L, Y // L
        iLL = np.arange(yy)
        for j in range(xx - 1):
            iLL = np.append(iLL, np.arange((j + 1) * B * yy, (j + 1) * B * yy + yy))
        iHL = np.add(iLL, B ** 2 * xx * yy)
        iLH = np.add(iHL, B ** 2 * xx * yy)
        iHH = np.add(iLH, B ** 2 * xx * yy)
        if i == level:
            cAHVD = [in1[iLL].reshape(xx, yy)]
        cAHVD.append(
            (
                in1[iHL].reshape(xx, yy),
                in1[iLH].reshape(xx, yy),
                in1[iHH].reshape(xx, yy)
            )
        )
    return cAHVD


def fftconvolve2d(shape: tuple, in2: np.ndarray, backend: str = 'full_scipy'):
    """
    Constructs a lazy linear operator to convolve a kernel and an image of shape (X, Y).

    Args:
        shape: tuple
            the shape of the signal this operator will convolves.
        in2: np.ndarray
             the kernel to convolve.
        backend: str, optional
            'pyfaust' or 'scipy' to use lazylinop.fft2(backend='scipy') or 'full_scipy' to use scipy.signal.convolve2d.

    Returns:
        The LazyLinearOp for the 2D convolution.

    Example:
        >>> import numpy as np
        >>> from lazylinop.wip.image import fftconvolve2d
        >>> from scipy.signal import convolve2d as sconvolve2d
        >>> X = np.random.rand(64, 64)
        >>> K = np.random.rand(4, 4)
        >>> C1 = fftconvolve2d(X.shape, K, backend='scipy')
        >>> C2 = fftconvolve2d(X.shape, K, backend='pyfaust')
        >>> C3 = fftconvolve2d(X.shape, K, backend='full_scipy')
        >>> np.allclose((C1 @ X.ravel()).reshape(64, 64), sconvolve2d(X, K, 'same'))
        True
        >>> np.allclose((C2 @ X.ravel()).reshape(64, 64), sconvolve2d(X, K, 'same'))
        True
        >>> np.allclose((C3 @ X.ravel()).reshape(64, 64), sconvolve2d(X, K, 'same'))
        True
    """
    X, Y = shape[0], shape[1]
    K, L = in2.shape
    P, Q = X + K - 1, Y + L - 1

    if backend == 'full_scipy':
        from scipy.signal import convolve2d as sconvolve2d, correlate2d
        return LazyLinearOp(
            shape=(P * Q, X * Y),
            matvec=lambda x: sconvolve2d(x.reshape(shape), in2, mode).ravel(),
            rmatvec=lambda x: correlate2d(x.reshape(shape), in2, mode).ravel()
        )
    else:
        if backend == 'pyfaust':
            from lazylinop.wip.signal import fft2
            F = fft2((P, Q), backend=backend, normed=True, diag_opt=True)
        elif backend == 'scipy':
            from lazylinop.wip.signal import fft2
            F = fft2((P, Q), backend=backend, norm='ortho')
        else:
            raise ValueError('Unknown backend')

        # operator to pad the flattened image
        # scipy.signal.convolve2d adds 0 only on one side along both axis
        x1 = 0#(P - X) // 2
        x2 = P - X - x1
        y1 = 0#(Q - Y) // 2
        y2 = Q - Y - y1
        P1 = pad((X, Y), ((x1, x2), (y1, y2)))

        # operator to pad the flattened kernel
        # scipy.signal.convolve2d adds 0 only on one side along both axis
        x1 = 0#(P - K) // 2
        x2 = P - K - x1
        y1 = 0#(Q - L) // 2
        y2 = Q - L - y1
        P2 = pad((K, L), ((x1, x2), (y1, y2)))

        Fin2 = np.multiply(np.sqrt(P * Q), F @ P2 @ in2.flatten())

        LLOp = F.H @ (diag(Fin2, k=0) @ F) @ P1

        return LLOp


def convolve2d(in1, in2: np.ndarray, mode: str = 'full', boundary: str = 'fill', method: str = 'fft', **kwargs):
    """Constructs a 2d convolution lazy linear operator.
    If shape of the image has been passed return Lazy Linear Operator.
    If image has been passed return the convolution result.
    Toeplitz based method use the fact that convolution of a kernel with an image
    can be written as a sum of Kronecker product between eye and Toeplitz matrices.

    Args:
        in1: tuple or np.ndarray,
             shape (tuple) of the signal to convolve with kernel.
             input_array (np.ndarray) to convolve with kernel, shape is (X, Y)
        in2: np.ndarray
            kernel to use for the convolution, shape is (K, L)
        mode: str, optional
            'full' computes convolution (input + padding)
            'valid' computes 'full' mode and extract centered output that does not depend on the padding. 
            'same' computes 'full' mode and extract centered output that has the same shape that the input.
            see also Scipy documentation of scipy.signal.convolve function for more details
        boundary: str, optional
            'fill' pads input array with zeros (default)
            'wrap' periodic boundary conditions
            'symm' symmetrical boundary conditions
            see also Scipy documentation of scipy.signal.convolve2d function
        method: str, optional
             'auto' to use the best method according to the kernel and input array dimensions
             'direct' to use nested loops (brute force) and it works with Numba decorators
             'scipy.linalg.toeplitz' to use lazy encapsulation of Scipy implementation of Toeplitz matrix
             'pyfaust.toeplitz' to use pyfaust implementation of Toeplitz matrix
             'lazylinop.convToeplitz' to use Toeplitz for convolution optimization
             'fft' to use Fast-Fourier-Transform to compute convolution
        kwargs:
            use_numba: bool
                if yes, use Numba decorator

    Returns:
        LazyLinearOp or np.ndarray

    Raises:
        ValueError
        mode is either 'full' (default), 'valid' or 'same'.
        ValueError
        boundary is either 'fill' (default), 'wrap' or 'symm'
        ValueError
        size of the kernel is greater than the size of signal.
        ValueError
        method is not in:
             'auto',
             'direct',
             'scipy.linalg.toeplitz',
             'pyfaust.toeplitz',
             'lazylinop.convToeplitz',
             'fft'
        Exception
            in1 expects tuple as (X, Y).
        Exception
            in1 expects array with shape (X, Y).
        ValueError
            negative dimension value is not allowed.

    Examples:
        >>> from lazylinop.wip.image import convolve2d
        >>> import scipy as sp
        >>> image = np.random.rand(6, 6)
        >>> kernel = np.random.rand(3, 3)
        >>> c1 = convolve2d(image, kernel, mode='same', boundary='fill', method='scipy.linalg.toeplitz')
        >>> c2 = convolve2d(image, kernel, mode='same', boundary='fill', method='pyfaust.toeplitz')
        >>> c3 = convolve2d(image.shape, kernel, mode='same', boundary='fill', method='lazylinop.convToeplitz') @ image.flatten()
        >>> c4 = sp.signal.convolve2d(image, kernel, mode='same', boundary='fill')
        >>> np.allclose(c1, c2)
        True
        >>> np.allclose(c2, c3)
        True
        >>> np.allclose(c3, c4)
        True

    References:
        See also `scipy.signal.convolve2d <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.convolve2d.html>`_
    """
    if not boundary in ['fill', 'wrap', 'symm']:
        raise ValueError("boundary is either 'fill' (default), 'wrap' or 'symm'")

    # check if image has been passed to the function
    # check if shape of the image has been passed to the function
    return_lazylinop = type(in1) is tuple

    if type(in1) is tuple:
        return_laylinop = True
        if len(in1) != 2:
            raise Exception("in1 expects tuple (X, Y).")
        X, Y = in1[0], in1[1]
    else:
        return_lazylinop = False
        if len(in1.shape) != 2:
            raise Exception("in1 expects array with shape (X, Y).")
        X, Y = in1.shape

    if X <= 0 or Y <= 0:
        raise ValueError("zero or negative dimension is not allowed.")
    K, L = in2.shape
    if K > X or L > Y:
        raise ValueError("size of the kernel is greater than the size of the image.")
    if X <= 0 or Y <= 0 or K <= 0 or L <= 0:
        raise ValueError("negative dimension value is not allowed.")

    # boundary conditions
    if boundary == 'fill':
        B = 1
    else:
        B = 3

    # shape of the output image (full mode)
    # it takes into account the boundary conditions
    P, Q = B * X + K - 1, B * Y + L - 1

    if method == 'fft' or (method == 'auto' and max(K, L) > 32):
        C = fftconvolve2d(np.array([B * X, B * Y]), in2, backend='scipy')
    elif method == 'direct' or (method == 'auto' and max(K, L) <= 32):
        import numba as nb
        from numba import prange, set_num_threads
        nb.config.THREADING_LAYER = 'omp'
        T = nb.config.NUMBA_NUM_THREADS
        # while T > 1 and ((X * Y * K * L) / T) < 100000:
        #     T -= 1
        # if T > 1:
        #     use_parallel = True
        #     nb.set_num_threads(T)
        # else:
        #     use_parallel = False
        use_parallel=bool(((X * Y * K * L) / T) >= 1000)
        @nb.jit(nopython=True, parallel=use_parallel, cache=True)
        def _matvec(shape, in1, in2):
            X, Y = shape[0], shape[1]
            K, L = in2.shape
            Ox, Oy = X + K - 1, Y + L - 1
            output = np.full((Ox, Oy), 0.0 * (in1[0] + in2[0, 0]))
            # brute force costs X * Y * K * L operations
            if False:
                T = nb.config.NUMBA_NUM_THREADS
                OperT = int(np.ceil(Ox / T))
                for t in prange(T):
                    for x in range(t * OperT, min(Ox, (t + 1) * OperT), 1):
                        for y in range(Oy):
                            if max(0, x - X + 1) > min(x + 1, K):
                                continue
                            for k in range(max(0, x - X + 1), min(x + 1, K)):
                                if max(0, y - Y + 1) > min(y + 1, L):
                                    continue
                                for l in range(max(0, y - Y + 1), min(y + 1, L)):
                                    # x >= k
                                    # x - X < k
                                    # y >= l
                                    # y - Y < l
                                    output[x, y] += in2[k, l] * in1[(x - k) * Y + y - l]
            else:
                for x in prange(Ox):
                    for y in range(Oy):
                        if max(0, x - X + 1) > min(x + 1, K):
                            continue
                        for k in range(max(0, x - X + 1), min(x + 1, K)):
                            if max(0, y - Y + 1) > min(y + 1, L):
                                continue
                            for l in range(max(0, y - Y + 1), min(y + 1, L)):
                                # x >= k
                                # x - X < k
                                # y >= l
                                # y - Y < l
                                # if (x - k) < X and (y - l) < Y:
                                # if x >= k and (x - k) < X and y >= l and (y - l) < Y:
                                output[x, y] += in2[k, l] * in1[(x - k) * Y + y - l]
            return output.ravel()

        @nb.jit(nopython=True, parallel=True, cache=True)
        def _rmatvec(shape, in1, in2):
            X, Y = shape[0], shape[1]
            K, L = in2.shape
            Ox, Oy = X + K - 1, Y + L - 1
            output = np.full((Ox, Oy), 0.0 * (in1[0] + in2[0, 0]))
            for x in prange(Ox):
                for y in range(Oy):
                    for k in range(0, max(0, min(K, X - x)), 1):
                        for l in range(0, max(0, min(L, Y - y)), 1):
                            output[x, y] += in2[k, l] * in1[(x + k) * Y + y + l]
            return output.ravel()

        C = LazyLinearOp(
            shape=(P * Q, X * Y),
            matvec=lambda x: _matvec((B * X, B * Y), x, in2),
            rmatvec=lambda x: _rmatvec((B * X, B * Y), x, in2)
        )
    else:
        # write 2d convolution as a sum of Kronecker products:
        # image * kernel = sum(kron(E_i, T_i), i, 1, M)
        # E_i is an eye matrix eye(P, n=X, k=-i).
        # T_i is a Toeplitz matrix build from the kernel.
        # first column is the i-th row of the kernel.
        # first row is 0
        if method == 'pyfaust.toeplitz':
            from pyfaust import toeplitz
        elif method == 'lazylinop.convToeplitz':
            from lazylinop.wip.code_optimization import eye_test, kron_eye, kron_test
        else:
            pass
        # K = 1
        LLOps = [None] * K
        for i in range(K):
            # does it need Toeplitz construction because it looks like an eye matrix ?
            if method == 'pyfaust.toeplitz':
                LLOps[i] = kron(eye(P, n=B * X, k=-i), toeplitz(np.pad(in2[i, :], (0, B * Y - 1)), np.pad([in2[i, 0]], (0, B * Y - 1)), diag_opt=True))
            elif method == 'lazylinop.convToeplitz':
                # LLOps[i] = kron_eye((P, B * X), -i, convToeplitz(np.pad(in2[i, :], (0, B * Y - 1)), np.full(B * Y, 0.0), L, **kwargs))
                LLOps[i] = kron_test(eye(P, n=B * X, k=-i), convToeplitz(np.pad(in2[i, :], (0, B * Y - 1)), np.full(B * Y, 0.0), L, **kwargs), use_numba=False)
                # LLOps[i] = kron_test(eye_test(P, n=B * X, k=-i), convToeplitz(np.pad(in2[i, :], (0, B * Y - 1)), np.full(B * Y, 0.0), L, **kwargs), use_numba=False)
                # LLOps[i] = kron(eye(P, n=B * X, k=-i), convToeplitz(np.pad(in2[i, :], (0, B * Y - 1)), np.full(B * Y, 0.0), L, **kwargs))
            elif method == 'scipy.linalg.toeplitz':
                # default
                LLOps[i] = kron(eye(P, n=B * X, k=-i), sp.linalg.toeplitz(np.pad(in2[i, :], (0, B * Y - 1)), np.full(B * Y, 0.0)))
            else:
                raise ValueError("method is not in ['auto', 'direct', 'scipy.linalg.toeplitz', 'pyfaust.toeplitz', 'lazylinop.convToeplitz', 'fft'].")
        C = sum(*LLOps, mt=False, af=False)

    if mode == 'full':
        i1 = (P - (X + K - 1)) // 2
        s1 = i1 + X + K - 1
        i2 = (Q - (Y + L - 1)) // 2
        s2 = i2 + Y + L - 1
    elif mode == 'valid':
        # compute full mode and extract what we need
        # number of rows to extract is X - K + 1 (centered)
        # number of columns to extract is Y - L + 1 (centered)
        # if boundary conditions extract image from the center
        i1 = (P - (X - K + 1)) // 2
        s1 = i1 + X - K + 1
        i2 = (Q - (Y - L + 1)) // 2
        s2 = i2 + Y - L + 1
        indices = ((np.arange(P * Q).reshape(P, Q))[i1:s1, i2:s2]).ravel()
    elif mode == 'same':
        # keep middle of the full mode
        # number of rows to extract is M (centered)
        # number of columns to extract is N (centered)
        # if boundary conditions extract image from the center
        i1 = (P - X) // 2
        s1 = i1 + X
        i2 = (Q - Y) // 2
        s2 = i2 + Y
        indices = ((np.arange(P * Q).reshape(P, Q))[i1:s1, i2:s2]).ravel()
    else:
        raise ValueError("mode is either 'full' (default), 'valid' or 'same'.")

    if mode == 'valid' or mode == 'same':    
        if B > 1:
            # if boundary conditions extract image from the center
            newC = (C @ bc2d((X, Y), n=1, boundary=boundary))[indices, :]
        else:
            newC = C[indices, :]
    else:
        # return full mode
        if B > 1:
            # if boundary conditions extract image from the center
            indices = ((np.arange(P * Q).reshape(P, Q))[i1:s1, i2:s2]).ravel()
            newC = (C @ bc2d((X, Y), n=1, boundary=boundary))[indices, :]
        else:
            newC = C

    if return_lazylinop:
        # return lazy linear operator
        # pyfaust.toeplitz returns 'complex' even if argument is 'real'
        ckernel = bool('complex' in in2.dtype.str)
        return LazyLinearOp(
            shape=newC.shape,
            matvec=lambda x: (
                newC @ x if ckernel or 'complex' in x.dtype.str
                else np.real(newC @ x)
            ),
            rmatvec=lambda x: (
                newC.T.conj() @ x if ckernel or 'complex' in x.dtype.str
                else np.real(newC.T.conj() @ x)
            )
        )
    else:
        # return result of the 2D convolution
        # pyfaust.toeplitz returns 'complex' even if argument is 'real'
        if 'complex' in in1.dtype.str or 'complex' in in2.dtype.str:
            return (newC @ in1.flatten()).reshape(s1 - i1, s2 - i2)
        else:
            return np.real((newC @ in1.flatten())).reshape(s1 - i1, s2 - i2)


def pad(shape: tuple, pad_width: tuple):
    """Constructs a lazy linear operator Op for padding.
    Op is applied to a flattened image.
    The output of the padding of the image is given by Op @ image.flatten(order='C').
    The function uses Kronecker trick vec(M @ X @ N) = kron(M.T, N) @ vec(X).

    Args:
        shape: tuple
        shape of the image
        pad_width: tuple
        It can be (A, B):
        Add A zero columns and rows before and B zero columns and rows after.
        or ((A, B), (C, D)):
        Add A zero rows before and B zero rows after.
        Add C zero columns to the left and D zero columns to the right.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            pad_width expects (A, B) or ((A, B), (C, D)).
        ValueError
            pad_width expects positive values.

    Examples:
        >>> from lazylinop.wip.image import pad
        >>> x = np.arange(1, 4 + 1, 1).reshape(2, 2)
        >>> x
        array([[1, 2],
               [3, 4]])
        >>> y = pad(x.shape, (1, 2)) @ x.flatten()
        >>> y.reshape(5, 5)
        array([[0., 0., 0., 0., 0.],
               [0., 1., 2., 0., 0.],
               [0., 3., 4., 0., 0.],
               [0., 0., 0., 0., 0.],
               [0., 0., 0., 0., 0.]])
        >>> x = np.arange(1, 6 + 1, 1).reshape(2, 3)
        >>> x
        array([[1, 2, 3],
               [4, 5, 6]])
        >>> y = pad(x.shape, ((2, 1), (2, 3))) @ x.flatten()
        >>> y.reshape(5, 8)
        array([[0., 0., 0., 0., 0., 0., 0., 0.],
               [0., 0., 0., 0., 0., 0., 0., 0.],
               [0., 0., 1., 2., 3., 0., 0., 0.],
               [0., 0., 4., 5., 6., 0., 0., 0.],
               [0., 0., 0., 0., 0., 0., 0., 0.]])

    References:
        See also `numpy.pad <https://numpy.org/doc/stable/reference/generated/numpy.pad.html>`_
    """
    W = len(pad_width)
    if W != 2:
        raise ValueError("pad_width expects (A, B) or ((A, B), (C, D)).")
    if type(pad_width[0]) is tuple:
        # pad_witdh is ((A, B), (C, D))
        for w in range(W):
            if pad_width[w][0] < 0 or pad_width[w][1] < 0:
                raise ValueError("pad_width expects positive values.")
            Ww = len(pad_width[w])
            if Ww != 2:
                raise ValueError("pad_width expects (A, B) or ((A, B), (C, D)).")
            if w == 0:
                M = eye(shape[0] + pad_width[w][0] + pad_width[w][1], n=shape[0], k=-pad_width[w][0])
            elif w == 1:
                # N = eye(shape[1], n=shape[1] + pad_width[w][0] + pad_width[w][1], k=pad_width[w][0])
                NT = eye(shape[1] + pad_width[w][0] + pad_width[w][1], n=shape[1], k=-pad_width[w][0])
        Op = kron(M, NT)
        return Op
    else:
        if pad_width[0] < 0 or pad_width[1] < 0:
            raise ValueError("pad_width expects positive values.")
        # pad_witdh is (A, B), pad each dimension
        M = eye(shape[0] + pad_width[0] + pad_width[1], n=shape[0], k=-pad_width[0])
        # N = eye(shape[1], n=shape[1] + pad_width[0] + pad_width[1], k=pad_width[0])
        NT = eye(shape[1] + pad_width[0] + pad_width[1], n=shape[1], k=-pad_width[0])
        Op = kron(M, NT)
        return Op


if __name__ == '__main__':
    import doctest
    doctest.testmod()
