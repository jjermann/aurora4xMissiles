#!/usr/bin/python3

import math

class AuroraData:
  def __init__(self):
    self.agilityTech = [20, 32, 48, 64, 80, 100, 128, 160, 200, 240, 320, 400]
    self.warheadTech = {
      "Gun-Type Fission"                  : 2.0,
      "Implosion Fission"                 : 3.0,
      "Levitated-pit Implosion"           : 4.0,
      "Fusion-boosted Fission"            : 5.0,
      "Two-stage Thermonuclear"           : 6.0,
      "Three-stage Thermonuclear"         : 8.0,
      "Cobalt"                            : 10.0,
      "Tri-Cobalt"                        : 12.0,
      "Antimatter Catalyzed Cobalt"       : 16.0,
      "Antimatter"                        : 20.0,
      "Advanced Antimatter"               : 24.0,
      "Gravitonic"                        : 30.0
    }
    self.engineTech = {
      "Conventional Engine"               : 0.1,
      "Nuclear Thermal Engine"            : 5.0,
      "Improved Nuclear Thermal Engine"   : 6.4,
      "Nuclear Pulse Engine"              : 8.0,
      "Improved Nuclear Pulse Engine"     : 10.0,
      "Ion Drive"                         : 12.5,
      "Magneto-plasma Drive"              : 16.0,
      "Internal Confinement Fusion Drive" : 20.0,
      "Magnetic Confinement Fusion Drive" : 25.0,
      "Inertial Confinement Fusion Drive" : 32.0,
      "Solid-core Anti-matter Drive"      : 40.0,
      "Gas-core Anti-matter Drive"        : 50.0,
      "Plasma-core Anti-matter Drive"     : 64.0,
      "Beam-core Anti-matter Drive"       : 80.0,
      "Photonic Drive"                    : 100.0
    }
    self.fuelConsumptionTech = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.25, 0.2, 0.16, 0.125, 0.1]
    self.minMultiplierTech = [0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1]
    self.maxMultiplierTech = [1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0]
    self.engineMultipliers = [ intm*1.0/20 for intm in range(2, 121) ]
    self.engineMsps = [ intmsp*1.0/100 for intmsp in range(10, 300) ] + [ intmsp*1.0/100 for intmsp in range(300, 1000, 10) ] + [ intmsp*1.0/100 for intmsp in range(1000, 5050, 50) ]


class TechnologyContext:
  def __init__(self):
    self.damagePerMsp = 20
    self.agilityPerMsp = 160
    self.EPPerHs = 50
    self.fuelConsumption = 0.2
    self.minPowerFactor = 0.1
    self.maxPowerFactor = 6

  def getEPPerMsp(self):
    return self.EPPerHs/20.0

  def setEPPerMsp(self, epPerMsp):
    self.EPPerHs = epPerMsp*20.0


class CalculationContext:
  def __init__(self):
    self.intendedTargetSpeed = 10000
    self.size = 6
    self.minExcessSize = 0
    self.minCth = 0
    self.minSpeed = None
    self.maxSpeed = None
    self.minRange = 0
    self.minDamage = 0
    self.maxDamage = None
    #obsolete (leave as 1)
    self.maxNr = 1


class EngineSetup:
  def __init__(self, technologyContext, nr, multiplier, msp):
    self.technologyContext = technologyContext
    self.nr = nr
    self.multiplier = multiplier
    self.msp = msp
    self._dispPrec = 5
    self._prec = 5

    epInternal = self.technologyContext.getEPPerMsp()*self.msp*self.multiplier
    fuelConsumptionBaseModifier = self.technologyContext.fuelConsumption
    fuelConsumptionSizeModifier = self.getFuelConsumptionSizeModifier()
    fuelConsumptionMultiplierModifier = self.getFuelConsumptionMultiplierModifier()
    fuelEfficiency = fuelConsumptionBaseModifier*fuelConsumptionSizeModifier*fuelConsumptionMultiplierModifier
    self.ep = round(epInternal, 2)
    # Remark: "Fuel per EPH" in the missile designer is = self.ep*self.fuelPerEPH, shouldn't that be "Fuel per Hour"?
    self.fuelPerEPH = fuelEfficiency

  def getFuelConsumptionSizeModifier(self):
    fuelConsumptionSizeModifier = math.sqrt(200.0/self.msp)
    return fuelConsumptionSizeModifier

  def getFuelConsumptionMultiplierModifier(self):
    if self.multiplier > self.technologyContext.maxPowerFactor:
      highBoostModifier = (self.multiplier - self.technologyContext.maxPowerFactor) * 4.0 / self.technologyContext.maxPowerFactor + 1.0
    else:
      highBoostModifier = 1.0
    fuelConsumptionMultiplierModifier = highBoostModifier * self.multiplier**2.5
    return fuelConsumptionMultiplierModifier

  def getFuelPerHour(self):
    return self.fuelPerEPH*self.ep

  def getTotalFuelPerSecond(self):
    return self.getFuelPerHour()*self.nr/3600.0

  def __repr__(self):
    nr = ""
    if self.nr > 1:
      nr = "{} x ".format(self.nr)
    return "{}EP = {}, MSP = {}, multiplier = {}, Fuel/EPH = {}, Fuel/Hour = {}".format(
      nr,
      round(self.ep, self._dispPrec),
      round(self.msp, self._dispPrec),
      round(self.multiplier, self._dispPrec),
      round(self.fuelPerEPH, self._dispPrec),
      round(self.getFuelPerHour(), self._dispPrec))

  def getTotalEngineMsp(self):
    return self.msp*self.nr

  def getSpeed(self, totalMsp):
    return round(1000*self.ep*self.nr*20.0/totalMsp, self._prec)

  def getRoundedSpeed(self, totalMsp):
    speed = self.getSpeed(totalMsp)
    return round(round(speed, -2))

  #range is in km
  def getRequiredFuelMsp(self, totalMsp, desiredRange):
    if desiredRange is None:
      return 0.0
    speed = self.getSpeed(totalMsp)
    fuelConsumptionPerSecond = self.getTotalFuelPerSecond()
    fuel = desiredRange*fuelConsumptionPerSecond/speed
    fuelMsp = fuel*1.0 / 2500
    return fuelMsp

