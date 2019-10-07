import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

im1 = np.zeros((50,50))
im2 = np.zeros((50,50))
im2[20:30,20:30] = 1

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0,50), ylim=(0,50))
#fig, ax = plt.subplots()
im = ax.imshow(im1)
im.set_animated = True
#line, = ax.plot([], [], lw=2)

# initialization function: plot the background of each frame
def init():
    #line.set_data([], [])
    im.set_array(im1)
    return im#line,

# animation function.  This is called sequentially
def animate(i):
    #x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (0.9 * i))
    im.set_data(im2*y)
    #line.set_data(x, y)
    return im#line,

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=5, blit=True)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
# anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()