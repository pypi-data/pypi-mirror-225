#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright notice
# ----------------
#
# Copyright (C) 2013-2023 Daniel Jung
# Contact: proggy-contact@mailbox.org
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
#
"""Implement a class whose instances hold discretized data representing continuous functions.
"""
__version__ = '0.1.2'

import collections.abc
import scipy
import scipy.interpolate


#=========================#
# coFunc class definition #
#=========================#


class coFunc(collections.abc.Sequence):  # MutableSequence?
    """Represent a continuous function using discrete datapoints (x-y value
    pairs).  Because of the assumption that the x-y value pairs represent a
    computer approximation of some continuous function, various mathematical
    operations can be implemented that seem natural from a mathematical
    viewpoint, but not as trivial in a computer environment where data can have
    different x-axis discretisations etc.
    """
    def __init__(self, x=[], y=[], dtype=None, attrs={}):
        """Initialize the continuous function object.
        """

        # store data, force numpy arrays
        self.x = scipy.array(x, dtype=dtype).flatten()
        self.y = scipy.array(y, dtype=dtype).flatten()

        # check dimensions
        if len(self.x.shape) != 1 or len(self.y.shape) != 1 \
                or self.x.shape[0] != self.y.shape[0]:
            raise ValueError('bad data shape')

        # sort data
        self.sort()

        # initialize attribute structure
        self.attrs = attrs

    def sort(self):
        """Sort data points by x-values.
        """
        ind = scipy.argsort(self.x)
        self.x = self.x[ind]
        self.y = self.y[ind]

    def _interp(self, kind='linear', bounds_error=True, fill_value=scipy.nan):
        """Return 1D interpolation object of the data.
        """
        return scipy.interpolate.interp1d(self.x, self.y, copy=False,
                                          kind=kind, bounds_error=bounds_error,
                                          fill_value=fill_value)

    def __call__(self, x, kind='linear', bounds_error=True,
                 fill_value=scipy.nan):
        """Get the value of the quantity at any given position x. Interpolate
        if needed. If bounds_error is True, error if x is out of range.
        Otherwise, return fill_value for x values out of range.
        """
        return self._n2ptype(self.y.dtype)(self._interp(
            kind=kind,
            bounds_error=bounds_error,
            fill_value=fill_value)(x))

    def _commonx(self, other, res='coarsest', source='linspace'):
        """Merge x-axis discretizations of this object and another.

        If method is "linspace", make a new uniform spacing.
        If method is "original", use one of the original discretizations.

        If res (resolution) is "self" or "this", use the resolution of this
        object.
        If res is "other", use the resolution of the other object.
        If res is "coarsest", use the coarsest discretization of the two
        objects.
        If res is "finest", use the finest discretization of the two objects.
        If res is "medium", use a medium discretization
        (implies method "linspace").
        """

        # if an empty function object is given
        if len(self) == 0 or len(other) == 0:
            return scipy.empty(shape=(0,))

        # determine extremal values
        min1, max1 = min(self.x),  max(self.x)  # use self.box()[:2]
        min2, max2 = min(other.x), max(other.x)  # use other.box()[:2]
        newmin = max(min1, min2)
        newmax = min(max1, max2)

        # choose coarsest discretization
        ### maybe offer option to use "coarse", "fine", "medium" discretization
        cand1 = self.x[scipy.logical_and(self.x >= newmin, self.x <= newmax)]
        cand2 = other.x[scipy.logical_and(other.x >= newmin,
                                          other.x <= newmax)]
        if res is not None and 'other'.startswith(res):
            winner = cand2
        elif res is not None and \
                ('self'.startswith(res) or 'this'.startswith(res)):
            winner = cand1
        elif res is not None and 'finest'.startswith(res):
            winner = cand1 if len(cand1) > len(cand2) else cand2
        elif res is not None and 'medium'.startswith(res):
            source = 'linspace'
            winner = [0]*scipy.ceil(scipy.mean(len(cand1), len(cand2)))
        else:
            winner = cand1 if len(cand1) < len(cand2) else cand2

        if source is not None and 'linspace'.startswith(source):
            newx = scipy.linspace(newmin, newmax, len(winner))
        else:
            # res may not be "medium" here!
            newx = winner

        return newx

    def _mathop(self, other, otype):
        """Perform mathematical operation of type "otype" between this object
        and another object "other". If "other" is also an instance of this
        class, use interpolation.
        """
        if type(other) is type(self):
            x = self._commonx(other)
            # maybe do not use interpolation if x values are completely equal?
            if len(x) > 1:
                y = getattr(self._interp()(x), otype)(other._interp()(x))
            else:
                x = []
                y = []
            new_attrs = self.attrs.copy()
            new_attrs.update(other.attrs)
            return type(self)(x=x, y=y, attrs=new_attrs)
        else:
            # assume scalar operation
            return type(self)(x=self.x, y=getattr(self.y, otype)(other),
                              attrs=self.attrs)

    def __add__(self, other):
        return self._mathop(other, '__add__')

    def __radd__(self, other):
        return self._mathop(other, '__add__')

    def __sub__(self, other):
        return self._mathop(other, '__sub__')

    def __rsub__(self, other):
        return -self+other

    def __mul__(self, other):
        return self._mathop(other, '__mul__')

    def __rmul__(self, other):
        return self._mathop(other, '__mul__')

    #return self._mathop(other, '__div__')

    def __rdiv__(self, other):
        return self**(-1)*other

    def __pow__(self, other):
        return self._mathop(other, '__pow__')

    def __mod__(self, other):
        return self._mathop(other, '__mod__')

    def __neg__(self):
        return type(self)(x=self.x, y=-self.y, attrs=self.attrs)

    def noise(self):
        """Measure for the "noisiness" (roughly, inverse of "continuity") of
        the data. Key question: How well can the x-y value pairs be fitted by
        one continuous curve?
        """
        ### what about the function scipy.stats.signaltonoise?
        return scipy.mean(scipy.absolute(self.diff().y))

    def diff(self, n=1):
        """Calculate the n-th order differential of the function.
        """
        x, y = self.diff(n=n-1).xy() if n > 1 else self.xy()
        x = self._filter_double(x)
        return type(self)(x=.5*(x[1:]+x[:-1]),
                          y=scipy.diff(y)/scipy.diff(x))

    def centroid(self):
        """Return the geometric center of all x-y data points.
        """
        return scipy.mean(self.x), scipy.mean(self.y)

    def __abs__(self):
        return type(self)(x=self.x, y=abs(self.y))

    def box(self):
        """Return bounding box, i.e. [x_min, x_max, y_min, y_max].
        """
        return min(self.x), max(self.x), min(self.y), max(self.y)

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return len(self.x)

    def __str__(self):
        """Return short string representation.
        """
        if len(self.attrs) > 0:
            return '<%s with %i ' % (type(self).__name__, len(self.x)) + \
                   'x-y value pair%s ' % self._plural(len(self.x)) + \
                   'and %i ' % len(self.attrs) + \
                   'attribute%s>' % self._plural(len(self.attrs))
        else:
            return '<%s with %i x-y value ' % (type(self).__name__,
                                               len(self.x)) + \
                   'pair%s>' % self._plural(len(self.x))

    def __repr__(self):
        """Return string representation.
        """
        if len(self.attrs) > 0:
            return '%s(x=%s, y=%s, attrs=%s)' % (type(self).__name__,
                                                 repr(self.x),
                                                 repr(self.y),
                                                 dict(self.attrs))
        else:
            return '%s(x=%s, y=%s)' % (self.__class__.__name__, repr(self.x),
                                       repr(self.y))

    @staticmethod
    def _filter_double(x, small=1e-6):
        """Filter double entries in x. Method: Multiply double entries with one
        plus some small value (x=x*1.000001).
        """

        #unique = numpy.unique(x) #???
        #unique, ind, inverse = numpy.unique(x, return_index=True,
                                            #return_inverse=True)

        ### old slow approach
        for i in xrange(len(x)):
            where = x == x[i]
            if sum(where) > 1:
                x[where] = scipy.linspace(x[i], x[i]*(1+small), len(where))
        return x

    @staticmethod
    def _n2ptype(numpy_type):
        """Convert a numpy data type to a close native Python type.
        Reference: http://stackoverflow.com/questions/9452775/converting-numpy-
                dtypes-to-native-python-types
        """
        return type(scipy.zeros(1, numpy_type).tolist()[0])

    @staticmethod
    def _plural(number):
        """Returns an empty string if the given number equals 1 and "s"
        otherwise.
        """
        return '' if number == 1 else 's'

    def copy(self):
        """Return copy of this continuous function object.
        """
        return type(self)(x=self.x, y=self.y, attrs=self.attrs)

    def xy(self):
        """Return x and y data as tuple (similar to what zip() does, but more
        efficient, as the raw data arrays are directly returned).
        """
        return self.x, self.y

    def combine(self, *others, **kwargs):
        """Combine the x-y pairs of this continuous function object with those
        of the given others. Returns a new continuous function instance. If cut
        is True, only the intersection of the x-axes is used, the rest of the
        input functions is cut away. Raise an exception if the x-axes do not
        intersect.
        """

        # get keyword arguments
        cut = kwargs.pop('cut', False)
        if len(kwargs) > 0:
            raise TypeError('%s() got an unexpected keyword argument "%s"'
                            % (__name__, kwargs.keys()[0]))

        new = self.copy()
        for other in others:
            # check type
            if type(other) is not type(self):
                raise TypeError('expected instance of %s'
                                % type(self).__name__)

            # combine x-y value pairs
            x = scipy.r_[new.x, other.x]
            y = scipy.r_[new.y, other.y]
            #x = self._filter_double(x)

            if cut:
                # determine extremal values
                min1, max1 = new.box()[:2]  # min(new.x), max(new.x)
                min2, max2 = other.box()[:2]  # min(other.x), max(other.x)
                newmin = max(min1, min2)
                newmax = min(max1, max2)

                # find indices to cut away
                keep = scipy.logical_and(x >= newmin, x <= newmax)
                if len(keep) == 0:
                    raise ValueError('x-axes do not intersect')

                # cut away
                x = x[keep]
                y = y[keep]

        # make new object, merge attributes
        new_attrs = new.attrs.copy()
        new_attrs.update(other.attrs)
        new = type(self)(x, y, attrs=new_attrs)

        # return new object
        return new

    def cut(self, range=None, lower=None, upper=None):
        """Cut away all data points whose x-value is outside of the given
        "range", or those that are smaller than "lower" or greater than
        "upper".
        """

        # get range
        if range is None:
            # default range captures all values
            range = self.box()[:2]
        else:
            range = list(range)
            if scipy.array(range).shape != (2,):
                raise ValueError('range must be 2-tuple')

        # overwrite range with lower and upper value
        range = list(range)
        if lower is not None:
            range[0] = lower
        if upper is not None:
            range[1] = upper

        #if range[0] >= range[1]:
            #raise ValueError, 'lower bound must be smaller than upper bound'
        ### so then, nothing is kept, just fine

        # cut away data points
        keep = scipy.logical_and(self.x >= range[0], self.x <= range[1])
        self.x = self.x[keep]
        self.y = self.y[keep]

    def globalmin(self):
        """Return global minimum of the function.
        """
        raise NotImplementedError

    def globalmax(self):
        """Return global maximum of the function.
        """
        raise NotImplementedError

    def localmin(self, endpoints=False):
        """Return all local minima of the function. If endpoints is False,
        exclude the first and the last data point from the search.
        """
        raise NotImplementedError

    def localmax(self, endpoints=False):
        """Return all local maxima of the function. If endpoints is False,
        exclude the first and the last data point from the search.
        """
        raise NotImplementedError

    def add(self, *points):
        """Add data points (2-tuples) to the function.
        """
        try:
            points = scipy.array(points)
            assert len(points.shape) == 2
            assert points.shape[1] == 2
        except AssertionError:
            raise ValueError('data points must be 2-tuples')
        if len(self) == 0:
            self.x = scipy.array(points[:, 0])
            self.y = scipy.array(points[:, 1])
        elif len(self) == 1 and self.x == '__EMPTY__' \
                and self.y == '__EMPTY__':
            #print('case!')
            self.x = scipy.array(points[:, 0])
            self.y = scipy.array(points[:, 1])
            #print(self.x, self.y)
        else:
            self.x = scipy.r_[self.x, points[:, 0]]
            self.y = scipy.r_[self.y, points[:, 1]]
            self.sort()

    #def conv(self, other) # convolution with another function
    #def __eq__(self, other, )

    def a2cf(self, attrname):
        """Convert a sequence-like attribute to a coFunc object where the
        y-data is the attribute and the x-data is the original x-data of this
        coFunc object.
        """
        attr = self.attrs.get(attrname)
        if isinstance(attr, tuple):
            # e.g. in the case of confidence intervals
            return (type(self)(self.x, part) for part in attr)
        else:
            return type(self)(self.x, attr)


