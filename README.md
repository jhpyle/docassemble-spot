This package provides a `datatype` for mapping descriptions of legal problems
to [NSMIv2] categories.  It uses the [Spot API] developed by the
[The Legal Innovation & Technology Lab] at [Suffolk Law School].

This package requires **docassemble** version 0.5.86 or later.

To use package, first [obtain an API key] for the [Spot API].

Then put that API key into your [Configuration]:

```
spot api key: abbaabba1234abbaabba1234abbaabba1234abbaabba1234abbaabba
```

Then you can use `spot` as a `datatype`.  For example:

```
question: |
  What is your legal issue?
fields:
  - no label: legal_issue
    input type: area
    datatype: spot
---
mandatory: True
question: |
  % if legal_issue.result == 'Housing':
  We can help you with that housing issue.
  % else:
  Sorry, we don't help with that.
  % endif
```

In this example, the variable `legal_issue` will become an object of type
`SpotResult`.  This is a subclass of `DAObject`.  The user's original text is
available at `legal_issue.source`.  The result is available at `legal_issue.result`.
When reduced to text, a `SpotResult` object returns `legal_issue.result`.  If the 
legal issue cannot not be determined, `legal_issue` will be `None` and an error
message will be written to the logs.  The [NSMIv2] code is available under `legal_issue.id`.

Only the first result is used for the `.result` and `.id` attributes.  If you 
want to inspect into the actual result returned by the API, you can find it 
under `legal_issue._full_result`.

[Spot API]: https://spot.suffolklitlab.org/
[Configuration]: https://docassemble.org/docs/config.html
[obtain an API key]: https://spot.suffolklitlab.org/user/new/
[The Legal Innovation & Technology Lab]: https://suffolklitlab.org/
[Suffolk Law School]: https://www.suffolk.edu/law
[NSMIv2]: http://betterinternet.law.stanford.edu/about-the-project/legal-issues-taxonomy-nsmiv2/