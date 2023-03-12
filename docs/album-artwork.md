---
title: Album artwork
nav_order: 3
---

# Album artwork
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

* TOC
{:toc}

---

## Introduction

This section will help you set up automatic album art uploading so the album artwork will show up in your status instead of the foobar logo.
This is achieved by uploading album artwork to your hosting service of choice and using the url it provides as the image.

## Setup

Firstly make sure you have version 1.3.0 or later of this plugin installed.
Then open up Preferences (Ctrl + P or File -> Preferences) and from there
under the Tools section there should be a section for Discord Rich Presence Integration.
Click on that and go to the advanced tab. At the bottom there should be a section called artwork.

To enable using the album artwork in your status you need to make sure the Upload artwork checkbox is checked.  
Then, in the Artwork upload command field, you need to write the full path to the program with the necessary parameters, that will handle the uploading.
It is recommended that you surround any paths with quotes, as paths containing spaces will most likely cause problems.
The exact commands that you need to input here change based on the script, and they are explained with more detail in the [Upload scripts](#upload-scripts) section.  
The last option is called Artwork identifier key, and it is better left untouched in most cases. What it does is explained in more detail in the [Descriptions of options](#descriptions-of-options) section.

Below is an image of an example configuration using a python script for uploading.

![Artwork upload settings]({{ site.baseurl }}/assets/img/artwork_upload_settings.png)



## Upload scripts

This section will contain pre-made upload scripts for ease of use that are maintained and updated, if at all, separately from this plugin by their respective authors.
Use them at your own discretion, we are not responsible for any damages or other problems the scripts might cause.

### Imgur
Scripts to use if you want to upload album art to [https://imgur.com](https://imgur.com)

### Standalone imgur uploader
This one is the easiest to install and use as it's just a single exe that you need download.
You can find the latest release here [https://github.com/s0hv/rust-imgur-upload/releases/latest](https://github.com/s0hv/rust-imgur-upload/releases/latest)
Then, to use it, just copy the path to the Artwork upload command like so `"C:\path\to\imgur-uploader.exe"`.
After this the album art feature should start working.

### Imgur upload script for Python 3.7 or later
This one requires a bit of technical knowledge but it's easier to customize for other needs if you have basic coding skills. 
You need to have python 3.7 or later installed along with the requests library.
Also, you need to obtain an imgur API token from here [https://api.imgur.com/oauth2/addclient](https://api.imgur.com/oauth2/addclient) (more instructions can be found here [https://apidocs.imgur.com/#intro](https://apidocs.imgur.com/#intro)).
Fill the form and for authorization type make sure to select "OAuth 2 authorization without a callback URL".
After obtaining the API client id you can move on to the code.

The code can be found from [this gist](https://gist.github.com/s0hv/5c07cfb4b939ee619d0efcc047991ceb).

After saving the script on your machine, replace the part that says 
`Insert imgur api client id here` with the client id you obtained earlier while keeping the single quotes in place (`'`)

After you have installed python, saved the script on your machine and inserted the client id to the script, you need to set the Artwork upload command as follows.
`"C:\path\to\python" "C:\path\to\imgur_upload.py"`

After these steps you should start seeing the album art show up in your discord status.

### Catbox
Scripts to use if you want to upload album art to [https://catbox.moe](https://catbox.moe)

### Catbox uploader for Powershell 7
To use this script you must have Powershell 7 installed (might work with 6, but I have not tested this). 
One way of installing it is with [winget](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.3#winget)
Also, for full UTF-8 support you must enable UTF-8 support from 
`Language -> Administrative language settings -> Change system locale -> Make sure this option is checked "Beta: Use Unicode UTF-8 for worldwide language support".`

The code can be found from [this gist](https://gist.github.com/vt-idiot/8a7161a48dc6f7f7719423e938217267).

After downloading set the Artwork upload command to the following value (assumes powershell 7 has been installed in the default location)
`"C:\Program Files\PowerShell\7\pwsh.exe" "C:\path\to\catbox.ps1"`

### Catbox uploader for Python 3.7 or later
The python setup for this is the same as for [imgur script](#imgur-upload-script-for-python-37-or-later).
The code can be found from [this gist](https://gist.github.com/mechabubba/db1200c05fbbecf753b23c92ee8e9271).

After you have installed python and saved the script on your machine, you need to set the Artwork upload command as follows.
`"C:\path\to\python" "C:\path\to\catbox_upload.py"`

## Descriptions of options

This section contains brief descriptions for the different options on the Artwork section in the settings of this plugin.

**Upload artwork** checkbox determines whether album art is uploaded and used as the image or not.

**Artwork upload command** contains the command that will be run to upload the image.
If this field is left empty and the checkbox is checked, the plugin will use the album art for images
that have already been uploaded but the default image will be shown otherwise.

**Artwork identifier key** determines a unique key based on properties on the track,
which will be used to determine if the track shares album artwork with another track.
By default, the value is `%album artist% - $if2([%album%],%title%) [ - %discnumber%]`
which assumes that every track on the same disc of an album has the same artwork.
This can be changed if necessary. The value accepts normal foobar2000 query syntax.


## Troubleshooting

#### I set up everything but it still is not working
There is most likely a problem with your upload script. Open up the console from View -> Console and start playing a new track.
Lines prefixed with "Discord Rich Presence Integration" are logs from this plugin, and they can be used to troubleshoot what is going wrong and where.

#### I changed the artwork, but it was not updated on discord
This is because the plugin saves the url after it has uploaded the image.
It won't update this url unless you manually tell it to clear the old url.
This can be done by selecting all of the tracks that need resetting of the url, 
right-clicking and from the Discord Rich Presence menu selecting "Clear artwork".
You can instantly regenerate the urls by clicking "Generate artwork url" from the same menu, or by simply playing the tracks.

## Technical details

This section is meant for those who want to create their own upload scripts.
The installation script will receive a filepath to the album art encoded in UTF-8 from the stdin pipe.
This filepath might point to a temporary file or a permanent file depending on where the file is originally stored.
It is best to assume that the file given to the process handling the uploading will be gone after the process exits.

The rough pipeline of the uploading process is as follows.
The plugin means this foobar2000 plugin and the upload process is the program that is run to upload the image.

1. The plugin writes the full filepath to the stdin of the upload process.
2. The upload process should then handle generating a web url that contains a copy of the given artwork file.
3. The plugin then waits 10 seconds for the upload process to write anything to the stdout pipe.
    1. If something is written to stdout pip the plugin reads at maximum 2048 bytes of it.
    2. If nothing is written or the process times out, it is considered a failure.
4. The plugin check the exit code of the upload process and the resulted value is treated as an error message if the exit code is nonzero.
