.. contents::

Benchmark results
=================
Detailed benchmark results.

Environment
-----------

- **Machine:** Linux ubuntu 3.2.0-44-generic #69-Ubuntu SMP Thu May 16 17:35:01 UTC 2013 x86_64
- **Libc version:** glibc 2.7
- **Python version:** 2.7
- **lychee.json version:** 1.0.1
- **ultrajson version:** 1.30
- **simplejson version:** 2.3.2
- **cjson version:** 1.0.5
- **yajl version:** 0.3.5
- **json version:** 2.0.9

Every function calls in 100 times and repead it 10 times then choose best time.

ASCII String
------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                242025.620 calls/sec             101532.413 calls/sec
json                       128896.865 calls/sec              96420.782 calls/sec
ultrajson                  134562.207 calls/sec              59552.804 calls/sec
simplejson                 104154.557 calls/sec              87272.243 calls/sec
================ ============================== ================================

Array with 100 Decimal numbers
------------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                  5318.604 calls/sec              81490.266 calls/sec
ultrajson                    2456.041 calls/sec              83551.873 calls/sec
simplejson                   3987.701 calls/sec              40485.560 calls/sec
json                            0.000 calls/sec              39542.792 calls/sec
================ ============================== ================================

Array with 100 [True, False, None] values
-----------------------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                 43836.789 calls/sec               8045.083 calls/sec
json                         3858.463 calls/sec               6808.714 calls/sec
ultrajson                    3290.863 calls/sec               5821.703 calls/sec
simplejson                   1667.835 calls/sec               6787.559 calls/sec
================ ============================== ================================

Array with 100 long numbers
---------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                 64726.914 calls/sec              52083.745 calls/sec
json                        50375.979 calls/sec              19127.618 calls/sec
simplejson                  44902.088 calls/sec              18961.591 calls/sec
ultrajson                       0.000 calls/sec                  0.000 calls/sec
================ ============================== ================================

Array with 1000 float numbers
-----------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                  8044.311 calls/sec               6777.797 calls/sec
ultrajson                    1160.337 calls/sec               7999.969 calls/sec
simplejson                   1099.228 calls/sec               2638.856 calls/sec
json                         1134.611 calls/sec               2550.101 calls/sec
================ ============================== ================================

Array with 1000 integers
------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                  4315.350 calls/sec               3119.346 calls/sec
ultrajson                    2219.220 calls/sec               2981.514 calls/sec
json                         1057.006 calls/sec                273.852 calls/sec
simplejson                    996.762 calls/sec                279.862 calls/sec
================ ============================== ================================

Array with 256 ASCII string
---------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                 32426.007 calls/sec              15356.438 calls/sec
json                        15571.369 calls/sec              11291.705 calls/sec
simplejson                  13111.297 calls/sec              13700.160 calls/sec
ultrajson                   18005.168 calls/sec               8440.262 calls/sec
================ ============================== ================================

Array with 256 ASCII string that start with date string
-------------------------------------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                 29560.251 calls/sec              13764.904 calls/sec
json                        14636.739 calls/sec              10711.231 calls/sec
simplejson                  12423.886 calls/sec              12597.777 calls/sec
ultrajson                   16292.356 calls/sec               7691.737 calls/sec
================ ============================== ================================

Array with 256 UTF-8 Unicode
----------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                  7293.427 calls/sec              15165.434 calls/sec
simplejson                   3368.243 calls/sec              13543.119 calls/sec
json                         3439.730 calls/sec              11383.027 calls/sec
ultrajson                    2903.517 calls/sec               3443.995 calls/sec
================ ============================== ================================

Array with 256 UTF-8 string
---------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                  6069.114 calls/sec              14785.857 calls/sec
simplejson                   2073.442 calls/sec              13450.180 calls/sec
json                         2117.843 calls/sec              11427.376 calls/sec
ultrajson                    3768.467 calls/sec               3443.515 calls/sec
================ ============================== ================================

