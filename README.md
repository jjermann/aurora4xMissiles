# aurora4xMissiles
AuroraC# missile optimizer

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
  techContext.damagePerMsp = 6
  techContext.agilityPerMsp = 48
  techContext.setEPPerMsp(0.32)
  techContext.fuelConsumption = 0.3
  techContext.minPowerFactor = 0.25
  techContext.maxPowerFactor = 3

  calcContext = CalculationContext()
  calcContext.intendedTargetSpeed = 5000
  calcContext.size = 12
  calcContext.minExcessSize = 1.0
  calcContext.minDamage = 23
  calcContext.maxDamage = 27
  calcContext.minSpeed = 10000
  calcContext.maxSpeed = 20000
  calcContext.minRange = 100000000
  calcContext.minCth = 30

  missileOpt = MissileOptimization(auroraData, techContext, calcContext)
  return missileOpt

example = getExampleOptimizer()
topMissiles = example.printTopMissiles()
print(topMissiles)
```

gives:

```
246 candidates:

Size = 12.0: WH MSP = 4.1667, Fuel MSP = 0.908, Agility MSP = 1.1253, Excess MSP = 1.0, Engine Power Modifier = 395%, Engine Size MSP = 4.8
Damage = 25, EP = 6.07, Speed = 10116.66667 km/s, Range = 100.06474m km, MR = 15, Cth = 50.58333% / 30.35% / 15.175%

Size = 12.0: WH MSP = 4.1667, Fuel MSP = 1.108, Agility MSP = 1.1253, Excess MSP = 1.0, Engine Power Modifier = 410%, Engine Size MSP = 4.6
Damage = 25, EP = 6.04, Speed = 10066.66667 km/s, Range = 100.06993m km, MR = 15, Cth = 50.33333% / 30.2% / 15.1%

Size = 12.0: WH MSP = 4.1667, Fuel MSP = 0.808, Agility MSP = 1.1253, Excess MSP = 1.0, Engine Power Modifier = 385%, Engine Size MSP = 4.9
Damage = 25, EP = 6.04, Speed = 10066.66667 km/s, Range = 101.9187m km, MR = 15, Cth = 50.33333% / 30.2% / 15.1%

Size = 12.0: WH MSP = 4.1667, Fuel MSP = 1.008, Agility MSP = 1.1253, Excess MSP = 1.0, Engine Power Modifier = 400%, Engine Size MSP = 4.7
Damage = 25, EP = 6.02, Speed = 10033.33333 km/s, Range = 103.47554m km, MR = 15, Cth = 50.16667% / 30.1% / 15.05%

Size = 12.0: WH MSP = 4.1667, Fuel MSP = 0.708, Agility MSP = 1.1253, Excess MSP = 1.0, Engine Power Modifier = 375%, Engine Size MSP = 5.0
Damage = 25, EP = 6.0, Speed = 10000.0 km/s, Range = 102.7697m km, MR = 15, Cth = 50.0% / 30.0% / 15.0%
```

The final candidates can be sorted according to any missile criteria
(default is damage but chance to hit would work as well)...
