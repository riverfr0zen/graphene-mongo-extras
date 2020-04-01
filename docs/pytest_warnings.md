# Ignoring deprecation warnings in tests

At time of writing some dependencies are causing Deprecation warnings. These can be suppressed when running pytest as follows: 

`pytest -W ignore::DeprecationWarning`
