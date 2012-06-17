skia-win32-dll
==============

Skia 2D graphic library build script for Windows (skia.dll).
and sample app.

Build instructions for msvs2010e.

1. Install Microsoft Visual Studio 2010e.  
Instructions for skia: https://sites.google.com/site/skiadocs/user-documentation/quick-start-guides/windows  
Chromium instructions (could be helpful): http://www.chromium.org/developers/how-tos/build-instructions-windows  

2. Install GYP (-r 1415).
    >svn checkout http://gyp.googlecode.com/svn/trunk/ gyp-read-only  
    >python setup.py install.

3. Checkout skia sources (-r 4270).
    >svn checkout http://skia.googlecode.com/svn/trunk/ skia-read-only
    
4. Copy required chromium files (/ext, /build, /base) to main skia folder.  
You could use files from this archive or update files from:
http://src.chromium.org/viewvc/chrome/trunk/src/  
Changes from original files:  
    - Calls to debug and logging header files are commented out (debugger.h,trace_event.h,logging.h).  
    - Fixed paths to skia header files.

5. Copy skia_dll_msvs2010e.py and /win32_app to main skia folder

6. Generate VisualStudio project files:
    >python skia_dll_msvs2010e.py  

    This script joins separate Skia .gyp files into one .gyp for shared lib (dll).
    And creates win32_app.gyp and skia_win32.gyp files
    Modify "skia_dll_config" dependencies to add (gpu, images, etc)

7. Open /out/skia_win32.sln, set win32_app as "StartUp Project".  
Remove project (core) as it's not required anymore (included by sfnt.gyp from Skia build files)  
Build the solution and run sample app!
