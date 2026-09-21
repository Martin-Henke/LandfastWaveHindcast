#This script contains functions to initialize plots with cartopy for Arctic projections.
#Many setting are hardcoded to maintain consistency across plotting script.s

import numpy as np
import cartopy.crs as ccrs
import cartopy.feature
import shapely
import matplotlib.tri as tri


def get_projection(extent, rotation = 0):
    """Set the projection of a Cartopy axis."""
    lon1,lon2,lat1,lat2 = extent[0],extent[1],extent[2],extent[3]
    centlong = (lon1+lon2)/2
    centlat = (lat1+lat2)/2
    proj = ccrs.LambertConformal(central_longitude=centlong+rotation,central_latitude=centlat)
    return proj

def get_extent(option = None):
    if option == None:
        print("No extent option provided - returning None")
        extent = None
    elif option == 'beaufort':
        x1,y1 = -157, 70.4
        x2,y2 = -141, 70.5
        extent = [x1, x2, y1, y2]
        rotation = -20
    elif option == 'chukchi':
        x1,y1 = -166.25, 65.6
        x2,y2 = -160, 71.65
        extent = [x1, x2, y1, y2]
        rotation = -15
    elif option == 'main':
        extent = [-169.3,-142, 65, 71.65]
        rotation = 0
    else:
        print("Extent option not recognized - returning None")
        extent = None
    return extent,rotation


def get_gridlines(ax,region = 'main',lw=0.75):
    if region == 'main':
        xticks = np.arange(-170, 190, 5)
        yticks = np.arange(55, 83, 1)
    elif region == 'chukchi':
        xticks = np.arange(-170, -150, 2.5)
        yticks = np.arange(65, 75, 2)
    elif region == 'beaufort':
        xticks = np.arange(-160, -130, 5)
        yticks = np.arange(67, 73.8, 0.5)
    else:#raise error
        raise ValueError("Unknown region specified")

    gl = ax.gridlines(draw_labels=True, linestyle='--',
                      xlocs=xticks, ylocs=yticks, alpha=0.75,
                      x_inline=False, y_inline=False,
                      linewidth=lw,
                      xpadding=10)
    return gl


def gl_styler(gl,l=False,r=False,t=False,b=False,fontsize=12):
    gl.bottom_labels = b
    gl.top_labels = t
    gl.right_labels = r
    gl.left_labels = l
    gl.xlabel_style = {'size': fontsize, 'rotation': 0, 'color': 'darkslategrey','ha':'center'}  # <-- Add pad here
    gl.ylabel_style = {'size': fontsize, 'rotation': 0, 'color': 'darkslategrey'} 
    return gl

def transformed_triangulation(lon,lat,elements,proj):
    xnew, ynew, _ = proj.transform_points(ccrs.PlateCarree(), lon, lat).T  #project the lon/lat to the map projection
    triang = tri.Triangulation(xnew,ynew, triangles=elements)
    return triang

def add_label(ax, label, dx=0.01,dy=0.98,fontsize=18):
    ax.text(dx, dy, label, transform=ax.transAxes, fontsize=fontsize,
         bbox=dict(facecolor='white', edgecolor='black',alpha=0.8, boxstyle='round,pad=0.2'))



def arctic_projection(option = None):
    if option == None:
        extent = [-168,-139 ,68,72]
        lon1,lon2,lat1,lat2 = extent[0],extent[1],extent[2],extent[3]
    elif option == 'beaufort':
        extent = [-156.5,-141 ,69.55,71.45]
        lon1,lon2,lat1,lat2 = extent[0],extent[1],extent[2],extent[3]
    elif option == 'chukchi':
        extent = [-169,-156.4,65.6,71.45]
        lon1,lon2,lat1,lat2 = extent[0],extent[1],extent[2],extent[3]
    elif option == 'arctic':
        extent = [150,230 ,55,83]
        lon1,lon2,lat1,lat2 = extent[0],extent[1],extent[2],extent[3]
    elif option == 'utq':
        extent = [-157.0, -155.0, 71.1, 71.5]
        lon1,lon2,lat1,lat2 = extent[0],extent[1],extent[2],extent[3]
    elif option == 'alaska':
        extent = [-169.3,-142, 65, 71.65]
        lon1,lon2,lat1,lat2 = extent[0],extent[1],extent[2],extent[3]
    elif option == 'northcoast':
        extent = [-164,-145,69.25,71.45]
        lon1,lon2,lat1,lat2 = extent[0],extent[1],extent[2],extent[3]

    centlong = (lon1+lon2)/2
    centlat = (lat1+lat2)/2
    #proj = ccrs.AlbersEqualArea(central_longitude=centlong,central_latitude=centlat)
    proj = ccrs.LambertConformal(central_longitude=centlong,central_latitude=centlat)
    #proj = ccrs.Stereographic(central_longitude=centlong,central_latitude=centlat)
    #proj = ccrs.NorthPolarStereo(central_longitude=centlong)
    return proj,extent

def transform_coordinates(lon,lat,proj):
    lon2d, lat2d = np.meshgrid(lon, lat)
    xnew, ynew, _ = proj.transform_points(ccrs.PlateCarree(), lon2d, lat2d).T
    return xnew.T, ynew.T


def init_axes(ax,extent,shapes = None, xlabels = False,ylabels = False,lines= True):
    #ax.set_facecolor((0.9, 0.9, 0.9))
    ax.set_facecolor('snow')
    
    step = 1
    ax.set_extent(extent, crs=ccrs.PlateCarree())
    if shapes:
        for shape in shapes:
            #continue
            ax.add_geometries([shapely.geometry.shape(shape)], ccrs.PlateCarree(), facecolor='snow', edgecolor='dimgrey', linewidth=0.1,zorder=2)
    else:
        ax.add_feature(cartopy.feature.LAND, zorder=2, edgecolor='black',facecolor='gainsboro', linewidth=0.25)
    extent = np.array(extent)
    extent = np.where(extent<0,extent+360,extent)
    xticks = np.arange(int(extent[0]), int(extent[1])+step, step)
    xticks = np.arange(-170,190,10)
    yticks = np.arange(int(extent[2]), int(extent[3])+step, step)
    
    gl = ax.gridlines(draw_labels=False, linestyle = '--',
                            xlocs = xticks, ylocs = yticks,alpha = 0.75,
                            x_inline = False, y_inline = False,
                            zorder = 102,linewidth = 0.5)
    gl.top_labels = False
    gl.right_labels = False
    
    #Lon labels
    if xlabels:
        gl.bottom_labels = True    
        gl.xlabel_style = {'size': 10, 'rotation': 45}
    else:
        gl.bottom_labels = False
    
    #Lat labels
    if ylabels:
        gl.left_labels = True
        gl.ylabel_style = {'size': 10}
    else:
        gl.left_labels = False

    #Lines
    if lines:
        gl.xlines = True
        gl.ylines = True
    
    return ax,gl 
