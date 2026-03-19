
try:
    import sys
    print("sys.path:", sys.path)
    import app_utils
    print("utils file:", utils.__file__)
    from app_utils import analysis_utils
    print("analysis_utils file:", analysis_utils.__file__)
    print("dir(analysis_utils):", dir(analysis_utils))
    from app_utils.analysis_utils import extract_top_keywords
    print("Import successful!")
except Exception as e:
    print("Import failed:", e)
    import traceback
    traceback.print_exc()
