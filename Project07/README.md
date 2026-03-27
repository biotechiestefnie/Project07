# PROJECT 7: Burrows-Wheeler Transform Algorithm

## Introduction

The Burrows-Wheeler Transform (BWT) is a reversible, block sorting algorithm that rearranges a string into a more compressible format by grouping similar characters together. It is widely used in data compression tools and bioinformatics tools like bowtie or bwa. The BWT has two key properties:
- It suffles strings so that identical characters tend to group together
- The transform can be reversed to obtain the original string

The encoding steps to the algorithm are as follows:

1. Add sentinel- append a special end-of-string character that is lexicographically smaller than any other character in the string to be encoded. Most frequently (and in this project), "$" is used. The sentinel is required to make the BWT reversible.
2. Generate rotations- create all cyclic permutations of the string. This will create a matrix in which all rows and columns contain every character of the original string.
3. Sort rows- sort the rotated strings lexicographically.
4. Extract final column: the BWT output is the last column of this sorted matrix. This string can be compressed using run-length encoding, and contains all the information needed to decipher the original string.

The decoding steps to the algorithm are as follows:

1. Starting with an empty matrix, prepend the BWT string to the final column.
2. Sort the row lexicographically- this yields the first column of the expected matrix.
3. Prepend BWT to the next column.
4. Sort the rows lexicographically.
5. And on, and on, until you have no columns left to fill!


BWT encoding can be used in bioinformatics to efficiently compress and index large genomic sequences, permitting rapid DNA sequence alignment. By transforming DNA sequences into a format that groups similar characters, it creates compact representations that allow fast searching for reads within massive datasets with low memory usage.

Furthermore, BWT is used to build an FM Index, which acts like a compressed full-text index allowing for rapid searching of specific genetic patterns, substrings, or motifs within sequences (Holt & McMillan, 2014). It is also used for analyzing pangenomes and detecting rare genomic rearrangements, especially in oncology studies, by handling repetitive sequences- a hallmark of human genomes and cancer genomes- efficiently.


## Pseudocode                                           

```
Fuction: BWT(string: str):
append dollar sign to end of string
determine string length -> depending on length, either initialize list or array if prohibitively long for all poss rotations
append string initially to ensure starting at first letter
append(string)
for len(string – 1):
	append(string[i + 1:] + string [:I + 1])
  sorted(list)
  initialize empty string for BWT
  go through each string in list and append last value to BWT

END FUNCTION
```

```
Function: suffix_array(strinf:str) -> list[int]:
Create a list of all suffixes of the text, each paired with starting position
for i in range(len(string-1):
	append[i, (string[i:]
  sorted(suffix_list, key=lambda x:x[1])
  return(sorted_suffix_list[0])
```

```
Function: BWT_from_suffix_array(text, suffix_postions)

initialize BWT_from_suffix string of len(input_string)
for each i in suffix positions
	if suffix at i = 0
		add input_string [-1] to BWT_from_suffix string
	else:
		add input_string[i-1] to BWT_from_suffix string
  return BWT_from_suffix
END FUNCTION
```

```
Function: run_length_encode(bwt_from_suffix: str):
    encoded_text = ""

    if BWT_string empty:
        return encoded_text
        symbol = BWT_string[0]
        counter = 1

    for I in range(len(BWT_string):
	      if BWT_string[i] == symbol
		    counter +=1

    else:
		    encoded_text+= symbol + counter
		    symbol = BWT_string[i]

        counter = 1
 
 return encoded_text 
END FUNCTION
```

```
Function: decode_run_length_encode():
    decoded_text = ""

    for i in range(len(encoded_text: 2)):
		    symbol = encoded_text[i]
		    count = encoded_text[i+1]
		    decoded_text += symbol*int(count)

	      return decoded_txt
END FUNCTION
```

