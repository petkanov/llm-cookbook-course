from manim import *

class ProbabilityDistributionMorph(Scene):
    def construct(self):
        # Axes for probability distribution
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1, 0.2],
            x_length=8,
            y_length=3,
            axis_config={"color": WHITE},
        ).to_edge(UP)

        x_labels = [MathTex(f"{i}") for i in range(1, 10)]
        for i, label in enumerate(x_labels, start=1):
            label.scale(0.5)
            label.next_to(axes.c2p(i, 0), DOWN, buff=0.1)
            self.add(label)

        # Initial probability distribution (e.g., softmax output)
        def prob_curve1(x):
            return 0.25 * np.exp(-0.5 * (x - 3) ** 2) + 0.1

        def prob_curve2(x):
            return 0.3 * np.exp(-0.5 * (x - 6) ** 2) + 0.1

        def prob_curve3(x):
            return 0.4 * np.exp(-0.5 * (x - 8) ** 2) + 0.1

        graph1 = axes.plot(prob_curve1, color=BLUE)
        graph2 = axes.plot(prob_curve2, color=GREEN)
        graph3 = axes.plot(prob_curve3, color=YELLOW)

        # Token boxes
        tokens = ["The", "cat", "sat"]
        token_mobs = VGroup()
        for i, token in enumerate(tokens):
            box = Rectangle(width=1.2, height=0.6, color=WHITE, fill_opacity=0.7)
            text = Text(token, font_size=28).move_to(box.get_center())
            group = VGroup(box, text).to_edge(DOWN).shift(LEFT*2 + RIGHT*i*2)
            token_mobs.add(group)

        # Show axes and initial curve
        self.play(Create(axes), Create(graph1))
        self.wait(0.5)

        # Animate first token appearing
        self.play(FadeIn(token_mobs[0]), run_time=0.5)
        self.wait(0.5)

        # Morph to next probability distribution, show next token
        self.play(Transform(graph1, graph2), FadeIn(token_mobs[1]), run_time=2)
        self.wait(0.5)

        # Morph to next probability distribution, show next token
        self.play(Transform(graph1, graph3), FadeIn(token_mobs[2]), run_time=2)
        self.wait(0.5)

        # Hold final frame
        self.wait(1)
