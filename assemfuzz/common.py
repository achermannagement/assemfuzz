"""
helpful functions that help setup

Copyright (C) 2017  Joshua Achermann

assem-fuzz is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

email: joshua.achermann@gmail.com
"""
import os
import pathlib
import glob
import shutil
import zipfile
import stat
import subprocess

from assemfuzz.definitions import (
    MY_FOLDER, THEIR_FOLDER, PATH_TO_ASSEMBLER,
    COMP_RUN_STRING_LINUX)

ZIP_PATH = 'nand2tetris.zip'

def their_cond(err):
    """extract error line from reference assembler error message"""
    return int(err.split()[2][:-1])

def their_assembler(input_path, windows=False):
    return run(THEIR_FOLDER, input_path, windows)

def run(folder, input_path, windows):
    """Run the reference assembler in given folder on given file"""
    if not windows:
        ext = ".sh"
    else:
        ext = ".bat"
    run_string = os.path.join(
        folder, PATH_TO_ASSEMBLER + ext)
    result = subprocess.run(
        COMP_RUN_STRING_LINUX.format(
            run_string, os.path.join(folder, input_path)),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return result

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
    """Extract given zipfile to mine/ folder"""
    extract_toolchain(tool_chain, MY_FOLDER)

def extract_their_toolchain(tool_chain):
    """Extract given zipfile to their/ folder"""
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
                    st_prev = os.stat(curr)
                    os.chmod(curr, st_prev.st_mode | stat.S_IEXEC)

def clean_testbench():
    """Clean the testbench"""
    shutil.rmtree(MY_FOLDER)
    shutil.rmtree(THEIR_FOLDER)
