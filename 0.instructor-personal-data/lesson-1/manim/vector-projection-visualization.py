from manim import *
import numpy as np

class VectorProjectionVisualization(ThreeDScene):
    def construct(self):
        # Set up the scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.camera.frame_center = ORIGIN
        
        # Create the axes
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        
        # Create the 3D vector
        vector = Arrow3D(
            start=ORIGIN,
            end=np.array([2, 3, 4]),
            color=YELLOW,
            thickness=0.05
        )
        
        # Create the 2D plane
        plane = Surface(
            lambda u, v: axes.c2p(u, v, 0),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(20, 20),
            fill_opacity=0.3,
            fill_color=BLUE,
            stroke_width=0.5,
            stroke_color=WHITE
        )
        
        # Calculate the projection vector
        original_end = np.array([2, 3, 4])
        projected_end = np.array([2, 3, 0])  # Projection onto the xy-plane
        
        # Create the projected vector
        projected_vector = Arrow3D(
            start=ORIGIN,
            end=projected_end,
            color=RED,
            thickness=0.05
        )
        
        # Create the dotted line showing the projection
        dotted_line = DashedLine(
            start=original_end,
            end=projected_end,
            color=WHITE,
            dash_length=0.1
        )
        
        # Add initial elements to the scene
        self.add(axes, plane)
        
        # Animation sequence
        # 1. Initial camera rotation to show the 3D vector (2.5 seconds total)
        self.play(Create(vector), run_time=1.5)  # Create vector first (1.5s)
        self.move_camera(phi=65 * DEGREES, theta=45 * DEGREES, run_time=1)  # Then move camera (1s)
        
        # 2. Show the projection (2 seconds)
        self.play(
            Create(dotted_line),
            Create(projected_vector),
            run_time=2
        )
        
        # 3. Cinematic rotation to show from different angles (5.5 seconds)
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(5.5)
        self.stop_ambient_camera_rotation()
        
        # Optional: Add labels for clarity (fixed in frame)
        # original_label = Text("Original Vector", font_size=24).set_color(YELLOW)
        # projected_label = Text("Projected Vector", font_size=24).set_color(RED)
        # original_label.next_to(vector.get_end(), OUT+RIGHT, buff=0.5)
        # projected_label.next_to(projected_vector.get_end(), RIGHT, buff=0.5)
        # self.add_fixed_in_frame_mobjects(original_label, projected_label)

# To render: manim -pql 0.instructor-personal-data/lesson-1/manim-test.py VectorProjectionVisualization