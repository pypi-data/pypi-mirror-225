# ./pyxb_build/ukrdc_schema/pv_2_0_schema.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:e92452c8d3e28a9e27abfc9994d2007779e7f4c9
# Generated 2023-08-15 13:07:03.777981 by PyXB version 1.2.6 using Python 3.9.17.final.0
# Namespace AbsentNamespace0

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:a0dd0daa-3b6c-11ee-a499-e1619d0001fc')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.CreateAbsentNamespace()
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Atomic simple type: [anonymous]
class STD_ANON (pyxb.binding.datatypes.integer):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 10, 20)
    _Documentation = None
STD_ANON._CF_minInclusive = pyxb.binding.facets.CF_minInclusive(value_datatype=STD_ANON, value=pyxb.binding.datatypes.integer(0))
STD_ANON._CF_maxInclusive = pyxb.binding.facets.CF_maxInclusive(value_datatype=STD_ANON, value=pyxb.binding.datatypes.integer(999999))
STD_ANON._CF_totalDigits = pyxb.binding.facets.CF_totalDigits(value=pyxb.binding.datatypes.positiveInteger(6))
STD_ANON._InitializeFacetMap(STD_ANON._CF_minInclusive,
   STD_ANON._CF_maxInclusive,
   STD_ANON._CF_totalDigits)
_module_typeBindings.STD_ANON = STD_ANON

# Atomic simple type: [anonymous]
class STD_ANON_ (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 25, 32)
    _Documentation = None
STD_ANON_._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(60))
STD_ANON_._InitializeFacetMap(STD_ANON_._CF_maxLength)
_module_typeBindings.STD_ANON_ = STD_ANON_

# Atomic simple type: [anonymous]
class STD_ANON_2 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 32, 32)
    _Documentation = None
STD_ANON_2._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_2._InitializeFacetMap(STD_ANON_2._CF_maxLength)
_module_typeBindings.STD_ANON_2 = STD_ANON_2

# Atomic simple type: [anonymous]
class STD_ANON_3 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 39, 32)
    _Documentation = None
STD_ANON_3._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_3._InitializeFacetMap(STD_ANON_3._CF_maxLength)
_module_typeBindings.STD_ANON_3 = STD_ANON_3

# Atomic simple type: [anonymous]
class STD_ANON_4 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 46, 32)
    _Documentation = None
STD_ANON_4._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_4._InitializeFacetMap(STD_ANON_4._CF_maxLength)
_module_typeBindings.STD_ANON_4 = STD_ANON_4

# Atomic simple type: [anonymous]
class STD_ANON_5 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 53, 32)
    _Documentation = None
STD_ANON_5._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_5._InitializeFacetMap(STD_ANON_5._CF_maxLength)
_module_typeBindings.STD_ANON_5 = STD_ANON_5

# Atomic simple type: [anonymous]
class STD_ANON_6 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 60, 32)
    _Documentation = None
STD_ANON_6._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
STD_ANON_6._InitializeFacetMap(STD_ANON_6._CF_maxLength)
_module_typeBindings.STD_ANON_6 = STD_ANON_6

# Atomic simple type: [anonymous]
class STD_ANON_7 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 67, 32)
    _Documentation = None
STD_ANON_7._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_7._InitializeFacetMap(STD_ANON_7._CF_maxLength)
_module_typeBindings.STD_ANON_7 = STD_ANON_7

# Atomic simple type: [anonymous]
class STD_ANON_8 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 74, 32)
    _Documentation = None
STD_ANON_8._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_8._InitializeFacetMap(STD_ANON_8._CF_maxLength)
_module_typeBindings.STD_ANON_8 = STD_ANON_8

# Atomic simple type: [anonymous]
class STD_ANON_9 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 87, 32)
    _Documentation = None
STD_ANON_9._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(50))
STD_ANON_9._InitializeFacetMap(STD_ANON_9._CF_maxLength)
_module_typeBindings.STD_ANON_9 = STD_ANON_9

# Atomic simple type: [anonymous]
class STD_ANON_10 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 94, 32)
    _Documentation = None
STD_ANON_10._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_10._InitializeFacetMap(STD_ANON_10._CF_maxLength)
_module_typeBindings.STD_ANON_10 = STD_ANON_10

# Atomic simple type: [anonymous]
class STD_ANON_11 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 101, 32)
    _Documentation = None
STD_ANON_11._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_11._InitializeFacetMap(STD_ANON_11._CF_maxLength)
_module_typeBindings.STD_ANON_11 = STD_ANON_11

# Atomic simple type: [anonymous]
class STD_ANON_12 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 108, 32)
    _Documentation = None
STD_ANON_12._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_12._InitializeFacetMap(STD_ANON_12._CF_maxLength)
_module_typeBindings.STD_ANON_12 = STD_ANON_12

# Atomic simple type: [anonymous]
class STD_ANON_13 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 115, 32)
    _Documentation = None
STD_ANON_13._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_13._InitializeFacetMap(STD_ANON_13._CF_maxLength)
_module_typeBindings.STD_ANON_13 = STD_ANON_13

# Atomic simple type: [anonymous]
class STD_ANON_14 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 122, 32)
    _Documentation = None
STD_ANON_14._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
STD_ANON_14._InitializeFacetMap(STD_ANON_14._CF_maxLength)
_module_typeBindings.STD_ANON_14 = STD_ANON_14

# Atomic simple type: [anonymous]
class STD_ANON_15 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 129, 32)
    _Documentation = None
STD_ANON_15._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_15._InitializeFacetMap(STD_ANON_15._CF_maxLength)
_module_typeBindings.STD_ANON_15 = STD_ANON_15

# Atomic simple type: [anonymous]
class STD_ANON_16 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 136, 32)
    _Documentation = None
STD_ANON_16._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_16._InitializeFacetMap(STD_ANON_16._CF_maxLength)
_module_typeBindings.STD_ANON_16 = STD_ANON_16

# Atomic simple type: [anonymous]
class STD_ANON_17 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 152, 44)
    _Documentation = None
STD_ANON_17._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(30))
STD_ANON_17._InitializeFacetMap(STD_ANON_17._CF_maxLength)
_module_typeBindings.STD_ANON_17 = STD_ANON_17

# Atomic simple type: [anonymous]
class STD_ANON_18 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 159, 44)
    _Documentation = None
STD_ANON_18._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(30))
STD_ANON_18._InitializeFacetMap(STD_ANON_18._CF_maxLength)
_module_typeBindings.STD_ANON_18 = STD_ANON_18

# Atomic simple type: [anonymous]
class STD_ANON_19 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 168, 44)
    _Documentation = None
STD_ANON_19._CF_length = pyxb.binding.facets.CF_length(value=pyxb.binding.datatypes.nonNegativeInteger(10))
STD_ANON_19._CF_whiteSpace = pyxb.binding.facets.CF_whiteSpace(value=pyxb.binding.facets._WhiteSpace_enum.collapse)
STD_ANON_19._InitializeFacetMap(STD_ANON_19._CF_length,
   STD_ANON_19._CF_whiteSpace)
_module_typeBindings.STD_ANON_19 = STD_ANON_19

# Atomic simple type: [anonymous]
class STD_ANON_20 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 177, 44)
    _Documentation = None
STD_ANON_20._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(30))
STD_ANON_20._InitializeFacetMap(STD_ANON_20._CF_maxLength)
_module_typeBindings.STD_ANON_20 = STD_ANON_20

# Atomic simple type: [anonymous]
class STD_ANON_21 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 184, 44)
    _Documentation = None
STD_ANON_21._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(60))
STD_ANON_21._InitializeFacetMap(STD_ANON_21._CF_maxLength)
_module_typeBindings.STD_ANON_21 = STD_ANON_21

# Atomic simple type: [anonymous]
class STD_ANON_22 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 191, 44)
    _Documentation = None
STD_ANON_22._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(60))
STD_ANON_22._InitializeFacetMap(STD_ANON_22._CF_maxLength)
_module_typeBindings.STD_ANON_22 = STD_ANON_22

# Atomic simple type: [anonymous]
class STD_ANON_23 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 198, 44)
    _Documentation = None
STD_ANON_23._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(60))
STD_ANON_23._InitializeFacetMap(STD_ANON_23._CF_maxLength)
_module_typeBindings.STD_ANON_23 = STD_ANON_23

# Atomic simple type: [anonymous]
class STD_ANON_24 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 205, 44)
    _Documentation = None
STD_ANON_24._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(60))
STD_ANON_24._InitializeFacetMap(STD_ANON_24._CF_maxLength)
_module_typeBindings.STD_ANON_24 = STD_ANON_24

# Atomic simple type: [anonymous]
class STD_ANON_25 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 212, 44)
    _Documentation = None
STD_ANON_25._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(10))
STD_ANON_25._InitializeFacetMap(STD_ANON_25._CF_maxLength)
_module_typeBindings.STD_ANON_25 = STD_ANON_25

# Atomic simple type: [anonymous]
class STD_ANON_26 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 219, 44)
    _Documentation = None
STD_ANON_26._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_26._InitializeFacetMap(STD_ANON_26._CF_maxLength)
_module_typeBindings.STD_ANON_26 = STD_ANON_26

# Atomic simple type: [anonymous]
class STD_ANON_27 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 226, 44)
    _Documentation = None
STD_ANON_27._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_27._InitializeFacetMap(STD_ANON_27._CF_maxLength)
_module_typeBindings.STD_ANON_27 = STD_ANON_27

# Atomic simple type: [anonymous]
class STD_ANON_28 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 233, 44)
    _Documentation = None
STD_ANON_28._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(100))
STD_ANON_28._InitializeFacetMap(STD_ANON_28._CF_maxLength)
_module_typeBindings.STD_ANON_28 = STD_ANON_28

# Atomic simple type: [anonymous]
class STD_ANON_29 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 247, 44)
    _Documentation = None
STD_ANON_29._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(70))
STD_ANON_29._InitializeFacetMap(STD_ANON_29._CF_maxLength)
_module_typeBindings.STD_ANON_29 = STD_ANON_29

# Atomic simple type: [anonymous]
class STD_ANON_30 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 254, 44)
    _Documentation = None
STD_ANON_30._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(5))
STD_ANON_30._InitializeFacetMap(STD_ANON_30._CF_maxLength)
_module_typeBindings.STD_ANON_30 = STD_ANON_30

# Atomic simple type: [anonymous]
class STD_ANON_31 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 270, 44)
    _Documentation = None
