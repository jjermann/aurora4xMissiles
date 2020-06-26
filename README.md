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
The first line of each result summarizes the _input_ parameter in the missile designer.
The second line summarizes how the respective missile performs.
Optionally a third output line can be specified with the functional parameter `infoFn`.


## CalculationContext

* `intendedTargetSpeed`
That's the speed used for `minCth`. Remark: This value is of no relevance for the optimization, it's just the intended velocity for `minCth`.
* `minCth`
That's the minimal chance to hit for the given `intendedTargetSpeed`.
* `size`
That's the desired missile size.
* `minExcessSize`
If you want to reserve some space for additional gadgets to put in the missile (e.g. ECM or sensors) then you can reserve it with `minExcessSize`.
* `minDamage`
The minimal damage of the missile _(very relevant for optimizer performance)_.
* `maxDamage`
The maximal damage of the missile _(very relevant for optimizer performance)_.
* `minSpeed`
The minimal speed of the missile in km/s _(relevant for optimizer performance)_.
* `maxSpeed`
The maximal speed of the missile in km/s _(relevant for optimizer performance)_.
* `minRange`
The minimal range of the missile in km _(relevant for optimizer performance)_.
* `maxRange`
The maximal range of the missile in km _(relevant for optimizer performance)_.


## Basic step-by-step instruction

0. To use the script you can first open a new repl on https://repl.it (language: `Python`) and just copy the content of [aurora4xMissiles.py](https://raw.githubusercontent.com/jjermann/aurora4xMissiles/master/aurora4xMissiles.py) (which already contains an example) in it then hit `Run`.
You can then adjust the example for your purposes...
1. Set `AuroraData` (default) and `TechnologyContext` based on your current game status.
2. Set the `CalculationContext` and run the `MissileOptimization` with `AuroraData`, `TechnologyContext` and `CalculationContext`, you can print the results with `printTopMissiles()`.
The initial goal should be to roughly determined the desired damage (ideally a square number).
To do this first set a very rough calculation context or try to calculate *some* example calculation contexts to get a rough idea what the damage should be.
If the optimizer is too slow then first try some example ranges for damage to reduce the number of candidates.
Since we are interested in the damage the default sorting (by damage) should be used (i.e. just `printTopMissiles()`, also see the example below).
3. In a next step I would suggest to narrow down on the desired `minRange` a bit and maybe already start thinking about very rough `minCth` and `minSpeed`/`maxSpeed` limits.
We can still use the default sorting here...
4. Now the more delicate optimizations kick in with the basic question: Do we generally want more speed or a greater chance to hit?
Now it makes sense to try different sortings and to further narrow down on `minSpeed` and `minCth`.
For speed based sorting you can use `printTopMissiles(sortFn = lambda m:m.getSpeed())`.
For `cth` based sorting you can use e.g. `printTopMissiles(sortFn = lambda m:m.getCth(35000), infoFn = lambda m: "Cth = {}".format(m.getCth(35000))`.
Again note that the precise value of the intended target speed (e.g. `35000`) is of no relevance for the optimization but it is of course of relevance to know (and limit) the chance to hit versus a specific speed.
In addition I suggest to also try sorting by engine power, it usually gives quite good results for both chance to hit and speed.
For engine power based sorting you can use `printTopMissiles(sortFn = lambda m:m.engineSetup.ep)`.
5. At the end you should ideally have narrowed down the candidates to a few hundreds or a few thousands and based on the various top candidates for speed, chance to hit and engine power it's time to pick your favorite missile.


## Example:

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
