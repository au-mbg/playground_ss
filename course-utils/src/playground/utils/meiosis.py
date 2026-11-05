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
    "Prophase I",
    "Metaphase I",
    "Anaphase I",
    "Telophase I & Cytokinesis",
    "Prophase II",
    "Metaphase II",
    "Anaphase II",
    "Telophase II & Cytokinesis"
]


# ============================================================
# 2. COLOURS
# ============================================================

# Each homologous pair has two different colours.
# Pair 1: purple and pink
# Pair 2: blue and green

PURPLE = "#684C91"
PINK = "#D16B86"
BLUE = "#3985A8"
GREEN = "#54A68A"

CENTROMERE = "#E5A83B"


# ============================================================
# 3. BASIC DRAWING FUNCTIONS
# ============================================================

def setup_axes(ax):
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")


def draw_cell(ax, center=(8, 5), width=8.6, height=7.2):

    ax.add_patch(patches.Ellipse(
        center,
        width=width,
        height=height,
        facecolor="#FCE8E8",
        edgecolor="#C77D9A",
        linewidth=2,
        zorder=0
    ))


def draw_nucleus(ax, center, radius=1.5, intact=True):

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


def draw_pole(ax, x, y):

    ax.add_patch(patches.Circle(
        (x, y),
        0.13,
        color="#D18B38",
        zorder=5
    ))


def draw_spindle(ax, x1, x2, y1, y2):

    ax.plot(
        [x1, x2],
        [y1, y2],
        color="#E5A83B",
        linewidth=1.1,
        alpha=0.55,
        zorder=2
    )


# ============================================================
# 4. CHROMOSOME DRAWING FUNCTIONS
# ============================================================

def draw_x_chromosome(ax, x, y, scale=0.4, angle=0, color=PURPLE):
    """
    Replicated chromosome with two sister chromatids
    joined at the centromere.
    """

    t = np.linspace(0, 1, 100)

    y_coords = scale * (1 - 2 * t)

    separation = 0.35 * scale
    x_offset = separation * (1 + np.cos(2 * np.pi * t)) / 2

    for x_coords in [-x_offset, x_offset]:

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
            color=color,
            linewidth=4,
            solid_capstyle="round",
            zorder=4
        )

    ax.add_patch(patches.Circle(
        (x, y),
        radius=0.045,
        color=CENTROMERE,
        zorder=5
    ))


def draw_single_chromatid(ax, x, y, direction=1, scale=0.38, color=PURPLE):
    """
    Individual chromosome after sister chromatids separate.
    The centromere leads towards the spindle pole.
    """

    t = np.linspace(0, 1, 60)

    arm_length = scale
    curve = 0.06 * scale * np.sin(np.pi * t)

    x_arm = x - direction * arm_length * t + curve

    upper_y = y + arm_length * 0.65 * t
    lower_y = y - arm_length * 0.65 * t

    ax.plot(
        x_arm,
        upper_y,
        color=color,
        linewidth=3.5,
        solid_capstyle="round",
        zorder=4
    )

    ax.plot(
        x_arm,
        lower_y,
        color=color,
        linewidth=3.5,
        solid_capstyle="round",
        zorder=4
    )

    ax.add_patch(patches.Circle(
        (x, y),
        radius=0.045,
        color=CENTROMERE,
        zorder=5
    ))


def draw_unreplicated_chromosome(ax, x, y, scale=0.25, angle=0, color=PURPLE):
    """
    One unreplicated chromosome in a haploid daughter cell.
    """

    t = np.linspace(0, 1, 50)

    x_coords = 0.10 * scale * np.sin(2 * np.pi * t)
    y_coords = scale * (1 - 2 * t)

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
        color=color,
        linewidth=3.5,
        solid_capstyle="round",
        zorder=4
    )


# ============================================================
# 5. HELPER: DRAW ONE CELL DURING MEIOSIS II
# ============================================================

