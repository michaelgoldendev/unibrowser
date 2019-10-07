import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()

def f(x, y):
    return np.sin(x) + np.cos(y)

x = np.linspace(0, 2 * np.pi, 50)
y = np.linspace(0, 2 * np.pi, 50).reshape(-1, 1)
# ims is a list of lists, each row is a list of artists to draw in the
# current frame; here we are just animating one artist, the image, in
# each frame
ims = []
for i in range(600):
    #x += np.pi / 15.
    #y += np.pi / 20.
    im0 = np.ones((150,150))
    im0[0,0] = 0
    if np.mod(i,2) == 1:
        im1 = 1
        im0[50:100,50:100] = im1
        im = plt.imshow(im0, animated=True, cmap='Greys', )
    else:
        im1 = 0
        im0[50:100,50:100] = im1
        im = plt.imshow(im0, animated=True, cmap='Greys')

    ims.append([im])

f = 6
ani = animation.ArtistAnimation(fig, ims, interval=1000/(2*f), blit=True) # interval in ms
                               # repeat_delay=1000)

# ani.save('dynamic_images.mp4')

plt.show()