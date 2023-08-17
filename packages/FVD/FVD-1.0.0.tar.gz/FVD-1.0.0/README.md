# Facebook Video Downloader

Under construction! Not ready for use yet! Currently experimenting and planning!

Developed by Razi Ahmed Iqbal (c) 2023

## How To Install
    pip install Facebook-Video-Downloader
## Usage
```python
from fbd import FacebookVideoDownloader as FVD
```
Calling module and Initializing Class
```python
video_url = 'https://www.facebook.com/facebook/videos/10153231379946729/'
instance = FVD.FacebookVideoDownloader('https://www.facebook.com/facebook/videos/10153231379946729/')
```
Getting Video Title
```python
title = instance.get_title()
```
**instance.get_title()** returns a string

Getting Video URL
```python
streams = instance.get_streams()
```
**instance.get_streams()** returns json response 

```json
{
    "sd_url": "https://scontent-cdg4-3.xx.fbcdn.net/v/t42.1790-4/10749875_10153231382106729_1430298193_n.mp4?_nc_cat=111&ccb=1-7&_nc_sid=985c63&efg=eyJ2ZW5jb2RlX3RhZyI6InNkIn0u00253D&_nc_ohc=Vrt1J_cpc68AX86r-bn&_nc_ht=scontent-cdg4-3.xx&oh=00_AfDEV-Td-tKaVdHT7cqC_h0uCQsoLL2SEGa_tu6GjJkVyw&oe=64E2121B",
    "hd_url": "https://scontent-cdg4-2.xx.fbcdn.net/v/t43.1792-4/10435682_10153231382156729_130140491_n.mp4?_nc_cat=103&ccb=1-7&_nc_sid=985c63&efg=eyJ2ZW5jb2RlX3RhZyI6ImhkIn0u00253D&_nc_ohc=ggUWOkt7j8gAX_mEBNj&_nc_ht=scontent-cdg4-2.xx&oh=00_AfBvZcnrk_WDVGt5mzp4BGkHTWOH8_DRUGAPI9H4oLDK2g&oe=64DCECE6"
}
```

Directly Downloading Video in the Directory
```python
streams = instance.download()
```
**instance.download()** downloads the available and best quality video
