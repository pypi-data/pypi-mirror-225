"""
Some basic tools for interacting with shapefiles. afloat-extras and proper config file required for full functionality.
"""
import pandas as pd
import matplotlib.pyplot as plt 
import shapefile


def xyzbathy_2_contourshp(infiles, outfile, levels, field_name='DEPTH', ):
    """
    Function to convert xyz scatter data into shapefiles of contours. Nominally it is for bathymetry, 
    a different field_name can be used for other scalars. 

    Parameters
    ----------
        infiles: string or list 
            Path of xyx formatted csv [or iterable of paths]. Use the headers X, Y, Z [in capitals]
        outfile: string
            Path of the shapefile to be produced
        levels: iterable 
            The levels the contours are to be specified at. Takes an iterable of numeric values.
        field_name: string
            The field name that the scalar field (Z, column) will be written to in the shp file. Default is "DEPTH" 
    """

    if type(infiles) == str:
        infiles = [infiles]
    
    CSs = []
    
    for infile in infiles:
        
        print('Contouring {}'.format(infile))
        
        df = pd.read_csv(infile)

        CS = plt.tricontour(df.X, df.Y, df.Z, 15, levels=levels, linewidths=0.5, colors='k')
        CSs += [CS]
        
    print('Done contouring.')
    plt.show()

    if False:
        for CS in CSs:
            for ii, segs in enumerate(CS.allsegs):

                print('{} m: {}'.format(levels[ii], len(segs)))

                for seg in segs:

                    plt.plot(seg[:, 0], seg[:, 1], 'k:', linewidth=0.5)

    with shapefile.Writer(outfile, shapeType=3) as w:
    
        w.field(field_name, 'N') # N = numbers
        
        for CS in CSs:
            for ii, segs in enumerate(CS.allsegs):
                print('{} m: {}'.format(levels[ii], len(segs)))

                for seg in segs:
                    plt.plot(seg[:, 0], seg[:, 1], 'k:', linewidth=0.5) 
                    w.line([seg])
                    w.record(DEPTH=levels[ii])
                    
    return CSs