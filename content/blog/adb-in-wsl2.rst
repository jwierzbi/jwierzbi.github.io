=======================================================================
Connecting to Android device from Windows Subsystem for Linux using ADB
=======================================================================

:author: Jarosław Wierzbicki
:category: Tips & Tricks
:date: 2021-06-01
:slug: adb-in-wsl2
:lang: en
:tags: ADB, Android, Linux, Windows, WSL, WSL2

A few weeks ago COVID-19 finally hit Taiwan (so far we've been doing pretty
well) and I had to move to work from home like the rest of the world (well at
least some of it). This forced me to use my work laptop for more than meetings.

Normally I use a Linux PC for daily work so to get at least some of the comfort
back I've set up Windows Subsystem for Linux version 2 (WSL2) on the laptop.

This didn't go without a few bumps along the way. The biggest one was the fact
that WSL2 doesn't support accessing USB devices (version 1 allegedly does [#]_
but I didn't have a chance to check) from Linux. And this was a problem for me
since I need to connect to an Android device frequently.

But as long as there's Internet there's hope. After digging for some time
I wasn't disappointed because it turned out that there is a solution to this
problem.

.. PELICAN_END_SUMMARY

How does Android Debug Bridge (ADB) work?
=========================================

Let's just quickly look at how the Android Debug Bridge (ADB) works.

