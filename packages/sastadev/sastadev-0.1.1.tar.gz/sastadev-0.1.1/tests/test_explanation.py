import pytest
from auchann.align_words import align_words

import sastadev.treebankfunctions as tbf
from sastadev import sasta_explanation


@pytest.mark.skip(reason='test code does not work')
def test():
    infullname = r"D:\Dropbox\jodijk\Utrecht\Projects\SASTADATA\Auris\outtreebanks\DLD07_corrected.xml"
    fulltreebank = tbf.getstree(infullname)
    treebank = fulltreebank.getroot()
    for tree in treebank:
        origutt = tbf.find1(tree, './/meta[@name="origutt"]/@value')
        cleanutt = tbf.find(tree, './/sentence/@value')
        explanationstr = sasta_explanation.finalmultiwordexplanation(tree)
        if explanationstr is not None:
            alignment = align_words(cleanutt, explanationstr)
        else:
            alignment = None
        if explanationstr is not None:
            print(
                f' Orig:{origutt}\nClean:{cleanutt}\n Expl:{explanationstr}\nAlign:{alignment}\n\n')


if __name__ == '__main__':
    test()
