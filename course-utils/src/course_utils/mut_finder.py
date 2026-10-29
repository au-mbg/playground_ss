import random
from IPython.display import display, HTML

# --- Fix seed for reproducibility ---
random.seed(42)

# --- Helper function to generate random DNA sequences ---
def random_dna(length):
    return ''.join(random.choices('acgt', k=length))

# --- Generate parental alleles ---
mom1 = random_dna(1000)
mom2 = random_dna(1000)
dad1 = random_dna(1000)
dad2 = random_dna(1000)

# --- Child inherits one allele from each parent ---
child1 = ''.join(random.choice([mom1[i], mom2[i]]) for i in range(1000))
child2 = ''.join(random.choice([dad1[i], dad2[i]]) for i in range(1000))

# --- Introduce independent de novo mutations in both child alleles ---
def introduce_mutations(seq, num_mutations, parents):
    seq_list = list(seq)
    mutation_positions = random.sample(range(len(seq)), num_mutations)
    for pos in mutation_positions:
        parent_bases = {allele[pos] for allele in parents}
        seq_list[pos] = random.choice([b for b in "acgt" if b not in parent_bases])
    return ''.join(seq_list), mutation_positions

child1, mut_pos_child1 = introduce_mutations(child1, 5, [mom1, mom2, dad1, dad2])
child2, mut_pos_child2 = introduce_mutations(child2, 5, [mom1, mom2, dad1, dad2])

# --- Scrollable sequence display (full sequences) ---
def show_sequences_scrollable(mom1, mom2, dad1, dad2, child1, child2):
    html = f"""
    <h4>Parental and Child Sequences</h4>
    <div style="font-family: monospace; white-space: nowrap; overflow-x: auto; border: 1px solid #ccc; padding: 10px;">
        <strong>Mom allele 1:</strong> {mom1}<br>
        <strong>Mom allele 2:</strong> {mom2}<br>
        <strong>Dad allele 1:</strong> {dad1}<br>
        <strong>Dad allele 2:</strong> {dad2}<br>
        <strong>Child allele 1:</strong> {child1}<br>
        <strong>Child allele 2:</strong> {child2}
    </div>
    """
    display(HTML(html))

# --- Display sequences before running mutation analysis ---
show_sequences_scrollable(mom1, mom2, dad1, dad2, child1, child2)

from IPython.display import display, HTML

# --- Function to find and highlight de novo mutations ---
def de_novo_mut(mom1, mom2, dad1, dad2, child, show_html=True, line_length=100):
    highlighted = []
    mutation_positions = []
    
    for i in range(len(child)):
        if child[i] in [mom1[i], mom2[i], dad1[i], dad2[i]]:
            highlighted.append(child[i])
        else:
            highlighted.append(f'<span style="color: red; font-weight: bold;">{child[i]}</span>')
            mutation_positions.append(i + 1)

    if show_html:
        html_lines = []
        for start in range(0, len(highlighted), line_length):
            line = ''.join(highlighted[start:start+line_length])
            html_lines.append(line)
        html_code = '<div style="white-space: pre; font-family: monospace; line-height: 1.5em; border: 1px solid #ddd; padding: 10px; text-align: left;">'
        html_code += '<br>'.join(html_lines)
        html_code += '</div>'
        display(HTML(html_code))
    
    return mutation_positions

# --- Run mutation detection and show results ---
print("Analyzing Child allele 1:")
mutations_found_1 = de_novo_mut(mom1, mom2, dad1, dad2, child1)
print(f"Found {len(mutations_found_1)} de novo mutations at positions: {mutations_found_1}\n")

print("Analyzing Child allele 2:")
mutations_found_2 = de_novo_mut(mom1, mom2, dad1, dad2, child2)
print(f"Found {len(mutations_found_2)} de novo mutations at positions: {mutations_found_2}")


