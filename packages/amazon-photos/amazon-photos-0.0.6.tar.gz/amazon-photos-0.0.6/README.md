# Amazon Photos API

## Table of Contents

- [Amazon Photos API](#amazon-photos-api)
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
- [Setup](#setup)
- [Query Syntax](#query-syntax)
- [Examples](#examples)

## Installation

```bash
pip install amazon-photos
```

## Setup

An `.env` file must be created with these cookie values.

```text
session-id=...
ubid-acbca=...
at-acbca=...
```

## Query Syntax

> For valid **location** and **people** IDs, see the results from the `aggregations()` method.

Example query:

#### `drive/v1/search`
```text
type:(PHOTOS OR VIDEOS)
AND things:(plant AND beach OR moon)
AND timeYear:(2019)
AND timeMonth:(7)
AND timeDay:(1)
AND location:(CAN#BC#Vancouver)
AND people:(CyChdySYdfj7DHsjdSHdy)
```

#### `/drive/v1/nodes`
```
kind:(FILE* OR FOLDER*)
AND contentProperties.contentType:(image* OR video*)
AND status:(AVAILABLE*)
AND settings.hidden:false
AND favorite:(true)
```

## Examples

```python
from amazon_photos import Photos

ap = Photos()

# get entire Amazon Photos library
ap.query("type:(PHOTOS OR VIDEOS)")

# query Amazon Photos library for specific photos/videos
ap.query("type:(PHOTOS OR VIDEOS) AND things:(plant AND beach OR moon) AND timeYear:(2023) AND timeMonth:(8) AND timeDay:(14) AND location:(CAN#BC#Vancouver)")

# convenience method to get all photos
ap.photos()

# convenience method to get all videos
ap.videos()

# get current usage stats
ap.usage()

# get all identifiers calculated by Amazon.
ap.aggregations(category="all")

# get specific identifiers calculated by Amazon.
ap.aggregations(category="location")

# get trash bin contents
ap.trashed()

# move a batch of images/videos to the trash bin
ap.trash([...])

# restore a batch of images/videos from the trash bin
ap.restore([...])

# upload a batch of images/videos
ap.upload([...])

# download a batch of images/videos
ap.download([...])

# permanently delete a batch of images/videos.
ap.delete([...])
```

## Common Paramters

| name            | type | description                                                                                                                                                                                                                                               |
|:----------------|:-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ContentType     | str  | `"JSON"`                                                                                                                                                                                                                                                  |
| _               | int  | `1690059771064`                                                                                                                                                                                                                                           |
| asset           | str  | `"ALL"`<br/>`"MOBILE"`<br/>`"NONE`<br/>`"DESKTOP"`<br/><br/>default: `"ALL"`                                                                                                                                                                              |
| filters         | str  | `"type:(PHOTOS OR VIDEOS) AND things:(plant AND beach OR moon) AND timeYear:(2019) AND timeMonth:(7) AND location:(CAN#BC#Vancouver) AND people:(CyChdySYdfj7DHsjdSHdy)"`<br/><br/>default: `"type:(PHOTOS OR VIDEOS)"`                                   |
| groupByForTime  | str  | `"day"`<br/>`"month"`<br/>`"year"`                                                                                                                                                                                                                        |
| limit           | int  | `200`                                                                                                                                                                                                                                                     |
| lowResThumbnail | str  | `"true"`<br/>`"false"`<br/><br/>default: `"true"`                                                                                                                                                                                                         |
| resourceVersion | str  | `"V2"`                                                                                                                                                                                                                                                    |
| searchContext   | str  | `"customer"`<br/>`"all"`<br/>`"unknown"`<br/>`"family"`<br/>`"groups"`<br/><br/>default: `"customer"`                                                                                                                                                     |
| sort            | str  | `"['contentProperties.contentDate DESC']"`<br/>`"['contentProperties.contentDate ASC']"`<br/>`"['createdDate DESC']"`<br/>`"['createdDate ASC']"`<br/>`"['name DESC']"`<br/>`"['name ASC']"`<br/><br/>default: `"['contentProperties.contentDate DESC']"` |
| tempLink        | str  | `"false"`<br/>`"true"`<br/><br/>default: `"false"`                                                                                                                                                                                                        |             |
