Title: Script to add maintainers to a Linux kernel patch
Date: 16 Aug 2023
tldr: A Python script to improve kernel patch submission workflow
Tags: linux, kernel, opensource

##### Introducing `add-maintainer.py`

I worked on adding a new script to improve the workflow of developers contributing patches to the Linux kernel. Here it is:

[[PATCH v2 0/1] Add add-maintainer.py script - Guru Das Srinagesh](https://lore.kernel.org/lkml/cover.1691049436.git.quic_gurus@quicinc.com/)

Its fate is yet to be decided - it's only at v2 now, and looks like there is already a mature tool named [`b4`](https://b4.docs.kernel.org/en/latest/) that possibly [does the same thing](https://b4.docs.kernel.org/en/latest/contributor/prep.html#prepare-the-list-of-recipients) as my script.

##### Update (Sep 1)

The upstream maintainers have ruled in favour of `b4`, sounding the death knell
for my script[ref]Mark Brown's response to [v3 of my script](https://lore.kernel.org/lkml/0f7b32e1-1b26-4543-bfec-471641a67416@sirena.org.uk/)[/ref]
[ref]Krzysztof being his usual [blunt and brutal self](https://lore.kernel.org/lkml/db8d5123-19d7-50d0-935b-a25d235e6e2e@linaro.org/)

##### Takeaways and Learnings

I am extremely proud of the effort I put into `v3` - I even added an `--undo`
flag! I think it's a fantastic nifty little script and:

1. Not only did I get to learn some Python, but also
2. Earned the satisfaction of independently identifying a problem that needed fixing, and
3. Solving the non-trivial problem using Python in Pythonic ways and following best practices.

Onwards and upwards, I say! On to the next problem. I'm on a roll.

---
