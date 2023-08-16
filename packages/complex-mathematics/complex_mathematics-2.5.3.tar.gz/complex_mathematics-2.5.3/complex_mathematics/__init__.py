# To update: update setup.py, follow version rules and remember to include necessary packages

# After that, run this: python setup.py sdist bdist_wheel

# Then this: twine upload dist/*

#MAJOR version: This number is incremented when backward-incompatible changes are introduced. This means that the new version might not be compatible with previous versions, and existing code that relies on the older version might break when using the new one.

#MINOR version: This number is incremented when backward-compatible features or enhancements are added. Existing code should continue to work as expected when upgrading to a higher minor version.

#PATCH version: This number is incremented for backward-compatible bug fixes or minor improvements. It indicates that the changes are limited to fixing issues without introducing new features or breaking changes.

#The version numbers are represented in the format MAJOR.MINOR.PATCH, where each component is a non-negative integer. For example, 1.2.3 indicates MAJOR version 1, MINOR version 2, and PATCH version 3.

#According to semantic versioning, developers should follow these rules:

#When making backward-incompatible changes (e.g., API changes that break existing code), increment the MAJOR version.

#When adding new features in a backward-compatible manner, increment the MINOR version.

#When making backward-compatible bug fixes or minor improvements, increment the PATCH version.

#Additional labels like pre-release or build metadata (e.g., 1.2.3-alpha, 1.2.3+build42) can be appended to the version for more specific versioning needs.