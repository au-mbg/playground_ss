import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import ipywidgets as widgets
import random

from IPython.display import display, clear_output


# ============================================================
# 1. PHASES
# ============================================================

PHASES = [
    "Prophase",
    "Prometaphase",
    "Metaphase",
    "Anaphase",
    "Telophase",
    "Cytokinesis"
]


# ============================================================
# 2. BASIC CELL DRAWING FUNCTIONS
# ============================================================

def draw_cell(ax):

    ax.add_patch(patches.Ellipse(
        (5, 5),
        width=8.6,
        height=7.2,
        facecolor="#FCE8E8",
        edgecolor="#C77D9A",
        linewidth=2,
        zorder=0
    ))


def draw_nucleus(ax, center=(5, 5), radius=2.0, intact=True):

    ax.add_patch(patches.Circle(
        center,
        radius,
        facecolor="#E8E3F5",
        edgecolor="#8175A8",
        linewidth=2,
        linestyle="-" if intact else "--",
        alpha=0.8,
        zorder=1
    ))


# ============================================================
# 3. CHROMOSOME DRAWING FUNCTIONS
# ============================================================

def draw_x_chromosome(ax, x, y, scale=0.4, angle=0):
    """
    Replicated chromosome:
    two complete sister chromatids joined at the centromere.
    """

    t = np.linspace(0, 1, 100)

    # Both chromatids run from top to bottom.
    y_coords = scale * (1 - 2 * t)

    # Sister chromatids are separated at the ends
    # and joined at the centromere.
    separation = 0.35 * scale
    x_offset = separation * (1 + np.cos(2 * np.pi * t)) / 2

    chromatids = [-x_offset, x_offset]

    for x_coords in chromatids:

        # Rotate the chromosome
        x_rotated = (
            x_coords * np.cos(angle)
            - y_coords * np.sin(angle)
        )

        y_rotated = (
            x_coords * np.sin(angle)
            + y_coords * np.cos(angle)
        )

        ax.plot(
            x + x_rotated,
            y + y_rotated,
            color="#684C91",
            linewidth=4,
            solid_capstyle="round",
            zorder=4
        )

    # Centromere
    ax.add_patch(patches.Circle(
        (x, y),
        radius=0.045,
        color="#E5A83B",
        zorder=5
    ))


def draw_unreplicated_chromosome(ax, x, y, scale=0.3, angle=0):
    """
    One unreplicated chromosome consisting of a single chromatid.
    Drawn as a slightly curved rod.
    """

    t = np.linspace(0, 1, 50)

    x_coords = 0.10 * scale * np.sin(2 * np.pi * t)
    y_coords = scale * (1 - 2 * t)

    # Rotate
    x_rotated = (
        x_coords * np.cos(angle)
        - y_coords * np.sin(angle)
    )

    y_rotated = (
        x_coords * np.sin(angle)
        + y_coords * np.cos(angle)
    )

    ax.plot(
        x + x_rotated,
        y + y_rotated,
        color="#684C91",
        linewidth=3.5,
        solid_capstyle="round",
        zorder=4
    )


def draw_single_chromatid(ax, x, y, direction=1, scale=0.38):
    """
    Draw one separated chromosome during anaphase.
    The centromere leads towards the spindle pole,
    with two short, curved arms trailing behind.
    """

    t = np.linspace(0, 1, 60)

    # Distance from centromere towards the chromosome arms
    arm_length = scale

    # Slight curvature in the chromosome arms
    curve = 0.06 * scale * np.sin(np.pi * t)

    # Both arms extend away from the direction of movement
    x_arm = x - direction * arm_length * t + curve

    upper_y = y + arm_length * 0.65 * t
    lower_y = y - arm_length * 0.65 * t

    ax.plot(
        x_arm,
        upper_y,
        color="#684C91",
        linewidth=3.5,
        solid_capstyle="round",
        zorder=4
    )

    ax.plot(
        x_arm,
        lower_y,
        color="#684C91",
        linewidth=3.5,
        solid_capstyle="round",
        zorder=4
    )

    # Centromere
    ax.add_patch(patches.Circle(
        (x, y),
        radius=0.045,
        color="#E5A83B",
        zorder=5
    ))


# ============================================================
# 4. SPINDLE DRAWING FUNCTIONS
# ============================================================

def draw_pole(ax, x, y):

    ax.add_patch(patches.Circle(
        (x, y),
        0.18,
        color="#D18B38",
        zorder=5
    ))


