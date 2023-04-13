import argparse
import os
import sys

import piexif
import piexif.helper
from PIL import Image


def read_info_from_image(image):
    items = image.info or {}

    geninfo = items.pop('parameters', None)

    if "exif" in items:
        exif = piexif.load(items["exif"])
        exif_comment = (exif or {}).get("Exif", {}).get(
            piexif.ExifIFD.UserComment, b'')
        try:
            exif_comment = piexif.helper.UserComment.load(exif_comment)
        except ValueError:
            exif_comment = exif_comment.decode('utf8', errors="ignore")

        if exif_comment:
            items['exif comment'] = exif_comment
            geninfo = exif_comment

        for field in ['jfif', 'jfif_version', 'jfif_unit', 'jfif_density', 'dpi', 'exif',
                      'loop', 'background', 'timestamp', 'duration']:
            items.pop(field, None)
    return geninfo, items


def parse_parameter_string(parameter_string):
    return_dict = {}
    if parameter_string is not None:
        negative_prompt_index = parameter_string.rfind("Negative prompt: ")
        parameter_start_index = parameter_string.rfind("Steps: ")

        if parameter_start_index != -1:
            if parameter_start_index == 0:
                prompt = None
                negative_prompt = None
            elif negative_prompt_index == 0:
                prompt = None
                negative_prompt = parameter_string[:parameter_start_index].rstrip(
                    '\n')
            else:
                if negative_prompt_index != -1:
                    prompt = parameter_string[:negative_prompt_index].rstrip(
                        '\n')
                    negative_prompt = parameter_string[negative_prompt_index:parameter_start_index].rstrip(
                        '\n')

                else:
                    prompt = parameter_string[:parameter_start_index].rstrip(
                        '\n')
                    negative_prompt = None

            parameters = parameter_string[parameter_start_index:]
            remaining_parameters = parameters.split(', ')
        else:
            prompt = None
            negative_prompt = None
            parameters = parameter_string
            remaining_parameters = parameters.split(', ')

        return_dict.update(
            {'Prompt': prompt, 'Negative prompt': negative_prompt})
        parsed_parameters = {key.strip(): value.strip()
                             for key, value in (pair.split(': ') for pair in remaining_parameters)}
        return_dict.update(parsed_parameters)
    return return_dict


def parse_PNG_metadata(im):
    im.load()  # Needed only for .png EXIF data (see citation above)

    metadata = {}
    parameter_string = im.info.get('parameters')
    post_processing = im.info.get('postprocessing')
    extras = im.info.get('extras')

    metadata.update(parse_parameter_string(parameter_string))

    if post_processing is not None:
        post_processing = post_processing.split(', ')
        parsed_parameters = {key.strip(): value.strip()
                             for key, value in (pair.split(': ') for pair in post_processing)}
        metadata.update(parsed_parameters)

    if extras is not None:
        extras = extras.split(', ')
        parsed_parameters = {key.strip(): value.strip()
                             for key, value in (pair.split(': ') for pair in extras)}
        metadata.update(parsed_parameters)
    return metadata


def parse_JPEG_metadata(im):
    metadata = {}
    try:
        parameter_string = im.info['exif'].decode('utf_16_be').split("䔀")[1]
    except:
        parameter_string = im.info['exif'].decode().replace('\x00', '')
    metadata.update(parse_parameter_string(parameter_string))
    return metadata


def read_SD_metadata(filename):
    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#png

    im = Image.open(filename)
    if im.format == 'PNG':
        d = parse_PNG_metadata(im)
    elif im.format == 'JPEG':
        d = parse_JPEG_metadata(im)
    return d


def list_used_models(path):
    models = set()
    for root, dirs, files in os.walk(path):
        for file in files:
            params = read_SD_metadata(os.path.join(root, file))
            model = params.get('Model')
            if model is not None:
                models.add(model)
    for model in sorted(models):
        print(model)


def main():
    parser = argparse.ArgumentParser(prog="sd_model_lister",    description="List model(s) used to generate Stable Diffusion outputs.",
                                     epilog="Thanks for using %(prog)s! :)",
                                     )
    parser.add_argument(
        "path", nargs="?", help="take the path to the target directory")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    args = parser.parse_args()
    if os.path.exists(args.path):
        list_used_models(args.path)
    else:
        print('Your provided path is not recognized or doest not exist. Please try again.')


if __name__ == "__main__":
    main()
