import os
import warnings
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from shapefile import Reader
from .infos import name_list
from matplotlib.path import Path
import matplotlib.patches as patches

def timing(aim = None):
    if aim is not None:
        now = dt.datetime.now()
        tmp = aim - now
        res = tmp.seconds
        print('waitting for {} seconds'.format(res))
        time.sleep(res)

def decompose_dim(arr, dim=0, *shape):
    """
    For input arrays, the specified dimensions are decomposed into the specified shapes
    
    Example:
    >>> arr = np.zeros([30, 200, 50])
    >>> d = decompose_dim(arr, 1, (20,-1))
    >>> d.shape
    (30, 20, 10, 50)
    """
    arr_shape = list(arr.shape)
    if np.iterable(shape[0]):
        shape = shape[0]
    if (-1 not in shape )&(np.prod(shape) != arr_shape[dim]):
        raise ValueError(f"The length of dimension {dim} must keep the same in decomposition")
    arr_shape[dim] = shape
    new_shape = []
    for i in arr_shape:
        if not np.iterable(i):
            new_shape.append(i)
        else:
            new_shape += list(i)
    return arr.reshape(new_shape)

def combine_dim(arr, *dim):
    """
    For the input array, reshape the specified dimension, making it a uniform dimension.
    
    Example:
    >>> arr = np.zeros([30, 10, 20, 50])
    >>> d = combine_dim(arr, 0, 1)
    >>> d.shape
    (300, 20, 50)
    """
    if np.iterable(dim[0]):
        dim = dim[0]
    else:
        dim = list(dim)
    shape = np.array(arr.shape)
    dim = np.sort(np.arange(len(shape))[dim])
    if ((dim[1:] - dim[:-1])!=1).any():
        warn_mes = "The input dimensions must be adjacent, otherwise other problems may result"
        np.warnings.warn(warn_mes, np.VisibleDeprecationWarning)
    shape[dim[-1]] = np.prod(shape[dim])
    shape = np.delete(shape, dim[:-1])
    return arr.reshape(shape)

def view(arr, **kwargs):
    """
    imshow an matrix
    """
    plt.colorbar(plt.imshow(arr, **kwargs)), plt.show()

def stat(arr, name='?', ndot=1):
    """
    print the data loss rate, mean variance,
    minimum, mean, maximum
    """
    nan_num = np.isnan(arr).sum()
    nan_rate = nan_num/np.prod(arr.shape)
    vmin, vmean, vmax = np.nanmin(arr), np.nanmean(arr), np.nanmax(arr)
    vmin, vmean, vmax = np.round(vmin, ndot), np.round(vmean, ndot), np.round(vmax, ndot)
    sd = np.sqrt(np.nanmean((arr-vmean)**2))
    sd = np.round(sd, ndot)
    print(f"{name}: {nan_rate*100:.1f}%, {arr.shape} {sd}\n{vmin}, {vmean}, {vmax}\n")


maskfile_path = os.path.dirname(__file__) + "/maskfiles"
def get_mask(*args):
    """
    Load built-in mask files.

    The optional names are:
    'china' for the edge of China.
    'jiangsu' for the JiangSu province of China.
    and so on.
    """
    das = []
    for name in args:
        filename = name_list.get(name, None)
        if not filename:
            warnings.warn(f"{name} was not found")
            continue
        ds = xr.open_dataset(f"{maskfile_path}/{filename}.nc")
        das.append(ds[list(ds.data_vars)[0]].rename("mask"))
    da = xr.merge(das)
    return da.mask
            
class MaskData:
    
    def __init__(self, data=None):
        y, x = list(data.dims)[-2:]
        self.data = data.rename({y:"lat", x:"lon"})
        self.fill_value = np.nan
        self.dims = data.dims
        self.lon = data.lon
        self.lat = data.lat

    def __lt__(self, other):
        return self.data.__lt__(other)

    def __le__(self, other):
        return self.data.__le__(other)

    def __eq__(self, other):
        return self.data.__eq__(other)

    def __ne__(self, other):
        return self.data.__ne__(other)

    def __gt__(self, other):
        return self.data.__gt__(other)

    def __ge__(self, other):
        return self.data.__ge__(other)

    def __add__(self, other):
        return self.data.__add__(other)

    def __sub__(self, other):
        return self.data.__sub__(other)

    def __mul__(self, other):
        return self.data.__mul__(other)

    def __truediv__(self, other):
        return self.data.__truediv__(other)

    def __floordiv__(self, other):
        return self.data.__floordiv__(other)

    def __mod__(self, other):
        return self.data.__mod__(other)

    def __divmod__(self, other):
        return self.data.__divmod__(other)

    def __pow__(self, other):
        return self.data.__pow__(other)

    def __repr__(self):
        return self.data.__repr__()

    def __str__(self):
        return self.data.__str__()

    def __len__(self):
        return self.data.__len__()

    def __getitem__(self, key):
        return self.data.__getitem__(key)

    def __setitem__(self, key, value):
        return self.data.__getitem__(key, value)

    def __delitem__(self, key):
        return self.data.__getitem__(key)

    def __iter__(self):
        return self.data.__iter__()

    def __reversed__(self):
        self.reverse()

    def __contains__(self, item):
        return self.data.__contains__(item)

    def __array__(self):
        return np.array(self.data)

    def where(self, cond, other=np.nan):
        return self.data.where(cond, other)

    def extent(self, lon, lat):
        y, x = self.data.dims[-2:]
        tmp = self.data.interp({x:lon, y:lat}, method="nearest", kwargs=dict(fill_value=self.fill_value))
        return tmp
    
    def reverse(self):
        self.fill_value = 1 if np.isnan(self.fill_value) else np.nan
        tmp = xr.where(self.data>0, np.nan, 1)
        self.data = tmp

