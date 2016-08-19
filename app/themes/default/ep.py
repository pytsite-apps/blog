"""PytSite Application Default Theme Endpoints.
"""
from datetime import datetime, timedelta
from pytsite import content, tpl, odm, lang, addthis, settings, comments, auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def home(args: dict, inp: dict) -> str:
    """Home.
    """
    exclude_ids = []

    latest = _get_articles(exclude_ids)

    latest_by_section = {}
    for sec in content.get_sections():
        latest_by_section[sec.alias] = _get_articles(exclude_ids, section=sec)

    args.update({
        'latest_articles': latest,
        'latest_by_section': latest_by_section,
        'sidebar': _get_sidebar(exclude_ids),
    })

    return tpl.render('content/home', args)


def content_article_index(args: dict, inp: dict) -> str:
    """Index of articles.
    """
    exclude_ids = [e.id for e in args.get('entities')]
    args.update({
        'sidebar': _get_sidebar(exclude_ids),
    })

    if 'author' in args and args['author']:
        args['author_widget'] = auth.widget.Profile('user-profile', user=args['author'])

    return tpl.render('content/index', args)


def content_article_view(args: dict, inp: dict) -> str:
    """Single article view.
    """
    e = args['entity']
    exclude_ids = [e.id]

    args.update({
        'related': _get_articles(exclude_ids, 3, e.section, 'views_count') if e.model == 'article' else [],
        'entity_tags': content.widget.EntityTagCloud('entity-tag-cloud', entity=args['entity']),
        'share_widget': addthis.widget.AddThis('add-this-share') if settings.get('addthis.pub_id') else '',
        'comments_widget': comments.get_widget().render(),
        'sidebar': _get_sidebar(exclude_ids),
    })

    return tpl.render('content/{}'.format(e.model), args)


def content_page_view(args: dict, inp: dict) -> str:
    """Single Page view.
    """
    return content_article_view(args, inp)


def _get_sidebar(exclude_ids: list) -> list:
    """Get sidebar content.
    """
    r = {
        'popular': _get_articles(exclude_ids, 3, sort_field='views_count', days=7),
        'latest': _get_articles(exclude_ids, 3, days=7),
        'tag_cloud': content.widget.TagCloud(
            uid='sidebar-tag-cloud',
            title=lang.t('tags_cloud'),
            css='block',
            term_css='hvr-sweep-to-right',
        ),
    }

    return r


def _get_articles(exclude_ids: list, count: int = 5, section: content.model.Section = None,
                  sort_field: str = 'publish_time', days: int = None):
    """Get articles.

    :rtype: list
    """
    # Setup articles finder
    f = content.find('article').where('_id', 'nin', exclude_ids).sort([(sort_field, odm.I_DESC)])

    # Filter by section
    if section:
        f.where('section', '=', section)

    if days:
        f.where('publish_time', '>=', datetime.now() - timedelta(days))

    r = []
    for article in f.get(count):
        # Show only articles which can be viewed by current user
        if article.check_permissions('view'):
            r.append(article)
        exclude_ids.append(article.id)

    return r
