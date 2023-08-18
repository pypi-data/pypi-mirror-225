import setuptools

setuptools.setup(
    name="modulairy-mail-sender",
    version="0.0.2",
    author="Fatih Mehmet ARSLAN",
    author_email="contact@fmarslan.com",
    description="This script enables sending emails asynchronously from Azure Service Bus. Each bus message contains a sender's email address along with SMTP configurations. The script utilizes its SMTP configuration of the message for sending emails.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    platforms="all",
    url="https://github.com/modulairy/mail-sender",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Internet",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Intended Audience :: Developers",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Microsoft",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8"
    ],
    install_requires=["aiosmtplib","azure-servicebus"],
    python_requires=">=3.8, <4",
    packages=['modulairy_mail_sender'],
    scripts=['bin/modulairy-mail-sender']
)
