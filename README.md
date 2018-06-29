# aurora4xMissiles
Aurora4x missile optimizer

The optimizer is quite slow unless the number of choices are reduced by specifying
boundaries for e.g. damage and/or speed.

Also the results are not always correct/optimal
(due to rounding issues): The internal calculation uses values which it assumes to be optimal
(e.g. an agility value just high enough for the MR. Because of rounding
issues the final result could be just _below_ that value though.
Please help in case you know an easy way to fix/improve this...

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

Size = 12.0: WH = 4.05, Fuel = 1.6325, Agility = 0.7875, Engine = 4.53, Excess = 1.0
  Speed = 50019 km/s, Damage = 81, Range = 2002 mkm, MR = 20, Cth = 333.4583% / 200.075% / 100.0375%
  missile engine: EP = 30.0113, MSP = 4.53, multiplier = 2.65, Fuel/EPH = 12.2291, Fuel/Hour = 367.012

Size = 12.0: WH = 4.05, Fuel = 1.5425, Agility = 0.7875, Engine = 4.62, Excess = 1.0
  Speed = 50050 km/s, Damage = 81, Range = 2011 mkm, MR = 20, Cth = 333.6667% / 200.2% / 100.1%
  missile engine: EP = 30.03, MSP = 4.62, multiplier = 2.6, Fuel/EPH = 11.5048, Fuel/Hour = 345.4894

Size = 12.0: WH = 4.05, Fuel = 1.5325, Agility = 0.7875, Engine = 4.63, Excess = 1.0
  Speed = 50158 km/s, Damage = 81, Range = 2001 mkm, MR = 20, Cth = 334.3889% / 200.6333% / 100.3167%
  missile engine: EP = 30.095, MSP = 4.63, multiplier = 2.6, Fuel/EPH = 11.4878, Fuel/Hour = 345.7263

Size = 12.0: WH = 4.05, Fuel = 1.4525, Agility = 0.7875, Engine = 4.71, Excess = 1.0
  Speed = 50044 km/s, Damage = 81, Range = 2014 mkm, MR = 20, Cth = 333.625% / 200.175% / 100.0875%
  missile engine: EP = 30.0262, MSP = 4.71, multiplier = 2.55, Fuel/EPH = 10.8162, Fuel/Hour = 324.7692

Size = 12.0: WH = 4.05, Fuel = 1.4425, Agility = 0.7875, Engine = 4.72, Excess = 1.0
  Speed = 50150 km/s, Damage = 81, Range = 2003 mkm, MR = 20, Cth = 334.3333% / 200.6% / 100.3%
  missile engine: EP = 30.09, MSP = 4.72, multiplier = 2.55, Fuel/EPH = 10.8005, Fuel/Hour = 324.9876

```

The final candidates can be sorted according to any missile criteria
(default is damage but chance to hit would work as well)...
