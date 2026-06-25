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
        self.act_stub(
            "Шаг 2: Поворот Yaw (вокруг Y)",
            CODE_YAW,
            highlight_lines=[3, 4, 5],
        )

    def act_pitch(self):
        self.act_stub(
            "Шаг 3: Поворот Pitch (вокруг X)",
            CODE_PITCH,
            highlight_lines=[3, 4, 5],
        )

    def act_projection(self):
        self.act_stub(
            "Шаг 4: Перспективная проекция",
            CODE_PROJECTION,
            highlight_lines=[1, 2],
        )

    def act_stub(self, title_str, code_str, highlight_lines):
        title = Text(title_str, font_size=32, color=BLUE).to_edge(UP)
        code_box = make_code_box(code_str, highlight_lines)
        self.play(Write(title), FadeIn(code_box))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(code_box))
