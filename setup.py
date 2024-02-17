from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import platform


def _post_install():
    """
    Provide instructions for setting environment variables post-installation.
    Tailors instructions based on the user's operating system.
    """
    godsight_home_instruction = ("Please set the GODSIGHT_HOME environment variable to point to your GodSight "
                                 "installation directory.")

    if platform.system() == "Windows":
        print(f"{godsight_home_instruction} On Windows, you can do this by running:\n")
        print('setx GODSIGHT_HOME "C:\\path\\to\\GodSight"\n')
        print("Replace 'C:\\path\\to\\GodSight' with the actual path to your GodSight installation directory.")
    elif platform.system() in ["Linux", "Darwin"]:  # Darwin is macOS's system name
        print(f"{godsight_home_instruction} On Linux or macOS, you can add this to your shell profile. For bash "
              f"users, run:\n")
        print('echo \'export GODSIGHT_HOME="/path/to/GodSight"\' >> ~/.bash_profile\n')
        print('echo \'export GODSIGHT_HOME="/path/to/GodSight"\' >> ~/.bashrc\n')
        print("Replace '/path/to/GodSight' with the actual path to your GodSight installation directory.")
        print("Then, source your profile or restart your terminal session to apply the changes.")
    else:
        print("Your operating system is not recognized. Please manually set the GODSIGHT_HOME environment variable.")


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        # Calling the superclass run method to handle the standard installation process.
        install.run(self)
        # Custom post-installation tasks.
        _post_install()


setup(
    name="GodSight",
    version="0.1.0",
    author="Dilusha",
    author_email="dilushamadushan9912@gmail.com",
    description="On-chain Analysis Extendable Framework",
    long_description="A longer description of your project",
    long_description_content_type="text/markdown",
    url="http://yourpackagehomepage.com",
    packages=find_packages(),
    install_requires=[
        'numpy==1.26.2',
        'pandas==2.1.4',
        'psycopg2==2.9.9',
        'psycopg2-binary==2.9.9',
        'python-dotenv==1.0.0',
        'requests==2.31.0',
        'SQLAlchemy==2.0.23',
        'pytz~=2024.1',
        'astor~=0.8.1',
        'setuptools~=68.2.0',
        'Flask==3.0.1',
        'Flask-Cors==4.0.0',
        'Flask-SQLAlchemy==3.1.1',
    ],
    entry_points={
        'console_scripts': [
            'GodSight=GodSight.main:main',  # Ensure this points to the correct module and callable
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    python_requires=">=3.10",
)
