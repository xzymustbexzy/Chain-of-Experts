def team_formulation(P, C, S, RequiredSkill, IndividualSkill):
    """
    Args:
        P: List of people or staff
        C: List of projects
        S: List of skills or expertise
        RequiredSkill: dict, key is a tuple (c, s), value is the required level of skill `s` for project `c`
        IndividualSkill: dict, key is a tuple (p, s), value is the level of skill `s` of individual `p`

    Returns:
        max_skill_shortage: a float, the minimized maximum skill shortage over all projects
    """
    max_skill_shortage = 0
    return max_skill_shortage