#================================================================#
# functions that operate on coFunc objects                       #
# additionally, you can use the builtin "sum", "min", "max" etc. #
#================================================================#


def mean(cofuncs):
    """Return the mean of the given coFunc objects.
    """
    # former cofunc.coFunc.mean from 2012-07-11
    return sum(cofuncs)/len(cofuncs)


def var(cofuncs):
    """Return the variance of the given coFunc objects.
    """
    m = mean(cofuncs)
    return mean([(cofunc-m)**2 for cofunc in cofuncs])


def intersection(cofuncs, enhance=1):
    """Return intersection of x-values of the given coFunc objects. Enhance the
    resolution of the new axis by the given factor.
    """

    # exclude the case of an empty list given
    if len(cofuncs) == 0:
        return scipy.empty(shape=(0,))

    # determine extremal values
    mins, maxs = [], []
    for cofunc in cofuncs:
        mi, ma = cofunc.box()[:2]
        mins.append(mi)
        maxs.append(ma)
    newmin = max(mins)
    newmax = min(maxs)

    # choose new discretization (worst resolution of the input coFunc objects)
    nums = []
    for cofunc in cofuncs:
        nums.append(sum(scipy.logical_and(cofunc.x >= newmin,
                                          cofunc.x <= newmax)))
    return scipy.linspace(newmin, newmax, min(nums)*enhance)


