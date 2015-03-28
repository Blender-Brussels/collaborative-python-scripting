# http://codepad-demo.d250.hu/p/bpybgebxl.py
# More info about this pad: http://blender-brussels.github.io/articles/collaborative-python-scripting/
# The idea is to fetch this script and run it through Blender regularly. An experiment during #bpybgebxl.
# http://blender-brussels.github.io
# Hello visitors. Please add your name and say 'Hi!' in the chat ------------------------------------------------>
# what you might expect out of this script: https://pbs.twimg.com/media/CBMggbjUUAAa0eR.png:large
import datetime
import bpy
import math
import mathutils
import random # https://docs.python.org/2/library/random.html
matUID = 0
waveUID = 0
# utils
def newMaterial():
    global matUID
    # creation of a new material
    newmatname = 'text_mat' + str( matUID )
    bpy.data.materials.new( newmatname )
    matUID += 1
    return bpy.data.materials[ newmatname ]
def applyColRotSize( color, rot, size):
    # linking the new material to object
    bpy.context.object.active_material = newMaterial()
    # setting the color
    bpy.context.object.active_material.diffuse_color = ( color[0], color[1], color[2] )
    bpy.ops.transform.rotate( value = rot[0], axis=(1,0,0) )
    bpy.ops.transform.rotate( value = rot[1], axis=(0,1,0) )
    bpy.ops.transform.rotate( value = rot[2], axis=(0,0,1) )
    bpy.ops.transform.resize( value = size )
# creation functions
def addText( text = "bravo!" , pos=(0,0,0), size=(1,1,1), color=(1,1,1), rot=(0,0,0) ):
    '''
    Function to add some text at position (pos), with size, color and rotation 
    @errors:
    convertViewVec: called in an invalid context
    '''
    # Create text
    bpy.ops.object.text_add()
    # Switch to edit mode
    bpy.ops.object.editmode_toggle()
    bpy.ops.font.delete(type='ALL')
    bpy.ops.font.text_insert(text=text)
    # Exit of edit mode
    bpy.ops.object.editmode_toggle()
    
    bpy.context.object.data.align = 'CENTER'
    # Give some volume to the text
    bpy.context.object.data.extrude = 0.1
    bpy.ops.transform.translate( value = pos )
    applyColRotSize(color, rot, size)
def addSphere( pos=(0,0,0), size=(1,1,1), color=(1,1,1), rot=(0,0,0) ):
    bpy.ops.mesh.primitive_ico_sphere_add( subdivisions = 3, location= pos )
    bpy.ops.object.shade_smooth()
    applyColRotSize(color, rot, size)
# ref: http://wiki.theprovingground.org/blender-py-mathmesh
def mathmesh( definition=(100,100), freq=1, amp=1, scale=1, pos=(0,0,0), size=(1,1,1), color=(1,1,1), rot=(0,0,0) ):
        global waveUID
        # mesh arrays
        verts = []
        faces = []
        # mesh variables
        numX = definition[0]
        numY = definition[1]
        #fill verts array
        for i in range (0, numX):
                for j in range(0,numY):
                    x = scale * i
                    y = scale * j
                    z = scale*((amp*math.cos(i*freq))+(amp*math.sin(j*freq)))
                    vert = (x,y,z) 
                    verts.append(vert)
        #fill faces array
        count = 0
        for i in range (0, numY *(numX-1)):
                if count < numY-1:
                    A = i
                    B = i+1
                    C = (i+numY)+1
                    D = (i+numY)
                    face = (A,B,C,D)
                    faces.append(face)
                    count = count + 1
                else:
                    count = 0
        #create mesh and object
        newwavemeshname = "wave_mesh_" + str( waveUID )
        newwavename = "wave_" + str( waveUID )
        waveUID += 1 
        mesh = bpy.data.meshes.new( newwavemeshname )
        object = bpy.data.objects.new( newwavename, mesh )
        #set mesh location
        bpy.context.scene.objects.link(object)
        #create mesh from python data
        mesh.from_pydata(verts,[],faces)
        mesh.update(calc_edges=True)
        bpy.ops.object.select_all(action='DESELECT')
        eggplate = bpy.context.scene.objects[newwavename]
        eggplate.select = True
        bpy.ops.object.shade_smooth()
        bpy.ops.transform.translate( value = pos )
        applyColRotSize(color, rot, size)
        eggplate.active_material = newMaterial()
        eggplate.active_material.diffuse_color = ( color[0], color[1], color[2] )
        eggplate.active_material.use_transparency = True
        eggplate.active_material.alpha = 0.125
        eggplate.active_material.use_shadeless = True
        eggplate.active_material.type = 'WIRE'
        #eggplate.active_material.raytrace_mirror.use = True
        
