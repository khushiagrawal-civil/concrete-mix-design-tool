from inputs import MixInputs
from mix_design import MixDesign

inputs = MixInputs(
    grade="M25",
    exposure="moderate",
    aggregate_size=20,
    slump=75,
    sand_zone="Zone II",
    aggregate_type="angular"
)

mix = MixDesign(inputs)
mix.generate_mix()