STD_ANON_31._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(30))
STD_ANON_31._InitializeFacetMap(STD_ANON_31._CF_maxLength)
_module_typeBindings.STD_ANON_31 = STD_ANON_31

# Atomic simple type: [anonymous]
class STD_ANON_32 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 367, 16)
    _Documentation = None
STD_ANON_32._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(50))
STD_ANON_32._InitializeFacetMap(STD_ANON_32._CF_maxLength)
_module_typeBindings.STD_ANON_32 = STD_ANON_32

# Atomic simple type: [anonymous]
class STD_ANON_33 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 399, 16)
    _Documentation = None
STD_ANON_33._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(110))
STD_ANON_33._InitializeFacetMap(STD_ANON_33._CF_maxLength)
_module_typeBindings.STD_ANON_33 = STD_ANON_33

# Atomic simple type: [anonymous]
class STD_ANON_34 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 406, 16)
    _Documentation = None
STD_ANON_34._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(1000))
STD_ANON_34._InitializeFacetMap(STD_ANON_34._CF_maxLength)
_module_typeBindings.STD_ANON_34 = STD_ANON_34

# Atomic simple type: [anonymous]
class STD_ANON_35 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 432, 16)
    _Documentation = None
STD_ANON_35._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(40))
STD_ANON_35._InitializeFacetMap(STD_ANON_35._CF_maxLength)
_module_typeBindings.STD_ANON_35 = STD_ANON_35

# Atomic simple type: [anonymous]
class STD_ANON_36 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 440, 16)
    _Documentation = None
STD_ANON_36._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
STD_ANON_36._InitializeFacetMap(STD_ANON_36._CF_maxLength)
_module_typeBindings.STD_ANON_36 = STD_ANON_36

# Atomic simple type: [anonymous]
class STD_ANON_37 (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 461, 16)
    _Documentation = None
STD_ANON_37._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(20))
STD_ANON_37._InitializeFacetMap(STD_ANON_37._CF_maxLength)
_module_typeBindings.STD_ANON_37 = STD_ANON_37

# Atomic simple type: pv_diagnosis_name
class pv_diagnosis_name (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'pv_diagnosis_name')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 478, 4)
    _Documentation = None
pv_diagnosis_name._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(150))
pv_diagnosis_name._InitializeFacetMap(pv_diagnosis_name._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'pv_diagnosis_name', pv_diagnosis_name)
_module_typeBindings.pv_diagnosis_name = pv_diagnosis_name

# Atomic simple type: ibd_disease_extent
class ibd_disease_extent (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """IBD Disease Extent"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ibd_disease_extent')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 486, 4)
    _Documentation = 'IBD Disease Extent'
ibd_disease_extent._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=ibd_disease_extent, enum_prefix=None)
ibd_disease_extent.Proctitis = ibd_disease_extent._CF_enumeration.addEnumeration(unicode_value='Proctitis', tag='Proctitis')
ibd_disease_extent.Left_Sided_Colitis = ibd_disease_extent._CF_enumeration.addEnumeration(unicode_value='Left Sided Colitis', tag='Left_Sided_Colitis')
ibd_disease_extent.Extensive_Colitis = ibd_disease_extent._CF_enumeration.addEnumeration(unicode_value='Extensive Colitis', tag='Extensive_Colitis')
ibd_disease_extent.Ileal_Crohns = ibd_disease_extent._CF_enumeration.addEnumeration(unicode_value='Ileal Crohns', tag='Ileal_Crohns')
ibd_disease_extent.Ileo_Colonic_Disease = ibd_disease_extent._CF_enumeration.addEnumeration(unicode_value='Ileo-Colonic Disease', tag='Ileo_Colonic_Disease')
ibd_disease_extent.Crohns_Colitis = ibd_disease_extent._CF_enumeration.addEnumeration(unicode_value='Crohns Colitis', tag='Crohns_Colitis')
ibd_disease_extent.Isolated_Upper_GI_Disease = ibd_disease_extent._CF_enumeration.addEnumeration(unicode_value='Isolated Upper GI Disease', tag='Isolated_Upper_GI_Disease')
ibd_disease_extent._InitializeFacetMap(ibd_disease_extent._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'ibd_disease_extent', ibd_disease_extent)
_module_typeBindings.ibd_disease_extent = ibd_disease_extent

# Atomic simple type: ibd_disease_complication
class ibd_disease_complication (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ibd_disease_complication')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 510, 4)
    _Documentation = None
ibd_disease_complication._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(60))
ibd_disease_complication._InitializeFacetMap(ibd_disease_complication._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'ibd_disease_complication', ibd_disease_complication)
_module_typeBindings.ibd_disease_complication = ibd_disease_complication

# Atomic simple type: body_part
class body_part (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'body_part')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 525, 4)
    _Documentation = None
body_part._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(60))
body_part._InitializeFacetMap(body_part._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'body_part', body_part)
_module_typeBindings.body_part = body_part

# Atomic simple type: family_history_description
class family_history_description (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'family_history_description')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 539, 4)
    _Documentation = None
family_history_description._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(60))
family_history_description._InitializeFacetMap(family_history_description._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'family_history_description', family_history_description)
_module_typeBindings.family_history_description = family_history_description

# Atomic simple type: smoking_history_description
class smoking_history_description (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'smoking_history_description')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 554, 4)
    _Documentation = None
smoking_history_description._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(60))
smoking_history_description._InitializeFacetMap(smoking_history_description._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'smoking_history_description', smoking_history_description)
_module_typeBindings.smoking_history_description = smoking_history_description

# Atomic simple type: surgical_history_description
class surgical_history_description (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'surgical_history_description')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 569, 4)
    _Documentation = None
surgical_history_description._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(60))
surgical_history_description._InitializeFacetMap(surgical_history_description._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'surgical_history_description', surgical_history_description)
_module_typeBindings.surgical_history_description = surgical_history_description

# Atomic simple type: vaccination_record_description
class vaccination_record_description (pyxb.binding.datatypes.string):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'vaccination_record_description')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 585, 4)
    _Documentation = None
vaccination_record_description._CF_maxLength = pyxb.binding.facets.CF_maxLength(value=pyxb.binding.datatypes.nonNegativeInteger(60))
vaccination_record_description._InitializeFacetMap(vaccination_record_description._CF_maxLength)
Namespace.addCategoryObject('typeBinding', 'vaccination_record_description', vaccination_record_description)
_module_typeBindings.vaccination_record_description = vaccination_record_description

# Atomic simple type: pv_status
class pv_status (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """Patient View Status"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'pv_status')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 591, 4)
    _Documentation = 'Patient View Status'
pv_status._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=pv_status, enum_prefix=None)
pv_status.Include = pv_status._CF_enumeration.addEnumeration(unicode_value='Include', tag='Include')
pv_status.Remove = pv_status._CF_enumeration.addEnumeration(unicode_value='Remove', tag='Remove')
pv_status.Lost = pv_status._CF_enumeration.addEnumeration(unicode_value='Lost', tag='Lost')
pv_status.Died = pv_status._CF_enumeration.addEnumeration(unicode_value='Died', tag='Died')
pv_status.Suspend = pv_status._CF_enumeration.addEnumeration(unicode_value='Suspend', tag='Suspend')
pv_status.Followup = pv_status._CF_enumeration.addEnumeration(unicode_value='Followup', tag='Followup')
pv_status._InitializeFacetMap(pv_status._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'pv_status', pv_status)
_module_typeBindings.pv_status = pv_status

# Atomic simple type: sex
class sex (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """Sex"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'sex')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 604, 4)
    _Documentation = 'Sex'
sex._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=sex, enum_prefix=None)
sex.M = sex._CF_enumeration.addEnumeration(unicode_value='M', tag='M')
sex.F = sex._CF_enumeration.addEnumeration(unicode_value='F', tag='F')
sex.U = sex._CF_enumeration.addEnumeration(unicode_value='U', tag='U')
sex._InitializeFacetMap(sex._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'sex', sex)
_module_typeBindings.sex = sex

# Atomic simple type: prepost
class prepost (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """Pre or Post Dialysis Result"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'prepost')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 615, 4)
    _Documentation = 'Pre or Post Dialysis Result'
prepost._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=prepost, enum_prefix=None)
prepost.PRE = prepost._CF_enumeration.addEnumeration(unicode_value='PRE', tag='PRE')
prepost.POST = prepost._CF_enumeration.addEnumeration(unicode_value='POST', tag='POST')
prepost._InitializeFacetMap(prepost._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'prepost', prepost)
_module_typeBindings.prepost = prepost

# Atomic simple type: rrtstatus
class rrtstatus (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """RRT Treatment Modality"""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'rrtstatus')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 624, 4)
    _Documentation = 'RRT Treatment Modality'
