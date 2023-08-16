import numpy as np
import cupy as cp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.spatial.distance import cdist


class Grid:
    def __init__(self, *, x0, x1, xstep=1, y0, y1, ystep=1):
        """initializes 2D grid with x0<=x<=x1 and y0<=y<=y1;
        Creates a 1D numpy array of grid coordinates in self.x and self.y"""
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.xstep = xstep
        self.ystep = ystep
        xvals = np.arange(x0, x1+xstep, xstep)
        yvals = np.arange(y1, y0-ystep, -ystep)
        xgrid, ygrid = np.meshgrid(xvals, yvals)
        self.x = np.ravel(xgrid)
        self.y = np.ravel(ygrid)
        # should match extent=(x0,x1,y0,y1) for compatibility with matplotlib.pyplot.contour
        # see https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contour.html
        self.extent = (self.x0, self.x1, self.y0, self.y1)  
        self.gshape = self.shape()
        self.len = self.gshape[0]*self.gshape[1]
        assert(self.x.shape == (self.len,))
        assert(self.y.shape == (self.len,))

    def as_xy_vectors(self):
        """returns [x,y] vectors for all grid points"""
        vectors = np.column_stack((self.x, self.y))
        assert(vectors.shape == (self.len, 2))
        return vectors
    
    def shape(self, *, x0=None, x1=None, xstep=None, y0=None, y1=None, ystep=None):
        """returns a tuple(number_of_rows,number_of_cols) for the natural shape of the current grid, or a subset"""
        x0 = self.x0 if x0 is None else x0
        x1 = self.x1 if x1 is None else x1
        y0 = self.y0 if y0 is None else y0
        y1 = self.y1 if y1 is None else y1
        xstep = self.xstep if xstep is None else xstep
        ystep = self.ystep if ystep is None else ystep
        if x1<x0:
            raise ValueError
        if y1<y0:
            raise ValueError
        if xstep<=0:
            raise ValueError
        if ystep<=0:
            raise ValueError
        number_of_rows = 1+int((y1-y0)/ystep)
        number_of_cols = 1+int((x1-x0)/xstep)
        return (number_of_rows,number_of_cols)

    def within_box(self, *, x0=None,x1=None,y0=None,y1=None):
        """returns a 1D numpy boolean array, suitable as an index mask, for testing whether a grid point is also in the defined box"""
        x0 = self.x0 if x0 is None else x0
        x1 = self.x1 if x1 is None else x1
        y0 = self.y0 if y0 is None else y0
        y1 = self.y1 if y1 is None else y1
        return (self.x>=x0) & (self.x<=x1) & (self.y>=y0) & (self.y<=y1)

    def within_disk(self, *, x0, y0, r, metric='euclidean', **kwargs):
        """returns 1D numpy boolean array, suitable as an index mask, for testing whether a grid point is also in the defined disk"""
        mask = (cdist([[x0,y0]], self.as_xy_vectors(), metric=metric, **kwargs)<=r).flatten()
        assert(mask.shape == (self.len,))
        return mask

    def index(self, *, x, y):
        """returns the unique 1D array index for grid point (x,y)"""
        isSelectedPoint = (self.x == x) & (self.y == y)
        indexes = np.flatnonzero((isSelectedPoint))
        assert(len(indexes) == 1)
        return indexes[0]

    def embedding(self, *, valid, fill=0.0):
        """
        returns an embedding function efunc from 1D arrays of size sum(valid)
        to arrays of size self.len

        valid is a np.array of type boolean, of size self.len

        fill is the value for indices outside the embedding. The default
        is zero (0.0).  Setting fill=np.nan can be useful for
        plotting purposes as matplotlib will omit np.nan values from various
        kinds of plots.
        """

        assert(self.len == len(valid))
        correct_z_len = valid.sum()

        def efunc(z):
            assert(len(z) == correct_z_len)
            v = np.full(self.len, fill)
            v[valid] = z
            return v

        return efunc

    def spatial_utilities(
        self,
        *,
        voter_ideal_points,
        metric='sqeuclidean',
        scale=-1,
        **kwargs
    ):
        """returns utility function values for each voter at each grid point"""
        return scale*cdist(
            voter_ideal_points,
            self.as_xy_vectors(),
            metric=metric,
            **kwargs
        )

    def plot(
        self,
        z,
        *,
        title=None,
        cmap=cm.gray_r,
        alpha=0.6,
        alpha_points=0.3,
        log=True,
        points=None,
        zoom=False,
        border=1,
        logbias=1e-100,
        figsize=(10, 10),
        dpi=72,
        fname=None
    ):
        """plots values z defined on the grid;
        optionally plots additional 2D points
         and zooms to fit the bounding box of the points"""
        plt.figure(figsize=figsize, dpi=dpi)
        plt.rcParams["font.size"] = "24"
        fmt = "%1.2f" if log else "%.2e"
        if zoom:
            assert(points.shape[0] > 2)
            assert(points.shape[1] == 2)
            [min_x, min_y] = np.min(points, axis=0)-border
            [max_x, max_y] = np.max(points, axis=0)+border
            box = {x0: min_x, x1: max_x, y0: min_y, y1: max_y}
            inZoom = self.within_box(**box)
            zshape = self.shape(**box)
            extent = (min_x, max_x, min_y, max_y)
            zraw = np.copy(z[inZoom]).reshape(zshape)
            x = np.copy(self.x[inZoom]).reshape(zshape)
            y = np.copy(self.y[inZoom]).reshape(zshape)
        else:
            zshape = self.gshape
            extent = self.extent
            zraw = z.reshape(zshape)
            x = self.x.reshape(zshape)
            y = self.y.reshape(zshape)
        zplot = np.log10(logbias+zraw) if log else zraw
        contours = plt.contour(x, y, zplot, extent=extent, cmap=cmap)
        plt.clabel(contours, inline=True, fontsize=12, fmt=fmt)
        plt.imshow(zplot, extent=extent, cmap=cmap, alpha=alpha)
        if points is not None:
            plt.scatter(
                points[:, 0],
                points[:, 1],
                alpha=alpha_points,
                color='black'
            )
        if title is not None:
            plt.title(title)
        if fname is None:
            plt.show()
        else:
            plt.savefig(fname)


