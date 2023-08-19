# The first nine numbers 1-9 (yksi to yhdeksän) that will repeat in all written numbers.
one_to_ten = [
    # The first index is left for zero but written as empty string to the end of the numbers in certain cases.
    '', 'yksi', 'kaksi', 'kolme', 'neljä', 'viisi', 'kuusi', 'seitsemän', 'kahdeksan', 'yhdeksän', 'kymmenen'
]

powers_of_ten = {
    100: 'sata',
    1000: 'tuhat',
    # https://fi.wikipedia.org/wiki/Suurten_lukujen_nimet
    1000000: 'miljoona',
    1000000000: 'miljardi',
    1000000000000: 'biljoona',
    1000000000000000: 'triljoona'
}

def number_to_word(n, space=False):
    """
    Convert a number into its Finnish textual representation.
    See for format recommendations:
    - https://www.kielikello.fi/-/luvut-ja-tekstin-hahmotettavuus
    - http://users.jyu.fi/~pamakine/kieli/suomi/numeraalit/numerot.html

    Parameters:
    - n (int): The number to convert. Must be a positive integer less than 10^18.
    - space (bool): If True, add a space between words. Default is False.

    Returns:
    - str: The textual representation of the number in Finnish.
    """

    # Check that the given number is a positive integer less than quintillion.
    if not isinstance(n, int) or n < 0 or n >= 1000000000000000000:
        raise ValueError("Number must be a positive integer less than 10^18.")

    # Handle zero
    if n == 0:
        return "nolla"

    # Main recursive function
    def _number_to_word(n):
        # "Zero" does not appear in number words.
        # Numbers from 1 to 9 are base for all numbers in the finnish base 10 number systems.
        if n < 11:
            return one_to_ten[n]
        # Numbers up to nineteen have special words.
        elif n < 20:
            return one_to_ten[n-10] + "toista"
        # Optimize for the easy cases between twenty and ninety-nine.
        elif n < 100:
            return one_to_ten[n // 10] + "kymmentä" + (one_to_ten[n % 10] if n % 10 != 0 else "")
        else:
            # Determine the maximum power of ten for which the number qualifies.
            max_power = max(power for power in powers_of_ten if power <= n)

            # First power numbers don't need repetition e.g., "sata, tuhat, miljoona..."
            if n // max_power == 1:
                # No spaces.
                return (powers_of_ten[max_power] + _number_to_word(n % max_power)).strip()

            prefix = _number_to_word(n // max_power)
            next_number = _number_to_word(n % max_power)
            # Special case: "tuhat" becomes "tuhatta"
            if max_power == 1000:
                separator = " " if space else ""
                affix = "ta"
            # Suffix "-a" is added to numbers like "sata" -> "sataa", "miljoona" -> "miljoonaa",...
            else:
                # Add a space after every power of a thousand.
                separator = " " if space and (max_power % 1000) == 0 else ""
                affix = "a"
                # one more special case for plain millions, billions etc.
                # "viisi miljoonaa" and "viisimiljoonaa viisi" are preferred formats
                if space and next_number == "" and n > 999999:
                    prefix += " "
            return (prefix + powers_of_ten[max_power] + affix + separator + next_number).strip()

    return _number_to_word(n)
