# -*- coding: utf-8 -*-
"""
Glossary -- BGLOSSARY
=====================
Author: Toni Heittola (toni.heittola@gmail.com)

"""

import os
import logging
import shutil
import copy
from bs4 import BeautifulSoup
from jinja2 import Template
from pelican import signals, contents
import yaml
import collections

logger = logging.getLogger(__name__)
__version__ = '0.1.0'

bglossary_default_settings = {
    'panel-color': 'panel-default',
    'header': 'Glossary',
    'mode': 'list',
    'template': {
        'panel': """
            <div class="panel {{ panel_color }}">
                {% if header %}
                    <div class="panel-heading">
                    <h3 class="panel-title">{{header}}</h3>
                    </div>
                {% endif %}
                {% if show_stats %}
                {% if latest_update or term_count or translation_counts %}
                <p class="text-right">
                    {% if term_count %}
                    <small class="text-muted"><strong>Terms</strong> {{term_count}}{% if latest_update or translation_counts %}, {% endif %}</small>
                    {% endif %}
                    {% if translation_counts -%}
                        <small class="text-muted"><strong>Translations</strong> 
                        {% for key, value in translation_counts.items() -%}
                        <img src="theme/images/bglossary_blank.gif" class="flag flag-{{key}}" />{{value}} {% endfor -%}
                        {% if latest_update %}, {% endif %}
                        </small>
                    {% endif %}
                    {% if latest_update %}
                    <small class="text-muted"><strong>Updated</strong> {{latest_update}}</small>
                    {% endif %}
                </p>                
                {% endif %}
                {% endif %}
                <table class="table bglossary-container">
                {{list}}
                </table>
            </div>
        """,
        'list': """
            {% if header %}<h1 class="section-heading">{{header}}</h1>{% endif %}
            {% if show_stats %}
            {% if latest_update or term_count or translation_counts %}            
            <p class="text-right">
                {% if term_count %}
                <small class="text-muted"><strong>Terms</strong> {{term_count}}{% if latest_update or translation_counts %}, {% endif %}</small>
                {% endif %}
                {% if translation_counts -%}
                    <small class="text-muted"><strong>Translations</strong> 
                    {% for key, value in translation_counts.items() -%}
                    <img src="theme/images/bglossary_blank.gif" class="flag flag-{{key}}" />{{value}} {% endfor -%}
                    {% if latest_update %}, {% endif %}
                    </small>
                {% endif %}
                {% if latest_update %}
                <small class="text-muted"><strong>Updated</strong> {{latest_update}}</small>
                {% endif %}
            </p>
            {% endif %}
            {% endif %}
            <div class="list-group bglossary-container"  style="padding-left:1em;">
                <div class="row">
                {{list}}
                </div>
            </div>
        """},
    'item-template': {
        'panel': """
            <tr>
                <td class="{{item_css}}">
                    <div class="row">
                        <div class="col-md-12">
                        <h2>{{term}}</h2>
                        {% if wikipedia %}
                            <a href="{{wikipedia}}" target="_blank" title="Wikipedia"><i class="pull-right fa fa-wikipedia-w fa-border" aria-hidden="true"></i></a>
                        {% endif %}
                        {% if wiktionary %}
                            <a href="{{wiktionary}}" target="_blank" title="Wiktionary"><i class="pull-right fa fa-book fa-border" aria-hidden="true"></i></a>
                        {% endif %} 
                        </div>
                        {% if definition %}
                        <div class="col-md-12">
                        <p class="small text-muted">
                        {{definition}}
                        </p>
                        </div>
                        {% endif %}                        
                        {% if de or es or fi or fr %}
                        <div class="col-md-12">
                        <div class="row">  
                            {% if de %}
                                <div class="col-md-12">
                                <img src="theme/images/bglossary_blank.gif" class="flag flag-de" alt="German" /> <em>
                                {% if de is iterable and de is not string %}
                                    {{ de|join(', ') }}                                
                                {% else %}                                
                                    {{ de }}
                                {% endif %}
                                </em>
                                </div>      
                            {% endif %} 
                            {% if es %}
                                <div class="col-md-12">
                                <img src="theme/images/bglossary_blank.gif" class="flag flag-es" alt="Spain" /> <em>
                                {% if es is iterable and es is not string %}
                                    {{ es|join(', ') }}                                
                                {% else %}                                
                                    {{ es }}
                                {% endif %}
                                </em>
                                </div>      
                            {% endif %}                                                  
                            {% if fi %}
                                <div class="col-md-12">
                                <img src="theme/images/bglossary_blank.gif" class="flag flag-fi" alt="Finland" /> <em>
                                {% if fi is iterable and fi is not string %}
                                    {{ fi|join(', ') }}                                
                                {% else %}                                
                                    {{ fi }}
                                {% endif %}
                                </em>
                                </div>   
                            {% endif %}
                            {% if fr %}
                                <div class="col-md-12">
                                <img src="theme/images/bglossary_blank.gif" class="flag flag-fr" alt="France" /> <em>
                                {% if fr is iterable and fr is not string %}
                                    {{ fr|join(', ') }}                                
                                {% else %}                                
                                    {{ fr }}
                                {% endif %}
                                </em>
                                </div>   
                            {% endif %}
                            </div>  
                        </div>
                        {% endif %}
                    </div>
                </td>
            </tr>
        """,
        'list': """
            <div class="row list-group-item">
                <div class="col-xs-12">
                    <div class="row">
                        <div class="col-xs-10">
                            <h2 class="list-group-item-heading {{item_css}}">{{term}} {% if abbreviation -%}({{abbreviation}}){% endif %}</h2>
                        </div>
                        <div class="col-xs-2 item-icons">
                            {% if wikipedia %}
                                <a href="{{wikipedia}}" target="_blank" title="Wikipedia">
                                <i class="fa fa-wikipedia-w fa-border pull-right" aria-hidden="true"></i>
                                </a>
                            {% endif %}
                            {% if wiktionary %}
                                <a href="{{wiktionary}}" target="_blank" title="Wiktionary">
                                <i class="fa fa-book fa-border pull-right" aria-hidden="true"></i>
                                </a>
                            {% endif %}                            
                        </div>
                    </div>
                    <div class="row">                                                
                        <div class="col-md-12" style="padding-left:3em">
                            {% if definition %}
                            <p class="text-muted text-justify">
                            {{definition}}
                            </p>
                            {% endif %}
                            {% if intra_link %}                            
                            <p class="text-justify"><strong>See also:</strong> {{ intra_link }}</p>                              
                            {% endif %}                                                        
                            {% if de or es or fi or fr %}
                                <div class="row">  
                                {% if de %}
                                    <div class="col-md-12">
                                    <img src="theme/images/bglossary_blank.gif" class="flag flag-de" alt="German" /> <em>
                                    {% if de is iterable and de is not string %}
                                        {{ de|join(', ') }}                                
                                    {% else %}                                
                                        {{ de }}
                                    {% endif %}
                                    </em>
                                    </div>      
                                {% endif %} 
                                {% if es %}
                                    <div class="col-md-12">
                                    <img src="theme/images/bglossary_blank.gif" class="flag flag-es" alt="Spain" /> <em>
                                    {% if es is iterable and es is not string %}
                                        {{ es|join(', ') }}                                
                                    {% else %}                                
                                        {{ es }}
                                    {% endif %}
                                    </em>
                                    </div>      
                                {% endif %}                                                  
                                {% if fi %}
                                    <div class="col-md-12">
                                    <img src="theme/images/bglossary_blank.gif" class="flag flag-fi" alt="Finland" /> <em>
                                    {% if fi is iterable and fi is not string %}
                                        {{ fi|join(', ') }}                                
                                    {% else %}                                
                                        {{ fi }}
                                    {% endif %}
                                    </em>
                                    </div>   
                                {% endif %}
                                {% if fr %}
                                    <div class="col-md-12">
                                    <img src="theme/images/bglossary_blank.gif" class="flag flag-fr" alt="France" /> <em>
                                    {% if fr is iterable and fr is not string %}
                                        {{ fr|join(', ') }}                                
                                    {% else %}                                
                                        {{ fr }}
                                    {% endif %}
                                    </em>
                                    </div>   
                                {% endif %}
                                </div>  
                            {% endif %}                            
                        </div>
                    </div>
                </div>
            </div>
        """},
    'alphabet-template': {
        'panel': """<tr><td colspan="20"><h1 class="alphabet"><span class="label label-default">{{alphabet}}</span></h1></td></tr>""",
        'list': """<h1 class="alphabet"><span class="label label-default">{{alphabet}}</span></h1>"""
    },
    'data-source': None,
    'set': None,
    'show': False,
    'minified': True,
    'generate_minified': True,
    'template-variable': False,
    'show-dividers': True,
    'show-stats': True,
    'sort': False,
    'fields': '',
    'site-url': '',
    'debug_processing': False
}

