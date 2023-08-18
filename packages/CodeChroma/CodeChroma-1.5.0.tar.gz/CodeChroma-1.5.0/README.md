<h1 align="center">CodeChroma</h1>

<p align="center" >
<img src="https://img.shields.io/github/last-commit/EddyBel/CodeChroma?color=%23AED6F1&style=for-the-badge" />
<img src="https://img.shields.io/github/license/EddyBel/CodeChroma?color=%23EAECEE&style=for-the-badge" />
<img src="https://img.shields.io/github/languages/top/EddyBel/CodeChroma?color=%23F9E79F&style=for-the-badge" />
<img src="https://img.shields.io/github/languages/count/EddyBel/CodeChroma?color=%23ABEBC6&style=for-the-badge" />
<img src="https://img.shields.io/github/languages/code-size/EddyBel/CodeChroma?color=%23F1948A&style=for-the-badge" />
</p>

<p align="center">Simple python text coloring package</p>

<p aling="center" >
<img src="./assets/Preview_1.png" width="100%" />
<img src="./assets/Preview_2.png" width="100%" />
<img src="./assets/Preview_3.png" width="100%" />
</p>

The "CodeChroma" project is a Python library for highlighting and coloring text in the terminal. With this library, users can highlight code syntax and color specific markdown elements, such as titles, links, parentheses and text in quotation marks.

## Why the project?

The project was created with the aim of improving the readability and aesthetics of text in projects using the terminal. On many occasions, text in the terminal can be difficult to read due to its flat, uncolored format, which can make work difficult and decrease efficiency. For this reason, a Python library was developed to allow text highlighting and coloring in a simple and easy to implement way.

The library allows users to highlight code syntax and color specific markdown elements, such as titles, links, parentheses and text in quotation marks, which improves the readability of the text and makes it easier to understand. In addition, this library is easy to implement in any project as it can be used with a simple library method, making the integration process quick and easy.

## Requirements

- [x] [Python>=3.7](https://www.python.org/downloads/)
- [x] [Virtualenv](https://virtualenv.pypa.io/en/latest/)

## Features

- [x] Allows to identify the code passed as a string and return the text with the syntax of the language colored.
- [x] Allows you to color key elements of the markdown syntax such as code, titles, links, etc.
- [x] Allows quick and easy implementation of the colors to be used.

## How to use

The library is simple to use and only requires installation and import.

```bash
pip install CodeChroma
```

The library allows you to color the text using only one method of the library for ease of use.

```python
from CodeChroma import TerminalColors

# We create an instance of the library
termcolor = TerminalColors()

#  Sample text for coloring
text = \
"""
# Sintaxis de Java

## Variables

En Java, existen diferentes tipos de variables, como enteros, flotantes, caracteres y booleanos.
Además de variables de tipo objeto como String o Arrays. Es importante declarar el tipo de
variable correcto para evitar errores en tiempo de ejecución. Por ejemplo, si quieres
almacenar un valor numérico entero, se debe utilizar "int" como el tipo de dato.

'''java
int numeroEntero = 10;
float decimal = 3.14f;
char letra = 'A';
boolean verdaderoOFalso = true;
'''
"""

# We color the text with its method "colorize_text", the text passed by parameter
# The function returns a new string with the text already colored.
colored_text = termcolor.colorize_text(text)
# We can display the new text
print(colored_text)
```

## Configuration

The library allows for a few extra settings, which allow the user to modify and color their text as needed.

### Colors

The colors can be easily modified from the parameters assigned when creating the instance of the TerminalColors class, you can write the available color you need for each colorable element.

```python
termcolor = TerminalColors(title="yellow", list_item="magenta", ...)
```

Another way to modify the colors of each element is from its elements attribute, for this it is necessary to pass some method either own of the library or personal (But it must be a method), that allows to color the text and to return the colored text.

```python
colors = Colors()
termcolor = TerminalColors(title="yellow", list_item="magenta")
termcolor.elements = {
        "title": colors.bg_cyan,
        "block": colors.yellow,
        "list-item": colors.magenta,
        "url": colors.cyan,
        "parentheses": colors.light_red,
        "string": colors.light_green,
        "code": colors.yellow,
        "lang": colors.red
      }
```

### Format

The TerminalColors class has some properties that modify how the string resulting from the coloring is displayed.

One of them is the programming language, with the view_lang property (boolean value, by default it is set to True) allows to modify if the identified language will be shown or not.

```python
termcolor.view_lang = False
```

The following format_code modifies whether the code is returned with or without the markdown code block characters "````", by default it is set to True.

```python
termcolor.format_code = False
```

## Methods

The TerminalColors class has some coloring methods as needed.

| FUNCTION             | PARAMS   | DESCRIPTION                                                                                                                                                 |
| -------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| coloring_text        | text:str | This function receives a text as a parameter and allows coloring the string with markdown formatting and features.                                          |
| color_code           | code:str | This function allows you to pass a code as a string, the function will identify the language and color it according to its syntax if it finds the language. |
| detect_code_language | code:str | This function also allows you to receive a code as a string and it will return a string with the language you identified in the code.                       |

## Licence

<h3 align="center">MIT</h3>

---

<p align="center">
  <a href="https://github.com/EddyBel" target="_blank">
    <img alt="Github" src="https://img.shields.io/badge/GitHub-%2312100E.svg?&style=for-the-badge&logo=Github&logoColor=white" />
  </a> 
  <a href="https://www.linkedin.com/in/eduardo-rangel-eddybel/" target="_blank">
    <img alt="LinkedIn" src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" />
  </a> 
</p>
