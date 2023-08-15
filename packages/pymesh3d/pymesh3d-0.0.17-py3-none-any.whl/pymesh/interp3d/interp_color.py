import numpy as np
import matplotlib as mpl

def interp_color(iso_vals, **kwargs):

    cmap = kwargs.pop("cmap", "jet")
    vmax = kwargs.pop("vmax", iso_vals.max())
    vmin = kwargs.pop("vmin", iso_vals.min())
    
    xp = [vmin, vmax]
    fp = [0, 256]
    color = mpl.colormaps[cmap](np.interp(iso_vals, xp, fp))
    return color