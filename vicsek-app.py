import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import time

st.markdown('''
# Simulating active matter
## The Vicsek Model

Original article [here](https://arxiv.org/pdf/cond-mat/0611743.pdf)
''')

with st.sidebar:
    with st.form("my_form"):
        v0 = st.number_input('Velocity', 0.5, 2.0, value = 1.0, step = 0.1)    
        eta = st.number_input('Random fluctuation in angle (in radians)', 0.0, 2.0, value = 0.5, step = 0.1)
        L = st.number_input('Sixe of box', 5, 20, value = 10, step = 5)
        R = st.number_input('Interaction radius', 1, 5, value = 1, step = 1)
        N = st.number_input('Number of birds', 100, 1000, value = 500, step = 100)
        Nt = st.number_input('Number of timesteps', 50, 100, value = 50, step = 10)
        dt = st.number_input('Time step', 0.1, 1.0, value = 0.2, step = 0.1)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")

# Initialize
np.random.seed(28)      # set the random number generator seed

# bird positions
x = np.random.rand(N,1)*L
y = np.random.rand(N,1)*L

# bird velocities
theta = 2 * np.pi * np.random.rand(N,1)
vx = v0 * np.cos(theta)
vy = v0 * np.sin(theta)

# Prep figure
fig = plt.figure(figsize=(4,4), dpi=80)
ax = plt.gca()

# Initial figure
plt.cla()
plt.quiver(x,y,vx,vy)
ax.set(xlim=(0, L), ylim=(0, L))
ax.set_aspect('equal')
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

the_plot = st.pyplot(plt)
time.sleep(0.1)

# Simulation Main Loop
for i in range(Nt):

    # move
    x += vx*dt
    y += vy*dt

    # apply periodic BCs
    x = x % L
    y = y % L

    # find mean angle of neighbors within R
    mean_theta = theta
    for b in range(N):
        neighbors = (x-x[b])**2+(y-y[b])**2 < R**2
        sx = np.sum(np.cos(theta[neighbors]))
        sy = np.sum(np.sin(theta[neighbors]))
        mean_theta[b] = np.arctan2(sy, sx)

    # add random perturbations
    theta = mean_theta + eta*(np.random.rand(N,1)-0.5)

    # update velocities
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)

    plt.cla()
    plt.quiver(x,y,vx,vy)
    ax.set(xlim=(0, L), ylim=(0, L))
    ax.set_aspect('equal')
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # plt.pause(0.001)
    the_plot.pyplot(plt)
    time.sleep(0.001)
