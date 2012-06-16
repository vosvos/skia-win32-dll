""" 2012.06.15
    1. This script joins separate Skia .gyp files (core,opts,effects,ports,utils...) 
       into one "gyp/skia_dll_msvs2010e.gyp", that could be used to create one shared lib (dll).
       see "skia_dll_config" below for more details.
       
    2. Creates "gyp/win32_app.gyp" and "skia_win32.gyp" files.
    3. Generates Visual Studio 2010 Express project files.
    
    More useful info (to build Release version) could be found in chromium gyp files like:
    http://src.chromium.org/viewvc/chrome/trunk/src/build/common.gypi
"""

import os
import sys
import pprint

script_dir = os.path.dirname(__file__)

# Directory within which we can find the gyp source.
gyp_source_dir = os.path.join(script_dir, 'third_party', 'externals', 'gyp')

# Directory within which we can find most of Skia's gyp configuration files.
gyp_config_dir = os.path.join(script_dir, 'gyp')

# Directory within which we want all generated files (including Makefiles)
# to be written.
output_dir = os.path.join(os.path.abspath(script_dir), 'out')

sys.path.append(os.path.join(gyp_source_dir, 'pylib'))
import gyp

skia_win32_config = """
{
  'targets': [
    {
      # Use this target to build everything provided by Skia.
      'target_name': 'main',
      'type': 'none',
      'dependencies': [
          'gyp/win32_app.gyp:win32_app', # this will include skia_dll.gyp
      ],
    },
  ],
}
"""

win32_app_config = """
{
    'targets': [{
        'target_name': 'win32_app',
        'type': 'executable',

        'defines': [
            'SKIA_DLL',
            'WIN32',
            #'SKIA_IMPLEMENTATION=1', commented - so it will be using dllimport (instead of export)
            #'SK_RELEASE' # define this in SkUserConfig.h
            '_UNICODE',
            'UNICODE',
            'OS_WIN', # for /ext
        ],
        
        'sources': [
            '../win32_app/skia_app.cpp',
        ],
        
        'dependencies' : [
            'skia_dll_msvs2010e.gyp:skia',
        ],
        
        'include_dirs' : [
            '../',
            '../include/config/',
            '../include/effects/',
            '../include/core/',
        ],

        'link_settings': 
        {
            'libraries': [
                '-lskia.lib',
            ],
        },
        
        'msvs_settings': 
        {
            'VCLinkerTool': {
                'AdditionalLibraryDirectories':
                ['$(OutDir)'], # this must be modified in case it's not Debug
            },              
        },
    },]
}

"""

skia_dll_config = """
{
'targets' : [

    {
        'target_name' : 'skia',
        'type' : 'shared_library',
        
        'defines': [
            'SKIA_DLL',
            'WIN32',
            'SKIA_IMPLEMENTATION=1',
            #'SK_RELEASE' # define this in SkUserConfig.h
            '_UNICODE',
            'UNICODE',
            'OS_WIN', # for /ext
        ],
        
        #include\core\skrefcnt.h(28): warning C4251: 'SkRefCnt::fInstanceCountHelper' : class 'SkRefCnt::SkInstanceCountHelper' needs to have dll-interface to be used by clients of class 'SkRefCnt'
        #include\core\skrefcnt.h(28) : see declaration of 'SkRefCnt::SkInstanceCountHelper'
        
        'msvs_disabled_warnings': [4251],
        
        'link_settings': 
        {
            'libraries': [
                '-lPsapi.lib' # for /ext
            ],
        },
        
        # better shared_library settings:
        # http://src.chromium.org/svn/trunk/src/build/common.gypi
        'msvs_settings': 
        {
              'VCCLCompilerTool': {
                'ExceptionHandling': '1',  # /EHsc
                'AdditionalOptions': [ '/EHsc' ], # common_conditions.gypi overwrites 'ExceptionHandling': '0', so we must add /EHsc
              },
        },
        
        'dependencies' :
        [
            'core.gyp:core',
            'ports.gyp:ports',
            'utils.gyp:utils',
            'effects.gyp:effects',
            'pdf.gyp:pdf', # jo prireike /ext
            
            # Note: A more slimmed-down library (with no source edits) can be compiled
            # by removing all dependencies below this comment, and uncommenting the
            # SkOSFile.cpp source below.
            
            #'animator.gyp:animator',
            #'gpu.gyp:skgr',
            #'gpu.gyp:gr',
            #'xml.gyp:xml',
            #'opts.gyp:opts',
            #'svg.gyp:svg',
            #'views.gyp:views',
            #'images.gyp:images',
        ],
        
        'include_dirs' : ['../',  ], # kad galetume pasiekti /ext /base ir /build
        
        'sources':
        [
            '../include/config/SkUserConfig.h',
            
            '../build/build_config.h',

            '../base/basictypes.h',
            '../base/compiler_specific.h',
            '../base/port.h',
            
            # skia extensions from: http://src.chromium.org/viewvc/chrome/trunk/src/skia/skia.gyp?view=markup
            '../ext/bitmap_platform_device.h',
            #'../ext/bitmap_platform_device_android.cc',
            #'../ext/bitmap_platform_device_android.h',
            '../ext/bitmap_platform_device_data.h',
            #'../ext/bitmap_platform_device_linux.cc',
            #'../ext/bitmap_platform_device_linux.h',
            #'../ext/bitmap_platform_device_mac.cc',
            #'../ext/bitmap_platform_device_mac.h',
            '../ext/bitmap_platform_device_win.cc',
            '../ext/bitmap_platform_device_win.h',
            '../ext/canvas_paint.h',
            '../ext/canvas_paint_common.h',
            #'../ext/canvas_paint_gtk.h',
            #'ext/canvas_paint_mac.h',
            '../ext/canvas_paint_win.h', # SITAS SVARBUS
            #'../ext/convolver.cc',
            #'../ext/convolver.h',
            #'../ext/google_logging.cc',
            #'../ext/image_operations.cc',
            #'../ext/image_operations.h',
            #'../ext/SkThread_chrome.cc',
            '../ext/platform_canvas.cc',
            '../ext/platform_canvas.h',
            #'../ext/platform_canvas_linux.cc',
            #'../ext/platform_canvas_mac.cc',
            #'../ext/platform_canvas_skia.cc', dubliuoja platform_canvas_win todel gauname linking error'a
            '../ext/platform_canvas_win.cc',
            '../ext/platform_device.cc',
            '../ext/platform_device.h',
            #'../ext/platform_device_linux.cc',
            #'../ext/platform_device_mac.cc',
            '../ext/platform_device_win.cc',
            #'../ext/SkMemory_new_handler.cpp', # dubliuoja SkMemory_malloc.c (bet gali buti kad jis yra tinkamesnis)
            #'../ext/skia_sandbox_support_win.h',
            #'../ext/skia_sandbox_support_win.cc',
            #'../ext/skia_trace_shim.h',
            #'../ext/skia_utils_mac.mm',
            #'../ext/skia_utils_mac.h',
            '../ext/skia_utils_win.cc',
            '../ext/skia_utils_win.h',
            '../ext/vector_canvas.cc',
            '../ext/vector_canvas.h',
            '../ext/vector_platform_device_emf_win.cc',
            '../ext/vector_platform_device_emf_win.h',
            '../ext/vector_platform_device_skia.cc',
            '../ext/vector_platform_device_skia.h',        
        ],
	},
]
}
"""