bglossary_settings = copy.deepcopy(bglossary_default_settings)


def load_glossary_registry(source):
    """

    :param source: filename of the data file
    :return: glossary registry
    """

    if source and os.path.isfile(source):
        try:
            with open(source, 'r') as field:
                glossary_registry = yaml.load(field)

            from datetime import datetime
            modification_timestamp = os.path.getmtime(source)
            modification_date = datetime.utcfromtimestamp(modification_timestamp).strftime('%Y-%m-%d')

            if 'data' in glossary_registry:
                glossary_registry = glossary_registry['data']

            glossary_data = collections.OrderedDict()

            if 'glossary' in glossary_registry:
                for item in glossary_registry['glossary']:
                    for field in item:
                        if len(field) == 2:
                            if not isinstance(item[field], list):
                                item[field] = [x.strip() for x in item[field].split(',')]

                            field_list = []
                            for i in item[field]:
                                parts = [x.strip() for x in i.split(',')]
                                if len(parts) == 2:
                                    field_list.append('<a class="text" href="' + parts[1] + '">' + parts[0] + '</a>')
                                else:
                                    field_list.append(parts[0])

                            item[field] = field_list

                    if isinstance(item['term'], list):
                        item['term'] = ', '.join(item['term'])

                    key = item['term'].lower().replace(' ', '_')

                    if key not in glossary_data:
                        glossary_data[key] = item

                    else:
                        logger.warn(
                            '`pelican-bglossary` term [{term}] appears multiple times in the glossary.'.format(
                                term=item['term']
                            ))
                        glossary_data[key] = item

            return {
                'glossary': glossary_data,
                'modification_date': modification_date,
            }

        except ValueError:
            logger.warn('`pelican-bglossary` failed to load file [' + str(source) + ']')
            return False

    else:
        logger.warn('`pelican-bglossary` failed to load file [' + str(source) + ']')
        return False


