from manim import *

RANGE = 3
START_ANGLE = 0.6


def correct_angle(angle):
    if angle < 0:
        return angle + 2 * PI
    else:
        return angle


class PolarCoordinate1(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            graph_origin=ORIGIN,
            x_min=-RANGE,
            x_max=RANGE,
            y_min=-RANGE,
            y_max=RANGE,
            x_axis_width=2 * RANGE,
            y_axis_height=2 * RANGE,
            x_axis_config={"tick_frequency": 2, "leftmost_tick": -2},
            y_axis_config={"tick_frequency": 2, "leftmost_tick": -2}
        )

    def construct(self):
        self.setup_axes(True)

        def get_radius(theta):
            return Line(ORIGIN, circle.point_at_angle(theta), color=ORANGE)

        def get_angle(theta):
            return Arc(start_angle=0, angle=theta, radius=circle.radius * 0.2, color=GREEN)

        def get_angle_shading(theta):
            return Sector(start_angle=0, angle=theta, outer_radius=circle.radius * 0.2, fill_color=GREEN,
                          fill_opacity=0.5)

        def get_point(theta):
            return Dot(color=BLUE).move_to(circle.point_at_angle(theta))

        circle = Circle(radius=2 * self.space_unit_to_x, color=BLUE)
        radius = get_radius(START_ANGLE)
        angle = get_angle(START_ANGLE)
        angle_shading = get_angle_shading(START_ANGLE)
        point = get_point(START_ANGLE)

        circle_group = VGroup(radius, angle, point, angle_shading)

        e_r = Arrow(point.get_center(), point.get_center() + radius.get_unit_vector(), buff=0)
        e_phi = Arrow(point.get_center(), point.get_center() + e_r.copy().rotate(PI / 2).get_unit_vector(), buff=0)

        p = MathTex(r"P", color=BLUE).move_to(point.get_center() + radius.get_unit_vector() * 0.5)
        r = MathTex(r"r", color=ORANGE).move_to(radius.get_center() + e_phi.get_unit_vector() * 0.3)
        phi = MathTex(r"\phi", color=GREEN).next_to(angle, RIGHT).shift(UP * 0.2)
        e_r_text = Text("radial basis vector").scale(0.5)
        e_phi_text = Text("tangential basis vector").scale(0.5)

        angleText, equal, angleNumber, piText = angleLabel = VGroup(
            MathTex(r"\phi", color=GREEN),
            MathTex(r"="),
            DecimalNumber(0, show_ellipsis=False, num_decimal_places=2, include_sign=False),
            MathTex(r"\pi")
        )
        angleLabel.arrange(RIGHT, buff=0.1).to_corner(UL)

        right_angle = Elbow(color=WHITE).set_points_as_corners([point.get_center() + e_phi.get_unit_vector(),
                                                                point.get_center() + e_r.get_unit_vector() + e_phi.get_unit_vector(),
                                                                point.get_center() + e_r.get_unit_vector()]).scale_to_fit_width(
            0.3, about_point=point.get_center())

        def update_angleValue(v):
            v.set_value(correct_angle(radius.get_angle()) / PI)

        def update_pText(p):
            p.move_to(point.get_center() + radius.get_unit_vector() * 0.5)

        def update_rText(r):
            r.move_to(radius.get_center() + e_phi.get_unit_vector() * 0.3)

        def update_er(er):
            e_r.put_start_and_end_on(point.get_center(), point.get_center() + radius.get_unit_vector())

        def update_ephi(ephi):
            e_phi.put_start_and_end_on(point.get_center(),
                                       point.get_center() + e_r.copy().rotate(PI / 2).get_unit_vector())

        def update_group(vg, dt):
            theta = (interpolate(0, 2 * PI, dt) + START_ANGLE) % (2 * PI)
            r, a, p, s = vg
            r.become(get_radius(theta))
            a.become(get_angle(theta))
            p.become(get_point(theta))
            s.become(get_angle_shading(theta))

        origin_label = MathTex("O").next_to(ORIGIN, DL)
        # self.wait(1)
        # self.play(ShowCreation(circle))

        self.wait(1)
        self.play(ShowCreation(point))
        self.play(Write(p), Write(origin_label))

        self.wait(1)
        self.play(ShowCreation(radius))
        self.wait()
        circle1 = Circle(radius=1 * self.space_unit_to_x, color=WHITE)
        circle2 = Circle(radius=2 * self.space_unit_to_x, color=WHITE)
        circle3 = Circle(radius=3 * self.space_unit_to_x, color=WHITE)
        self.play(ShowCreation(circle1), ShowCreation(circle2), ShowCreation(circle3))
        self.wait(2)
        self.play(Uncreate(circle1), Uncreate(circle2), Uncreate(circle3))

        self.play(ShowCreation(angle), ShowCreation(angle_shading))
        self.play(Write(phi))

        self.wait(3)
        self.play(Uncreate(p))
        self.play(ShowCreation(e_r))
        self.play(Write(e_r_text.next_to(e_r, UR)))

        self.wait(3)
        self.play(TransformFromCopy(e_r, e_phi))
        self.play(Write(e_phi_text.next_to(e_phi, UL)))

        self.wait(3)
        self.play(ShowCreation(right_angle))

        e_r.add_updater(update_er)
        e_phi.add_updater(update_ephi)

        p.add_updater(update_pText)

        angleNumber.add_updater(update_angleValue)
        # self.play(Transform(phi, angleText))
        # self.play(Write(angleLabel))

        r.add_updater(update_rText)

        p.remove_updater(update_pText)
        r.remove_updater(update_rText)

        self.play(Uncreate(e_r_text), Uncreate(e_phi_text), Uncreate(right_angle))
        r.add_updater(update_rText)
        # self.play(UpdateFromAlphaFunc(circle_group, update_group, run_time=1, rate_func=smooth))
        r.remove_updater(update_rText)

        e_r_text.become(MathTex("e_r").next_to(e_r, UR))
        e_phi_text.become(MathTex("e_\\phi").next_to(e_phi, UL))
        phi_new = MathTex("\\phi", color=GREEN).next_to(angle, RIGHT).shift(UP * 0.2)
        # self.play(Write(e_r_text), Write(e_phi_text), Transform(phi, phi_new), FadeOutAndShift(angleLabel, UP),
        #          FadeOutAndShift(r, UP))
        screen = VGroup(self.x_axis, self.y_axis, radius, point, e_phi, e_r, e_phi_text, e_r_text, angle, angle_shading,
                        phi_new, phi, origin_label)
        self.play(ApplyMethod(screen.to_edge, LEFT))
        self.wait()


