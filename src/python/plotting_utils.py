import matplotlib

################################################################################
# Utility functions intended for use by other functions an classes in this module
################################################################################

def get_plottable( input_axis, object_type ):
    '''Get the children of the input axis which are the object type specified'''
    children = input_axis.get_children()
    objects  = [obj for obj in children if type(obj) == object_type]
    return objects
# end get_plottable
    

def get_plottables( input_axis, object_types ):
    '''Get the children of the input axis which are any of the object types specified'''    
    objects = []
    for obj_type in object_types:
        more_objects = get_plottable( input_axis, obj_type )
        objects.extend( more_objects )
    return objects
# end get_plottables


def get_lines( input_axis ):
    '''Get the children of the input axis which are line objects'''
    children = input_axis.get_children()
    lines    = [l for l in children if type(l) == matplotlib.lines.Line2D]
    return lines


def get_color_rgb( artist ):
    '''
    Attempts to get the color of the input artist as an RGB vector
    Colors are accessed differently depending on whether the artist
    is a line, collection, etc. Also, there may be more than one
    color (e.g., edge color versus face color), and sometimes the
    color is stored as a string (like this: 'b') instead of a vector
    '''
    artist_type = type(artist)
    if artist_type == matplotlib.lines.Line2D:
        color = artist.get_color()
    elif artist_type == matplotlib.collections.PathCollection:
        color = artist.get_facecolor()[0]
    else:
        print 'Could not get color RGB--assuming blue for no good reason'
        color = [0, 0, 1]

    color_rgb = matplotlib.colors.colorConverter.to_rgb( color )
    return color_rgb
# end get_color_rgb
