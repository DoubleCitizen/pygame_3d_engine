from manim import *
import numpy as np


CODE_TRANSLATION = """relative_XYZ = XYZ - camera_pos
X, Y, Z = relative_XYZ"""

CODE_YAW = """yaw = -angle_yaw

X_new = X * np.cos(yaw) - Z * np.sin(yaw)
Z_new = X * np.sin(yaw) + Z * np.cos(yaw)
X, Z = X_new, Z_new"""

CODE_PITCH = """pitch = -angle_pitch

Y_new = Y * np.cos(pitch) - Z * np.sin(pitch)
Z_new = Y * np.sin(pitch) + Z * np.cos(pitch)
Y, Z = Y_new, Z_new"""

CODE_PROJECTION = """x_proj = (X * focal_length) / Z
y_proj = (Y * focal_length) / Z

screen_x = screen_width / 2 + x_proj
screen_y = screen_height / 2 - y_proj"""


def make_code_box(code_str: str, highlight_lines: list = None) -> VGroup:
    """Returns a styled code box positioned on the right side of screen."""
    bg = Rectangle(width=5.5, height=3.2, fill_color="#1e1e1e", fill_opacity=1,
                   stroke_color=GREY, stroke_width=1)
    lines = code_str.strip().split("\n")
    text_group = VGroup()
    for i, line in enumerate(lines):
        color = YELLOW if (highlight_lines and (i + 1) in highlight_lines) else WHITE
        t = Text(line, font="Courier New", font_size=18, color=color)
        text_group.add(t)
    text_group.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    text_group.move_to(bg.get_center())
    group = VGroup(bg, text_group)
    group.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)
    return group


