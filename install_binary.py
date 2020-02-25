import re
import io
import os
import requests
import zipfile
import stat
from pspy_placeholder import out_path
from distutils.util import get_platform

tag = re.compile('refs/tags/v(\S+)')


def make_executable(cmd_path):
    if os.lstat(cmd_path).st_mode & stat.S_IEXEC:
        pass
    else:
        os.chmod(cmd_path, stat.S_IEXEC)


def show_tags(url=r"https://github.com/purescript-python/purescript-python"):
    """
    Use ls-remote in gitPython
    https://stackoverflow.com/questions/35585236/git-ls-remote-in-gitpython
    """
    import git
    g = git.cmd.Git()
    for ref in g.ls_remote(url).split('\n'):
        found = tag.findall(ref.split('\t')[-1].strip())
        if not found:
            continue
        yield found[0]


def mk_tmplt(template):
    if isinstance(template, dict):

        def check(data,
                  *,
                  tmplt=tuple((k, mk_tmplt(v)) for k, v in template.items())):
            if not isinstance(data, dict):
                return False
            for k, v in tmplt:
                if k not in data:
                    return False
                if not v(data[k]):
                    return False
            return True

    elif isinstance(template, list):

        def check(data, *, tmplt=tuple(map(mk_tmplt, template))):
            if not isinstance(data, list):
                return False
            if len(data) != len(tmplt):
                return False
            for t, v in zip(tmplt, data):
                if not t(v):
                    return False
            return True

    elif isinstance(template, type):

        def check(data, *, t=template):
            return isinstance(data, t)

    elif template is any:
        check = lambda _: True
    elif hasattr(template, 'match'):
        check = template.match
    else:

        def check(data, *, o=template):
            return data == o

    return check


def traverse(f, data):
    if isinstance(data, dict):
        for each in data.values():
            yield from traverse(f, each)
    elif isinstance(data, list):
        for each in data:
            yield from traverse(f, each)
    if f(data):
        yield data


def gq(tmp, data):
    return traverse(mk_tmplt(tmp), data)

class ZipFileWithPermissions(zipfile.ZipFile):
    def _extract_member(self, member, targetpath, pwd):
        if not isinstance(member, zipfile.ZipInfo):
            member = self.getinfo(member)
        targetpath = super()._extract_member(member, targetpath, pwd)

        attr = member.external_attr >> 16
        if attr != 0:
            os.chmod(targetpath, attr)
        return targetpath

def get_binary():
    from purescripto.version import __blueprint_version__
    max_fit_tag = max(filter(__blueprint_version__.startswith, show_tags()))

    print('Downloading binaries from purescript-python/purescript-python...')
    data = requests.get(
        r"https://api.github.com/repos/purescript-python/purescript-python/releases/tags/v{}"
        .format(max_fit_tag)).json()
    print('Binaries downloaded.')
    plat_name = get_platform()
    matcher = re.compile('\S+' + re.escape(plat_name))
    tmplt = {'browser_download_url': matcher}
    try:
        each = next(gq(tmplt, data))
    except StopIteration:
        import sys
        print(
            f"It seems that binaries for your platform (which name is ${plat_name}) is not available.\n"
            "Following way must work, but can be quite time-consuming:\n"
            "Firstly, Install Haskell Stack Build Tool: https://docs.haskellstack.org/en/stable/README/\n"
            "Second, Clone https://github.com/purescript-python/purescript-python, then do `stack install .`"
        )
        sys.exit(1)

    url = each['browser_download_url']
    zf = ZipFileWithPermissions(io.BytesIO(requests.get(url).content))
    exe = "pspy-blueprint"
    if 'win' in url:
        exe += '.exe'

    out_path.mkdir(exist_ok=True, parents=True, mode=0o777)
    zf.extract(exe, path=str(out_path))
    make_executable(str(out_path / exe))

if __name__ == "__main__":
    get_binary()
