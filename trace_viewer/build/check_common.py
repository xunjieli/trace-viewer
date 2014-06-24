# Copyright (c) 2013 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import os

from trace_viewer import trace_viewer_project


FILE_GROUPS = ["tracing_html_files",
    "tracing_css_files",
    "tracing_js_files",
    "tracing_img_files"]


def CheckCommon(file_name, listed_files):
  project = trace_viewer_project.TraceViewerProject()
  known_files = []
  build_dir = os.path.join(project.src_path, 'build')
  def handle(dirpath, dirnames, filenames):
    for name in filenames:
      if not (name.endswith(("_test.js",
                             "_test_data.js",
                             "tests.html",
                             ".py",
                             ".pyc")) or
         name.startswith((".")) or
         dirpath == build_dir):
        x = os.path.relpath(os.path.normpath(os.path.join(dirpath, name)),
                            project.trace_viewer_path)
        known_files.append(x)
    if '.svn' in dirnames:
      dirnames.remove('.svn')

  for (dirpath, dirnames, filenames) in os.walk(project.src_path):
    handle(dirpath, dirnames, filenames)

  for (dirpath, dirnames, filenames) in os.walk(
      os.path.join(project.tvcm_path, 'src')):
    handle(dirpath, dirnames, filenames)

  u = set(listed_files).union(set(known_files))
  i = set(listed_files).intersection(set(known_files))
  diff = list(u - i)

  if len(diff) == 0:
    return ''

  error = 'Entries in ' + file_name + ' do not match files on disk:\n'
  in_file_only = list(set(listed_files) - set(known_files))
  in_known_only = list(set(known_files) - set(listed_files))

  if len(in_file_only) > 0:
    error += '  In file only:\n    ' + '\n    '.join(sorted(in_file_only))
  if len(in_known_only) > 0:
    if len(in_file_only) > 0:
      error += '\n\n'
    error += '  On disk only:\n    ' + '\n    '.join(sorted(in_known_only))

  return error