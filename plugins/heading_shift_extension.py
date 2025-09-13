from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

class HeadingShiftProcessor(Treeprocessor):
    def run(self, root):
        for el in root.iter():
            if el.tag in [f'h{i}' for i in range(1, 7)]:
                level = int(el.tag[1])
                new_level = level + 4
                if 1 <= new_level <= 6:
                    el.tag = f'h{new_level}'
                else:
                    el.tag = 'p'  # fallback for levels > h6

class HeadingShiftExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(HeadingShiftProcessor(md), 'heading_shift', 15)

def makeExtension(**kwargs):
    return HeadingShiftExtension(**kwargs)
