#+
#   ARES/HADES/BORG Package -- ./scripts/ares_tools/read_all_h5.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#   Copyright (C) 2009-2020 Jens Jasche <jens.jasche@fysik.su.se>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
import os
import numpy as np
import numexpr as ne
import h5py as h5

def isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter


try:
    import tqdm

    if isnotebook():
      u_tqdm = tqdm.tqdm_notebook
    else:
      u_tqdm = tqdm.tqdm

    def progress(iterator):
        L = list(iterator)
        return u_tqdm(L)
except:
    def progress(iterator):
        for i, q in enumerate(iterator):
            if ((i % 100) == 0):
                print(i)
            yield q


def default_slicer(x): return x[...]


class Bunch(object):
    def __init__(self, **kwds):
        self.__dict__.update(**kwds)

    def __del__(self):
        if hasattr(self, '_lazy') and self._lazy:
            # close the file/group
            if isinstance(self._group, h5.File):
                print("Closing HDF5 file")
                try:
                    self._group.close()
                except:
                    # Eat all exceptions
                    pass

    def insert(self, aname, data):
        if len(aname) == 1:
            self.__dict__.update({aname[0]: data})
        else:
            if aname[0] in self.__dict__:
                k = self.__dict__[aname[0]]
            else:
                k = Bunch()
                self.__dict__.update({aname[0]: k})
            k.insert(aname[1:], data)


def read_group(g, lazy=False):
    m = {}
    for k in g:
        if hasattr(g[k], 'keys'):
            m[k] = read_group(g[k], lazy=lazy)
        else:
            if lazy:
                m[k] = g[k]
            else:
                m[k] = g[k][:]
    if lazy:
        m['_group'] = g
    m['_lazy'] = lazy

    return Bunch(**m)


def read_attr_group(g, ename, bunch, slicer=default_slicer):
    for a in ename:
        g = g[a]
    if bunch == None:
        bunch = Bunch()

    bunch.insert(ename, slicer(g))
    return bunch


def read_all_h5(fname, lazy=False):
    if lazy:
        f = h5.File(fname, mode="r")
        return read_group(f, lazy=True)
    else:
        with h5.File(fname, mode="r") as f:
            return read_group(f, lazy=False)


def read_attr_h5(fname, egroup, slicer=default_slicer):
    with h5.File(fname, mode="r") as f:
        b = None
        for e in egroup:
            b = read_attr_group(f, e, b, slicer=slicer)
    return b


def grabber(obj, e):
    if len(e) == 1:
        return getattr(obj, e[0])
    else:
        return grabber(getattr(obj, e[0]), e[1:])


def rebuild_spliced_h5(path, element_list, ncpu, verbose=False, flex_cpu=False):
    """Rebuild a set of fields which are spliced across different hdf5 files.
    The use of this function is typically dedicated to the analysis of MPI run.

    Parameters
    ----------
    path         : string
                   base path for the set of hdf5 file. A suffix "_[CPUID]" will be appended.
    element_list : list of string
                   list of elements to rebuild from the set of files
    ncpu         : int
                   number of cpus for the run
    verbose      : boolean
                   if True the code will run with verbose output
    flex_cpu     : boolean
                   if True, ncpu is understood as the maximum number of cpus. If the code does
                   find a file then it stops the rebuilding without failing.

    Returns
    -------
       dictionnary
       each element name is a key, and the value is a numpy array. The arrays are concatenated
       according to their first axis.
    """
    b = [None for e in element_list]
    egrab = [e.split('.') for e in element_list]

    for cpu in range(ncpu):
        fname = path + "_%d" % cpu
        if verbose:
            print("Loading CPU file '%s'" % fname)
        try:
            a = read_attr_h5(fname, egrab)
        except OSError:
            if flex_cpu:
                break
            raise
        for j, e in enumerate(egrab):
            if b[j] is None:
                b[j] = grabber(a, e)
            else:
                b[j] = np.append(b[j], grabber(a, e), axis=0)

    dtype = [(e, t[0].dtype, t[0].shape) for e, t in zip(element_list, b)]
    arr = {}
    for e, q in zip(element_list, b):
        arr[e] = q
    return arr


def chain_iterator(path, start=0, step=1, err_up=0, end=-1, prefix="mcmc", need_id=False):
    import os

    i = start
    while True:
        fname = os.path.join(path, "%s_%d.h5" % (prefix,i,))
        try:
            os.stat(fname)
        except IOError:
            if (i >= err_up):
                return
            else:
                i += step
                continue

        if need_id:
          yield (i,fname)
        else:
          yield fname
        i += step
        if end > 0 and i > end:
          break


