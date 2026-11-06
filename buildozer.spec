[app]
title = Mis Gastos
package.name = misgastos
package.domain = org.ejemplo
source.dir = .
source.include_exts = py,kv,png,jpg,ttf
version = 0.1
requirements = python3==3.11.5,hostpython3==3.11.5,kivy==2.3.0,sqlite3
orientation = portrait
fullscreen = 0

# Android
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.ndk = 25b
p4a.branch = v2024.01.21
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
