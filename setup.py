from distutils.core import setup
from pathlib import Path
project_dir = Path(__file__).parent


setup(
    name='govcrawl',
    packages=['govcrawl'],
    version='0.0.1',
    license='BSD 2-clause "Simplified" license',
    long_description=(project_dir / 'README.md').read_text(),
    long_description_content_type="text/markdown",
    author='YOUR NAME',
    author_email='yuhang.tao.email@gmail.com',
    url='https://github.com/TITC/gov_crawler',
    keywords=['crawler', 'document'],
    install_requires=['beautifulsoup4',
                      'handytools == 0.0.5.4',
                      'numpy == 1.22.4',
                      'pandas == 1.4.2',
                      'streamlit == 1.10.0',
                      'textract == 1.6.5',
                      'tqdm == 4.64.0'],
    classifiers=[
        'License :: OSI Approved :: BSD 2-clause "Simplified" license',
        'Programming Language :: Python :: 3.8.8',
    ],
)
