from ordered_set import OrderedSet
from itertools import product

zf = None
"""zfill, the maximum number of bits in the highest number, also 
can be used to know how much vars exists in the highest number"""

combinable = {}
"""Stores the uncombinable terms to use later"""

def validate(minterms: list[str]) -> list[int]:
    """This validate function takes list of strings and validates each value
        if its an integar and that it is greater or equal to zero, and duplicates 
        is removed

        Args:
            minterms (list[str]): the list of strings in format: "`value_1 value_2 value_3 ...`"

        Returns:
            list[int]: no-duplicates list of integar values where (value>=0).
    """
    validated_minterms = set()
    for value in minterms:
        if value.isdecimal():
            validated_minterms.add(int(value))
        else:
            print(f"Incorrect value entered. ({value}) (value>=0)")
            exit(1)
    return list(validated_minterms)
    
def parse_minterms() -> list[int]:
    """asks the user for input of the minterms to be calculated later
        
        **format**: Space-separated integers as a single input string.
            "`value_1 value_2 value_3 ...`"
            
        returns them as a list of integars
    """
    minterms = input("Minterms (leave a space between each integar value, value>=0):\n").split()
    return validate(minterms)

def first_grouping(minterms: list[int]) -> dict[int, list[str]]:
    """Groups minterms by the number of 1s in their binary representation.
        
        This function converts each minterm into its binary form and counts how many 1s it contains.
        It then groups minterms with the same number of 1s together in a dictionary.

        Returns: A dictionary where:
        - The keys are the count of 1s in the binary representation.
        - The values are lists of binary strings that have that many 1s.

        Example:
            Input: [3, 5, 7, 1]
            Binary: ['11', '101', '111', '1']
            Output: {1: ['1'], 2: ['11', '101'], 3: ['111']}"""
    global zf
    step_1_result = {}
    if zf is None:
        zf = max(list(map(lambda value: len(bin(value)[2:]), minterms)))
    for minterm in minterms:
        binary = bin(minterm)[2:].zfill(zf)
        ones = binary.count('1')
        step_1_result.setdefault(ones, []).append(binary)
    return step_1_result
            
def second_grouping(terms: dict[int, list[str]]) -> dict[int, list[str]]:
    """Compares adjacent groups and combines terms that differ by one bit.
    
        args:
            terms (dict[int, list[str]]): Grouped minterms.
        
        returns:
            dict[int, list[str]]: Dictionary of combined terms.
    """
    global uncombinable
    result = {}
    keys = sorted(terms.keys())
    for i in range(len(keys) - 1):
        key, next_key = keys[i], keys[i+1]
        for term1 in terms[key]:
            for term2 in terms[next_key]:
                combined = combine_two_terms(term1, term2)
                if combined:
                    result.setdefault(key, []).append(combined)
                    combinable[term1] = True
                    combinable[term2] = True
                
    return result
    
    
def combine_two_terms(term1: str, term2: str) -> str | None:
    """Combines two binary terms if they are differing by one bit.
    
        args:
            term1 (str): First binary term.
            term2 (str): Second binary term.
        
        returns:
            str | None: The different bit will be replaced with '-' or returns None if no different bit is found or has 2 or more different bits (can't combine).
            
        info:
            This is used in step_2"""
    diff = [i for i in range(len(term1)) if term1[i] != term2[i]]
    if len(diff) == 1:
        return term1[:diff[0]] + '-' + term1[diff[0]+1:]
    return None

def find_prime_implicants(minterms: list[int]) -> set[str]:
    """Finds Prime Implicants by continuously combining terms until no more combinations are possible.
        
        args:
            minterms (list[int]): List of minterms.
        
        returns:
            set[str]: Set of Prime Implicants.
        """
    
    num_vars = zf
    groups = first_grouping(minterms)
    prime_implicants = OrderedSet()
    
    while groups:
        new_groups = second_grouping(groups)
        unused_terms = {term for group in groups.values() for term in group} - {term for group in new_groups.values() for term in group}
        # adds all terms to prime_implicants to later choose the best
        prime_implicants.update(unused_terms)
        groups = new_groups
    return prime_implicants
    
def find_essential_prime_implicants(minterms: list[int], prime_implicants: set[str]) -> set[str]:
    """Finds Essential Prime Implicants from the Prime Implicant Chart.
    
    Args:
        minterms (list[int]): List of minterms.
        prime_implicants (set[str]): Set of Prime Implicants.
    
    Returns:
        set[str]: Set of Essential Prime Implicants.
    """
    global combinable
    uncombineable = []
    for prime_implicant in prime_implicants:
        if not combinable.get(prime_implicant, False):
            uncombineable.append(prime_implicant)
    
    # table method , last step
    table = {minterm: [] for minterm in minterms}
    
    for implicant in uncombineable:
        covered_minterms = get_minterms_from_implicant(implicant)
        for minterm in covered_minterms:
            if minterm in table:
                table[minterm].append(implicant)
    
    essential_prime_implicants = set()
    for key, value in table.items():
        if len(value) == 1:
            essential_prime_implicants.add(value[0])
    
    return essential_prime_implicants
        
    

    



def get_minterms_from_implicant(implicant: str) -> set[int]:
    """Generates all possible minterms from a prime implicant by replacing '-' with 0 and 1.
    
    Args:
        implicant (str): A binary string with '-' as don't cares.
    
    Returns:
        set[int]: Set of integers representing the minterms covered by this implicant.
    """
    indices = [i for i, bit in enumerate(implicant) if bit == '-']  # Positions of '-'
    replacements = product('01', repeat=len(indices))  # All possible 0/1 replacements

    minterms = set()
    for replacement in replacements:
        implicant_list = list(implicant)
        for i, bit in zip(indices, replacement):
            implicant_list[i] = bit  # Replace '-' with 0 or 1
        minterms.add(int(''.join(implicant_list), 2))  # Convert to integer

    return minterms

def get_in_alphabet(essential_prime_implicants: list[str]) -> str:
    
    final = []
    for epi in essential_prime_implicants:
        current = ''
        for i in range(len(epi)):
            if epi[i] == '1':
                current += chr(ord('A') + i)
            elif epi[i] == '0':
                current += chr(ord('A') + i) + '`'
        final.append(current)
        
    return '+'.join(final)
                
    
                
    

def tabular_method() -> str:
    """The Tabular Method for finding the Minimal Sum of Products (MSOP) of a Boolean
        function. This method is used to find the Prime Implicants and Essential Prime
        Implicants of a Boolean function."""
    minterms = parse_minterms()
    pi = find_prime_implicants(minterms)
    epi = find_essential_prime_implicants(minterms, pi)
    alpha = get_in_alphabet(epi)
    return alpha
    