class DerivativeDemo(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            graph_origin=ORIGIN,
            x_min=-RANGE,
            x_max=RANGE,
            y_min=-RANGE,
            y_max=RANGE,
            x_axis_width=2 * RANGE,
            y_axis_height=2 * RANGE,
            x_axis_config={"tick_frequency": 2, "leftmost_tick": -2},
            y_axis_config={"tick_frequency": 2, "leftmost_tick": -2}
        )

    def construct(self):
        self.setup_axes()

        def get_radius(theta):
            return Line(ORIGIN, circle.point_at_angle(theta), color=ORANGE)

        def get_angle(theta):
            return Arc(start_angle=0, angle=theta, radius=circle.radius * 0.2, color=GREEN)

        def get_angle_shading(theta):
            return Sector(start_angle=0, angle=theta, outer_radius=circle.radius * 0.2, fill_color=GREEN,
                          fill_opacity=0.5)

        def get_point(theta):
            return Dot(color=BLUE).move_to(circle.point_at_angle(theta))

        circle = Circle(radius=2 * self.space_unit_to_x, color=BLUE)
        radius = get_radius(START_ANGLE)
        angle = get_angle(START_ANGLE)
        angle_shading = get_angle_shading(START_ANGLE)
        point = get_point(START_ANGLE)
        relative_origin = Dot(ORIGIN, fill_opacity=0, stroke_opacity=0)

        circle_group = VGroup(radius, angle, point, angle_shading)

        e_r = Arrow(point.get_center(), point.get_center() + radius.get_unit_vector(), buff=0)
        e_phi = Arrow(point.get_center(), point.get_center() + e_r.copy().rotate(PI / 2).get_unit_vector(), buff=0)

        p = MathTex(r"P", color=BLUE).move_to(point.get_center() + radius.get_unit_vector() * 0.5)
        r = MathTex(r"r", color=ORANGE).move_to(radius.get_center() + e_phi.get_unit_vector() * 0.3)
        phi = MathTex(r"\phi", color=GREEN).next_to(angle, RIGHT).shift(UP * 0.2)
        e_r_text = MathTex("e_r").next_to(e_r, UR)
        e_phi_text = MathTex("e_\\phi").next_to(e_phi, UL)

        angleText, equal, angleNumber, piText = angleLabel = VGroup(
            MathTex(r"\phi", color=GREEN),
            MathTex(r"="),
            DecimalNumber(0, show_ellipsis=False, num_decimal_places=2, include_sign=False),
            MathTex(r"\pi")
        )
        angleLabel.arrange(RIGHT, buff=0.1).to_corner(UL)

        radial_x = Line(ORIGIN,
                        self.coords_to_point(2 * np.cos(START_ANGLE), 0)
                        , color=RED)
        radial_y = Line(self.coords_to_point(2 * np.cos(START_ANGLE), 0),
                        self.coords_to_point(2 * np.cos(START_ANGLE), 2 * np.sin(START_ANGLE))
                        , color=YELLOW)
        radial_xlabel = MathTex("\\cos{", "\phi}").next_to(radial_x, DOWN).set_color_by_tex_to_color_map({
            "\\cos{": RED, "\phi}": GREEN
        })
        radial_ylabel = MathTex("\\sin{", "\phi}").next_to(radial_y, RIGHT).set_color_by_tex_to_color_map({
            "\\sin{": YELLOW, "\phi}": GREEN
        })
        radial_label = VGroup(radial_xlabel, radial_ylabel)

        line0 = MathTex("{d", "\\over", " dt}", "e", "_r")

        line1 = MathTex("=", "{d", "\\over", " dt}", "(", "\\cos{", "\\phi}", ", ", "\\sin{", "\\phi}", ")")

        line2 = MathTex("=", "(", "{d", "\\over", " dt}", "\\cos{\\phi}", ", ", "{d", "\\over", " dt}", "\\sin{\\phi})")

        line3 = MathTex("=", "{d", "\\phi", "\\over", " dt}", "(-\\sin{\\phi}", ", ", "\\cos{\\phi})")

        line4 = MathTex("{d", "\\over", "dt}", "e_r", "={d", "\\phi", "\\over", " dt}", "(-\\sin{\\phi}", ", ",
                        "\\cos{\\phi})")

        line5 = MathTex("{d", "\\over", "dt}", "e_r", "={d", "\\phi", "\\over", " dt}", "e_\\phi")

        self.add(e_r, e_phi, radius, angle, angle_shading, phi, point, e_r_text, e_phi_text)
        e_r_clone = e_r.copy().set_color(ORANGE).put_start_and_end_on(ORIGIN, point.get_center())
        e_phi_clone = Arrow(ORIGIN, self.coords_to_point(-2 * np.sin(START_ANGLE), 2 * np.cos(START_ANGLE)),
                            buff=0)

        e_phi_x = Line(self.coords_to_point(-2 * np.sin(START_ANGLE), 2 * np.cos(START_ANGLE)),
                       self.coords_to_point(0, 2 * np.cos(START_ANGLE)), color=RED)
        e_phi_y = Line(ORIGIN, self.coords_to_point(0, 2 * np.cos(START_ANGLE)), color=YELLOW)

        e_phi_angle = Arc(start_angle=PI / 2, angle=START_ANGLE, radius=circle.radius * 0.2, color=GREEN)
        e_phi_angle_shading = Sector(start_angle=PI / 2, angle=START_ANGLE, outer_radius=circle.radius * 0.2,
                                     color=GREEN, fill_opacity=0.5)
        e_phi_angle_label = MathTex("\\phi", color=GREEN).next_to(e_phi_angle, UP).shift(LEFT * 0.05)

        e_phi_x_label = MathTex("-", "\\sin{\\phi}").next_to(e_phi_x, UP).set_color_by_tex_to_color_map({
            "\\sin{": RED, "\phi}": GREEN
        }).shift(LEFT * 0.3)

        e_phi_y_label = MathTex("\\cos{\\phi}").next_to(e_phi_y, RIGHT).set_color_by_tex_to_color_map({
            "\\cos{": YELLOW, "\phi}": GREEN
        }).shift(UP * 0.2)

        screen = VGroup(self.x_axis, self.y_axis, e_r, e_phi, e_r_clone, radius, angle, angle_shading, phi, point,
                        radial_x, radial_y, radial_ylabel, radial_xlabel, e_r_text, e_phi_text, e_phi_clone, e_phi_x,
                        e_phi_y, e_phi_angle_shading, e_phi_angle, e_phi_angle_label, e_phi_x_label, e_phi_y_label) \
            .to_edge(LEFT)

        to_isolate = ["\\frac{d}{dt}", "r", "e_r", "F=m", "a", "\\frac{d^2x}{dx^2}", "(", ")", "=", "d", "dt"]
        newton2l = VGroup(
            MathTex("F=ma", substrings_to_isolate=to_isolate),
            MathTex("F=m\\frac{d^2x}{dx^2}", substrings_to_isolate=to_isolate)
        ).next_to(screen, RIGHT, buff=4)

        displacement = MathTex("r", "e_r")

        line01 = MathTex("{d", "\\over", "dt}", "(", "r", "e_r", ")").next_to(screen, RIGHT, buff=4)

        line02 = MathTex("=", "{d", "r", "\\over", "dt}", "e_r", "+", "r", "{d", "e_r", "\\over", "dt}") \
            .next_to(line01, DOWN)
        line03 = MathTex("{d", "\\over", "dt}", "(", "r", "e_r", ")", "=", "{d", "r", "\\over", "dt}", "e_r", "+", "r",
                         "{d", "e_r", "\\over", "dt}")

        displacement.next_to(line01, UP)

        self.play(Write(newton2l[0]))
        self.wait()
        self.play(FadeOutAndShift(newton2l[0]))
        line03.to_corner(UL, buff=SMALL_BUFF).scale(0.5).shift(LEFT)

        self.wait()
        self.play(Write(displacement))
        self.play(TransformMatchingTex(displacement, line01, run_time=2))
        self.wait()
        self.play(TransformMatchingTex(line01.copy(), line02, run_time=2))
        self.wait()
        self.play(Transform(line01, line03[:6]), Transform(line02, line03[6:]))
        self.remove(line01, line02)
        self.add(line03)
        self.wait()

        self.play(TransformFromCopy(e_r, e_r_clone))
        self.remove(radius)
        self.wait()
        self.play(TransformFromCopy(radius, radial_y), TransformFromCopy(radius, radial_x))
        self.wait()
        self.play(Write(radial_label))
        self.wait()

        line0.next_to(screen, RIGHT, buff=4).to_edge(UP)
        line1.next_to(line0, DOWN)
        line2.next_to(line1, DOWN)
        line3.next_to(line2, DOWN)
        line4.to_corner(DL, buff=SMALL_BUFF).scale(0.8)
        line5.to_corner(DL, buff=SMALL_BUFF).scale(0.8)

        self.wait()
        self.play(Write(line0))
        self.wait()
        self.play(TransformFromCopy(line0[:3], line1[1:4]), TransformFromCopy(line0[3], line1[4]),
                  TransformFromCopy(line0[4], line1[10]), Write(line1[7]), Write(line1[0]))
        self.play(TransformFromCopy(radial_xlabel[0], line1[5], run_time=2, path_along_arc=PI / 2),
                  TransformFromCopy(radial_xlabel[1], line1[6], run_time=2, path_along_arc=PI / 2),
                  TransformFromCopy(radial_ylabel[0], line1[8], run_time=2, path_along_arc=PI / 2),
                  TransformFromCopy(radial_ylabel[1], line1[9], run_time=2, path_along_arc=PI / 2))

        self.wait()
        self.play(TransformMatchingTex(line1.copy(), line2, run_time=2, path_along_arc=PI / 2))
        self.wait()
        self.play(TransformMatchingTex(line2.copy(), line3, run_time=2, path_along_arc=PI / 2))
        self.wait()
        self.play(FadeOutAndShift(line1, UP), FadeOutAndShift(line2, UP), Transform(line0, line4[:4]),
                  Transform(line3, line4[4:]))
        self.remove(line0, line3)
        self.add(line4)
        self.wait()

        self.play(Uncreate(radial_x), Uncreate(radial_y), Uncreate(radial_xlabel), Uncreate(radial_ylabel),
                  Uncreate(e_r), Uncreate(e_r_text))
        self.wait()
        self.play(Transform(e_phi, e_phi_clone), Uncreate(point), ApplyMethod(e_phi_text.next_to, e_phi_clone, LEFT))
        self.play(ShowCreation(e_phi_angle_shading), ShowCreation(e_phi_angle), run_time=0.8)
        self.play(Write(e_phi_angle_label), run_time=0.5)
        self.wait()
        self.play(TransformFromCopy(e_phi_clone, e_phi_x), TransformFromCopy(e_phi_clone, e_phi_y))
        self.wait()
        self.play(Write(e_phi_x_label), Write(e_phi_y_label))
        self.wait()

        line10 = MathTex("{d", "\\over", "dt}", "e_{", "\\phi}")
        line11 = MathTex("=", "{d", "\\over", "dt}", "(", "-", "\\sin{\\phi}", ", ", "\\cos{\\phi}", ")")
        line12 = MathTex("=", "(", "-", "{d", "\\over", "dt}", "\\sin{\\phi}", ",", "{d", "\\over", "dt}",
                         "\\cos{\\phi}", ")")
        line13 = MathTex("=", "{d", "\\phi", "\\over", "dt}", "(", "-", "\\cos{\\phi}", ",", "-\\sin{\\phi}", ")")
        line14 = MathTex("=", "-", "{d", "\\phi", "\\over", "dt}", "(", "\\cos{\\phi}", ",", "\\sin{\\phi})")
        line15 = MathTex("=", "-", "{d", "\\phi", "\\over", "dt}", "e_{", "r}")
        line16 = MathTex("{d \\over dt}", "e_{", "\\phi}", "=", "-", "{d", "\\phi", "\\over", "dt}", "e_{", "r}")

        line10.next_to(screen, RIGHT, buff=4).to_edge(UP)
        line11.next_to(line10, DOWN)
        line12.next_to(line11, DOWN)
        line13.next_to(line12, DOWN)
        line14.next_to(line13, DOWN)
        line15.next_to(line14, DOWN)
        line16.to_corner(DR, buff=SMALL_BUFF).scale(0.8)

        self.play(Write(line10))
        self.wait()
        self.play(TransformFromCopy(line10[0], line11[1], run_time=2, path_along_arc=PI / 2),
                  TransformFromCopy(line10[1], line11[2], run_time=2, path_along_arc=PI / 2),
                  TransformFromCopy(line10[2], line11[3], run_time=2, path_along_arc=PI / 2),
                  TransformFromCopy(line10[3], line11[4], run_time=2, path_along_arc=PI / 2),
                  TransformFromCopy(line10[4], line11[9], run_time=2, path_along_arc=PI / 2))
        self.play(TransformFromCopy(e_phi_x_label[0], line11[5], run_time=2, path_along_arc=PI / 2),
                  TransformFromCopy(e_phi_x_label[1], line11[6], run_time=2, path_along_arc=PI / 2),
                  TransformFromCopy(e_phi_y_label, line11[8], run_time=2, path_along_arc=PI / 2),
                  Write(line11[0], run_time=2), Write(line11[7], run_time=2))
        self.wait()
        self.play(TransformMatchingTex(line11.copy(), line12), run_time=2, path_along_arc=PI / 2)
        self.wait()
        self.play(TransformMatchingTex(line12.copy(), line13), run_time=2, path_along_arc=PI / 2)
        self.wait()
        self.play(TransformMatchingTex(line13.copy(), line14), run_time=2, path_along_arc=PI / 2)
        self.wait()
        self.play(TransformMatchingTex(line14.copy(), line15), run_time=2, path_along_arc=PI / 2)
        self.wait()
        self.play(FadeOutAndShift(line11), FadeOutAndShift(line12), FadeOutAndShift(line13), FadeOutAndShift(line14))
        self.wait()
        self.play(Transform(line10, line16[:3]), Transform(line15, line16[3:]))
        self.remove(line10, line15)
        self.add(line16)
        self.wait()
        self.play(TransformMatchingTex(line4, line5))

        self.wait()
        self.play(FadeOutAndShift(screen, UP))
        self.wait()

        general_velocity_formula = MathTex("{d", "\\over", "dt}", "(", "r", "e_r", ")", "=", "{d", "r", "\\over", "dt}",
                                           "e_r", "+", "r", "{d", "\\phi", "\\over", " dt}", "e_\\phi")

        velocity_original = line03.copy().scale(2).move_to(ORIGIN)
        d_r = MathTex("{d", "e_r", "\\over", "dt}", "=", "{d", "\\phi", "\\over", "dt}", "e_\\phi").to_corner(UL).scale(
            0.5)
        d_phi = MathTex("{d", "e_\\phi", "\\over", "dt}", "e_{", "\\phi}", "=", "-", "{d", "\\phi", "\\over", "dt}",
                        "e_{", "r}").next_to(d_r, DOWN).scale(0.5)

        self.play(Transform(line03, velocity_original), TransformMatchingTex(line5, d_r),
                  TransformMatchingTex(line16, d_phi))
        self.remove(line03, line5, line16)
        self.add(velocity_original)
        self.wait()
        self.play(ApplyMethod(velocity_original.next_to, general_velocity_formula, UP))
        self.wait()
        self.play(TransformFromCopy(d_r[5:], general_velocity_formula[15:], run_time=1, path_along_arc=PI / 2))
        self.play(
            TransformFromCopy(velocity_original[:15], general_velocity_formula[:15], run_time=2, path_along_arc=PI / 2))
        self.wait()
        self.play(FadeOutAndShift(velocity_original, UP))
        self.wait()


