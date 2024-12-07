# Kroky Library

## Overview

The Kroky Library is a Python package designed to help you select meal true code for easier customization (auto meal selection) and auto login. This documentation provides an overview of the library's functionality, installation instructions, and usage examples.

## Installation

To install the Kroky Library, use pip:

```bash
pip install kroky
```

## Usage


### Initialize kroky
```python
from kroky import Kroky

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

### Get user data
```py
print(login.user_info()
```

### Change password
```py
print(login.change_password(password, password))
```

## Asinronus Usage
### Initialize kroky
```py
from kroky import KrokyAsync

async def main():
    async with KrokyAsync("USERNAME", "PASSWORD") as kroky:


asyncio.run(main())
```
### Get meal
```py
print(await kroky.get_menu(pos))
```

### Select meal
```py
print(await kroky.select_meal(date, id))
```

### Get user data
```py
print(await kroky.user_info())
```

### Change password
```py
print(await kroky.change_password("password", "password")
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
    - `id` (int): [id can be get from html on kroky website (alternative will be added shortly)]
- **Returns**: [Returns if meal was selected seccessfuly or not]

### `user_info()`

- **Description**: [can display user info]
- **Returns**: [Return user info]

### `change_password(password, password2)`

- **Description**: [can change user password]
- **Parameters**:
    - `password` (str): [new password]
    - `password2` (int): [retype new password]
- **Returns**: [Returns if it succided in changing the password]

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
