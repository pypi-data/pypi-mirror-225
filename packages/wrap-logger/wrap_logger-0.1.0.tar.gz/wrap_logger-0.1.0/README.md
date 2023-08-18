# Wrap Logger

A library to wrap around objects and modules in Python and log property
accesses and calls.

## Rationale

In some cases when programming, errors can break things to the point where
you have no idea where things went wrong, for example, crashing the runtime
environment before a backtrace can be printed. In these cases, it can be
extremely useful to log changes to data that are potentially related to the
issue, but doing so can be tedious and slow. I needed a simple solution to
easily inject logging into objects, and so I created `wrap-logger`.

## Usage

Using `wrap-logger` is simple. Simply call the `wrap` function, which will
return a wrapped version.

### With a module

```py
import foo
from wrap_logger import wrap

# Now all function calls and global reads/writes will be logged
foo = wrap(foo)
```

### With a class

```py
from wrap_logger import wrap

class Simple:
    """Simple class for testing purposes"""
    def __init__(self) -> None:
        self.value = 42

    def __repr__(self) -> str:
        return 'simple'

    def echo(self, value: str) -> str:
        return value


obj = wrap(Simple())


# Getting a property causes things to be logged
variable = obj.value
# [WRAP LOG] > Get  simple.value
# [WRAP LOG] < Get  simple.value: gave 42

# Same for setting properties
obj.value = 43
# [WRAP LOG] > Set  simple.value: 42 -> 43
# [WRAP LOG] < Set  simple.value

# And calling functions
obj.echo('hello world')
# [WRAP LOG] > Call simple.echo('hello world')
# [WRAP LOG] < Call simple.echo('hello world'): returned 'hello world'
```

### Without Pip

`wrap-logger` requires no dependencies, and can even function with some parts
of the standard library missing. Simply head over to the releases tab where the
`wrap-logger.zip` file is attached, then extract it into a new folder within
your project, where you can import it easily. You should then be able to use it
normally, importing it from your desired location.

## Implementation details

`wrap-logger` wraps objects in a `WrapLogger` class. Although the class does
override the `__class__` property so as to fool `isinstance` checks, fooling
the `type` function does not appear to work, so those checks may fail leading
to potentially erroneous behaviour.

## TODOs

`wrap-logger` was thrown together so I could quickly debug another project, so
it is incomplete. If there is demand (hint: create an issue), I will be happy
to try my hand at implementing the following features:

* [ ] Specify output file that `wrap-logger` prints to
* [ ] Recursive wrapping, so that attributes of attributes are also logged
* [ ] Configuration on what is/isn't logged (currently it just prints
      everything)
* [ ] Figure out what happens if you use `wrap-logger` on itself. Does it
      crash? Does it delete System 32? Does the space-time continuum collapse?
      Who knows!
