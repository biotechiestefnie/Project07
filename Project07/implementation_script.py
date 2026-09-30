from collections import Counter
from typing import Dict, List, Tuple


def normalize_text(text: str) -> str:
    """
    Ensures consistent lexicographic behavior by converting
    string to uppercase and appending a unique sentinel character '$' if
    not already present
    Args:
        text (str): Input string to normalize
    Returns:
        Normalized string in uppercase ending with sentinel '$'
    """

    text = text.upper()  # Convert all chars to uppercase letters
    # Add sentinel if not included, skip code block if present
    if '$' not in text:
        text += '$'

    return text


def generate_rotations(text: str) -> list[str]:
    """
    For string of length n, function produces n rotations where each rotation
    shifts starting position by one character
    Args:
        text (str): Input string of length n, normalized to uppercase with sentinel '$'
    Returns:
        sorted_rotations (str): List of all cyclic rotations of input string sorted lecicographically
    """

    rotations = [text]  # Store original string as first rotation

    # Iterate over each rotation offset
    for i in range(len(text) - 1):
        # Slice and concatenate to rotate left by i+1 positions
        rotated = text[i + 1:] + text[:i + 1]
        # Append generated rotation to list
        rotations.append(rotated)

    # Sort the full list of rotations (must sort the LIST, not a single string)
    sorted_rotations = sorted(rotations)

    # Return the sorted list AFTER the loop completes
    return sorted_rotations


def extract_last_column(sorted_rotations: list[str]) -> str:
    """
    The Burrows–Wheeler Transform is defined as the sequence of last
    characters from each sorted rotation
    Parameter:
        sorted_rotations (list): Lexicographically sorted list of cyclic rotations.
    Returns:
        The Burrows–Wheeler Transform string
    """

    # Each rotation is same length, so last character is rotation[-1]
    return ''.join(rotation[-1] for rotation in sorted_rotations)


def BWT(string: str) -> str:
    """
    Compute the Burrows–Wheeler Transform (BWT) of a string
    This function orchestrates the four conceptual steps of BWT construction:
        1. Normalize input (uppercase + sentinel)
        2. Generate all cyclic rotations
        3. Sort rotations lexicographically
        4. Extract the last column of the sorted matrix
    Parameter:
        sequence(str): Input string to transform
    Returns:
        BWT (str): Burrows–Wheeler Transform of input sequence
    """

    # Apply helper function to normalize text string
    text = normalize_text(string)
    # Apply helper function to generate rotations of text
    sorted_rotations = generate_rotations(text)
    # Return BWT
    return extract_last_column(sorted_rotations)


def suffix_array(string: str) -> List[int]:
    """
    Compute the suffix array of a string.
    The suffix array is an array of starting positions of all suffixes of the
    input string, sorted in lexicographic order of suffixes. Sentinel '$' ensures
    proper ordering and uniqueness of suffixes.

    Parameter:
            string(str): Input string to compute suffix array
    Returns:
        sorted_positions (List- ints): Starting positions of all suffixes
        of string, sorted lexicographically by suffixes
    """
    # Append sentinel if not present, skip if present
    if '$' not in string:
        string += '$'

    # Initialize list for suffix rotations
    suffix_rotations: List[Tuple[int, str]] = []

    # For each possible starting position, record (index, suffix)
    for i in range(len(string)):
        rotated_string_suffix = string[i:]
        suffix_rotations.append((i, rotated_string_suffix))

    # Sort by suffix string
    sorted_rotations = sorted(suffix_rotations, key=lambda x: x[1])

    # Extract starting positions only
    sorted_positions: List[int] = [pos for pos, _ in sorted_rotations]

    return sorted_positions


def BWT_from_suffix_array(text: str, suffix_positions: List[int]) -> str:
    """
    Given a text with sentinel in last position and suffix array, constructs BWT by
    taking for each suffix the character immediately preceding that suffix in
    original text
    Args:
        text (str): Input string with sentinel character immediately preceding
        suffix_positions (list): suffix array of the text, i.e., a list of starting indices of
            all suffixes in lexicographic order.
    Returns:
        BWT (str): Burrows–Wheeler Transform of the input text
    """

    n = len(text)  # Determine length of string
    bwt_chars: List[str] = []  # Initialize empty list for suffix array

    for pos in suffix_positions:
        # If suffix starts at index 0, wrap around and take last character
        if pos == 0:
            bwt_chars.append(text[-1])
        else:
            # Otherwise, take the character immediately preceding the suffix
            bwt_chars.append(text[pos - 1])

    return ''.join(bwt_chars)


