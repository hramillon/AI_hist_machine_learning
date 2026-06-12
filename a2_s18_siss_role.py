
from manim import *
import numpy as np
 
class SwissRoll(ThreeDScene):
    def construct(self):
        # Génération des points du Swiss roll
        np.random.seed(42)
        n = 300
        t = 1.5 * np.pi * (1 + 2 * np.random.rand(n))
        height = np.random.rand(n)
        
        # Couleurs selon t (position angulaire)
        colors = color_gradient([BLUE, GREEN, YELLOW, RED], n)
        color_map = [colors[i] for i in np.argsort(np.argsort(t))]
 
        def swiss_coords(alpha):
            # alpha=1 : Swiss roll 3D, alpha=0 : déplié 2D
            x = np.cos(t) * t * alpha + t * (1 - alpha) * 1.5
            y = height * 3 - 1.5
            z = np.sin(t) * t * alpha
            # normalisation
            x = (x - x.mean()) / x.std() * 1.5
            z = (z - z.mean()) / z.std() * 1.5 * alpha
            return x, y, z
 
        # Créer les dots
        alpha_tracker = ValueTracker(1.0)
 
        def make_dots():
            a = alpha_tracker.get_value()
            x, y, z = swiss_coords(a)
            grp = VGroup()
            for i in range(n):
                d = Dot3D(point=[x[i], y[i], z[i]], radius=0.05, color=color_map[i])
                grp.add(d)
            return grp
 
        dots = always_redraw(make_dots)
 
        # Titre
        title = Text("Swiss Roll — vue 3D", font_size=32).to_corner(UL)
 
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        self.add(dots)
        self.play(Write(title), run_time=1)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
 
        # Projection bête depuis le dessus
        title2 = Text("Projection du dessus → structure perdue", font_size=28).to_corner(UL)
        self.play(
            ReplacementTransform(title, title2),
            self.camera.phi_tracker.animate.set_value(0*DEGREES),
            run_time=2
        )
        self.wait(2)
 
        # Déroulage progressif
        title3 = Text("Déroulage → structure préservée", font_size=28).to_corner(UL)
        self.play(
            ReplacementTransform(title2, title3),
            self.camera.phi_tracker.animate.set_value(70*DEGREES),
            self.camera.theta_tracker.animate.set_value(-90*DEGREES),
            alpha_tracker.animate.set_value(0.0),
            run_time=4
        )
        self.wait(2)
 
