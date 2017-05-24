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