def cal_count(string: str) -> Dict[str, int]:
    """
    For each character in alphabet of input string, calculates how many characters
    in string are lexicographically smaller. Standard C-array used in FM-index backward search
    Parameter:
        BWT (str): input used to compute cumulative counts
    Returns:
        count_array (dict): maps each character to number of chars in string  lexicographically
        smaller than that char
    """

    # Count occurrences of each char
    char_counts = Counter(string)

    # Sort characters lexicographically
    sorted_char_counts = dict(sorted(char_counts.items(), key=lambda x: x[0]))

    count_array: Dict[str, int] = {}
    cumulative_count = 0

    # For each character in sorted order, store cumulative count of smaller chars
    for char in sorted_char_counts.keys():
        count_array[char] = cumulative_count
        cumulative_count += char_counts[char]

    return count_array


def cal_occur(bwt_string: str) -> Dict[str, List[int]]:
    """
    Builds occurrence table used in FM-index backward search. For
    each char in alphabet of BWT string, returns a list where
    the i-th entry is number of times char appears in BWT
    up to and including position i.
    Parameter::
        bwt_string (str): Burrows–Wheeler transformed string with sentinel char
    Returns:
        occur (dict): dictionary mapping each char to list of integers. For given
        char c, occur[c][i] is number of occurrences of c in bwt_string[0:i+1].
    """

    # Extract alphabet from BWT string (unique characters only)
    alphabet = sorted(set(bwt_string))

    # Initialize occurrence table: each char maps to list of zeros
    occur: Dict[str, List[int]] = {
        char: [0] * len(bwt_string) for char in alphabet
    }

    # Iterate through each position in BWT string
    for i, char in enumerate(bwt_string):
        # if index greater than 0 (not first char in string)
        if i > 0:
            # Copy previous counts into current position for all characters
            for c in alphabet:
                occur[c][i] = occur[c][i - 1]

        # Increment count for character at current position
        occur[char][i] += 1

    return occur


def update_range(
    lower: int,
    upper: int,
    count: Dict[str, int],
    occur: Dict[str, List[int]],
    a: str
) -> Tuple[int, int]:
    """
    During backward search in the FM-index, updates current
    [lower, upper] range in suffix array corresponding to pattern
    suffix processed so far, when a new character a is prepended.
    Notes: This function assumes that the character a is present in the count
           dictionary and that occur[a] is defined for all positions in the BWT.
    The update uses the standard FM-index formulas:
        lower = C[a] + Occ(a, lower - 1)
        upper = C[a] + Occ(a, upper) - 1
    with convention that Occ(a, -1) = 0, which is handled by a special
    case when lower == 0.
    Parameters:
        lower:
            Current lower boundary (inclusive) of suffix array range.
        upper:
            Current upper boundary (inclusive) of the suffix array range.
        count:
            C-array mapping each character to the number of characters
            lexicographically smaller than it in the BWT.
        occur:
            Occurrence table mapping each character to a list of cumulative
            occurrence counts at each position in the BWT.
        a:
            The character being processed in the pattern (moving right to left).
    Returns:
        lower_new, upper_new (tuple): updated range
    """
    # Handle Occurrence (a, lower - 1) with boundary condition at lower == 0
    if lower == 0:
        lower_new = count[a]
    else:
        lower_new = count[a] + occur[a][lower - 1]

    # Upper bound uses Occ(a, upper) directly
    upper_new = count[a] + occur[a][upper] - 1

    return lower_new, upper_new


