import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install

# Optional: Define any post-installation actions if necessary
def _post_install_actions():
    pass  # Here you can put any post-installation logic

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        _post_install_actions()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        _post_install_actions()

# Read the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define your project's dependencies
install_requires = [
    'numpy',
    'pandas',
    # Add other dependencies as needed
]

setuptools.setup(
    name="YourFrameworkName",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A brief description of your framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://yourframeworkhomepage.com",
    project_urls={
        "Bug Tracker": "https://yourframeworkhomepage.com/issues",
    },
    install_requires=install_requires,
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'yourframeworkkeyword=your_package.main_module:main_function',
        ],
    },
    python_requires=">=3.6",
)

