from astroCAST.analysis import Video

from pathlib import Path
import time

folder = Path("/media/janrei1/data/22A7x11")

ast = folder.joinpath("22A7x11-1.dff.ast.tiff")
neu = folder.joinpath("22A7x11-1.dff.neu.tiff")

assert ast.is_file()
assert neu.is_file()

ast = Video(ast)
a = ast.show()

print("hello")
time.sleep(60)