def draw_meiosis_II_cell(ax, center_x, phase):

    cx = center_x
    cy = 5

    draw_cell(
        ax,
        center=(cx, cy),
        width=5.5,
        height=7.2
    )

    # Two replicated chromosomes in this haploid cell.
    # One chromosome from each homologous pair.

    chromosome_positions = [
        (cx, 5.8, PURPLE),
        (cx, 4.2, BLUE)
    ]

    if phase == "Prophase II":

        draw_nucleus(ax, (cx, cy), radius=1.7, intact=True)

        for x, y, color in chromosome_positions:
            draw_x_chromosome(
                ax, x, y,
                scale=0.45,
                color=color
            )

        draw_pole(ax, cx - 1.9, 5)
        draw_pole(ax, cx + 1.9, 5)

    elif phase == "Metaphase II":

        draw_pole(ax, cx - 1.9, 5)
        draw_pole(ax, cx + 1.9, 5)

        for x, y, color in chromosome_positions:

            draw_x_chromosome(
                ax, x, y,
                scale=0.45,
                color=color
            )

            draw_spindle(ax, cx - 1.9, x, 5, y)
            draw_spindle(ax, cx + 1.9, x, 5, y)

        ax.plot(
            [cx, cx],
            [3.1, 6.9],
            color="#777777",
            linestyle="--",
            alpha=0.4
        )

    elif phase == "Anaphase II":

        draw_pole(ax, cx - 1.9, 5)
        draw_pole(ax, cx + 1.9, 5)

        for color in [PURPLE, BLUE]:

            # One chromatid moves towards each pole.
            draw_single_chromatid(
                ax,
                cx - 0.8, 5,
                direction=-1,
                scale=0.32,
                color=color
            )

            draw_single_chromatid(
                ax,
                cx + 0.8, 5,
                direction=1,
                scale=0.32,
                color=color
            )

            draw_spindle(ax, cx - 1.9, cx - 0.8, 5, 5)
            draw_spindle(ax, cx + 1.9, cx + 0.8, 5, 5)


# ============================================================
# 6. DRAW THE EIGHT MEIOSIS PHASES
# ============================================================

def draw_phase(ax, phase):

    setup_axes(ax)

    # --------------------------------------------------------
    # PROPHASE I
    # --------------------------------------------------------

    if phase == "Prophase I":

        draw_cell(ax)
        draw_nucleus(ax, (8, 5), radius=2.0, intact=True)

        # Homologous chromosomes pair up.
        # Two tetrads are represented by two pairs of X chromosomes.

        positions = [
            (6.8, 5.8, PURPLE),
            (7.6, 5.8, PINK),
            (8.4, 4.3, BLUE),
            (9.2, 4.3, GREEN)
        ]

        for x, y, color in positions:

            draw_x_chromosome(
                ax, x, y,
                scale=0.48,
                color=color
            )

        draw_pole(ax, 4, 5)
        draw_pole(ax, 12, 5)


    # --------------------------------------------------------
    # METAPHASE I
    # --------------------------------------------------------

    elif phase == "Metaphase I":

        draw_cell(ax)

        draw_pole(ax, 4, 5)
        draw_pole(ax, 12, 5)

        # Homologous pairs line up together at the equator.
        # Each pair consists of two replicated chromosomes.

        positions = [
            (8.0, 7.0, PURPLE),
            (8.0, 5.7, PINK),
            (8.0, 4.3, BLUE),
            (8.0, 3.0, GREEN)
        ]

        for x, y, color in positions:

            draw_x_chromosome(
                ax, x, y,
                scale=0.48,
                color=color
            )

            draw_spindle(ax, 4, x, 5, y)
            draw_spindle(ax, 12, x, 5, y)

        ax.plot(
            [8, 8],
            [2.5, 7.5],
            color="#777777",
            linestyle="--",
            alpha=0.4
        )


    # --------------------------------------------------------
    # ANAPHASE I
    # --------------------------------------------------------

    elif phase == "Anaphase I":

        draw_cell(ax)

        draw_pole(ax, 4, 5)
        draw_pole(ax, 12, 5)

        # Homologous chromosomes separate.
        # Sister chromatids remain joined.
        #
        # One homolog from each pair moves to each pole.

        left_chromosomes = [
            (5.5, 6.0, PURPLE),
            (5.5, 4.0, BLUE)
        ]

        right_chromosomes = [
            (10.5, 6.0, PINK),
            (10.5, 4.0, GREEN)
        ]

        for x, y, color in left_chromosomes + right_chromosomes:

            draw_x_chromosome(
                ax, x, y,
                scale=0.48,
                color=color
            )

        for x, y, color in left_chromosomes:
            draw_spindle(ax, 4, x, 5, y)

        for x, y, color in right_chromosomes:
            draw_spindle(ax, 12, x, 5, y)


    # --------------------------------------------------------
    # TELOPHASE I & CYTOKINESIS
    # --------------------------------------------------------

    elif phase == "Telophase I & Cytokinesis":

        # Two daughter cells.
        # Each contains two replicated chromosomes.

        for cx, colors in [
            (4.5, [PURPLE, BLUE]),
            (11.5, [PINK, GREEN])
        ]:

            draw_cell(
                ax,
                center=(cx, 5),
                width=5.0,
                height=6.5
            )

            draw_nucleus(
                ax,
                (cx, 5),
                radius=1.35
            )

            positions = [
                (cx - 0.55, 5.4),
                (cx + 0.55, 4.6)
            ]

            for (x, y), color in zip(positions, colors):

                draw_x_chromosome(
                    ax, x, y,
                    scale=0.38,
                    color=color
                )


    # --------------------------------------------------------
    # PROPHASE II
    # --------------------------------------------------------

    elif phase == "Prophase II":

        # Two cells enter the second division.

        draw_meiosis_II_cell(ax, 4.5, "Prophase II")
        draw_meiosis_II_cell(ax, 11.5, "Prophase II")


    # --------------------------------------------------------
    # METAPHASE II
    # --------------------------------------------------------

    elif phase == "Metaphase II":

        draw_meiosis_II_cell(ax, 4.5, "Metaphase II")
        draw_meiosis_II_cell(ax, 11.5, "Metaphase II")


    # --------------------------------------------------------
    # ANAPHASE II
    # --------------------------------------------------------

    elif phase == "Anaphase II":

        draw_meiosis_II_cell(ax, 4.5, "Anaphase II")
        draw_meiosis_II_cell(ax, 11.5, "Anaphase II")


    # --------------------------------------------------------
    # TELOPHASE II & CYTOKINESIS
    # --------------------------------------------------------

    elif phase == "Telophase II & Cytokinesis":

        # Four haploid daughter cells.
        # Each contains two unreplicated chromosomes.

        daughter_cells = [
            (4.0, 7.2, [PURPLE, BLUE]),
            (12.0, 7.2, [PINK, GREEN]),
            (4.0, 2.8, [PURPLE, BLUE]),
            (12.0, 2.8, [PINK, GREEN])
        ]

        for cx, cy, colors in daughter_cells:

            ax.add_patch(patches.Ellipse(
                (cx, cy),
                width=3.4,
                height=3.4,
                facecolor="#FCE8E8",
                edgecolor="#C77D9A",
                linewidth=2,
                zorder=0
            ))

            draw_nucleus(
                ax,
                (cx, cy),
                radius=0.85
            )

            # Two individual chromosomes in each cell.

            positions = [
                (cx - 0.3, cy + 0.2),
                (cx + 0.3, cy - 0.2)
            ]

            for (x, y), color in zip(positions, colors):

                draw_unreplicated_chromosome(
                    ax, x, y,
                    scale=0.22,
                    color=color
                )