#def median(*cofuncs)


def combine(cofuncs, cut=False):
    """Combine the x-y pairs of the given continuous function objects. Return a
    new continuous function instance. If cut is True, only the intersection of
    the x-axes is kept, the rest of the input functions is cut away. In that
    case, raise an exception if the x-axes do not intersect.
    """
    return cofuncs[0].combine(*cofuncs[1:], cut=cut)


#=====================================#
# provide some ready-to-use functions #
#=====================================#


class Sin(coFunc):
    """Create coFunc object representing a sinusoidal function.
    """
    def __init__(self, range=(-10, 10), step=.1, amp=1, freq=1, phase=0):
        raise NotImplementedError


#========================#
# continuous 2D function #
#========================#


class coFunc2d(object):  # collections.abc.Sequence? collections.abc.MutableSequence?
    """Represent a continuous 2D function using discrete datapoints (x-y-z
    value triples).  Because of the assumption that the x-y-z value triples
    represent a computer approximation of a continuous 2D function, various
    mathematical operations can be implemented that seem like natural from a
    mathematical point of view, but not as trivial in a computer environment
    where the data can have different x- and y-axis discretisations etc.
    """
    # To do:
    # --> add math
    # --> return slices (intersections with planes) as 1D coFunc objects

    def __init__(self, x=[], y=[], z=[], dtype=None, attrs={}):
        """Initialize the continuous 2D function object.
        """
        
        # store data, force numpy arrays
        self.x = scipy.array(x, dtype=dtype).flatten()
        self.y = scipy.array(y, dtype=dtype).flatten()
        self.z = scipy.array(z, dtype=dtype).flatten()

        # check dimensions
        if len(self.x.shape) != 1 or len(self.y.shape) != 1 \
                or len(self.z.shape) != 1 \
                or self.x.shape[0] != self.y.shape[0] \
                or self.x.shape[0] != self.z.shape[0]:
            raise ValueError('bad data shape')

        # sort data
        #self.sort()

        # initialize attribute structure
        self.attrs = Bundle(**attrs)

    def _interp(self, kind='linear', bounds_error=True, fill_value=scipy.nan):
        """Return 2D interpolation object of the data.
        """
        return scipy.interpolate.interp2d(self.x, self.y, self.z, copy=False,
                                          kind=kind, bounds_error=bounds_error,
                                          fill_value=fill_value)

    def __call__(self, x, y, kind='linear', bounds_error=True,
                 fill_value=scipy.nan):
        """Get the function value at any given coordinate (x, y). Interpolate
        if needed. If bounds_error is True, error if (x, y) is out of range.
        Otherwise, return fill_value for (x, y) out of range.
        """
        return self._n2ptype(self.y.dtype)(self._interp(
            kind=kind,
            bounds_error=bounds_error,
            fill_value=fill_value)(x))

    def __abs__(self):
        """Return new coFunc2d object with the absolute z-values of this
        object.
        """
        return type(self)(x=self.x, y=self.y, z=abs(self.z))

    def box(self):
        """Return bounding box, i.e. [x_min, x_max, y_min, y_max, z_min,
        z_max].
        """
        return (min(self.x), max(self.x), min(self.y), max(self.y),
                min(self.z), max(self.z))

    def __getitem__(self, index):
        return self.x[index], self.y[index], self.z[index]

    def __len__(self):
        return len(self.x)

    def __str__(self):
        """Return short string representation.
        """
        if len(self.attrs) > 0:
            return '<%s with %i ' % (type(self).__name__, len(self.x)) + \
                   'x-y-z value triple%s ' % self._plural(len(self.x)) + \
                   'and %i ' % len(self.attrs) + \
                   'attribute%s>' % self._plural(len(self.attrs))
        else:
            return '<%s with %i x-y-z value ' % (type(self).__name__,
                                                 len(self.x)) + \
                   'triple%s>' % self._plural(len(self.x))

    def __repr__(self):
        """Return complete string representation.
        """
        if len(self.attrs) > 0:
            return '%s(x=%s, y=%s, z=%s, attrs=%s)' % (type(self).__name__,
                                                       repr(self.x),
                                                       repr(self.y),
                                                       repr(self.z),
                                                       dict(self.attrs))
        else:
            return '%s(x=%s, y=%s, z=%s)' % (self.__class__.__name__,
                                             repr(self.x), repr(self.y),
                                             repr(self.z))

    @staticmethod
    def _n2ptype(numpy_type):
        """Convert a numpy data type to a close native Python type.  Reference:
        http://stackoverflow.com/questions/9452775/converting-numpy-
        dtypes-to-native-python-types
        """
        # copied from coFunc._n2ptype
        return type(scipy.zeros(1, numpy_type).tolist()[0])

    @staticmethod
    def _plural(number):
        """Returns an empty string is the given number equals 1 and "s"
        otherwise.
        """
        # copied from coFunc._plural (written 2012-07-11)
        return '' if number == 1 else 's'

    def copy(self):
        """Return copy of this continuous 2D function object.
        """
        # based on coFunc.copy (written 2012-06-28)
        return type(self)(x=self.x, y=self.y, z=self.z, attrs=self.attrs)

    def xyz(self):
        """Return x, y and z data as tuple (similar to what zip() does, but
        more efficient, as the raw data arrays are directly returned).
        """
        return self.x, self.y, self.z

    def add(self, *points):
        """Add data points (3-tuples) to the function object.
        """
        # based on coFunc.add (written 2012-07-12)
        try:
            points = scipy.array(points)
            assert len(points.shape) == 2
            assert points.shape[1] == 3
        except AssertionError:
            raise ValueError('data points must be 3-tuples')
        if len(self) == 0:
            self.x = scipy.array(points[:, 0])
            self.y = scipy.array(points[:, 1])
            self.z = scipy.array(points[:, 2])
        else:
            self.x = scipy.r_[self.x, points[:, 0]]
            self.y = scipy.r_[self.y, points[:, 1]]
            self.z = scipy.r_[self.z, points[:, 2]]
            #self.sort()

    def a2cf(self, attrname):
        """Convert an array-like attribute to a coFunc2d object where the
        z-data is the attribute and the x- and y-data are the original x- and
        y-data of this coFunc2d object.
        """
        # based on coFunc.a2cf (developed 2012-11-12 until 2012-11-13)
        attr = self.attrs.get(attrname)
        if isinstance(attr, tuple):
            # e.g. in the case of confidence intervals
            return (type(self)(self.x, self.y, part) for part in attr)
        else:
            return type(self)(self.x, self.y, attr)


def __main__():
    import doctest
    doctest.testmod()
