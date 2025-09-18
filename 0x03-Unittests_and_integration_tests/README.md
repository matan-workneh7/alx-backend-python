# Python - Unit Tests

## Project Overview

This project demonstrates how to write **unit tests** in Python using the `unittest` framework and the `parameterized` library.

The main focus is testing the `access_nested_map` function in `utils.py`, ensuring it correctly navigates nested dictionaries using a given path.

---

## Tools Used

- **unittest**  
    Python’s built-in testing framework

- **parameterized**  
    Run a single test with multiple input sets

---

## File Structure

- `utils.py`  
    Contains the `access_nested_map` function

- `test_utils.py`  
    Unit tests for `access_nested_map`

---

## Running the Tests

1. Navigate to the project root directory.
2. Run the following command:

     ```bash
     python3 -m unittest test_utils.py -v
     ```

     > The `-v` flag enables verbose output.

---

## Example Output

```
test_access_nested_map_0 (test_utils.TestAccessNestedMap) ... ok
test_access_nested_map_1 (test_utils.TestAccessNestedMap) ... ok
test_access_nested_map_2 (test_utils.TestAccessNestedMap) ... ok
test_access_nested_map_3 (test_utils.TestAccessNestedMap) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.002s

OK
```

---

## Notes

- Each test case checks a different nested path in a dictionary.
- Tests are **parameterized**: one test method runs with multiple input sets.
- This approach keeps tests **clean**, **readable**, and **efficient**.

---