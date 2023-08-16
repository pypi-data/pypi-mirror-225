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

    # Those data are not always available for all 3DHistech scanners.
    # In this specific case, P1000 are being tested.
    assert data.get("datafile.ProfileType") is not None
    assert data.get("datafile.ProfileName") is not None
    assert data.get("initfile.GENERAL.slide_name") is not None

