from manim import *

class TextScene(Scene):
    def construct(self):
        coriolis_force_def = Text(
            """The Coriolis force is what is known as a "fictitious force" \n
            that acts on a mass which is in motion \n
            within a frame of reference that is rotating."""
        ).scale(0.7)

        self.play(Write(coriolis_force_def, run_time=10))
        self.wait()
        self.play(FadeOutAndShift(coriolis_force_def, UP))
        self.wait()
        