rrtstatus._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=rrtstatus, enum_prefix=None)
rrtstatus.HD = rrtstatus._CF_enumeration.addEnumeration(unicode_value='HD', tag='HD')
rrtstatus.PD = rrtstatus._CF_enumeration.addEnumeration(unicode_value='PD', tag='PD')
rrtstatus.TP = rrtstatus._CF_enumeration.addEnumeration(unicode_value='TP', tag='TP')
rrtstatus.GEN = rrtstatus._CF_enumeration.addEnumeration(unicode_value='GEN', tag='GEN')
rrtstatus.XFER = rrtstatus._CF_enumeration.addEnumeration(unicode_value='XFER', tag='XFER')
rrtstatus._InitializeFacetMap(rrtstatus._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'rrtstatus', rrtstatus)
_module_typeBindings.rrtstatus = rrtstatus

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """PatientView XML Schema"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 7, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element sequence uses Python identifier sequence
    __sequence = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'sequence'), 'sequence', '__AbsentNamespace0_CTD_ANON_sequence', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 9, 16), )

    
    sequence = property(__sequence.value, __sequence.set, None, None)

    
    # Element dateofreport uses Python identifier dateofreport
    __dateofreport = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'dateofreport'), 'dateofreport', '__AbsentNamespace0_CTD_ANON_dateofreport', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 18, 16), )

    
    dateofreport = property(__dateofreport.value, __dateofreport.set, None, None)

    
    # Element flag uses Python identifier flag
    __flag = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'flag'), 'flag', '__AbsentNamespace0_CTD_ANON_flag', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 19, 16), )

    
    flag = property(__flag.value, __flag.set, None, None)

    
    # Element centredetails uses Python identifier centredetails
    __centredetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'centredetails'), 'centredetails', '__AbsentNamespace0_CTD_ANON_centredetails', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 20, 16), )

    
    centredetails = property(__centredetails.value, __centredetails.set, None, None)

    
    # Element gpdetails uses Python identifier gpdetails
    __gpdetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'gpdetails'), 'gpdetails', '__AbsentNamespace0_CTD_ANON_gpdetails', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 83, 16), )

    
    gpdetails = property(__gpdetails.value, __gpdetails.set, None, None)

    
    # Element patient uses Python identifier patient
    __patient = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'patient'), 'patient', '__AbsentNamespace0_CTD_ANON_patient', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 145, 16), )

    
    patient = property(__patient.value, __patient.set, None, None)

    _ElementMap.update({
        __sequence.name() : __sequence,
        __dateofreport.name() : __dateofreport,
        __flag.name() : __flag,
        __centredetails.name() : __centredetails,
        __gpdetails.name() : __gpdetails,
        __patient.name() : __patient
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 21, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element centrecode uses Python identifier centrecode
    __centrecode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'centrecode'), 'centrecode', '__AbsentNamespace0_CTD_ANON__centrecode', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 23, 28), )

    
    centrecode = property(__centrecode.value, __centrecode.set, None, None)

    
    # Element centrename uses Python identifier centrename
    __centrename = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'centrename'), 'centrename', '__AbsentNamespace0_CTD_ANON__centrename', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 24, 28), )

    
    centrename = property(__centrename.value, __centrename.set, None, None)

    
    # Element centreaddress1 uses Python identifier centreaddress1
    __centreaddress1 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'centreaddress1'), 'centreaddress1', '__AbsentNamespace0_CTD_ANON__centreaddress1', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 31, 28), )

    
    centreaddress1 = property(__centreaddress1.value, __centreaddress1.set, None, None)

    
    # Element centreaddress2 uses Python identifier centreaddress2
    __centreaddress2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'centreaddress2'), 'centreaddress2', '__AbsentNamespace0_CTD_ANON__centreaddress2', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 38, 28), )

    
    centreaddress2 = property(__centreaddress2.value, __centreaddress2.set, None, None)

    
    # Element centreaddress3 uses Python identifier centreaddress3
    __centreaddress3 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'centreaddress3'), 'centreaddress3', '__AbsentNamespace0_CTD_ANON__centreaddress3', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 45, 28), )

    
    centreaddress3 = property(__centreaddress3.value, __centreaddress3.set, None, None)

    
    # Element centreaddress4 uses Python identifier centreaddress4
    __centreaddress4 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'centreaddress4'), 'centreaddress4', '__AbsentNamespace0_CTD_ANON__centreaddress4', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 52, 28), )

    
    centreaddress4 = property(__centreaddress4.value, __centreaddress4.set, None, None)

    
    # Element centrepostcode uses Python identifier centrepostcode
    __centrepostcode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'centrepostcode'), 'centrepostcode', '__AbsentNamespace0_CTD_ANON__centrepostcode', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 59, 28), )

    
    centrepostcode = property(__centrepostcode.value, __centrepostcode.set, None, None)

    
    # Element centretelephone uses Python identifier centretelephone
    __centretelephone = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'centretelephone'), 'centretelephone', '__AbsentNamespace0_CTD_ANON__centretelephone', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 66, 28), )

    
    centretelephone = property(__centretelephone.value, __centretelephone.set, None, None)

    
    # Element centreemail uses Python identifier centreemail
    __centreemail = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'centreemail'), 'centreemail', '__AbsentNamespace0_CTD_ANON__centreemail', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 73, 28), )

    
    centreemail = property(__centreemail.value, __centreemail.set, None, None)

    _ElementMap.update({
        __centrecode.name() : __centrecode,
        __centrename.name() : __centrename,
        __centreaddress1.name() : __centreaddress1,
        __centreaddress2.name() : __centreaddress2,
        __centreaddress3.name() : __centreaddress3,
        __centreaddress4.name() : __centreaddress4,
        __centrepostcode.name() : __centrepostcode,
        __centretelephone.name() : __centretelephone,
        __centreemail.name() : __centreemail
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 84, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element gpname uses Python identifier gpname
    __gpname = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'gpname'), 'gpname', '__AbsentNamespace0_CTD_ANON_2_gpname', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 86, 28), )

    
    gpname = property(__gpname.value, __gpname.set, None, None)

    
    # Element gpaddress1 uses Python identifier gpaddress1
    __gpaddress1 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'gpaddress1'), 'gpaddress1', '__AbsentNamespace0_CTD_ANON_2_gpaddress1', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 93, 28), )

    
    gpaddress1 = property(__gpaddress1.value, __gpaddress1.set, None, None)

    
    # Element gpaddress2 uses Python identifier gpaddress2
    __gpaddress2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'gpaddress2'), 'gpaddress2', '__AbsentNamespace0_CTD_ANON_2_gpaddress2', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 100, 28), )

    
    gpaddress2 = property(__gpaddress2.value, __gpaddress2.set, None, None)

    
    # Element gpaddress3 uses Python identifier gpaddress3
    __gpaddress3 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'gpaddress3'), 'gpaddress3', '__AbsentNamespace0_CTD_ANON_2_gpaddress3', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 107, 28), )

    
    gpaddress3 = property(__gpaddress3.value, __gpaddress3.set, None, None)

    
    # Element gpaddress4 uses Python identifier gpaddress4
    __gpaddress4 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'gpaddress4'), 'gpaddress4', '__AbsentNamespace0_CTD_ANON_2_gpaddress4', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 114, 28), )

    
    gpaddress4 = property(__gpaddress4.value, __gpaddress4.set, None, None)

    
    # Element gppostcode uses Python identifier gppostcode
    __gppostcode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'gppostcode'), 'gppostcode', '__AbsentNamespace0_CTD_ANON_2_gppostcode', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 121, 28), )

    
    gppostcode = property(__gppostcode.value, __gppostcode.set, None, None)

    
    # Element gptelephone uses Python identifier gptelephone
    __gptelephone = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'gptelephone'), 'gptelephone', '__AbsentNamespace0_CTD_ANON_2_gptelephone', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 128, 28), )

    
    gptelephone = property(__gptelephone.value, __gptelephone.set, None, None)

    
    # Element gpemail uses Python identifier gpemail
    __gpemail = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'gpemail'), 'gpemail', '__AbsentNamespace0_CTD_ANON_2_gpemail', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 135, 28), )

    
    gpemail = property(__gpemail.value, __gpemail.set, None, None)

    _ElementMap.update({
        __gpname.name() : __gpname,
        __gpaddress1.name() : __gpaddress1,
        __gpaddress2.name() : __gpaddress2,
        __gpaddress3.name() : __gpaddress3,
        __gpaddress4.name() : __gpaddress4,
        __gppostcode.name() : __gppostcode,
        __gptelephone.name() : __gptelephone,
        __gpemail.name() : __gpemail
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 146, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element personaldetails uses Python identifier personaldetails
    __personaldetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'personaldetails'), 'personaldetails', '__AbsentNamespace0_CTD_ANON_3_personaldetails', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 148, 28), )

    
    personaldetails = property(__personaldetails.value, __personaldetails.set, None, None)

    
    # Element clinicaldetails uses Python identifier clinicaldetails
    __clinicaldetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'clinicaldetails'), 'clinicaldetails', '__AbsentNamespace0_CTD_ANON_3_clinicaldetails', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 242, 28), )

    
    clinicaldetails = property(__clinicaldetails.value, __clinicaldetails.set, None, None)

    
    # Element testdetails uses Python identifier testdetails
    __testdetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'testdetails'), 'testdetails', '__AbsentNamespace0_CTD_ANON_3_testdetails', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 279, 28), )

    
    testdetails = property(__testdetails.value, __testdetails.set, None, None)

    
    # Element drugdetails uses Python identifier drugdetails
    __drugdetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'drugdetails'), 'drugdetails', '__AbsentNamespace0_CTD_ANON_3_drugdetails', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 280, 28), )

    
    drugdetails = property(__drugdetails.value, __drugdetails.set, None, None)

    
    # Element letterdetails uses Python identifier letterdetails
    __letterdetails = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'letterdetails'), 'letterdetails', '__AbsentNamespace0_CTD_ANON_3_letterdetails', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 281, 28), )

    
    letterdetails = property(__letterdetails.value, __letterdetails.set, None, None)

    
    # Element diagnostics uses Python identifier diagnostics
    __diagnostics = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'diagnostics'), 'diagnostics', '__AbsentNamespace0_CTD_ANON_3_diagnostics', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 282, 28), )

    
    diagnostics = property(__diagnostics.value, __diagnostics.set, None, None)

    
    # Element footcheckup uses Python identifier footcheckup
    __footcheckup = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'footcheckup'), 'footcheckup', '__AbsentNamespace0_CTD_ANON_3_footcheckup', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 298, 28), )

    
    footcheckup = property(__footcheckup.value, __footcheckup.set, None, None)

    
    # Element eyecheckup uses Python identifier eyecheckup
    __eyecheckup = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'eyecheckup'), 'eyecheckup', '__AbsentNamespace0_CTD_ANON_3_eyecheckup', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 314, 28), )

    
    eyecheckup = property(__eyecheckup.value, __eyecheckup.set, None, None)

    
    # Element allergy uses Python identifier allergy
    __allergy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'allergy'), 'allergy', '__AbsentNamespace0_CTD_ANON_3_allergy', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 332, 28), )

    
    allergy = property(__allergy.value, __allergy.set, None, None)

    _ElementMap.update({
        __personaldetails.name() : __personaldetails,
        __clinicaldetails.name() : __clinicaldetails,
        __testdetails.name() : __testdetails,
        __drugdetails.name() : __drugdetails,
        __letterdetails.name() : __letterdetails,
        __diagnostics.name() : __diagnostics,
        __footcheckup.name() : __footcheckup,
        __eyecheckup.name() : __eyecheckup,
        __allergy.name() : __allergy
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 149, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element surname uses Python identifier surname
    __surname = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'surname'), 'surname', '__AbsentNamespace0_CTD_ANON_4_surname', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 151, 40), )

    
    surname = property(__surname.value, __surname.set, None, None)

    
    # Element forename uses Python identifier forename
    __forename = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'forename'), 'forename', '__AbsentNamespace0_CTD_ANON_4_forename', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 158, 40), )

    
    forename = property(__forename.value, __forename.set, None, None)

    
    # Element dateofbirth uses Python identifier dateofbirth
    __dateofbirth = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'dateofbirth'), 'dateofbirth', '__AbsentNamespace0_CTD_ANON_4_dateofbirth', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 165, 40), )

    
    dateofbirth = property(__dateofbirth.value, __dateofbirth.set, None, None)

    
    # Element sex uses Python identifier sex
    __sex = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'sex'), 'sex', '__AbsentNamespace0_CTD_ANON_4_sex', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 166, 40), )

    
    sex = property(__sex.value, __sex.set, None, None)

    
    # Element nhsno uses Python identifier nhsno
    __nhsno = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'nhsno'), 'nhsno', '__AbsentNamespace0_CTD_ANON_4_nhsno', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 167, 40), )

    
    nhsno = property(__nhsno.value, __nhsno.set, None, None)

    
    # Element ethnicorigin uses Python identifier ethnicorigin
    __ethnicorigin = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ethnicorigin'), 'ethnicorigin', '__AbsentNamespace0_CTD_ANON_4_ethnicorigin', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 175, 40), )

    
    ethnicorigin = property(__ethnicorigin.value, __ethnicorigin.set, None, None)

    
    # Element hospitalnumber uses Python identifier hospitalnumber
    __hospitalnumber = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'hospitalnumber'), 'hospitalnumber', '__AbsentNamespace0_CTD_ANON_4_hospitalnumber', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 176, 40), )

    
    hospitalnumber = property(__hospitalnumber.value, __hospitalnumber.set, None, None)

    
    # Element address1 uses Python identifier address1
    __address1 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'address1'), 'address1', '__AbsentNamespace0_CTD_ANON_4_address1', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 183, 40), )

    
    address1 = property(__address1.value, __address1.set, None, None)

    
    # Element address2 uses Python identifier address2
    __address2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'address2'), 'address2', '__AbsentNamespace0_CTD_ANON_4_address2', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 190, 40), )

    
    address2 = property(__address2.value, __address2.set, None, None)

    
    # Element address3 uses Python identifier address3
    __address3 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'address3'), 'address3', '__AbsentNamespace0_CTD_ANON_4_address3', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 197, 40), )

    
    address3 = property(__address3.value, __address3.set, None, None)

    
    # Element address4 uses Python identifier address4
    __address4 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'address4'), 'address4', '__AbsentNamespace0_CTD_ANON_4_address4', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 204, 40), )

    
    address4 = property(__address4.value, __address4.set, None, None)

    
    # Element postcode uses Python identifier postcode
    __postcode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'postcode'), 'postcode', '__AbsentNamespace0_CTD_ANON_4_postcode', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 211, 40), )

    
    postcode = property(__postcode.value, __postcode.set, None, None)

    
    # Element telephone1 uses Python identifier telephone1
    __telephone1 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'telephone1'), 'telephone1', '__AbsentNamespace0_CTD_ANON_4_telephone1', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 218, 40), )

    
    telephone1 = property(__telephone1.value, __telephone1.set, None, None)

    
    # Element telephone2 uses Python identifier telephone2
    __telephone2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'telephone2'), 'telephone2', '__AbsentNamespace0_CTD_ANON_4_telephone2', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 225, 40), )

    
    telephone2 = property(__telephone2.value, __telephone2.set, None, None)

    
    # Element mobile uses Python identifier mobile
    __mobile = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mobile'), 'mobile', '__AbsentNamespace0_CTD_ANON_4_mobile', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 232, 40), )

    
    mobile = property(__mobile.value, __mobile.set, None, None)

    _ElementMap.update({
        __surname.name() : __surname,
        __forename.name() : __forename,
        __dateofbirth.name() : __dateofbirth,
        __sex.name() : __sex,
        __nhsno.name() : __nhsno,
        __ethnicorigin.name() : __ethnicorigin,
        __hospitalnumber.name() : __hospitalnumber,
        __address1.name() : __address1,
        __address2.name() : __address2,
        __address3.name() : __address3,
        __address4.name() : __address4,
        __postcode.name() : __postcode,
        __telephone1.name() : __telephone1,
        __telephone2.name() : __telephone2,
        __mobile.name() : __mobile
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_4 = CTD_ANON_4


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 243, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element rrtstatus uses Python identifier rrtstatus
    __rrtstatus = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rrtstatus'), 'rrtstatus', '__AbsentNamespace0_CTD_ANON_5_rrtstatus', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 245, 40), )

    
    rrtstatus = property(__rrtstatus.value, __rrtstatus.set, None, None)

    
    # Element tpstatus uses Python identifier tpstatus
    __tpstatus = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'tpstatus'), 'tpstatus', '__AbsentNamespace0_CTD_ANON_5_tpstatus', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 246, 40), )

    
    tpstatus = property(__tpstatus.value, __tpstatus.set, None, None)

    
    # Element diagnosisedta uses Python identifier diagnosisedta
    __diagnosisedta = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'diagnosisedta'), 'diagnosisedta', '__AbsentNamespace0_CTD_ANON_5_diagnosisedta', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 253, 40), )

    
    diagnosisedta = property(__diagnosisedta.value, __diagnosisedta.set, None, None)

    
    # Element diagnosisdate uses Python identifier diagnosisdate
    __diagnosisdate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'diagnosisdate'), 'diagnosisdate', '__AbsentNamespace0_CTD_ANON_5_diagnosisdate', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 260, 40), )

    
    diagnosisdate = property(__diagnosisdate.value, __diagnosisdate.set, None, None)

    
    # Element diagnosis uses Python identifier diagnosis
    __diagnosis = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'diagnosis'), 'diagnosis', '__AbsentNamespace0_CTD_ANON_5_diagnosis', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 261, 40), )

    
    diagnosis = property(__diagnosis.value, __diagnosis.set, None, None)

    
    # Element ibddiseaseextent uses Python identifier ibddiseaseextent
    __ibddiseaseextent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ibddiseaseextent'), 'ibddiseaseextent', '__AbsentNamespace0_CTD_ANON_5_ibddiseaseextent', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 262, 40), )

    
    ibddiseaseextent = property(__ibddiseaseextent.value, __ibddiseaseextent.set, None, None)

    
    # Element ibddiseasecomplications uses Python identifier ibddiseasecomplications
    __ibddiseasecomplications = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ibddiseasecomplications'), 'ibddiseasecomplications', '__AbsentNamespace0_CTD_ANON_5_ibddiseasecomplications', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 263, 40), )

    
    ibddiseasecomplications = property(__ibddiseasecomplications.value, __ibddiseasecomplications.set, None, None)

    
    # Element bodypartsaffected uses Python identifier bodypartsaffected
    __bodypartsaffected = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'bodypartsaffected'), 'bodypartsaffected', '__AbsentNamespace0_CTD_ANON_5_bodypartsaffected', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 264, 40), )

    
    bodypartsaffected = property(__bodypartsaffected.value, __bodypartsaffected.set, None, None)

    
    # Element familyhistory uses Python identifier familyhistory
    __familyhistory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'familyhistory'), 'familyhistory', '__AbsentNamespace0_CTD_ANON_5_familyhistory', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 265, 40), )

    
    familyhistory = property(__familyhistory.value, __familyhistory.set, None, None)

    
    # Element smokinghistory uses Python identifier smokinghistory
    __smokinghistory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'smokinghistory'), 'smokinghistory', '__AbsentNamespace0_CTD_ANON_5_smokinghistory', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 266, 40), )

    
    smokinghistory = property(__smokinghistory.value, __smokinghistory.set, None, None)

    
    # Element surgicalhistory uses Python identifier surgicalhistory
    __surgicalhistory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'surgicalhistory'), 'surgicalhistory', '__AbsentNamespace0_CTD_ANON_5_surgicalhistory', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 267, 40), )

    
    surgicalhistory = property(__surgicalhistory.value, __surgicalhistory.set, None, None)

    
    # Element vaccinationrecord uses Python identifier vaccinationrecord
    __vaccinationrecord = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'vaccinationrecord'), 'vaccinationrecord', '__AbsentNamespace0_CTD_ANON_5_vaccinationrecord', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 268, 40), )

    
    vaccinationrecord = property(__vaccinationrecord.value, __vaccinationrecord.set, None, None)

    
    # Element bloodgroup uses Python identifier bloodgroup
    __bloodgroup = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'bloodgroup'), 'bloodgroup', '__AbsentNamespace0_CTD_ANON_5_bloodgroup', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 269, 40), )

    
    bloodgroup = property(__bloodgroup.value, __bloodgroup.set, None, None)

    _ElementMap.update({
        __rrtstatus.name() : __rrtstatus,
        __tpstatus.name() : __tpstatus,
        __diagnosisedta.name() : __diagnosisedta,
        __diagnosisdate.name() : __diagnosisdate,
        __diagnosis.name() : __diagnosis,
        __ibddiseaseextent.name() : __ibddiseaseextent,
        __ibddiseasecomplications.name() : __ibddiseasecomplications,
        __bodypartsaffected.name() : __bodypartsaffected,
        __familyhistory.name() : __familyhistory,
        __smokinghistory.name() : __smokinghistory,
        __surgicalhistory.name() : __surgicalhistory,
        __vaccinationrecord.name() : __vaccinationrecord,
        __bloodgroup.name() : __bloodgroup
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_5 = CTD_ANON_5


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 283, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element diagnostic uses Python identifier diagnostic
    __diagnostic = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'diagnostic'), 'diagnostic', '__AbsentNamespace0_CTD_ANON_6_diagnostic', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 285, 40), )

    
    diagnostic = property(__diagnostic.value, __diagnostic.set, None, None)

    _ElementMap.update({
        __diagnostic.name() : __diagnostic
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_6 = CTD_ANON_6


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 286, 44)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element diagnosticdate uses Python identifier diagnosticdate
    __diagnosticdate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'diagnosticdate'), 'diagnosticdate', '__AbsentNamespace0_CTD_ANON_7_diagnosticdate', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 288, 52), )

    
    diagnosticdate = property(__diagnosticdate.value, __diagnosticdate.set, None, None)

    
    # Element diagnosticresult uses Python identifier diagnosticresult
    __diagnosticresult = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'diagnosticresult'), 'diagnosticresult', '__AbsentNamespace0_CTD_ANON_7_diagnosticresult', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 289, 52), )

    
    diagnosticresult = property(__diagnosticresult.value, __diagnosticresult.set, None, None)

    
    # Element diagnosticname uses Python identifier diagnosticname
    __diagnosticname = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'diagnosticname'), 'diagnosticname', '__AbsentNamespace0_CTD_ANON_7_diagnosticname', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 290, 52), )

    
    diagnosticname = property(__diagnosticname.value, __diagnosticname.set, None, None)

    
    # Element diagnostictype uses Python identifier diagnostictype
    __diagnostictype = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'diagnostictype'), 'diagnostictype', '__AbsentNamespace0_CTD_ANON_7_diagnostictype', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 291, 52), )

    
    diagnostictype = property(__diagnostictype.value, __diagnostictype.set, None, None)

    _ElementMap.update({
        __diagnosticdate.name() : __diagnosticdate,
        __diagnosticresult.name() : __diagnosticresult,
        __diagnosticname.name() : __diagnosticname,
        __diagnostictype.name() : __diagnostictype
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_7 = CTD_ANON_7


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 299, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element datestamp uses Python identifier datestamp
    __datestamp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'datestamp'), 'datestamp', '__AbsentNamespace0_CTD_ANON_8_datestamp', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 301, 40), )

    
    datestamp = property(__datestamp.value, __datestamp.set, None, None)

    
    # Element foot uses Python identifier foot
    __foot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'foot'), 'foot', '__AbsentNamespace0_CTD_ANON_8_foot', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 302, 40), )

    
    foot = property(__foot.value, __foot.set, None, None)

    _ElementMap.update({
        __datestamp.name() : __datestamp,
        __foot.name() : __foot
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_8 = CTD_ANON_8


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 303, 44)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element ptpulse uses Python identifier ptpulse
    __ptpulse = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ptpulse'), 'ptpulse', '__AbsentNamespace0_CTD_ANON_9_ptpulse', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 305, 52), )

    
    ptpulse = property(__ptpulse.value, __ptpulse.set, None, None)

    
    # Element dppulse uses Python identifier dppulse
    __dppulse = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'dppulse'), 'dppulse', '__AbsentNamespace0_CTD_ANON_9_dppulse', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 306, 52), )

    
    dppulse = property(__dppulse.value, __dppulse.set, None, None)

    
    # Attribute side uses Python identifier side
    __side = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'side'), 'side', '__AbsentNamespace0_CTD_ANON_9_side', pyxb.binding.datatypes.string, required=True)
    __side._DeclarationLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 308, 48)
    __side._UseLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 308, 48)
    
    side = property(__side.value, __side.set, None, None)

    _ElementMap.update({
        __ptpulse.name() : __ptpulse,
        __dppulse.name() : __dppulse
    })
    _AttributeMap.update({
        __side.name() : __side
    })
_module_typeBindings.CTD_ANON_9 = CTD_ANON_9


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 315, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element datestamp uses Python identifier datestamp
    __datestamp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'datestamp'), 'datestamp', '__AbsentNamespace0_CTD_ANON_10_datestamp', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 317, 40), )

    
    datestamp = property(__datestamp.value, __datestamp.set, None, None)

    
    # Element location uses Python identifier location
    __location = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'location'), 'location', '__AbsentNamespace0_CTD_ANON_10_location', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 318, 40), )

    
    location = property(__location.value, __location.set, None, None)

    
    # Element eye uses Python identifier eye
    __eye = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'eye'), 'eye', '__AbsentNamespace0_CTD_ANON_10_eye', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 319, 40), )

    
    eye = property(__eye.value, __eye.set, None, None)

    _ElementMap.update({
        __datestamp.name() : __datestamp,
        __location.name() : __location,
        __eye.name() : __eye
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_10 = CTD_ANON_10


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 320, 44)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element rgrade uses Python identifier rgrade
    __rgrade = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rgrade'), 'rgrade', '__AbsentNamespace0_CTD_ANON_11_rgrade', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 322, 52), )

    
    rgrade = property(__rgrade.value, __rgrade.set, None, None)

    
    # Element mgrade uses Python identifier mgrade
    __mgrade = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mgrade'), 'mgrade', '__AbsentNamespace0_CTD_ANON_11_mgrade', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 323, 52), )

    
    mgrade = property(__mgrade.value, __mgrade.set, None, None)

    
    # Element va uses Python identifier va
    __va = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'va'), 'va', '__AbsentNamespace0_CTD_ANON_11_va', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 324, 52), )

    
    va = property(__va.value, __va.set, None, None)

    
    # Attribute side uses Python identifier side
    __side = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'side'), 'side', '__AbsentNamespace0_CTD_ANON_11_side', pyxb.binding.datatypes.string, required=True)
    __side._DeclarationLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 326, 48)
    __side._UseLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 326, 48)
    
    side = property(__side.value, __side.set, None, None)

    _ElementMap.update({
        __rgrade.name() : __rgrade,
        __mgrade.name() : __mgrade,
        __va.name() : __va
    })
    _AttributeMap.update({
        __side.name() : __side
    })
_module_typeBindings.CTD_ANON_11 = CTD_ANON_11


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 333, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element allergysubstance uses Python identifier allergysubstance
    __allergysubstance = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'allergysubstance'), 'allergysubstance', '__AbsentNamespace0_CTD_ANON_12_allergysubstance', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 335, 40), )

    
    allergysubstance = property(__allergysubstance.value, __allergysubstance.set, None, None)

    
    # Element allergytypecode uses Python identifier allergytypecode
    __allergytypecode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'allergytypecode'), 'allergytypecode', '__AbsentNamespace0_CTD_ANON_12_allergytypecode', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 336, 40), )

    
    allergytypecode = property(__allergytypecode.value, __allergytypecode.set, None, None)

    
    # Element allergyreaction uses Python identifier allergyreaction
    __allergyreaction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'allergyreaction'), 'allergyreaction', '__AbsentNamespace0_CTD_ANON_12_allergyreaction', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 337, 40), )

    
    allergyreaction = property(__allergyreaction.value, __allergyreaction.set, None, None)

    
    # Element allergyconfidencelevel uses Python identifier allergyconfidencelevel
    __allergyconfidencelevel = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'allergyconfidencelevel'), 'allergyconfidencelevel', '__AbsentNamespace0_CTD_ANON_12_allergyconfidencelevel', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 338, 40), )

    
    allergyconfidencelevel = property(__allergyconfidencelevel.value, __allergyconfidencelevel.set, None, None)

    
    # Element allergyinfosource uses Python identifier allergyinfosource
    __allergyinfosource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'allergyinfosource'), 'allergyinfosource', '__AbsentNamespace0_CTD_ANON_12_allergyinfosource', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 339, 40), )

    
    allergyinfosource = property(__allergyinfosource.value, __allergyinfosource.set, None, None)

    
    # Element allergystatus uses Python identifier allergystatus
    __allergystatus = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'allergystatus'), 'allergystatus', '__AbsentNamespace0_CTD_ANON_12_allergystatus', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 340, 40), )

    
    allergystatus = property(__allergystatus.value, __allergystatus.set, None, None)

    
    # Element allergydescription uses Python identifier allergydescription
    __allergydescription = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'allergydescription'), 'allergydescription', '__AbsentNamespace0_CTD_ANON_12_allergydescription', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 341, 40), )

    
    allergydescription = property(__allergydescription.value, __allergydescription.set, None, None)

    
    # Element allergyrecordeddate uses Python identifier allergyrecordeddate
    __allergyrecordeddate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'allergyrecordeddate'), 'allergyrecordeddate', '__AbsentNamespace0_CTD_ANON_12_allergyrecordeddate', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 342, 40), )

    
    allergyrecordeddate = property(__allergyrecordeddate.value, __allergyrecordeddate.set, None, None)

    _ElementMap.update({
        __allergysubstance.name() : __allergysubstance,
        __allergytypecode.name() : __allergytypecode,
        __allergyreaction.name() : __allergyreaction,
        __allergyconfidencelevel.name() : __allergyconfidencelevel,
        __allergyinfosource.name() : __allergyinfosource,
        __allergystatus.name() : __allergystatus,
        __allergydescription.name() : __allergydescription,
        __allergyrecordeddate.name() : __allergyrecordeddate
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_12 = CTD_ANON_12


# Complex type letterdetails with content type ELEMENT_ONLY
class letterdetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type letterdetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'letterdetails')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 353, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element letter uses Python identifier letter
    __letter = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'letter'), 'letter', '__AbsentNamespace0_letterdetails_letter', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 355, 12), )

    
    letter = property(__letter.value, __letter.set, None, None)

    _ElementMap.update({
        __letter.name() : __letter
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.letterdetails = letterdetails
Namespace.addCategoryObject('typeBinding', 'letterdetails', letterdetails)


# Complex type letter with content type ELEMENT_ONLY
class letter (pyxb.binding.basis.complexTypeDefinition):
    """Complex type letter with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'letter')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 360, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element letterdate uses Python identifier letterdate
    __letterdate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'letterdate'), 'letterdate', '__AbsentNamespace0_letter_letterdate', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 362, 12), )

    
    letterdate = property(__letterdate.value, __letterdate.set, None, None)

    
    # Element lettertitle uses Python identifier lettertitle
    __lettertitle = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'lettertitle'), 'lettertitle', '__AbsentNamespace0_letter_lettertitle', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 363, 12), )

    
    lettertitle = property(__lettertitle.value, __lettertitle.set, None, None)

    
    # Element letterfilename uses Python identifier letterfilename
    __letterfilename = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'letterfilename'), 'letterfilename', '__AbsentNamespace0_letter_letterfilename', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 364, 12), )

    
    letterfilename = property(__letterfilename.value, __letterfilename.set, None, None)

    
    # Element letterfiletype uses Python identifier letterfiletype
    __letterfiletype = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'letterfiletype'), 'letterfiletype', '__AbsentNamespace0_letter_letterfiletype', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 365, 12), )

    
    letterfiletype = property(__letterfiletype.value, __letterfiletype.set, None, None)

    
    # Element lettertype uses Python identifier lettertype
    __lettertype = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'lettertype'), 'lettertype', '__AbsentNamespace0_letter_lettertype', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 366, 12), )

    
    lettertype = property(__lettertype.value, __lettertype.set, None, None)

    
    # Element lettercontent uses Python identifier lettercontent
    __lettercontent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'lettercontent'), 'lettercontent', '__AbsentNamespace0_letter_lettercontent', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 373, 12), )

    
    lettercontent = property(__lettercontent.value, __lettercontent.set, None, '\n                        Letter content should be sent as a CDATA section to avoid parsing errors. E.g. and end with the string \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t')

    
    # Element letterfilebody uses Python identifier letterfilebody
    __letterfilebody = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'letterfilebody'), 'letterfilebody', '__AbsentNamespace0_letter_letterfilebody', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 379, 12), )

    
    letterfilebody = property(__letterfilebody.value, __letterfilebody.set, None, '\n                        This property is used when the Note is binary data, e.g DOC, PDF, JPG\n                    ')

    _ElementMap.update({
        __letterdate.name() : __letterdate,
        __lettertitle.name() : __lettertitle,
        __letterfilename.name() : __letterfilename,
        __letterfiletype.name() : __letterfiletype,
        __lettertype.name() : __lettertype,
        __lettercontent.name() : __lettercontent,
        __letterfilebody.name() : __letterfilebody
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.letter = letter
Namespace.addCategoryObject('typeBinding', 'letter', letter)


# Complex type drugdetails with content type ELEMENT_ONLY
class drugdetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type drugdetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'drugdetails')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 389, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element drug uses Python identifier drug
    __drug = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'drug'), 'drug', '__AbsentNamespace0_drugdetails_drug', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 391, 12), )

    
    drug = property(__drug.value, __drug.set, None, None)

    _ElementMap.update({
        __drug.name() : __drug
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.drugdetails = drugdetails
Namespace.addCategoryObject('typeBinding', 'drugdetails', drugdetails)


# Complex type drug with content type ELEMENT_ONLY
class drug (pyxb.binding.basis.complexTypeDefinition):
    """Complex type drug with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'drug')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 395, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element drugstartdate uses Python identifier drugstartdate
    __drugstartdate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'drugstartdate'), 'drugstartdate', '__AbsentNamespace0_drug_drugstartdate', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 397, 12), )

    
    drugstartdate = property(__drugstartdate.value, __drugstartdate.set, None, None)

    
    # Element drugname uses Python identifier drugname
    __drugname = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'drugname'), 'drugname', '__AbsentNamespace0_drug_drugname', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 398, 12), )

    
    drugname = property(__drugname.value, __drugname.set, None, None)

    
    # Element drugdose uses Python identifier drugdose
    __drugdose = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'drugdose'), 'drugdose', '__AbsentNamespace0_drug_drugdose', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 405, 12), )

    
    drugdose = property(__drugdose.value, __drugdose.set, None, None)

    
    # Element code uses Python identifier code
    __code = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'code'), 'code', '__AbsentNamespace0_drug_code', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 412, 12), )

    
    code = property(__code.value, __code.set, None, None)

    _ElementMap.update({
        __drugstartdate.name() : __drugstartdate,
        __drugname.name() : __drugname,
        __drugdose.name() : __drugdose,
        __code.name() : __code
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.drug = drug
Namespace.addCategoryObject('typeBinding', 'drug', drug)


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 413, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element codetype uses Python identifier codetype
    __codetype = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'codetype'), 'codetype', '__AbsentNamespace0_CTD_ANON_13_codetype', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 415, 24), )

    
    codetype = property(__codetype.value, __codetype.set, None, None)

    
    # Element codevalue uses Python identifier codevalue
    __codevalue = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'codevalue'), 'codevalue', '__AbsentNamespace0_CTD_ANON_13_codevalue', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 416, 24), )

    
    codevalue = property(__codevalue.value, __codevalue.set, None, None)

    _ElementMap.update({
        __codetype.name() : __codetype,
        __codevalue.name() : __codevalue
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_13 = CTD_ANON_13


# Complex type testdetails with content type ELEMENT_ONLY
class testdetails (pyxb.binding.basis.complexTypeDefinition):
    """Complex type testdetails with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'testdetails')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 423, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element test uses Python identifier test
    __test = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'test'), 'test', '__AbsentNamespace0_testdetails_test', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 425, 12), )

    
    test = property(__test.value, __test.set, None, None)

    _ElementMap.update({
        __test.name() : __test
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.testdetails = testdetails
Namespace.addCategoryObject('typeBinding', 'testdetails', testdetails)


# Complex type test with content type ELEMENT_ONLY
class test (pyxb.binding.basis.complexTypeDefinition):
    """Complex type test with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'test')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 429, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element testname uses Python identifier testname
    __testname = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'testname'), 'testname', '__AbsentNamespace0_test_testname', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 431, 12), )

    
    testname = property(__testname.value, __testname.set, None, None)

    
    # Element testcode uses Python identifier testcode
    __testcode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'testcode'), 'testcode', '__AbsentNamespace0_test_testcode', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 438, 12), )

    
    testcode = property(__testcode.value, __testcode.set, None, None)

    
    # Element units uses Python identifier units
    __units = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'units'), 'units', '__AbsentNamespace0_test_units', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 439, 12), )

    
    units = property(__units.value, __units.set, None, None)

    
    # Element daterange uses Python identifier daterange
    __daterange = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'daterange'), 'daterange', '__AbsentNamespace0_test_daterange', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 446, 12), )

    
    daterange = property(__daterange.value, __daterange.set, None, None)

    
    # Element result uses Python identifier result
    __result = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'result'), 'result', '__AbsentNamespace0_test_result', True, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 452, 12), )

    
    result = property(__result.value, __result.set, None, None)

    _ElementMap.update({
        __testname.name() : __testname,
        __testcode.name() : __testcode,
        __units.name() : __units,
        __daterange.name() : __daterange,
        __result.name() : __result
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.test = test
Namespace.addCategoryObject('typeBinding', 'test', test)


# Complex type [anonymous] with content type EMPTY
class CTD_ANON_14 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type EMPTY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 447, 16)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Attribute start uses Python identifier start
    __start = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'start'), 'start', '__AbsentNamespace0_CTD_ANON_14_start', pyxb.binding.datatypes.date, required=True)
    __start._DeclarationLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 448, 20)
    __start._UseLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 448, 20)
    
    start = property(__start.value, __start.set, None, None)

    
    # Attribute stop uses Python identifier stop
    __stop = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'stop'), 'stop', '__AbsentNamespace0_CTD_ANON_14_stop', pyxb.binding.datatypes.date, required=True)
    __stop._DeclarationLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 449, 20)
    __stop._UseLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 449, 20)
    
    stop = property(__stop.value, __stop.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __start.name() : __start,
        __stop.name() : __stop
    })
_module_typeBindings.CTD_ANON_14 = CTD_ANON_14


# Complex type result with content type ELEMENT_ONLY
class result (pyxb.binding.basis.complexTypeDefinition):
    """Complex type result with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'result')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 456, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element datestamp uses Python identifier datestamp
    __datestamp = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'datestamp'), 'datestamp', '__AbsentNamespace0_result_datestamp', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 458, 12), )

    
    datestamp = property(__datestamp.value, __datestamp.set, None, None)

    
    # Element prepost uses Python identifier prepost
    __prepost = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'prepost'), 'prepost', '__AbsentNamespace0_result_prepost', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 459, 12), )

    
    prepost = property(__prepost.value, __prepost.set, None, None)

    
    # Element value uses Python identifier value_
    __value = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'value'), 'value_', '__AbsentNamespace0_result_value', False, pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 460, 12), )

    
    value_ = property(__value.value, __value.set, None, None)

    _ElementMap.update({
        __datestamp.name() : __datestamp,
        __prepost.name() : __prepost,
        __value.name() : __value
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.result = result
Namespace.addCategoryObject('typeBinding', 'result', result)


# Complex type pv_diagnosis with content type SIMPLE
class pv_diagnosis (pyxb.binding.basis.complexTypeDefinition):
    """Complex type pv_diagnosis with content type SIMPLE"""
    _TypeDefinition = pv_diagnosis_name
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'pv_diagnosis')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 471, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pv_diagnosis_name
    
    # Attribute primary uses Python identifier primary
    __primary = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'primary'), 'primary', '__AbsentNamespace0_pv_diagnosis_primary', pyxb.binding.datatypes.boolean, unicode_default='false')
    __primary._DeclarationLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 474, 16)
    __primary._UseLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 474, 16)
    
    primary = property(__primary.value, __primary.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __primary.name() : __primary
    })
