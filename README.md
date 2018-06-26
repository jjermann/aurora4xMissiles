# aurora4xMissiles
Aurora4x missile optimizer

Currently it's not perfect yet:
it's quite slow unless you reduce the number of choices by specifying boundaries
for damage and/or speed, also the results are not entirely correct
(probably some slightly wrong rounding math regarding MR/fuel/speed).
Please help in case you know how to fix it...

Nevertheless I find it quite usefull...

To run it online e.g. copy paste the content of aurora4xMissiles.py in
repl.it (for Python3) and modify the content to your situation...

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
50 candidates:

Size = 12.0: WH = 4.05, Fuel = 1.63, Agility = 0.79, Engine = 4.53, Excess = 1.0
  Speed = 50019 km/s, Damage = 81, Range = 2002 mkm, MR = 20, Cth = 333.46% / 200.07% / 100.04%
  missile engine: EP = 30.0113, MSP = 4.53, multiplier = 2.65, Fuel/EPH = 12.23, Fuel/Hour = 367.01

Size = 12.0: WH = 4.05, Fuel = 1.54, Agility = 0.79, Engine = 4.62, Excess = 1.0
  Speed = 50050 km/s, Damage = 81, Range = 2011 mkm, MR = 20, Cth = 333.67% / 200.2% / 100.1%
  missile engine: EP = 30.03, MSP = 4.62, multiplier = 2.6, Fuel/EPH = 11.5, Fuel/Hour = 345.49

Size = 12.0: WH = 4.05, Fuel = 1.53, Agility = 0.79, Engine = 4.63, Excess = 1.0
  Speed = 50158 km/s, Damage = 81, Range = 2001 mkm, MR = 20, Cth = 334.39% / 200.63% / 100.32%
  missile engine: EP = 30.095, MSP = 4.63, multiplier = 2.6, Fuel/EPH = 11.49, Fuel/Hour = 345.73

Size = 12.0: WH = 4.05, Fuel = 1.45, Agility = 0.79, Engine = 4.71, Excess = 1.0
  Speed = 50044 km/s, Damage = 81, Range = 2014 mkm, MR = 20, Cth = 333.62% / 200.18% / 100.09%
  missile engine: EP = 30.0262, MSP = 4.71, multiplier = 2.55, Fuel/EPH = 10.82, Fuel/Hour = 324.77

Size = 12.0: WH = 4.05, Fuel = 1.44, Agility = 0.79, Engine = 4.72, Excess = 1.0
  Speed = 50150 km/s, Damage = 81, Range = 2003 mkm, MR = 20, Cth = 334.33% / 200.6% / 100.3%
  missile engine: EP = 30.09, MSP = 4.72, multiplier = 2.55, Fuel/EPH = 10.8, Fuel/Hour = 324.99
```

The final candidates can be sorted according to any missile criteria
(default is damage but chance to hit would work as well)...