Array with 256 unicode escaped string
-------------------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                  6095.663 calls/sec               4362.251 calls/sec
ultrajson                    3723.835 calls/sec               1659.008 calls/sec
json                         2091.745 calls/sec                504.383 calls/sec
simplejson                   2080.302 calls/sec                455.614 calls/sec
================ ============================== ================================

Default function
----------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json               1519675.362 calls/sec                  0.000 calls/sec
ultrajson                  241607.373 calls/sec                  0.000 calls/sec
json                       213233.554 calls/sec                  0.000 calls/sec
simplejson                 145383.154 calls/sec                  0.000 calls/sec
================ ============================== ================================

Empty Arrays
------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                483214.747 calls/sec              84819.090 calls/sec
ultrajson                   46060.883 calls/sec              61311.270 calls/sec
json                        34292.405 calls/sec              18139.100 calls/sec
simplejson                  13326.250 calls/sec              18082.794 calls/sec
================ ============================== ================================

Empty Object
------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                338796.769 calls/sec             166374.613 calls/sec
ultrajson                   99109.263 calls/sec             105809.889 calls/sec
simplejson                  25614.070 calls/sec              19519.285 calls/sec
json                        30203.096 calls/sec              10782.827 calls/sec
================ ============================== ================================

Encode array of datetime objects
--------------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json               1370687.582 calls/sec            2872810.959 calls/sec
ultrajson                  367598.948 calls/sec              73365.471 calls/sec
simplejson                  22457.054 calls/sec              66052.031 calls/sec
json                        27093.237 calls/sec              60751.796 calls/sec
================ ============================== ================================

Ensure ASCII from ASCII string
------------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json               1282661.774 calls/sec            1010675.663 calls/sec
ultrajson                  934143.430 calls/sec             540503.093 calls/sec
json                       625082.563 calls/sec             374491.429 calls/sec
simplejson                 571431.063 calls/sec             390895.061 calls/sec
================ ============================== ================================

Ensure ASCII from UTF-8 string
------------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json               1124478.284 calls/sec                  0.000 calls/sec
ultrajson                  863025.514 calls/sec                  0.000 calls/sec
json                       400219.847 calls/sec                  0.000 calls/sec
simplejson                 397187.879 calls/sec                  0.000 calls/sec
================ ============================== ================================

Ensure ASCII from UTF-8 unicode
-------------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json               1205259.770 calls/sec                  0.000 calls/sec
ultrajson                  689852.632 calls/sec                  0.000 calls/sec
json                       610524.600 calls/sec                  0.000 calls/sec
simplejson                 588261.431 calls/sec                  0.000 calls/sec
================ ============================== ================================

Ensure ASCII from mixed UTF-8 and ASCII string
----------------------------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                902000.860 calls/sec            1121471.658 calls/sec
ultrajson                  495195.277 calls/sec             377525.113 calls/sec
json                       291676.217 calls/sec             307725.899 calls/sec
simplejson                 278506.242 calls/sec             295998.871 calls/sec
================ ============================== ================================

Medium complex object
---------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                 37861.563 calls/sec              15477.137 calls/sec
ultrajson                   14469.604 calls/sec              11803.636 calls/sec
simplejson                   4529.192 calls/sec               5181.351 calls/sec
json                         5544.428 calls/sec               3086.135 calls/sec
================ ============================== ================================

Mixed UTF-8 and ASCII string
----------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json               1043359.204 calls/sec            1124478.284 calls/sec
ultrajson                  523633.458 calls/sec             378889.250 calls/sec
json                       294130.715 calls/sec             291676.217 calls/sec
simplejson                 275397.505 calls/sec             291676.217 calls/sec
================ ============================== ================================

Object with large keys and large string values
----------------------------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                   273.493 calls/sec                 64.166 calls/sec
json                          161.392 calls/sec                 96.481 calls/sec
simplejson                    136.980 calls/sec                 94.758 calls/sec
ultrajson                     163.609 calls/sec                 44.294 calls/sec
================ ============================== ================================