class CameraPipelineScene(ThreeDScene):
    def construct(self):
        self.act_translation()
        self.act_yaw()
        self.act_pitch()
        self.act_projection()

    # ------------------------------------------------------------------
    def act_translation(self):
        title = Text("Шаг 1: Сдвиг (Translation)", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))

        # Axes
        axes = ThreeDAxes(
            x_range=[-4, 4], y_range=[-3, 3], z_range=[-4, 4],
            x_length=5, y_length=4, z_length=5,
            axis_config={"color": GREY}
        )
        axes.scale(0.7).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        labels = axes.get_axis_labels(
            Text("X", font_size=20), Text("Y", font_size=20), Text("Z", font_size=20)
        )

        # World point P and camera C
        world_point = np.array([1.5, 0.8, 1.2])
        camera_pos  = np.array([-1.0, -0.5, -0.8])

        p_dot = Dot3D(axes.c2p(*world_point), color=GREEN, radius=0.08)
        c_dot = Dot3D(axes.c2p(*camera_pos),  color=RED,   radius=0.08)
        p_label = Text("P (точка мира)", font_size=18, color=GREEN).next_to(p_dot, UP, buff=0.15)
        c_label = Text("C (камера)",     font_size=18, color=RED  ).next_to(c_dot, DOWN, buff=0.15)

        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(axes), Write(labels))
        self.play(FadeIn(p_dot), Write(p_label), FadeIn(c_dot), Write(c_label))
        self.wait(1)

        # Formula
        formula = MathTex(r"\vec{r} = P - C", font_size=36, color=WHITE)
        formula.next_to(title, DOWN, buff=0.4).shift(LEFT * 2)
        self.play(Write(formula))

        # Animate: move camera to origin, shift world point accordingly
        relative = world_point - camera_pos
        p_dot_new = Dot3D(axes.c2p(*relative), color=GREEN, radius=0.08)
        c_dot_new = Dot3D(axes.c2p(0, 0, 0),   color=RED,   radius=0.08)
        origin_label = Text("(0,0,0)", font_size=16, color=RED).next_to(c_dot_new, DOWN, buff=0.1)

        self.play(
            Transform(c_dot, c_dot_new),
            Transform(p_dot, p_dot_new),
            FadeOut(c_label), FadeOut(p_label),
        )
        self.play(Write(origin_label))

        # Code box
        code_box = make_code_box(CODE_TRANSLATION, highlight_lines=[1, 2])
        self.play(FadeIn(code_box))
        self.wait(2)

        self.play(FadeOut(VGroup(title, axes, labels, p_dot, c_dot, origin_label,
                                  formula, code_box)))

        # Reset camera orientation for subsequent 2D acts
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)

    # ------------------------------------------------------------------
    def act_yaw(self):
        title = Text("Шаг 2: Поворот Yaw (вокруг Y)", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))

        # Top-down 2D view: XZ plane
        axes2d = Axes(
            x_range=[-3, 3], y_range=[-3, 3],
            x_length=5, y_length=5,
            axis_config={"color": GREY, "include_tip": True},
        )
        axes2d.scale(0.75).to_edge(LEFT, buff=0.5)
        x_lbl = Text("X", font_size=20).next_to(axes2d.x_axis.get_end(), RIGHT, buff=0.1)
        z_lbl = Text("Z", font_size=20).next_to(axes2d.y_axis.get_end(), UP, buff=0.1)
        view_lbl = Text("Вид сверху (XZ)", font_size=20, color=GREY_B).next_to(axes2d, DOWN, buff=0.2)

        self.play(Create(axes2d), Write(x_lbl), Write(z_lbl), Write(view_lbl))

        # Forward arrow at yaw=0 (pointing along +Z, i.e. up in XZ view)
        yaw_tracker = ValueTracker(0)
        forward_arrow = always_redraw(lambda: Arrow(
            start=axes2d.c2p(0, 0),
            end=axes2d.c2p(
                -np.sin(yaw_tracker.get_value()) * 2,
                 np.cos(yaw_tracker.get_value()) * 2
            ),
            color=YELLOW, buff=0, stroke_width=4
        ))
        point_dot = always_redraw(lambda: Dot(
            axes2d.c2p(
                -np.sin(yaw_tracker.get_value()) * 1.5,
                 np.cos(yaw_tracker.get_value()) * 1.5
            ),
            color=GREEN, radius=0.1
        ))
        forward_lbl = Text("вперёд", font_size=18, color=YELLOW).next_to(forward_arrow, UP, buff=0.1)

        self.play(GrowArrow(forward_arrow), FadeIn(point_dot), Write(forward_lbl))

        # Rotation matrix formula
        matrix = MathTex(
            r"R_y = \begin{pmatrix} \cos\theta & 0 & \sin\theta \\ 0 & 1 & 0 \\ -\sin\theta & 0 & \cos\theta \end{pmatrix}",
            font_size=28
        ).next_to(title, DOWN, buff=0.35).shift(LEFT * 1.5)
        self.play(Write(matrix))

        # Animate yaw rotation
        self.play(yaw_tracker.animate.set_value(PI / 3), run_time=2, rate_func=smooth)
        self.wait(0.5)
        self.play(yaw_tracker.animate.set_value(-PI / 4), run_time=1.5, rate_func=smooth)
        self.wait(0.5)
        self.play(yaw_tracker.animate.set_value(0), run_time=1, rate_func=smooth)

        # Code box
        code_box = make_code_box(CODE_YAW, highlight_lines=[3, 4, 5])
        self.play(FadeIn(code_box))
        self.wait(2)

        self.play(FadeOut(VGroup(title, axes2d, x_lbl, z_lbl, view_lbl,
                                  forward_arrow, point_dot, forward_lbl,
                                  matrix, code_box)))

    def act_pitch(self):
        title = Text("Шаг 3: Поворот Pitch (вокруг X)", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))

        # Side 2D view: ZY plane
        axes2d = Axes(
            x_range=[-3, 3], y_range=[-3, 3],
            x_length=5, y_length=5,
            axis_config={"color": GREY, "include_tip": True},
        )
        axes2d.scale(0.75).to_edge(LEFT, buff=0.5)
        z_lbl = Text("Z", font_size=20).next_to(axes2d.x_axis.get_end(), RIGHT, buff=0.1)
        y_lbl = Text("Y", font_size=20).next_to(axes2d.y_axis.get_end(), UP, buff=0.1)
        view_lbl = Text("Вид сбоку (ZY)", font_size=20, color=GREY_B).next_to(axes2d, DOWN, buff=0.2)

        self.play(Create(axes2d), Write(z_lbl), Write(y_lbl), Write(view_lbl))

        pitch_tracker = ValueTracker(0)
        forward_arrow = always_redraw(lambda: Arrow(
            start=axes2d.c2p(0, 0),
            end=axes2d.c2p(
                 np.cos(pitch_tracker.get_value()) * 2,
                 np.sin(pitch_tracker.get_value()) * 2
            ),
            color=YELLOW, buff=0, stroke_width=4
        ))
        point_dot = always_redraw(lambda: Dot(
            axes2d.c2p(
                 np.cos(pitch_tracker.get_value()) * 1.5,
                 np.sin(pitch_tracker.get_value()) * 1.5
            ),
            color=GREEN, radius=0.1
        ))

        self.play(GrowArrow(forward_arrow), FadeIn(point_dot))

        matrix = MathTex(
            r"R_x = \begin{pmatrix} 1 & 0 & 0 \\ 0 & \cos\phi & -\sin\phi \\ 0 & \sin\phi & \cos\phi \end{pmatrix}",
            font_size=28
        ).next_to(title, DOWN, buff=0.35).shift(LEFT * 1.5)
        self.play(Write(matrix))

        self.play(pitch_tracker.animate.set_value(PI / 4), run_time=2, rate_func=smooth)
        self.wait(0.5)
        self.play(pitch_tracker.animate.set_value(-PI / 4), run_time=1.5, rate_func=smooth)
        self.wait(0.5)
        self.play(pitch_tracker.animate.set_value(0), run_time=1, rate_func=smooth)

        code_box = make_code_box(CODE_PITCH, highlight_lines=[3, 4, 5])
        self.play(FadeIn(code_box))
        self.wait(2)

        self.play(FadeOut(VGroup(title, axes2d, z_lbl, y_lbl, view_lbl,
                                  forward_arrow, point_dot, matrix, code_box)))

    def act_projection(self):
        title = Text("Шаг 4: Перспективная проекция", font_size=32, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))

        # Side view diagram: camera at origin, screen plane at z=f, point at z=Z
        focal = 2.5
        point_z = 4.5
        point_x = 1.5

        axes2d = Axes(
            x_range=[-2.5, 2.5], y_range=[-0.5, 5.5],
            x_length=4.5, y_length=5,
            axis_config={"color": GREY, "include_tip": True},
        )
        axes2d.scale(0.75).to_edge(LEFT, buff=0.5)
        x_ax_lbl = Text("X", font_size=20).next_to(axes2d.x_axis.get_end(), RIGHT, buff=0.1)
        z_ax_lbl = Text("Z", font_size=20).next_to(axes2d.y_axis.get_end(), UP, buff=0.1)

        self.play(Create(axes2d), Write(x_ax_lbl), Write(z_ax_lbl))

        # Camera (pinhole) at origin
        cam_dot = Dot(axes2d.c2p(0, 0), color=RED, radius=0.12)
        cam_lbl = Text("камера", font_size=18, color=RED).next_to(cam_dot, LEFT, buff=0.15)

        # Screen plane at Z = focal
        screen_line = Line(axes2d.c2p(-2, focal), axes2d.c2p(2, focal), color=BLUE, stroke_width=3)
        screen_lbl = Text("экран (Z=f)", font_size=18, color=BLUE).next_to(screen_line, RIGHT, buff=0.1)

        # 3D Point P
        p_dot = Dot(axes2d.c2p(point_x, point_z), color=GREEN, radius=0.1)
        p_lbl = Text("P(X, Z)", font_size=18, color=GREEN).next_to(p_dot, RIGHT, buff=0.1)

        # Ray from camera through P to screen
        proj_x = (point_x * focal) / point_z
        proj_dot = Dot(axes2d.c2p(proj_x, focal), color=YELLOW, radius=0.1)
        proj_lbl = Text("x_proj", font_size=18, color=YELLOW).next_to(proj_dot, UP, buff=0.1)

        ray = DashedLine(axes2d.c2p(0, 0), axes2d.c2p(point_x, point_z), color=GREY_B)

        self.play(FadeIn(cam_dot), Write(cam_lbl))
        self.play(Create(screen_line), Write(screen_lbl))
        self.play(FadeIn(p_dot), Write(p_lbl))
        self.play(Create(ray))
        self.play(FadeIn(proj_dot), Write(proj_lbl))

        # Similar triangles formula
        formula = MathTex(
            r"\frac{x_{proj}}{f} = \frac{X}{Z} \implies x_{proj} = \frac{X \cdot f}{Z}",
            font_size=30
        ).next_to(title, DOWN, buff=0.35).shift(LEFT * 1)
        self.play(Write(formula))
        self.wait(1)

        # Show effect of focal length
        focal_label = Text("focal_length влияет на угол обзора (FOV):", font_size=20, color=GREY_B)
        focal_label.next_to(formula, DOWN, buff=0.3).shift(LEFT * 0.5)
        self.play(Write(focal_label))

        # Final screen coordinate formula
        screen_formula = MathTex(
            r"screen\_x = \frac{W}{2} + x_{proj}",
            font_size=28, color=WHITE
        ).next_to(focal_label, DOWN, buff=0.25)
        self.play(Write(screen_formula))

        # Code box
        code_box = make_code_box(CODE_PROJECTION, highlight_lines=[1, 2, 4, 5])
        self.play(FadeIn(code_box))
        self.wait(3)

        self.play(FadeOut(VGroup(title, axes2d, x_ax_lbl, z_ax_lbl,
                                  cam_dot, cam_lbl, screen_line, screen_lbl,
                                  p_dot, p_lbl, ray, proj_dot, proj_lbl,
                                  formula, focal_label, screen_formula, code_box)))

    def act_stub(self, title_str, code_str, highlight_lines):
        title = Text(title_str, font_size=32, color=BLUE).to_edge(UP)
        code_box = make_code_box(code_str, highlight_lines)
        self.play(Write(title), FadeIn(code_box))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(code_box))
