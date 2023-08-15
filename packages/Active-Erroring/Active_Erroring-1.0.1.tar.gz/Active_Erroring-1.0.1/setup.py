from setuptools import setup

setup(
    name='Active_Erroring',  # * Your package will have this name
    packages=['active_erroring'],  # import this_name
    version='1.0.1',  # * To be increased every time your change your library
    license='MIT',  # Type of license. More here: https://help.github.com/articles/licensing-a-repository
    description='This package can be used to raise custom errors and have fun.',
    # Short description of your library
    author='Armen-Jean Andreasian',  # Your name
    author_email='armen.andreasian77@gmail.com',  # Your email
    url='https://example.com',  # Homepage of your library (e.g. github or your website)
    keywords=['active_erroring', 'raising', 'custom', 'python'],  # Keywords users can search on pypi.org
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Who is the audience for your library?
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Type a license again
        'Programming Language :: Python :: 3.8',  # Python versions that your library supports
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