_module_typeBindings.pv_diagnosis = pv_diagnosis
Namespace.addCategoryObject('typeBinding', 'pv_diagnosis', pv_diagnosis)


# Complex type ibd_disease_complications with content type SIMPLE
class ibd_disease_complications (pyxb.binding.basis.complexTypeDefinition):
    """Complex type ibd_disease_complications with content type SIMPLE"""
    _TypeDefinition = ibd_disease_complication
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ibd_disease_complications')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 503, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is ibd_disease_complication
    
    # Attribute primary uses Python identifier primary
    __primary = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'primary'), 'primary', '__AbsentNamespace0_ibd_disease_complications_primary', pyxb.binding.datatypes.boolean, unicode_default='false')
    __primary._DeclarationLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 506, 16)
    __primary._UseLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 506, 16)
    
    primary = property(__primary.value, __primary.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __primary.name() : __primary
    })
_module_typeBindings.ibd_disease_complications = ibd_disease_complications
Namespace.addCategoryObject('typeBinding', 'ibd_disease_complications', ibd_disease_complications)


# Complex type body_parts_affected with content type SIMPLE
class body_parts_affected (pyxb.binding.basis.complexTypeDefinition):
    """Complex type body_parts_affected with content type SIMPLE"""
    _TypeDefinition = body_part
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'body_parts_affected')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 518, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is body_part
    
    # Attribute primary uses Python identifier primary
    __primary = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'primary'), 'primary', '__AbsentNamespace0_body_parts_affected_primary', pyxb.binding.datatypes.boolean, unicode_default='false')
    __primary._DeclarationLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 521, 16)
    __primary._UseLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 521, 16)
    
    primary = property(__primary.value, __primary.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __primary.name() : __primary
    })