ADB is a command line tool that implements client-server architecture [#]_. It
consists of three parts:

* A client, which runs on a development machine and sends commands to the device
  with the help of the server. This is the :code:`adb` command line tool.
* A server, which runs on the development machine and communicates directly with
  the device (daemon). It accepts commands from the client and forwards them
  to the device (it's started by :code:`adb`).
* A daemon (:code:`adbd`), which runs on a device and accepts commands from the
  server.

When we execute :code:`adb` command it tries to connect to the server. If the
server is not running it's going to be automatically started:

.. code-block:: plain
   :hl_lines: 2

    $ adb devices
    * daemon not running; starting now at tcp:5037
    * daemon started successfully
    List of devices attached
    0123456789A     device

Sure enough when we list the processes:

.. code-block:: plain
   :hl_lines: 2

    $ ps -eo pid,command | awk '!/grep/ && /adb/'
    599501 adb -L tcp:5037 fork-server server --reply-fd 4

We can see that the ADB server is running in the background. The above line
also tells us that the server is listening on TCP socket localhost:5037
(localhost is implicit here).

The fact that the server is listening on a TCP socket already hints at how we
can make the ADB working in WSL2.

Connecting from WSL to ADB
==========================

As I already mentioned we need a server and a client to connect to an Android
device. Let's take a look at how to set those two up.

The server
----------

The first thing we have to do is to determine the version of the client that
runs in WSL. We can do that by running (in WSL):

.. code-block:: plain
   :hl_lines: 2

    $ adb version
    Android Debug Bridge version 1.0.41
    Version 30.0.4-6686687
    Installed as /home/jaro/platform-tools/adb

In my case, it's 1.0.41. This is important because we need to match this version
on the Windows side. The easiest way is just to download the appropriate version
for example from `this website <androidmtk.com_>`_. But there are also other
methods [#]_ [#]_ if you don't feel comfortable downloading stuff from random
websites on the Internet |winking-face|.

.. |winking-face| unicode:: 0x1F609
.. _androidmtk.com: https://androidmtk.com/download-android-sdk-platform-tools

When we get the appropriate version of the tool set up in our Windows we can
check if the version indeed matches the Linux counterpart:

.. code-block:: plain
   :hl_lines: 2

    C:\Users\jaro\platform-tools>adb.exe version
    Android Debug Bridge version 1.0.41
    Version 30.0.4-6686687
    Installed as C:\Users\jaro\platform-tools\adb.exe

It does! We can now start the server:

.. code-block:: plain

    C:\platform-tools> adb.exe -a -P 5037 nodaemon server

This command will run the ADB server in the foreground (I find it more
convenient than running it in the background as it tells me that the server is
indeed running on Windows). The :code:`-a` option will make the server listen on
all interfaces (important!) on port :code:`5037`. Specifying a port is
superfluous as the server by default starts on port :code:`5037` but I included
it for clarity reasons.

The above might trigger a Windows firewall alert that will ask if we want to set
up a rule for the ADB.

.. image:: {attach}images/windows_defender_dialog.png
   :alt: Windows Defender Firewall dialog.

From the perspective of accessing the ADB from WSL, it doesn't make much
difference. If we allow the access then we'll be able to access the ADB server
also from another computer on the network.

We now have a working ADB server running. Let's take care of the client next.

The client
----------

The first thing we need to do to establish a connection to the server is to
obtain the Windows IP address. There are two addresses we can use:

.. code-block:: plain
   :hl_lines: 6 13

    C:\Users\jaro>ipconfig

    Ethernet adapter vEthernet (WSL):

    ...
    IPv4 Address. . . . . . . . . . . : 172.20.96.1
    Subnet Mask . . . . . . . . . . . : 255.255.240.0
    Default Gateway . . . . . . . . . :

    Wireless LAN adapter Wi-Fi:

    ...
    IPv4 Address. . . . . . . . . . . : 192.168.0.203
    Subnet Mask . . . . . . . . . . . : 255.255.255.0
    Default Gateway . . . . . . . . . : 192.168.0.1

The first IP address is an address of a WSL virtual machine's interface
:code:`vEthernet (WS)` and in my case, it's **172.20.96.1**. The second address
is the address of my Wi-Fi interface and it's **192.168.0.203**.

We can use both of those addresses but in the case of the Wi-Fi address (or
other physical interfaces), we have to enable access to :code:`adb.exe` in
Windows Defender Firewall. Otherwise, this approach will not work. That is why
using the IP address of the virtual network interface is easier. Allowing
communication between Windows and Linux is this interface's purpose after all.

Getting the IP address of the server from Windows after every reboot is a little
inconvenient. Luckily this address is also available for Linux in
*/etc/resolv.conf* file [#]_:

.. code-block:: plain

    $ cat cat /etc/resolv.conf
    # This file was automatically generated by WSL...
    # [network]
    # generateResolvConf = false
    nameserver 172.20.96.1

Armed with the IP address of the server we can finally make the connection. We
can do this by executing :code:`adb` command with an IP address and TCP port
of the server like below:

.. code-block:: plain

    $ adb -H 172.20.96.1 -P 5037 devices
    List of devices attached
    0123456789A     device

Specifying the IP address/hostname and port each time we want to access a
device sounds tedious. There is a better way. We can make use of an
:code:`ADB_SERVER_SOCKET` environment variable:

.. code-block:: plain
   :hl_lines: 1

    $ export ADB_SERVER_SOCKET=tcp:$(cat /etc/resolv.conf | awk '/nameserver/ {print $2}'):5037
    $ adb devices
    List of devices attached
    0123456789A     device

We could even put this into our *~/.bashrc* and not worry about it anymore.

Summary
=======

While not instantaneously obvious, accessing Android devices using ADB from
Windows Subsystem for Linux is pretty easy. Once we set up the tools all it
takes is to execute two commands.

One on Windows to run the ADB server:

.. code-block:: plain

    C:\platform-tools> adb.exe -a -P 5037 nodaemon server

And one on Linux to connect the ADB client to the server:

.. code-block:: plain

    $ export ADB_SERVER_SOCKET=tcp:$(cat /etc/resolv.conf | awk '/nameserver/ {print $2}'):5037

After that, it just works.

Further reading
===============

.. [#] `Exceptions for using WSL 1 rather than WSL 2 <https://docs.microsoft.com/en-us/windows/wsl/compare-versions#exceptions-for-using-wsl-1-rather-than-wsl-2>`_
.. [#] `Android Debug Bridge (adb) <https://developer.android.com/studio/command-line/adb>`_
.. [#] `SDK Platform Tools release notes <https://developer.android.com/studio/releases/platform-tools>`_
.. [#] `Is there a way to install an older version of Android platform-tools? <https://stackoverflow.com/questions/53453640/is-there-a-way-to-install-an-older-version-of-android-platform-tools>`_
.. [#] `Accessing Windows networking apps from Linux (host IP) <https://docs.microsoft.com/en-us/windows/wsl/compare-versions#accessing-windows-networking-apps-from-linux-host-ip>`_