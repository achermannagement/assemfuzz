# assemfuzz TODO

## Project
+ Fix lint issues
+ Improved git development flow
+ Upload package to PyPi

## Performance
+ Multiprocessing may be implemented in a more performant way

## Features

### Setup
+ As the Nand2Tetris software suite is also under the GPL, I should be able to have the setup script grab the zipfile as part of setup without licensing issue

### Application
+ More helpful error messages

### Fuzzers
+ More robust invalid Hack assembly generation
+ More robust Hack assembly comment generation

## Testing
+ Use continous integration (like TravisCI)
+ Add failure testing for both Compare and Fail handlers
+ Tests invoking \_\_main\_\_.py directly

## Documentation
+ Use a document generator (like Sphinx)

## Optional
+ Hack assembly state exhaustion (testing every possible line of Hack assembly sequentially)

## Other
+ I hope to extend this fuzzing platform to include more of Nand2Tetris stack
+ Originally I planned to include an example assembler (my Java implementation) but Java is insanely easy to decompile and it would be basically posting the solution which is detrimental to the purpose of education, so instead I included instructions to use the reference assembler