_module_typeBindings.body_parts_affected = body_parts_affected
Namespace.addCategoryObject('typeBinding', 'body_parts_affected', body_parts_affected)


# Complex type family_history with content type SIMPLE
class family_history (pyxb.binding.basis.complexTypeDefinition):
    """Complex type family_history with content type SIMPLE"""
    _TypeDefinition = family_history_description
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'family_history')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 532, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is family_history_description
    
    # Attribute primary uses Python identifier primary
    __primary = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'primary'), 'primary', '__AbsentNamespace0_family_history_primary', pyxb.binding.datatypes.boolean, unicode_default='false')
    __primary._DeclarationLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 535, 16)
    __primary._UseLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 535, 16)
    
    primary = property(__primary.value, __primary.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __primary.name() : __primary
    })
_module_typeBindings.family_history = family_history
Namespace.addCategoryObject('typeBinding', 'family_history', family_history)


# Complex type smoking_history with content type SIMPLE
class smoking_history (pyxb.binding.basis.complexTypeDefinition):
    """Complex type smoking_history with content type SIMPLE"""
    _TypeDefinition = smoking_history_description
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'smoking_history')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 547, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is smoking_history_description
    
    # Attribute primary uses Python identifier primary
    __primary = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'primary'), 'primary', '__AbsentNamespace0_smoking_history_primary', pyxb.binding.datatypes.boolean, unicode_default='false')
    __primary._DeclarationLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 550, 16)
    __primary._UseLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 550, 16)
    
    primary = property(__primary.value, __primary.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __primary.name() : __primary
    })
