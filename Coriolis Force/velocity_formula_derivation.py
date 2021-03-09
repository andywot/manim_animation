from manim import *


class Formula(Scene):
    def construct(self):
        to_isolate = ["\\frac{d}{dt}", "r", "e_r", "F=m", "a", "\\frac{d^2x}{dx^2}", "(", ")", "=", "d", "dt"]
        newton2l = VGroup(
            MathTex("F=ma", substrings_to_isolate=to_isolate),
            MathTex("F=m\\frac{d^2x}{dx^2}", substrings_to_isolate=to_isolate)
        ).next_to(screen, RIGHT, buff=4)

        displacement = MathTex("r", "e_r")

        line01 = MathTex("{d", "\\over", "dt}", "(", "r", "e_r", ")").next_to(screen, RIGHT, buff=4)

        line02 = MathTex("=", "{d", "r", "\\over", "dt}", "e_r", "+", "r", "{d", "e_r", "\\over", "dt}") \
            .next_to(line01, DOWN)

        displacement.next_to(line01, UP)

        self.play(Write(newton2l[0]))
        self.wait()
        self.play(TransformMatchingTex(newton2l[0], newton2l[1]))
        self.wait()
        self.play(ApplyMethod(newton2l[1].to_corner, UL))

        self.wait()
        self.play(Write(displacement))
        self.play(TransformMatchingTex(displacement, line01, run_time=2))
        self.wait()
        self.play(TransformMatchingTex(line01.copy(), line02, run_time=2))
        self.wait()
