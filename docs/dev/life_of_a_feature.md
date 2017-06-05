# Life of a Feature

## Starting a Feature
A feature can start in one of two ways: as an issue or as a pull request.

### Issues
If you have an idea for a feature but are unsure about it or don't want to
implement it, Create an issue for it in the issue tracker.  Before you do this,
*please* make sure there isn't already an issue or open pull request for your
idea.

### Pull Request
If you have an idea for a feature and want to work on it, do the following:

  1. Fork the spade repo
  2. Create a new feature branch: `git checkout -b feature/<branch name>` in
     your newly-forked repo.
  3. Open a pull request in the upstream spade repo with the prefix `[wip]`.

This will allow developers and reviewers to see that a feature is being worked
on.  The `[wip]` prefix lets reviewers know that the issue is currently being
worked on and shouldn't be treated as finished.  It also lets others know that
you are working on a particular feature and that they probably shouldn't start
on it themselves.

If you're implementing a feature that started as an issue, please link it
somewhere in the body of your pull request by adding `closes #<issue_number>`.
This will update the issue timeline to reflect that you've opened a pull
request and will close the issue when the feature is complete.

Please try to isolate your pull request to roughly one major addition or
modification of code.  Large pull requests that try to do a lot of work mean
larger review times and less people who can work on spade concurrently.

## Developing a Feature
### Styling
In order to keep the codebase roughly homogeneous, we have a [style guide][1].
It's mostly similar to PEP8 with some additions.  You can (and should) use
pylint to perform a rough check on your code, though it's not perfect and you
should take a look at the style guide.

### Pylint
Also use pylint to perform rough error checking, since it can catch a lot of
stuff that the compiler would in other languages.  I've set it up to pretty much
perform every check it can.  Also, don't add pylint ignore comments unless you
have a good reason.

### Tests
Spade requires tests be created for any new code added, so please be sure to
write them.  This is to allow us to verify the code you wrote works, both upon
submission and later on when we start modifying/replacing stuff you might
depend on, refactoring, etc.  Please try to keep disk writes to a minimum and
try to mock out any calls to apis you don't control.  Also prefer many tests
that test single paths of execution over huge tests that test several, as that
allows testing to be done concurrently (and thereby quicker).

### Documentation
Spade also requies that feature code and usage be documented.  Check out the
[documenting code][2] page for more info.

## Submitting a Feature
Once your contribution is ready to ship, remove the `[wip]` marker from your
title and [request a contributor to review it][3].  Please make sure that pylint
doesn't complain about anything and all of the tests pass.

[1]: docs/dev/styleguide.md
[2]: docs/dev/documenting_code.md
[3]: https://github.com/blog/2291-introducing-review-requests
