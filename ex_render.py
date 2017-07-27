import fresnel
import gsd
import gsd.fl
import gsd.hoomd
import numpy
import PIL
import IPython
import io
import math
import sys

device = fresnel.Device(mode='cpu');
preview_tracer = fresnel.tracer.Preview(device, 300, 300, aa_level=3)
path_tracer = fresnel.tracer.Path(device, 300, 300)

blue = fresnel.color.linear([0.25,0.5,1])*0.9;
orange = fresnel.color.linear([1.0,0.714,0.169])*0.9

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
    scene.lights = fresnel.light.cloudy();
    g = fresnel.geometry.Sphere(scene, position=frame.particles.position, radius=numpy.ones(frame.particles.N)*0.5)
    g.material = fresnel.material.Material(solid=0.0, color=blue, primitive_color_mix=1.0, specular=1.0, roughness=0.2)
    g.outline_width = 0.07
    scene.camera = fresnel.camera.orthographic(position=(height, height, height), look_at=(0,0,0), up=(0,1,0), height=height)

    g.color[frame.particles.typeid == 0] = blue;
    g.color[frame.particles.typeid == 1] = orange;

    scene.background_color = (1,1,1)

    return path_tracer.sample(scene, samples=64, light_samples=20)

def render_disk_frame(frame, Ly=None):

    if Ly is None:
        if hasattr(frame, 'configuration'):
            Ly = frame.configuration.box[1]
        else:
            Ly = frame.box.Ly;

    scene = fresnel.Scene(device)
    g = fresnel.geometry.Sphere(scene, position=frame.particles.position, radius=frame.particles.diameter*0.5)
    g.material = fresnel.material.Material(solid=1.0, color=blue, primitive_color_mix=1.0)
    g.outline_width = 0.1
    scene.camera = fresnel.camera.orthographic(position=(0, 0, 10), look_at=(0,0,0), up=(0,1,0), height=Ly)

    g.color[frame.particles.typeid == 0] = blue;
    g.color[frame.particles.typeid == 1] = orange;

    scene.background_color = (1,1,1)

    return preview_tracer.render(scene)

def render_polygon_frame(frame, verts, Ly=None):

    if Ly is None:
        if hasattr(frame, 'configuration'):
            Ly = frame.configuration.box[1]
        else:
            Ly = frame.box.Ly;

    scene = fresnel.Scene(device)
    ang = numpy.arctan2(frame.particles.orientation[:,3], frame.particles.orientation[:,0])*2
    g = fresnel.geometry.Prism(scene, vertices=verts, position=frame.particles.position[:,0:2], angle=ang, height=numpy.ones(frame.particles.N)*0.5)
    g.outline_width = 0.1
    g.material = fresnel.material.Material(solid=1.0, color=blue)
    scene.camera = fresnel.camera.orthographic(position=(0, 0, 10), look_at=(0,0,0), up=(0,1,0), height=Ly)
    scene.background_color = (1,1,1)

    return preview_tracer.render(scene)

def display_movie(frame_gen, gsd_file):
    f = gsd.fl.GSDFile(gsd_file, 'rb')
    t = gsd.hoomd.HOOMDTrajectory(f)

    a = frame_gen(t[0]);

    if tuple(map(int, (PIL.__version__.split(".")))) < (3,4,0):
        print("Warning! Movie display output requires pillow 3.4.0 or newer.")
        print("Older versions of pillow may only display the first frame.")

    im0 = PIL.Image.fromarray(a[:,:, 0:3], mode='RGB').convert("P", palette=PIL.Image.ADAPTIVE);
    ims = [];
    for f in t[1:]:
        a = frame_gen(f);
        im = PIL.Image.fromarray(a[:,:, 0:3], mode='RGB')
        im_p = im.quantize(palette=im0);
        ims.append(im_p)

    f = io.BytesIO()
    im0.save(f, 'gif', save_all=True, append_images=ims, duration=1000, loop=0)

    if (sys.version_info[0] >= 3):
        size = len(f.getbuffer())/1024;
        if (size > 2000):
            print("Size:", size, "KiB")
    return IPython.display.display(IPython.display.Image(data=f.getvalue()))