def shp4mask(res, *shpfiles, center=0, encoding='utf-8', ax=None, attrs=["collections"]):
    codes = shp2codes(*shpfiles, center=center, encoding=encoding)
    clip =  codes2clip(*codes, ax=ax)
    if hasattr(res, "set_clip_path"):
        res.set_clip_path(clip)
    else:
        for attr in attrs:
            tmp = res.__getattribute__(attr)
            if hasattr(tmp, "set_clip_path"):
                tmp.set_clip_path(clip)
            else:
                for collection in tmp:
                    collection.set_clip_path(clip)

def _parts2codes(points, parts):
    codes = []
    if len(parts) > 2:
        clip_ponits = []
        for parm in np.lib.stride_tricks.sliding_window_view(parts, (2)):
            pts = points[slice(*parm)]
            clip_ponits.append(pts)
            codes += [Path.MOVETO]
            codes += [Path.LINETO] * (len(pts)-2)
            codes += [Path.CLOSEPOLY]
        points = np.vstack(clip_ponits)
    else:
        codes += [Path.MOVETO]
        codes += [Path.LINETO] * (len(points)-2)
        codes += [Path.CLOSEPOLY]
    return points, codes

def shp2codes(*shpfiles, center=0, encoding='utf-8'):
    points, codes = [], []
    for shpfile in shpfiles:
        if isinstance(shpfile, str):
            shpfile = Reader(shpfile, encoding=encoding)
        shape = shpfile.shape()
        pts = np.array(shpfile.shape().points)
        pts[:, 0] -= center
        a, b = _parts2codes(pts, shape.parts)
        points.append(a)
        codes += b
    return np.vstack(points), codes

def codes2clip(points, codes, ax=None):
    if ax is None:
        ax = plt.gca()
    clip = Path(points, codes)
    clip = patches.PathPatch(clip, transform=ax.transData)
    return clip


def read_ascii(file,skip=1,dtype=float):
    f = open(file,'r')
    if skip>0:
        f.readlines(skip)
    data = []
    for line in f:
        d = [float(i) for i in line.split(' ') if i not in['','\n']]
        data.append(d)
    return np.array(data)


def maskout(x,y,points,groups=50):
    d = np.array(points)
    num = len(d)
    idx = np.argsort(d[:,0])
    d = d[idx,:]

    mask_shape = len(y),len(x)
    mask = np.zeros(mask_shape)
    size = np.round(num/groups)
    groups = np.int(np.ceil(num/size))
    x0 = np.zeros([groups])
    y0 = np.zeros([2,groups])

    for i in range(groups):
        st, ed = int(i*size), int(i*size+size)
        x0[i] = np.mean(d[st:ed,0])
        tmp = np.sort(d[st:ed,1])
        y0[0,i], y0[1,i] = tmp[0], tmp[-1]

    extend_x0 = np.hstack([np.array([x0[0]-0.001]),x0,np.array([x0[-1]+0.001])])
    p=np.argmin(np.abs(x.reshape(-1,1)-extend_x0),axis=1)
    start, end = np.where(p>0)[0][0],np.where(p<groups+1)[0][-1]

    for i in range(start,end+1):
        st = np.where(y>y0[0,p[i]-1])[0][0]
        ed = np.where(y<y0[1,p[i]-1])[0][-1]
        mask[st:ed+1,i] = 1

    mask = mask==0
    return mask

