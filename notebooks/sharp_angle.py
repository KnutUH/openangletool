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
class SharpeningAngle:
    """Documentation for SharpeningAngle"""

    def __init__(self, sharpening_setup):
        self.radius_wheel = 0.5 * sharpening_setup["Wheel diameter"]
        self.jig_to_outside_support = sharpening_setup["Jig length"]
        self.thickness_jig = sharpening_setup["Jig thickness"]
        self.apex_offset = sharpening_setup["Apex offset"]
        self.radius_support = 0.5 * sharpening_setup["Support diameter"]

        self.center_support_to_jig_reference = (
            self.radius_support + 0.5 * self.thickness_jig + self.apex_offset
        )
        self.apex_to_jig_reference = self.jig_to_outside_support - self.radius_support
        self.correction_angle = np.arctan(
            self.center_support_to_jig_reference / self.apex_to_jig_reference
        )

        self.apex_to_center_support = np.sqrt(
            self.center_support_to_jig_reference**2 + self.apex_to_jig_reference**2
        )

    def distance_center_axel_to_center_support(self, angle_degree):
        corrected_angle = np.radians(angle_degree) + 0.5 * np.pi - self.correction_angle
        return np.sqrt(
            self.apex_to_center_support**2
            + self.radius_wheel**2
            - 2
            * self.apex_to_center_support
            * self.radius_wheel
            * np.cos(corrected_angle)
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

    def sharpening_angle_degrees(self, distance):
        corrected_angle = np.acos(
            (distance**2 + self.apex_to_center_support**2 + self.radius_wheel**2)
            / (2 * self.apex_to_center_support * self.radius_wheel)
        )
        return np.degrees(corrected_angle + self.correction_angle)


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
