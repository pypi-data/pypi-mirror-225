# MediaWikiTitleParser

![Tests](https://github.com/NguoiDungKhongDinhDanh/mwtp/actions/workflows/tests.yaml/badge.svg)
![License](https://img.shields.io/pypi/l/mwtp.svg)
![Supported versions](https://img.shields.io/pypi/pyversions/mwtp.svg)

MWTP is a parser for MediaWiki titles. Its logic is partly derived from
[mediawiki.Title][1], and hence is licensed under GNU GPL.

It works as simple as follows:

```python
from mwtp import TitleParser as Parser


parser = Parser(namespaces_data, namespace_aliases)
title = parser.parse(' _ FoO: this/is A__/talk page _ ')

print(repr(title))
# Title('Thảo luận:This/is A /talk page')
```

`namespaces_data` and `namespace_aliases` can be queried directly from [a wiki's
API][2] using `action=query&meta=siteinfo&siprop=namespaces|namespacealiases`:

```python
namespaces_data = {
  '0': {
    'id': 0,
    'case': 'first-letter',
    'name': '',
    'subpages': False,
    'content': True,
    'nonincludable': False
  },
  '1': {
    'id': 1,
    'case': 'first-letter',
    'name': 'Thảo luận',
    'subpages': True,
    'canonical': 'Talk',
    'content': False,
    'nonincludable': False
  },
  ...: ...
}
```

```python
namespace_aliases = [
  { 'id': 1, 'alias': 'Foo' },
  ...
]
```

[1]: https://github.com/wikimedia/mediawiki/tree/c237f0548845662759bfcc6419cec9ca02d03c18/resources/src/mediawiki.Title
[2]: https://www.mediawiki.org/wiki/Special:ApiSandbox#action=query&meta=siteinfo&siprop=namespaces%7Cnamespacealiases