def draw_spindle(ax, x1, x2, y1=5, y2=5):

    ax.plot(
        [x1, x2],
        [y1, y2],
        color="#E5A83B",
        linewidth=1.2,
        alpha=0.6,
        zorder=2
    )


# ============================================================
# 5. DRAW THE MITOSIS PHASES
# ============================================================

def draw_phase(ax, phase):

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")

    draw_cell(ax)


    # --------------------------------------------------------
    # PROPHASE
    # --------------------------------------------------------

    if phase == "Prophase":

        draw_nucleus(ax, radius=2.0)

        positions = [
            (4.0, 5.8, 0.1),
            (5.7, 5.6, -0.2),
            (4.5, 4.2, -0.2),
            (6.0, 4.3, 0.15)
        ]

        for x, y, angle in positions:
            draw_x_chromosome(
                ax, x, y,
                scale=0.4,
                angle=angle
            )

        draw_pole(ax, 2, 5)
        draw_pole(ax, 8, 5)


    # --------------------------------------------------------
    # PROMETAPHASE
    # --------------------------------------------------------

    elif phase == "Prometaphase":

        draw_nucleus(ax, radius=2.0, intact=False)

        positions = [
            (3.8, 6.0, 0.1),
            (5.2, 6.0, -0.2),
            (4.5, 4.5, 0.2),
            (6.0, 4.0, -0.1)
        ]

        for x, y, angle in positions:
            draw_x_chromosome(
                ax, x, y,
                scale=0.38,
                angle=angle
            )

        draw_pole(ax, 2, 5)
        draw_pole(ax, 8, 5)

        for x, y, angle in positions:
            draw_spindle(ax, 2, x, 5, y)
            draw_spindle(ax, 8, x, 5, y)


    # --------------------------------------------------------
    # METAPHASE
    # --------------------------------------------------------

    elif phase == "Metaphase":

        draw_pole(ax, 2, 5)
        draw_pole(ax, 8, 5)

        # Four separate replicated chromosomes at the equator

        positions = [
            (4.7, 3.6, 0.15),
            (5.3, 4.5, -0.15),
            (4.7, 5.5, -0.15),
            (5.3, 6.4, 0.15)
        ]

        for x, y, angle in positions:
            draw_x_chromosome(
                ax, x, y,
                scale=0.38,
                angle=angle
            )

        # Spindle fibres

        for x, y, angle in positions:
            draw_spindle(ax, 2, x, 5, y)
            draw_spindle(ax, 8, x, 5, y)

        # Metaphase plate

        ax.plot(
            [5, 5],
            [2, 8],
            color="#777777",
            linestyle="--",
            alpha=0.4
        )


    # --------------------------------------------------------
    # ANAPHASE
    # --------------------------------------------------------

    elif phase == "Anaphase":

        draw_pole(ax, 2, 5)
        draw_pole(ax, 8, 5)

        # Four chromosomes move towards each pole.
        # Each chromosome is now a single chromatid.

        positions = [3.5, 4.5, 5.5, 6.5]

        for y in positions:

            # Moving towards the left pole
            draw_single_chromatid(
                ax,
                3.5, y,
                direction=-1,
                scale=0.38
            )

            # Moving towards the right pole
            draw_single_chromatid(
                ax,
                6.5, y,
                direction=1,
                scale=0.38
            )

            draw_spindle(ax, 2, 3.5, 5, y)
            draw_spindle(ax, 8, 6.5, 5, y)


    # --------------------------------------------------------
    # TELOPHASE
    # --------------------------------------------------------

    elif phase == "Telophase":

        # Two new round nuclei form

        draw_nucleus(
            ax,
            center=(3.0, 5),
            radius=1.35
        )

        draw_nucleus(
            ax,
            center=(7.0, 5),
            radius=1.35
        )

        # Four individual, unreplicated chromosomes in each nucleus

        left_positions = [
            (2.5, 5.5, 0.1),
            (3.3, 5.5, -0.1),
            (2.5, 4.5, -0.1),
            (3.3, 4.5, 0.1)
        ]

        right_positions = [
            (6.5, 5.5, 0.1),
            (7.3, 5.5, -0.1),
            (6.5, 4.5, -0.1),
            (7.3, 4.5, 0.1)
        ]

        for x, y, angle in left_positions + right_positions:
            draw_unreplicated_chromosome(
                ax, x, y,
                scale=0.20,
                angle=angle
            )


    # --------------------------------------------------------
    # CYTOKINESIS
    # --------------------------------------------------------

    elif phase == "Cytokinesis":

        # Remove the original cell drawing

        ax.clear()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect("equal")
        ax.axis("off")

        # Draw two daughter cells

        for x in [2.7, 7.3]:

            ax.add_patch(patches.Ellipse(
                (x, 5),
                width=4.2,
                height=4.6,
                facecolor="#FCE8E8",
                edgecolor="#C77D9A",
                linewidth=2,
                zorder=0
            ))

            # Nucleus in each daughter cell

            draw_nucleus(
                ax,
                center=(x, 5),
                radius=1.0
            )

            # Four individual, unreplicated chromosomes
            # in each daughter cell

            positions = [
                (-0.4, 0.4, 0.1),
                (0.4, 0.4, -0.1),
                (-0.4, -0.4, -0.1),
                (0.4, -0.4, 0.1)
            ]

            for dx, dy, angle in positions:

                draw_unreplicated_chromosome(
                    ax,
                    x + dx,
                    5 + dy,
                    scale=0.20,
                    angle=angle
                )


