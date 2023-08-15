import setuptools

# used by python -m build
setuptools.setup(
    name='database-without-orm-local',
    version='0.0.33',  # https://pypi.org/project/database-without-orm-local/
    author="Circles",
    author_email="info@circles.life",
    description="Circles Local Database without ORM Python PyPI Package",
    long_description="This is a package for sharing common Database methods",
    long_description_content_type="text/markdown",
    url="https://github.com/javatechy/dokr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: Other/Proprietary License",
         "Operating System :: OS Independent",
    ],
)
