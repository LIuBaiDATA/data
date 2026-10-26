[app]

title = My App
package.name = myapp
package.domain = org.shipit
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,txt,json,html,js,css,mp3,wav,ogg,gif,xml
source.exclude_exts = spec,pyc,pyo
source.exclude_dirs = tests, bin, venv, .venv, .git, .github, dist, build, __pycache__
version = 0.1.0

# 维持 Kivy 2.1.0，并加入 setuptools 以解决依赖冲突
requirements = python3,kivy==2.1.0,pyjnius,setuptools==57.0.0

orientation = portrait
fullscreen = 0

#------------------------------------------------------------------------------
# Android specific
#------------------------------------------------------------------------------
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.logcat_filters = *:S python:D

#------------------------------------------------------------------------------
# Buildozer settings
#------------------------------------------------------------------------------
[buildozer]
log_level = 2
warn_on_root = 0