def get_attribute(attrs, name, default=None):
    """
    Get div attribute
    :param attrs: attribute dict
    :param name: name field
    :param default: default value
    :return: value
    """

    if 'data-'+name in attrs:
        return attrs['data-'+name]
    else:
        return default


def generate_listing(settings):
    """
    Generate glossary listing

    :param settings: settings dict
    :return: html content
    """

    glossary_registry = load_glossary_registry(source=settings['data-source'])

    if glossary_registry and 'glossary' in glossary_registry and glossary_registry['glossary']:
        if 'sets' in glossary_registry and settings['set'] in glossary_registry['sets']:
            glossary = glossary_registry['sets'][settings['set']]

        else:
            glossary = glossary_registry['glossary']

        if settings['sort']:
            glossary = collections.OrderedDict(sorted(glossary.items()))

        logger.warn(
            '`pelican-bglossary` has [{term_count}] terms'.format(
                term_count=len(glossary)
            ))

        from flashtext import KeywordProcessor
        keyword_processor = KeywordProcessor()

        from textblob import TextBlob

        intra_links = {}
        for item_key, item in glossary.items():
            term = item.get('term', '')

            for t in term.split(','):
                t = t.strip()

                tt = TextBlob(t)
                if tt.tags[-1][1] == 'NN':
                    anchor = term.replace(' ', '-').lower()
                    if 'abbreviation' in item:
                        anchor += '-' + item.get('abbreviation', '').replace(' ', '-').lower()

                    words = list(tt.words)
                    words[-1] = tt.words[-1].pluralize()
                    t_plural = " ".join(words)

                    words = list(tt.words)
                    words[-1] = tt.words[-1].singularize()
                    t_singular = " ".join(words)

                    keyword_processor.add_keyword(
                        t_singular.lower(),
                        '<a href="#{anchor}">{term}</a>'.format(
                            anchor=anchor,
                            term=t_singular.lower()
                        )
                    )
                    keyword_processor.add_keyword(
                        t_plural.lower(),
                        '<a href="#{anchor}">{term}</a>'.format(
                            anchor=anchor,
                            term=t_plural.lower()
                        )
                    )

                if len(t.split(' ')) > 1:
                    anchor = term.replace(' ', '-').lower()
                    if 'abbreviation' in item:
                        anchor += '-' + item.get('abbreviation', '').replace(' ', '-').lower()

                    intra_links[term.lower()] = anchor

                    if 'abbreviation' in item:
                        intra_links[item.get('abbreviation', '').lower()] = anchor

                        keyword_processor.add_keyword(
                            t.lower(),
                            '<a href="#{anchor}">{term}</a>'.format(
                                anchor=anchor,
                                term=item.get('abbreviation')
                            )
                        )

                    keyword_processor.add_keyword(
                        t.lower(),
                        '<a href="#{anchor}">{term}</a>'.format(
                            anchor=anchor,
                            term=t
                        )
                    )

        for item_key, item in glossary.items():
            term = item.get('term', '')

            for t in term.split(','):
                if len(t.split(' ')) == 1:
                    anchor = term.replace(' ', '-').lower()
                    if 'abbreviation' in item:
                        anchor += '-' + item.get('abbreviation', '').replace(' ', '-').lower()

                    intra_links[term.lower()] = anchor

                    if 'abbreviation' in item:
                        intra_links[item.get('abbreviation', '').lower()] = anchor

                        keyword_processor.add_keyword(
                            t.lower(),
                            '<a href="#{anchor}">{term}</a>'.format(
                                anchor=anchor,
                                term=item.get('abbreviation')
                            )
                        )

                    keyword_processor.add_keyword(
                        t.lower(),
                        '<a href="#{anchor}">{term}</a>'.format(
                            anchor=anchor,
                            term=t
                        )
                    )

        html = "\n"
        alphabet_header_template = Template(settings['alphabet-template'][settings['mode']].strip('\t\r\n').replace('&gt;', '>').replace('&lt;', '<'))

        current_letter = None
        term_count = 0
        translation_counts = {}
        active_translations = []
        for field in settings['fields']:
            if len(field) == 2:
                active_translations.append(field)
        for glossary_key, glossary_item in glossary.items():
            if current_letter != glossary_item['term'][0].upper():
                if settings['show-dividers']:
                    html += alphabet_header_template.render(alphabet=glossary_item['term'][0].upper())

                current_letter = glossary_item['term'][0].upper()

            if 'definition' in glossary_item:

                glossary_item['definition'] = keyword_processor.replace_keywords(glossary_item['definition'])

            if 'intra_link' in glossary_item:
                glossary_item['intra_link'] = keyword_processor.replace_keywords(glossary_item['intra_link'])

            html += generate_listing_item(
                glossary_item=glossary_item,
                settings=settings,
            ) + "\n"

            term_count += 1

            for lang in active_translations:
                if lang in glossary_item and glossary_item[lang]:
                    if lang not in translation_counts:
                        translation_counts[lang] = 0
                    translation_counts[lang] += 1

        html += "\n"

        template = Template(settings['template'][settings['mode']].strip('\t\r\n').replace('&gt;', '>').replace('&lt;', '<'))

        return BeautifulSoup(
            template.render(
                list=html,
                header=settings.get('header'),
                site_url=settings.get('site-url'),
                panel_color=settings.get('panel-color'),
                show_stats=settings.get('show-stats'),
                latest_update=glossary_registry['modification_date'],
                term_count=term_count,
                translation_counts=translation_counts
            ), "html.parser"
        )

    else:
        return ''