# ============================================================
# 6. CREATE THE MITOSIS ORDERING WIDGET
# ============================================================

def mitosis_widget():

    # Shuffle the illustrations for this instance
    shuffled_phases = PHASES.copy()
    random.shuffle(shuffled_phases)

    # --------------------------------------------------------
    # CREATE SIX INDEPENDENT DROPDOWNS
    # --------------------------------------------------------

    dropdowns = []

    for i in range(6):

        shuffled_options = PHASES.copy()
        random.shuffle(shuffled_options)

        dropdown = widgets.Dropdown(
            options=["Choose a phase"] + shuffled_options,
            value="Choose a phase",
            description="",
            layout=widgets.Layout(width="100%")
        )

        dropdowns.append(dropdown)

    # --------------------------------------------------------
    # CREATE ILLUSTRATIONS AND CARDS
    # --------------------------------------------------------

    cards = []

    for i, phase in enumerate(shuffled_phases):

        output = widgets.Output()

        with output:

            fig, ax = plt.subplots(figsize=(3, 3))

            draw_phase(ax, phase)

            plt.show()
            plt.close(fig)

        card = widgets.VBox(
            [
                widgets.Label(f"Cell {i+1}"),
                dropdowns[i],
                output
            ],
            layout=widgets.Layout(
                width="100%",
                align_items="center"
            )
        )

        cards.append(card)

    # --------------------------------------------------------
    # ARRANGE THE SIX CARDS IN A 2 x 3 GRID
    # --------------------------------------------------------

    puzzle_grid = widgets.GridBox(
        children=cards,
        layout=widgets.Layout(
            grid_template_columns="repeat(3, 1fr)",
            grid_gap="20px",
            width="100%"
        )
    )

    # --------------------------------------------------------
    # BUTTONS AND FEEDBACK
    # --------------------------------------------------------

    check_button = widgets.Button(
        description="Check my answers",
        button_style="success",
        icon="check"
    )

    reveal_button = widgets.Button(
        description="Reveal correct order",
        button_style="info",
        icon="eye"
    )

    feedback = widgets.Output()

    # --------------------------------------------------------
    # CHECK ANSWERS
    # --------------------------------------------------------

    def check_answers(button):

        with feedback:

            clear_output()

            answers = [
                dropdown.value
                for dropdown in dropdowns
            ]

            if "Choose a phase" in answers:

                print("Please select a phase for all six cells.")
                return

            correct = sum(
                answers[i] == shuffled_phases[i]
                for i in range(6)
            )

            print(f"You got {correct} out of 6 correct!")

            if correct == 6:
                print(
                    "Excellent! You have identified all six "
                    "phases correctly!"
                )

            else:
                print(
                    "Have another look at the illustrations "
                    "and try again."
                )

    # --------------------------------------------------------
    # REVEAL ANSWERS
    # --------------------------------------------------------

    def reveal_answers(button):

        for i in range(6):
            dropdowns[i].value = shuffled_phases[i]

        with feedback:

            clear_output()

            print(
                "Here is the correct answer for each illustration!"
            )

    # --------------------------------------------------------
    # CONNECT BUTTONS
    # --------------------------------------------------------

    check_button.on_click(check_answers)
    reveal_button.on_click(reveal_answers)

    buttons = widgets.HBox(
        [check_button, reveal_button],
        layout=widgets.Layout(
            justify_content="center",
            gap="15px"
        )
    )

    # --------------------------------------------------------
    # RETURN THE COMPLETE WIDGET
    # --------------------------------------------------------

    return widgets.VBox(
        [
            puzzle_grid,
            buttons,
            feedback
        ],
        layout=widgets.Layout(
            width="100%"
        )
    )