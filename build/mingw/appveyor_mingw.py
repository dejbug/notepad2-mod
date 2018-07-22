from collections import namedtuple
import os, os.path
import re

ROOTS = (
	ur"C:\mingw-w64",
	# ur"mingw-w64",
)

"""https://sourceforge.net/projects/mingw-w64/files/mingw-w64/mingw-w64-release/
"""

SAMPLE_DIR_STDOUT = """
i686-5.3.0-posix-dwarf-rt_v4-rev0
i686-6.3.0-posix-dwarf-rt_v5-rev1
x86_64-6.3.0-posix-seh-rt_v5-rev1
x86_64-7.2.0-posix-seh-rt_v5-rev1
x86_64-7.3.0-posix-seh-rt_v5-rev0
"""

Version = namedtuple("Version", "path info")

def find_versions(recurse=False):
	for root in ROOTS:
		for t,dd,nn in os.walk(root):
			for d in dd:
				x = parse_mingw_distro_name(d)
				if x:
					yield Version(os.path.abspath(os.path.join(t, d)), x)
			if not recurse:
				break

def parse_mingw_distro_name(text):
	r = re.match(r"""(?x)
		(?P<arch>x86_64|i686|[^-]+)
		-(?P<version>\d+\.\d+\.\d+)
		(?:-(?P<threads>posix|win32))?
		(?:-(?P<eh>sjlj|seh|dwarf))?
		(?:-rt_(?P<rt>v\d+))?
		(?:-rev(?P<rev>\d+))?
		""", text)
	if r: return r.groupdict()
	return {}

def test_parse_mingw_distro_name():
	for line in iter_lines(SAMPLE_DIR_STDOUT):
		yield parse_mingw_distro_name(line)

def iter_lines(text):
	for r in re.finditer(r'(?m)^\s*(\S+)\s*$', SAMPLE_DIR_STDOUT):
		yield r.group(1)

def get_highest_version():
	try:
		versions = find_versions()
		versions = sorted(versions, key=lambda v: v.info["version"])
		versions = reversed(versions)
		return versions.next()
	except StopIteration:
		pass


if "__main__" == __name__:
	version = get_highest_version()
	if version:
		print version.path
	else:
		print "."
		exit(1)
