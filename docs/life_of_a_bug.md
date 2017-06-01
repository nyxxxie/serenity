# Life of a Feature
This document describes the lifes-cycle of a bug, from discovery to fix.
It is meant to be useful for anyone who either wants to report a bug or anyone
who wants to patch some bugs.

## Discovery
When a bug is discovered, it should be submitted to the issue tracker on
Github.  Use the [bug report template](docs/bug_template.txt) to ensure we get
all the information necessary to figure out what the problem is, and please keep
an eye out for any additional questions we might have.

## Bug is triaged and/or assigned
After we've understood the nature and scope of the bug, it will be catagorized
and eventually assigned.  Alternately, if a bug is not immediately assigned
anyone from the community may choose to patch it themselves.  Bugs that we
either can't solve or don't have the time to solve and are particularly
important or valuable will get a special `[help wanted]` tag, and should be
particularly noted by anyone who wants to patch bugs.

## Bug is fixed
After someone has identified the cause of the bug, they should fork the repo,
create a new `bugfix` branch (see [branching](docs/branching.md) for more info)
and start a `[wip][bugfix]` pull request to let others know they are working on
that fix.  This process pretty closely matches that of
[creating a new feature](docs/life_of_a_feature.md), so give that proccess a
look for more detail.  Once the fix is done, the issue will be closed and spade
will be less broken!
