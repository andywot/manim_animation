from manim import *

START_ANGLE = 0
OPACITY_DECAY = 0.993


class CircularMotionDemo(GraphScene):
    def construct(self):
        circle = Circle(radius=3, color=BLUE)

        def get_radius(theta):
            return Line(ORIGIN, circle.point_at_angle(theta), color=ORANGE)

        def get_point(theta):
            return Dot(color=BLUE, radius=0.15).move_to(circle.point_at_angle(theta))

        path = VMobject(color=YELLOW)
        dot = get_point(START_ANGLE)
        line = get_radius(START_ANGLE)
        path.set_points_as_corners([dot.get_center(), dot.get_center()])


        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path.become(previous_path)

            CURRENT_OPACITY = path.get_stroke_opacity()
            path.set_stroke(opacity=CURRENT_OPACITY * OPACITY_DECAY)

        def update_group(vg, dt):
            theta = (interpolate(0, 6 * PI, dt) + START_ANGLE) % (2 * PI)
            r, p = vg
            r.become(get_radius(theta))
            p.become(get_point(theta))

        circle_group = VGroup(line, dot)
        path.add_updater(update_path)

        self.add(path, dot, line)
        self.play(UpdateFromAlphaFunc(circle_group, update_group, run_time=6, rate_func=double_smooth))
        self.wait()
