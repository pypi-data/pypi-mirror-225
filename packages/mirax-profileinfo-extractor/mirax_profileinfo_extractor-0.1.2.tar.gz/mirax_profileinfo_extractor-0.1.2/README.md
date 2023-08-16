## Mirax profile info extractor

This simple lib helps extract extra information from Mirax files that are not provided by other open source libraries like
[Openslide](https://github.com/openslide/openslide).

## How to install?

`pip install mirax_profileinfo_extractor`

## How to build?

Run `make` and find the built package in the `dist` folder.

## How to use?

Add the lib to your project from pypi and call the function `get_mirax_profile_info` passing the path to the file as parameter.

```python
from mirax_profileinfo_extractor.extractor import get_mirax_profile_info

mirax_info = get_mirax_profile_info('path/to/file.mrxs')
print(mirax_info)
```

## License

MIT License

Copyright (c) [2023] [Pathologywatch]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.