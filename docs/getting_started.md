# Getting Started

## Getting started
Spade attempts to make use of the convention and layouts popular in other
projects.  The hardest part about getting started will likely be getting familar
enough with the codebase to understand how you might contribute an improvement
or idea you have.  We reccomend the following to understand what's going on:
  * Check out [this document] for a description of how the repo is organized.
    Use this to hone in on areas that might be relevant to your proposed
    contribution and to understand where it might belong.
  * When trying to learn about a method or class, how you learn it depends on the
    reason why you need to learn about it:
      1. *What is it for?* All documented components should explain their
         purpose, so check the generated sphinx docs or the docstrings
         associated with that component.
      2. *How do I use it?* First check out the docs for that method, and then
         check out the relevant tests associated with it and its usages in the
         codebase.
      3. *How does it work?* Read the code, which should be sufficiently
         commented that you can understand what it's doing.
    As you contribute yourself, keep these assumptions of how a component will
    be documented in mind so that other developers can expect the same
    experience when reading your code.  Code that isn't sufficiently documented
    *is a valid issue* and may be raised in the issue tracker.

### Task ideas
If you want to contribute but don't know where to start, here are some tasks
that you can do right now without needing to be too creative:
  * Solve or lend your expertise to an issue in the issue tracker.
  * Review open pull requests (including those in progess).
  * Implement approved features in the issue tracker (if they don't already
    have a pull request open)
  * Create new tests for cases we don't cover.  You can easily assess this using
    pytest-cov.  Check out Testing section for more info.

The biggest challenge to getting started is getting to know the codebase well
enough to feel comfortable contributing.  Here are some low-complexity tasks
that you may consider engaging in to help become familiar with spade:
  * Create new tests
  * Investigate/fix low complexity bugs
  * Implement appr