PATTERN MATCHING/FM INDEX
Function: count array
```
def cal_count(string: str) ->[str, int]
    # initialize dictionary to track char counts
    # char = key, count = value
    banana = string  

    cal_counts =  Counter(string)
    sorted({"b": 1, "a": 3, "n": 2})
    {"a": 3, "b":1, "n": 2})

    B A N A N A 

   cal_counts = A: 3 B:1 N: 2
   Score = 0 
   Count_array = {}
   For char in tracker.keys():
      Count_array[char] = score # A: 0
      Score += cal_counts[char] 

   Score = 4 char = N
   Count_array { A:0, B:3, N:4}
   Score =  3+1
END FUNCTION
```
Function- Occurrence Array: 
```
def cal_occur(BWT_string: str) -> dict[str:list[int]]
   N = length(BWT)
   # Iterate through each unique symbol in input string and initialize dictionary
   For symbol/symbol in BWT string.unique():
      Cal_occur[symbol] =  [0] * N  # {symbol1: [0, 0, 0], symbol2: [0,0,0]

   # Iterate through each position in BWT_string
   For i in len(BWT_string):
      # Identify character at the current position
      Current_char = BWT_string[i]

   # For each character in alphabet update new value at position i
   For char in BWT_string.unique():
       cal_occur[char][i] = cal_occur[char][i-1]
       # Update count for the current character
       Cal_occur[current_char][i] += 1

   Return cal_occur
END OF FUNCTION
```

Function: Update Range
```
def update_range(
    lower: int,
    upper: int,
    count: dict[str,int],
    occur: dict[str, list[int]],
a: str) -> tuple[int, int]:
Function to update range given character a
Updates search range during backward search in BWT pattern match algorithm when processing char a
    Calculate new start position using char count and occurrence at range start
    calculate new end position using char count and occurrences at range end

    return new start and end position
END FUNCTION
```
Function: Find Match
```
Find_match(pattern, transformed, counts, occurrences, suffix_positions) list[int]:
Function to find exact matching by applying burrows wheeler transform
    # Apply BWT
    Suffix_array = suffix_array(reference)
    Bwt = bwt_from_suffix_array(reference, suffix_array)
    # Initialize lower and upper bounds
    Lower = 0
    Upper = len(bwt)
    # Create count and occur dicts
    count= cal_count()
    Occur = cal_occur()
    # Initialize indices list
    Indices = []

    # For each char in the pattern processing right to left update range
    For char in reverse(query):
        # If range is empty return empty list
        If lower > upper: break
            # Update range
            Lower, upper = update_range(lower, upper, count, occur, char)

        # Note index if lower and upper are the same
        If lower == upper:
           Indices.append(lower)
           # Collect all suffix positions within the final range
           Match = reference[lower:upper]  # this might be upper +1 (not sure rn)

    Return match


END OF FUNCTION
```
Function: Run length Encode
```
def run_length_encode(bwt_string: str) -> str:
    # Initialize encoded text string 
    # Check if input string is empty and return empty 
    # Initialize symbol and counter variables 
    # Iterate through each character in the string 
            # If next character is the same as the last current symbol add 1 to the counter 
            # If the next character is different add symbol and counter to encoded string 
    # Add last symbol after loop and return string 

END OF FUNCTION
```
Function: Decode Run Length Encode
```
def run_length_decode(encoded: str) -> str:
# Initialize decoded string 
# Iterate through each symbol, counter pair in string 
         # Extract number of times to repeat each symbol 
# Return decoded_string 

END OF FUNCTION
```
MISSING:
```
Function: BWT inversion
```
MISSING:
```
driver code for implementation
```

## Successes
Our team worked well together and shared ideas and resources that we found exceedingly helpful fo rlearning how ot implement the Burrows-Wheeler Transform. Specifically, on Tuesday, March 17th, after class, I (Stefanie) began researching the algorithm and identified a resource that I shared with my team, in addition to several teammates I had worked with on previous projects.The resource was an interactive tutorial by Robert Aboukhalil, co-creator of Sandbox-bio, an renouned educational platform for bioinformatics. This tutorial walks the reader through each step of the BWT algorithm and includes a greatly simplified approach to BWT inversion, which we demonstrated in our example in the introduction of this README document. 

## Struggles
We struggled initially with understanding the inversion process of the BWT and how to implement that in code. Upon discovering Dr. Aboukhalil's (2025) interactive tutorial, "The Burrows-Wheeler Transform", however, we learned a much easier way to recreate the original matrix so we could recover the initial string. Even so, upon reviewing our final code, we realized we had not implemented the BWT inversion, which we needed to recover our initial sequence. This was implemented at the 12th hour, and so the pseudocode is missing for this, but will be included very shortly. 

