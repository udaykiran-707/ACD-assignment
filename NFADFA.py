import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


# ============================================================
# 1. DFA VISUALIZATION
# ============================================================

def visualize_dfa(states, transitions, start_state, final_states):
    G = nx.DiGraph()

    # Add states
    for state in states:
        G.add_node(state)

    # Add transitions
    for (source, symbol), destination in transitions.items():
        if G.has_edge(source, destination):
            G[source][destination]["label"] += ", " + symbol
        else:
            G.add_edge(source, destination, label=symbol)

    pos = nx.spring_layout(G, seed=10)

    # Draw states
    normal_states = [s for s in states if s not in final_states]

    nx.draw_networkx_nodes(
        G, pos,
        nodelist=normal_states,
        node_color="lightblue",
        node_size=2000
    )

    nx.draw_networkx_nodes(
        G, pos,
        nodelist=list(final_states),
        node_color="lightgreen",
        node_size=2000
    )

    # Draw edges
    nx.draw_networkx_edges(
        G, pos,
        arrows=True,
        arrowsize=20,
        connectionstyle="arc3,rad=0.1"
    )

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=12)

    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_size=11
    )

    # Start arrow
    start_position = pos[start_state]

    plt.annotate(
        "",
        xy=start_position,
        xytext=(start_position[0] - 0.25,
                start_position[1] + 0.25),
        arrowprops=dict(arrowstyle="->", lw=1.5)
    )

    plt.title("DFA Visualization")
    plt.axis("off")
    plt.show()


# Example DFA
dfa_states = {"q0", "q1"}

dfa_transitions = {
    ("q0", "0"): "q0",
    ("q0", "1"): "q1",
    ("q1", "0"): "q0",
    ("q1", "1"): "q1"
}

dfa_start = "q0"
dfa_final = {"q1"}

visualize_dfa(
    dfa_states,
    dfa_transitions,
    dfa_start,
    dfa_final
)


# ============================================================
# 2. NFA VISUALIZATION
# ============================================================

def visualize_nfa(states, transitions, start_state, final_states):
    G = nx.MultiDiGraph()

    # Add states
    for state in states:
        G.add_node(state)

    # Add transitions
    for (source, symbol), destinations in transitions.items():
        for destination in destinations:
            G.add_edge(
                source,
                destination,
                label=symbol
            )

    pos = nx.spring_layout(G, seed=20)

    # Draw normal states
    normal_states = [s for s in states if s not in final_states]

    nx.draw_networkx_nodes(
        G, pos,
        nodelist=normal_states,
        node_color="lightyellow",
        node_size=2000
    )

    # Draw final states
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=list(final_states),
        node_color="lightgreen",
        node_size=2000
    )

    # Draw edges
    nx.draw_networkx_edges(
        G, pos,
        arrows=True,
        arrowsize=20,
        connectionstyle="arc3,rad=0.15"
    )

    # Draw state labels
    nx.draw_networkx_labels(G, pos, font_size=12)

    # Create edge labels
    edge_labels = {}

    for source, destination, data in G.edges(data=True):
        key = (source, destination)

        if key in edge_labels:
            edge_labels[key] += ", " + data["label"]
        else:
            edge_labels[key] = data["label"]

    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_size=11
    )

    # Start arrow
    start_position = pos[start_state]

    plt.annotate(
        "",
        xy=start_position,
        xytext=(start_position[0] - 0.25,
                start_position[1] + 0.25),
        arrowprops=dict(arrowstyle="->", lw=1.5)
    )

    plt.title("NFA Visualization")
    plt.axis("off")
    plt.show()


# Example NFA
nfa_states = {"q0", "q1", "q2"}

nfa_alphabet = {"0", "1"}

nfa_transitions = {
    ("q0", "0"): {"q0"},
    ("q0", "1"): {"q0", "q1"},
    ("q1", "1"): {"q2"},
    ("q2", "0"): {"q2"},
    ("q2", "1"): {"q2"}
}

nfa_start = "q0"
nfa_final = {"q2"}

