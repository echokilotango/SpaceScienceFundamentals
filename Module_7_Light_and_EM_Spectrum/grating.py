import numpy as np
import math as m

# This is the main class encapsulating all simulation methods
class wave_simulation_AI:

    # Constructor of the class. It takes the following parameters:
    # dx_in - size of one pixel in the simulation grid
    # dt_in - time step
    # sz_x_in - height of the simulation grid / pixels
    # sz_y_in - width of the simulation grid / pixels
    # steps_in - number of steps in the simulation
    # broadcast_func_in - function defining the speed of wave propagation and the elements broadcasting the waves
    def __init__(self, dx_in, dt_in, sz_x_in, sz_y_in, steps_in, broadcast_func_in):
        self.dx = dx_in
        self.dt = dt_in
        self.sz_x = sz_x_in
        self.sz_y = sz_y_in
        self.steps = steps_in
        self.broadcast_func = broadcast_func_in

    # Inplementation of the laplace operator that is used in the wave equation
    # It takes the following parameters:
    # u_array - grid containing the displacement values
    # dx - step size to be used in the aproximation fo the second derivative
    def Laplace(self, u_array, dx):
        sz_x = u_array.shape[0]
        sz_y = u_array.shape[1]

        dx2 = np.zeros((sz_x, sz_y), float)
        dy2 = np.zeros((sz_x, sz_y), float)

        dx2[1:sz_x - 1, 1:sz_y - 1] = ((u_array[0:(sz_x - 2), 1:(sz_y - 1)] - u_array[1:(sz_x - 1),
                                                                              1:(sz_y - 1)]) / dx - (
                                       u_array[1:(sz_x - 1), 1:(sz_y - 1)] - u_array[2:sz_x, 1:(sz_y - 1)]) / dx) / dx
        dy2[1:sz_x - 1, 1:sz_y - 1] = ((u_array[1:(sz_x - 1), 0:(sz_y - 2)] - u_array[1:(sz_x - 1),
                                                                              1:(sz_y - 1)]) / dx - (
                                       u_array[1:(sz_x - 1), 1:(sz_y - 1)] - u_array[1:(sz_x - 1), 2:sz_y]) / dx) / dx

        return (dx2 + dy2)

    # A simple edge detector intended for signification of the steps in the refractive index
    # It takes the following parameters:
    # c_array - The grid contining the wave propagation speed values for every pixel
    def Edge_detect(self, c_array):
        sz_x = c_array.shape[0]
        sz_y = c_array.shape[1]
        dx = np.zeros((sz_x, sz_y), float)
        contour = np.zeros((sz_x, sz_y), float)
        dx[0:(sz_x - 1), 0:(sz_y - 1)] = (np.abs(c_array[0:(sz_x - 1), 1:(sz_y)] - c_array[1:(sz_x), 1:(sz_y)]) + np.abs(
            c_array[1:(sz_x), 0:(sz_y - 1)] - c_array[1:(sz_x), 1:(sz_y)]) > 0)
        contour[dx>0]=1

        return (contour)

    # The method that actually executes the simulation
    def run(self):

        u_array = np.zeros((self.sz_x, self.sz_y), float)
        u_array_v = np.zeros((self.sz_x, self.sz_y), float)

        arr_new_r = np.zeros((self.sz_x, self.sz_y), float)
        arr_new_g = np.zeros((self.sz_x, self.sz_y), float)
        arr_new_b = np.zeros((self.sz_x, self.sz_y), float)

        outputdata = np.zeros((self.sz_x, self.sz_y, 3), int)

        import matplotlib.pyplot as plt
        import matplotlib.animation as animation

        fig, ax = plt.subplots(figsize=(12, 10))
        fig.suptitle('Wave Simulation - EM Spectrum & Optics', fontsize=14, fontweight='bold')
        
        im = ax.imshow(outputdata, cmap='hot')
        ax.set_xticks([])
        ax.set_yticks([])
        
        time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, 
                            color='white', fontsize=12, fontweight='bold')

        def animate(frame):
            nonlocal u_array, u_array_v, arr_new_r, arr_new_g, arr_new_b, outputdata
            
            b_el, b_el_mask, c = self.broadcast_func(frame)

            u_array[b_el_mask == 1] = b_el[b_el_mask == 1]
            u_array_v = u_array_v + np.multiply(np.square(c), self.Laplace(u_array, self.dx) * self.dt)
            u_array = u_array + u_array_v * self.dt

            arr_new = u_array
            arr_new[b_el_mask == 1] = 0

            arr_new_r = np.maximum(arr_new, 0) / np.max(np.maximum(arr_new, 0) + 1e-10)
            arr_new_g = np.minimum(arr_new, 0) / np.min(np.minimum(arr_new, 0) + 1e-10)
            arr_new_b = np.ones((self.sz_x, self.sz_y), float)
            arr_new_b[b_el_mask == 1] = 1
            arr_new_b[self.Edge_detect(c) == 1] = 1
            
            # Mark prism outline as BLACK (mask value 2)
            arr_new_r[b_el_mask == 2] = 0
            arr_new_g[b_el_mask == 2] = 0
            arr_new_b[b_el_mask == 2] = 0

            outputdata[0:self.sz_x, 0:self.sz_y, 0] = arr_new_r[0:self.sz_x, 0:self.sz_y] * 255
            outputdata[0:self.sz_x, 0:self.sz_y, 1] = arr_new_g[0:self.sz_x, 0:self.sz_y] * 255
            outputdata[0:self.sz_x, 0:self.sz_y, 2] = arr_new_b * 255

            im.set_array(outputdata.astype(np.uint8))
            time_text.set_text(f'Step: {frame}/{self.steps}')
            
            return [im, time_text]

        ani = animation.FuncAnimation(fig, animate, frames=self.steps, interval=50, 
                                      blit=True, repeat=True)
        plt.tight_layout()
        plt.show()

