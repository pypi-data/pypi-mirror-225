class Equation:
    def __init__(self, Rstar=10, fp=0.5, ne=2, fe=1, fi=0.01, fc=0.01, L=10_000) -> None:
        """The Drake Equation, which was the agenda for a meeting of experts held in West Virginia in 1961, estimates N, the number of transmitting societies in the Milky Way galaxy.

        Args:
            Rstar (int, optional): The rate of formation of stars suitable for the development of intelligent life (number per year). Defaults to 10.
            fp (float, optional): The fraction of those stars with planetary systems. Defaults to 0.5.
            ne (int, optional): The number of planets, per solar system, with an environment suitable for life. Defaults to 2.
            fe (int, optional): The fraction of suitable planets on which life actually appears. Defaults to 1.
            fi (float, optional): The fraction of life bearing planets on which intelligent life emerges. Defaults to 0.01.
            fc (float, optional): The fraction of civilizations that develop a technology that produces detectable signs of their existence. Defaults to 0.01.
            L (_type_, optional): The average length of time such civilizations produce such signs (years). Defaults to 10_000.
        """
        self.no_tech_adv_civ = 0
        self.ro_star_formation = Rstar
        self.fo_stars_with_planet_systems = fp
        self.no_planets_suitable_life = ne
        self.no_planets_with_life = fe
        self.fo_planets_with_intel = fi
        self.fo_civs_with_detectable_tech = fc
        self.avg_life_of_detectable_civs = L

    def estimate(self) -> int:
        """Estimates the number of technologically advanced civilizations that have emerged over the history of the observable universe

        Returns:
            Decimal: the number of technologically advanced civilizations 
        """
        self.no_tech_adv_civ = self.ro_star_formation * self.fo_stars_with_planet_systems * self.no_planets_suitable_life * \
            self.no_planets_with_life * self.fo_planets_with_intel * \
            self.fo_civs_with_detectable_tech * self.avg_life_of_detectable_civs
        return int(self.no_tech_adv_civ)
