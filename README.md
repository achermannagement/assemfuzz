# assemfuzz
This is a project to make a fuzzing platform for the Hack assembly language from the Nand2Tetris (http://nand2tetris.org/) course. A fuzzer generates vast quantities of random (valid or invalid) code in order to test program robustness. It is especially good at detecting inputs that crash a program. However, as we are provided a reference Hack assembler we can also use fuzzing to ensure program correctness.

## Features
* Largely automated fuzzing platform
* Excellent coverage of Hack assembly structures (90%+ in one pass)
* Uses predefined and randomly generated labels
* Error logging
* Multiprocessor support
* Can additionally check for assembler error handling

## Getting Started
Download the Nand2Tetris Software Suite to grab the reference assembler.

### Prerequisites
Nand2Tetris Software Suite: (http://nand2tetris.org/software.php)

### Installing
Download the Nand2Tetris software suite (this guide assumes it is in the ~/Downloads directory).

Clone the repo.

    git clone https://github.com/achermannagement/assemfuzz.git

Use the setup script.

### Fuzzing Your Assembler
Run

    python3 setup.py prepare --path ~/Downloads/nand2tetris.zip

to in order to make the testing directories.

Move your assembler into the mine/ directory.

Update `RUN_STRING` in myprogram.py to run your assembler

You should also update the `my_cond` function in myprogram.py so it extracts the line number from your error messages OR make it `None` if your program does not return a line number in its error messages.

Run the program

    python3 assemfuzz.py

If your assembler produces the same output as the reference assembler for the fuzzed file, you will get a message saying tests passed.

This only runs a single assembly file against your assembler though so you might want to run more to have more confidence in your assembler, run

    python3 assemfuzz.py -n 1000

to have a thousand passes done.

#### Failure Handling
If your assembler output does not match the reference compiler, the fuzzing will halt and a note is made in the error log. The offending fuzzing file should remain in the mine directory so you can investigate the issue manually.

### Configuration
All configuration for assemfuzz is through arguments.
You can run the program with the help flag in order to see what options are available.

## Running the tests
PyTest and Tox are used to run tests in the setup file.

First run the prepare command to extract the software suite.

    python3 setup.py prepare --path nand2tetris.zip --test 1

Run the tests with the path to software suite as an argument.

    tox

You can also run pytest directly.

    python3 -m pytest

### Coverage
An argument can be provided in the setup script to enable coverage testing.

    python3 -m pytest --cov

### Pylint
Pylint is used to measure code quality in this project. You can run it with

    python3 -m pytest --pylint

## TODO
See TODO.md

## Contributing
assemfuzz is not envisioned to become a large project but if you are keen to help feel free to fork this project or report an issue for bugs or desired features

## Built With

* [pytest](https://docs.pytest.org/en/latest/) - Testing framework
* [setuptools](https://setuptools.readthedocs.io/en/latest/) - Packaging framework
* [pytest-cov](https://pypi.org/project/pytest-cov/) - pytest coverage testing
* [pytest-pylint](https://pypi.org/project/pytest-pylint/) - pytest pylint plugin

## Authors

* **Joshua Achermann** - *Initial work* - [achermannagement](https://github.com/achermannagement)

See also the list of [contributors](https://github.com/achermannagement/assemfuzz/contributors) who participated in this project.

## License

This project is licensed under the GPL License - see the LICENSE file for details

## Acknowledgments
* [Noam Nisan & Shimon Schocken's Nand2Tetris Course and Book](http://nand2tetris.org/)
* [Jeff Knupp's Open Sourcing a Python Project the Right Way](https://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/)
* [PurpleBooth's README-Template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [yebblies for inspiration](https://github.com/yebblies)
