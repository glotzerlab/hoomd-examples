import fresnel
import gsd
import gsd.fl
import gsd.hoomd
import numpy
import PIL
import IPython
import io
import math

device = fresnel.Device(mode='cpu');
tracer = fresnel.tracer.Direct(device, 300, 300)

def render_disks(gsd_file):
    global device;

    f = gsd.fl.GSDFile(gsd_file, 'rb')
    t = gsd.hoomd.HOOMDTrajectory(f)

    return render_disk_frame(t[-1])

def render_sphere_frame(frame, height=None):

    if height is None:
        if hasattr(frame, 'configuration'):
            Ly = frame.configuration.box[1]
            height = Ly * math.sqrt(3)
        else:
            Ly = frame.box.Ly;
            height = Ly * math.sqrt(3)

    scene = fresnel.Scene(device)
    g = fresnel.geometry.Sphere(scene, position=frame.particles.position, radius=numpy.ones(frame.particles.N)*0.5)
    g.material = fresnel.material.Material(solid=0.0, color=fresnel.color.linear([0.25,0.5,1]), primitive_color_mix=1.0)
    g.outline_width = 0.1
    scene.camera = fresnel.camera.Orthographic(position=(height, height, height), look_at=(0,0,0), up=(0,1,0), height=height)

    g.color[frame.particles.typeid == 0] = fresnel.color.linear([0.25,0.5,1])
    g.color[frame.particles.typeid == 1] = fresnel.color.linear([1.0,0.714,0.169])

    scene.background_color = (1,1,1)
    scene.light_direction = (4,3,0)

    return tracer.render(scene)

def render_disk_frame(frame, Ly=None):

    if Ly is None:
        if hasattr(frame, 'configuration'):
            Ly = frame.configuration.box[1]
        else:
            Ly = frame.box.Ly;

    scene = fresnel.Scene(device)
    g = fresnel.geometry.Sphere(scene, position=frame.particles.position, radius=frame.particles.diameter*0.5)
    g.material = fresnel.material.Material(solid=1.0, color=fresnel.color.linear([0.25,0.5,1]), primitive_color_mix=0.0)
    g.outline_width = 0.05
    scene.camera = fresnel.camera.Orthographic(position=(0, 0, 10), look_at=(0,0,0), up=(0,1,0), height=Ly)
    scene.background_color = (1,1,1)

    return tracer.render(scene)

def render_polygon_frame(frame, verts, Ly=None):

    if Ly is None:
        if hasattr(frame, 'configuration'):
            Ly = frame.configuration.box[1]
        else:
            Ly = frame.box.Ly;

    scene = fresnel.Scene(device)
    ang = numpy.arctan2(frame.particles.orientation[:,3], frame.particles.orientation[:,0])*2
    g = fresnel.geometry.Prism(scene, vertices=verts, position=frame.particles.position[:,0:2], angle=ang, height=numpy.ones(frame.particles.N)*0.5)
    g.outline_width = 0.05
    g.material = fresnel.material.Material(solid=1.0, color=fresnel.color.linear([0.25,0.5,1]))
    scene.camera = fresnel.camera.Orthographic(position=(0, 0, 10), look_at=(0,0,0), up=(0,1,0), height=Ly)
    scene.background_color = (1,1,1)

    return tracer.render(scene)

def display_movie(frame_gen, gsd_file):
    f = gsd.fl.GSDFile(gsd_file, 'rb')
    t = gsd.hoomd.HOOMDTrajectory(f)

    a = frame_gen(t[0]);

    im0 = PIL.Image.fromarray(a[:,:, 0:3], mode='RGB').convert("P", palette=PIL.Image.ADAPTIVE);
    ims = [];
    for f in t[1:]:
        a = frame_gen(f);
        im = PIL.Image.fromarray(a[:,:, 0:3], mode='RGB')
        im_p = im.quantize(palette=im0);
        ims.append(im_p)

    f = io.BytesIO()
    im0.save(f, 'gif', save_all=True, append_images=ims, duration=1000, loop=0)

    print("Size:", len(f.getbuffer())/1024, "KiB")
    return IPython.display.display(IPython.display.Image(data=f.getvalue()))
