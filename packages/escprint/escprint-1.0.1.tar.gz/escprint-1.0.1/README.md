# escprint
Library for formatting and styling terminal outputs via ANSI escape sequences. 

## Installation
```bash
pip install escprint
```

## Usage 
```python
from escprint import esc
```

### esc.print
This is useful for a basic print statement. The first argument is the string to print, while the rest are styles/colors to format the string with. 

****Note that all styles are cleared after the print statement is executed***

All of the keyword arguments valid for python's **print** function are valid, as well as several others, shown in examples below.

<a href="#string-table">A list of valid formatting strings can be found at the bottom of this document.</a>

```python
esc.print("Hello World!", "red","underline", end="")
```
Different Escape Arguments can be deliminated by a "/"
```python
esc.print("Hello World!", "red/underline", end="")
```
#### <div id="kwargs"></div>Keyword Args
| Keyword     | Description |
| ----------- | ----------- |
| bg   | sets background color, either color code (int) or R,G,B (tuple) |
| fg   | sets foreground color , either color code (int) or R,G,B (tuple) |
| prefix | sets prefix to prepend to string |
| precall | a function to call before print statement|
| postcall| a function to call after print statement |

To get more specific with color preferences, you can use the **fg** or **bg** keyword argument to plug in either a color code value ranging from 0 to 255, or an (R,G,B) tuple. **fg** sets the foreground color, while **bg** sets the background. 

<a href="#color-codes">These color codes can also be found at the bottom of this document.</a>
```python
esc.print("Print white color", fg=255)

esc.print("Print white color, with black background.", fg=(255,255,255), bg=(0,0,0))
```

Prefixes are also valid
```python
esc.print("World!", "red/underline", prefix="Hello ")
```
**precall** & **postcall** keyword arguments can be passed as well. These are functions that will be called before and after the print statement, respectively.
```python
esc.print("World", "red", precall=lambda:print("Hello"), postcall=lambda:print("!"))
``` 
<br/>

### esc.printf
Sometimes, we want different characters/words to have different styles. 
```python
esc.printf(
    "This is normal, ",
    ("but this is red and underlined, ", "red/underline"),
    ("and this is blue and italic", "blue/italic")
)
```
We can also set a default style as well, with the default keyword argument. 
```python
esc.printf(
    "This is red ",
    ("This is blue", "blue"),
    "This is still red",
    default="red"
)
```

All other <a href="#kwargs">keyword arguments</a> valid for **esc.print** are valid for this function as well.
```python
esc.printf(
    "These are separated by newlines",
    ["and this is red and underlined, ", "red/underline"],
    end="\n"
)
```
<br/>

### esc.create_fn
If we are constantly printing the same styles over and over, we might want to create a printing function to do it for us.
```python
print_yellow_italic = esc.create_fn("yellow","italic")

print_yellow_italic("This will be yellow and italic", end="")
```
Note that the <a href="#kwargs">keyword arguments</a> allowed for 
**esc.print** are valid when creating the function.
```python
print_yellow_italic = esc.create_fn("yellow","italic",precall=print("'Ello Govna"))
```
<br/>

### esc.input
We also might want to format our inputs as well.

Here, the prompt is "What is your name? ". The prompts style is set via the ***prompt*** keyword argument. The input style will be set via the ***input*** keyword argument. 
```python
user_input = esc.input(
    "What is your name? ", 
    prompt="yellow/italic", 
    input="red/underline", 
    end=""
)
```
<br/>

### esc.set
This is used to set the terminal outputs to a style indefinitely. 
```python
esc.set("cyan","underline","italic")
# OR
esc.set("cyan/underline/italic")
```
The keyword arguments ***bg***, ***fg***, are valid keywords as well.
```python
esc.set(fg=(122,56,255))
```
<br/>

### esc.clear
This is used to reset all terminal output styles to their default.
```python
esc.set("red")
print("This is red")
esc.clear()
print("This is normal")
```
<br/>

### esc.cursor_up
This moves the cursor position up by an integer ***n***, which defaults to 1. 
```python
esc.cursor_up(2)
```
<br/>

### esc.cursor_down
This moves the cursor position down by an integer ***n***, which defaults to 1. 
```python
esc.cursor_down(2)
```
<br/>

### esc.cursor_left
This moves the cursor position left by an integer ***n***, which defaults to 1. 
```python
esc.cursor_left(2)
```
<br/>

### esc.cursor_right
This moves the cursor position right by an integer ***n***, which defaults to 1. 
```python
esc.cursor_right(2)
```
<br/>

### esc.erase_to_endln
This erases everything from the current position of your cursor to the end of the line.
```python
esc.erase_to_endln()
```
<br/>

### esc.erase_screen
This erases everything on the screen.
```python
esc.erase_screen()
```
<br/>

