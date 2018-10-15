Pelican-bglossary - Glossary for Pelican
========================================

`pelican-bglossary` is an open source Pelican plugin to produce glossary from yaml data structure. The plugin is developed to be used with Markdown content and Bootstrap 3 based template. 

**Author**

Toni Heittola (toni.heittola@gmail.com), [GitHub](https://github.com/toni-heittola), [Home page](http://www.cs.tut.fi/~heittolt/)

Installation instructions
=========================

## Requirements

**bs4** and **flashtext** are required. To ensure that all external modules are installed, run:

    pip install -r requirements.txt

**bs4** (BeautifulSoup) for parsing HTML content

    pip install beautifulsoup4

## Pelican installation

Make sure you include [Bootstrap](http://getbootstrap.com/) in your template.

Make sure the directory where the plugin was installed is set in `pelicanconf.py`. For example if you installed in `plugins/pelican-bglossary`, add:

    PLUGIN_PATHS = ['plugins']

Enable `pelican-bglossary` with:

    PLUGINS = ['pelican-bglossary']

Insert glossary list or panel into the page template:
 
    {% if page.bglossary %}
        {{ page.bglossary }}
    {% endif %}

Insert glossary list or panel into the article template:

    {% if article.bglossary %}
        {{ article.bglossary }}
    {% endif %}

Usage
=====

Glossary generation is triggered for the page either by setting BGLOSSARY metadata for the content (page or article) or using `<div>` with class `bglossary`.

Layouts

- **bglossary**, full glossary  

There is two layout modes available: `panel` and `list`.

## Glossary registry

Registry has two parts: 
    - **`glossary`** containing information of each item in glossary

Example yaml-file:

    glossary:
      - term: supervised learning
        definition: learning method which learns from labeled examples
        fi: ohjattu oppiminen
        de: Überwachtes Lernen
        es: aprendizaje supervisado
        fr: apprentissage supervisé
        wikipedia: https://en.wikipedia.org/wiki/Supervised_learning
        intra_link: unsupervised learning

      - term: unsupervised learning
        definition: machine learning technique to learn from unlabeled data
        fi: ohjaamaton oppiminen
        de: Unüberwachtes Lernen
        es: aprendizaje no supervisado
        fr: apprentissage non supervisé
        wikipedia: https://en.wikipedia.org/wiki/Unsupervised_learning
        intra_link: supervised learning

The default templates support following fields:

- term
- definition
- translation fields: `fi`, `de`,  `es`, and  `fr`
- wikipedia
- wiktionary
- intra_link, cross linking between terms

## Parameters

The parameters can be set in global, and content level. Globally set parameters are are first overwritten content meta data, and finally with div parameters.

### Global parameters

Parameters for the plugin can be set in `pelicanconf.py' with following parameters:

| Parameter                 | Type      | Default       | Description  |
|---------------------------|-----------|---------------|--------------|
| BGLOSSARY_SOURCE         | String    |  | YAML-file to contain glossary registry, see example format above. |
| BGLOSSARY_TEMPLATE       | Dict of Jinja2 templates |  | Two templates can be set for panel and list  |
| BGLOSSARY_ITEM_TEMPLATE  | Dict of Jinja2 templates |  | Two templates can be set for panel and list  |
| BGLOSSARY_PANEL_COLOR          | String    | panel-primary |  CSS class used to color the panel template in the default template. Possible values: panel-default, panel-primary, panel-success, panel-info, panel-warning, panel-danger |
| BGLOSSARY_HEADER               | String    | Content       | Header text  |
| BGLOSSARY_SORT              | Boolean    | False       | Sorting of the listing based on term  |
| BGLOSSARY_DEBUG_PROCESSING | Boolean    | False  | Show extra information in when run with `DEBUG=1` |

### Content wise parameters

| Parameter                 | Example value     | Description  |
|---------------------------|-----------|--------------|
| BGLOSSARY                | True      | Enable bglossary listing for the page |
| BGLOSSARY_SOURCE         | content/data/glossary.yaml | Personnel registry file |
| BGLOSSARY_MODE           | panel | Layout type, panel or list |
| BGLOSSARY_PANEL_COLOR    | panel-info | CSS class used to color the panel template in the default template. Possible values: panel-default, panel-primary, panel-success, panel-info, panel-warning, panel-danger |
| BGLOSSARY_HEADER         | Personnel | Header text  |
| BGLOSSARY_FIELDS         | email, photo, affiliation | comma separated list of field to be shown |
| BGLOSSARY_SORT        | True | Sorting of the listing based on term |

Example:

    Title: Test page
    Date: 2017-01-05 10:20
    Category: test
    Slug: test-page
    Author: Test Person
    bglossary: True
    bglossary_header: Glossary
    bglossary_fields: wikipedia, wiktionary, fi, fr, es, intra_link
    
Personnel listing is available in template in variable `page.bglossary` or `article.bglossary`
   
### Div wise parameters

Valid for `<div>` class `bglossary`:

| Parameter                 | Example value     | Description  |
|---------------------------|-------------|--------------|
| data-source               | content/data/glossary.yaml | Glossary registry file
| data-mode                 | panel       | Layout type, panel or list |
| data-header               | Glossary   | Header text |
| data-panel-color          | panel-info | CSS class used to color the panel template in the default template. Possible values: panel-default, panel-primary, panel-success, panel-info, panel-warning, panel-danger |
| data-fields               | email, photo, affiliation | comma separated list of field to be shown |
| data-sort                 | True | Sorting of the listing based on term |

Example listing:

    <div class="bglossary" data-source="content/data/glossary.yaml" data-set="set1" data-fields="wikipedia, wiktionary, de, fi, fr, es, intra_link"></div>
