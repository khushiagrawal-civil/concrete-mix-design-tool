class MixInputs:
    def __init__(
        self,
        grade="M25",
        exposure="moderate",
        aggregate_size=20,
        slump=75,
        sand_zone="Zone II",
        aggregate_type="angular",  # angular / sub-angular / rounded
        specific_gravity_cement=3.15,
        specific_gravity_fa=2.65,
        specific_gravity_ca=2.7
    ):
        self.grade = grade
        self.exposure = exposure
        self.aggregate_size = aggregate_size
        self.slump = slump
        self.sand_zone = sand_zone
        self.aggregate_type = aggregate_type
        self.sg_cement = specific_gravity_cement
        self.sg_fa = specific_gravity_fa
        self.sg_ca = specific_gravity_ca