def join_gyp_data(config_data, target_data):
    
    for key, value in target_data.items():
        if not key in config_data:
            config_data[key] = value # new data
        elif isinstance(value, list):
            config_data[key].extend(value) # append list data
        
            if key != "conditions": # remove duplicates
                config_data[key] = list(set(config_data[key]))
                

def create_skia_dll_gyp(config_str, skia_gyp_file):
    config_data = eval(config_str, {'__builtins__': None}, None)
    
    config_target = config_data["targets"][0]
    
    dependencies = config_target["dependencies"][:]
    del config_target["dependencies"] # no longer needed - could be replaced by new dependencies

    for target in dependencies:
        path, target_name = target.split(":")
        
        path = os.path.join(gyp_config_dir, path)
        
        gyp_data = eval(open(path).read(), {'__builtins__': None}, None)
        targets = gyp_data["targets"]
        for target_data in targets:
            if target_data["target_name"] == target_name:
                join_gyp_data(config_target, target_data)
                break
    
    # remove original dependencies
    config_target["dependencies"] = list(set(config_target.get("dependencies", [])).difference(set(dependencies)))

    del config_target["msvs_guid"] # remove core.gyp guid
    
    file = open(skia_gyp_file, "w")
    file.write(pprint.pformat(config_data, width=10, indent=4))
    file.close()
    
    
if __name__ == '__main__':
    args = [] #sys.argv[1:]
  
    # Set CWD to the directory containing this script.
    # This allows us to launch it from other directories, in spite of gyp's
    # finickyness about the current working directory.
    # See http://b.corp.google.com/issue?id=5019517 ('Linux make build
    # (from out dir) no longer runs skia_gyp correctly')
    os.chdir(os.path.abspath(script_dir))
    
    # create skia_main.gyp
    skia_win32_file = "skia_win32.gyp"
    file = open(skia_win32_file, "w")
    file.write(skia_win32_config)
    file.close()
    
    # create win32_app.gyp
    file = open(os.path.join(gyp_config_dir, "win32_app.gyp"), "w")
    file.write(win32_app_config)
    file.close()
    

    skia_gyp_file = os.path.join(gyp_config_dir, "skia_dll_msvs2010e.gyp")
    #variables = create_variables("msvs") # galima bus pratestuoti tik su {}
    #print "variables: ", variables
    include_file = os.path.join(gyp_config_dir, 'common.gypi')
    depth = '.'
    
    # create skia dll gyp
    create_skia_dll_gyp(skia_dll_config, skia_gyp_file)

    args.append(skia_win32_file)

    # Always include common.gypi.
    # We do this, rather than including common.gypi explicitly in all our gyp
    # files, so that gyp files we use but do not maintain (e.g.,
    # third_party/externals/libjpeg/libjpeg.gyp) will include common.gypi too.
    args.append('-I' + include_file)

    args.extend(['--depth', depth])

    # Tell gyp to write the Makefiles into output_dir
    args.extend(['--generator-output', os.path.abspath(output_dir)])

    # Tell make to write its output into the same dir
    args.extend(['-Goutput_dir=.'])

    # Special arguments for generating Visual Studio projects:
    # - msvs_version forces generation of Visual Studio 2010 project so that we
    #   can use msbuild.exe
    # - msvs_abspath_output is a workaround for
    #   http://code.google.com/p/gyp/issues/detail?id=201
    args.extend(['-Gmsvs_version=2010e'])

    print 'Updating projects from gyp files...'
    sys.stdout.flush()

    # Off we go...
    print "ARGS: ", args
    sys.exit(gyp.main(args))



