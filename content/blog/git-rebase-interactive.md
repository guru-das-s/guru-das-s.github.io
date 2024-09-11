Title: Fun with git rebase --interactive
Date: 2023-12-02T23:41:29-08:00
tldr: The amazing exec and autosquash features of git rebase interactive
Tags: git

_This is the second in a series of blog posts related to some powerful features of
`git` I've used over the years. Previously, I wrote about `git rebase --onto` which
[you can read here]({filename}git-rebase-onto.md)._

`git` offers many powerful features, and one such feature I have used
extensively in kernel development is `git rebase --interactive`. Here is what the man
page has to say about it:

```
-i, --interactive
    Make a list of the commits which are about to be rebased. Let the user edit that
    list before rebasing. This mode can also be used to split commits (see SPLITTING
    COMMITS below).
```

That this feature exists is impressive on its own: in the list of commits that
appears, one can reorder commits, delete them, rework their commit messages, combine
("squash", "fixup") them, and even merge them in recent versions of `git`. But where
this really shines is how it allows, via an optional flag, for executing any
arbitrary shell command for one or even all of the commits in the list. I'm talking
about `git rebase --interactive --exec`.

##### Usecase: Pick a bunch of `linux-next` commits

Frequently we run into the situation where we need some patches that are accepted by
maintainers into their own trees but are not merged by Linus into his main
repository. This occurs when a developer posts a patch to the mailing lists ("pushes
a patch upstream") that is an urgent fix of some kind, required in a product
kernel ("downstream"). The downstream kernel, such as the one the Android Open Source
Project uses (the Android Common Kernel), usually has [strict
requirements](https://android.googlesource.com/kernel/common/+/refs/heads/android-mainline#common-kernel-patch-requirements)
of the commit messages of patches it accepts for merging. One of these requirements
is:

> _If the patch is not merged from an upstream branch, the subject must be tagged
> with the type of patch: `UPSTREAM:`, `BACKPORT:`, `FROMGIT:`, `FROMLIST:`, or
> `ANDROID:`_

Some projects may even require specific
`git-trailers` [ref] [Git - git-interpret-trailers
Documentation](https://git-scm.com/docs/git-interpret-trailers#_description) [/ref]
in the commit message, e.g.:
```
Git-commit: 26b4ca3c39012368ab22b06cd35dd6b77f0f3e00
Git-repo: https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
```

This means every single patch being pushed to the downstream kernel project would
need to be tagged this way. If we need to get, say, 10 or 20 patches merged from a
maintainer's tree or linux-next, we need a scalable way of tagging all of them with
one of the above subject prefixes and adding those git trailers. This is where `git
rebase --interactive --exec` really shines.

From within the downstream kernel, add the `linux-next` remote:
```
git remote add linux-next https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git
git fetch linux-next
```
Gather list of commits required. These may be abbreviated SHAs too, for convenience.
```
base_sha=$(git rev-parse HEAD)
pick_commits=(<sha1> <sha2> ... <shaN>)
```
Cherry pick each commit and add the first trailer:
```
for commit in "${pick_commits[@]}"; do
    git cherry-pick $commit
    git commit --amend --no-edit --trailer "Git-commit: $(git rev-parse $commit)"
done
```
Now, add the subject prefix `FROMGIT:` to all the commits that were just cherry picked:
```
git rebase -i --exec 'git commit --amend -m "FROMGIT: $(git show -s --format=%B)"' $base_sha
```
Next, add the second trailer to all the commits that were cherry picked:
```
git rebase -i --exec 'git commit --amend --no-edit --trailer "Git-repo: https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git"' $base_sha
```
Finally, add one's own Signed-off-by to all the cherry picked commits:
```
git rebase -i --exec 'git commit --amend --no-edit -s' $base_sha
```

##### git fixup and `git rebase --interactive --autosquash`

This blog post: [Auto-squashing Git
Commits](https://thoughtbot.com/blog/autosquashing-git-commits) goes into great
detail on what this feature is, and how it may be made use of.

---