class Missile:
  def __init__(self, technologyContext, warheadMsp, fuelMsp, engineSetup, agilityMsp, excessMsp):
    self.technologyContext = technologyContext
    self.warheadMsp = warheadMsp
    self.fuelMsp = fuelMsp
    self.engineSetup = engineSetup
    self.agilityMsp = agilityMsp
    self.excessMsp = excessMsp
    self._dispPrec = 5
    self._prec = 5

  def __repr__(self):
    return self.getInputDataRepresentation() + '\n' + self.getMissileRepresentation() + '\n'

  def getInputDataRepresentation(self):
    inputDataRepresentation = f'Size = {self.getSize()}: WH MSP = {round(self.warheadMsp, self._dispPrec)}, Fuel MSP = {round(self.fuelMsp, self._dispPrec)}, Agility MSP = {round(self.agilityMsp, self._dispPrec)}, Excess MSP = {self.excessMsp}, Engine Power Modifier = {round(self.engineSetup.multiplier*100)}%, Engine Size MSP = {round(self.engineSetup.getTotalEngineMsp(), self._dispPrec)}'
    return inputDataRepresentation

  def getMissileRepresentation(self):
    missileRepresentation = f'Damage = {self.getDamage()}, EP = {round(self.engineSetup.ep, self._dispPrec)}, Speed = {round(self.getSpeed(), self._dispPrec)} km/s, Range = {round(self.getRange()/1000000, self._dispPrec)}m km, MR = {self.getMr()}, Cth = {round(self.getCth(3000), self._dispPrec)}% / {round(self.getCth(5000), self._dispPrec)}% / {round(self.getCth(10000), self._dispPrec)}%'
    return missileRepresentation

  def getGameMissileRepresentation(self):
    gameMissileRepresentation = f'Missile Size: {self.getSize()} MSP  ({self.getSize()*5.0} Tons)     Warhead: {round(self.warheadMsp, self._dispPrec)}    Manoeuvre Rating: {self.getMr()}\n'
    gameMissileRepresentation += f'Speed: {round(self.getSpeed(), self._dispPrec)} km/s     Fuel: {round(self.getFuel(), self._dispPrec)}     Flight Time: {round(self.getFlightTime()/60.0)} minutes     Range: {round(self.getRange()/1000000), self._dispPrec}m km\n'
    gameMissileRepresentation += f'Chance to Hit: 1k km/s {round(self.getCth(1000), self._dispPrec)}%   3k km/s {round(self.getCth(3000), self._dispPrec)}%   5k km/s {round(self.getCth(5000), self._dispPrec)}%   10k km/s {round(self.getCth(10000), self._dispPrec)}%\n'
    return gameMissileRepresentation

  def getSize(self):
    size = self.warheadMsp + self.engineSetup.getTotalEngineMsp() + self.fuelMsp + self.agilityMsp + self.excessMsp
    return round(size, self._prec)

  def getSpeed(self):
    speed = self.engineSetup.getSpeed(self.getSize())
    return round(speed, self._prec)

  def getRoundedSpeed(self):
    roundedSpeed = self.engineSetup.getRoundedSpeed(self.getSize());
    return roundedSpeed

  def getDamage(self):
    damage = math.floor(self.technologyContext.damagePerMsp*self.warheadMsp)
    return damage

  def getFuel(self):
    fuel = self.fuelMsp*2500
    return round(fuel, self._prec)

  def getRange(self):
    range = self.getFuel()*self.getSpeed()*1.0/self.engineSetup.getTotalFuelPerSecond()
    return round(range, self._prec)

  def getFlightTime(self):
    flightTimeInSeconds = self.getFuel()*1.0/self.engineSetup.getTotalFuelPerSecond()
    return flightTimeInSeconds

  def getMr(self):
    mr = 10 + round(self.technologyContext.agilityPerMsp*self.agilityMsp/self.getSize())
    return mr

  def getCth(self, targetSpeed):
    cth = self.getSpeed()/targetSpeed*self.getMr()
    return round(cth, self._prec)


