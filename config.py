import shutil
import os

# Define source directory and destination directory
src_dir = os.path.abspath(r'src\user_functions')
dst_dir = os.path.abspath(r'src\extraction\user_functions')

# Remove the destination directory if it exists
if os.path.exists(dst_dir):
    shutil.rmtree(dst_dir)

# Copy entire directory
shutil.copytree(src_dir, dst_dir)