# Mind Map to Markdown for Roam import

Got a Mind Map  with contents you'd like to import into Roam?

Soon, this Python application *might* do what just you want.

It will take a Freeplane `.mm` Mind Map file and convert it into Markdown ready for manual import into Roam.

I think Freemind mind maps should also work, but I have not yet tested them.

It's currently pre-Alpha (I started the project on 16 October 2021)
1. It needs Python >= 3.8
2. It uses Pyhthon's lxml package, so you may also need to install the appropriate library
3. Don't rely on it for a critical project!
4. If you do try it, manually check the generated Markdown before you try to import!

It's not user-friendly at the moment.

## Installing

If you are comfortable with GitHub and Python,
```bash
https://github.com/romilly/fp2md4roam.git
cd fp2md4roam
pip3 install html2text
pip3 install lxml
pip3 install logzero
python3
```

```python
from fp2md4roam.convert import convert
from fp2md4roam.filing import FSFiler, RoamFileMaker

fs_filer = RoamFileMaker(FSFiler('<directory-for-output-file>'))
convert('<path-to-mindmap-file>', fs_filer)
```

This will create a file called BrainRules.md in the output directory.

### TO DO

1. Allow specification of the output file name, or generate it from the input file name
2. Lots more testing!
3. Easier invocation
4. Documentation
5. Once enough people have tested it, it will be packaged and released