We also struggled with implementing our functions as separate code blocks in a Jupyter notebook, because this caused issues for us when it came to ensuring each function was compatible with the others and the whole program would run as one unit. Consequently, we created a python file and implemented all functions as one script, then executed to ensure it ran, and also ran test cases from this file. This python implementation file is included in our project directory. This may seem trivial to many people, but having a single script to run makes it much easier to ensure cohesion throughout the code in terms of  parameters and returns, dependencies, and also debugging for me (Stefanie), as I do not come from a strong coding background, but rather, from a Molecular Biology background. Nevertheless, we were ultimately able to identify problems with the cell-by-cell implementation in Jupyter Notebook, and we corrected these to ensure proper execution. Finally, we replaced the functions within each cell of the Jupyter Notebook with the corrected versions of each function.

# Personal Reflections
## Group Leader- Stefanie Moreno
Working as the team lead on this Burrows–Wheeler Transform project pushed me to balance conceptual clarity with practical implementation, and that tension ended up being one of the most rewarding parts of the assignment. Being completely unfamiliar with this algorithm, I conducted extensive research to augment my understanding from the lecture, and I found several excellent resources that I shared with my teammates and many of my prior teammates. What surprised me was how much discipline it took to turn that understanding into clean, modular, reproducible code—especially for something as deceptively compact as the BWT pipeline.

One of the biggest challenges was keeping the implementation aligned with first‑principles thinking. It’s easy to write a function that “just works,” but much harder to break eadch function down into single actions that reflect the logical structure of the algorithm. Leading the team through that process, from sequence normalization, rotation generation, lexicographic sorting, last‑column extraction, suffix array construction, FM‑index range updates, run length encoding and decoding, and BWT inversion to recover the original sequenceforced all of us to slow down and articulate why each step exists. That ended up being a major success: our final code isn’t just functional, it’s readable and defensible.

I am also proud of how we handled debugging and cross‑checking. There were several moments where our expectations didn’t match the output, and instead of patching symptoms, we traced the logic back to the exact conceptual step that needed correction. That kind of collaborative troubleshooting is exactly what I strive to enable in a team environment. By the end, we had a pipeline that not only performs the BWT, FM‑index search, and run‑length encoding/decoding correctly, but also reflects a shared understanding of why each component works.

Overall, leading this project reinforced how important it is to write code that teaches as much as it executes. The final script is something I feel confident handing off to anyone learning these algorithms for the first time, and that’s the standard I aim for when I am guiding a team.

## Other members
Marcos: Working with Stefanie and Chantera has been really productive. Although I initially felt pretty confident about the algorithm, as I had been able to follow it pretty well in class, we met multiple times throughout the week, focusing mostly on the conceptual component. These sessions, where we all talked about the algorithm and how to implement it, were very beneficial, as they allowed me to get an even better grasp of how it worked, and let me realize what parts I was not so comfortable with. Stefanie even provided an additional resource that visually explained in a very intuitive way how to reconstruct the rotations matrix from the BWT in order to get the original string, which helped me even more. We all complemented and helped each other throughout the project, which made it a very good experience. We didn't run into too many issues during the implementation, aside from making sure we were working with the correct indices during the pattern matching step. I'm happy with how the group worked together and how we achieved our final implementation!

 Chantera: I am grateful to my team for the spending time conceptualizing BWT.  Marcos was able to walk us through some of the functions while Stephanie also provided us with a great interactive [reference](https://sandbox.bio/concepts/bwt) that helped us to internalize the algorithm. Writing down the pseudocode during our lessons last week also was beneficial.
 
As a visual learner, the cyclic nature of the algorithm made it easer to internalize. Yet I am still working through understanding `update_range` as I am not certain why we updated the lower and upper ranges as we do. I also think although I understand the algorithm I would need to spend more time on the practical application of the algorithm in bioinformatics.

# Generative AI Appendix
Not used for this assignment

# References
Aboukhalil, R. (2025, Oct 9). The Burrows-Wheeler transform. *Sandbox.bio. Retrieved on Mar 18, 2026, from https://sandbox.bio/concepts/bwt

CMU School of Computer Science. (2018, Nov 29). Design & analysis of algorithms: Burrows-Wheeler Transform. *Lecture #25*, p.1-8. https://www.cs.cmu.edu/~15451-f18/lectures/lec25-bwt.pdf

Holt, J. & McMillan, L. (2014). Merging of multi-string BWTs with applications. *Bioinformatics*, 30(24): 3524-3531. https://doi.org/10.1093/bioinformatics/btu584

