# aurora4xMissiles
Aurora4x missile optimizer

The optimizer will try to find all possible missile designs satisfying the
given restrictions. It is quite slow unless the number of choices is reduced
enough by specifying enough boundary conditions (e.g. damage, speed, cth).

To run it online e.g. copy paste the content of aurora4xMissiles.py in
repl.it (for Python3) and modify the content to your situation...

The main optimizer class is `MissileOptimization`. It requires `AuroraData`
(basic game data), `TechnologyContext` (research level relevant for missiles)
and `CalculationContext` (boundary conditions). The top 5 optimized results 
then be fetched with the command `missileOptimization.printTopMissiles()`.
Optionally a sorting parameter can be specified (by default it's damage then cth).

For more details please see the source code...

Example:

```python
def getExampleOptimizer():
  auroraData = AuroraData()
  techContext = TechnologyContext()
  techContext.damagePerMsp = 20
  techContext.agilityPerMsp = 160
  techContext.EPPerHs = 50
  techContext.fuelConsumption = 0.2
  techContext.MinPowerFactor = 0.1
  techContext.MaxPowerFactor = 6

  calcContext = CalculationContext()
  calcContext.size = 12
  calcContext.minExcessSize = 1.0
  calcContext.minDamage = 80
  calcContext.maxDamage = 81
  calcContext.minSpeed = 50000
  calcContext.maxSpeed = 1000000
  calcContext.minRange = 2000000000
  calcContext.minCth = 100

  missileOpt = MissileOptimization(auroraData, techContext, calcContext)
  return missileOpt


example = getExampleOptimizer()
topMissiles = example.printTopMissiles()
print(topMissiles)
```

gives:

```
246 candidates:

Size = 12.0: WH = 4.05, Fuel = 1.5324, Agility = 0.7876, Engine = 4.63, Excess = 1.0
  Speed = 50200 km/s (50158.33333 km/s), Damage = 81, Range = 2001 mkm, Fuel = 3831.0, MR = 21, Cth = 351.10833% / 210.665% / 105.3325%
  missile engine: EP = 30.095, MSP = 4.63, multiplier = 2.6, Fuel/EPH = 11.48783, Fuel/Hour = 345.7263

Size = 12.0: WH = 4.05, Fuel = 1.4424, Agility = 0.7876, Engine = 4.72, Excess = 1.0
  Speed = 50200 km/s (50150.0 km/s), Damage = 81, Range = 2003 mkm, Fuel = 3606.0, MR = 21, Cth = 351.05% / 210.63% / 105.315%
  missile engine: EP = 30.09, MSP = 4.72, multiplier = 2.55, Fuel/EPH = 10.80052, Fuel/Hour = 324.98758

Size = 12.0: WH = 4.05, Fuel = 1.5424, Agility = 0.7876, Engine = 4.62, Excess = 1.0
  Speed = 50000 km/s (50050.0 km/s), Damage = 81, Range = 2011 mkm, Fuel = 3856.0, MR = 21, Cth = 350.35% / 210.21% / 105.105%
  missile engine: EP = 30.03, MSP = 4.62, multiplier = 2.6, Fuel/EPH = 11.50481, Fuel/Hour = 345.48941

Size = 12.0: WH = 4.05, Fuel = 1.4524, Agility = 0.7876, Engine = 4.71, Excess = 1.0
  Speed = 50000 km/s (50043.75 km/s), Damage = 81, Range = 2014 mkm, Fuel = 3631.0, MR = 21, Cth = 350.30625% / 210.18375% / 105.09187%
  missile engine: EP = 30.02625, MSP = 4.71, multiplier = 2.55, Fuel/EPH = 10.81617, Fuel/Hour = 324.76916

Size = 12.0: WH = 4.05, Fuel = 1.6324, Agility = 0.7876, Engine = 4.53, Excess = 1.0
  Speed = 50000 km/s (50018.75 km/s), Damage = 81, Range = 2002 mkm, Fuel = 4081.0, MR = 21, Cth = 350.13125% / 210.07875% / 105.03938%
  missile engine: EP = 30.01125, MSP = 4.53, multiplier = 2.65, Fuel/EPH = 12.22915, Fuel/Hour = 367.01195
```

The final candidates can be sorted according to any missile criteria
(default is damage but chance to hit would work as well)...
