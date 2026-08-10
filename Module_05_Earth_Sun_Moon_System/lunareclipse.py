import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

frames = 120
shadow_positions = np.linspace(-2, 2, frames)

fig, ax = plt.subplots()
fig.patch.set_facecolor("black")
ax.set_facecolor("black")
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect("equal")
ax.set_title("Lunar Eclipse - Sept 7, 2025", color="white")

moon = plt.Circle((0, 0), 1, color="lightgray", zorder=1)
ax.add_patch(moon)

umbra = plt.Circle((-2, 0), 1.2, color="black", alpha=0.9, zorder=2)
ax.add_patch(umbra)

def get_moon_color(umbra_center_x):
    if abs(umbra_center_x) < 0.5:
        return (0.6, 0.1, 0.1)
    elif abs(umbra_center_x) < 1.5:
        return "dimgray"
    else:
        return "lightgray"

def animate(i):
    pos = shadow_positions[i]
    umbra.set_center((pos, 0))
    moon.set_color(get_moon_color(pos))
    
    if abs(pos) < 0.5:
        phase = "Total Eclipse (Blood Moon)"
    elif abs(pos) < 1.5:
        phase = "Partial Eclipse"
    else:
        phase = "Full Moon"
    
    ax.set_title(f"{phase} - Sept 7, 2025", color="white")
    return umbra, moon

ani = animation.FuncAnimation(fig, animate, frames=frames, interval=100, blit=True)
ani.save("lunar_eclipse_2025.mp4", writer="ffmpeg", fps=10)
plt.show()