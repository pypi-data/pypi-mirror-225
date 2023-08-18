# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_hasattr
from plone.app.contenttypes.browser.folder import FolderView
# from plone.app.contenttypes.browser.collection import CollectionView
from collective.taxonomy.browser import TaxonomyCollectionView
from plone.app.vocabularies.metadatafields import get_field_label
from zope.interface import implementer
from zope.interface import Interface


# class IFolderView(ICollection):
#     """Marker Interface for IFolderView"""


# @implementer(IFolderView)
class CollectionView(TaxonomyCollectionView):
    """
    """

    def tabular_field_label(self, field):
        """ Look up label overrides, if no match then
            return the internationalized label (Message object) corresponding
            to the field (Plone default labels).
        """
        if safe_hasattr(self.context, "label_overrides"):
            if self.context.label_overrides:
                for loverride in self.context.label_overrides:
                    if not loverride:
                        continue
                    source_label, target_label = loverride.split("|")
                    if source_label != field:
                        continue
                    return target_label

        return super().tabular_field_label(field)
