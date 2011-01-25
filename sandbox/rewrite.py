"""
String rewrite systems.
"""


class Rewrite (object):
    """
    Rewrite system
    """
    def __init__(self, alphabet, rules):
        """
        alphabet: tuple of characters.
        rules: dictionary whose key is rewritten to value.

        We mean "character" the strings never overlap each other.
        """
        self.alphabet = alphabet
        self.rules = dict(rules)

    def simplify(self, string):
        """
        Left-most reduction.
        """
        max_redux = max([len(k) for k in self.rules])
        i = 0
        while i < len(string):
            for j in range(i + 1, i + max_redux + 1):
                if string[i:j] in self.rules:
                    redux = string[i:j]
                    string = string.replace(redux, self.rules[redux], 1)
                    i = max(0, i - max_redux)
                    break
            else:
                i += 1
        return string

    def __contains__(self, string):
        """
        Return True if string consists of only the characters in
        alphabet, i.e., the string is in the Kleene closure.
        """
        for c in self.alphabet:
            string = "".join(string.split(c))
        return string == ""
