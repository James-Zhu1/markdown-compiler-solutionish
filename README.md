# Lab: The Ralph Loop and Workspaces

You will fix a broken markdown compiler.  In the process you will
learn two ideas you will reuse for the rest of the course:

1. **The Ralph loop** -- run the tests, hand the failures to an
   LLM, apply the patch, repeat.
2. **Workspaces** -- use git worktrees so the loop's work is
   isolated and its landing is atomic.

The compiler is one you have seen before.  Four functions in
`markdown_compiler/util/line_functions.py` are stubs; the other five
are implemented.  Your job is to close the gap.

## Part 0: setup

    $ git clone https://github.com/mikeizbicki/markdown-compiler
    $ cd markdown-compiler
    $ export OPENROUTER_API_KEY='...'
    $ eval "$(dic --init)"
    $ ./test.sh

`test.sh` is two lines.  Read it:

    #!/bin/sh
    exec python3 -m pytest .github/tests -x --tb=short

Two flags matter.  `.github/` is a hidden directory, so
`files-to-prompt .` does not pick up the tests: a model prompted
with the repo does not read the answer key.  `-x` stops at the
first failure, so the suite tells the model one thing to fix and
not four.

Run `./test.sh` and see.  It fails on `test_headers`.

## Part 1: the naive loop

Write `ralph.sh`:

    #!/bin/bash
    for i in $(seq 1 8); do
        if ./test.sh > /tmp/out 2>&1; then
            echo "green after $i rounds"
            exit 0
        fi
        committe <<EOF
    $(files-to-prompt markdown_compiler/)

    The tests failed with:

    $(cat /tmp/out)
    EOF
    done

Run it.  Each round fixes one test; the loop goes green.

Now break it deliberately:

1. Ctrl-C in the middle of a `git apply`.  What does
   `git status` say?  What does the next loop iteration do?
2. `git stash` a change before starting.  The loop commits on
   top of it.
3. Start two `ralph.sh` processes at once.  They share
   `.git/index` and neither is safe.
4. Start the loop on a tree whose tests were already red.  It
   burns eight API calls and produces nothing.

Every one of these is a *safety* failure: the loop did work it
should not have, or un-did work it should have kept.

## Part 2: a workspace

A git worktree is a second working tree over the same object
store and refs.

    $ git worktree add -b ralph /tmp/ralph HEAD
    $ cd /tmp/ralph

Observe the isolation:

    $ touch x && git add x && git commit -qm x
    $ ls ..                     # no x in the original tree
    $ git log --all --oneline   # commit visible from both
    $ git -C .. checkout ralph  # refused

The isolation is partial on purpose: separate working tree and
index, shared objects and refs.  A fresh `git clone` would also
isolate, but it would lose the shared history the merge in Part 3
needs.

Now move the loop into the worktree.  Redo each failure above.
Every one is now safe.

## Part 3: atomic landing

The rounds of a loop are a *search*.  The history you want to
publish is one commit.  Try this in a scratch repo:

    $ for i in 1 2 3; do echo $i >> f && git commit -aqm "round $i"; done
    $ git reset --soft HEAD~3
    $ git commit -q -m 'as one commit'

The three rounds are the one commit now.  Add the same step to
`ralph.sh`: when the loop lands green, squash the rounds into one
commit and merge the branch into the one you started on.

Run `git reflog` after the squash.  The three rounds are still
there -- unreachable, but not gone.

## Part 4: the real thing

`itera` is the loop you just wrote, with the failure modes above
already handled.  Read it.

    $ less ~/geni/scripts/itera.sh

Find `itera-validate`, `itera-prepare`, `itera-run`,
`itera-record`, `itera-rollback`.  Match each to a piece of
`ralph.sh`, or to a piece you deliberately did not write.

Now use it on a problem that actually needs the loop:

1. **Markdown lists.** Ordered, unordered, nested.  `pytest -x`
   walks the cases one at a time.
2. **Valid HTML.** `xmllint --html --noout README.html` must exit
   0.  The compiler currently emits `<p><pre>...</pre></p>`.
3. **Extra credit.** `--add_css` must visibly change the rendered
   page.  Playwright MCP gives the model a browser and a camera;
   see the sandbox notes in the README for the cache path.

    $ itera --max 8 --test './test.sh' 'implement markdown lists'

## Submission

Push three branches to a new repo:

1. `naive` -- the Part 1 loop, one commit per round.
2. `worktree` -- the Part 2 loop, landing as one commit.
3. `itera` -- the Part 4 loop, landing as one commit.

Submit the repo url to canvas.
