import argparse
import os
import sys

from PIL import Image


def read_SD_metadata(filename):
    # https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#png

    im = Image.open(filename)
    im.load()  # Needed only for .png EXIF data (see citation above)

    parameters = im.info['parameters'].split('\n')
    prompt = parameters[0]
    remaining_parameters = [x.split(', ') for x in parameters[1:]]
    d = {'Prompt': prompt.strip()}
    for pairs in remaining_parameters:
        n = {key.strip(): value.strip()
             for key, value in (pair.split(': ') for pair in pairs)}
        d.update(n)
    return d


def list_used_models(path):
    models = set()
    for root, dirs, files in os.walk(path):
        for file in files:
            try:
                params = read_SD_metadata(os.path.join(root, file))
                model = params['Model']
                models.add(model)
            except:
                pass
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
