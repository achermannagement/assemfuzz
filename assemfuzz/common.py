import os
import pathlib
import glob
import shutil
import zipfile
import stat

import assemfuzz.definitions

ZIP_PATH = 'nand2tetris.zip'
MY_FOLDER = assemfuzz.definitions.MY_FOLDER
THEIR_FOLDER = assemfuzz.definitions.THEIR_FOLDER

def make_folders():
    """Make the empty testbench"""
    pathlib.Path(MY_FOLDER).mkdir(parents=True, exist_ok=True)
    pathlib.Path(THEIR_FOLDER).mkdir(parents=True, exist_ok=True)

def prepare_tests(path):
    """Prepare for testing by extracting the refernce assembler into both folders"""
    make_folders()
    extract_toolchain(path, MY_FOLDER)
    extract_toolchain(path, THEIR_FOLDER)

def extract_my_toolchain(tool_chain):
    extract_toolchain(tool_chain, MY_FOLDER)

def extract_their_toolchain(tool_chain):
    extract_toolchain(tool_chain, THEIR_FOLDER)

def extract_toolchain(tool_chain, folder):
    """Extract from zipfile into the selected folder and makes the files inside executable"""
    if tool_chain is not None:
        with zipfile.ZipFile(tool_chain, 'r') as assem_zip:
            assem_zip.extractall(folder)
            source_dir = os.path.join(folder, "nand2tetris", "tools")
            dest_dir = folder
            for filename in glob.glob(os.path.join(source_dir, '*'), recursive=True):
                shutil.move(filename, dest_dir)
            shutil.rmtree(os.path.join(folder, "nand2tetris"))
            # need to chmod to allow executing
            for root, _, files in os.walk(dest_dir):
                for curr in files:
                    curr = os.path.join(root, curr)
                    st = os.stat(curr)
                    os.chmod(curr, st.st_mode | stat.S_IEXEC)

def clean_testbench():
    """Clean the testbench"""
    shutil.rmtree(MY_FOLDER)
    shutil.rmtree(THEIR_FOLDER)
