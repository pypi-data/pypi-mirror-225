"""
Various tools for quality controling or otherwise preprocessing turbulence timeseries data. For more conventional QAQC use the pIMOS library. 

These functions work on continuous individual blocks of data. If they are to be done blockwise 
this must be handled elsewhere.   

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import path as mplpath

def unwrap(x, prev_block_median, ambiguity_velocity=0.23, verbose = False):
    """
    Unwrap a block of data, or don't if not needed:

    Parameters
    ----------
    x : np.array
        The block of data that is potentially wrapped
    prev_block_median : numeric
        The median of the previous block. This is used in the event of a phase wrap to help determine whether its wrapped likely wrapped high or low. 
    ambiguity_velocity(optional) : numeric
        This is the +/- ambiguity point that maps to +/- pi. Default is 0.23, which is very specific and prob shouldn't be a default. 

    Returns
    -------
    thats_a_wrap: boolean
        Flag for wrap detection. True if wrapped, False if not wrapped.
    X : np.array
        Output data. Equal to  x if the block was not deemed to be wrapped, or an unwrapped version otherwise. 

    """

    def detect_wrap(x, prev_block_median, ambiguity_velocity, verbose = False):
        """
        Detect whether wrap is suspected. Method is to do a test unwrap (direction does not matter) 
        and compare the new variance with the old. If it goes down it's assumed to be wrapped. 
        """
        
        vb = np.nanvar(x)

        X = unwrap_block(x, prev_block_median, ambiguity_velocity, verbose = verbose)

        thats_a_wrap = np.nanvar(X) < np.nanvar(x) # Check based on variance shift
        thats_a_wrap = np.max(np.diff(X[~np.isnan(X)])) < max(np.diff(x[~np.isnan(x)]))
        
        if verbose:
            if thats_a_wrap:
                print('Var X = {}; var x = {}; Wrapped'.format(np.nanvar(X), vb))
            else:
                print('Var X = {}; var x = {}; Not wrapped wooo!!'.format(np.nanvar(X), vb))

        if verbose and thats_a_wrap:
            plt.figure(figsize=(12, 8))

            ax = plt.subplot2grid((3, 20), (0, 0), rowspan=1, colspan=29)
            ax.plot(x, linewidth=3)
            ax.plot(X)
            ax.grid(linestyle='-')
            plt.show()

        return thats_a_wrap, X

    def unwrap_block(x, prev_block_median, ambiguity_velocity, verbose = False):
        """
        Only having auto detection from now on. 
        """
        
        X  = x.copy()
        X_ = X.copy()

        sx = np.sort(x)
        db = np.diff(sx);                           # Measure "spikes"
        mdb = np.max(db);                           # Take largest "spike"
        dbi = int(np.mean(np.nonzero(db==mdb)))     # Get index of largest "spike"

        ind = np.arange(dbi, dbi+2)

        brk = np.mean(sx[ind])                      # Find largest "spike" mid velocity
        
        median_above = np.nanmedian(x[x > brk])
        median_below = np.nanmedian(x[x < brk])

        if verbose:
            print('Largest spike is {} m/s, from {} to {}, midpoint is {}'.format(mdb, sx[ind[0]], sx[ind[1]], brk))
            print('Median of all points above(below) the break is {}({})'.format(median_above, median_below))
        
        if np.abs(median_above-prev_block_median) < np.abs(median_below-prev_block_median): # Modified this line fro orig
            hlt = 'low';
            direction = 'down';
        else:
            hlt = 'high';
            direction = 'up';
        
        # print('It is thus assumed that the {} values are phase wrapped.'.format(hlt))

        if direction == 'down':
                phase_wrapped = x < brk
                
                X[phase_wrapped] = x[phase_wrapped] + 2*ambiguity_velocity;
        if direction == 'up':
                phase_wrapped = x > brk
                
                X[phase_wrapped] = x[phase_wrapped] - 2*ambiguity_velocity;
        
        if verbose:
            print('n changed = {} (of {}).'.format(sum(phase_wrapped), len(phase_wrapped)))

        return X

    # Main function
    x = x.copy()

    thats_a_wrap, X = detect_wrap(x, prev_block_median, ambiguity_velocity=ambiguity_velocity, verbose = verbose)
    if thats_a_wrap:
        pass
    else:
        X = x 
        
    if verbose:
        if thats_a_wrap:
            print('I''m not wrapped but it is wrapped')
        else:
            print('I''m wrapped that it isn''t wrapped')

    return thats_a_wrap, X 
 
def despike(u, fs, interp_opt='linear', intensity = 0.9, verbose=False):
    """
    Despike a single block of data. Binning to be done outside. Same as despikei but returns the first output only.  

    See also
    --------

    afloat.clean.despikei

    """

    U, di = despikei(u, fs, interp_opt='linear', intensity = 0.9, verbose=False)

    return U

def despikei(u, fs, interp_opt='linear', intensity = 0.9, verbose=False):
    """
    Despike a single block of data. Binning to be done outside.  

    Parameters
    ----------
    u : np.array
        Data to be despiked. Assumed to be well spaced in the dimension that it is sampled (time or space).
    fs : numeric
        The sample frequency of the data.
    intensity : numeric
        The intensity threshold used in the phase space method.

    Returns
    -------
    U : np.array
        Despiked u array
    di : 
        Indices of modified data

    """

    def phase_space_thres(u, fs, intensity = 0.9, verbose=False):
        """
        This function actually detects the spikes and nans them out. Single block, single component. 
        """

         # not oriignally part of the method. 

        n = len(u)
        u = u - u.mean(0) # Maybe should detrend

        du = np.zeros_like(u)
        d2u = np.zeros_like(u)
        
        # Take the centered difference.
        du[1:-1] = (u[2:] - u[:-2]) / 2
        # And again.
        d2u[2:-2] = (du[1:-1][2:] - du[1:-1][:-2]) / 2
        
        std_u = np.std(u, axis=0)
        std_du = np.std(du, axis=0)
        std_d2u = np.std(d2u, axis=0)
        
        # goringnikora(data,tplot)
        ## Part 1 of Phase-Threshold Method
        # Eq 7 Nikora & Goring

        ## Part 2 of Phase Threshold Method

        # Expected absolute maximum using Eq.2
        Lambda_u = (2*np.log(n))**0.5
        em_u    =   Lambda_u * std_u; 
        em_du   =   Lambda_u * std_du; 
        em_d2u  =   Lambda_u * std_d2u; 

        ## Part 3 of Phase Threshold Method
        # Eq.9
        theta = np.arctan(np.nansum(u*std_d2u)/np.nansum(u**2))

        if verbose:
            print('Theta = {}'.format(theta))

        A = np.array([[np.cos(theta)**2, np.sin(theta)**2], [np.sin(theta)**2, np.cos(theta)**2]])
        LHS = np.array([[em_u**2], [em_d2u**2]])
        ab2 = np.linalg.inv(A) @ LHS
        a = np.sqrt(ab2[0])
        b = np.sqrt(ab2[1])

        def index_from_ellipse(x, y, r_x, r_y, phi):

            origin_x = np.mean(x)
            origin_y = np.mean(y)

            xp, yp  = calculate_ellipse(origin_x, origin_y, r_x, r_y, phi)

            xy_1 = np.transpose(np.vstack((xp, yp)))
            p = mplpath.Path(xy_1)
            points = np.transpose(np.vstack((x, y)))
            ind = ~p.contains_points(points)

            return xp, yp, ind

        # d2u vs u
        r_x = intensity*a
        r_y = intensity*b
        xp_1, yp_1, ind_1 = index_from_ellipse(u, d2u, r_x, r_y, theta)

        # du vs u
        r_x = intensity*em_u
        r_y = intensity*em_du
        xp_2, yp_2, ind_2 = index_from_ellipse(u, du, r_x, r_y, 0)
        
        # d2u vs du
        r_x = intensity*em_du
        r_y = intensity*em_d2u
        xp_3, yp_3, ind_3 = index_from_ellipse(du, d2u, r_x, r_y, 0)

        ind = ind_1 | ind_2 | ind_3

        if verbose:
            
            print('Total to go = {}'.format(sum(ind)))

            plt.figure(figsize=(5, 15))

            ax = plt.subplot2grid((3, 20), (0, 0), rowspan=1, colspan=29)
            plt.plot(u, d2u, '.')
            plt.plot(u[ind_1], d2u[ind_1], '.')
            plt.plot(xp_1, yp_1)
            ax.grid(linestyle='-')

            ax = plt.subplot2grid((3, 20), (1, 0), rowspan=1, colspan=29)
            plt.plot(u, du, '.')
            plt.plot(u[ind_2], du[ind_2], '.')
            plt.plot(xp_2, yp_2)
            ax.grid(linestyle='-')
            
            ax = plt.subplot2grid((3, 20), (2, 0), rowspan=1, colspan=29)
            plt.plot(du, d2u, '.')
            plt.plot(du[ind_3], d2u[ind_3], '.')
            plt.plot(xp_3, yp_3)
            ax.grid(linestyle='-')
            
        return ind

    def calculate_ellipse(origin_x, origin_y, r_x, r_y, phi=0):
        """

        """
        
        ang = np.linspace(-np.pi, np.pi, 1000)

        x = origin_x + r_x*np.cos(ang)*np.cos(phi) - r_y*np.sin(ang)*np.sin(phi)
        y = origin_y + r_y*np.sin(ang)*np.cos(phi) + r_x*np.cos(ang)*np.sin(phi)

        x = np.append(x, x[0])
        y = np.append(y, y[0])
        
        return x, y 

    """
    Main function start
    """

    if np.any(np.isnan(u)):
        raise Exception('Fill nans before despiking')

    ind = phase_space_thres(u, fs, intensity=intensity, verbose=verbose)

    U = u.copy()
    if verbose:
        sn = np.sum(np.sum(np.isnan(U)))
        print('Nans in the data before despike: {}'.format(sn)) 
    
    U[ind] = np.nan
    di = np.isnan(U)
    if verbose:
        sn = np.sum(np.sum(di))
        print('Nans in the data after despike: {}'.format(sn)) 
    
    U = fillgaps(U, extrapFlg=True)
    if verbose:
        sn = np.sum(np.sum(np.isnan(U)))
        print('Nans in the data after the gapfill: {}'.format(sn)) 

    if verbose:
    
        plt.show()

        plt.figure(figsize=(15, 5))
        plt.plot(u)
        plt.plot(U)

    return U, di

def logical_clean(x, index):
    """
    Remove data indicated by a logiocal index and interpolate over the gaps created.  
    """

    xo = x.copy()
    xo[index] = np.nan

    xo = fillgaps(xo)

    return xo

def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Parameters
    ----------
    y : 1d numpy array 
        Data record with possible NaNs

    Returns
    -------
    nans : np.array
        Array of bools - logical indices of NaNs
    index : function
        A function, with signature indices=index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    
    Example
    -------
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]

def fillnans(y, first_gone=None):
    """
    Fill nans in a 1D or 2D np array.
    """

    if not type(None) == type(first_gone):
        y[first_gone::, :] = np.nan
    
    s = y.shape
    if len(s) == 1:
        y = y[:, None]
        n = s
        mm = 1
    elif len(s) == 2:
        nn, mm = s
    else:
        raise(Exception)
        
    for m in np.arange(0, mm):
                
        nans, x= nan_helper(y[:, m])

        if sum(nans)>0 and sum(nans)<len(nans):
            y[nans, m]= np.interp(x(nans), x(~nans), y[~nans, m])

    return y


def fillgaps(a, maxgap=np.inf, dim=0, extrapFlg=False):
    """
    Linearly fill NaN value in an array.

    Parameters
    ----------
    a : |np.ndarray|
      The array to be filled.

    maxgap : |np.ndarray| (optional: inf)
      The maximum gap to fill.

    dim : int (optional: 0)
      The dimension to operate along.

    extrapFlg : bool (optional: False)
      Whether to extrapolate if NaNs are found at the ends of the
      array.

    See Also
    --------

    interpgaps : Linearly interpolates in time.

    Notes
    =====

    This function interpolates assuming spacing/timestep between
    successive points is constant. If the spacing is not constant, use
    interpgaps.

    This was duplicated from the DOLFyn function of the same name. See lkilcher/DOLFyN on github. 

    """

    # If this is a multi-dimensional array, operate along axis dim.
    if a.ndim > 1:
        raise Exception("This functionality has been removed")

    a = np.asarray(a)
    nd = a.ndim
    if dim < 0:
        dim += nd
    if (dim >= nd):
        raise ValueError("dim must be less than a.ndim; dim=%d, rank=%d."
                         % (dim, nd))
    ind = [0] * (nd - 1)
    i = np.zeros(nd, 'O')
    indlist = list(range(nd))
    indlist.remove(dim)
    i[dim] = slice(None, None)
    # outshape = np.asarray(a.shape).take(indlist)
    # Ntot = np.product(outshape)
    i.put(indlist, ind)
    # k = 0

    gd = np.nonzero(~np.isnan(a))[0]

    # Here we extrapolate the ends, if necessary:
    if extrapFlg and gd.__len__() > 0:
        if gd[0] != 0 and gd[0] <= maxgap:
            a[:gd[0]] = a[gd[0]]
        if gd[-1] != a.__len__() and (a.__len__() - (gd[-1] + 1)) <= maxgap:
            a[gd[-1]:] = a[gd[-1]]

    # Here is the main loop
    if gd.__len__() > 1:
        inds = np.nonzero((1 < np.diff(gd)) & (np.diff(gd) <= maxgap + 1))[0]
        for i2 in range(0, inds.__len__()):
            ii = list(range(gd[inds[i2]] + 1, gd[inds[i2] + 1]))
            a[ii] = (np.diff(a[gd[[inds[i2], inds[i2] + 1]]]) *
                     (np.arange(0, ii.__len__()) + 1) /
                     (ii.__len__() + 1) + a[gd[inds[i2]]]).astype(a.dtype)

    return a

        
#%%

# ho = 1

#%%