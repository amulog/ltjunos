########################################
LTJunos
########################################

Overview
========

LTJunos is a log template parser from `System Log Explorer <https://apps.juniper.net/syslog-explorer/>`_ (by `Juniper Networks <https://www.juniper.net/>`_).
LTJunos converts the excel file of Junos log templates obtained from System Log Explorer into some formats for automatic use.

* Source: https://github.com/amulog/ltjunos
* Bug Reports: https://github.com/amulog/ltjunos/issues
* Author: `Satoru Kobayashi <https://github.com/cpflat/>`_
* License: `BSD-3-Clause <https://opensource.org/licenses/BSD-3-Clause>`_


How to obtain the list?
=======================

First, obtain the excel file of a log template list from `System Log Explorer <https://apps.juniper.net/syslog-explorer/>`_.
You need a Juniper account to obtain it (Guest account is enough).

![where](./syslog_explorer.png)

1. Go to `System Log Explorer <https://apps.juniper.net/syslog-explorer/>`_.

2. Select a Junos release you are intersted.

3. Click Excel icon (see screenshot).

4. (Create Juniper account if you need.)

5. Then you will get the excel file.

Please take care when using the list because Juniper networks claims a copyright on the list.



How to parse the list?
======================

You can parse the excel list into json file with the following command.

::

    python ltjunos.py -o output.json System_Log_Messages_Junos_OS_[release].xlsx

You can also generate `amulog <https://github.com/amulog/amulog>`_ log templates (for import-ext mode).

::

    python ltjunos.py -t amulog-plain -o lt_amulog.txt System_Log_Messages_Junos_OS_[release].xlsx
