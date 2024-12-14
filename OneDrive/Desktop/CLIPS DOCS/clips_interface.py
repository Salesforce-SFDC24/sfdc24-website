from clips import Environment

def run_clips_rule(rule_file, facts):
    """
    Load CLIPS rules and evaluate them with given facts.
    """
    env = Environment()
    env.load(rule_file)

    for fact in facts:
        env.assert_string(fact)

    env.run()

    results = []
    for fact in env.facts():
        if fact.template.name != "initial-fact":
            results.append(fact)

    return results
