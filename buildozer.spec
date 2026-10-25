# Shipit OS generated buildozer.spec
# Edit title / package.name / requirements as needed, then re-run shipit.

[app]

# (str) Title of your application
title = My App

# (str) Package name
package.name = myapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.shipit

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,txt,json,html,js,css,mp3,wav,ogg,gif,xml

# (list) Source files to exclude
source.exclude_exts = spec,pyc,pyo

# (list) List of directory to exclude
source.exclude_dirs = tests, bin, venv, .venv, .git, .github, dist, build, __pycache__

# (str) Application versioning
version = 0.1.0

# (list) Application requirements (comma separated)
# 修改点 1：锁定 Kivy 稳定版本，补全底层依赖，解决 config.pxi 报错
requirements = python3,kivy==2.3.0,sdl2,pyjnius

# (str) Supported orientation
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#------------------------------------------------------------------------------
# Android specific
#------------------------------------------------------------------------------

android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True

# 修改点 2：只保留 64 位架构，去掉 armeabi-v7a，避开 32 位编译地狱
android.archs = arm64-v8a

android.logcat_filters = *:S python:D

#------------------------------------------------------------------------------
# Buildozer settings
#------------------------------------------------------------------------------

[buildozer]

log_level = 2
warn_on_root = 0