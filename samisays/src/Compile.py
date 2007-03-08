from distutils.core import setup
import py2exe

setup(console=['SamiSays.py'],

options = {
    "py2exe": {
        "dist_dir": "../../dist",
    },
},

)
