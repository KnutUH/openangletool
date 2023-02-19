# %%
import numpy as np


sharpening_setup = {
    "Wheel diameter": 250,
    "Jig thickness": 12,
    "Jig length": 139,
    "Apex offset": 0,
    "Support diameter": 12,
}


# %%
class AngleCalculator:
    """
    Implementation of calculations usefull for grinding
    
    """
    def __init__(
        """
        
        """
        self, wheel_diameter, support_diameter, jig_lenght, jig_thickness, apex_offset=0
    ):
        self.radius_wheel = 0.5 * wheel_diameter
        self.radius_support = 0.5 * support_diameter
        self.apex_to_jig_reference = jig_length - self.radius_support
        self.thickness_jig = jig_thickness
        self.apex_offset = apex_offset

        self.center_support_to_jig_reference = (
            self.radius_support + 0.5 * self.thickness_jig + self.apex_offset
        )

        # the correction angle due to thickness of jig and apex offset
        self.correction_angle = np.arctan(
            self.center_support_to_jig_reference / self.apex_to_jig_reference
        )

        # pythagoras to calculate
        self.apex_to_center_support = np.sqrt(
            self.center_support_to_jig_reference**2 + self.apex_to_jig_reference**2
        )

    def distance_center_axel_to_center_support(self, angle_degree):
        """
        For given grinding angle in degrees return the distance from the 
        center of the axel of the grinding wheel to the center of the support.
        
        The Law of cosines (https://en.wikipedia.org/wiki/Law_of_cosines)is used.
        The vertices of triangle considered are,
        
          A: center of axel
          B: apex of the blade
          C: center of the support
          
        To find the length of BC and angle between AB and BC consider the triangle
        BCD where the vertices are,
        
          B and C as above
          D: jig reference point
          
        The length of BD is the jig_length minus the radius of the support, the 
        length of CD is the radius of the support plus half the thickness of the 
        jig plus any apex offset. The angle between BC and CD is 90 degrees and 
        the lenght of BC can be found by the Pytagorean theorem. This angle,
        between BD and BC (correction angle) can be found by the inverse tangence 
        of CD/BD.
        
        The grinding angle is the angle between a tangent to the grinding wheel
        in apex point (B) which is 90 degrees to AB hence the angle between AB and
        BC is 90 degrees + the grinding angle minus the correction angle.
        
        """
        corrected_angle = np.radians(angle_degree) + 0.5 * np.pi - self.correction_angle
        return np.sqrt(
            self.apex_to_center_support**2
            + self.radius_wheel**2
            - 2
            * self.apex_to_center_support
            * self.radius_wheel
            * np.cos(corrected_angle)
        )
    
    def sharpening_angle_degrees_from_radial_distance(self, distance):
        """
        For given distance from center of axel to center of support return 
        the grinding angle in degrees.
        
        see documentation of the function distance_center_axel_to_center_support()
        """
        corrected_angle = np.acos(
            (distance**2 + self.apex_to_center_support**2 + self.radius_wheel**2)
            / (2 * self.apex_to_center_support * self.radius_wheel)
        )
        return np.degrees(corrected_angle + self.correction_angle)
    
    def sharpening_angle_degrees(self, horisontal, vertical):
        return self.sharpening_angle_degrees_from_radial_distance(
            np.sqrt(horisontal**2 + vertical**2)
        )

    def distance_outside_support_to_wheel(self, angle_degree):
        return (
            self.distance_center_axel_to_center_support(angle_degree)
            - self.radius_wheel
            + self.radius_support
        )

    def vertical_distance_center_axel_to_center_support(
        self, angle_degree, horisontal_offset_support
    ):
        return np.sqrt(
            self.distance_center_axel_to_center_support(angle_degree) ** 2
            - horisontal_offset_support**2
        )

    def horizontal_distance_center_axel_to_center_support(
        self, angle_degree, vertical_offset_support
    ):
        return np.sqrt(
            self.distance_center_axel_to_center_support(angle_degree) ** 2
            - vertical_offset_support**2
        )



# %%
sa = SharpeningAngle(sharpening_setup)

# %%
print(vars(sa))
print(
    "hei",
)

# %%
h_r = sa.distance_outside_support_to_wheel(15)
print(f"h_r: {h_r: .1f}")

vertical_distance_top_of_machine_to_center_axel = 29  # T8
horizontal_offset_support = 50  # T8
h_n = (
    sa.vertical_distance_center_axel_to_center_support(15, horizontal_offset_support)
    - vertical_distance_top_of_machine_to_center_axel
    + sa.radius_support
)
print(f"h_n: {h_n: .1f}")

# %%

# %%
angles = np.linspace(10, 20)
angles

# %%
s_dist = sa.distance_outside_support_to_wheel(angles)
s_dist

# %%
import matplotlib.pyplot as plt


# %%
plt.scatter(angles, s_dist)

# %%
