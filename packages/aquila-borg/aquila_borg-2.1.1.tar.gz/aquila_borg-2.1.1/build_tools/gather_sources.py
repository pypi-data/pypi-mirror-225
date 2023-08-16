#+
#   ARES/HADES/BORG Package -- ./build_tools/gather_sources.py
#   Copyright (C) 2014-2020 Guilhem Lavaux <guilhem.lavaux@iap.fr>
#
#   Additional contributions from:
#      Guilhem Lavaux <guilhem.lavaux@iap.fr> (2023)
#   
#+
# ARES TAG: authors_num = 1
# ARES TAG: name(0) = Guilhem Lavaux
# ARES TAG: email(0) = guilhem.lavaux@iap.fr
# ARES TAG: year(0) = 2014-2020
import sys
import shutil
import tempfile
import re
import time
from git import Repo,Tree,Blob,Submodule

distribute_text=""

def build_slice(start, end):
  if end == start:
    return str(start)
  else:
    return str(start)+"-"+str(end)

def line_injection(tag, text, func):
  output = []
  for line in text.split('\n'):
    if line.find(tag) >= 0:
      line = func(line)
    output.append(line)
  return "\n".join(output)

def build_years(years):
  year_list = []
  start = prev_y = years[0]
  for y in years[1:]:
    if y != prev_y+1:
      year_list.append(build_slice(start, prev_y))
      start = y
    prev_y = y
  year_list.append(build_slice(start, prev_y))

  return ", ".join(year_list) #[str(y) for y in years])

class BadFileData(Exception):
  pass

def checked_author(data, i):
  defaults = {
     'name(0)': 'Guilhem Lavaux',
     'email(0)': 'guilhem.lavaux@iap.fr',
     'year(0)': '2014-2020',
     'name(1)': 'Jens Jasche',
     'email(1)': 'jens.jasche@fysik.su.se',
     'year(1)': '2009-2020'
  }
  codes = ['name(%d)' % i, 'email(%d)' % i, 'year(%d)' % i]
  if any(not s in data for s in codes):
    if i <= 1:
      print("   \033[1mWARNING: Using default author data. Please fix file.\033[0m")
    else:
      print("   \033[41mERROR: Need more author data. Please fix file.\033[0m")
      raise BadFileData()

  defaults.update(data)
  return tuple(map(lambda k: defaults[k], codes))

def main_author_handler(line, data, fname):
  num = int(data.get('authors_num', 2))
  output = []
  for i in range(num):
     name, email, year = checked_author(data, i)
     this_line = re.sub('@MAIN_NAME@', name, line)
     this_line = re.sub('@MAIN_EMAIL@', email, this_line)
     output.append( re.sub('@MAIN_YEAR@', year, this_line) )
  return "\n".join(output)

discard_set = set(['Temp'])

def apply_license(license, relimit, filename, authors):
  header = re.sub(r'@FILENAME@', filename, license)
  # Look for the AUTHORS tag in the license template, it has to be support both type of comment.
  m = re.search(
      r'^([@#/<>()\w\-*+ \t\n:.]+)\n([#/()\w\-* \t]*)@AUTHORS@([#/()\w\-* \t]*)\n([@#/()\w\-*+ \n:.;,<>]+)$',
      header, flags=re.MULTILINE)
  init_header,pre_author,post_author,final_header = m.group(1,2,3,4)
  header = init_header + '\n'
  author_list = list( authors.keys())
  author_list.sort()
  for author in author_list:
    if author in discard_set:
      continue
    a_data = authors[author]
    email = a_data['email']
    years = a_data['years']
    years = build_years(years)
    header += pre_author + ("%(name)s <%(email)s> (%(years)s)" % dict(name=author,email=email, years=years)) + post_author + '\n'
  header += final_header

  m = re.search(
      r'^([@#/<>(),\w\-*+ \t\n:.]+)\n([#/()\w\-* \t]*)@DISTRIBUTE@([#/()\w\-* \t]*)\n([@#/()\w\-*+ \n:.;,<>]+)$',
      header, flags=re.MULTILINE)
  if m is None:
     print("We reached an invalid state.")
     print(f"Header is:\n{header}")
     sys.exit(1)
  init_header,pre_distribute,post_distribute,final_header = m.group(1,2,3,4)
  header = f"{init_header}\n"
  for distribute_line in distribute_text.split('\n'):
    header += f"{pre_distribute}{distribute_line}{post_distribute}\n"
  header += final_header

  with open(filename, mode="rt", encoding="UTF-8") as f:
      lines = f.read()

  # Now look for the tag section
  specials = {}
  for a in re.finditer(r"(#|//) ARES TAG:[ \t]*(?P<tag>[\w()]+)[ \t]*=[ \t]*(?P<value>[\w\t \-_\.@]*)", lines):
    b = a.groupdict()
    specials[b['tag']] = b['value']

  header = line_injection('@MAIN_NAME@', header, lambda l: main_author_handler(l, specials, filename))

  lines = re.sub(relimit, lambda x: (("" if x.group(1) is None else x.group(1)) + header), lines)

  with tempfile.NamedTemporaryFile(delete=False,encoding="UTF-8",mode="wt") as tmp_sources:
    tmp_sources.write(lines)

  shutil.move(tmp_sources.name, filename)