def generate_listing_item(glossary_item, settings, main_highlight=False):
    """

    Generate glossary in listing

    :param glossary_item: glossary data
    :param settings: settings dict
    :return: html content
    """

    if main_highlight:
        if settings['mode'] == 'panel':
            if 'main' in glossary_item and glossary_item['main']:
                item_css = 'active'
            else:
                item_css = ''

        else:
            if 'main' in glossary_item and glossary_item['main']:
                item_css = ''
            else:
                item_css = 'text-muted'

    else:
        item_css = ''

    valid_fields = [u'term', u'abbreviation', u'definition']  # default fields
    valid_fields += settings['fields']          # user defined fields

    filtered_fields = {}
    for field in glossary_item:
        if field in valid_fields:
            filtered_fields[field] = glossary_item[field]
        else:
            filtered_fields[field] = None

    template = Template(settings['item-template'][settings['mode']].strip('\t\r\n').replace('&gt;', '>').replace('&lt;', '<'))
    filtered_fields['site_url'] = settings['site-url']
    filtered_fields['item_css'] = item_css

    html = BeautifulSoup(template.render(**filtered_fields), "html.parser")
    return html.decode()


def bglossary(content):
    """
    Main processing

    """
    global bglossary_settings

    if isinstance(content, contents.Static):
        return

    soup = BeautifulSoup(content._content, 'html.parser')

    # Template variable
    if bglossary_settings['template-variable']:
        # We have page variable set
        bglossary_settings['show'] = True
        div_html = generate_listing(settings=bglossary_settings)

        if div_html:
            content.bglossary = div_html.decode()

    else:
        content.bglossary = None

    # bglossary divs
    bglossary_divs = soup.find_all('div', class_='bglossary')

    if bglossary_divs:
        if bglossary_settings['debug_processing']:
            logger.debug(msg='[{plugin_name}] title:[{title}] divs:[{div_count}]'.format(
                plugin_name='bglossary',
                title=content.title,
                div_count=len(bglossary_divs)
            ))

        bglossary_settings['show'] = True

        for bglossary_div in bglossary_divs:
            # We have div in the page
            settings = copy.deepcopy(bglossary_settings)
            settings['data-source'] = get_attribute(bglossary_div.attrs, 'source', bglossary_settings['data-source'])
            settings['set'] = get_attribute(bglossary_div.attrs, 'set', bglossary_settings['set'])
            settings['template'] = get_attribute(bglossary_div.attrs, 'template', bglossary_settings['template'])
            settings['item-template'] = get_attribute(bglossary_div.attrs, 'item-template', bglossary_settings['item-template'])
            settings['mode'] = get_attribute(bglossary_div.attrs, 'mode', bglossary_settings['mode'])
            settings['header'] = get_attribute(bglossary_div.attrs, 'header', bglossary_settings['header'])
            settings['panel-color'] = get_attribute(bglossary_div.attrs, 'panel-color', bglossary_settings['panel-color'])
            settings['fields'] = get_attribute(bglossary_div.attrs, 'fields', bglossary_settings['fields'])
            settings['show-dividers'] = get_attribute(bglossary_div.attrs, 'show-dividers', bglossary_settings['show-dividers']) in ['True', 'true']
            settings['show-stats'] = get_attribute(bglossary_div.attrs, 'show-stats', bglossary_settings['show-stats']) in ['True', 'true']

            if isinstance(settings['fields'], str):
                settings['fields'] = [x.strip() for x in settings['fields'].split(',')]

            if not isinstance(settings['fields'], list):
                settings['fields'] = [x.strip() for x in settings['fields'].split(',')]

            settings['sort'] = get_attribute(bglossary_div.attrs, 'sort', bglossary_settings['sort'])

            if settings['sort'] == 'True' or settings['sort'] == 'true':
                settings['sort'] = True

            else:
                settings['sort'] = False

            div_html = generate_listing(settings=settings)

            if div_html:
                bglossary_div.replaceWith(div_html)

    if bglossary_settings['show']:

        if bglossary_settings['minified']:
            html_elements = {
                'css_include': ['<link rel="stylesheet" href="' + bglossary_settings['site-url'] + '/theme/css/bglossary.min.css">']
            }

        else:
            html_elements = {
                'css_include': ['<link rel="stylesheet" href="' + bglossary_settings['site-url'] + '/theme/css/bglossary.css">']
            }

        if u'scripts' not in content.metadata:
            content.metadata[u'scripts'] = []

        if u'styles' not in content.metadata:
            content.metadata[u'styles'] = []

        for element in html_elements['css_include']:
            if element not in content.metadata[u'styles']:
                content.metadata[u'styles'].append(element)

    content._content = soup.decode()


