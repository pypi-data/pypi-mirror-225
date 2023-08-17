import os
import sys
from pathlib import Path

root_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent.resolve()

if sys.platform == "win32":
    EXT = "dll"
elif sys.platform == "darwin":  # macOS
    EXT = "dylib"
else:  # Assume Linux or similar
    EXT = "so"


def test_extract_profile_info():
    """Test extract_profile_info() function."""
    # Remove the shared library if it exists
    os.system(f'rm -f {root_dir}/dist/libprofileinfo_extractor.{EXT}')
    # Compiles the C library first
    os.system(f"cd {root_dir} && make shared_lib")
    # Now import the function
    from src.mirax_profileinfo_extractor.extractor import get_mirax_profile_info

    # Provide your own Mirax file, by default one from the company,
    # not accessible to the public, is used
    mirax_file = os.getenv("MIRAX_FILE")
    if not mirax_file:
        raise Exception("Please provide a Mirax file path in the MIRAX_FILE environment variable")
    data = get_mirax_profile_info(mirax_file)

    assert data.get("datafile.ProfileName") is not None and len(data["datafile.ProfileName"]) > 0
    assert data.get("initfile.GENERAL.slide_name") is not None and len(data["initfile.GENERAL.slide_name"]) > 0

    mirax_file2 = os.getenv("MIRAX_FILE_2")
    if mirax_file2:
        # Call the function twice to make sure there are no double free errors
        data_2 = get_mirax_profile_info(mirax_file2, include_initfile_metadata=False)

        assert data_2.get("datafile.ProfileName") is not None and len(data_2["datafile.ProfileName"]) > 0
        assert data_2.get("initfile.GENERAL.slide_name") is None
    print("Test passed")


if __name__ == '__main__':
    test_extract_profile_info()
