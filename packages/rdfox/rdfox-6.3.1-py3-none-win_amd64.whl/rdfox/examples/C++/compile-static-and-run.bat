cl /EHsc /W3 /WX /MT /I "..\..\include" /D CRDFOX_EXPORT /FeCppRDFoxStaticDemo.exe CppRDFoxDemo.cpp ws2_32.lib shlwapi.lib kernel32.lib shell32.lib ole32.lib /link /LIBPATH:"..\..\lib" /WHOLEARCHIVE:libRDFox-static.lib
xcopy /s /Y ..\data .
.\CppRDFoxStaticDemo.exe
        