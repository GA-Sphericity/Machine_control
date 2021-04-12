from math import pi, sqrt
import turtle as t

def r(s):
    ''' returns the radius of a sphere with the same voulme as a cube with the side s'''
    k = ( 3 / (4*pi) )**(1/3)
    return k*s

def splice_single_vector(vector, radius, segment_length, stepper_length):
    vector_length = sqrt( vector["x"]**2 + vector["y"]**2 )
    vector_length_mm = vector_length * radius
    x_mm = vector["x"] * radius
    y_mm = vector["y"] * radius
    x_steps = int(x_mm / stepper_length + 0.5)
    y_steps = int(y_mm / stepper_length + 0.5)
    
    ratio = segment_length / vector_length_mm
    
    x_steps_per_segment = int(ratio*x_steps)
    y_steps_per_segment = int(ratio*y_steps)
    
    result = []
    x_steps_taken = 0
    y_steps_taken = 0
    while ( abs(x_steps_taken) + abs(x_steps_per_segment) < abs(x_steps)-1) or ( abs(y_steps_taken)+abs(y_steps_per_segment) < abs(y_steps)-1): # rör ej, det fungerar på något sätt
        result.append([x_steps_per_segment, y_steps_per_segment])
        x_steps_taken = sum( map(lambda a: a[0], result) )
        y_steps_taken = sum( map(lambda a: a[1], result) )
        
    x_steps_left = int(x_steps - x_steps_taken)
    y_steps_left = int(y_steps - y_steps_taken)
    if ( x_steps_left + y_steps_left ):
        result.append( [x_steps_left, y_steps_left] )
        
    return result
    
def splice_vectors(vector_list, radius, segment_length, stepper_length):
    result = []
    for v in vector_list:
        vector_tmp = splice_single_vector(v, radius, segment_length, stepper_length)
        for u in vector_tmp:
            result.append(u)
    return result

def convert_positions(position, radius, segment_length, stepper_length):
    result = [ {"x": p["x"]*radius/stepper_length, "y": p["y"]*radius/stepper_length } for p in position ]
    return result

def convert(movement, position, cube_side, segment_length, stepper_length):
    radius = r(cube_side)
    mov = splice_vectors(movement, radius, segment_length, stepper_length)
    pos = convert_positions(position, radius, segment_length, stepper_length)
    mov = [ {"x" : m[0], "y" : m[1]} for m in mov ]

    t.clear()
    scale = 0.025
    t.speed(500)
    t.penup()
    t.setpos(0,0)
    t.pendown()
    t.speed(50)
    t.setpos(pos[0]["x"]*scale, pos[0]["y"]*scale)
    for p in pos[1:]:
        t.setpos(p["x"]*scale, p["y"]*scale)
    
    return mov, pos