# ============================================================
# 7. MAIN WIDGET FUNCTION
# ============================================================

def meiosis_ordering_widget():
    """
    Interactive meiosis phase-ordering puzzle.

    Students arrange eight illustrated stages of meiosis
    in the correct chronological order.
    """

    # Shuffle the illustrations for each new widget instance.
    shuffled_phases = PHASES.copy()
    random.shuffle(shuffled_phases)

    # --------------------------------------------------------
    # CREATE EIGHT INDEPENDENT DROPDOWNS
    # --------------------------------------------------------

    dropdowns = []

    for i in range(8):

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

            fig, ax = plt.subplots(figsize=(4, 3))

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
    # ARRANGE THE EIGHT CARDS IN A 2 x 4 GRID
    # --------------------------------------------------------

    puzzle_grid = widgets.GridBox(
        children=cards,
        layout=widgets.Layout(
            grid_template_columns="repeat(4, 1fr)",
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

                print("Please select a phase for all eight cells.")
                return

            correct = sum(
                answers[i] == shuffled_phases[i]
                for i in range(8)
            )

            print(f"You got {correct} out of 8 correct!")

            if correct == 8:

                print(
                    "Excellent! You have identified all eight "
                    "stages of meiosis correctly!"
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

        for i in range(8):
            dropdowns[i].value = shuffled_phases[i]

        with feedback:

            clear_output()

            print("Here is the correct order of meiosis!")

    check_button.on_click(check_answers)
    reveal_button.on_click(reveal_answers)

    # --------------------------------------------------------
    # RETURN THE COMPLETE WIDGET
    # --------------------------------------------------------

    buttons = widgets.HBox(
        [check_button, reveal_button],
        layout=widgets.Layout(
            justify_content="center",
            gap="15px"
        )
    )

    return widgets.VBox(
        [
            puzzle_grid,
            buttons,
            feedback
        ],
        layout=widgets.Layout(width="100%")
    )
