# Sev segment

A Python library for controlling a 4-digit 7-segment display on a Raspberry Pi.

### Install and Use the Library

**Install the library:**

```bash
pip install .
```

**Use the library in your project:**

```python
from sevensegment.display import SevenSegmentDisplay
import time

display = SevenSegmentDisplay()
try:
    while True:
        display.display_number('1111')
        time.sleep(0.010)
except KeyboardInterrupt:
    display.cleanup()
```

```python
from sevensegment.display import SevenSegmentDisplay

display = SevenSegmentDisplay()
display.display_number('1234')
display.cleanup()
```
