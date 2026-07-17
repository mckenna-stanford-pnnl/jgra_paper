#========================================================================
# Name: functions.py
# Author: McKenna W. Stanford
# Author Contact: mckenna.stanford@pnnl.gov
# Date Created: 02/04/2025
#
# Utility: Holds home-made functions that I use frequently.
#========================================================================

#=====================================
# Imports
#=====================================
import numpy as np
import matplotlib as mpl
import math

#---------------------------------------------------------------
# Finds the value in an array nearest to the input value
#---------------------------------------------------------------
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx

#---------------------------------------------------------------
# Converts a numpy datetime64 object to a python datetime object 
#---------------------------------------------------------------
def to_datetime(date):
    """
    Converts a numpy datetime64 object to a python datetime object 
    Input:
      date - a np.datetime64 object
    Output:
      DATE - a python datetime object
    """
    timestamp = ((date - np.datetime64('1970-01-01T00:00:00'))
                 / np.timedelta64(1, 's'))
    
    return datetime.datetime.fromtimestamp(timestamp, datetime.UTC)

#---------------------------------------------------------------
#---------------------------------------------------------------
class MidpointNormalize(mpl.colors.Normalize):
    def __init__(self, vmin=None, vmax=None, vcenter=None, clip=False):
        self.vcenter = vcenter
        super().__init__(vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        # Note also that we must extrapolate beyond vmin/vmax
        x, y = [self.vmin, self.vcenter, self.vmax], [0, 0.5, 1.]
        return np.ma.masked_array(np.interp(value, x, y,
                                            left=-np.inf, right=np.inf))

    def inverse(self, value):
        y, x = [self.vmin, self.vcenter, self.vmax], [0, 0.5, 1]
        return np.interp(value, x, y, left=-np.inf, right=np.inf)

#---------------------------------------------------------------
#---------------------------------------------------------------
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=256):
    """ Truncate colormap.
    """
    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

#---------------------------------------------------------------
#---------------------------------------------------------------
def calc_latlon(lon1, lat1, dist, angle):
    """
    Haversine formula to calculate lat/lon locations from distance and angle.
    
    lon1:   longitude in [degree]
    lat1:   latitude in [degree]
    dist:   distance in [km]
    angle:  angle in [degree]
    """


    # Earth radius
    # R_earth = 6378.39  # at Equator [km]
    R_earth = 6374.2  # at 40 degree latitude [km]
#     R_earth = 6356.91  # at the pole [km]

    # Conver degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    bearing = math.radians(angle)

    lat2 = math.asin(math.sin(lat1) * math.cos(dist/R_earth) +
                     math.cos(lat1) * math.sin(dist/R_earth) * math.cos(bearing))
    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(dist/R_earth) * math.cos(lat1),
                             math.cos(dist/R_earth) - math.sin(lat1) * math.sin(lat2))
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    return lon2, lat2

#---------------------------------------------------------------
#---------------------------------------------------------------
def var_filled_hist2d(x,y,z,xbins,ybins):
    nx = len(xbins)-1
    ny = len(ybins)-1
    mean_z = np.zeros([nx,ny])
    for ii in range(nx):
        for jj in range(ny):
            dumid = np.where( (x >= xbins[ii]) & (x < xbins[ii+1]) & (y >= ybins[jj]) & (y < ybins[jj+1]) )
            if np.size(dumid) > 0.:
                mean_z[ii,jj] = np.mean(z[dumid])

    return mean_z

#---------------------------------------------------------------
#---------------------------------------------------------------
def make_box_whisker(var_dict,ax,xvar):
    """
    Makes box and whisker plots given a dictionary of the percentiles, the input variable, and the axis on which to plot
    """
    tmp_50 = var_dict['50']
    tmp_75 = var_dict['75']
    tmp_25 = var_dict['25']
    tmp_10 = var_dict['10']
    tmp_90 = var_dict['90']
    
    
    nl = len(tmp_50)
    dx = np.diff(norm_lifetime)[0]
    
    ln = dx/4
    
    for ii in range(nl):
        ax.plot([xvar[ii]-ln,xvar[ii]+ln],[tmp_50[ii],tmp_50[ii]],lw=1,c='maroon')
        
    #-------------------
    # Upper quartile
    #-------------------
    for ii in range(nl):
        x0 = xvar[ii]-ln
        y0 = tmp_50[ii]
        hgt = tmp_75[ii]-tmp_50[ii]
        wdth = (xvar[ii]+ln)-(xvar[ii]-ln)
        ax.add_patch(Rectangle((x0,y0),wdth,hgt,lw=1, ec="maroon", fc="red",alpha=0.25))
        
    #-------------------
    # Lower quartile
    #-------------------
    for ii in range(nl):
        x0 = xvar[ii]-ln
        y0 = tmp_25[ii]
        hgt = tmp_50[ii]-tmp_25[ii]
        wdth = (xvar[ii]+ln)-(xvar[ii]-ln)
        ax.add_patch(Rectangle((x0,y0),wdth,hgt,lw=1, ec="maroon", fc="red",alpha=0.25))   
        
    #-------------------
    # Whiskers
    #-------------------
    # 90
    for ii in range(nl):
        ax.plot([xvar[ii],xvar[ii]],[tmp_75[ii],tmp_90[ii]],lw=0.5,c='maroon')
        
    # 10
    for ii in range(nl):
        ax.plot([xvar[ii],xvar[ii]],[tmp_10[ii],tmp_25[ii]],lw=0.5,c='maroon')    
    

