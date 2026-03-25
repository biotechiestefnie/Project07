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


                    |                    |                     |                    |
EXAMPLE!!   |---------|                    
C A T $     | $ C A T |            0 0 0 T      0 0 0 $    0 0 T $     0 0 $ C    0 T $ C
A T $ C ->  | A T $ C | BWT = TC$A 0 0 0 C  ->  0 0 0 A -> 0 0 C A  -> 0 0 A T -> 0 C A T 
T $ C A sort| C A T $ |            0 0 0 $ sort 0 0 0 C    0 0 $ C     0 0 C A    0 $ C A
$ C A T     | T $ C A |            0 0 0 A      0 0 0 T    0 0 A T     0 0 T $    0 A T $              | original|            prepend        sort     prepend       sort     prepend
            | matrix  |
            |---------|                                         |
                                                                
                                reconstructed   $ C A T         T $ C A         0 $ C A
                                  matrix!!!     A T $ C         C A T $         0 A T $
                                        ->      C A T $         $ C A T         0 C A T
                                                T $ C A         A T $ C         0 T $ C                                                     sort           prepend          sort


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

0 A T G C $               4 $ A T G C
1 T G C $ A               0 A T G C $
2 G C $ A T.              3 C $ A T G
3 C $ A T G               2 G C $ A T
4 $ A T G C               1 T G C $ A
[4, 0, 3, 2, 1]

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
Function: Finc Match
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




Successes: the outside resource for inversion
Struggles: 
<img width="520" height="650" alt="image" src="https://github.com/user-attachments/assets/c199b1cc-44db-4be9-ba3f-833073014c43" />

```

## Successes
Our team worked well together and shared ideas and resources that we found exceedingly helpful for learning how to implement the Burrows-Wheeler Transform. Specifically, on Tuesday, March 17th, after class, I (Stefanie) began researching the algorithm and identified a resource that I shared with my team, in addition to several teammates I had worked with on previous projects.The resource was an interactive tutorial by Robert Aboukhalil, co-creator of Sandbox-bio, an renouned educational platform for bioinformatics. This tutorial walks the reader through each step of the BWT algorithm and includes a greatly simplified approach to BWT inversion, which we demonstrated in our example in the introduction of this README document. 

## Struggles
I was going to add a sentence or two Our team did a great job conceptualizing BWT but it was not without its struggles. As we all had strengths and weaknesses with the algorithm, being able to articulate our understanding was a skill we had to develop as we are rarely put into the teacher role.

As for implementation, although our team implemented the `encoding` and `decoding` functions, we did not actually use it in our FM search so our `find_match` although functional is not leveraging compression and decompression. This was more of an oversight on our behalf, as we were focused on implementing the function's concept. In future edits, our goal would be to include those two functions to showcase the power of BWT.

# Personal Reflections
## Group Leader
Group leader's reflection on the project

## Other members
Marcos: Working with Stefanie and Chantera has been really productive. Although I initially felt pretty confident about the algorithm, as I had been able to follow it pretty well in class, we met multiple times throughout the week, focusing mostly on the conceptual component. These sessions, where we all talked about the algorithm and how to implement it, were very beneficial, as they allowed me to get an even better grasp of how it worked, and let me realize what parts I was not so comfortable with. Stefanie even provided an additional resource that visually explained in a very intuitive way how to reconstruct the rotations matrix from the BWT in order to get the original string, which helped me even more. We all complemented and helped each other throughout the project, which made it a very good experience. We didn't run into too many issues during the implementation, aside from making sure we were working with the correct indices during the pattern matching step. I'm happy with how the group worked together and how we achieved our final implementation!

 Chantera: I am grateful to my team for the spending time conceptualizing BWT.  Marcos was able to walk us through some of the functions while Stephanie also provided us with a great interactive [reference](https://sandbox.bio/concepts/bwt) that helped us to internalize the algorithm. Writing down the pseudocode during our lessons last week also was beneficial.
 
As a visual learner, the cyclic nature of the algorithm made it easer to internalize. Yet I am still working through understanding `update_range` as I am not certain why we updated the lower and upper ranges as we do. I also think although I understand the algorithm I would need to spend more time on the practical application of the algorithm in bioinformatics.

# Generative AI Appendix
Not used for this assignment

# References
Aboukhalil, R. (2025, Oct 9). The Burrows-Wheeler transform. *Sandbox.bio. Retrieved on Mar 18, 2026, from https://sandbox.bio/concepts/bwt

Holt, J. & McMillan, L. (2014). Merging of multi-string BWTs with applications. *Bioinformatics*, 30(24): 3524-3531. https://doi.org/10.1093/bioinformatics/btu584

