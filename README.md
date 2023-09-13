
# VagrantBoxDownloader

VagrantBoxDownloader is a Python script that allows you to download Vagrant boxes from the Vagrant cloud ("https://app.vagrantup.com/boxes/search?provider=virtualbox") using web scraping (beautiful soup4). It helps you quickly fetch Vagrant boxes and save them locally for offline use or personal development projects.

By default, it just downloads the box that Virtualbox is set as the provider. and it creates the box file in this format "(box-name).(version).box" and then creates all of your box's download links as a TxT file! 

you can modify the script to download the box of your choice! (eg. libvirt, lxc)
## Prerequisites

- Python >=3.9
- pip3
- Dependencies: listed in ('requirements.txt')

## Installation

Clone this repository to your local machine:

```
git clone https://github.com/majidv7/VagrantBoxDownloader.git
```

Install Dependencies
```
cd VagrantBoxDownloader
```
```
pip3 install -r requirements.txt
```
## Usage

```
python3 vagrant_box_downloader.py
```
Follow the on-screen instructions to enter the page number or range and start the download process.
