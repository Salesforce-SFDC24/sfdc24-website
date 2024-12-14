from clips import Environment

def run_clips_rule(rules_file, facts):
    """
    Load CLIPS rules and evaluate them with given facts.
    """
    env = Environment()
    env.load(rules_file)

    # Assert each fact into the environment
    for fact in facts:
        env.assert_string(fact)

    # Run rules
    print("Running CLIPS...")
    env.run()

    # Collect and return results
    results = []
    for fact in env.facts():
        if fact.template.name != "initial-fact":
            results.append(fact)
    return results

if __name__ == "__main__":
    # Test rules.clp
    rules_file = "rules.clp"  # Ensure this file exists in your directory
    test_facts = [
        '(decision (input "critical"))',
        '(decision (input "optional"))'
    ]

    # Run CLIPS and print results
    results = run_clips_rule(rules_file, test_facts)
    print("Results from CLIPS:")
    for result in results:
        print(result)