class Eof:

    def __init__(self,datasets,center=True):

        """
        data : an array with (n,***) shape. n is the time series grids
        return : an object with EOF analyzing methods
        """

        d = datasets.copy()
        n_times, *self._shape = d.shape
        d.shape = n_times, -1
        self._idx = np.isnan(d).any(axis=0)
        d = d[:,~self._idx]
        self.neofs = np.sum(~self._idx)
        if center:
            d = d-np.mean(d,0)
        cov = np.matmul(d.T,d)
        self._eig_val, self._eig_matrix = np.linalg.eig(cov)

        self._pcs = np.matmul(self._eig_matrix, d.T)

    def eofs(self,neofs=3):
        tmp = np.nan*np.zeros([neofs,np.prod(self._shape)])
        tmp[:,~self._idx] = self._eig_matrix[:,:neofs].T
        return tmp.reshape(neofs,*self._shape)

    def pcs(self,npcs=3):
        return self._pcs[:npcs].T

    def eigenvalues(self,neigs=None):
        if neigs is not None:
            r = self._eig_val[:neigs]
        else:
            r = self._eig_val
        return r

    def varianceFraction(self,neigs=None):
        return self.eigenvalues(neigs)/np.sum(self._eig_val)

class MultivariateEof:

    def __init__(self,datasets,center=True):

        data, info = self._merge_fields(datasets)
        self._shapes = info['shapes']
        self._slicers = info['slicers']
        self.solver = Eof(data,center=center)
        self.neofs = self.solver.neofs

    def eofs(self,neofs=3):
        modes = self.solver.eofs(neofs=neofs)
        return self._unwrap(modes)

    def pcs(self,npcs=3):
        return self.solver.pcs(npcs=npcs)

    def eigenvalues(self,neigs=None):
        return self.solver.eigenvalues(neigs)

    def varianceFraction(self,neigs=None):
        return self.solver.varianceFraction(neigs)


    def _unwrap(self, modes):
        """Split a returned mode field into component parts."""
        nmodes = modes.shape[0]
        modeset = [modes[:, slicer].reshape((nmodes,) + shape)
                   for slicer, shape in zip(self._slicers, self._shapes)]
        return modeset


    def _merge_fields(self, fields):
        """Merge multiple fields into one field.

        Flattens each field to (time, space) dimensionality and
        concatenates to form one field. Returns the merged array
        and a dictionary {'shapes': [], 'slicers': []} where the entry
        'shapes' is a list of the input array shapes minus the time
        dimension ans the entry 'slicers' is a list of `slice` objects
        that can be used to select each individual field from the merged
        array.

        """
        info = {'shapes': [], 'slicers': []}
        islice = 0
        for field in fields:
            info['shapes'].append(field.shape[1:])
            channels = np.prod(field.shape[1:])
            info['slicers'].append(slice(islice, islice + channels))
            islice += channels
        try:
            merged = np.concatenate(
                [field.reshape([field.shape[0], np.prod(field.shape[1:])])
                 for field in fields], axis=1)
        except ValueError:
            raise ValueError('all fields must have the same first dimension')
        return merged, info

def _get_shape(data,origin_scale,new_scale):
    origin_shape = data.shape
    origin_x_right = (origin_shape[1]-1)*origin_scale[0]
    origin_y_down = (origin_shape[0]-1)*origin_scale[1]
    s2, s1 = round(origin_x_right/new_scale[0])+1, round(origin_y_down/new_scale[1])+1
    s2 = s2+1 if s2*new_scale[0]<origin_x_right else s2
    s1 = s1+1 if s2*new_scale[1]<origin_y_down else s1
    return origin_shape,(s1,s2)

def inter(orgin,ref,n,shape):
    new_data = np.zeros(n)
    for i in range(n):
        index = int(i//ref)
        new_index = index if index == shape-1 else index+1
        delta = (i%ref)*(orgin[new_index]-orgin[new_index-1])/ref
        new_data[i] = orgin[index] + delta
    return new_data

def downscale(data,origin_scale,new_scale):
    origin_shape, new_shape = _get_shape(data,origin_scale,new_scale)
    new_data = np.zeros(new_shape)
    ref, conti = np.array(origin_scale)/np.array(new_scale), 0
    for j in range(0,new_shape[0]):
        index_origin = int(j//ref[1])
        if (conti==1)|(j%ref[1]==0):
            new_data[j, :], index_new = inter(data[index_origin, :], ref[0], new_shape[1], origin_shape[1]), j
            if index_origin+1<origin_shape[0]:
                gradi = inter(data[index_origin + 1, :], ref[0], new_shape[1], origin_shape[1]) - new_data[j, :]
        if (j%ref[1]+1)<=ref[1]:
            cul = new_data[index_new,:] if conti==0 else inter(data[index_origin, :], ref[0], new_shape[1], origin_shape[1])
            new_data[j,:] = cul + (j%ref[1])*gradi/ref[1]
            conti = 0
        elif (j%ref[1]+1)>ref[1]:
            conti = 1
            new_data[j, :] = new_data[index_new,:] + (j % ref[1]) * gradi/ref[1]
    return new_data




if __name__ == "__main__":
    arr = np.zeros([300, 20, 50])
    d = decompose_dim(arr, 0, [-1, 5, 2])
    print(d.shape)
    d = combine_dim(d, [0,1])
    print(d.shape)
    
