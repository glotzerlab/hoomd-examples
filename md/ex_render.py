import fresnel
import gsd
import gsd.fl
import gsd.hoomd
import numpy

# temporary - eventually this helper will be part of Fresnel
import PIL.Image
import io
import IPython.display
def showarray(a, fmt='png'):
    f = io.BytesIO()
    PIL.Image.fromarray(a, mode='RGBA').save(f, fmt)
    return IPython.display.display(IPython.display.Image(data=f.getvalue()))

device = fresnel.Device();

def render_disks(gsd_file):
    global device;

    f = gsd.fl.GSDFile(gsd_file, 'rb')
    t = gsd.hoomd.HOOMDTrajectory(f)

    return render_disk_frame(t[-1])

def render_disk_frame(frame, Ly=None):

    if Ly is None:
        if hasattr(frame, 'configuration'):
            Ly = frame.configuration.box[1]
        else:
            Ly = frame.box.Ly;

    scene = fresnel.Scene(device)
    g = fresnel.geometry.Sphere(scene, position=frame.particles.position, radius=numpy.ones(frame.particles.N)*0.5)
    g.material = fresnel.material.Material(solid=1.0, color=(0.25,0.5,1), geometry_color_mix=0.0)
    cam = fresnel.camera.Orthographic(position=(0, 0, 10), look_at=(0,0,0), up=(0,1,0), height=Ly)
    whitted = fresnel.tracer.Whitted(device, 300, 300)
    whitted.set_camera(cam)
    return whitted.render(scene)

def render_polygon_frame(frame, verts, Ly=None):

    if Ly is None:
        if hasattr(frame, 'configuration'):
            Ly = frame.configuration.box[1]
        else:
            Ly = frame.box.Ly;

    scene = fresnel.Scene(device)
    ang = numpy.arctan2(frame.particles.orientation[:,3], frame.particles.orientation[:,0])*2
    g = fresnel.geometry.Prism(scene, vertices=verts, position=frame.particles.position[:,0:2], angle=ang, height=numpy.ones(frame.particles.N)*0.5)
    g.material = fresnel.material.Material(solid=1.0, color=(0.25,0.5,1), geometry_color_mix=0.0)
    cam = fresnel.camera.Orthographic(position=(0, 0, 10), look_at=(0,0,0), up=(0,1,0), height=Ly)
    whitted = fresnel.tracer.Whitted(device, 300, 300)
    whitted.set_camera(cam)
    return whitted.render(scene)

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
