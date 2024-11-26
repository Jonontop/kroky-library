# Kroky Library

## Overview

The Kroky Library is a Python package designed to [provide a brief description of what your library does]. This documentation provides an overview of the library's functionality, installation instructions, and usage examples.

## Installation

To install the Kroky Library, use pip:

```bash
pip install kroky-library
```

## Usage


### Initialize kroky
```python
from kroky import Kroky

# Describe what this example does
login = Kroky(username:str, password:str)
```

### Get meals
```py
    print(login.get_menu(pos))
```

### Select meal
```py
    print(login.select_meal(date, id))
```
## Functions

### `get_menu(pos)`

- **Description**: [Displays all meals in selected week]
- **Parameters**:
    - `pos` (int): [pos is week defining -1 is last week, 0 is current week, 1 is next week]
- **Returns**: [return json]

### `select_meal(date, id)`

- **Description**: [Can select specific meal on specific day]
- **Parameters**:
    - `date` (str): [date needs to be entered in this form YYYY-MM-DD]
    - `date` (int): [id can be get from html on kroky website (alternative will be added shortly)]
- **Returns**: [Returns if meal was selected seccessfuly or not]

## Contributing

If you would like to contribute to the Kroky Library, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/Jonontop/kroky-library).
