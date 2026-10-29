import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from matplotlib.patches import Ellipse, Circle
from IPython.display import display

import sys
sys.path.insert(0, "course_utils")

# Genotypes associated with each flower colour
phenotypes = {
    "Red": "RR",
    "Pink": "Rr",
    "White": "rr"
}

colours = {
    "RR": "#D93645",
    "Rr": "#F28F9B",
    "rr": "#FFF9EF"
}

phenotype_names = {
    "RR": "Red",
    "Rr": "Pink",
    "rr": "White"
}

# Possible alleles passed on by each parent
gametes = {
    "RR": ["R", "R"],
    "Rr": ["R", "r"],
    "rr": ["r", "r"]
}


def draw_tiny_flower(ax, x, y, genotype, size=0.12):
    """Draw one flower with a colour determined by its genotype."""
    colour = colours[genotype]

    for i in range(5):
        angle = np.deg2rad(90 + i * 72)
        px = x + size * 0.65 * np.cos(angle)
        py = y + size * 0.65 * np.sin(angle)

        ax.add_patch(
            Ellipse(
                (px, py),
                width=size * 0.8,
                height=size * 1.2,
                angle=i * 72,
                facecolor=colour,
                edgecolor="#C66B72" if genotype != "rr" else "#D8CFC3",
                linewidth=0.5,
                zorder=3
            )
        )

    # Flower centre
    ax.add_patch(
        Circle(
            (x, y),
            size * 0.18,
            facecolor="#E9B949",
            edgecolor="#B88724",
            linewidth=0.4,
            zorder=4
        )
    )

    # Stem
    ax.plot(
        [x, x],
        [y - size * 0.6, y - size * 2.0],
        color="#426B43",
        linewidth=0.7,
        zorder=1
    )


def flower_garden(parent1, parent2, n_offspring=30):
    """Simulate offspring and display flowers and phenotype counts."""

    # Convert parental flower colours to genotypes
    genotype1 = phenotypes[parent1]
    genotype2 = phenotypes[parent2]

    # Generate all possible offspring genotypes
    outcomes = []

    for a1 in gametes[genotype1]:
        for a2 in gametes[genotype2]:
            genotype = "".join(
                sorted([a1, a2], key=lambda allele: allele.islower())
            )
            outcomes.append(genotype)

    # Expected probabilities from the genetic cross
    genotypes = ["RR", "Rr", "rr"]

    expected = {
        g: outcomes.count(g) / len(outcomes)
        for g in genotypes
    }

    # Randomly simulate the offspring
    rng = np.random.default_rng()
    offspring = rng.choice(outcomes, size=n_offspring)

    # Count the simulated flower colours
    counts = [
        np.sum(offspring == g)
        for g in genotypes
    ]

    # Create two plots side by side
    columns = min(10, n_offspring)
    rows = int(np.ceil(n_offspring / columns))

    fig, axes = plt.subplots(
        2, 1,
        figsize=(10, max(6, rows * 0.55+3)),
        gridspec_kw={"height_ratios": [2, 1]}
    )

    fig.patch.set_facecolor("#FFFEFA")

    # LEFT: Draw the simulated offspring as a garden
    ax = axes[0]
    ax.set_facecolor("#FFFEFA")

    for i, genotype in enumerate(offspring):
        row = i // columns
        col = i % columns

        x = col + 0.5
        y = rows - row - 0.5

        draw_tiny_flower(ax, x, y, genotype)

    ax.set_xlim(0, columns)
    ax.set_ylim(-0.4, rows + 0.4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Simulated offspring", color="#24464A")

    # RIGHT: Bar chart of simulated phenotype counts
    ax = axes[1]
    ax.set_facecolor("#FFFEFA")

    names = ["Red", "Pink", "White"]
    bar_colours = ["#D93645", "#F28F9B", "#FFF9EF"]
    edge_colours = ["#A92332", "#C66B72", "#BEB5A8"]

    bars = ax.bar(
        names,
        counts,
        color=bar_colours,
        edgecolor=edge_colours,
        linewidth=1.5
    )

    ax.bar_label(bars, padding=4, fontsize=11)
    ax.set_ylabel("Number of flowers")
    ax.set_title("Simulated flower colours", color="#24464A")
    ax.set_ylim(0, max(counts) * 1.2 + 1)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)

    fig.suptitle(
        f"{parent1} × {parent2} (n = {n_offspring})",
        fontsize=15,
        fontweight="bold",
        color="#24464A"
    )

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

    # Compare expected and simulated proportions
    print("Phenotype proportions")
    print(f"{'Colour':<10} {'Expected':>10} {'Simulated':>12}")

    for genotype in genotypes:
        observed = np.mean(offspring == genotype)

        print(
            f"{phenotype_names[genotype]:<10} "
            f"{expected[genotype]:>9.1%} "
            f"{observed:>11.1%}"
        )
def flower_garden_widget():
    """Create an interactive flower genetics widget."""

    parent1 = widgets.Dropdown(
        options=["Red", "Pink", "White"],
        value="Red",
        description="Parent 1:"
    )

    parent2 = widgets.Dropdown(
        options=["Red", "Pink", "White"],
        value="White",
        description="Parent 2:"
    )

    n_slider = widgets.IntSlider(
        value=30,
        min=10,
        max=100,
        step=10,
        description="Offspring:",
        continuous_update=False
    )

    ui = widgets.VBox([parent1, parent2, n_slider])

    output = widgets.interactive_output(
        flower_garden,
        {
            "parent1": parent1,
            "parent2": parent2,
            "n_offspring": n_slider
        }
    )

    return widgets.VBox([ui, output])