_module_typeBindings.smoking_history = smoking_history
Namespace.addCategoryObject('typeBinding', 'smoking_history', smoking_history)


# Complex type surgical_history with content type SIMPLE
class surgical_history (pyxb.binding.basis.complexTypeDefinition):
    """Complex type surgical_history with content type SIMPLE"""
    _TypeDefinition = surgical_history_description
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'surgical_history')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 562, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is surgical_history_description
    
    # Attribute primary uses Python identifier primary
    __primary = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'primary'), 'primary', '__AbsentNamespace0_surgical_history_primary', pyxb.binding.datatypes.boolean, unicode_default='false')
    __primary._DeclarationLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 565, 16)
    __primary._UseLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 565, 16)
    
    primary = property(__primary.value, __primary.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __primary.name() : __primary
    })
_module_typeBindings.surgical_history = surgical_history
Namespace.addCategoryObject('typeBinding', 'surgical_history', surgical_history)


# Complex type vaccination_record with content type SIMPLE
class vaccination_record (pyxb.binding.basis.complexTypeDefinition):
    """Complex type vaccination_record with content type SIMPLE"""
    _TypeDefinition = vaccination_record_description
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'vaccination_record')
    _XSDLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 577, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is vaccination_record_description
    
    # Attribute primary uses Python identifier primary
    __primary = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'primary'), 'primary', '__AbsentNamespace0_vaccination_record_primary', pyxb.binding.datatypes.boolean, unicode_default='false')
    __primary._DeclarationLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 580, 16)
    __primary._UseLocation = pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 580, 16)
    
    primary = property(__primary.value, __primary.set, None, None)

    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __primary.name() : __primary
    })
