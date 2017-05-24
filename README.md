# ColorString

## Example

```python
from colorstring import ColorString

first = ColorString("first", "blue", "yellow", "bold")
second = ColorString("second", fg="red", frmt="normal")
third = ColorString("third")

print(first, second, third)

added = first + second + third
print(added)

spliced = added[2:8]
print(spliced)
```
outputs:
```
^[1;34;43mfirst^[0m ^[0;31;48msecond^[0m ^[0;38;48mthird^[0m
^[1;34;43mfirst^[0m^[0;31;48msecond^[0m^[0;38;48mthird^[0m
^[1;34;43mr^[0m^[1;34;43ms^[0m^[1;34;43mt^[0m^[0;31;48ms^[0m^[0;31;48me^[0m^[0;31;48mc^[0m
```
