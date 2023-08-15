cl /EHsc /W3 /WX /MT /I "..\..\include" /FeCRDFoxSharedDemo.exe CRDFoxDemo.c libRDFox.lib /link /LIBPATH:"..\..\lib"
copy ..\..\lib\libRDFox.dll .
xcopy /s /Y ..\data .
.\CRDFoxSharedDemo.exe
        