from manim import *
import numpy as np

class SwissRoll(ThreeDScene):
    def construct(self):
        np.random.seed(42)
        n = 300
        t = 1.5 * np.pi * (1 + 2 * np.random.rand(n))
        h = np.random.rand(n) * 2 - 1
        t_norm = (t - t.min()) / (t.max() - t.min())

        def make_pts(alpha_z=1.0, alpha_unroll=0.0):
            x = np.cos(t) * t * (1 - alpha_unroll) + t_norm * 4 * alpha_unroll
            y = h
            z = np.sin(t) * t * alpha_z * (1 - alpha_unroll)
            pts = np.stack([x, y, z], axis=1)
            pts[:, 0] = (pts[:, 0] - pts[:, 0].mean()) / pts[:, 0].std() * 2.0
            pts[:, 2] = (pts[:, 2] - pts[:, 2].mean()) / (pts[:, 2].std() + 1e-6) * 2.0 * alpha_z
            return pts

        colors = [interpolate_color(BLUE, RED, float(t_norm[i])) for i in range(n)]
        pts = make_pts()
        dots = VGroup(*[Dot3D(pts[i], radius=0.04, color=colors[i]) for i in range(n)])

        # ── 1. Vue 3D ───────────────────────────────────────────────────────
        self.set_camera_orientation(phi=65*DEGREES, theta=-60*DEGREES)
        title = Text("Swiss Roll — 3D", font_size=30).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.add(dots)
        self.play(Write(title), FadeIn(dots), run_time=2)
        self.wait(2)

        # ── 2. Projection ───────────────────────────────────────────────────
        pts_flat = make_pts(alpha_z=0.0)
        title2 = Text("Projection (dessus) → dimensions perdues", font_size=26).to_corner(UL)
        self.play(
            FadeOut(title),
            *[dots[i].animate.move_to(pts_flat[i]) for i in range(n)],
            self.camera.phi_tracker.animate.set_value(0*DEGREES),
            run_time=3
        )
        self.add_fixed_in_frame_mobjects(title2)
        self.play(Write(title2), run_time=1)
        self.wait(2)

        # ── 3. Déroulage ────────────────────────────────────────────────────
        pts_unrolled = make_pts(alpha_z=1.0, alpha_unroll=1.0)
        title3 = Text("Déroulage → structure préservée", font_size=28).to_corner(UL)
        self.play(
            FadeOut(title2),
            *[dots[i].animate.move_to(pts[i]) for i in range(n)],
            self.camera.phi_tracker.animate.set_value(65*DEGREES),
            run_time=2
        )
        self.add_fixed_in_frame_mobjects(title3)
        self.play(
            Write(title3),
            *[dots[i].animate.move_to(pts_unrolled[i]) for i in range(n)],
            self.camera.phi_tracker.animate.set_value(75*DEGREES),
            self.camera.theta_tracker.animate.set_value(-90*DEGREES),
            run_time=4
        )
        self.wait(2)