# -*- coding: utf-8 -*-

from collective.tabularlabeloverrides import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from z3c.form import validator
from z3c.form.validator import SimpleFieldValidator
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import provider


class ITabularLabelOverridesMarker(Interface):
    pass


@provider(IFormFieldProvider)
class ITabularLabelOverrides(model.Schema):
    """ """

    label_overrides = schema.Tuple(
        title=_(
            "Label Overrides",
        ),
        description=_(
            "One override mapping per line. Use the format: 'toreplace|replacewith'",
        ),
        value_type=schema.TextLine(title="Label Override"),
        # default='',
        required=False,
        readonly=False,
    )


class LabelOverridesValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        if not value:
            return
        for lo in value:
            if not lo:
                continue
            lo_parts = lo.split("|")
            if len(lo_parts) != 2:
                raise Invalid(_(u'Label overrides in wrong format, use "toreplace|replacewith" format!'))


validator.WidgetValidatorDiscriminators(LabelOverridesValidator, field=ITabularLabelOverrides["label_overrides"])


@implementer(ITabularLabelOverrides)
@adapter(ITabularLabelOverridesMarker)
class TabularLabelOverrides(object):
    def __init__(self, context):
        self.context = context

    @property
    def label_overrides(self):
        if safe_hasattr(self.context, "label_overrides"):
            return self.context.label_overrides
        return tuple()

    @label_overrides.setter
    def label_overrides(self, value):
        self.context.label_overrides = value
