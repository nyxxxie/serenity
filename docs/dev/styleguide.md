# Style Guide
We mostly adhere to [PEP8][1], with the following additions and specifications.

Table of Contents:
  * [General](#general)
    * [Tabbing](#tabbing)
    * [Line length](#line-length)
    * [Line wrapping](#line-wrapping)
  * [Functions](#functions)
    * [Type Hints](#type-hints)
  * [Commenting](#line-length)
    * [When to comment](#when-to-comment)
    * [Punctuation in comments](#punctuation-in-comments)
    * [Logical block commenting](#logical-block-commenting)
  * [Classes](#classes)
    * [Method Order](#method-order)
  * [Imports](#imports)
    * [Relative imports](#relative-imports)
  * [Exceptions](#exceptions)
    * [When to use](#when-to-use)
    * [Throwing plain Exception](#throwing-plain-exception)


## General

### Tabbing
#### Rule
Use spaces for indents.
#### Reason
Tabs are great because they are one byte and can be set to appear to be any
number of spaces you prefer, but that same flexibility breaks style when people
use spaces to align arguments and conditionals.  This mixing isn't even allowed
in Python3.

### Line length
#### Rule
Line length is limited to 80 chars.  This limit may be lifted if the line
contains a url, a comment, or in other specific scenarios when trying to stick
to the rule produces ugly code.
#### Reason
Column limits are useful because they keep code from extending past a reasonable
editing window.  Obviously no one is programming on an 80 char terminal anymore,
but this limit is still useful because it helps fit more information on your
screen (documentation, more editing windows, etc).

### Line wrapping
#### Rule
if you need to wrap a function or conditional that goes over the 80 char limit,
please adhere to the following style.  Notice:
  1. All wrapped lines are double indented.  This is to distinquish them from
     the next line.
  2. No words are cut off in the middle and continued on the next line.  This is
     to increase readability.  Be sure to und your wrapped string line with a
     space!
  3. If it makes sense, you may start typing arguments on the next line.  This
     is acceptable if proportionally the size of arguments don't match up or if
     a function invocation is exceptionally long and there is little room for
     the first argument.  Avoid the latter if there are only a few arguments,
     however.
#### Example
```python
var = HugeFunctionCall(("This is a massive string that will wrap.  It "
        "displays the value of some variable to via format, so notice how we "
        "enclose it in parens!  Here's that value: {}.").format(value))
    #do stuff
```


## Functions

### Method Size
#### Rule
Avoid huge functions.  Split out functionality into private or helper methods if
a particular block in a function is performing a large task, even if it's only
used in one specific area.

### Type Hints
#### Rule
Please use [type hints][2] whenever you expect an argument to be of a specific
type.  
#### Reason
Allows implicit documentation and free type checking.  
#### Example
```python
def seek(self, offset: int=0, from_what: int=0) -> int:
    ...
```


## Commenting

### When to comment
#### Rule
Please comment anything that wouldn't be immediately apparant to the average
python programmer who has little-to-no experience with this codebase.  This is
mostly left to your best judgement, but please be considerate and note that it's
far better to have too many comments than barely any comments.

### Punctuation in comments
#### Rule
Do not use periods at the end of a comment unless your comment consists of
multiple sentences or is long.
#### Reason
This is both because most comments aren't complete sentences and because the
period at the end looks bad when the comment is smaller.  This is more of a best
judgement kind of thing, so do what you feel is right.

### Logical block commenting
#### Rule
"Logical Blocks" are defined as sections of code that perform a discrete task,
and are often separated by newlines.  It is prefered that logical blocks are 
commented to explain what they are attempting to achieve.
#### Reason
Commenting blocks is useful because it allows someone who is reading your code
to quickly determine what each "block" is intended to do without needing to
actually spend time figuring it out.  We shouldn't have to reverse engineer the
code of a reverse engineering tool, after all :)
#### Example
```python
# If this isn't the first column rendered, space ourselves out from the
# previous column
if (start != 0):
    start += COLUMN_GAP

# Calc width of the address bar
width = BYTES_PER_ROW * self.font_width()
width += (2 * TEXT_OFFSET)

...
```


## Classes

### Method order
#### Rule
Class methods must be declared in the following order:
  1. Special class methods (`__init__`, `__str__`, etc)
  2. Public class methods
  3. Private class methods (prefixed with \_)

Refrain from using double underscore prefixes for methods and variables.


## Imports

### Relative imports
#### Rule
Don't use relative imports.  If you need to import code from spade, use the full
path.
#### Reason
Looks bad and makes object location more obscure.


## Exceptions

### When to use
#### Rule
Use exceptions only in cases where a method failing is a potentially fatal
action, where fatal is defined as the program entering an invalid state.
The program crashing is FAR preferable to it functioning incorrectly and
creating difficult to diagnose bugs.

### Throwing plain Exception
#### Rule
NEVER throw an Exception, subclass it or use an existing subclassed exception
relevant to your error.

[1]:  https://www.python.org/dev/peps/pep-0008/#code-lay-out
[2]:  https://www.python.org/dev/peps/pep-0484/
