## Designed with <3 by dejbug.

import os, os.path
import re
import sys

from argparse import ArgumentParser
from collections import namedtuple

ROOTS = (
	ur"C:\mingw-w64",
	ur"mingw-w64",
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

KEYS = ("arch", "version", "threads", "eh", "rt", "rev", )

Version = namedtuple("Version", "path info")

def find_versions(recurse=False, roots=ROOTS):
	for root in roots:
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

def filter_versions(versions, **kk):
	if not kk:
		return versions

	def filter_func(version):
		for k,v in kk.items():
			if k in version.info:
				if hasattr(v, "__iter__"):
					if version.info[k] in v: return True
				else:
					if v == version.info[k]: return True
			return False

	return filter(filter_func, versions)

def get_highest_version(**kk):
	versions = find_versions()
	versions = filter_versions(versions, **kk)
	versions = sorted(versions, key=lambda v: v.info["version"])
	versions = reversed(versions)
	try:
		return versions.next()
	except StopIteration:
		pass

def get_choices(versions, key):
	return tuple(set(v.info[key] for v in versions if key in v.info))

def get_choices_dict(versions):
	versions = tuple(versions)
	d = {}
	for key in KEYS:
		d[key] = get_choices(versions, key)
	return d

def parse_args(argv=sys.argv, choices={}):
	info = "Find the highest version of MinGW on the system."
	note = ""
	p = ArgumentParser(description=info, epilog=note)
	# p.add_argument("root", nargs="*", help="folders to search")
	g = p.add_argument_group("filters", "If any of these is passed, only versions matching the given values will be considered. The possible values for each option are listed in braces to the right. If no options are listed at all, no MinGW was found.")
	for key in KEYS:
		g.add_argument('--%s' % key, choices=choices[key], help="Search only MinGW versions matching value.")
	a = p.parse_args(argv[1:])
	return p, a

def dict_from_namespace(ns):
	d = {}
	for key in KEYS:
		value = getattr(ns, key)
		if value: d[key] = value
	return d

def main(argv=sys.argv):
	# version = get_highest_version(arch=("i686", "x86_64"), rt="v4")

	versions = find_versions()
	choices = get_choices_dict(versions)

	parser, args = parse_args(sys.argv, choices)
	version = get_highest_version(**dict_from_namespace(args))

	if version:
		print version.path
	else:
		print "."
		exit(1)


if "__main__" == __name__:
	main()