def process_page_metadata(generator, metadata):
    """
    Process page metadata

    """
    global bglossary_default_settings, bglossary_settings
    bglossary_settings = copy.deepcopy(bglossary_default_settings)

    if u'bglossary' in metadata and (metadata['bglossary'] == 'True' or metadata['bglossary'] == 'true'):
        bglossary_settings['show'] = True
        bglossary_settings['template-variable'] = True
    else:
        bglossary_settings['show'] = False
        bglossary_settings['template-variable'] = False

    if u'bglossary_source' in metadata:
        bglossary_settings['data-source'] = metadata['bglossary_source']

    if u'bglossary_set' in metadata:
        bglossary_settings['set'] = metadata['bglossary_set']

    if u'bglossary_mode' in metadata:
        bglossary_settings['mode'] = metadata['bglossary_mode']

    if u'bglossary_panel_color' in metadata:
        bglossary_settings['panel-color'] = metadata['bglossary_panel_color']

    if u'bglossary_header' in metadata:
        bglossary_settings['header'] = metadata['bglossary_header']

    if u'bglossary_fields' in metadata:
        bglossary_settings['fields'] = metadata['bglossary_fields']
        bglossary_settings['fields'] = [x.strip() for x in bglossary_settings['fields'].split(',')]

    if u'bglossary_sort' in metadata and (metadata['bglossary_sort'] == 'True' or metadata['bglossary_sort'] == 'true'):
        bglossary_settings['sort'] = True


