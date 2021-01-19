import os

import pytest

from PIL import Image, ImageColor, ImageDraw, SvgImagePlugin

from .helper import assert_image_equal, assert_image_similar, hopper

EXTRA_DIR = "Tests/images/svg"


def test_quick():
    ImageColor.colormap['currentcolor'] = ImageColor.colormap['black']

    for fn in ['path-lines']:
        im = Image.new('RGBA', (24, 24))
        draw = ImageDraw.Draw(im)
        SvgImagePlugin.draw_svg_file(os.path.join(EXTRA_DIR, fn+'.svg'), draw, im.size, '#00000000')
        im.show()
        compare = Image.open(os.path.join(EXTRA_DIR, fn+'.png'))
        compare.show()
        show_image = Image.new('RGBA', (24*3, 24), 'cyan')
        show_image.paste(im, (6, 0, 30, 24))
        show_image.paste(compare, (42, 0, 66, 24))
        show_image.show()

        assert im.size == (24, 24)
        assert_image_similar(im, compare, 50)

def xtest_sanity():
    # Arrange
    # Created with Inkscape --export-type=png Tests/images/svg/path-lines.svg
    test_root = "Tests/images/svg/path-lines"
    test_file = test_root + '.svg'
    compare = Image.open(test_root + '.png')
    compare.show()

    # Act
    with Image.open(test_file) as im:
        im.show()

        # Assert
        assert im.size == (24, 24)

        assert_image_similar(im, compare, 5)  # visually verified

    invalid_file = "Tests/images/flower.jpg"
    with pytest.raises(SyntaxError):
        SvgImagePlugin.SvgImageFile(invalid_file)


def xtest_im1():
    with Image.open("Tests/images/sunraster.im1") as im:
        with Image.open("Tests/images/sunraster.im1.png") as target:
            assert_image_equal(im, target)


@pytest.mark.skipif(
    not os.path.exists(EXTRA_DIR), reason="Extra image files not installed"
)
def xtest_others():
    files = (
        os.path.join(EXTRA_DIR, f)
        for f in os.listdir(EXTRA_DIR)
        if os.path.splitext(f)[1] in (".sun", ".SUN", ".ras")
    )
    for path in files:
        with Image.open(path) as im:
            im.load()
            assert isinstance(im, SunImagePlugin.SunImageFile)
            target_path = f"{os.path.splitext(path)[0]}.png"
            # im.save(target_file)
            with Image.open(target_path) as target:
                assert_image_equal(im, target)
