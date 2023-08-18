import codecs
from setuptools import setup


SCHEDULE_VERSION = "1.3.1"
SCHEDULE_DOWNLOAD_URL = "https://github.com/yusefmaali/schedule-cronjob/tarball/" + SCHEDULE_VERSION


def read_file(filename):
    """
    Read a utf8 encoded text file and return its contents.
    """
    with codecs.open(filename, "r", "utf8") as f:
        return f.read()


setup(
    name="schedule-cronjob",
    packages=["schedule"],
    package_data={"schedule": ["py.typed"]},
    version=SCHEDULE_VERSION,
    description="Job scheduling for humans. With cronjob support.",
    long_description=read_file("README.rst"),
    license="MIT",
    author="Daniel Bader",
    author_email="mail@dbader.org",
    maintainer="Yusef Maali",
    maintainer_email="contact@yusefmaali.net",
    url="https://github.com/yusefmaali/schedule-cronjob",
    download_url=SCHEDULE_DOWNLOAD_URL,
    keywords=[
        "schedule",
        "periodic",
        "jobs",
        "scheduling",
        "clockwork",
        "cron",
        "scheduler",
        "job scheduling",
        "cronjob",
        "cronjob scheduling"
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: English",
    ],
    python_requires=">=3.7",
)
