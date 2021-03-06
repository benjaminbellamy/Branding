#!/bin/python
import os
import subprocess
import platform
from pathlib import Path

langs_and_fonts = {
    'de-DE': 'Sarabun-Bold',
    'en-US': 'Sarabun-Bold',
    'fr-FR': 'Sarabun-Bold',
    'he-IL': 'Arimo-Bold',
    'nl-NL': 'Sarabun-Bold',
    'it-IT': 'Sarabun-Bold',
    'es-ES': 'Sarabun-Bold'
}


def generate_text(text, font):
    print(text)
    os.system(
        "convert -size 1698x750 xc:none -gravity Center -pointsize 130 -fill '#167df0' -font "
        + font
        + ' -annotate 0 "'
        + text
        + '" /tmp/text.png')


def generate_tablet_text(text, font):
    print(text)
    os.system(
        "convert -size 1730x350 xc:none -gravity Center -pointsize 80 -fill '#167df0' -font "
        + font
        + ' -annotate 0 "'
        + text
        + '" /tmp/text.png')


def simple_phone(text, background_file, screenshotFile, outputFile, font):
    generate_text(text, font)
    os.system('convert templates/' + background_file
              + ' templates/phone.png -geometry +0+0 -composite '
              + screenshotFile + ' -geometry +306+992 -composite '
              + '/tmp/text.png -geometry +0+0 -composite '
              + outputFile)


def simple_tablet(text, screenshot_file, output_file, font):
    generate_tablet_text(text, font)
    os.system('convert ' + screenshot_file + ' -resize 1285 "/tmp/resized-image.png"')
    os.system('convert templates/tablet.png '
              + '/tmp/resized-image.png -geometry +224+459 -composite '
              + '/tmp/text.png -geometry +0+0 -composite '
              + output_file)


def two_phones(text, raw_screenshots_path, output_file, font):
    generate_text(text, font)
    os.system('convert templates/background2.png '
              + 'templates/twophones-a.png -geometry +0+10 -composite '
              + raw_screenshots_path + '/03a.png -geometry +119+992 -composite '
              + 'templates/twophones-b.png -geometry +0+0 -composite '
              + raw_screenshots_path + '/03b.png -geometry +479+1540 -composite '
              + '/tmp/text.png -geometry +0+0 -composite '
              + output_file)


def generate_screenshots(language, font):
    Path('output/' + language).mkdir(parents=True, exist_ok=True)
    with open('raw/' + language + '/texts.txt') as textDefinitions:
        texts = textDefinitions.readlines()
    raw_screenshots_path = 'raw/' + language
    output_path = 'output/' + language

    if not Path(raw_screenshots_path + '/00.png').is_file():
        raw_screenshots_path = 'raw/en-US'

    simple_phone(texts[0], 'background1.png', raw_screenshots_path + '/00.png', output_path + '/00.png', font)
    two_phones(texts[3], raw_screenshots_path, output_path + '/01.png', font)
    simple_phone(texts[1], 'background1.png', raw_screenshots_path + '/01.png', output_path + '/02.png', font)
    simple_phone(texts[2], 'background2.png', raw_screenshots_path + '/02.png', output_path + '/03.png', font)
    simple_phone(texts[4], 'background1.png', raw_screenshots_path + '/04.png', output_path + '/04.png', font)
    simple_phone(texts[5], 'background2.png', raw_screenshots_path + '/05.png', output_path + '/05.png', font)
    if len(texts) == 7:
        simple_tablet(texts[6], raw_screenshots_path + '/tablet.png', output_path + '/tablet.png', font)
    os.system('mogrify -resize 1120 "' + output_path + '/0*.png"')


def check_os():
    """Currently only working on Linux."""
    return platform.system() == 'Linux'


def check_packages():
    """ImageMagicks convert and morgify are required."""
    common = b'Version: ImageMagick'
    try:
        return common in subprocess.check_output(['convert', '-version']) and common in subprocess.check_output(
            ['mogrify', '-version'])
    except subprocess.CalledProcessError:
        return False


def check_fonts():
    """Check if required fonts are installed."""
    try:
        for font in langs_and_fonts.values():
            if bytes(font.encode()) not in subprocess.check_output(['fc-list', '-v']):
                return False
    except subprocess.CalledProcessError:
        return False
    return True


if __name__ == '__main__':
    assert (check_os())
    assert (check_packages())
    assert (check_fonts())
    for lang, font in langs_and_fonts.items():
        generate_screenshots(lang, font)