def assert_valid_transition_matrix(P, *, decimal=10):
    """ asserts that numpy or cupy array is square and that each row sums to 1.0
        with default tolerance of 10 decimal places"""
    rows, cols = P.shape
    assert rows == cols
    xp = cp.get_array_module(P)
    xp.testing.assert_array_almost_equal(
        P.sum(axis=1),
        xp.ones(shape=(rows)), decimal
    )


def assert_zero_diagonal_int_matrix(M):
    """ asserts that numpy or cupy array is square and the diagonal is 0.0 """
    rows, cols = M.shape
    assert rows == cols
    xp = cp.get_array_module(M)
    xp.testing.assert_array_equal(
        xp.diagonal(M),
        xp.zeros(shape=(rows), dtype=int)
    )


class MarkovChainGPU():
    def __init__(self, *, P, computeNow=True, tolerance=1e-10):
        """initializes a MarkovChainGPU instance by copying in the transition
        matrix P and calculating chain properties"""
        self.P = cp.asarray(P)  # copy transition matrix to cudapy as necessary
        assert_valid_transition_matrix(P)
        diagP = cp.diagonal(self.P)
        self.absorbing_points = cp.equal(diagP, 1.0)
        self.unreachable_points = cp.equal(cp.sum(self.P, axis=0), diagP)
        self.has_unique_stationary_distibution = \
            not cp.any(self.absorbing_points)
        if computeNow and self.has_unique_stationary_distibution:
            self.find_unique_stationary_distribution(tolerance=tolerance)

    def L1_norm_of_single_step_change(self, x):
        """returns float(L1(xP-x))"""
        return float(cp.linalg.norm(cp.dot(x, self.P) - x, ord=1))

    def solve_for_unit_eigenvector(self):
        """This is another way to potentially find the stationary distribution,
        but can suffer from numerical irregularities like negative entries.
        Assumes eigenvalue of 1.0 exists and solves for the eigenvector by
        considering a related matrix equation Q v = b, where:
        Q is P transpose minus the identity matrix I, with the first row
        replaced by all ones for the vector scaling requirement;
        v is the eigenvector of eigenvalue 1 to be found; and
        b is the first basis vector, where b[0]=1 and 0 elsewhere."""
        n = self.P.shape[0]
        Q = cp.transpose(self.P)-cp.eye(n)
        Q[0] = cp.ones(n)
        b = cp.zeros(n)
        b[0] = 1.0
        self.unit_eigenvector = cp.linalg.solve(Q, b)
        return self.unit_eigenvector

    def find_unique_stationary_distribution(
        self,
        *,
        tolerance,
        start_power=2
    ):
        """finds the stationary distribution for a Markov Chain by
        taking a sufficiently high power of the transition matrix"""
        if cp.any(self.absorbing_points):
            self.stationary_distribution = None
            return None
        unconverged = True
        check1 = 0  # upper left when P is from a grid
        check2 = int(self.P.shape[0]/2)  # center when P is from a grid
        power = start_power
        cP = self.P
        cP_LT = cp.linalg.matrix_power(cP, start_power)
        diags = {
            'power': [],
            'sum1minus1': [],
            'sum2minus1': [],
            'sad': [],
            'diff1': [],
            'diff2': []
        }
        while unconverged:
            cP_LT = cp.linalg.matrix_power(cP_LT, 2)
            power = power * 2
            row1 = cP_LT[check1]
            row2 = cP_LT[check2]
            # cast to float is required because cp.sum yields a cp.cparray
            # with zero dimensions instead of a scalar
            #
            # sum_..._ces = L1 norm of two different rows of P^power
            sum_absolute_diff = float(cp.linalg.norm(row1 - row2, ord=1))
            # diff1 = L1 norm of 1-step evolved row1 minus itself
            diff1 = self.L1_norm_of_single_step_change(row1)
            # diff2 = L1 norm of 1-step evolved row2 minus itself
            diff2 = self.L1_norm_of_single_step_change(row2)
            # sum1 = sum of row1, which should be 1.0
            sum1 = float(cp.sum(row1))
            # sum2 = sum of row2, which should be 1.0
            sum2 = float(cp.sum(row2))
            diags['sad'].append(sum_absolute_diff)
            diags['power'].append(power)
            diags['diff1'].append(diff1)
            diags['diff2'].append(diff2)
            diags['sum1minus1'].append(sum1-1.0)
            diags['sum2minus1'].append(sum2-1.0)
            unconverged = (sum_absolute_diff > tolerance)
            if not unconverged:
                # these extra steps are taken when there is a possible solution
                # use an average over all the rows to collapse cp_LT
                self.stationary_distribution = cp.average(cP_LT, axis=0)
                # double check the solution via an L1 norm
                self.check_norm = self.L1_norm_of_single_step_change(
                    self.stationary_distribution
                )
                unconverged = (self.check_norm > tolerance)

        self.power = power
        self.stationary_diagnostics = diags
        del cP_LT
        return self.stationary_distribution


