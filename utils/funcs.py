
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

def step_1(minterms: list[int]) -> dict[int, list[str]]:
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
    step_1_result = {}
    zf = max(list(map(lambda value: len(bin(value)[2:]), minterms)))
    for minterm in minterms:
        binary = bin(minterm)[2:].zfill(zf)
        ones = binary.count('1')
        step_1_result.setdefault(ones, []).append(binary)
    return step_1_result
            
def step_2(step_1_result: dict[int, list[str]]) -> dict[int, list[str]]:
    """Compares adjacent groups and combines terms that differ by one bit.
    
        Args:
            step_1_result (dict[int, list[str]]): Grouped minterms from step 1.
        
        Returns:
            dict[int, list[str]]: Dictionary of combined terms.
    """
    step_2_result = {}
    keys = sorted(step_1_result.keys())
    for i in range(len(keys) - 1):
        key, next_key = keys[i], keys[i+1]
        for term1 in step_1_result[key]:
            for term2 in step_1_result[next_key]:
                combined = combine_terms(term1, term2)
                if combined:
                    step_2_result.setdefault(key, []).append(combined)
    return step_2_result
    
    
def combine_terms(term1: str, term2: str) -> str | None:
    """Combines two binary terms if they are differing by one bit.
    
    Args:
        term1 (str): First binary term.
        term2 (str): Second binary term.
    
    Returns:
        str | None: The different bit will be replaced with '-' or returns None if no different bit is found or has 2 or more different bits (can't combine).
    """
    # print(term1)
    # print(term2)
    diff = [i for i in range(len(term1)) if term1[i] != term2[i]]
    if len(diff) == 1:
        return term1[:diff[0]] + '-' + term1[diff[0]+1:]
    return None