from setuptools import setup, find_packages

setup(
    name="malgrabber",
    version="1.2",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4",
        "asyncio",
        "aiohttp"
    ],
    author="Swargaraj Bhowmik",
    author_email="contact@swargarajbhowmik.me",
    license="MIT",
    description="This Package is designed to provide developers with a straightforward way to access MyAnimeList's data programmatically.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/swargarajbhowmik/malgrabber"
)
