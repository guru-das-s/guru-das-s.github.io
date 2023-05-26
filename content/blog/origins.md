Title: How I generate gurudas.dev
Slug: how-i-generate-gurudas-dev
Date: 25 May 2023

##### Beginnings

I've always wanted my own website. Like, forever. Not Wordpress-like, but my
own, written from scratch. I figured out that this meant that I would have to
use a static site generator. This post is all about how I bought my first
domain, chose a hosting provider, set up DNS correctly, generated my website's
content, and set up auto-deploy upon `git push`.

The motivation to create this website came from a co-worker who I discovered had
built his site using [Skeleton](http://getskeleton.com/). This seemed doable to
me, not knowing the basics of getting a website up and running. I tried not to use
Skeleton like he did, but since I had zero experience with web development (save
the occasional tinkering with HTML in those Web 1.0 days when I had blogs on
Blogger.com and Wordpress) I eventually figured out the basics of what I needed
to know in order to get started - a path which eventually led me to use
Skeleton.

##### The Github repo

The code for my website is [here on
Github](https://github.com/guru-das-s/guru-das-s.github.io).

##### Choosing a domain and a provider

Naming things is hard - it took me a while before I settled on this current
domain name. Google Domains has a pretty good deal for `.dev` domains (currently
$12 annually) and for an extra $6 a month, I got a custom email address on this
domain too via their Workspace Business Starter option.

I had to set up these DNS records: `A`, `CNAME`, and `TXT` (for Github Pages,
see below).

##### Using Pelican as my static site generator

I [asked Hacker News](https://news.ycombinator.com/item?id=35019343) which
static site generator to use, and based on the responses, I went with my gut
feeling and decided to use Pelican. I liked the documentation and it seemed to
use Python (which I wanted to use), so it was an easy decision for me.

I couldn't be happier with my choice. Pelican seems to have a bunch of different
[plugins](https://github.com/pelican-plugins) which allow you to do things like
adding a [sitemap](https://github.com/pelican-plugins/sitemap) to your site, and
adding a ["Read More" link](https://github.com/pelican-plugins/read-more) to
your blog posts, and so on.

Building my own website from scratch using Pelican has been a very rewarding and
fulfilling experience. I don't know a lot of HTML or CSS beyond the very basics,
so I'm getting to learn a considerable amount of how they work together, and the
various tags and options available.

###### Creating a custom theme based on Skeleton

Now, since I wanted a custom website theme, I found Pelican to be quite
forbidding as a newbie since the documentation says that in order to create a
new theme, you've <i> got to </i> have ALL these templates:

    └── templates
        ├── archives.html         // to display archives
        ├── period_archives.html  // to display time-period archives
        ├── article.html          // processed for each article
        ├── author.html           // processed for each author
        ├── authors.html          // must list all the authors
        ├── categories.html       // must list all the categories
        ├── category.html         // processed for each category
        ├── index.html            // the index (list all the articles)
        ├── page.html             // processed for each page
        ├── tag.html              // processed for each tag
        └── tags.html             // must list all the tags. Can be a tag cloud.

> <i> templates </i> contains all the templates that will be used to generate
> the content. The template files listed above are mandatory...

What they <i> didn't </i> say in that section was that one does not need to
specify every single one of those files, and that the files thus omitted will
simply be inherited from the `simple` theme. This they shoved into a separate
section on
[Inheritance](https://docs.getpelican.com/en/latest/themes.html#inheritance) way
down in the page:

> If one of the mandatory files in the `templates/` directory of your theme is
> missing, it will be replaced by the matching template from the simple theme.

The theme is very bare bones and is adapted from the source code of the
[getskeleton.com](getskeleton.com) website.

##### Setting up a Worflow via Github Actions

Choosing Github Pages for hosting was an easy choice was easy as this is offered
for free. Plus, I was excited about setting up a CI/CD pipeline for generating
my website through Github Actions and Workflows. I looked at existing examples
and got that up and running too! Check it out:
[deploy.yml](https://github.com/guru-das-s/guru-das-s.github.io/blob/master/.github/workflows/deploy.yml)

##### Credits:

- [pyladies-brazil](https://github.com/pyladies-brazil/br-pyladies-pelican): I
  referred to this repository and their corresponding
  [website](http://brasil.pyladies.com/) extensively while trying to learn how
  to pick and choose the pieces I want in my Pelican setup.