# MAIN
bpy.context.scene.world.use_sky_blend = True
bpy.context.scene.world.horizon_color = ( random.random(), random.random(), random.random() )
bpy.context.scene.world.zenith_color = ( random.random(), random.random(), random.random() )
bpy.context.scene.objects['Cube'].select = True
bpy.ops.object.delete()
addText( 'YO!', pos=(0,-0.5,0) )
for i in range(300):
    newSize = random.uniform(0.5,3)
    addText( random.choice('+.:|-=o°'), 
            pos = (random.uniform(-7, 7), random.uniform(-7,7), random.uniform(-7, 7)), 
            size = (newSize, newSize, newSize),
            color = (random.random(),random.random(),random.random(), 1),
            rot = (random.uniform(-1,1), random.uniform(-1,1), random.uniform(-1,1)) ) 
for i in range(100):
    now = datetime.datetime.utcnow()
    angl = i / 100 * ( math.pi * 2 )
    s = 0.1 + (math.cos( angl * 5 )* 0.05)
    addSphere( 
        pos = ( math.cos( angl ) * 3, math.sin( angl ) * 3, math.tan( angl * float( now.strftime('%M') ) / 60 ) ),
        size = ( s,s,s ),
        color= ( abs(math.cos(angl)), abs(math.sin( angl)) , 0 ) )
for i in range( 20 ):
    mathmesh(
        amp= 0.5 + i * 0.1,
        freq = ( i + 0.01 ) * 0.1,
        pos = ( -4,-4, -3 + i * 0.2 ),
        size = ( 0.15,0.15,0.15 ),
        rot=( 0,0,0.01 * i ),
        color = (random.random(),random.random(),random.random())
        )
bpy.context.scene.objects['Lamp'].data.type = 'SUN'
bpy.context.scene.objects['Lamp'].data.energy = 0
# adapting the output path - one file per second, max
now = datetime.datetime.utcnow()
bpy.context.scene.render.filepath = '/tmp/bgebpybxl_' + now.strftime('%Y.%m.%d-%H.%M.%S') + '-'
for i in range( 17 ):
    bpy.ops.object.lamp_add( type='POINT' )
    bpy.context.object.data.energy = 0.7
    bpy.context.object.data.color = ( random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1))
    bpy.context.object.data.shadow_method = 'RAY_SHADOW'
    bpy.ops.transform.translate( value = (random.uniform(-5, 5), random.uniform(-5,5), random.uniform(-5, 5) ) )
bpy.context.scene.world.mist_settings.use_mist = True
bpy.context.scene.world.mist_settings.depth = 15
bpy.context.scene.world.mist_settings.start = 3
'''
#!/bin/sh    
# A shell script to download the python script and run it in Blender
curl http://codepad-demo.d250.hu/p/bpybgebxl.py/export/txt -o bpybgebxl.py
./blender --verbose --background --factory-startup --render-output // --python bpybgebxl.py --render-frame 1
'''
'''
# To convert the series of renders in a gif animation
convert -delay 50 -loop 0 -resize 50%  bgebpybxl_2015.03.28-*.png bpybgebxl.gif
'''
'''
# Continuous render
# =================
# Maybe not safe as you are running Python on your machine without knowing what's in the code. 
# And Python can do a lot of stuff...
#!/bin/sh
COUNTER=0
while [  $COUNTER -lt 100 ]; do
    COUNTER=`expr $COUNTER + 1`
    echo The counter is $COUNTER
    curl http://codepad-demo.d250.hu/p/bpybgebxl.py/export/txt -o bpybgebxl.py
    ./blender --background --factory-startup --render-output // --python bpybgebxl.py --render-frame 1
    mv 0001.png $COUNTER.png
    sleep 20
done
'''
# APPLY SCRIPT BEFORE RENDERING!