def read_chain_h5(path, element_list, start=0, step=1, err_up=0, slicer=default_slicer, prefix="mcmc", flexible=True):
    """
    read_chain_h5(path,element_list,start=0,step=1,err_up=0,slicer=default_slicer)

    Arguments:
      * path: path where you have the chain (mcmc_* files)
      * element_list: list of strings where the MCMC objects are stored. For example, you
                      have scalars.galaxy_nmean_0 for the nbar parameter of the first catalog.
      * start: the first element of the chain to consider
      * step: if you want to thin the chain by "step"
      * err_up: whether to accept I/O errors when opening files up to the specified MCMC id
      * slicer: a lambda function that can only take a subset of the array of the
      specified MCMC object. For example, it can be lambda d: d[:,:,64], to indicate only
       the plane 64 in the 3d grid that is being loaded. [64,...]

    Returns:
      * a columned numpy array "a". You have one column for each element_id of the
      element_list.  You can access one of the column like this:
      a["scalars.galaxy_nmean_0"]

  """
    i = start
    b = [[] for e in element_list]
    egrab = [e.split('.') for e in element_list]
    for fname in progress(chain_iterator(path, start=start, step=step, err_up=err_up, prefix=prefix)):
        try:
          a = read_attr_h5(fname, egrab, slicer=slicer)
        except OSError:
          if not flexible:
              raise
          else:
              break
        for j, e in enumerate(egrab):
            b[j].append(grabber(a, e))

    dtype = [(e, t[0].dtype, t[0].shape) for e, t in zip(element_list, b)]

    arr = np.empty(len(b[0]), dtype=dtype)
    for e, q in zip(element_list, b):
        arr[e] = q
    return arr


def chain_compute_xcor(path, start=0, Nbins=100):
    import cosmotool as ct
    import numexpr as ne

    i = 0

    with h5.File(os.path.join(path, "restart.h5_0"), mode="r") as f:
        L0 = f['scalars']['L0'][:]
        L1 = f['scalars']['L1'][:]
        L2 = f['scalars']['L2'][:]
        N0 = int(f['scalars']['N0'][:])
        N1 = int(f['scalars']['N1'][:])
        N2 = int(f['scalars']['N2'][:])

    ix = np.fft.fftfreq(N0, d=1.0/L0)[:, None, None]
    iy = np.fft.fftfreq(N1, d=1.0/L1)[None, :, None]
    iz = np.fft.fftfreq(N2, d=1.0/L2)[None, None, :]
    r2 = ne.evaluate('sqrt(ix**2+iy**2+iz**2)')
    rmax = r2.max()
    ir = (r2 * Nbins / rmax).astype(np.int32).ravel()
    xi = []
    W = np.bincount(ir, minlength=Nbins)

    fft = ct.CubeFT(L0, N0)

    while True:
        try:
            if i % 10 == 0:
                print(i)
            fname = os.path.join(path, "mcmc_%d.h5" % (i+start))
            with h5.File(fname, mode="r") as f:
                fft.density = f["scalars"]["s_field"][:]

            fft.rfft()
            ne.evaluate("complex(real(d)**2 + imag(d)**2, 0)",
                        local_dict={'d': fft.dhat}, out=fft.dhat, casting='unsafe')
            fft.irfft()

            xi.append(np.bincount(
                ir, weights=fft.density.ravel(), minlength=Nbins))
            i += 1

        except Exception as e:
            print(repr(e))
            break

    xi = np.array(xi) / W

    r = np.arange(Nbins) * rmax / Nbins
    return r, xi


def explore_chain(path, start, end=-1, step=1, quiet=True):
    """
    Arguments:
      * path
      * start
      * end
      * step

    Returns:
      * iterator with hdf5 object. Example:
           for i in explore_chain(".", 0):
              mean = i['/scalars/galaxy_nmean_0'][0]
              # Then do stuff with "mean"
  """
    n = int(start)
    nmax = int(end)
    step = int(step)
    k = 0

    while (nmax == -1) or (n < nmax):
        p = path + "/mcmc_%d.h5" % n
        if not quiet and (k % 100) == 0:
            print("%d" % n)
        try:
            f = h5.File(p, mode="r")
        except Exception as e:
            print(e)
            break

        try:
            yield n, f['scalars']
        finally:
            f.close()

        n += step
        k += 1


