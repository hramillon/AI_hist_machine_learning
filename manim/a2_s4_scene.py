from manim import *

class DimensionTransition(ThreeDScene):
    def construct(self):
        # Configuration de la caméra initiale (vue de face / 2D)
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        # 1. Étape 1D : Le Point
        point = Dot(point=ORIGIN, color=BLUE, radius=0.1)
        
        self.play(Create(point))
        self.wait(1)

        # 2. Étape 2D : Le Carré
        carre = Square(side_length=2, color=BLUE).move_to(ORIGIN)
        
        # Transformation du point en carré
        self.play(Transform(point, carre))
        self.wait(1)

        # 3. Étape 3D : Le Cube
        cube = Cube(side_length=2, fill_opacity=0.3, fill_color=BLUE, stroke_width=2, stroke_color=BLUE_D)
        
        # Passage de la caméra en vue 3D perspective pendant la transition en cube
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, run_time=1.5)
        self.play(Transform(point, cube), run_time=1)
        self.wait(1)

        # 4. Ajout des flèches de coordonnées (Axes 3D)
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        
        self.play(Create(axes), run_time=1)
        self.wait(0.5)

        # 5. Rotation continue du cube pour l'effet 3D
        self.begin_ambient_camera_rotation(rate=0.4)
        self.wait(4)
        self.stop_ambient_camera_rotation()