# This function simulates a passage of a plane wave through a piece material with high refractive index
def broadcast_func_lin_wave(t):

    broadcast_el = np.zeros((1024, 1024), float)
    broadcast_el_mask = np.zeros((1024, 1024), int)

    broadcast_el[0:5, 0:1024] = 0
    broadcast_el_mask[0:5, 0:1024] = 1
    broadcast_el[5:15, 5:(1024-5)] = m.sin(2*m.pi*t*0.008)
    broadcast_el_mask[5:15, 5:(1024-5)] = 1

    c_const = 6
    c = np.ones((1024, 1024), float) * c_const
    c[502:542, (200):(1024-200)] = c_const * 0.5

    return broadcast_el, broadcast_el_mask, c

# This function simulates a passage of a plane wave through a prism with dispersion
def broadcast_func_prism_wave(t):

    broadcast_el = np.zeros((1024, 1024), float)
    broadcast_el_mask = np.zeros((1024, 1024), int)

    # Wave source - plane wave entering from left
    broadcast_el[0:5, 0:1024] = 0
    broadcast_el_mask[0:5, 0:1024] = 1
    broadcast_el[5:15, 5:(1024 - 5)] = m.sin(2 * m.pi * t * 0.024)
    broadcast_el_mask[5:15, 5:(1024 - 5)] = 1

    c_const = 6
    c = np.ones((1024, 1024), float) * c_const

    # TRIANGULAR PRISM - equilateral triangle centered in middle
    prism_top_x = 300
    prism_bottom_x = 800
    prism_top_y = 200
    prism_bottom_y = 800
    
    # Mark prism outline in broadcast_el_mask to show as BLUE (blue channel forced to 1)
    outline_thickness = 12
    
    # Left edge: from (300, 200) to (800, 800)
    for x in range(prism_top_x, prism_bottom_x):
        y = int(prism_top_y + (x - prism_top_x) * (prism_bottom_y - prism_top_y) / (prism_bottom_x - prism_top_x))
        for dy in range(-outline_thickness, outline_thickness):
            if 0 <= y + dy < 1024:
                broadcast_el_mask[x, y + dy] = 2  # Mark outline (will show as constant color)
                c[x, y + dy] = 6  # Normal wave speed at outline
    
    # Right edge: from (800, 200) to (300, 800) (mirrored)
    for x in range(prism_top_x, prism_bottom_x):
        y = int(prism_top_y + (prism_bottom_x - x) * (prism_bottom_y - prism_top_y) / (prism_bottom_x - prism_top_x))
        for dy in range(-outline_thickness, outline_thickness):
            if 0 <= y + dy < 1024:
                broadcast_el_mask[x, y + dy] = 2  # Mark outline
                c[x, y + dy] = 6
    
    # Bottom edge: horizontal line from (300, 800) to (800, 800)
    for x in range(prism_top_x, prism_bottom_x):
        for dy in range(-outline_thickness, outline_thickness):
            if 0 <= prism_bottom_y + dy < 1024:
                broadcast_el_mask[x, prism_bottom_y + dy] = 2  # Mark outline
                c[x, prism_bottom_y + dy] = 6
    
    # Fill INSIDE prism with slower wave speed (causes refraction/dispersion)
    for x in range(prism_top_x, prism_bottom_x):
        for y in range(prism_top_y, prism_bottom_y):
            # Check if inside triangle
            left_edge_y = prism_top_y + (x - prism_top_x) * (prism_bottom_y - prism_top_y) / (prism_bottom_x - prism_top_x)
            right_edge_y = prism_top_y + (prism_bottom_x - x) * (prism_bottom_y - prism_top_y) / (prism_bottom_x - prism_top_x)
            
            if y >= left_edge_y and y >= right_edge_y and y <= prism_bottom_y:
                if broadcast_el_mask[x, y] != 2:  # Don't overwrite outline
                    c[x, y] = 6 * 0.4  # Slower inside prism = refraction

    return broadcast_el, broadcast_el_mask, c

