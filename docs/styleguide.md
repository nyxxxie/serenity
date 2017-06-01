TODO: separate this out to be more organized (like http://google.github.io/styleguide/pyguide.html)

## Code style
Code must adhere to [PEP8][1] with the following additions/exceptions:
  * Line length is limited to 79 chars, however this restriction may be lifted
    ignored if it would result in ugly code.  For example, if you add a comment
    to a line that increases that line's length to 100, that is acceptable.
    The pylint config bundled with this repo defaults to 80, so if you go over
    and trigger a warning please make sure there's a good reason for it.
  * Class methods must be declared in the following order:
      1. Special class methods (`__init__`, `__str__`, etc)
      2. Public class methods
      3. Private class methods (prefixed with _)
  * Refrain from using double underscore prefixes for methods and variables.
  * Please use [type hints][2] whenever you expect an argument to be of a
    specific type.
  * Please comment anything that wouldn't be immediately apparant to the average
    python programmer who has little-to-no experience with this codebase.  This
    is mostly left to your best judgement, but please be considerate and note
    that it's far better to have too many comments than barely any comments.
  * Do not use periods at the end of a comment unless your comment consists of
    multiple sentences or is long.  This is both because most comments aren't
    complete sentences and because the period at the end looks bad when the
    comment is smaller.  This is more of a best judgement kind of thing, so do
    what you feel is right.
  * It is preferred that all "blocks" of code that perform a distinct task
    should have comment inserted before them explaining their purpose.  This
    makes it easier to read code quickly and understand what the author
    intended for it to do.  It also readability, since it's easy to deliniate
    what blocks perform what specific functionality.
  * Prefer `format` to `%`.
  * Don't use relative imports.  If you need to import code from spade, use the
    full path.
  * Avoid huge methods.  Split out functionality into private or helper methods
    if a particular block in a function is performing a large task, even if it's
    only used in one specific area.
  * Use exceptions only in cases where a method failing is a potentially fatal
    action, where fatal is defined as the program entering an invalid state.
    The program crashing is FAR preferable to it functioning incorrectly and
    creating difficult to diagnose bugs.
  * NEVER throw an Exception, subclass it or use an existing subclassed
    exception relevant to your error.
  * Use spaces for indents.  Tabs are great because they are one byte and can
    be set to appear to be any number of spaces you prefer, but that same
    flexibility breaks style when people use spaces to align arguments and
    conditionals.  This mixing isn't even allowed in Python3.
  * If you need to wrap a function or conditional that goes over the 80 char
    limit, please adhere to the following style.  Notice:
      1. All wrappe lines are double indented.  This is to distinquish them
         from the next line.
      2. No words are cut off in the middle and continued on the next line.
         This is to increase readability.  Be sure to und your wrapped string
         line with a space!
      3. If it makes sense, you may start typing arguments on the next line.
         This is acceptable if proportionally the size of arguments don't match
         up or if a function invocation is exceptionally long and there is
         little room for the first argument.  Avoid the latter if there are
         only a few arguments, however.

```python
var = HugeFunctionCall(("This is a massive string that will wrap.  It "
        "displays the value of some variable to via format, so notice how we "
        "enclose it in parens!  Here's that value: {}.").format(value))
    #do stuff
```

[1]:  https://www.python.org/dev/peps/pep-0008/#code-lay-out
[2]:  https://www.python.org/dev/peps/pep-0484/
