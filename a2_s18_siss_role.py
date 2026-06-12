from manim import *
import numpy as np

class SwissRoll(ThreeDScene):
    def construct(self):
        np.random.seed(42)
        n = 200
        t = 1.5 * np.pi * (1 + 2 * np.random.rand(n))
        h = np.random.rand(n) * 3 - 1.5
        t_norm = (t - t.min()) / (t.max() - t.min())

        def get_points(alpha):
            x = np.cos(t) * t * alpha + t / t.max() * 2.5 * (1 - alpha)
            y = h
            z = np.sin(t) * t * alpha
            pts = np.stack([x, y, z], axis=1)
            pts[:, 0] -= pts[:, 0].mean()
            pts[:, 2] -= pts[:, 2].mean()
            return pts

        pts3d = get_points(1.0)
        pts2d = get_points(0.0)

        dots = VGroup(*[
            Dot3D(pts3d[i], radius=0.05,
                  color=interpolate_color(BLUE, RED, float(t_norm[i])))
            for i in range(n)
        ])

        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        self.add(dots)

        title = Text("Swiss Roll 3D", font_size=32).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1)
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(3)
        self.stop_ambient_camera_rotation()

        title2 = Text("Projection → structure perdue", font_size=28).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title2)
        self.play(
            ReplacementTransform(title, title2),
            self.camera.phi_tracker.animate.set_value(0*DEGREES),
            run_time=2
        )
        self.wait(2)

        title3 = Text("Déroulage → structure préservée", font_size=28).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title3)
        self.play(
            ReplacementTransform(title2, title3),
            self.camera.phi_tracker.animate.set_value(75*DEGREES),
            self.camera.theta_tracker.animate.set_value(-90*DEGREES),
            *[dots[i].animate.move_to(pts2d[i]) for i in range(n)],
            run_time=4
        )
        self.wait(2)