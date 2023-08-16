# -*- coding: utf-8 -*-
import uuid
import math
from .feeds.util import cantilever_deflect_endload, cantilever_deflect_uniload
from .feeds import operation
from .shape import Shape
from .params import Param
from .toolmaterial import ToolMaterial, HSS, Carbide
from .toolpixmap import EndmillPixmap, \
                        BullnosePixmap, \
                        ChamferPixmap, \
                        VBitPixmap, \
                        DrillPixmap

class Tool(object):
    API_VERSION = 1

    def __init__(self, label, shape, id=None, filename=None):
        self.id = id or str(uuid.uuid1())
        self.label = label
        self.filename = filename # Keep in mind: Not every tool is file-based
        self.shape = Shape(shape) if isinstance(shape, str) else shape
        self.pixmap = None  # for caching a ToolPixmap

        # Used for internal attributes, but also by the serializer to
        # store attributes unknown to BTL. Maps name to value.
        self.attrs = {}

    def __str__(self):
        return '{} "{}" "{}"'.format(self.id, self.label, self.shape.name)

    def __eq__(self, other):
        if other is None:
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'filename': self.filename,
            'shape': self.shape.to_dict(),
            'attrs': self.attrs,
        }

    def set_attrib(self, name, value):
        self.attrs[name] = value

    def get_non_btl_attribs(self):
        return {k:v for k, v in self.attrs.items() if not k.startswith('btl-')}

    def get_attrib(self, name, default=None):
        return self.attrs.get(name, default)

    def get_attrib_as_param(self, name, default=None):
        value = self.attrs[name]
        return Param(name, v=value)

    def set_label(self, label):
        self.label = label

    def get_label(self):
        return self.label

    def set_stickout(self, stickout):
        self.set_attrib('btl-stickout', float(stickout))

    def get_stickout(self):
        stickout = self.get_attrib('btl-stickout')
        if stickout is not None:
            return float(stickout)
        ce = self.shape.get_cutting_edge()
        if ce is not None:
            return ce+3
        length = self.shape.get_length()
        return length/2 if length else None

    def set_notes(self, notes):
        self.attrs['btl-notes'] = notes

    def get_notes(self):
        return self.attrs.get('btl-notes', '')

    def set_coating(self, coating):
        self.attrs['btl-coating'] = coating

    def get_coating(self):
        return self.attrs.get('btl-coating', '')

    def set_hardness(self, hardness):
        self.attrs['btl-hardness'] = hardness

    def get_hardness(self):
        return self.attrs.get('btl-hardness', '')

    def set_material(self, tool_material):
        """
        Unfortunately some, but not all, of the FreeCAD default shapes
        have a Material property in shape file. This is bad because:

        - A shape is is a geometry, and a geometry does not have a material.
          So I think it isn't the right design.

        - If we try to store the material in the shape, and the shape file
          does not have this property, then the property is not saved.

        - If we try to store it in the tool instead, that property may exist
          twice; once in the tool, and again in the shape, which also
          results in the property being shown twice in the UI.

        To work around this, we:

        - Hide the material property of the shape in the UI main tab.

        - Show a static material property of the shape in the secondary
          tab.

        - Store the property in the shape, but only if it already has
          a shape property. Otherwise we store it in the tool.
        """
        assert issubclass(tool_material, ToolMaterial)
        if self.shape.get_material() is not None:
            self.shape.set_material(tool_material)
            return
        self.set_attrib('btl-material', tool_material.name)

    def get_material(self):
        material = self.shape.get_material()
        if material is not None:
            return material
        material = self.get_attrib('btl-material')
        if material.lower() == 'hss':
            return HSS
        elif material.lower() == 'carbide':
            return Carbide
        return None

    def supports_feeds_and_speeds(self):
        if not self.shape.is_builtin():
            return False
        return self.shape.name in ('endmill',
                                   'torus',
                                   'bullnose',
                                   'ballend',
                                   'chamfer',
                                   'vbit')

    def get_pixmap(self):
        if self.pixmap:
            return self.pixmap
        stickout = self.get_stickout()
        shank_d = self.shape.get_shank_diameter()
        diameter = self.shape.get_diameter()
        cutting_edge = self.shape.get_cutting_edge()
        if self.shape.name == 'endmill':
            self.pixmap = EndmillPixmap(stickout,
                                        shank_d,
                                        diameter,
                                        cutting_edge)
        elif self.shape.name in ('torus', 'bullnose', 'ballend'):
            corner_r = self.shape.get_corner_radius()
            self.pixmap = BullnosePixmap(stickout,
                                         shank_d,
                                         diameter,
                                         cutting_edge=cutting_edge,
                                         corner_radius=corner_r)
        elif self.shape.name == 'vbit':
            ce_angle = self.shape.get_cutting_edge_angle()
            tip_w = self.shape.get_tip_diameter()
            self.pixmap = VBitPixmap(stickout,
                                     shank_d,
                                     diameter,
                                     brim=cutting_edge,
                                     lead_angle=ce_angle/2,
                                     tip_w=tip_w)
        elif self.shape.name == 'chamfer':
            radius = self.shape.get_radius()
            self.pixmap = ChamferPixmap(stickout,
                                        shank_d,
                                        diameter,
                                        brim=cutting_edge,
                                        radius=radius)
        elif self.shape.name == 'drill':
            angle = self.shape.get_tip_angle()
            self.pixmap = DrillPixmap(stickout,
                                      diameter,
                                      angle=angle)
        return self.pixmap

    def set_materials(self, materials):
        self.attrs['btl-materials'] = materials

    def get_materials(self):
        return self.attrs.get('btl-materials', '')

    def set_supplier(self, supplier):
        self.attrs['btl-supplier'] = supplier

    def get_supplier(self):
        return self.attrs.get('btl-supplier', '')

    def serialize(self, serializer):
        return serializer.serialize_tool(self)

    @classmethod
    def deserialize(cls, serializer, id):
        return serializer.deserialize_tool(id)

    def to_string(self, indent=0, summarize=False):
        result = []
        indent = ' '*indent
        result.append('{}Tool "{}" ({}) (instance {})'.format(
            indent,
            self.label,
            self.id,
            id(self)
        ))

        shape = self.shape.get_label()
        shape_name = self.shape.name
        result.append(f'{indent}  Shape = {shape} ({shape_name})')

        shape_str = self.shape.to_string(indent=2, summarize=summarize)
        return '\n'.join(result) + '\n' + shape_str

    def dump(self, indent=0, summarize=False):
        print(self.to_string(indent, summarize))

    def get_chipload_for_material(self, thematerial):
        chipload = self.shape.get_chipload()
        if chipload:
            return chipload
        diameter = self.shape.get_diameter()
        tool_material = self.get_material()
        return diameter/thematerial.get_chipload_divisor(tool_material)

    def get_speed_for_material(self, thematerial, op=operation.Profiling):
        """
        Returns the min_speed and max_speed in m/min for milling, slotting, or
        drilling the given material.
        """
        op = operation.Profiling if op is operation.HSM else op
        tool_material = self.get_material()
        speeds = thematerial.get_speeds(tool_material)
        min_speed, max_speed = speeds.get(op, (None, None))
        if not min_speed or not max_speed:
            return None, None
        return min_speed, max_speed

    def get_inertia(self):
        """
        Returns a tuple (solid_inertia, fluted_inertia) (mm⁴)
        """
        # Estimated equivalent of the fluted portion = 80% of the fluted diameter
        # "Determination of the Equivalent Diameter of an End Mill Based on its
        # Compliance", L. Kops, D.T. Vo
        diameter = self.shape.get_diameter()
        fluted_inertia = (math.pi * ((diameter*0.8) / 2)**4) / 4

        # Moment of inertia equation for a SOLID round beam (shank partion of the end mill)
        # https://en.wikipedia.org/wiki/List_of_area_moments_of_inertia
        shank_d = self.shape.get_shank_diameter()
        if shank_d:
            solid_inertia = (math.pi/4) * (shank_d/2)**4
        else:
            solid_inertia = fluted_inertia

        return solid_inertia, fluted_inertia

    def get_deflection(self, doc, force):
        """
        Assuming a non-plunging/non-drilling operation, this function returns the
        deflection resulting from the engagement with the given force.

        Returns a single factor, the deflection.

        doc: mm
        force: N
        returns: mm
        """
        # "Metal Cutting Theory and Practice", By David A. Stephenson, John S. Agapiou, p362
        # "Structural modeling of end mills for form error and stability analysis", E.B. Kivanc, E. Budak
        stickout = self.get_stickout()
        cutting_edge = self.shape.get_cutting_edge() or stickout
        shank_l = stickout-cutting_edge  # Length of the shank portion
        non_cutting = cutting_edge-doc # Length of the non-cutting flute portion

        solid_inertia, fluted_inertia = self.get_inertia()

        # Point load at the end of the shank.
        tool_material = self.get_material()
        elasticity = tool_material.elasticity
        deflectionShank = cantilever_deflect_endload(force, shank_l, elasticity, solid_inertia)
        # Point load at the end of the fluted section that isn't currently cutting.
        deflectionNonCutting = cantilever_deflect_endload(force, non_cutting, elasticity, fluted_inertia)
        # Uniform load along fluted section in cut,
        deflectionCutting = cantilever_deflect_uniload(force, doc, elasticity, fluted_inertia)

        # NOTE: We ignore the contribution from the angle of deflection,
        # which should be negligible for cutting purposes.
        return deflectionShank+deflectionNonCutting+deflectionCutting

    def get_max_deflection(self, force):
        """
        Returns the theoretical maximum deflection, were all forces acting
        on the tip of the endmill.

        force: N
        returns: mm
        """
        stickout = self.get_stickout()
        tool_material = self.get_material()
        solid_inertia, fluted_inertia = self.get_inertia()
        return cantilever_deflect_endload(force,
                                          stickout,
                                          tool_material.elasticity,
                                          min(solid_inertia, fluted_inertia))

    def get_bend_limit(self, doc):
        """
        Returns the maximum force to permanently bend the end mill at the given depth of cut.
        Yield is the STRESS at which the material deforms permanently.

        stress = F * L * Radius / I
        F = (I * stress) / (r * l)
        Returns force in N
        """
        # TODO: Estimate Yield for the fluted portion of the end mill separately
        stickout = self.get_stickout()
        tool_material = self.get_material()
        cutting_edge = self.shape.get_cutting_edge() or stickout
        diameter = self.shape.get_diameter()
        shank_d = self.shape.get_shank_diameter() or diameter
        yield_strength = tool_material.yield_strength
        shank_l = max(0.000001, stickout-cutting_edge)
        non_cutting = max(0.000001, stickout-doc)
        solid_inertia, fluted_inertia = self.get_inertia()
        return min((yield_strength*solid_inertia) / ((shank_d/2)* shank_l),
                   (yield_strength*fluted_inertia) / ((diameter/2) * non_cutting))

    def get_twist_limit(self):
        """
        # Returns the maximum torque in Nm to shear the end mill
        # http://www.engineeringtoolbox.com/torsion-shafts-d_947.html
        """
        # TODO: Estimate Shear for the fluted portion of the end mill separately
        tool_material = self.get_material()
        diameter = self.shape.get_diameter()
        shank_d = self.shape.get_shank_diameter() or diameter
        shear_strength = tool_material.shear_strength
        solid_inertia, fluted_inertia = self.get_inertia()
        return min((shear_strength*solid_inertia) / (shank_d/2),
                   (shear_strength*fluted_inertia) / (diameter/2))

    def validate(self):
        stickout = self.get_stickout()
        cutting_edge = self.shape.get_cutting_edge() or stickout
        corner_r = self.shape.get_corner_radius()
        diameter = self.shape.get_diameter()
        ce_angle = self.shape.get_cutting_edge_angle()
        if cutting_edge > stickout:
            raise AttributeError(f"Flute length {cutting_edge} is larger than stickout {stickout}")
        if abs(corner_r or 0) > diameter/2:
            raise AttributeError(f"Corner radius {corner_r} is larger than tool radius {diameter/2}")
        if corner_r and ce_angle:
            raise AttributeError("Tool has radius and cutting edge angle; only one supported")
        if ce_angle and (ce_angle < 0 or ce_angle > 180):
            raise AttributeError("Cutting edge angle must be between 0 and 180 degrees")
