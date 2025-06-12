import json
import subprocess

# Standard license texts
LICENSE_TEMPLATES = {
    "MIT License": """MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""",
    "BSD License": """BSD 3-Clause License

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.""",
    "Apache Software License": """Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

1. Definitions
...

You may obtain a copy of the License at:

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.""",
    "Mozilla Public License 2.0 (MPL 2.0)": """Mozilla Public License Version 2.0

You can obtain a copy at https://www.mozilla.org/MPL/2.0/

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this file,
You can obtain one at https://mozilla.org/MPL/2.0/.

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
for the specific language governing rights and limitations under the License.""",
    "Python Software Foundation License": """PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2

1. This LICENSE AGREEMENT is between the Python Software Foundation ("PSF"), and the Individual or
    Organization ("Licensee") accessing and otherwise using this software.

2. Subject to the terms and conditions of this License Agreement, PSF hereby grants Licensee a nonexclusive,
    royalty-free license.

...

A copy of this license is available at https://docs.python.org/3/license.html""",
    "The Unlicense (Unlicense)": """This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE.""",
}

# Step 1: Run pip-licenses
print("📦 Running pip-licenses...")
result = subprocess.run(
    ["pip-licenses", "--from=mixed", "--with-license-file", "--with-authors", "--with-url", "--format=json"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

if result.returncode != 0:
    print("❌ Error running pip-licenses:", result.stderr)
    exit(1)

# Step 2: Parse output
try:
    licenses = json.loads(result.stdout)
except json.JSONDecodeError as e:
    print("❌ Failed to parse JSON:", e)
    exit(1)

# Step 3: Write final output
output_file = "THIRD_PARTY_LICENSES.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("Third-Party Licenses\n")
    f.write("====================\n\n")
    for pkg in licenses:
        f.write(f"## {pkg['Name']} ({pkg['Version']})\n")
        f.write(f"Author(s): {pkg.get('Author') or 'Unknown'}\n")
        f.write(f"License: {pkg['License']}\n")
        f.write(f"Homepage: {pkg.get('URL') or 'N/A'}\n\n")

        license_text = pkg.get("LicenseFileText", "").strip()

        if not license_text:
            template = LICENSE_TEMPLATES.get(pkg["License"])
            if template:
                f.write(template + "\n")
            else:
                f.write("(No license text found; please check manually using the URL above)\n")
        else:
            f.write(license_text + "\n")

        f.write("\n" + "-" * 80 + "\n\n")

print(f"✅ License report written to: {output_file}")
