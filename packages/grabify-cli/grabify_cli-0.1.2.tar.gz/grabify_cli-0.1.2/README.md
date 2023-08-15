# Grabify

[![PyPI - Version](https://img.shields.io/pypi/v/grabify-cli.svg)](https://pypi.org/project/grabify-cli)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/grabify-cli)](https://pypi.org/project/grabify-cli)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/grabify-cli.svg)](https://pypi.org/project/grabify-cli)

Command-line tool that allows you to download images and metadata from Spotify.

## Installation

To install Grabify, run the following command:

```
pip install grabify-cli
```

## Usage

To use Grabify, run the following command:

```
grabify <url> [PARAMS]
```

Where `<url>` is the Spotify URL of the track or album you want to download, and `PARAMS` are optional parameters.

## Example

### Data

There is example how to download data for the track "Bending Hectic" by The Smile

```
grabify data https://open.spotify.com/track/2tA4gq8tO9TPPPpbgK5n4
```

This will save the data to the file `Downloads/grabify/bending_hectic.json`.

### Artwork

For example, to download the artwork for the album "Currents" by Tame Impala, you would run the following command:

```
grabify art https://open.spotify.com/album/79dL7FLiJFOO0EoehUHQBv
```

This will save the artwork to the file `Downloads/grabify/Currents.jpg`.

## Contributing

Contributions are welcome! Please submit pull requests to the [GitHub repository](https://github.com/woidzero/grabify).

## Support

For support, email <a href="mailto://woidzerov@gmail.com">woidzerov@gmail.com</a>

## License

`grabify` is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
