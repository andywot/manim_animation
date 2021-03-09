from manim import *

RANGE = 3.5


class LowPressure(GraphScene):
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
            x_axis_config={"tick_frequency": 3.5},
            y_axis_config={"tick_frequency": 3.5}
        )

    def construct(self):
        self.setup_axes()
        circle = VGroup(
            Circle(radius=1 * self.space_unit_to_x, color=BLUE).set_opacity(0.2),
            Circle(radius=2 * self.space_unit_to_x, color=BLUE).set_opacity(0.2),
            Circle(radius=3 * self.space_unit_to_x, color=BLUE).set_opacity(0.2)
        )
        arrows = VGroup(
            Arrow(self.coords_to_point(0, np.sqrt(2)), ORIGIN),
            Arrow(self.coords_to_point(0, -np.sqrt(2)), ORIGIN),
            Arrow(self.coords_to_point(np.sqrt(2), 0), ORIGIN),
            Arrow(self.coords_to_point(-np.sqrt(2), 0), ORIGIN),
            Arrow(self.coords_to_point(1, 1), ORIGIN),
            Arrow(self.coords_to_point(-1, -1), ORIGIN),
            Arrow(self.coords_to_point(-1, 1), ORIGIN),
            Arrow(self.coords_to_point(1, -1), ORIGIN)
        )
        pulling_force = MathTex("F_{P}=", "{dP \\over dr}").next_to(arrows[0], UR)
        deflected_arrows = VGroup(
            Arrow(self.coords_to_point(0, np.sqrt(2)), self.coords_to_point(-1, 1)),
            Arrow(self.coords_to_point(0, -np.sqrt(2)), self.coords_to_point(1, -1)),
            Arrow(self.coords_to_point(np.sqrt(2), 0), self.coords_to_point(1, 1)),
            Arrow(self.coords_to_point(-np.sqrt(2), 0), self.coords_to_point(-1, -1)),
            Arrow(self.coords_to_point(1, 1), self.coords_to_point(0, np.sqrt(2))),
            Arrow(self.coords_to_point(-1, -1), self.coords_to_point(0, -np.sqrt(2))),
            Arrow(self.coords_to_point(-1, 1), self.coords_to_point(-np.sqrt(2), 0)),
            Arrow(self.coords_to_point(1, -1), self.coords_to_point(np.sqrt(2), 0))
        )
        coriolis_force_arrow = Arrow(self.coords_to_point(np.sqrt(2), 0), RIGHT * 4, color=RED)
        coriolis_force = MathTex("F_{coriolis}", "= 2\\rho v\\Omega", " \\sin{\\lambda}",
                                 tex_to_color_map={"F_{coriolis}": RED}).next_to(coriolis_force_arrow, UP * 2).scale(
            0.8)
        framebox1 = SurroundingRectangle(coriolis_force[2], buff=.1)
        centripetal_force = MathTex("F = ", "\\rho {v^2 \\over r}")
        equality = MathTex("\\rho {v^2 \\over r}", "= 2\\rho v\\Omega", " \\sin{\\lambda}", "+",
                           "{dP \\over dr}")
        equality_rearranged1 = MathTex("\\rho", "{", "v^2", "\\over", "r}", "=", " 2\\rho v\\Omega", " \\sin{\\lambda}",
                                       "+",
                                       "{dP \\over dr}")
        equality_rearranged2 = MathTex("{", "\\rho", "\\over", "r}", "v^2", "-", "2\\rho v\\Omega", " \\sin{\\lambda}",
                                       "-", "{dP \\over dr}", "=", "0")

        self.play(ShowCreation(circle, run_time=2))
        self.wait(2)
        self.play(ShowCreation(arrows, run_time=1.5))
        self.wait(2)
        self.play(Write(pulling_force, run_time=2))
        self.wait(2)
        self.play(ApplyMethod(pulling_force.to_corner, UL))
        self.wait(4)
        i = 0
        for arrow in arrows:
            self.play(Transform(arrow, deflected_arrows[i], run_time=0.2))
            i = i + 1
        self.remove(arrows, deflected_arrows)
        self.add(deflected_arrows)
        self.play(Rotate(deflected_arrows, run_time=3, rate_func=smooth))
        self.wait(2)
        i = 0
        for arrow in deflected_arrows:
            self.play(Uncreate(arrow, run_time=0.2))
        arrows[0].become(Arrow(self.coords_to_point(np.sqrt(2), 0), ORIGIN))
        self.play(ShowCreation(arrows[0]))

        self.play(ShowCreation(coriolis_force_arrow))
        self.wait(2)
        self.play(Write(coriolis_force, run_time=10, rate_func=rush_from))
        self.wait(2)
        self.play(ShowCreation(framebox1))
        self.wait(4)
        self.play(Uncreate(framebox1))
        self.play(ApplyMethod(coriolis_force.to_edge, LEFT))
        self.wait()
        self.play(FocusOn(arrows[0], run_time=0.5))
        self.wait()
        self.play(FocusOn(coriolis_force_arrow, run_time=0.5))
        self.wait()
        screen = VGroup(self.x_axis, self.y_axis, circle, arrows[0], coriolis_force_arrow)
        self.play(FadeOutAndShift(screen, UP))
        self.wait()
        self.play(Write(centripetal_force))
        self.wait(2)
        self.play(Uncreate(centripetal_force[0]), Transform(centripetal_force[1], equality[0]),
                  Transform(coriolis_force[1], equality[1]),
                  Transform(coriolis_force[2], equality[2]), Transform(pulling_force[1], equality[4]),
                  Write(equality[3]), Uncreate(coriolis_force[0]), Uncreate(pulling_force[0]))
        self.wait()
        self.clear()
        self.add(equality_rearranged1)
        self.wait()
        self.play(TransformMatchingTex(equality_rearranged1, equality_rearranged2, run_time=2, path_along_arc=PI / 2))
        self.clear()
        self.add(equality_rearranged2)
        self.wait(3)

        distance = MathTex("r = 300\\, 000m")
        dP = MathTex("{dP \\over dr} = {400 Pa \\over 200\\, 000 m}")
        omega = MathTex("\\Omega = {2\\pi \\over 24 \\cross 60 \\cross 60} rad \\, s^{-1}")
        rho = MathTex("\\rho = 1.2 kg \\, m^{-3}")
        answer = MathTex("v = 10.8 m\\, s^{-1} \\approx 24mph")
        answer_real = MathTex("v_{real} = 12mph")

        self.play(ApplyMethod(equality_rearranged2.to_edge, UP))
        self.wait()
        distance.next_to(equality_rearranged2, DOWN)
        dP.next_to(distance, DOWN)
        omega.next_to(dP, DOWN)
        rho.next_to(omega, DOWN)

        self.play(Write(distance))
        self.wait()
        self.play(Write(dP))
        self.wait()
        self.play(Write(omega), Write(rho))
        self.wait()
        answer.move_to(equality_rearranged2)

        self.play(FadeOutAndShift(distance, UP), FadeOutAndShift(dP, UP), FadeOutAndShift(omega, UP),
                  FadeOutAndShift(rho, UP), FadeOutAndShift(equality_rearranged2, UP))
        self.play(Write(answer))
        self.wait()
        self.play(Write(answer_real))
        self.play(ApplyMethod(answer.next_to, answer_real, UP))
        self.wait(10)

        self.camera.background_color = "#ece6e2"
        logo_green = "#87c2a5"
        logo_blue = "#525893"
        logo_red = "#e07a5f"
        logo_black = "#343434"
        ds_m = MathTex(r"\mathbb{M}", fill_color=logo_black).scale(7)
        ds_m.shift(2.25 * LEFT + 1.5 * UP)
        circle = Circle(color=logo_green, fill_opacity=1).shift(LEFT)
        square = Square(color=logo_blue, fill_opacity=1).shift(UP)
        triangle = Triangle(color=logo_red, fill_opacity=1).shift(RIGHT)
        logo = VGroup(triangle, square, circle, ds_m)  # order matters
        logo.move_to(ORIGIN)

        self.clear()
        animation_credit = Text("Animation created using:", color=BLACK).to_edge(UP)
        self.play(Write(animation_credit))
        self.play(ShowCreation(logo))
        self.wait(2)
