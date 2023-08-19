## Version 0.5.1 - _2023-08-18_

* Remove unneeded files from being packaged in the wheel
* Fix syntax highlighting in dark mode

## Version 0.5.0 - _2023-06-27_

* Drop compatibility with python 3.6 and 3.7.
* Add compatibility with python 3.11.
* Update bootstrap to 5.3.0.
* Switch build to hatchling instead of setuptools.
* Add dark mode, selected by the preferred color scheme.

## Version 0.4.3 - _2022-04-21_

* Do not print the menu bar and the alerts, only the page content.
* Show the URL of outside links in print media.
* Update bootstrap to 5.1.3.
* Drop compatibility with python 3.5.

## Version 0.4.2 - _2021-10-06_

* Add compatibility with python 3.10.
* Update bootstrap to 5.1.2.

## Version 0.4.1 - _2021-06-03_

* Fix: use the non-emoji version of unicode symbol for external links,
  tasklist marks and backreference links.

## Version 0.4.0 - _2021-05-20_

* Update bootstrap to 5.0.1.
* Remove jquery: not needed by bootstrap anymore.
* Update autosize to 5.0.0.

## Version 0.3.3 - _2021-02-05_

* Update bootstrap to 4.6.0.
* Add compatibility with python 3.9.

## Version 0.3.2 - _2021-01-09_

* Use a safer method to write files to prevent data loss.
* Make the editor tab-friendly by reorganizing the buttons.

## Version 0.3.1 - _2020-10-31_

* Fix: bootstrap and jquery versions in README and about page.
* Fix: correctly use static content when hosted outside of the app.
* Update bootstrap to 4.5.3.

## Version 0.3.0 - _2020-07-27_

* Update bootstrap to 4.5.0 and jquery to 3.5.1.
* Fix: Make sure the browser does not use stall data after an application
  update.
* Fix: Indicate the minimum version of requirements in setup.py.
* Switch to _importlib_ instead of _pkg_resources_ to access the package data.
  Drop _setuptools_ requirements.

## Version 0.2.0 - _2020-05-08_

* Remove a few markdown extensions for faster rendering: Symbols tranformations
  (_smartypants_) and inline highlighting.

## Version 0.1.1 - _2020-05-03_

* Fix version displayed in about page

## Version 0.1.0 - _2020-05-01_

* First release
