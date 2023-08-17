from setuptools import setup, find_packages, find_namespace_packages

# pypi long description
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='opaw',
    packages=find_packages(),
    version='0.4.5',
    license='MIT',
    description='Unofficial python wrapper of OpenAI API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='hiimanget',
    author_email='hiimanget@gmail.com',
    url='https://github.com/hiimanget/openai-pw',
    keywords=['openai', 'python', 'api', 'wrapper'],
    install_requires=['openai', 'openai-whisper', 'whisper_timestamped'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
)
