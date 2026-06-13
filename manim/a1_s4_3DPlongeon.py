from manim import *
import numpy as np

class GrandPlongeon3D(ThreeDScene):
    def construct(self):
        # 1. Configuration initiale de la caméra (Vue macro)
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES, zoom=0.5)
        
        # 2. Création du nuage de points abstrait
        points = VGroup()
        for _ in range(1500):
            # Positionnement aléatoire dans un cube
            pos = np.random.uniform(-4, 4, 3)
            dot = Dot3D(point=pos, radius=0.02, color=BLUE_A)
            points.add(dot)
            
        self.add(points)
        self.wait(1)

        # 3. Animation de plongée et zoom immersif
        self.move_camera(
            phi=105 * DEGREES,   # Changement d'angle
            theta=180 * DEGREES, # Rotation de la caméra
            zoom=8.0,            # Zoom massif (immersion)
            run_time=5,
            rate_func=exponential_decay # Accélération de l'effet
        )
        self.wait()