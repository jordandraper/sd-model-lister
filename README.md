# Stable Diffusion Model Lister
[![forthebadge](http://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/built-by-developers.svg)](http://forthebadge.com)
[![forthebadge](http://forthebadge.com/images/badges/check-it-out.svg)](http://www.logan1x.me/Python-Scripts/)

The Stable Diffusion Model Lister helps you identify which models produce the best results after training by listing the models associated with the images in a specified directory. This script is particularly useful for users who have pruned their image outputs and want to trace back the models that generated the remaining images.

## Getting Started

Pre-built binaries are available for your convenience, but you can also download the source code and run it directly.

<!-- ### Prerequisites

```
Give examples
``` -->


### Binaries
- Supported Architecture
    - sd-model-lister-arm64 for **M1 macOS**
    - sd-model-lister-x64.exe for **Windows**

Download the latest [release](https://github.com/jordandraper/stable-diffusion-model-lister/releases) for your system and run from the command line as

```bash
sd-model-lister-x64.exe  [PATH_TO_STABLE_DIFFUSION_IMAGES]
```

### Source

Make sure you've already git installed. Then you can run the following commands to get the scripts on your computer:

macOS, Linux, and Windows:

```bash
git clone https://github.com/jordandraper/stable-diffusion-model-lister
cd stable-diffusion-model-lister
pip install -r requirements.txt
```

Then depending on how Python is called by your system PATH,
```
python sd_model_lister.py [PATH_TO_STABLE_DIFFUSION_IMAGES]
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Jordan Draper** - *Initial work* - [jordandraper](https://github.com/jordandraper)

<!-- See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project. -->

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

