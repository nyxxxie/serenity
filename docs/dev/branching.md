# Branching
This short document attempts to describe the branching strategy used in this
project.

## Branching strategy
All new additions/modifications to the codebase must be developed in branches.
Upon completion, these will then be merged into master.  These "development"
branches should adhere to the following naming format:
  * `feature/descriptive-name` - For new features/modifications (see [loaf][1]).
  * `bugfix/descriptive-name` - For fixing errors in existing code (see [loab][2]).

This model allows us to keep a clear history of what features were introduced to
the mainline when, and allows us to revert code if need be.  It's also fairly
standard across most projects, and is basically [gitflow][3] without a develop
branch.

## Releasing versions
Since we merge directly into master upon feature completion, its safe to say
that things might change unexpectedly for users at some point.  For users that
want a more consistant experience, official versions of spade will be tagged,
with the most recent released version being marked with the `latest` tag.

[1]: docs/dev/life_of_a_feature.md
[2]: docs/dev/life_of_a_bug.md
[3]: http://nvie.com/posts/a-successful-git-branching-model/
