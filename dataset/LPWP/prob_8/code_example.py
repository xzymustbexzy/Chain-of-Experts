
with open("code_example.py", "w") as f:
    f.write("""def prob_8(clothing_company, tech_company):
    \"""
    Args:
        clothing_company: an integer, representing the investment in the clothing company.
        tech_company: an integer, representing the investment in the tech company.
    Returns:
        obj: an integer, representing the maximum profit.
    \"""
    obj = 0.07 * clothing_company + 0.10 * tech_company
    # To be implemented
    return obj
    """)
