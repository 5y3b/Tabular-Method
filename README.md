# Tabular Method for Boolean Function Minimization

This project implements the **Tabular Method** for finding the **Minimal Sum of Products (MSOP)** of a Boolean function. The method is used to identify **Prime Implicants** and **Essential Prime Implicants** for simplification.

## 📂 Files

- `main.py` - The main entry point of the program.
- `utils/funcs.py` - Contains all functions used in the Tabular Method.

## 🚀 Installation & Usage

### Clone the Repository

```sh
git clone https://github.com/5y3b/Tabular-Method.git
cd Tabular-Method
```

### Run the Program

```sh
python main.py
```

The program will prompt you to enter minterms and don't-care terms for simplification.

---

## 🔧 Functions Overview

### `validate(minterms: list[str]) -> list[int]`

Validates and filters minterms, ensuring they are unique non-negative integers.

### `parse_minterms() -> list[int]`

Prompts the user to input minterms and returns them as a list of integers.

### `parse_dont_cares() -> list[int]`

Prompts the user to input don't-care terms and returns them as a list of integers.

### `first_grouping(minterms: list[int]) -> dict[int, list[str]]`

Groups minterms by the number of 1s in their binary representation.

### `second_grouping(terms: dict[int, list[str]]) -> dict[int, list[str]]`

Combines terms that differ by a single bit.

### `combine_two_terms(term1: str, term2: str) -> str | None`

Combines two binary terms if they differ by one bit.

### `find_prime_implicants(minterms: list[int]) -> set[str]`

Finds Prime Implicants by iteratively combining terms.

### `find_essential_prime_implicants(minterms: list[int], prime_implicants: set[str], dont_care: list[int]=[]) -> set[str]`

Identifies Essential Prime Implicants from the Prime Implicant Chart.

### `get_minterms_from_implicant(implicant: str) -> set[int]`

Generates all possible minterms covered by a prime implicant.

### `get_in_alphabet(essential_prime_implicants: list[str]) -> str`

Converts essential prime implicants to a human-readable format.

### `tabular_method() -> str`

Implements the **Tabular Method** and returns the minimized Boolean function.

---

## 📜 License

This project is licensed under the **MIT License**.

---

### ⭐ Contributions & Support

Feel free to fork the project, submit issues, or contribute via pull requests!

Enjoy simplifying Boolean functions! 🎯

