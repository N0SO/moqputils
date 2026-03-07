#!/usr/bin/python
"""
Update History:
* Sat Apr 23 2022 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 -First interation for 2021 MOQP.
* Sat Dec 06 2023 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.0 -Updated to take file names from the actual directory where.
-         the certificate files are located.
* Wed Jun 12 2024 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.1.1 -If the list file includes award names (4 fields vs 3) use them.
-         
* Mon Aug 11 2025 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.2.0 -Refactored the code to use pypdf to split the merged .pdf file
-         into individual files. No more need to use a separate utility
-         to split the files. Works with MISSOURI, but SHOWME and the
-         award certs may require a little tweaking.
* Tue Aug 12 2025 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.2.1 -Made code changes from yesterday a class to make it easier to
-         roll in award certs by creating a child class.
* Tue Aug 14 2025 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.2.2 - added (-t --typeAward) option to command line to select the
-          target type of award the list is for (shome, missouri or 
-          category.
- V0.2.3 - Changed download link text to be DOWNLOAD or (for multi-op
-          stations,) DOWNLOAD <CALLSIGN>.
"""
VERSION = '0.2.3'
#print(f'Make HTML Certificates Download Page utility V{VERSION}')
