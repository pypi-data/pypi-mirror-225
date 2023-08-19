![A program documented with vicdocs](https://github.com/capjamesg/vicdocs/blob/main/vicdocs.png?raw=true)

# vicdocs

`vicdocs` is a documentation generator for [VisionScript](https://visionscript.dev).

`vicdocs` reads a VisionScript file (`.vic`), parses the comments, and generates a HTML document with:

1. The program code;
2. The title, description, and author information specified (if any);
3. A list of function definitions.

`vicdocs` only works with single-file scripts.

## Installation

`vicdocs` is available on PyPI, so you can install it with `pip`:

```bash
pip install vicdocs
```

## Usage

To generate a documentation file, run `vicdocs` with the path to the VisionScript file as the first argument:

```bash
vicdocs file.vic
```

This will generate a HTML file in a `{file}-docs`, where `{file}` is the name of the VisionScript file for which you are generating documentation.

## License

This project is licensed under an [MIT license](LICENSE).