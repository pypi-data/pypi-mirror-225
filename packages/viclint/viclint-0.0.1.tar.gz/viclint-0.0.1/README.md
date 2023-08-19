# viclint

viclint is the official code linter for [VisionScript](https://visionscript.dev).

You can use `viclint` to ensure your code conforms to the VisionScript style.

## Installation

To install viclint, run the following command:

```bash
pip install viclint
```

## Usage

To use viclint, run:

```bash
viclint <path>
```

`<path>` can be a single file or a directory whose `.vic` files you want to lint.

A file must end in `.vic` to be linted.

Here is an example output from the linter:

```
🪄 Linting ./camera.vic...
✨ Your code is now prettier! ✨
```

If the lint failed, you will see an error message:

```
🪄 Linting ./camera.vic...
🚨 ./camera.vic failed to lint.
```

## License

This project is licensed under an [MIT license](LICENSE).

## Related Resources

- [VisionScript Website and Documentation](https://visionscript.dev)
- [VisionScript GitHub repository](https://github.com/capjamesg/visionscript)
- [VisionScript Visual Studio Code extension](https://github.com/capjamesg/)