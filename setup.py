from setuptools import setup, find_packages

def readme():
    with open('README.md', 'r') as f:
        return f.read()

setup(
    name='DAICommit',
    version='1.0.7',
    author='Discq192',
    author_email='guziienkomatvei@gmail.com',
    description='Auto-generate impressive commits in 1 second. Killing lame commits with AI 🤯🔫',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/Matvey-Guzienko/aicommit',
    install_requires=['openai>=1.53.0', 'google-generativeai>=0.8.3', 'anthropic>=0.38.0', 'rich==13.9.4', 'pick==2.4.0', 'GitPython>=3.1.43', 'colorama>=0.4.6', 'pydantic>=2.9.2', 'tiktoken>=0.8.0'],
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='AI commit git aicommit',
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'aicommit = DAICommit.__main__:main',
        ],
    }
)