class VotingModel():
    def __init__(
        self,
        *,
        utility_functions,
        number_of_voters,
        number_of_feasible_alternatives,
        majority,
        zi
    ):
        """initializes a VotingModel with utility_functions for each voter,
        the number_of_voters,
        the number_of_feasible_alternatives,
        the majority size, and whether to use zi fully random agenda or
        intelligent challengers random over winning set+status quo"""
        assert(
            utility_functions.shape ==
            (number_of_voters, number_of_feasible_alternatives)
        )
        self.utility_functions = utility_functions
        self.number_of_voters = number_of_voters
        self.number_of_feasible_alternatives = number_of_feasible_alternatives
        self.majority = majority
        self.zi = zi
        self.analyzed = False

    def analyze(self):
        self.MarkovChain = MarkovChainGPU(P=self._get_transition_matrix())
        self.core_points = cp.asnumpy(self.MarkovChain.absorbing_points)
        self.core_exists = np.any(self.core_points)
        if not self.core_exists:
            self.stationary_distribution = \
                cp.asnumpy(self.MarkovChain.stationary_distribution)
        self.analyzed = True

    def what_beats(self, *, index):
        """returns array of size number_of_feasible_alternatives
        with value 1 where alternative beats current index by some majority"""
        assert(self.analyzed)
        points = cp.asnumpy(self.MarkovChain.P[index, :] > 0).astype('int')
        points[index] = 0
        return points

    def what_is_beaten_by(self, *, index):
        """returns array of size number_of_feasible_alternatives
        with value 1 where current index beats alternative by some majority"""
        assert(self.analyzed)
        points = cp.asnumpy(self.MarkovChain.P[:, index] > 0).astype('int')
        points[index] = 0
        return points

    def plots(
        self,
        *,
        grid,
        voter_ideal_points,
        diagnostics=False,
        log=True,
        embedding=lambda z: z,
        zoomborder=0,
        dpi=72,
        figsize=(10, 10),
        fprefix=None,
        title_core='Core (aborbing) points',
        title_sad='L1 norm of difference in two rows of P^power',
        title_diff1='L1 norm of change in corner row',
        title_diff2='L1 norm of change in center row',
        title_sum1minus1='Corner row sum minus 1.0',
        title_sum2minus1='Center row sum minus 1.0',
        title_unreachable_points='Dominated (unreachable) points',
        title_stationary_distribution_no_grid='Stationary Distribution',
        title_stationary_distribution='Stationary Distribution',
        title_stationary_distribution_zoom='Stationary Distribution (zoom)'
    ):
        def _fn(name):
            return None if fprefix is None else fprefix+name

        def _save(fname):
            if fprefix is not None:
                plt.savefig(fprefix+fname)

        if self.core_exists:
            grid.plot(
                embedding(self.core_points.astype('int')),
                log=log,
                points=voter_ideal_points,
                zoom=True,
                title=title_core,
                dpi=dpi,
                figsize=figsize,
                fname=_fn("core.png")
            )
            return None  # when core exists abort as additional plots undefined
        if diagnostics:
            df = pd.DataFrame(self.MarkovChain.stationary_diagnostics)
            df.plot.scatter(
                'power', 'sad', loglog=True,
                title=title_sad, figsize=figsize
            )
            _save("diagnostic_sad.png")
            df.plot.scatter(
                'power', 'diff1', loglog=True,
                title=title_diff1, figsize=figsize
            )
            _save("diagnostic_diff1.png")
            df.plot.scatter(
                'power', 'diff2', loglog=True,
                title=title_diff2, figsize=figsize
            )
            _save("diagnostic_diff2.png")
            df.plot.scatter(
                'power', 'sum1minus1', logx=True,
                title=title_sum1minus1, figsize=figsize
            )
            _save("diagnostic_sum1minus1.png")
            df.plot.scatter(
                'power', 'sum2minus1', logx=True,
                title=title_sum2minus1, figsize=figsize
            )
            _save("diagnostic_sum2minus1.png")
            if grid is not None:
                grid.plot(
                    embedding(
                        cp
                        .asnumpy(self.MarkovChain.unreachable_points)
                        .astype('int'),
                    ),
                    log=log,
                    title=title_unreachable_points,
                    dpi=dpi,
                    figsize=figsize,
                    fname=_fn("unreachable.png")
                )
        z = self.stationary_distribution
        if grid is None:
            pd.Series(z).plot(
                title=title_stationary_distribution_no_grid,
                figsize=figsize
            )
            _save("stationary_distribubtion_no_grid.png")
        else:
            grid.plot(
                embedding(z),
                log=log,
                points=voter_ideal_points,
                title=title_stationary_distribution,
                figsize=figsize,
                dpi=dpi,
                fname=_fn("stationary_distribution.png")
            )
            if voter_ideal_points is not None:
                grid.plot(
                    embedding(z),
                    log=log,
                    points=voter_ideal_points,
                    zoom=True,
                    border=zoomborder,
                    title=title_stationary_distribution_zoom,
                    figsize=figsize,
                    dpi=dpi,
                    fname=_fn("stationary_distribution_zoom.png")
                )

    def _get_transition_matrix(self):
        utility_functions = self.utility_functions
        majority = self.majority
        zi = self.zi
        nfa = self.number_of_feasible_alternatives
        cV = cp.zeros(shape=(nfa, nfa), dtype=int)
        cU = cp.asarray(utility_functions)
        for a in range(nfa):
            total_votes_for_challenger_when_status_quo_is_a = \
                cp.greater(cU, cU[:, a, cp.newaxis]).astype('int').sum(axis=0)
            total_votes_shape = \
                total_votes_for_challenger_when_status_quo_is_a.shape
            assert(total_votes_shape == (nfa,))
            cV[a] = cp.greater_equal(
                total_votes_for_challenger_when_status_quo_is_a,
                majority
            ).astype('int')
        assert_zero_diagonal_int_matrix(cV)
        cV_sum_of_row = cV.sum(axis=1)  # sum up all col for each row
        # set up the ZI and MI transiation matrices
        if zi:
            cP = cp.divide(
                cp.add(
                    cV,
                    cp.diag(cp.subtract(nfa, cV_sum_of_row))
                ),
                nfa
            )
        else:
            cP = cp.divide(
                cp.add(cV, cp.eye(nfa)),
                (1+cV_sum_of_row)[:, cp.newaxis]
            )
        assert_valid_transition_matrix(cP)
        return cP


class CondorcetCycle(VotingModel):

    def __init__(self, *,  zi):
        # docs suggest to call superclass directly
        # instead of using super()
        # https://docs.python.org/3/tutorial/classes.html#inheritance
        VotingModel.__init__(
            self,
            zi=zi,
            number_of_voters=3,
            majority=2,
            number_of_feasible_alternatives=3,
            utility_functions=np.array([
                [3, 2, 1],  # first agent prefers A>B>C
                [1, 3, 2],  # second agent prefers B>C>A
                [2, 1, 3]   # third agents prefers C>A>B
            ])
        )
