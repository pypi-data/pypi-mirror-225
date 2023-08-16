from setuptools import setup,find_packages

setup(
    name='IPtool',        # Change this to your project's name
    version='1.0.0',          # Change this to your project's version
    description='IP analysis tool',  # Change this to your project's description
    author='ibrahem shreif',       # Change this to your name
    author_email='ibrahemelhw@gmail.com',   # Change this to your email
    url='https://github.com/MRIiiIiIiI/IPAnalyzer',  # Change this to your project's repository URL

    packages=find_packages(),            # Add the package name(s) if your project has packages
    install_requires=['art','time'],      # Add any project dependencies here

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
