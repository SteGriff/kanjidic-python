# kanjidic-python

Processes kanjidict2.xml into a JSON dictionary.

This project is forked from <https://github.com/onlyskin/kanjiapi.dev> and completely derived from it. I hacked and slashed it and haven't improved it at all. Please check out onlyskin's project. It will also help you understand some of the code that's removed or unused in this fork.

## Setup

You need Python 3 and `make`. You can install `make` on Windows with `choco install make` if you have Chocolatey.

Install python libraries using requirements.txt

You will also need to `pip install`:
 * `ujson` <https://pypi.org/project/ujson/#files>
 * `lxml` <https://pypi.org/project/lxml/#files>
 
...both of which will require wheels (pre-built binaries) on Windows (probably). You can download the wheels from the links above. Pick the one best for your version of Python and your architecture (i.e. `win_amd64`).

I used ` ujson-4.0.1-cp39-cp39-win_amd64.whl` and `lxml-4.5.2-cp39-cp39-win_amd64.whl`.

You can then run `pip install <whl file>`.

Save and extract the kanji dictionary file `kanjidic2.xml` from [EDRDG](http://www.edrdg.org/wiki/index.php/KANJIDIC_Project) to the root of the project.


## Build

Run `make` to build the JSON output, which will go to the `out` directory.

## Output

An example output JSON is in this gist: [kanji.json](https://gist.github.com/SteGriff/07f5b89599554b5fa185587d3461b90f) and is 1.8Mb.


