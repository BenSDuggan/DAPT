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


To clean up after a release:

1. Navigate to the misc folder ``cd misc``
2. Make the ``clean_after_release.sh`` script runnable (``chmod + clean_after_release.sh``)
3. Run the script (``./clean_after_release.sh``)