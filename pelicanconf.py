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
USE_FOLDER_AS_CATEGORY = True
DEFAULT_CATEGORY = 'blog'
CATEGORY_SAVE_AS=''
CATEGORIES_SAVE_AS=''
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
TAGS_URL = 'tags/'
TAGS_SAVE_AS='tags/index.html'
ARTICLE_PATHS = ['blog', 'til']
ARTICLE_URL = '{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
PAGE_PATHS = ['pages']
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
DRAFT_SAVE_AS='{category}/drafts/{slug}.html'
DRAFT_PAGE_SAVE_AS=''

FEED_MAX_ITEMS = 15
FEED_ATOM = "feed.atom"

YEAR_ARCHIVE_URL = 'blog/{date:%Y}/'
YEAR_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/index.html'
MONTH_ARCHIVE_URL = 'blog/{date:%Y}/{date:%m}/'
MONTH_ARCHIVE_SAVE_AS = 'blog/{date:%Y}/{date:%m}/index.html'

DIRECT_TEMPLATES = ['index', 'blog', 'til', 'tags']
BLOG_URL = 'blog/'
BLOG_SAVE_AS = 'blog/index.html'
TIL_URL = 'til/'
TIL_SAVE_AS = 'til/index.html'

DEFAULT_DATE_FORMAT = '%d %b %Y'
PAGE_ORDER_BY = 'date'

# Delete output directory upon every run
DELETE_OUTPUT_DIRECTORY = True

LOAD_CONTENT_CACHE = False

PLUGINS = [
        'read_more',
        'sitemap',
        'simple_footnotes',
        'neighbors',
]

# "read more" plugin conf
SUMMARY_MAX_LENGTH = 60
SUMMARY_END_SUFFIX = "... "
READ_MORE_LINK = '<span>→ Continue reading</span>'

SLUGIFY_SOURCE = 'basename'

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {
            'guess_lang': 'false',
            'css_class': 'highlight',
        },
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
}

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
