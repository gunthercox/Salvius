Voce
voce.sourceforge.net

This file contains basic installation and usage info.  For more documentation, visit the website.

------------------------------------
Package contents
------------------------------------
lib - directory containing compiled Voce, FreeTTS, and Sphinx4 libraries
samples - directory containing example applications that show how to use Voce
src - directory containing the Voce source code for Java and C++
changelog.txt - a list of changes for each version
license-BSD.txt - BSD Open Source license
license-LGPL.txt - LGPL Open Source license
readme.txt - you're reading it
vocabulary.txt - a list of the words Voce can recognize (via Sphinx4)


------------------------------------
List of dependencies
------------------------------------
1. FreeTTS (version 1.2.1 included in this package) - freetts.sourceforge.net
2. CMUSphinx4 (version 1.0beta included in this package) - cmusphinx.sourceforge.net
3. Java 1.5 runtime environment; also, Java SDK required to build Voce from source
4. Java Native Interface (JNI) (usually included in the Java SDK) required for C++ applications


------------------------------------
Setting up dependencies
------------------------------------
The term 'javadir' here refers to the root of your Java runtime environment installation.  If you are using the Java SDK, the runtime environment is usually included in the 'jre' directory.

The term 'class path' refers to the place where all Voce class files (packaged into jar files) are located.  This can be anywhere, as long as you tell Voce about the class path.

Make sure the jvm library can be located at runtime.  In win32, the file 'jvm.dll' (usually in javadir\bin\client) must be in your "path" environment variable.  In UNIX, the file 'libjvm.so' must be in your library path environment variable.  Do NOT move these libraries out of their default locations; as of Java 2 SDK v1.2, they look for other runtime environment libraries relative to their own locations.


------------------------------------
Library build instructions
------------------------------------
Java - The Voce jar file should already be present in the 'lib' directory, so you won't need to build it... but if you want to build it anyway, use the included build scripts (*.bat in win32, *.sh in UNIX).

C++ - Same as Java instructions.  The Voce Java jar is used by the C++ version via the Java Native Interface.


------------------------------------
Using Voce in your application
------------------------------------
See the 'synthesisTest' and 'recognitionTest' sample applications for examples.


------------------------------------
Tips for good recognition results
------------------------------------
* A good microphone makes a world of difference.  I saw substantial improvements in recognition accuracy when I switched to a cheap Labtec headset after using my laptop's built-in microphone.
