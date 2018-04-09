# assem-fuzz

This is a project to make a fuzzing platform for the Hack assembly platform from the Nand2Tetris (http://nand2tetris.org/) series.

## Getting Started

Download the Nand2Tetris Software Suite to grab the reference assembler.

### Prerequisites

Nand2Tetris Software Suite: (http://nand2tetris.org/software.php)

### Installing

This will give an example of how to use the program by changing it to fuzz the reference compiler against itself on a linux system.

Unzip the software suite.

```
cd ~/Downloads
unzip nand2tetris.zip
```

Clone the repo.

```
git clone https://github.com/achermannagement/assem-fuzz.git
```

Make two directories.

```
cd assem-fuzz
mkdir mine
mkdir theirs
```

Move the tools into both folders as executable.

```
cd ..
cp -r nand2tetris/tools/* assem-fuzz/mine
cp -r nand2tetris/tools/* assem-fuzz/theirs
cd assem-fuzz
chmod +x mine/Assembler.sh
chmod +x theirs/Assembler.sh
```

Update the RUN_STRING in myprogram.py
```
RUN_STRING = "{}/{}.sh {}".format(MY_FOLDER, PATH_TO_ASSEMBLER, PATH_TO_TEST_FILE)
```

You should also update the my_cond function in myprogram.py so it extracts the line number from your error messages.
```
return int(err.split()[4][:-1])
```

Run the program

```
python3 assemfuzz.py
Test passed
All tests passed? True
```

### Configuration

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## TODO
See TODO.md

## Built With

* [pytest](https://docs.pytest.org/en/latest/) - Testing framework
* [setuptools](https://setuptools.readthedocs.io/en/latest/) - Packaging framework
* [pytest-cov]() - pytest coverage testing
* [pytest-pylint]() - pytest pylint testing

## Authors

* **Joshua Achermann** - *Initial work* - [achermannagement](https://github.com/achermannagement)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the GPL License - see the LICENSE file for details

## Acknowledgments

* Jeff Knupp's Open Sourcing a Python Project the Right Way
* Hat tip to anyone who's code was used
* Inspiration
* etc

