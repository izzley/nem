# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'nem'

SPIDER_MODULES = ['nem.spiders']
NEWSPIDER_MODULE = 'nem.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nem (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'nem.middlewares.NemSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'nem.middlewares.NemDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'nem.pipelines.ExtractCSV': 300,
}

# Log settings 
# See https://doc.scrapy.org/en/latest/topics/settings.html#std-setting-LOG_FILE

LOG_ENABLED = True
# Default: True
# Whether to enable logging.

LOG_ENCODING = 'utf-8'
# Default: 'utf-8'
# The encoding to use for logging.

# LOG_FILE = "scrapylog.txt"
# Default: None
# File name to use for logging output. If None, standard error will be used.

# LOG_FORMAT
# Default: '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
# String for formatting log messages. 
# Refer to the Python logging documentation for the qwhole list of available placeholders.

# LOG_DATEFORMAT
# Default: '%Y-%m-%d %H:%M:%S'
# String for formatting date/time, expansion of the %(asctime)s placeholder in LOG_FORMAT. 
# Refer to the Python datetime documentation for the whole list of available directives.

# LOG_FORMATTER
# Default: scrapy.logformatter.LogFormatter
# The class to use for formatting log messages for different actions.

# LOG_LEVEL
# Default: 'DEBUG'
# Minimum level to log. Available levels are: CRITICAL, ERROR, WARNING, INFO, DEBUG. 
# For more info see Logging.

# LOG_STDOUT
# Default: False
# If True, all standard output (and error) of your process will be redirected to the log. 
# For example if you print('hello') it will appear in the Scrapy log.

# LOG_SHORT_NAMES
# Default: False
# If True, the logs will just contain the root path. 
# If it is set to False then it displays the component responsible for the log output

# LOGSTATS_INTERVAL
# Default: 60.0
# The interval (in seconds) between each logging printout of the stats by LogStats.

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
