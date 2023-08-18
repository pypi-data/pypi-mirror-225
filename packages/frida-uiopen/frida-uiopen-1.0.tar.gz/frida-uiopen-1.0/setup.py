import glob
import os

from setuptools import setup

pkg_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "frida_uiopen"))

agents = glob.glob(os.path.join(pkg_dir, "*_agent.*"))
assert len(agents) > 0, "Agents not compiled; run “npm install && npm run build” in agents/*/"

setup(
    name="frida-uiopen",
    version="1.0",
    description="Invoke the openURL of iOS based on frida.",
    long_description="A frida command-line tool that supports iOS devices that attempt to open resources at a "
                     "specified URL.",
    long_description_content_type="text/markdown",
    author="Summer",
    author_email="cuihaixu@126.com",
    url="https://github.com/Cuihaixu/frida-uiopen",
    install_requires=[
        "colorama >= 0.2.7, < 1.0.0",
        "frida >= 16.0.9, < 17.0.0",
        "prompt-toolkit >= 2.0.0, < 4.0.0",
        "pygments >= 2.0.2, < 3.0.0",
    ],
    license="wxWindows Library Licence, Version 3.1",
    zip_safe=False,
    keywords="frida uiopen debugger dynamic instrumentation inject javascript windows macos linux ios iphone ipad "
             "android qnx",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: JavaScript",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=["frida_uiopen"],
    package_data={
        "frida_uiopen": agents,
    },
    entry_points={
        "console_scripts": [
            "frida = frida_tools.repl:main",
            "frida-uiopen = frida_uiopen.uiopen:main"
        ]
    },
)