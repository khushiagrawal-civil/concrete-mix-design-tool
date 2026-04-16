from constants import *

class MixDesign:

    def __init__(self, inputs):
        self.i = inputs

    # VALIDATION 
    def validate_grade(self):
        input_grade = int(self.i.grade[1:])
        min_required = MIN_GRADE[self.i.exposure]

        if input_grade < min_required:
            raise ValueError(
                f"Grade {self.i.grade} not allowed for {self.i.exposure}. "
                f"Minimum required: M{min_required}"
            )

    # TARGET STRENGTH 
    def target_strength(self):
        fck = int(self.i.grade[1:])
        S = STD_DEV[self.i.grade]
        X = X_VALUES[self.i.grade]

        return max(fck + 1.65 * S, fck + X)

    # WATER-CEMENT RATIO 
    def water_cement_ratio(self, f_target):
        if f_target <= 25:
            wc = 0.55
        elif f_target <= 30:
            wc = 0.50
        elif f_target <= 35:
            wc = 0.45
        elif f_target <= 40:
            wc = 0.42
        elif f_target <= 45:
            wc = 0.40
        else:
            wc = 0.38

        durability_limit = DURABILITY[self.i.exposure]["max_wc"]
        return min(wc, durability_limit)

    # WATER CONTENT 
    def water_content(self):
        base_water = WATER_CONTENT[self.i.aggregate_size]

        # Slump adjustment
        slump_diff = self.i.slump - 50
        adjustment = (slump_diff / 25) * 0.03 * base_water

        water = base_water + adjustment

        # Aggregate type correction
        if self.i.aggregate_type == "sub-angular":
            water -= 10
        elif self.i.aggregate_type == "rounded":
            water -= 20

        return water

    # CEMENT CONTENT 
    def cement_content(self, water, wc):
        cement = water / wc
        min_cement = DURABILITY[self.i.exposure]["min_cement"]

        cement = max(cement, min_cement)

        # 🔥 WARNING instead of hard cap
        if cement > MAX_CEMENT:
            print("Warning: Cement content exceeded 450 kg/m³")

        return cement

    # AGGREGATE FRACTION 
    def coarse_aggregate_fraction(self):
        return CA_VOLUME[self.i.aggregate_size][self.i.sand_zone]

    # ABSOLUTE VOLUME 
    def absolute_volume(self, cement, water, ca_ratio):
        air = AIR_CONTENT[self.i.aggregate_size]

        V_cement = cement / (self.i.sg_cement * 1000)
        V_water = water / 1000
        V_air = air

        V_agg = 1 - (V_cement + V_water + V_air)

        V_ca = V_agg * ca_ratio
        V_fa = V_agg - V_ca

        mass_ca = V_ca * self.i.sg_ca * 1000
        mass_fa = V_fa * self.i.sg_fa * 1000

        return mass_ca, mass_fa

    # TRIAL MIXES 
    def trial_mixes(self, base_wc, water):
        variations = [base_wc, base_wc * 0.9, base_wc * 1.1]
        mixes = []

        for wc in variations:
            cement = self.cement_content(water, wc)
            ca_ratio = self.coarse_aggregate_fraction()
            ca, fa = self.absolute_volume(cement, water, ca_ratio)

            mixes.append({
                "w/c": round(wc, 3),
                "cement": round(cement, 2),
                "coarse_agg": round(ca, 2),
                "fine_agg": round(fa, 2)
            })

        return mixes

    # MAIN FUNCTION 
    def generate_mix(self, print_steps=True):
        self.validate_grade()

        f_target = self.target_strength()
        wc = self.water_cement_ratio(f_target)
        water = self.water_content()
        cement = self.cement_content(water, wc)
        ca_ratio = self.coarse_aggregate_fraction()
        ca, fa = self.absolute_volume(cement, water, ca_ratio)

        trials = self.trial_mixes(wc, water)

        if print_steps:
            print("\n--- FINAL MIX ---")
            print(f"Target strength: {f_target:.2f} MPa")
            print(f"W/C ratio: {wc}")
            print(f"Water: {water:.2f} kg/m³")
            print(f"Cement: {cement:.2f} kg/m³")
            print(f"Coarse Aggregate: {ca:.2f} kg/m³")
            print(f"Fine Aggregate: {fa:.2f} kg/m³")

            print("\n--- TRIAL MIXES ---")
            for i, mix in enumerate(trials):
                print(f"\nTrial {i+1}:")
                for k, v in mix.items():
                    print(f"{k}: {v}")

        return {
            "final_mix": {
                "target_strength": f_target,
                "w/c": wc,
                "water": water,
                "cement": cement,
                "coarse_agg": ca,
                "fine_agg": fa
            },
            "trials": trials
        }
    
   