def build_power_histogram(path, start=0, step=1, Nhisto=100, quiet=True, logP=True, Prange=(0.1, 1e5)):
    """
    Use the scalars.powerspectrum mcmc element to build the PDF of the posterior
    powerspectrum

    Arguments:
       * path
       * start
       * step
       * Nhisto: number of bins for each k mode of the P(k) histogram
       * quiet:
       * logP: whether you want to use a log scale for plotting
       * Prange: a tuple for giving the entire P range to represent

     Returns:
       * a tuple: t=(kmodes, Pgrid, Pk_pdf_values) which is directly usable in pcolormesh
         like pcolormesh(*t)
  """
    # print path+ "/restart.h5_0"
    for _, scalars in explore_chain(path, start, end=start+1, step=1, quiet=quiet):
        Nk = scalars["powerspectrum"].size
    with h5.File(path + "/restart.h5_0", mode="r") as f:
        k_mode = f["/scalars/k_modes"][:]

    Phisto = np.zeros((Nk, Nhisto), dtype=np.int)
    if logP:
        logPmin = np.log10(Prange[0])
        DeltaLog = np.log10(Prange[1]/Prange[0])/(Nhisto)

        def transform(P): return ((np.log10(P)-logPmin)/DeltaLog)
    else:
        Pmin = Prange[0]
        DeltaP = (Prange[1]-Prange[0])/(Nhisto)

        def transform(P): return (P-Pmin)/DeltaP

    for n, scalars in explore_chain(path, start, step=step, quiet=quiet):
        P = scalars["powerspectrum"][:]
        iP = np.floor(transform(P))
        ik = np.where((np.isnan(iP) == False)*(iP >= 0)*(iP < Nhisto))
        iP = iP[ik].astype(np.int)
        for i, j in zip(ik[0], iP):
            Phisto[i, j] = Phisto[i, j]+1

    k_mode = k_mode[:, None].repeat(Nhisto, axis=1)
    if logP:
        Pg = 10**((np.arange(Nhisto)+0.5)*DeltaLog + logPmin)
    else:
        Pg = ((np.arange(Nhisto)+0.5)*DeltaP + Pmin)

    Pg = Pg[None, :].repeat(Nk, axis=0)
    return k_mode, Pg, Phisto


def read_chain_complex_avg_dev(path, op, start=0, end=-1, do_dev=False, step=1, slicer=default_slicer, prefix="mcmc"):
    """
    Compute mean and standard deviation of the given element_list

    Arguments:
      * path
      * op:
      * element_list
      * start
      * do_dev: boolean for computing the standard deviation (or not)
      * slicer:


     Returns:
      * a columned numpy array. Each column has a name that corresponds to an element with an additional dimension. For example, a['scalars.galaxy_nmean_0'][0] -> mean,
      a['scalars.galaxy_nmean_0'][1] is the standard deviation.
  """
    i = 0
    b = None
    bd = None
    try:
      for fname in progress(chain_iterator(path, start=start, step=step, end=end, prefix=prefix)):
        with h5.File(fname, mode="r") as ff:
            if b is None:
                b = op(ff)
                if do_dev:
                    bd = np.zeros(b.shape)
            else:
                data = op(ff)
                ne.evaluate('r*a+k*c',
                            dict(k=1/float(i+1),
                                 r=(float(i)/float(i+1)),
                                 a=b,
                                 c=data),
                            out=b)
            if do_dev and i > 1:
                ne.evaluate('k*(xn-mun)**2 + f*bdn',
                            dict(k=1/float(i),
                                 f=float(i)/float(i+1),
                                 xn=data,
                                 mun=b,
                                 bdn=bd),
                            out=bd)
            i += 1

    except OSError:
      pass

    bd = np.sqrt(bd)
    return b, bd


def read_chain_avg_dev(path, element_list, start=0, end=-1, do_dev=False, operator=lambda x: x, step=1, slicer=default_slicer, prefix="mcmc", err_up=0):
    """
    Compute mean and standard deviation of the given element_list

    Arguments:
      * path
      * element_list
      * start
      * do_dev: boolean for computing the standard deviation (or not)
      * operator: applies the operator on all the elements before computing the mean and
        standard deviation.
      * slicer:


     Returns:
      * a columned numpy array. Each column has a name that corresponds to an element with an additional dimension. For example, a['scalars.galaxy_nmean_0'][0] -> mean,
      a['scalars.galaxy_nmean_0'][1] is the standard deviation.
  """
    i = 0
    b = [None for e in element_list]
    bd = [None for e in element_list]
    egrab = [e.split('.') for e in element_list]
    for fname in progress(chain_iterator(path, start=start, step=step, end=end, err_up=err_up, prefix=prefix)):
            a = read_attr_h5(fname, egrab, slicer=slicer)
            for j, e in enumerate(egrab):
                if b[j] is None:
                    b[j] = operator(grabber(a, e))
                    if do_dev:
                        bd[j] = np.zeros(b[j].shape)
                else:
                    data = operator(grabber(a, e))
                    ne.evaluate('r*a+k*c',
                                dict(k=1/float(i+1),
                                     r=(float(i)/float(i+1)),
                                     a=b[j],
                                     c=data),
                                out=b[j])
                    if do_dev and i > 0:
                        ne.evaluate('k*(xn-mun)**2 + f*bdn',
                                    dict(k=1/float(i),
                                         f=float(i)/float(i+1),
                                         xn=data,
                                         mun=b[j],
                                         bdn=bd[j]),
                                    out=bd[j])
                i+=1

    dtype = [(e, t.dtype, t.shape) for e, t in zip(element_list, b)]

    arr = np.empty(2 if do_dev else 1, dtype=dtype)
    for e, q, q2 in zip(element_list, b, bd):
        arr[e][0] = q
        if do_dev:
            arr[e][1] = np.sqrt(q2)
    return arr