class PolarAcceleration1(Scene):
    def construct(self):
        d_r = MathTex("{d", "e_r", "\\over", "dt}", "=", "{d", "\\phi", "\\over", "dt}", "e_\\phi").to_corner(UL).scale(
            0.7)
        d_phi = MathTex("{d", "e_\\phi", "\\over", "dt}", "=", "-", "{d", "\\phi", "\\over", "dt}", "e_{",
                        "r}").next_to(d_r, DOWN).scale(0.7)

        dt = MathTex("{d", "\\over", "dt}")

        line30 = MathTex("\\frac{d}{dt}", "(", "r", "e_r", ")", "=", "{d", "r", "\\over", "dt}",
                         "e_r", "+", "r", "{d", "\\phi", "\\over", " dt}", "e_\\phi")
        line31 = MathTex("\\frac{d^2}{dt^2}", "(", "r", "e_r", ")", "=", "{d", "\\over", "dt}", "(", "{d", "r",
                         "\\over", "dt}", "e_r", ")", "+", "{d", "\\over", "dt}", "(", "r", "{d", "\\phi", "\\over",
                         " dt}", "e_\\phi", ")")
        line31a = MathTex("\\frac{d^2}{dt^2}", "(", "r", "e_r", ")")
        line31b = MathTex("=", "{d", "\\over", "dt}", "(", "{d", "r",
                          "\\over", "dt}", "e_r", ")", "+", "{d", "\\over", "dt}", "(", "r", "{d", "\\phi", "\\over",
                          " dt}", "e_\\phi", ")")
        line32 = MathTex("=", "{d^2", "r", "\\over", "dt^2}", "e_r", "+", "{d", "r", "\\over", "dt}", "{d", "e_r",
                         "\\over", "dt}", "+", "{d", "r", "\\over", "dt}", "{d", "\\phi", "\\over", "dt}", "e_\\phi",
                         "+", "r", "{d", "\\over", "dt}", "(", "{d", "\\phi", "\\over", "dt}", "e_\\phi",
                         ")")
        line33 = MathTex("=", "{d^2", "r", "\\over", "dt^2}", "e_r", "+", "{d", "r", "\\over", "dt}", "{d", "e_r",
                         "\\over", "dt}", "+", "{d", "r", "\\over", "dt}", "{d", "\\phi", "\\over", "dt}", "e_\\phi",
                         "+", "r", "{d^2", "\\phi", "\\over", "dt^2}", "e_\\phi", "+", "r", "{d", "\\phi", "\\over",
                         "dt}", "{d", "e_\\phi", "\\over", "dt}")
        line34 = MathTex("=", "{d^2", "r", "\\over", "dt^2}", "e_r", "+", "{d", "r", "\\over", "dt}",
                         "{d", "\\phi", "\\over", "dt}", "e_\\phi", "+", "{d", "r", "\\over", "dt}", "{d", "\\phi",
                         "\\over", "dt}", "e_\\phi",
                         "+", "r", "{d^2", "\\phi", "\\over", "dt^2}", "e_\\phi", "-", "r", "{d", "\\phi", "\\over",
                         "dt}", "{d", "\\phi", "\\over", "dt}", "e_{", "r}")
        line35 = MathTex("\\frac{d^2}{dt^2}", "(", "r", "e_r", ")", "=", "{d^2", "r", "\\over", "dt^2}", "e_r", "+",
                         "{d", "r", "\\over", "dt}",
                         "{d", "\\phi", "\\over", "dt}", "e_\\phi", "+", "{d", "r", "\\over", "dt}", "{d", "\\phi",
                         "\\over", "dt}", "e_\\phi",
                         "+", "r", "{d^2", "\\phi", "\\over", "dt^2}", "e_\\phi", "-", "r", "{d", "\\phi", "\\over",
                         "dt}", "{d", "\\phi", "\\over", "dt}", "e_{", "r}")
        line36 = MathTex("\\frac{d^2}{dt^2}", "(", "r", "e_r", ")", "=", "{d^2", "r", "\\over", "dt^2}", "e_r", "+",
                         "2", "{d", "r", "\\over", "dt}",
                         "{d", "\\phi", "\\over", "dt}", "e_\\phi",
                         "+", "r", "{d^2", "\\phi", "\\over", "dt^2}", "e_\\phi", "-", "r", "\\left(", "{d", "\\phi",
                         "\\over", "dt}", "\\right)", "^2", "e_{", "r}")
        line37 = MathTex("\\ddot", "r", "=", "\\ddot", "r", "e_r", "+", "2", "\\dot", "r", "\\dot", "\\phi", "e_\\phi",
                         "+", "r", "\\ddot", "\\phi", "e_\\phi", "-", "r", "\\dot", "\\phi", "^2", "e_{", "r}")
        line37a = MathTex("\\ddot r = ", "\\ddot r e_r", "+", "2\\dot r \\dot \\phi e_\\phi", "+", "r \\ddot \\phi e_\\phi", "-", "r \\dot \\phi^2 e_{r}")
        line38  = MathTex("\\ddot r = ", "\\ddot r e_r", "-", "r \\dot \\phi^2 e_{r}", "+", "2\\dot r \\dot \\phi e_\\phi", "+", "r \\ddot \\phi e_\\phi")
        framebox1 = SurroundingRectangle(line38[1], buff=.1)
        framebox2 = SurroundingRectangle(line38[3], buff=.1)
        framebox3 = SurroundingRectangle(line38[5], buff=.1)
        framebox4 = SurroundingRectangle(line38[7], buff=.1)

        self.add(d_r, d_phi, line30)
        self.wait()
        self.play(ApplyMethod(line30.to_edge, UP))

        dt.next_to(line30, LEFT, buff=SMALL_BUFF)
        line31.next_to(line30, DOWN)
        line31a.move_to(line31)
        line31b.next_to(line31, DOWN)
        line32.next_to(line31b, DOWN)
        line33.next_to(line32, DOWN)

        self.wait()
        self.play(Write(dt))
        self.wait()
        self.play(TransformMatchingTex(line30.copy(), line31, run_time=2, path_along_arc=PI / 2,
                                       key_map={
                                           "\\frac{d}{dt}": "\\frac{d^2}{dt^2}"
                                       }))
        self.wait()
        self.play(Transform(line31[5:], line31b, run_time=2, path_along_arc=PI / 2),
                  Transform(line31[:5], line31a, run_time=2, path_along_arc=PI / 2),
                  FadeOutAndShift(line30, UP), FadeOutAndShift(dt, UP))
        self.wait()
        self.play(TransformMatchingTex(line31b.copy(), line32, run_time=2, path_along_arc=PI / 2))
        self.wait()
        self.play(TransformMatchingTex(line32.copy(), line33, run_time=2, path_along_arc=PI / 2))

        self.wait()
        self.clear()
        self.add(d_r, d_phi, line31a, line31b, line32, line33)
        self.play(FadeOutAndShift(line31b, UP), FadeOutAndShift(line32, UP))

        self.play(ApplyMethod(line33.next_to, line31a, DOWN))
        self.wait()
        line34.next_to(line33, DOWN)
        self.play(TransformFromCopy(d_r[5:], line34[11:16], run_time=2, path_along_arc=PI / 2),
                  TransformFromCopy(d_phi[6:], line34[39:], run_time=2, path_along_arc=PI / 2),
                  TransformFromCopy(d_phi[5], line34[33], run_time=2, path_along_arc=PI / 2))
        self.play(TransformFromCopy(line33[:11], line34[:11], run_time=2, path_along_arc=PI / 2),
                  TransformFromCopy(line33[15:32], line34[16:33], run_time=2, path_along_arc=PI / 2),
                  TransformFromCopy(line33[33:38], line34[34:39], run_time=2, path_along_arc=PI / 2))
        self.wait()
        self.play(FadeOutAndShift(d_r, UP), FadeOutAndShift(d_phi, UP), FadeOutAndShift(line33, UP))
        self.wait()
        self.play(Transform(line31a, line35[:5], run_time=2, path_along_arc=PI / 2),
                  Transform(line34, line35[5:], run_time=2, path_along_arc=PI / 2))
        self.wait()
        self.clear()
        self.add(line35)
        self.play(TransformMatchingTex(line35, line36, run_time=2, path_along_arc=PI / 2))
        self.wait()
        self.play(TransformMatchingTex(line36, line37, run_time=2, path_along_arc=PI / 2, key_map={
            "{d^2": "\\ddot",
            "{d": "\\dot"
        }))
        self.wait()
        self.clear()
        self.add(line37a)
        self.play(TransformMatchingTex(line37a, line38, path_along_arc=PI / 2))
        self.wait()
        self.play(ShowCreation(framebox1))
        self.wait()
        self.play(ReplacementTransform(framebox1, framebox4))
        self.wait()
        self.play(ReplacementTransform(framebox4, framebox2))
        self.wait()
        self.play(ReplacementTransform(framebox2, framebox3))
        self.wait()