_module_typeBindings.vaccination_record = vaccination_record
Namespace.addCategoryObject('typeBinding', 'vaccination_record', vaccination_record)


patientview = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'patientview'), CTD_ANON, documentation='PatientView XML Schema', location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 3, 4))
Namespace.addCategoryObject('elementBinding', patientview.name().localName(), patientview)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'sequence'), STD_ANON, scope=CTD_ANON, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 9, 16)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'dateofreport'), pyxb.binding.datatypes.dateTime, scope=CTD_ANON, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 18, 16)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'flag'), pv_status, scope=CTD_ANON, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 19, 16)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'centredetails'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 20, 16)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'gpdetails'), CTD_ANON_2, scope=CTD_ANON, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 83, 16)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'patient'), CTD_ANON_3, scope=CTD_ANON, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 145, 16)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 9, 16))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 83, 16))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'sequence')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 9, 16))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'dateofreport')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 18, 16))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'flag')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 19, 16))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'centredetails')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 20, 16))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'gpdetails')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 83, 16))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(None, 'patient')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 145, 16))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'centrecode'), pyxb.binding.datatypes.string, scope=CTD_ANON_, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 23, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'centrename'), STD_ANON_, scope=CTD_ANON_, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 24, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'centreaddress1'), STD_ANON_2, scope=CTD_ANON_, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 31, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'centreaddress2'), STD_ANON_3, scope=CTD_ANON_, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 38, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'centreaddress3'), STD_ANON_4, scope=CTD_ANON_, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 45, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'centreaddress4'), STD_ANON_5, scope=CTD_ANON_, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 52, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'centrepostcode'), STD_ANON_6, scope=CTD_ANON_, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 59, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'centretelephone'), STD_ANON_7, scope=CTD_ANON_, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 66, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'centreemail'), STD_ANON_8, scope=CTD_ANON_, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 73, 28)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 24, 28))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 31, 28))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 38, 28))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 45, 28))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 52, 28))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 59, 28))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 66, 28))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 73, 28))
    counters.add(cc_7)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'centrecode')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 23, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'centrename')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 24, 28))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'centreaddress1')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 31, 28))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'centreaddress2')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 38, 28))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'centreaddress3')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 45, 28))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'centreaddress4')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 52, 28))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'centrepostcode')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 59, 28))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'centretelephone')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 66, 28))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(None, 'centreemail')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 73, 28))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()




CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'gpname'), STD_ANON_9, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 86, 28)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'gpaddress1'), STD_ANON_10, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 93, 28)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'gpaddress2'), STD_ANON_11, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 100, 28)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'gpaddress3'), STD_ANON_12, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 107, 28)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'gpaddress4'), STD_ANON_13, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 114, 28)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'gppostcode'), STD_ANON_14, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 121, 28)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'gptelephone'), STD_ANON_15, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 128, 28)))

CTD_ANON_2._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'gpemail'), STD_ANON_16, scope=CTD_ANON_2, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 135, 28)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 86, 28))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 93, 28))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 100, 28))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 107, 28))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 114, 28))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 121, 28))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 128, 28))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 135, 28))
    counters.add(cc_7)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'gpname')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 86, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'gpaddress1')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 93, 28))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'gpaddress2')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 100, 28))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'gpaddress3')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 107, 28))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'gpaddress4')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 114, 28))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'gppostcode')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 121, 28))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'gptelephone')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 128, 28))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_2._UseForTag(pyxb.namespace.ExpandedName(None, 'gpemail')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 135, 28))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_2._Automaton = _BuildAutomaton_2()




CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'personaldetails'), CTD_ANON_4, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 148, 28)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'clinicaldetails'), CTD_ANON_5, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 242, 28)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'testdetails'), testdetails, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 279, 28)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'drugdetails'), drugdetails, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 280, 28)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'letterdetails'), letterdetails, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 281, 28)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'diagnostics'), CTD_ANON_6, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 282, 28)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'footcheckup'), CTD_ANON_8, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 298, 28)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'eyecheckup'), CTD_ANON_10, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 314, 28)))

CTD_ANON_3._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'allergy'), CTD_ANON_12, scope=CTD_ANON_3, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 332, 28)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 242, 28))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 279, 28))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 280, 28))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 281, 28))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 282, 28))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 298, 28))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 314, 28))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 332, 28))
    counters.add(cc_7)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'personaldetails')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 148, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'clinicaldetails')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 242, 28))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'testdetails')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 279, 28))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'drugdetails')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 280, 28))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'letterdetails')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 281, 28))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'diagnostics')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 282, 28))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'footcheckup')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 298, 28))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'eyecheckup')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 314, 28))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_3._UseForTag(pyxb.namespace.ExpandedName(None, 'allergy')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 332, 28))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_3._Automaton = _BuildAutomaton_3()




CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'surname'), STD_ANON_17, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 151, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'forename'), STD_ANON_18, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 158, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'dateofbirth'), pyxb.binding.datatypes.date, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 165, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'sex'), sex, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 166, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'nhsno'), STD_ANON_19, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 167, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ethnicorigin'), pyxb.binding.datatypes.string, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 175, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'hospitalnumber'), STD_ANON_20, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 176, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'address1'), STD_ANON_21, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 183, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'address2'), STD_ANON_22, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 190, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'address3'), STD_ANON_23, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 197, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'address4'), STD_ANON_24, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 204, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'postcode'), STD_ANON_25, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 211, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'telephone1'), STD_ANON_26, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 218, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'telephone2'), STD_ANON_27, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 225, 40)))

CTD_ANON_4._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mobile'), STD_ANON_28, scope=CTD_ANON_4, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 232, 40)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 165, 40))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 166, 40))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 175, 40))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 176, 40))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 183, 40))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 190, 40))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 197, 40))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 204, 40))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 211, 40))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 218, 40))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 225, 40))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 232, 40))
    counters.add(cc_11)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'surname')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 151, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'forename')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 158, 40))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'dateofbirth')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 165, 40))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'sex')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 166, 40))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'nhsno')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 167, 40))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'ethnicorigin')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 175, 40))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'hospitalnumber')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 176, 40))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'address1')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 183, 40))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'address2')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 190, 40))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'address3')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 197, 40))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'address4')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 204, 40))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'postcode')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 211, 40))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'telephone1')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 218, 40))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'telephone2')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 225, 40))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_4._UseForTag(pyxb.namespace.ExpandedName(None, 'mobile')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 232, 40))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    transitions.append(fac.Transition(st_8, [
         ]))
    transitions.append(fac.Transition(st_9, [
         ]))
    transitions.append(fac.Transition(st_10, [
         ]))
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_11, True) ]))
    st_14._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_4._Automaton = _BuildAutomaton_4()




CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rrtstatus'), rrtstatus, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 245, 40)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'tpstatus'), STD_ANON_29, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 246, 40)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'diagnosisedta'), STD_ANON_30, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 253, 40)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'diagnosisdate'), pyxb.binding.datatypes.date, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 260, 40)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'diagnosis'), pv_diagnosis, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 261, 40)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ibddiseaseextent'), ibd_disease_extent, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 262, 40)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ibddiseasecomplications'), ibd_disease_complications, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 263, 40)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'bodypartsaffected'), body_parts_affected, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 264, 40)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'familyhistory'), family_history, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 265, 40)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'smokinghistory'), smoking_history, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 266, 40)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'surgicalhistory'), surgical_history, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 267, 40)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'vaccinationrecord'), vaccination_record, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 268, 40)))