UTF-8 String
------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                190477.021 calls/sec             241468.279 calls/sec
ultrajson                  101630.821 calls/sec             137698.752 calls/sec
simplejson                  69499.652 calls/sec              93979.476 calls/sec
json                        66980.262 calls/sec              88189.739 calls/sec
================ ============================== ================================

UTF-8 Unicode
-------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json               1514189.170 calls/sec            2637927.044 calls/sec
ultrajson                  730714.983 calls/sec             806596.923 calls/sec
simplejson                 609637.209 calls/sec             537731.282 calls/sec
json                       599186.286 calls/sec             487709.767 calls/sec
================ ============================== ================================

real_data.json file contents
----------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                  2639.521 calls/sec                631.737 calls/sec
ultrajson                     578.638 calls/sec                568.246 calls/sec
simplejson                    355.094 calls/sec                488.282 calls/sec
json                          355.025 calls/sec                187.543 calls/sec
================ ============================== ================================

ultrajson_sample.json file contents
-----------------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                  1678.702 calls/sec                721.531 calls/sec
ultrajson                     646.497 calls/sec                672.567 calls/sec
json                          527.282 calls/sec                285.443 calls/sec
simplejson                    484.914 calls/sec                305.594 calls/sec
================ ============================== ================================

ultrajson_sample.json file contents as unicode data
---------------------------------------------------

================ ============================== ================================
Lib                                      Encode                           Decode
================ ============================== ================================
lychee.json                  1685.150 calls/sec                943.753 calls/sec
ultrajson                     642.467 calls/sec                463.495 calls/sec
json                          530.966 calls/sec                353.419 calls/sec
simplejson                    482.859 calls/sec                399.154 calls/sec
================ ============================== ================================


SUMMARY
-------

=========== =================== =================== =================== ========
Lib                      Encode              Decode                 AVG   Slower
=========== =================== =================== =================== ========
lychee.json        11468651.021         9594347.448        10531499.234   1.00 x
ultrajson           5297455.408         2679838.379         3988646.893   2.64 x
json                3422922.225         1853517.376         2638219.801   3.99 x
simplejson          3192555.888         1930576.677         2561566.283   4.11 x
=========== =================== =================== =================== ========

WINNERS
^^^^^^^

========================================================= ========== ===========
Benchmark                                                 Encode     Decode     
========================================================= ========== ===========
ASCII String                                              lychee.jsonlychee.json
Array with 100 Decimal numbers                            lychee.jsonultrajson  
Array with 100 [True, False, None] values                 lychee.jsonlychee.json
Array with 100 long numbers                               lychee.jsonlychee.json
Array with 1000 float numbers                             lychee.jsonultrajson  
Array with 1000 integers                                  lychee.jsonlychee.json
Array with 256 ASCII string                               lychee.jsonlychee.json
Array with 256 ASCII string that start with date string   lychee.jsonlychee.json
Array with 256 UTF-8 Unicode                              lychee.jsonlychee.json
Array with 256 UTF-8 string                               lychee.jsonlychee.json
Array with 256 unicode escaped string                     lychee.jsonlychee.json
Default function                                          lychee.json\-         
Empty Arrays                                              lychee.jsonlychee.json
Empty Object                                              lychee.jsonlychee.json
Encode array of datetime objects                          lychee.jsonlychee.json
Ensure ASCII from ASCII string                            lychee.jsonlychee.json
Ensure ASCII from UTF-8 string                            lychee.json\-         
Ensure ASCII from UTF-8 unicode                           lychee.json\-         
Ensure ASCII from mixed UTF-8 and ASCII string            lychee.jsonlychee.json
Medium complex object                                     lychee.jsonlychee.json
Mixed UTF-8 and ASCII string                              lychee.jsonlychee.json
Object with large keys and large string values            lychee.jsonjson       
UTF-8 String                                              lychee.jsonlychee.json
UTF-8 Unicode                                             lychee.jsonlychee.json
real_data.json file contents                              lychee.jsonlychee.json
ultrajson_sample.json file contents                       lychee.jsonlychee.json
ultrajson_sample.json file contents as unicode data       lychee.jsonlychee.json
========================================================= ========== ===========