visualize_nfa(
    nfa_states,
    nfa_transitions,
    nfa_start,
    nfa_final
)


# ============================================================
# 3. NFA TO DFA CONVERSION
# ============================================================

def nfa_to_dfa(
    nfa_states,
    alphabet,
    nfa_transitions,
    nfa_start,
    nfa_final
):
    # DFA start state is {NFA start state}
    start = frozenset([nfa_start])

    dfa_states = {start}
    dfa_transitions = {}

    queue = deque([start])

    while queue:

        current = queue.popleft()

        for symbol in alphabet:

            next_states = set()

            # Find all NFA destinations
            for state in current:

                destinations = nfa_transitions.get(
                    (state, symbol),
                    set()
                )

                next_states.update(destinations)

            next_state = frozenset(next_states)

            # Store DFA transition
            dfa_transitions[
                (current, symbol)
            ] = next_state

            # Add new DFA state
            if next_state not in dfa_states:
                dfa_states.add(next_state)
                queue.append(next_state)

    # DFA final state:
    # Any DFA state containing an NFA final state
    dfa_final = set()

    for state in dfa_states:
        if any(nfa_state in nfa_final for nfa_state in state):
            dfa_final.add(state)

    return (
        dfa_states,
        dfa_transitions,
        start,
        dfa_final
    )


# Perform conversion
converted_states, converted_transitions, converted_start, converted_final = \
    nfa_to_dfa(
        nfa_states,
        nfa_alphabet,
        nfa_transitions,
        nfa_start,
        nfa_final
    )


# ============================================================
# 4. PRINT NFA → DFA CONVERSION
# ============================================================

print("\n================ NFA TO DFA CONVERSION ================\n")

print("DFA States:")

for state in converted_states:
    print(set(state))

print("\nDFA Transitions:")

for (source, symbol), destination in converted_transitions.items():
    print(
        set(source),
        "--", symbol, "-->",
        set(destination)
    )

print("\nDFA Start State:")
print(set(converted_start))

print("\nDFA Final States:")

for state in converted_final:
    print(set(state))


# ============================================================
# 5. VISUALIZE CONVERTED DFA
# ============================================================

def visualize_converted_dfa(
    states,
    transitions,
    start_state,
    final_states
):

    G = nx.DiGraph()

    # Convert frozensets to readable names
    def state_name(state):
        if len(state) == 0:
            return "∅"

        return "{" + ",".join(sorted(state)) + "}"

    # Add nodes
    for state in states:
        G.add_node(state_name(state))

    # Add edges
    for (source, symbol), destination in transitions.items():

        source_name = state_name(source)
        destination_name = state_name(destination)

        if G.has_edge(source_name, destination_name):
            G[source_name][destination_name]["label"] += ", " + symbol
        else:
            G.add_edge(
                source_name,
                destination_name,
                label=symbol
            )

    pos = nx.spring_layout(G, seed=30)

    start_name = state_name(start_state)
    final_names = [state_name(s) for s in final_states]

    normal_names = [
        state_name(s)
        for s in states
        if s not in final_states
    ]

    # Normal states
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=normal_names,
        node_color="lightblue",
        node_size=2500
    )

    # Final states
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=final_names,
        node_color="lightgreen",
        node_size=2500
    )

    # Edges
    nx.draw_networkx_edges(
        G, pos,
        arrows=True,
        arrowsize=20,
        connectionstyle="arc3,rad=0.1"
    )

    # Labels
    nx.draw_networkx_labels(
        G, pos,
        font_size=11
    )

    edge_labels = nx.get_edge_attributes(G, "label")

    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_size=11
    )

    # Start arrow
    start_position = pos[start_name]

    plt.annotate(
        "",
        xy=start_position,
        xytext=(
            start_position[0] - 0.3,
            start_position[1] + 0.3
        ),
        arrowprops=dict(
            arrowstyle="->",
            lw=1.5
        )
    )

    plt.title("NFA → DFA Conversion")
    plt.axis("off")
    plt.show()


visualize_converted_dfa(
    converted_states,
    converted_transitions,
    converted_start,
    converted_final
)
