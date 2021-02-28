.. _updates:

Updates
=======

Guide for pushing updates
-------------------------

0. Install requirements by running ``pip install twine``
1. Test the code locally be running ``pip install .`` in the root directory.
2. Update the version in `setup.py </setup.py>`_ file.
3. Run ``python3 setup.py sdist bdist_wheel``.
4. Run ``twine upload dist/*``.


New way:

1. ``python3 -m pip install --upgrade build``
2. ``python3 -m build``
3. ``python3 -m pip install --upgrade twine``
4a. ``python3 -m twine upload --repository testpypi dist/*`` uploads to test
4b. ``twine upload dist/*`` uploads to production
5a. ``python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-pkg-YOUR-USERNAME-HERE`` to install from test
5b. ``python3 -m pip install dapt`` to install from production


To clean up after a release:

1. Navigate to the misc folder ``cd misc``
2. Make the ``clean_after_release.sh`` script runnable (``chmod + clean_after_release.sh``)
3. Run the script (``./clean_after_release.sh``)