def apply_python_license(filename, authors):
  license="""#+
#   ARES/HADES/BORG Package -- @FILENAME@
#   Copyright (C) @MAIN_YEAR@ @MAIN_NAME@ <@MAIN_EMAIL@>
#
#   Additional contributions from:
#      @AUTHORS@
#   @DISTRIBUTE@
#+
"""

  print("Shell/Python/Julia file: %s" % filename)
  relimit=r'^(#!.*\n)?#\+\n(#.*\n)*#\+\n'
  apply_license(license, relimit, filename, authors)


def apply_cpp_license(filename, authors):
  license="""/*+
    ARES/HADES/BORG Package -- @FILENAME@
    Copyright (C) @MAIN_YEAR@ @MAIN_NAME@ <@MAIN_EMAIL@>

    Additional contributions from:
       @AUTHORS@
    @DISTRIBUTE@
+*/
"""
  relimit = r'(?s)^()/\*\+.*\+\*/\n'
  print("C++ file: %s" % filename)
  apply_license(license, relimit, filename, authors)


def patch_author_list(authors):
  patcher={
     'Guilhem Lavaux':'guilhem.lavaux@iap.fr',
     'Jens Jasche':'j.jasche@tum.de'}
  for a in patcher.keys():
    if a in authors:
      data = authors[a]
      data['email'] = patcher[a]

  author_merge(authors, 'MinhMPA', 'Minh Nguyen')
  author_merge(authors, 'Minh MPA', 'Minh Nguyen')
  author_merge(authors, 'flo', 'Florian Führer')
  author_merge(authors, 'LAVAUX Guilhem', 'Guilhem Lavaux')

def author_merge(authors, a_from, a_to):
  if a_from in authors:
    data1 = authors[a_from]
    del authors[a_from]
    if a_to in authors:
      data2 = authors[a_to]
      s = set(data2['years'])
      for y in data1['years']:
        s.add(y)
      s = list(s)
      s.sort()
      data2['years'] = s
    else:
      authors[a_to] = data1

def check_authors(repo, fname):
  authors={}
  author_names={}
  for c,_ in repo.blame('HEAD',fname,w=True,M=True):
    if not c.author.name in authors:
      authors[c.author.name] = set()
    author_names[c.author.name] = c.author.email
    authors[c.author.name].add(time.gmtime(c.authored_date)[0])

  for k in authors.keys():
    authors[k] = list(authors[k])
    authors[k].sort()

  authors = {k:dict(email=author_names[k],years=authors[k]) for k in authors.keys()}
  patch_author_list(authors)
  return authors

def manage_file(repo, fname):
  authors = check_authors(repo, fname)
  if re.match(".*\.(sh|py|pyx|jl)$",fname) != None:
    apply_python_license(fname, authors)
  if re.match('.*\.(tcc|cpp|hpp|h)$', fname) != None:
    apply_cpp_license(fname, authors)

def analyze_tree(repo, prefix, t):
  for entry in t:
    if type(entry) == Submodule:
#      analyze_tree(prefix + "/" + entry.path, Repo(entry.path).tree())
#entry.module())
      print("Seeing a submodule at path " + entry.path)
      continue
    ename = entry.name
    if ename == 'external' or ename == 'cmake_modules':
      continue
    if type(entry) == Tree:
      analyze_tree(repo, prefix + "/" + ename, entry)
    elif type(entry) == Blob:
      fname=prefix+"/"+ename
      manage_file(repo, fname)


if __name__=="__main__":
  repo = Repo(".")
  assert repo.bare == False
  if len(sys.argv) > 1:
     for f in sys.argv[1:]:
        manage_file(repo, f)
  else:
     t = repo.tree()
     analyze_tree(repo, ".", t)
