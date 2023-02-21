# %%
import numpy as np


# %%
class AngleCalculator:
    """Calculations usefull for grinding."""

    def __init__(
        self, wheel_diameter, support_diameter, jig_lenght, jig_thickness, apex_offset=0
    ):
        """Initialize the AngleCalculator instance.

        Parameters
        ----------
        wheel_diameter:  The diameter of the grinding wheel
        support_diameter:  The diameter
        jig_lenght: The le
        jig_thickness:
        apex_offset: int, optional, default is 0

        Examples
        --------
        >>> import numpy as np
        >>> wheel = 250
        >>> support = 12
        >>> calc = AngleCalculator(wheel_diameter=wheel, support_diameter=support,
        ...                        jig_length=139, jig_thickness=12)
        >>> g_angle = 15
        >>> h_r = calc.distance_center_axel_to_center_support(g_angle) - 0.5*wheel + 0.5*support
        >>> h_offset = 50
        >>> v_offset = 29
        >>> h_n = calc.vertical_distance_center_axel_to_center_support(g_angle, h_offset) - v_offset
        >>> print(f'h_r: {h_r: .1f}')
        h_r:  78.9
        >>> print(f'h_n: {h_n: .1f}')
        h_n:  168.5

        Returns
        -------
        None.
        """
        self.radius_wheel = 0.5 * wheel_diameter
        self.radius_support = 0.5 * support_diameter
        self.apex_to_jig_reference = jig_lenght - self.radius_support
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

        The Law of cosines (https://en.wikipedia.org/wiki/Law_of_cosines) is used.
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
        corrected_angle = np.arccos(
            (
                -(distance**2)
                + self.apex_to_center_support**2
                + self.radius_wheel**2
            )
            / (2 * self.apex_to_center_support * self.radius_wheel)
        )
        return np.degrees(corrected_angle + self.correction_angle - 0.5 * np.pi)

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

    def vertical_distance_refpoint_to_outside_support(
        self, angle_degree, vertical_refpoint, horisontal_offset_support
    ):
        return (
            self.vertical_distance_center_axel_to_center_support(
                angle_degree, horisontal_offset_support
            )
            - vertical_refpoint
            + self.radius_support
        )

    def horizontal_distance_center_axel_to_center_support(
        self, angle_degree, vertical_offset_support
    ):
        return np.sqrt(
            self.distance_center_axel_to_center_support(angle_degree) ** 2
            - vertical_offset_support**2
        )

    def min_distance_limit(self):
        return self.distance_center_axel_to_center_support(0)

    def max_distance(self):
        return self.distance_center_axel_to_center_support(90)


# %%
calc = AngleCalculator(250, 12, 139, 12)
min_d = calc.min_distance_limit()
min_d

# %%
d = calc.distance_center_axel_to_center_support(0)
d

# %%
h_r = calc.distance_center_axel_to_center_support(15) - 0.5*250 + 0.5*12
print(f'h_r: {h_r: .1f}')

# %%
h_r = calc.distance_outside_support_to_wheel(15)
print(f"h_r: {h_r: .1f}")

# %%
vertical_distance_top_of_machine_to_center_axel = 29  # T8
horizontal_offset_support = 50  # T8
h_n = (
    calc.vertical_distance_center_axel_to_center_support(15, horizontal_offset_support)
    - vertical_distance_top_of_machine_to_center_axel
    + 6
)
print(f"h_n: {h_n: .1f}")

# %%
max_d = calc.max_distance()
max_d

# %%
calc.sharpening_angle_degrees_from_radial_distance(d)

# %%
calc.sharpening_angle_degrees_from_radial_distance(min_d)

# %%
calc.sharpening_angle_degrees_from_radial_distance(max_d)

# %%
angles = np.linspace(5, 30)
h_rs = calc.distance_outside_support_to_wheel(angles)
h_rs

# %%
import matplotlib.pyplot as plt


# %%
plt.scatter(angles, s_dist)

# %%
