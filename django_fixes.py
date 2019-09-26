from PIL import Image as Img
from PIL import ExifTags
from io import BytesIO

from django.core.files import File
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile


def fix_image_orientation(image):
    if image:
        pilImage = Img.open(BytesIO(image.read()))
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif_data = pilImage._getexif()
        if exif_data:
            exif = dict(exif_data.items())
            if exif[orientation] == 3:
                pilImage = pilImage.rotate(180, expand=True)
            elif exif[orientation] == 6:
                pilImage = pilImage.rotate(270, expand=True)
            elif exif[orientation] == 8:
                pilImage = pilImage.rotate(90, expand=True)

            output = BytesIO()
            pilImage.save(output, format='JPEG')
            output.seek(0)
            return File(output, image.name)
    return image


class BetterImageFieldFile(ImageFieldFile):
    def save(self, name, content, save=True):
        content = fix_image_orientation(content)
        super().save(name, content, save)


class BetterImageField(ImageField):
    attr_class = BetterImageFieldFile