def init_default_config(pelican):
    """
    Handle settings from pelicanconf.py

    """
    global bglossary_default_settings, bglossary_settings

    bglossary_default_settings['site-url'] = pelican.settings['SITEURL']

    if 'BGLOSSARY_SOURCE' in pelican.settings:
        bglossary_default_settings['data-source'] = pelican.settings['BGLOSSARY_SOURCE']

    if 'BGLOSSARY_TEMPLATE' in pelican.settings:
        bglossary_default_settings['template'].update(pelican.settings['BGLOSSARY_TEMPLATE'])

    if 'BGLOSSARY_ITEM_TEMPLATE' in pelican.settings:
        bglossary_default_settings['item-template'].update(pelican.settings['BGLOSSARY_ITEM_TEMPLATE'])

    if 'BGLOSSARY_HEADER' in pelican.settings:
        bglossary_default_settings['header'] = pelican.settings['BGLOSSARY_HEADER']

    if 'BGLOSSARY_PANEL_COLOR' in pelican.settings:
        bglossary_default_settings['panel-color'] = pelican.settings['BGLOSSARY_PANEL_COLOR']

    if 'BGLOSSARY_MINIFIED' in pelican.settings:
        bglossary_default_settings['minified'] = pelican.settings['BGLOSSARY_MINIFIED']

    if 'BGLOSSARY_GENERATE_MINIFIED' in pelican.settings:
        bglossary_default_settings['generate_minified'] = pelican.settings['BGLOSSARY_GENERATE_MINIFIED']

    if 'BGLOSSARY_SORT' in pelican.settings:
        bglossary_default_settings['sort'] = pelican.settings['BGLOSSARY_SORT']

    if 'BGLOSSARY_DEBUG_PROCESSING' in pelican.settings:
        bglossary_default_settings['debug_processing'] = pelican.settings['BGLOSSARY_DEBUG_PROCESSING']

    bglossary_settings = copy.deepcopy(bglossary_default_settings)


