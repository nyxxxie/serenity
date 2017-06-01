# Life of a Feature

## Starting a Feature
A feature can start in one of two ways: as an issue or as a pull request.

### Issues
If you have an idea for a feature but are unsure about it or don't want to
implement it, Create an issue for it in the issue tracker.  Before you do this,
*please* make sure there isn't already an issue or open pull request for your
idea.

### Pull Request
If you have an idea or see an issue relating to a feature you'd like to work
on:

  1. Fork the spade repo
  2. Create a new feature branch: `git checkout -b feature/<branch name>`
  3. Open a pull request in the upstream spade repo with the prefix `[wip]`.

The `[wip]` prefix lets reviewers know that the issue is currently being worked
on and shouldn't be treated as finished.  It also lets others know that you are
working on a particular feature and that they probably shouldn't start on it
themselves.  If you're implementing a feature that started as an issue, please
link it in the body of your pull request.  This will update the issue timeline
to reflect that you've opened a pull request, helping to keep track of who is
working on what.

## Developing a Feature
## Submitting a Feature
