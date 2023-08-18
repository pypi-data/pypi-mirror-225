# coding: utf-8

# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from memas_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from memas_client.model.citation import Citation
from memas_client.model.cited_document import CitedDocument
from memas_client.model.corpus_pathname import CorpusPathname
