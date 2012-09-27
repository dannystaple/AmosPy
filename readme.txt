Code to extract plain text from Amos tokenised files.

Author: Danny Staple
Contributors: Matt Oxenham - for providing key information on Amos tokens
License: PSF - Open source, GPL Compatible, less restrictive.
Version: 0.1 Alpha - not all tokens available, memory banks not available.
Target Audience: Developers, or nostalgic people finding old Amiga files, or willing to help make sense of them.

Use:
While rummaging through ancient files and source code, I found a bunch of Amos and Amos Pro source files.
Amos was a fun learning language on the Commodore Amiga family of computers, derived from STOS (so some of this may be compatible),
which I used during the 90's. The files it stores are not plain text however, they use a binary format with byte counts,
token values, extension references. Amos files also can contain embedded sound, fonts, graphics and other data
resources.

This is intended to find a way to get human readable code from the files, and possibly get all of the other data
info from them too. This is intended to prevent the format becoming unknown, arcane and unreadable.

Currently, the only way I know of to read these is with an Amiga or an Amiga emulator running a version of Amos.
Even some of the later "Amos like" projects on the internet will not read these files.