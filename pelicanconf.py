AUTHOR = 'Guru Das Srinagesh'
SITENAME = 'Guru Das Srinagesh'
SITEURL = 'https://gurudas.dev'

PATH = 'content'

TIMEZONE = 'America/Los_Angeles'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = "theme/gurudas"
DISPLAY_PAGES_ON_MENU = True

# Prevent generation of files we don't need.
ARCHIVES_SAVE_AS=''
AUTHOR_SAVE_AS=''
AUTHORS_SAVE_AS=''
CATEGORY_SAVE_AS=''
CATEGORIES_SAVE_AS=''
TAGS_SAVE_AS=''
ARTICLE_PATHS = ['blog']
ARTICLE_URL_END = '{date:%Y}/{date:%m}/{date:%d}/{slug}'
ARTICLE_URL = 'blog/{}.html'.format(ARTICLE_URL_END)
ARTICLE_SAVE_AS = 'blog/{}.html'.format(ARTICLE_URL_END)
PAGE_PATHS = ['pages']
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
DRAFT_SAVE_AS='blog/drafts/{slug}.html'
DRAFT_PAGE_SAVE_AS=''

YEAR_ARCHIVE_URL = 'blog/{date:%Y}/'
YEAR_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_URL = 'blog/{date:%Y}/{date:%m}/'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/index.html'

DIRECT_TEMPLATES = ['index', 'blog']
BLOG_URL = 'blog/'
BLOG_SAVE_AS = 'blog/index.html'

DEFAULT_DATE_FORMAT = '%d %b %Y'
PAGE_ORDER_BY = 'date'

# Delete output directory upon every run
DELETE_OUTPUT_DIRECTORY = True

LOAD_CONTENT_CACHE = False

PLUGINS = [
        'read_more',
        'sitemap',
        'simple_footnotes',
]

# "read more" plugin conf
SUMMARY_MAX_LENGTH = 55
SUMMARY_END_SUFFIX = "... →"
READ_MORE_LINK = '<span>Continue reading</span>'

SLUGIFY_SOURCE = 'basename'

SITEMAP = {
    "format": "xml",
}

STATIC_PATHS = [
    'extras/robots.txt',
    'images',
    'downloads/guru_das_srinagesh_resume.pdf',
]

EXTRA_PATH_METADATA = {
    'extras/robots.txt': {'path': 'robots.txt'},
}
