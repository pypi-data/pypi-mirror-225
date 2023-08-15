from setuptools import setup, find_packages
import codecs
import os
# 
here = os.path.abspath(os.path.dirname(__file__))
# 
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()\

from pathlib import Path
this_directory = Path(__file__).parent
#long_description = (this_directory / "README.md").read_text()

VERSION = '''0.10'''
DESCRIPTION = '''Some image augmentation tools for yolov5'''

# Setting up
setup(
    name="tools4yolo",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/tools4yolo',
    author="Johannes Fischer",
    author_email="aulasparticularesdealemaosp@gmail.com",
    description=DESCRIPTION,
long_description = long_description,
long_description_content_type="text/markdown",
    #packages=['PILasOPENCV', 'Pillow', 'a_cv2_easy_resize', 'a_cv_imwrite_imread_plus', 'deepcopyall', 'fast_color_checker', 'flatten_any_dict_iterable_or_whatsoever', 'get_rectangle_infos', 'getpartofimg', 'list_all_files_recursively', 'numexpr', 'numpy', 'opencv_python', 'opencv_python_headless', 'pandas', 'regex', 'rembg', 'scikit_learn', 'torch'],
    keywords=['image', 'augmentation', 'yolov5'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['PILasOPENCV', 'Pillow', 'a_cv2_easy_resize', 'a_cv_imwrite_imread_plus', 'deepcopyall', 'fast_color_checker', 'flatten_any_dict_iterable_or_whatsoever', 'get_rectangle_infos', 'getpartofimg', 'list_all_files_recursively', 'numexpr', 'numpy', 'opencv_python', 'opencv_python_headless', 'pandas', 'regex', 'rembg', 'scikit_learn', 'torch'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*