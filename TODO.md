# assemfuzz TODO

## Features

### Setup
+ As the Nand2Tetris software suite is also under the GPL I should be able to have the setup script grab the zipfile as part of setup without licensing issue

### Application
+ More helpful error messages

### Fuzzers
+ More robust invalid Hack assembly generation
+ More robust Hack assembly comment generation

## Testing
+ Replace pytest-runner with tox
+ Using continous integration (like TravisCI)
+ Add failure testing for both Compare and Fail handlers

## Documentation
+ Using a document generator (like Sphinx)

## Optional
+ Hack assembly state exhaustion (testing every possible line of Hack assembly sequentially)

## OTHER
+ I hope to extend this fuzzing platform to include more of Nand2Tetris stack