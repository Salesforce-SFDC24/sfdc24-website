import matplotlib.pyplot as plt

def visualize_results(results):
    """
    Visualize CLIPS results using a bar chart.
    """
    priorities = [fact['priority'] for fact in results]
    counts = {priority: priorities.count(priority) for priority in set(priorities)}

    plt.bar(counts.keys(), counts.values())
    plt.xlabel("Priority")
    plt.ylabel("Count")
    plt.title("Task Priorities from CLIPS")
    plt.show()

# Example results
example_results = [
    {"priority": "High"},
    {"priority": "Low"},
    {"priority": "High"}
]

visualize_results(example_results)
