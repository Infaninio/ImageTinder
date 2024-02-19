# ImageTinder
Quick and dirty tool to sort Images

ImageTinder can be used to sort a huge amout of images into two different groups (Keep and Trash).

You open a folder with your images. The tool will display one image after the other.
You can reject or accept the image.
If you accept the image it will bi marked as checked by adding the string '_checked' to the filename.
If you reject the image it will be moved to a different directory. ('Trash' Folder in the parent directory of your current folder.)

You can control the tool also with the keyboard. The letter 'A' will trash the image, the letter 'D' will check the image.

## WebApp

```shell
flask --app WebUi run --debug # Start for live debugging/change
```


# TODOs
- Possibility to view videos
    - skip video frames
- Handle out of images properly
- Location
- Detect newly added images even when loading config file
- Get list of all images, based on filter/reviews.
- Metadata for .itsf files
    - Project name
- Get date from filename if not in metadata
