# ra2csf

A Python library for reading, writing, and updating `.csf` files from Command & Conquer: Red Alert 2 and Command & Conquer: Yuri's Revenge.

## Installation

```bash
pip install ra2csf
```

## Overview

CSF (Command String File) files contain localized text strings used in Red Alert 2 and Yuri's Revenge. This library provides simple functions to load, dump, and update these files.

## Core Functions

### `ra2csf.load(file)`

Load a CSF file and return a dictionary mapping string labels to their values.

**Parameters:**

- `file` - Path to CSF file (str) or file-like object

**Returns:** `dict[str, str]` - Dictionary where keys are label names and values are the corresponding text strings.

**Example:**

```python
import ra2csf

# Load from file path
strings = ra2csf.load("ra2.csf")
print(strings["NAME: Soviet War Factory"])
# Output: "Soviet War Factory"

# Load from file object
with open("ra2.csf", "rb") as f:
    strings = ra2csf.load(f)
```

### `ra2csf.dump(strmap, file)`

Write a dictionary of strings to a CSF file.

**Parameters:**

- `strmap` - Dictionary mapping label names (str) to text values (str)
- `file` - Output path (str) or writable file-like object

**Example:**

```python
import ra2csf

new_strings = {
    "NAME: Soviet War Factory": "Soviet War Factory",
    "DESC: Soviet War Factory": "Produces heavy vehicles",
    "NAME: Tesla Reactor": "Tesla Reactor",
}

ra2csf.dump(new_strings, "custom.csf")
```

### `ra2csf.update(file, strmap)`

Update an existing CSF file with new or modified strings. Existing strings not in the update map remain unchanged.

**Parameters:**

- `file` - Path to existing CSF file (str)
- `strmap` - Dictionary of label names and values to add or modify

**Example:**

```python
import ra2csf

# Update specific strings
ra2csf.update("ra2.csf", {
    "NAME: Soviet War Factory": "Soviet Tank Factory",
    "NAME: New Unit": "Apocalypse Tank",
})
```

## Complete Example

```python
import ra2csf

# Load original
strings = ra2csf.load("original.csf")

# Make modifications
strings["NAME: Tesla Coil"] = "Tesla Tower"

# Save to new file
ra2csf.dump(strings, "modified.csf")

# Or update in-place
ra2csf.update("original.csf", {
    "NAME: Tesla Coil": "Tesla Tower"
})
```

## Advanced Usage

### Loading with Extra Data

The `load` function handles both standard entries (with ` RTS` label) and extra data entries (with `WRTS` label), but returns only the string values by default.

### Custom File Objects

All functions accept either file paths or file-like objects:

```python
import io
import ra2csf

# Using BytesIO
buffer = io.BytesIO()
ra2csf.dump({"LABEL": "Text"}, buffer)
buffer.seek(0)
loaded = ra2csf.load(buffer)
```

## Development

```bash
# Install with dev dependencies
pip install ra2csf[dev]

# Run tests
pytest
```
