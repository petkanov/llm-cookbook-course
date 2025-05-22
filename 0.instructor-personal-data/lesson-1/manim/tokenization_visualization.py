from manim import *

class TokenizationVisualization(Scene):
    def construct(self):
        # 1. Show sentence
        sentence = "The quick brown fox jumps"
        sentence_mob = Text(sentence, font_size=36)
        self.play(Write(sentence_mob))
        self.wait(0.5)

        # 2. Split into tokens
        tokens = ["The", "quick", "brown", "fox", "jumps"]
        token_mobs = VGroup(*[Rectangle(width=1.4, height=0.7, color=BLUE).set_fill(BLUE, 0.1).move_to(LEFT*3 + RIGHT*i*1.6) for i in range(len(tokens))])
        token_texts = VGroup(*[Text(tok, font_size=28).move_to(token_mobs[i]) for i, tok in enumerate(tokens)])

        # Animate splitting
        self.play(
            sentence_mob.animate.shift(UP*1.5),
            LaggedStart(*[FadeIn(token_mobs[i], shift=DOWN) for i in range(len(tokens))], lag_ratio=0.15),
            LaggedStart(*[Write(token_texts[i]) for i in range(len(tokens))], lag_ratio=0.15),
            run_time=1.2
        )
        self.wait(0.3)

        # 3. Show numerical representations
        numbers = ["101", "205", "309", "412", "523"]
        number_mobs = VGroup(*[Text(num, font_size=24, color=YELLOW).next_to(token_mobs[i], DOWN, buff=0.2) for i, num in enumerate(numbers)])
        self.play(LaggedStart(*[FadeIn(number_mobs[i], shift=DOWN) for i in range(len(numbers))], lag_ratio=0.15), run_time=0.8)
        self.wait(0.2)

        # 4. Move tokens to 3D space (simulate high-dimensional vectors)
        vector_origins = [np.array([-4 + i*2, -1.5, 0]) for i in range(len(tokens))]
        vector_targets = [np.array([-2 + i*1.2, -2.5 + (i%2)*1.2, 0]) for i in range(len(tokens))]
        vectors = VGroup(*[
            Arrow(start=vector_origins[i], end=vector_targets[i], buff=0.1, color=GREEN, max_tip_length_to_length_ratio=0.2)
            for i in range(len(tokens))
        ])
        token_dots = VGroup(*[Dot(vector_targets[i], color=BLUE) for i in range(len(tokens))])

        # Animate tokens and numbers moving to vector space
        self.play(
            *[Transform(token_mobs[i], token_mobs[i].copy().move_to(vector_targets[i])) for i in range(len(tokens))],
            *[Transform(token_texts[i], token_texts[i].copy().move_to(vector_targets[i] + UP*0.4)) for i in range(len(tokens))],
            *[Transform(number_mobs[i], number_mobs[i].copy().move_to(vector_targets[i] + DOWN*0.4)) for i in range(len(tokens))],
            run_time=1.2
        )
        self.play(LaggedStart(*[GrowArrow(vectors[i]) for i in range(len(tokens))], lag_ratio=0.1), FadeIn(token_dots), run_time=0.8)

        # 5. Show arrows to next most probable token (simulate prediction)
        prediction_arrows = VGroup(*[
            Arrow(start=vector_targets[i], end=vector_targets[i+1], buff=0.1, color=RED, max_tip_length_to_length_ratio=0.2)
            for i in range(len(tokens)-1)
        ])
        self.play(LaggedStart(*[GrowArrow(prediction_arrows[i]) for i in range(len(tokens)-1)], lag_ratio=0.12), run_time=0.8)

        self.wait(0.5)
        all_objs = VGroup(
            *token_mobs, *token_texts, *number_mobs, *vectors, *token_dots, *prediction_arrows, sentence_mob
        )
        self.play(FadeOut(all_objs), run_time=0.5)