from manim import *
import numpy as np

class Scene16(ThreeDScene):
    def construct(self):
        RED_COL   = "#E84855"
        BLUE_COL  = "#3A86FF"
        PLANE_COL = "#A8DADC"

        np.random.seed(42)
        n = 28

        angles_r = np.linspace(0, 2 * np.pi, n, endpoint=False)
        r_inner  = np.random.uniform(0.6, 1.1, n)
        red_pts  = [np.array([r_inner[i] * np.cos(angles_r[i]),
                               r_inner[i] * np.sin(angles_r[i]), 0]) for i in range(n)]

        angles_b = np.linspace(0, 2 * np.pi, n, endpoint=False)
        r_outer  = np.random.uniform(1.9, 2.5, n)
        blue_pts = [np.array([r_outer[i] * np.cos(angles_b[i]),
                               r_outer[i] * np.sin(angles_b[i]), 0]) for i in range(n)]

        # ── PARTIE 1 : vue 2D avec axes ───────────────────────────────
        axes_2d = Axes(
            x_range=[-3.5, 3.5, 1], y_range=[-3.5, 3.5, 1],
            x_length=7, y_length=7,
            axis_config={"color": GREY, "stroke_width": 2, "include_tip": True},
            x_axis_config={"numbers_to_include": [-3,-2,-1,1,2,3]},
            y_axis_config={"numbers_to_include": [-3,-2,-1,1,2,3]},
        )
        x_lab_2d = axes_2d.get_x_axis_label(MathTex("x_1"), direction=RIGHT)
        y_lab_2d = axes_2d.get_y_axis_label(MathTex("x_2"), direction=UP)

        self.play(Create(axes_2d), Write(x_lab_2d), Write(y_lab_2d), run_time=0.8)

        red_dots_2d  = VGroup(*[Dot(axes_2d.c2p(p[0], p[1]), radius=0.09, color=RED_COL)
                                 for p in red_pts])
        blue_dots_2d = VGroup(*[Dot(axes_2d.c2p(p[0], p[1]), radius=0.09, color=BLUE_COL)
                                 for p in blue_pts])

        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in red_dots_2d],  lag_ratio=0.04, run_time=1.0),
            LaggedStart(*[GrowFromCenter(d) for d in blue_dots_2d], lag_ratio=0.04, run_time=1.0),
        )
        self.wait(1.0)

        # ── TRANSITION vers 3D ────────────────────────────────────────
        self.play(FadeOut(VGroup(axes_2d, x_lab_2d, y_lab_2d,
                                 red_dots_2d, blue_dots_2d)), run_time=0.5)

        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES)

        axes_3d = ThreeDAxes(
            x_range=[-3.2, 3.2, 1], y_range=[-3.2, 3.2, 1], z_range=[0, 3.5, 1],
            x_length=6.4, y_length=6.4, z_length=3.5,
            axis_config={"color": GREY, "stroke_width": 1.5},
            tips=False
        )
        x_lab_3d = axes_3d.get_x_axis_label(MathTex("x_1"), direction=RIGHT)
        y_lab_3d = axes_3d.get_y_axis_label(MathTex("x_2"), direction=UP)
        z_lab_3d = MathTex("z", color=WHITE, font_size=32).next_to(
            axes_3d.get_z_axis().get_end(), OUT * 0.4 + UP * 0.3
        )

        # Équation de la 3e dimension, fixée à l'écran
        eq = MathTex(r"z = \sqrt{x_1^2 + x_2^2}", font_size=36, color="#FFD166")
        self.add_fixed_in_frame_mobjects(eq)
        eq.to_corner(UL, buff=0.4)

        self.play(Create(axes_3d), Write(x_lab_3d), Write(y_lab_3d), Write(z_lab_3d),
                  Write(eq), run_time=1.0)

        # Points à plat z=0
        flat_red  = VGroup(*[Dot3D(axes_3d.c2p(p[0], p[1], 0), radius=0.09, color=RED_COL)
                              for p in red_pts])
        flat_blue = VGroup(*[Dot3D(axes_3d.c2p(p[0], p[1], 0), radius=0.09, color=BLUE_COL)
                              for p in blue_pts])

        self.play(
            LaggedStart(*[FadeIn(d) for d in flat_red],  lag_ratio=0.04, run_time=0.8),
            LaggedStart(*[FadeIn(d) for d in flat_blue], lag_ratio=0.04, run_time=0.8),
        )
        self.wait(0.4)

        # Lift vers z = r
        def lifted(p, color):
            r = np.sqrt(p[0]**2 + p[1]**2)
            return Dot3D(axes_3d.c2p(p[0], p[1], r), radius=0.09, color=color)

        lifted_red  = VGroup(*[lifted(p, RED_COL)  for p in red_pts])
        lifted_blue = VGroup(*[lifted(p, BLUE_COL) for p in blue_pts])

        self.play(
            Transform(flat_red,  lifted_red,  run_time=1.4),
            Transform(flat_blue, lifted_blue, run_time=1.4),
        )
        self.wait(0.6)

        # Plan séparateur z = 1.5
        sep_z = 1.5
        sep_plane = Surface(
            lambda u, v: axes_3d.c2p(u * 3.0, v * 3.0, sep_z),
            u_range=[-1, 1], v_range=[-1, 1],
            resolution=(8, 8),
            fill_color=PLANE_COL, fill_opacity=0.45,
            stroke_color=PLANE_COL, stroke_width=1.0
        )
        self.play(Create(sep_plane), run_time=0.9)
        self.wait(1.5)

        # ── PARTIE 3 : retour 2D ──────────────────────────────────────
        self.play(FadeOut(VGroup(axes_3d, sep_plane, flat_red, flat_blue,
                                 x_lab_3d, y_lab_3d, z_lab_3d, eq)), run_time=0.6)
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)

        axes_2d_b = Axes(
            x_range=[-3.5, 3.5, 1], y_range=[-3.5, 3.5, 1],
            x_length=7, y_length=7,
            axis_config={"color": GREY, "stroke_width": 2, "include_tip": True},
            x_axis_config={"numbers_to_include": [-3,-2,-1,1,2,3]},
            y_axis_config={"numbers_to_include": [-3,-2,-1,1,2,3]},
        )
        x_lab_2db = axes_2d_b.get_x_axis_label(MathTex("x_1"), direction=RIGHT)
        y_lab_2db = axes_2d_b.get_y_axis_label(MathTex("x_2"), direction=UP)

        red_dots_f  = VGroup(*[Dot(axes_2d_b.c2p(p[0], p[1]), radius=0.09, color=RED_COL)
                                for p in red_pts])
        blue_dots_f = VGroup(*[Dot(axes_2d_b.c2p(p[0], p[1]), radius=0.09, color=BLUE_COL)
                                for p in blue_pts])

        sep_circle = Circle(radius=axes_2d_b.c2p(sep_z, 0)[0] - axes_2d_b.c2p(0, 0)[0],
                            color=PLANE_COL, stroke_width=4)

        self.play(Create(axes_2d_b), Write(x_lab_2db), Write(y_lab_2db), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(d) for d in red_dots_f],  lag_ratio=0.04, run_time=0.8),
            LaggedStart(*[FadeIn(d) for d in blue_dots_f], lag_ratio=0.04, run_time=0.8),
        )
        self.play(Create(sep_circle), run_time=1.0)
        self.play(sep_circle.animate.set_stroke(width=6).set_color(YELLOW), run_time=0.5)
        self.wait(2.5)