# This function simulates a passage of a plane wave through a lens
def broadcast_func_circlular_lens(t):
    broadcast_el = np.zeros((1024, 1024), float)
    broadcast_el_mask = np.zeros((1024, 1024), int)

    broadcast_el[0:5, 0:1024] = 0
    broadcast_el_mask[0:5, 0:1024] = 1
    broadcast_el[5:15, 5:(1024 - 5)] = m.sin(2 * m.pi * t * 0.020)
    broadcast_el_mask[5:15, 5:(1024 - 5)] = 1

    c_const = 6
    c = np.ones((1024, 1024), float) * c_const

    for y in range(100,1024 - 100):

        c[(542-round(m.pow(m.pow((1024-200)/2,2)-m.pow(-(y-100)+((1024-200)/2),2),0.5))):542, y] = c_const * 0.6

    return broadcast_el, broadcast_el_mask, c

# This function simulates a passage of a plane wave through a Fresnel lens
def broadcast_func_fresnel(t):
    broadcast_el = np.zeros((1024, 1024), float)
    broadcast_el_mask = np.zeros((1024, 1024), int)

    broadcast_el[0:5, 0:1024] = 0
    broadcast_el_mask[0:5, 0:1024] = 1

    if (t<800):
        broadcast_el[5:15, 5:(1024 - 5)] = m.sin(2 * m.pi * t * 0.024)
    broadcast_el_mask[5:15, 5:(1024 - 5)] = 1

    c_const = 6
    c = np.ones((1024, 1024), float) * c_const

    for y in range(100,1024 - 100):

        y_full=m.pow(m.pow((1024 - 200) / 2, 2) - m.pow(-(y - 100) + ((1024 - 200) / 2), 2), 0.5)
        my_lambda = 2*c_const * 0.5 * (1/0.024)*0.01/0.1

        c[(542-round(y_full-round(y_full/(my_lambda)-0.5)*(my_lambda))):542, y] = c_const * 0.5

    return broadcast_el, broadcast_el_mask, c

# This function simulates a passage of a plane wave through a blazed grating
def broadcast_func_blazed_grading(t):

    broadcast_el = np.zeros((1024, 1024), float)
    broadcast_el_mask = np.zeros((1024, 1024), int)

    broadcast_el[0:5, 0:1024] = 0
    broadcast_el_mask[0:5, 0:1024] = 1
    broadcast_el[5:15, 5:(1024 - 5)] = m.sin(2 * m.pi * t * 0.024)
    broadcast_el_mask[5:15, 5:(1024 - 5)] = 1

    c_const = 6
    c = np.ones((1024, 1024), float) * c_const

    for y in range(200,1024 - 200):
        y_full = (542 - round((y - 201) / 3))
        my_lambda = 2*c_const * 0.5 * (1 / 0.024) * 0.01 / 0.1

        c[(542-round(y_full-round(y_full/(my_lambda)-0.5)*(my_lambda))):542, y] = c_const * 0.5

    return broadcast_el, broadcast_el_mask, c

dx = 0.1
dt = 0.01
sz_x = 1024
sz_y = 1024
steps = 3000

my_sim = wave_simulation_AI(dx, dt, sz_x, sz_y, steps, broadcast_func_prism_wave)

my_sim.run()