import h_transport_materials as htm
from h_transport_materials import Diffusivity, Solubility, Permeability

VANADIUM_MOLAR_VOLUME = 8.34e-6  # m3/mol  https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/vanadium

u = htm.ureg

volk_diffusivity = Diffusivity(
    D_0=2.9e-8 * u.m**2 * u.s**-1,
    E_D=4.2 * u.kJ * u.mol**-1,
    isotope="H",
    source="volkl_5_1975",
    range=(173 * u.K, 573 * u.K),
)

veleckis_solubility = Solubility(
    isotope="H",
    range=(519 * u.K, 827 * u.K),
    S_0=1.38e-1 * u.mol * u.m**-3 * u.Pa**-0.5,
    E_S=-29.0 * u.kJ * u.mol**-1,
    source="veleckis_thermodynamic_1969",
)

qi_diffusivity = Diffusivity(
    D_0=5.6e-8 * u.m**2 * u.s**-1,
    E_D=9.1 * u.kJ * u.mol**-1,
    range=(
        u.Quantity(-150, u.degC),
        u.Quantity(200, u.degC),
    ),
    source="qi_tritium_1983",
    isotope="H",
)  # TODO get data from experimental points, see issue #64

malo_permeability = Permeability(
    pre_exp=1.27e-04 * u.mol * u.m**-1 * u.s**-1 * u.Pa**-0.5,
    act_energy=8667 * u.K * htm.k_B,
    source="malo_experimental_2022",
    range=(
        u.Quantity(250, u.degC),
        u.Quantity(550, u.degC),
    ),
    isotope="D",
)

properties = [
    volk_diffusivity,
    veleckis_solubility,
    qi_diffusivity,
    malo_permeability,
]

for prop in properties:
    prop.material = htm.VANADIUM

htm.database += properties
