from manim import *
import numpy as np

class MarkovChainAnimation(Scene):
    def construct(self):
        # Set up the Markov chain nodes
        states = ["w₁", "w₂", "w₃"]
        vertices = [Dot(radius=0.3, color=BLUE).set_fill(opacity=0.8) for _ in states]
        labels = [Text(state, font_size=24).next_to(vertices[i], UP, buff=0.1) 
                 for i, state in enumerate(states)]
        
        # Position the vertices horizontally
        for i, vertex in enumerate(vertices):
            vertex.move_to(3 * (i - 1) * RIGHT)
            
        # Create the vertex group
        vertex_group = VGroup(*vertices, *labels)
        
        # Create transition edges with probabilities
        # P(w₂|w₁) = 0.7, P(w₃|w₁) = 0.3
        # P(w₁|w₂) = 0.4, P(w₃|w₂) = 0.6
        # P(w₁|w₃) = 0.2, P(w₂|w₃) = 0.8
        prob_values = {
            (0, 1): "0.7", (0, 2): "0.3",
            (1, 0): "0.4", (1, 2): "0.6",
            (2, 0): "0.2", (2, 1): "0.8"
        }
        
        edges = []
        probs = []
        arrows = []
        
        for start, end in prob_values.keys():
            # Create curved arrows
            if abs(start - end) == 1:
                arrow = CurvedArrow(
                    vertices[start].get_center(), 
                    vertices[end].get_center(),
                    angle=PI/4,
                    color=RED
                )
            else:
                arrow = CurvedArrow(
                    vertices[start].get_center(), 
                    vertices[end].get_center(), 
                    angle=PI/3,
                    color=RED
                )
            arrows.append(arrow)
            
            # Create probability labels
            prob = Text(prob_values[(start, end)], font_size=20, color=GREEN)
            prob.move_to(arrow.point_from_proportion(0.5) + 0.4 * UP)
            probs.append(prob)
            
        # Probability flow shapes
        flow_dots = [Dot(color=YELLOW, radius=0.08) for _ in range(6)]
        
        # Conditional probability formulas
        formula1 = MathTex(r"P(w_2|w_1) = \frac{P(w_1, w_2)}{P(w_1)}", color=WHITE)
        formula1.to_corner(UL).shift(DOWN)
        
        formula2 = MathTex(r"P(w_3|w_2) = \frac{P(w_2, w_3)}{P(w_2)}", color=WHITE)
        formula2.to_corner(UL).shift(DOWN)
        
        # Animation sequence
        self.play(
            Create(vertex_group),
            run_time=1
        )
        
        self.play(
            *[Create(arrow) for arrow in arrows],
            run_time=1
        )
        
        self.play(
            *[Write(prob) for prob in probs],
            Write(formula1),
            run_time=1
        )
        
        # Animate probability flow for w₁ → w₂
        flow_path_1 = [
            vertices[0].get_center(),
            arrows[0].point_from_proportion(0.5),
            vertices[1].get_center()
        ]
        
        self.play(
            MoveAlongPath(flow_dots[0], 
                          VMobject().set_points_as_corners(flow_path_1)),
            run_time=1
        )
        
        # Animate probability flow for w₂ → w₃
        flow_path_2 = [
            vertices[1].get_center(),
            arrows[3].point_from_proportion(0.5),
            vertices[2].get_center()
        ]
        
        self.play(
            Transform(formula1, formula2),
            MoveAlongPath(flow_dots[1], 
                          VMobject().set_points_as_corners(flow_path_2)),
            run_time=1
        )
        
        # Animate probability flow for w₃ → w₁ and w₃ → w₂ simultaneously
        flow_path_3 = [
            vertices[2].get_center(),
            arrows[4].point_from_proportion(0.5),
            vertices[0].get_center()
        ]
        
        flow_path_4 = [
            vertices[2].get_center(),
            arrows[5].point_from_proportion(0.5),
            vertices[1].get_center()
        ]
        
        self.play(
            MoveAlongPath(flow_dots[2], 
                          VMobject().set_points_as_corners(flow_path_3)),
            MoveAlongPath(flow_dots[3], 
                          VMobject().set_points_as_corners(flow_path_4)),
            FadeOut(formula2),
            run_time=1.5
        )
        
        # Final fade out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1
        )


if __name__ == "__main__":
    # Uncomment the line below and run this file to render animation
    # (Make sure you have Manim installed)
    # os.system("manim -pql markov_chain_animation.py MarkovChainAnimation")
    pass 