def move_resources(gen):
    """
    Move files from css folders to output folder, use minified files.

    """

    plugin_paths = gen.settings['PLUGIN_PATHS']

    if bglossary_settings['minified']:
        if bglossary_settings['generate_minified']:
            minify_css_directory(gen=gen, source='css', target='css.min')

        css_target = os.path.join(gen.output_path, 'theme', 'css', 'bglossary.min.css')

        if not os.path.exists(os.path.join(gen.output_path, 'theme', 'css')):
            os.makedirs(os.path.join(gen.output_path, 'theme', 'css'))

        for path in plugin_paths:
            css_source = os.path.join(path, 'pelican-bglossary', 'css.min', 'bglossary.min.css')
            if os.path.isfile(css_source):
                shutil.copyfile(css_source, css_target)

            if os.path.isfile(css_target):
                break
    else:
        css_target = os.path.join(gen.output_path, 'theme', 'css', 'bglossary.css')

        if not os.path.exists(os.path.join(gen.output_path, 'theme', 'css')):
            os.makedirs(os.path.join(gen.output_path, 'theme', 'css'))

        for path in plugin_paths:
            css_source = os.path.join(path, 'pelican-bglossary', 'css', 'bglossary.css')

            if os.path.isfile(css_source):
                shutil.copyfile(css_source, css_target)

            if os.path.isfile(css_target):
                break

    img_target_flags = os.path.join(gen.output_path, 'theme', 'images', 'bglossary_flags.png')
    img_target_blank = os.path.join(gen.output_path, 'theme', 'images', 'bglossary_blank.gif')

    if not os.path.exists(os.path.join(gen.output_path, 'theme', 'images')):
        os.makedirs(os.path.join(gen.output_path, 'theme', 'images'))

    for path in plugin_paths:
        img_source_flags = os.path.join(path, 'pelican-bglossary', 'images', 'bglossary_flags.png')
        img_source_blank = os.path.join(path, 'pelican-bglossary', 'images', 'bglossary_blank.gif')
        if os.path.isfile(img_source_flags):
            shutil.copyfile(img_source_flags, img_target_flags)

        if os.path.isfile(img_source_blank):
            shutil.copyfile(img_source_blank, img_target_blank)

        if os.path.isfile(img_target_flags) and os.path.isfile(img_target_blank):
            break


def minify_css_directory(gen, source, target):
    """
    Move CSS resources from source directory to target directory and minify. Using rcssmin.

    """

    import rcssmin

    plugin_paths = gen.settings['PLUGIN_PATHS']
    for path in plugin_paths:
        source_ = os.path.join(path, 'pelican-bglossary', source)
        target_ = os.path.join(path, 'pelican-bglossary', target)
        if os.path.isdir(source_):
            if not os.path.exists(target_):
                os.makedirs(target_)

            for root, dirs, files in os.walk(source_):
                for current_file in files:
                    if current_file.endswith(".css"):
                        current_file_path = os.path.join(root, current_file)
                        with open(current_file_path) as css_file:
                            with open(os.path.join(target_, current_file.replace('.css', '.min.css')), "w") as minified_file:
                                minified_file.write(rcssmin.cssmin(css_file.read(), keep_bang_comments=True))


def register():
    """
    Register signals

    """

    signals.initialized.connect(init_default_config)
    signals.article_generator_context.connect(process_page_metadata)
    signals.page_generator_context.connect(process_page_metadata)
    signals.article_generator_finalized.connect(move_resources)

    signals.content_object_init.connect(bglossary)
