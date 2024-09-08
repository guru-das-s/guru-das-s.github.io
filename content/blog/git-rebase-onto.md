Title: How I used git rebase --onto
Date: 2023-11-09T23:25:28-08:00
tldr: Git rebase onto, an underrated but powerful command

On one of my daily trawlings of Hacker News, I came across Julia Evans' blogpost on
[confusing git
terminology](https://jvns.ca/blog/2023/11/01/confusing-git-terminology/#rebase-onto)
that lists `git rebase --onto` as one such confusing command. I had never used this
`--onto` flag before and her description didn't really help me visualize the problem
or the solution.

I shrugged and let it go, not thinking much of it at the time.

I ended up using it recently, when I had to rebase a feature branch based off a
couple of weeks old, stale, `master` branch ***onto*** the up-to-date tip of the
same `master` branch.

***

Since I was using Gerrit, my feature branch had a `topic:XYZ` set. This `XYZ` topic
series of mine had about ~20 commits, and the master branch had advanced quite a bit
with almost ~15K commits [ref] This large number of changes is because the project
was the Linux kernel actively being developed by a global team of developers. [/ref],
some of which were also large merge commits.

My erstwhile strategy for cherrypicking the whole series onto the moving tip of the
`master` branch was as follows:

```bash
git config pull.rebase true
git pull <server/project> <refs/changes/12345/4>
```

(where `12345` was the last change in the series)

This worked at the time I had published this strategy to our internal documentation
at work so that other developers could make use of my `XYZ` series on top of the
latest, up-to-date `master` branch. Over time, though, the series ran into a merge
conflict once the master branch had advanced sufficiently enough. And that is when I
was asked to rebase the series to fix this merge conflict and update the
documentation.

When I tried the above instructions on top of the up-to-date master branch, it did
not work because git tried to interactively rebase _all_ the ~15K changes one by one
and then somehow ran into merge conflicts on changes unrelated to mine. Resolving
merge conflicts unrelated to my changes was a clear sign that I was doing something
wrong &mdash; there _had_ to be a better way.

After a bit of Googling, I found this answer [ref]
[Git: Interactively rebase a range of commits - Stack
Overflow](https://stackoverflow.com/questions/45336573/git-interactively-rebase-a-range-of-commits)
[/ref]
on Stack Overflow that succintly expressed what I had to do:

```
git rebase --onto <final_base_commit> <initial_base_commit> <head>
```

This was interesting. The fact that I had come across this recently was fresh in my
mind, and hence I quickly consulted the `man` page for `git-rebase`:

```
First let’s assume your topic is based on branch next. For example, a feature
developed in topic depends on some functionality which is found in next.

        o---o---o---o---o  master
             \
              o---o---o---o---o  next
                               \
                                o---o---o  topic

We want to make topic forked from branch master; for example, because the
functionality on which topic depends was merged into the more stable master branch.
We want our tree to look like this:

        o---o---o---o---o  master
            |            \
            |             o'--o'--o'  topic
             \
              o---o---o---o---o  next

We can get this using the following command:

    git rebase --onto master next topic
```


Aha! When read alongside the man page, the Stack Overflow answer's recommendation
started to make sense.

`final_base_commit` would be my current `HEAD`, i.e. the current (up-to-date)
tip of the `master` branch.

`initial_base_commit` would be the **parent of** the first patch in my series.
In my case, this was `<SHA>^` where `<SHA>` was that of the first patch - easily
available by inspection on Gerrit. Let's say this was `43487e7b567cfb^`.

`head` would be the `FETCH_HEAD` after running `git fetch` on the **last change** in
my series, i.e.
```
git fetch <server/project> <refs/changes/12345/4>
```

Thus, the final command became:

```
git rebase --onto HEAD 43487e7b567cfb^ FETCH_HEAD
```
The merge conflict I had to fix was fairly trivial, and I was done in no time.

I was really impressed by the power of this feature as I was dreading having to
manually cherry-pick all of the ~20 changes in my series.

---