CTD_ANON_5._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'bloodgroup'), STD_ANON_31, scope=CTD_ANON_5, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 269, 40)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 245, 40))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 246, 40))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 253, 40))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 260, 40))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 261, 40))
    counters.add(cc_4)
    cc_5 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 262, 40))
    counters.add(cc_5)
    cc_6 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 263, 40))
    counters.add(cc_6)
    cc_7 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 264, 40))
    counters.add(cc_7)
    cc_8 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 265, 40))
    counters.add(cc_8)
    cc_9 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 266, 40))
    counters.add(cc_9)
    cc_10 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 267, 40))
    counters.add(cc_10)
    cc_11 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 268, 40))
    counters.add(cc_11)
    cc_12 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 269, 40))
    counters.add(cc_12)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'rrtstatus')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 245, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'tpstatus')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 246, 40))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'diagnosisedta')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 253, 40))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'diagnosisdate')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 260, 40))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'diagnosis')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 261, 40))
    st_4 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_5, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'ibddiseaseextent')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 262, 40))
    st_5 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_6, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'ibddiseasecomplications')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 263, 40))
    st_6 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_7, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'bodypartsaffected')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 264, 40))
    st_7 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_8, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'familyhistory')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 265, 40))
    st_8 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_9, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'smokinghistory')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 266, 40))
    st_9 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_10, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'surgicalhistory')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 267, 40))
    st_10 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_11, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'vaccinationrecord')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 268, 40))
    st_11 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_12, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_5._UseForTag(pyxb.namespace.ExpandedName(None, 'bloodgroup')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 269, 40))
    st_12 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_3, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_4, True) ]))
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_4, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_4, False) ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_5, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_5, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_5, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_6, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_6, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_6, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_7, True) ]))
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_7, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_7, False) ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_8, True) ]))
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_8, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_8, False) ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
        fac.UpdateInstruction(cc_9, True) ]))
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_9, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_9, False) ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
        fac.UpdateInstruction(cc_10, True) ]))
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_10, False) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_10, False) ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_11, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_11, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_12, True) ]))
    st_12._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_5._Automaton = _BuildAutomaton_5()




CTD_ANON_6._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'diagnostic'), CTD_ANON_7, scope=CTD_ANON_6, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 285, 40)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_6._UseForTag(pyxb.namespace.ExpandedName(None, 'diagnostic')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 285, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_6._Automaton = _BuildAutomaton_6()




CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'diagnosticdate'), pyxb.binding.datatypes.dateTime, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 288, 52)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'diagnosticresult'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 289, 52)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'diagnosticname'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 290, 52)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'diagnostictype'), pyxb.binding.datatypes.string, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 291, 52)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 291, 52))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'diagnosticdate')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 288, 52))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'diagnosticresult')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 289, 52))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'diagnosticname')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 290, 52))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(None, 'diagnostictype')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 291, 52))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_7._Automaton = _BuildAutomaton_7()




CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'datestamp'), pyxb.binding.datatypes.date, scope=CTD_ANON_8, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 301, 40)))

CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'foot'), CTD_ANON_9, scope=CTD_ANON_8, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 302, 40)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(None, 'datestamp')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 301, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(None, 'foot')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 302, 40))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_8._Automaton = _BuildAutomaton_8()




CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ptpulse'), pyxb.binding.datatypes.string, scope=CTD_ANON_9, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 305, 52)))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'dppulse'), pyxb.binding.datatypes.string, scope=CTD_ANON_9, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 306, 52)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 305, 52))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 306, 52))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(None, 'ptpulse')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 305, 52))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(None, 'dppulse')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 306, 52))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_9._Automaton = _BuildAutomaton_9()




CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'datestamp'), pyxb.binding.datatypes.date, scope=CTD_ANON_10, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 317, 40)))

CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'location'), pyxb.binding.datatypes.string, scope=CTD_ANON_10, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 318, 40)))

CTD_ANON_10._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'eye'), CTD_ANON_11, scope=CTD_ANON_10, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 319, 40)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, 'datestamp')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 317, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, 'location')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 318, 40))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_10._UseForTag(pyxb.namespace.ExpandedName(None, 'eye')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 319, 40))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_10._Automaton = _BuildAutomaton_10()




CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rgrade'), pyxb.binding.datatypes.string, scope=CTD_ANON_11, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 322, 52)))

CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mgrade'), pyxb.binding.datatypes.string, scope=CTD_ANON_11, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 323, 52)))

CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'va'), pyxb.binding.datatypes.string, scope=CTD_ANON_11, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 324, 52)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 322, 52))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 323, 52))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 324, 52))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(None, 'rgrade')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 322, 52))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(None, 'mgrade')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 323, 52))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(None, 'va')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 324, 52))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_11._Automaton = _BuildAutomaton_11()




CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'allergysubstance'), pyxb.binding.datatypes.string, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 335, 40)))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'allergytypecode'), pyxb.binding.datatypes.string, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 336, 40)))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'allergyreaction'), pyxb.binding.datatypes.string, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 337, 40)))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'allergyconfidencelevel'), pyxb.binding.datatypes.string, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 338, 40)))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'allergyinfosource'), pyxb.binding.datatypes.string, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 339, 40)))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'allergystatus'), pyxb.binding.datatypes.string, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 340, 40)))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'allergydescription'), pyxb.binding.datatypes.string, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 341, 40)))

CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'allergyrecordeddate'), pyxb.binding.datatypes.date, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 342, 40)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, 'allergysubstance')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 335, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, 'allergytypecode')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 336, 40))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, 'allergyreaction')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 337, 40))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, 'allergyconfidencelevel')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 338, 40))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, 'allergyinfosource')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 339, 40))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, 'allergystatus')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 340, 40))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, 'allergydescription')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 341, 40))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(None, 'allergyrecordeddate')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 342, 40))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_12._Automaton = _BuildAutomaton_12()




letterdetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'letter'), letter, scope=letterdetails, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 355, 12)))

def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(letterdetails._UseForTag(pyxb.namespace.ExpandedName(None, 'letter')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 355, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
letterdetails._Automaton = _BuildAutomaton_13()




letter._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'letterdate'), pyxb.binding.datatypes.dateTime, scope=letter, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 362, 12)))

letter._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'lettertitle'), pyxb.binding.datatypes.string, scope=letter, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 363, 12)))

letter._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'letterfilename'), pyxb.binding.datatypes.string, scope=letter, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 364, 12)))

letter._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'letterfiletype'), pyxb.binding.datatypes.string, scope=letter, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 365, 12)))

letter._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'lettertype'), STD_ANON_32, scope=letter, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 366, 12)))

letter._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'lettercontent'), pyxb.binding.datatypes.string, scope=letter, documentation='\n                        Letter content should be sent as a CDATA section to avoid parsing errors. E.g. and end with the string \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t', location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 373, 12)))

letter._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'letterfilebody'), pyxb.binding.datatypes.base64Binary, scope=letter, documentation='\n                        This property is used when the Note is binary data, e.g DOC, PDF, JPG\n                    ', location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 379, 12)))

def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 363, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 364, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 365, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 373, 12))
    counters.add(cc_3)
    cc_4 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 379, 12))
    counters.add(cc_4)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(letter._UseForTag(pyxb.namespace.ExpandedName(None, 'letterdate')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 362, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(letter._UseForTag(pyxb.namespace.ExpandedName(None, 'lettertitle')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 363, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(letter._UseForTag(pyxb.namespace.ExpandedName(None, 'letterfilename')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 364, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(letter._UseForTag(pyxb.namespace.ExpandedName(None, 'letterfiletype')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 365, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(letter._UseForTag(pyxb.namespace.ExpandedName(None, 'lettertype')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 366, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(letter._UseForTag(pyxb.namespace.ExpandedName(None, 'lettercontent')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 373, 12))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_4, False))
    symbol = pyxb.binding.content.ElementUse(letter._UseForTag(pyxb.namespace.ExpandedName(None, 'letterfilebody')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 379, 12))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_4, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
letter._Automaton = _BuildAutomaton_14()




drugdetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'drug'), drug, scope=drugdetails, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 391, 12)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(drugdetails._UseForTag(pyxb.namespace.ExpandedName(None, 'drug')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 391, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
drugdetails._Automaton = _BuildAutomaton_15()




drug._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'drugstartdate'), pyxb.binding.datatypes.date, scope=drug, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 397, 12)))

drug._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'drugname'), STD_ANON_33, scope=drug, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 398, 12)))

drug._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'drugdose'), STD_ANON_34, scope=drug, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 405, 12)))

drug._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'code'), CTD_ANON_13, scope=drug, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 412, 12)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 405, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 412, 12))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(drug._UseForTag(pyxb.namespace.ExpandedName(None, 'drugstartdate')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 397, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(drug._UseForTag(pyxb.namespace.ExpandedName(None, 'drugname')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 398, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(drug._UseForTag(pyxb.namespace.ExpandedName(None, 'drugdose')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 405, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(drug._UseForTag(pyxb.namespace.ExpandedName(None, 'code')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 412, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
drug._Automaton = _BuildAutomaton_16()




CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'codetype'), pyxb.binding.datatypes.string, scope=CTD_ANON_13, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 415, 24)))

CTD_ANON_13._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'codevalue'), pyxb.binding.datatypes.string, scope=CTD_ANON_13, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 416, 24)))

def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 415, 24))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 416, 24))
    counters.add(cc_1)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, 'codetype')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 415, 24))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_13._UseForTag(pyxb.namespace.ExpandedName(None, 'codevalue')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 416, 24))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_13._Automaton = _BuildAutomaton_17()




testdetails._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'test'), test, scope=testdetails, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 425, 12)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(testdetails._UseForTag(pyxb.namespace.ExpandedName(None, 'test')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 425, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
         ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
testdetails._Automaton = _BuildAutomaton_18()




test._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'testname'), STD_ANON_35, scope=test, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 431, 12)))

test._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'testcode'), pyxb.binding.datatypes.string, scope=test, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 438, 12)))

test._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'units'), STD_ANON_36, scope=test, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 439, 12)))

test._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'daterange'), CTD_ANON_14, scope=test, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 446, 12)))

test._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'result'), result, scope=test, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 452, 12)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 439, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 452, 12))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(test._UseForTag(pyxb.namespace.ExpandedName(None, 'testname')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 431, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(test._UseForTag(pyxb.namespace.ExpandedName(None, 'testcode')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 438, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(test._UseForTag(pyxb.namespace.ExpandedName(None, 'units')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 439, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(test._UseForTag(pyxb.namespace.ExpandedName(None, 'daterange')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 446, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(test._UseForTag(pyxb.namespace.ExpandedName(None, 'result')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 452, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
test._Automaton = _BuildAutomaton_19()




result._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'datestamp'), pyxb.binding.datatypes.dateTime, scope=result, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 458, 12)))

result._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'prepost'), prepost, scope=result, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 459, 12)))

result._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'value'), STD_ANON_37, scope=result, location=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 460, 12)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 459, 12))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(result._UseForTag(pyxb.namespace.ExpandedName(None, 'datestamp')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 458, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(result._UseForTag(pyxb.namespace.ExpandedName(None, 'prepost')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 459, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(result._UseForTag(pyxb.namespace.ExpandedName(None, 'value')), pyxb.utils.utility.Location('file://///home/runner/work/resources/resources/schema/pv2/PV_2_0.xsd', 460, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
result._Automaton = _BuildAutomaton_20()

