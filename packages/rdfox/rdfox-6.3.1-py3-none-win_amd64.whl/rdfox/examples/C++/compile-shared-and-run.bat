cl /EHsc /W3 /WX /MT /I "..\..\include" /FeCppRDFoxSharedDemo.exe CppRDFoxDemo.cpp libRDFox.lib /link /LIBPATH:"..\..\lib"
copy ..\..\lib\libRDFox.dll .
xcopy /s /Y ..\data .
.\CppRDFoxSharedDemo.exe
        