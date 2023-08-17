Title: Script to add maintainers to a Linux kernel patch
Date: 16 Aug 2023

##### Introducing `add-maintainer.py`

I worked on adding a new script to improve the workflow of developers contributing patches to the Linux kernel. Here it is:

[[PATCH v2 0/1] Add add-maintainer.py script - Guru Das Srinagesh](https://lore.kernel.org/lkml/cover.1691049436.git.quic_gurus@quicinc.com/)

Its fate is yet to be decided - it's only at v2 now, and looks like there is already a mature tool named [`b4`](https://b4.docs.kernel.org/en/latest/) that possibly [does the same thing](https://b4.docs.kernel.org/en/latest/contributor/prep.html#prepare-the-list-of-recipients) as my script.