### esc.erase_line
This erases everything on the line the cursor is on.
```python
esc.erase_line()
```
<br/>

### esc.erase_prev
This moves the cursor up 1, and erases everything on that line. 
```python
esc.erase_prev()
```
<br/>

### esc.hide_cursor
This hides the cursor. 
```python
esc.hide_cursor()
```
<br/>

### esc.show_cursor
This unhides, or shows the cursor.
```python
esc.show_cursor()
```
<br/>

### esc.enable_alt_buffer
This enables an alternative buffer. 
```python
esc.enable_alt_buffer()
```
<br/>

### esc.disable_alt_buffer
This disables the alternative buffer. 
```python
esc.disable_alt_buffer()
```
<br/>

### esc.save_cursor
This saves the cursor position.
```python
esc.save_cursor()
```
<br/>

### esc.restore_cursor
This restores the cursor position to the previously saved one.
```python
esc.restore_cursor()
```
<br/>

### esc.save_screen
This saves the current screen.
```python
esc.save_screen()
```
<br/>

### esc.restore_screen
This restores the saved screen.
```python
esc.restore_screen()
```
<br/>

### esc.fg_code
Sets the foreground color to a color code.
 ```python
esc.fg_code(255)
```
<br/>

### esc.bg_code
Sets the background color to a color code.
 ```python
esc.fg_code(255)
```
<br/>

### esc.fg_code
Sets the foreground color to a color code.
 ```python
esc.fg_code(255)
```
<br/>

### esc.bg_code
Sets the background color to a color code.
 ```python
esc.bg_code(255)
```
<br/>

### esc.fg_rgb
Sets the foreground color to an rgb color code.
 ```python
esc.fg_rgb(255, 142, 34)
```
<br/>

### esc.bg_code
Sets the background color to an rgb color code.
 ```python
esc.bg_rgb(255, 142, 34)
```
<br/>

### esc.terminal_size
Returns an (x,y) pair representing the width and height of the screen in terms of columns/lines.
```python
size = esc.terminal_size()
n_cols = size.x
n_lines = size.y
# move cursor halfway up the screen, and halfway to the right
esc.cursor_up(n_lines/2)
esc.cursor_right(n_cols/2)
```
<br/>

### esc.cursor_to_top
Sets the cursor position to the top of the screen. 
```python
esc.cursor_to_top()
```
<br/>

### esc.cursor_home
Sets the cursor position to the home position (0,0). 
```python
esc.cursor_home()
```
<br/>

## <div id="string-table"></div> Formatting Strings
## Text Decoration
| String | Description |
| ------ | ----------- |
| reset | reset formatting to default |
| bold | make text bold |
| dim | make text dim |
| blink | make text blink |
| italic | make text italic |
| i | italic shorthand |
| underline | underline text |
| u | underline shorthand |
## Color
| String | Description |
| ------ | ----------- |
| black | set foreground color to black |
| white | set foreground color to white |
| red | set foreground color to red|
| green | set foreground color to green |
| yellow | set foreground color to yellow |
| blue | set foreground color to blue |
| magenta | set foreground color to magenta |
| cyan | set foreground color to cyan |
| Black | set foreground color to bright black |
| White | set foreground color to bright white |
| Red | set foreground color to bright red|
| Green | set foreground color to bright green |
| Yellow | set foreground color to bright yellow |
| Blue | set foreground color to bright blue |
| Magenta | set foreground color to bright magenta |
| Cyan | set foreground color to bright cyan |
| bblack | set background color to black |
| bwhite | set background color to white |
| bred | set background color to red|
| bgreen | set background color to green |
| byellow | set background color to yellow |
| bblue | set background color to blue |
| bmagenta | set background color to magenta |
| bcyan | set background color to cyan |
| bBlack | set background color to bright black |
| bWhite | set background color to bright white |
| bRed | set background color to bright red|
| bGreen | set background color to bright green |
| bYellow | set background color to bright yellow |
| bBlue | set background color to bright blue |
| bMagenta | set background color to bright magenta |
| bCyan | set background color to bright cyan |

## Other
| String | Description |
| ------ | ----------- |
| reverse | reverse foreground & background |
| hidden | hide text |
| strike | strikethrough text |
| strikethrough | strikethrough text|
| delete | delete character |
| home | set cursor to home position |
| request | request cursor position |
| savecursor | save cursor position |
| restorecursor | restore cursor position |

## <div id="color-codes"></div> Color Codes
<img src="https://user-images.githubusercontent.com/995050/47952855-ecb12480-df75-11e8-89d4-ac26c50e80b9.png"/>
<br/><br/>

## Resources
### • <a href="https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797#list-of-keyboard-strings"> Christian Petersen - ANSI Escape Sequences </a>
