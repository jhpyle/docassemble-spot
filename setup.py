import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = ('.*', 'CVS', '_darcs', './build', './dist', 'EGG-INFO', '*.egg-info')
def find_package_data(where='.', package='', exclude=standard_exclude, exclude_directories=standard_exclude_directories):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                        or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out

setup(name='docassemble.spot',
      version='0.0.3',
      description=('Provides a datatype for legal issue spotting using the Spot API.'),
      long_description="This package provides a `datatype` for mapping descriptions of legal problems\r\nto [NSMIv2] categories.  It uses the [Spot API] developed by the\r\n[The Legal Innovation & Technology Lab] at [Suffolk Law School].\r\n\r\nThis package requires **docassemble** version 0.5.86 or later.\r\n\r\nTo use package, first [obtain an API key] for the [Spot API].\r\n\r\nThen put that API key into your [Configuration]:\r\n\r\n```\r\nspot api key: abbaabba1234abbaabba1234abbaabba1234abbaabba1234abbaabba\r\n```\r\n\r\nThen you can use `spot` as a `datatype`.  For example:\r\n\r\n```\r\nquestion: |\r\n  What is your legal issue?\r\nfields:\r\n  - no label: legal_issue\r\n    input type: area\r\n    datatype: spot\r\n---\r\nmandatory: True\r\nquestion: |\r\n  % if legal_issue.result == 'Housing':\r\n  We can help you with that housing issue.\r\n  % else:\r\n  Sorry, we don't help with that.\r\n  % endif\r\n```\r\n\r\nIn this example, the variable `legal_issue` will become an object of type\r\n`SpotResult`.  This is a subclass of `DAObject`.  The user's original text is\r\navailable at `legal_issue.source`.  The result is available at `legal_issue.result`.\r\nWhen reduced to text, a `SpotResult` object returns `legal_issue.result`.  If the \r\nlegal issue cannot not be determined, `legal_issue` will be `None` and an error\r\nmessage will be written to the logs.  The [NSMIv2] code is available under `legal_issue.id`.\r\n\r\nOnly the first result is used for the `.result` and `.id` attributes.  If you \r\nwant to inspect into the actual result returned by the API, you can find it \r\nunder `legal_issue._full_result`.\r\n\r\n[Spot API]: https://spot.suffolklitlab.org/\r\n[Configuration]: https://docassemble.org/docs/config.html\r\n[obtain an API key]: https://spot.suffolklitlab.org/user/new/\r\n[The Legal Innovation & Technology Lab]: https://suffolklitlab.org/\r\n[Suffolk Law School]: https://www.suffolk.edu/law\r\n[NSMIv2]: http://betterinternet.law.stanford.edu/about-the-project/legal-issues-taxonomy-nsmiv2/",
      long_description_content_type='text/markdown',
      author='Jonathan Pyle',
      author_email='jhpyle@gmail.com',
      license='The MIT License (MIT)',
      url='https://docassemble.org',
      packages=find_packages(),
      namespace_packages=['docassemble'],
      install_requires=[],
      zip_safe=False,
      package_data=find_package_data(where='docassemble/spot/', package='docassemble.spot'),
     )