def find_match(query: str, reference: str) -> List[int]:
    """
    Builds an FM-index implicitly from reference string by computing
    its suffix array and BWT, then performs backward search to find
    all occurrences of the query. It returns the starting positions (0-based)
    of all exact matches of the query in the reference.
    Parameters::
        query (str): Pattern string to search for
        reference (str): Text string to search within with sentinel char at end
    Returns:
        A sorted list of 0-based starting positions of all occurrences of the
        query in the reference. If no matches are found, an empty list is
        returned.
    """

    # Ensure reference has a sentinel marker
    if '$' not in reference:
        reference = reference + '$'

    # Build suffix array and BWT
    suffix_pos = suffix_array(reference)
    bwt = BWT_from_suffix_array(reference, suffix_pos)

    # Initialize search range over the entire BWT
    lower = 0
    upper = len(bwt) - 1

    # Precompute C-array and Occ table
    count = cal_count(bwt)
    occur = cal_occur(bwt)

    # Process query characters from right to left (backward search)
    for char in reversed(query):
        # If character not in alphabet, no matches are possible
        if char not in count:
            return []

        # Update the search range
        lower, upper = update_range(lower, upper, count, occur, char)

        # If the range becomes empty, there are no matches
        if lower > upper:
            return []

    # Collect all matching positions in the final range
    return sorted(suffix_pos[lower: upper + 1])


def run_length_encode(bwt_string: str) -> str:
    """
    Scans the input string from left to right, groups consecutive
    identical characters into runs, and returns an encoded string where each
    run is represented as the character followed by its count (in decimal).
    Parameter:
        bwt_string (str): Input string to encode, typically a BWT string but not
            restricted to that
    Returns:
        encoded_string(str): run-length encoded string of form 'a3n2b1$1a2', where each
        character is followed by length of its consecutive run.
    """

    # Handle empty input
    if not bwt_string:
        return ""

    encoded_string = ""

    # Initialize current run
    symbol = bwt_string[0]
    counter = 1

    # Iterate through the string starting from the second character
    for i in range(1, len(bwt_string)):
        if bwt_string[i] == symbol:
            # Extend current run
            counter += 1

        else:
            # Close current run and start a new one
            encoded_string += symbol + str(counter)
            symbol = bwt_string[i]
            counter = 1

    # Append the final run
    encoded_string += symbol + str(counter)

    return encoded_string


def run_length_decode(encoded: str) -> str:
    """
    Reconstructs original string by parsing an encoded
    representation where each run is stored as a character followed by its
    count (in decimal), and expanding each run back into repeated characters.
    Note:
        This implementation assumes that the encoding format is strictly
        alternating single characters and their counts, with counts written
        as one or more decimal digits (e.g., 'a12b3'). It parses digits
        following each character until a non-digit is encountered.
    Parameter::
        encoded (str): A run-length encoded string of the form 'a3n2b1$1a2', or more
            generally 'char + integer' repeated.
    Returns:
        decoded_string (str): The decoded string obtained by expanding all runs in the encoded input.
    """
    decoded_string = ""
    i = 0
    n = len(encoded)

    while i < n:
        # Current symbol
        symbol = encoded[i]
        i += 1

        # Parse one or more digits for the count
        count_str = ""
        while i < n and encoded[i].isdigit():
            count_str += encoded[i]
            i += 1

        # Convert count and expand run
        count = int(count_str)
        decoded_string += symbol * count

    return decoded_string


def inverse_BWT(bwt: str) -> str:
    """
    Reconstruct original string from its Burrows–Wheeler Transform.
    Standard LF-mapping reconstruction.

    Parameter:
        bwt (str): BWT string containing exactly one sentinel '$'
    Returns:
        original (str): Original string reconstructed from BWT
    """

    # Initialize table of empty strings
    table = [""] * len(bwt)

    # Repeat len(bwt) times to reconstruct full matrix
    for _ in range(len(bwt)):
        # Prepend BWT characters to each row
        table = sorted([bwt[i] + table[i] for i in range(len(bwt))])

    # Return the row ending with sentinel
    for row in table:
        if row.endswith("$"):
            return row


if __name__ == "__main__":
    # Test sequence
    seq = "AATACGACTTGAAGTAGA"

    print("Original sequence:")
    print(seq)

    # Compute BWT
    bwt_seq = BWT(seq)
    print("\nBWT of sequence:")
    print(bwt_seq)

    # Inverse BWT
    original_from_bwt = inverse_BWT(bwt_seq)
    print("\nReconstructed original from BWT:")
    print(original_from_bwt)

    # Run-length encode BWT
    rle = run_length_encode(bwt_seq)
    print("\nRun-length encoded BWT:")
    print(rle)

    # Decode RLE
    decoded_rle = run_length_decode(rle)
    print("\nDecoded run-length encoding:")
    print(decoded_rle)


