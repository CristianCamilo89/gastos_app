<<<<<<< HEAD
# gastos_app
App de Gastos
=======
# Mis Gastos (Kivy + SQLite)

## Probar en PC
    pip install kivy matplotlib
    python main.py

## Compilar APK (Android) con Buildozer
Requiere Linux (Ubuntu) o WSL2 en Windows.

    sudo apt update
    sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config \
        zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    pip install --user --upgrade buildozer cython==0.29.36 virtualenv
    cd gastos_app
    buildozer android debug          # primera vez: tarda 20-40 min (descarga SDK/NDK)
    # APK en ./bin/misgastos-0.1-arm64-v8a_armeabi-v7a-debug.apk

Instalar en el celular:
    buildozer android deploy run     # con USB y depuración USB activada
o copia el .apk al teléfono y ábrelo (permitir "orígenes desconocidos").

## iOS
Solo desde macOS con Xcode: usar kivy-ios (toolchain build python3 kivy; toolchain create ...).

## Notas
- matplotlib en python-for-android es pesado/frágil. Si falla la compilación, quítalo de
  `requirements` en buildozer.spec: la app usa automáticamente barras nativas de Kivy.
- Android 10+: el CSV puede no poder escribirse en Download; en ese caso se guarda en la carpeta
  privada de la app y se muestra la ruta.
>>>>>>> c68d5ae (Primera Version)