class MissileOptimization:
  def __init__(self, auroraData, technologyContext, calculationContext):
    self.auroraData = auroraData
    self.technologyContext = technologyContext
    self.calculationContext = calculationContext
    self._auroraData = AuroraData()
    # Precision must be lower than the high precision used in Missile
    self._prec = 4

    self._allWarhead = self._getAllWarheadMsp()
    if len(self._allWarhead) > 0:
      self._minWarheadMsp = min(self._allWarhead)
    else:
      self._minWarheadMsp = 10000000.0
    self._allEngines = self._getAllEngineSetup()
    if len(self._allEngines) > 0:
      self._minEngineMsp = min([e.getTotalEngineMsp()+e.getRequiredFuelMsp(self.calculationContext.size, self.calculationContext.minRange) for e in self._allEngines])
    else:
      self._minEngineMsp = 10000000.0
    self._allMr = self._getAllMr()
    self._allMissiles = None

  def __repr__(self):
    outputStr = "Engine candidates: {}".format(len(self._allEngines)) + "\n"
    outputStr += "Warhead candidates: {}".format(len(self._allWarhead)) + "\n"
    outputStr += "MR candidates: {0}".format(len(self._allMr)) + "\n"
    return outputStr

  def _getAllEngineSetup(self):
    maxMsp = self.calculationContext.size - self.calculationContext.minExcessSize - self._minWarheadMsp
    engineSetups = []
    for msp in self.auroraData.engineMsps:
      for multiplier in self.auroraData.engineMultipliers:
        if self._checkMultiplier(multiplier):
          maxNr = math.floor(maxMsp*1.0/msp)
          if not self.calculationContext.maxNr is None:
            maxNr = min(maxNr, self.calculationContext.maxNr)
          for nr in range(1, maxNr + 1):
            engineSetup = EngineSetup(self.technologyContext, nr, multiplier, msp)
            if self._checkEngine(engineSetup):
              engineSetups.append(engineSetup)
    return engineSetups

  def _checkMultiplier(self, multiplier):
    if not (self.technologyContext.minPowerFactor is None or multiplier >= self.technologyContext.minPowerFactor):
      return False
    # if not (self.technologyContext.maxPowerFactor is None or multiplier <= self.technologyContext.maxPowerFactor):
    #   return False
    return True

  def _checkEngine(self, engineSetup):
    speed = engineSetup.getRoundedSpeed(self.calculationContext.size)
    if not (self.calculationContext.minSpeed is None or speed>=self.calculationContext.minSpeed):
      return False
    if not (self.calculationContext.maxSpeed is None or speed<=self.calculationContext.maxSpeed):
      return False
    return True

  def _getAllWarheadMsp(self):
    minDmg = self.calculationContext.minDamage
    maxMsp = self.calculationContext.size - self.calculationContext.minExcessSize
    damagePerMsp = self.technologyContext.damagePerMsp
    mspPerDamage = 1.0/damagePerMsp
    damageSteps = math.floor(maxMsp / mspPerDamage)
    if not self.calculationContext.maxDamage is None:
      maxDmg = min(damageSteps, self.calculationContext.maxDamage)
    else:
      maxDmg = damageSteps
    # minDmgStep = 10*10**(-self._prec)*mspPerDamage
    # warheadMsps = [round(minDmgStep + dmg*mspPerDamage, self._prec) for dmg in range(minDmg, maxDmg+1)]
    warheadMsps = [math.ceil(dmg*mspPerDamage*10**self._prec)*1.0/(10**self._prec) for dmg in range(minDmg, maxDmg+1)]
    return warheadMsps

  def _getAllMr(self):
    maxMsp = self.calculationContext.size - self.calculationContext.minExcessSize - self._minWarheadMsp - self._minEngineMsp
    agilityPerMsp = self.technologyContext.agilityPerMsp
    mrPerMsp = agilityPerMsp*1.0/self.calculationContext.size
    mspPerMr = 1.0/mrPerMsp
    minAgilityStep = 10*10**(-self._prec)*mspPerMr
    initialMspForMr = minAgilityStep + 0.5*self.calculationContext.size/agilityPerMsp
    remainingMsp = maxMsp-initialMspForMr
    mrSteps = math.floor(remainingMsp / mspPerMr)
    agilityMsps = [0] + [round(initialMspForMr + k*mspPerMr, self._prec) for k in range(0, mrSteps+1)]
    return agilityMsps

  def getAllMissiles(self):
    if self._allMissiles is None:
      missiles = []
      remainingMsp = self.calculationContext.size - self.calculationContext.minExcessSize
      for warhead in self._allWarhead:
        remainingMspAfterWarhead = remainingMsp - warhead
        for engineSetup in [e for e in self._allEngines if e.getTotalEngineMsp() <= remainingMspAfterWarhead]:
          remainingMspAfterEngines = remainingMspAfterWarhead - engineSetup.getTotalEngineMsp()
          for agility in [a for a in self._allMr if a <= remainingMspAfterEngines]:
            fuelMsp = remainingMspAfterEngines - agility
            if (fuelMsp > 0):
               missile = Missile(self.technologyContext, warhead, fuelMsp, engineSetup, agility, self.calculationContext.minExcessSize)
               if self._checkMissile(missile):
                 missiles.append(missile)
      self._allMissiles = missiles
    return self._allMissiles

  def _checkMissile(self, missile):
    size = missile.getSize()
    calcCtx = self.calculationContext
    if size > calcCtx.size:
      raise Exception("Size = {} > {}".format(size, calcCtx.size))
    if missile.excessMsp < calcCtx.minExcessSize:
      raise Exception("ExcessMsp = {} < {}".format(missile.excessMsp, calcCtx.minExcessSize))
    speed = missile.getRoundedSpeed()
    if not calcCtx.minSpeed is None and speed < calcCtx.minSpeed:
      raise Exception("Speed = {} < {}".format(speed, calcCtx.minSpeed))
    if not calcCtx.maxSpeed is None and speed > calcCtx.maxSpeed:
      raise Exception("Speed = {} > {}".format(speed, calcCtx.maxSpeed))
    if not calcCtx.minDamage is None and missile.getDamage() < calcCtx.minDamage:
      raise Exception("Damage = {} < {}".format(missile.getDamage(), calcCtx.minDamage))
    if not calcCtx.maxDamage is None and missile.getDamage() > calcCtx.maxDamage:
      raise Exception("Damage = {} > {}".format(missile.getDamage(), calcCtx.maxDamage))
    if not calcCtx.minRange is None and missile.getRange() < calcCtx.minRange:
      return False
    if not calcCtx.minCth is None and missile.getCth(calcCtx.intendedTargetSpeed) < calcCtx.minCth:
      return False
    return True

  def _dmgCthSort(self, missile):
    return (missile.getDamage(), missile.getCth(self.calculationContext.intendedTargetSpeed))

  def getTopMissiles(self, sortFn = None, reverse=True, top=5):
    if (sortFn is None):
      sortFn = self._dmgCthSort
    allMissiles = self.getAllMissiles()
    sortedMissiles = sorted(allMissiles, key=sortFn, reverse=reverse)
    return sortedMissiles[:top]

  def printTopMissiles(self, sortFn = None, reverse=True, top=5, infoFn = None, reprFn = None):
    if (sortFn is None):
      sortFn = self._dmgCthSort
    candidates = len(self.getAllMissiles())
    topMissiles = self.getTopMissiles(sortFn=sortFn, reverse=reverse, top=top)
    outputStr = "{} candidates:\n\n".format(candidates)
    for m in topMissiles:
      if reprFn is None:
        if infoFn is None:
          info = ""
        else:
          info = "  {}\n".format(infoFn(m))
        outputStr += "{}{}\n".format(m, info)
      else:
        outputStr += "{}\n".format(reprFn(m))
    return outputStr


# EXAMPLE

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
  calcContext.minDamage = 13
  calcContext.maxDamage = 14
  calcContext.minSpeed = 10000
  calcContext.maxSpeed = 20000
  calcContext.minRange = 100000000
  calcContext.minCth = 30

  # calcContext.size = 1
  # calcContext.minDamage = 1
  # calcContext.maxDamage = 1
  # calcContext.minSpeed = 10000
  # calcContext.maxSpeed = 20000
  # calcContext.minRange = 100000
  # calcContext.minCth = 100

  missileOpt = MissileOptimization(auroraData, techContext, calcContext)
  return missileOpt

example = getExampleOptimizer()
print(example)

#In case missiles should be sorted by chance to hit (descending), including an infoFn:
#topMissiles = example.printTopMissiles(sortFn = lambda m:m.getCth(100000), infoFn = lambda m: "Cth = {}".format(m.getCth(100000)))
#In case missiles should be sorted by damage
topMissiles = example.printTopMissiles()
print(topMissiles)
