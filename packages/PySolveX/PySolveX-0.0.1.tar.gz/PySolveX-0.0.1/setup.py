from setuptools import setup, find_packages

requirements = [
	"pydub",
	"speechrecognition",
	"selenium",
	"wget"
]

setup(
    name="PySolveX",
    version="0.0.1",
    author="VIRUS",
    install_requires=requirements,
    keywords=[
        "Bypass reCaptcha V3","Bypass-reCaptcha-V3","Bypass reCaptcha",
        "Bypass-reCaptcha","Bypass reCaptcha V2","Bypass-reCaptcha-V2",
        "Solve-reCaptcha-V2","Google reCaptcha","Google-reCaptcha"
    ],
    description="Bypassing reCaptcha V3, V2 by Selenium.",
    packages=find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ]
)
