"""
compatibility between Python version
"""

# __builtins__.set is in >=2.4, sets.Set is in >=2.3.
# Be careful that the compatibility is not perfect.
try:
    set, frozenset
except NameError:
    import sets
    __builtins__["set"] = sets.Set
    __builtins__["frozenset"] = sets.ImmutableSet
    del sets
