#!/usr/bin/python3

import math

class AuroraData:
  def __init__(self):
    self.agilityTech = [20, 32, 48, 64, 80, 100, 128, 160, 200, 240, 320, 400]
    self.warheadTech = {
      "Gun-Type Fission"            : 2.0,
      "Implosion Fission"           : 3.0,
      "Levitated-pit Implosion"     : 4.0,
      "Fusion-boosted Fission"      : 5.0,
      "Two-stage Thermonuclear"     : 6.0,
      "Three-stage Thermonuclear"   : 8.0,
      "Cobalt"                      : 10.0,
      "Tri-Cobalt"                  : 12.0,
      "Antimatter Catalyzed Cobalt" : 16.0,
      "Antimatter"                  : 20.0,
      "Advanced Antimatter"         : 24.0,
      "Gravitonic"                  : 30.0
    }
    self.warheadTech = {}
    self.engineTech = {
      "Conventional"                : 0.2,
      "Nuclear Thermal"             : 5.0,
      "Nuclear Pulse"               : 8.0,
      "Ion"                         : 12.0,
      "Magneto-Plasma"              : 16.0,
      "Internal Confinement Fusion" : 20.0,
      "Magnetic Confinement Fusion" : 25.0,
      "Inertial Confinement Fusion" : 32.0,
      "Solid-core Anti-matter"      : 40.0,
      "Gas-core Anti-matter"        : 50.0,
      "Plasma-core Anti-matter"     : 60.0,
      "Beam-core Anti-matter"       : 80.0,
      "Photonic Drive"              : 100.0
    }
    self.fuelConsumptionTech = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.25, 0.2, 0.16, 0.125, 0.1]
    self.minMultiplierTech = [0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1]
    self.maxMultiplierTech = [1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0]
    self.engineMultipliers = [ intm*1.0/20 for intm in range(2, 121) ]
    self.engineMsps = [ intmsp*1.0/100 for intmsp in range(10, 500) ]
  

class TechnologyContext:
  def __init__(self):
    self.damagePerMsp = 20
    self.agilityPerMsp = 160
    self.EPPerHs = 50
    self.fuelConsumption = 0.2
    self.MinPowerFactor = 0.1
    self.MaxPowerFactor = 6

  def getEPPerMsp(self):
    return self.EPPerHs/20.0


class CalculationContext:
  def __init__(self):
    self.intendedTargetSpeed = 10000
    self.size = 6
    self.minExcessSize = 0
    self.minCth = 0
    self.minSpeed = None
    self.maxSpeed = None
    self.maxNr = 1
    self.minRange = 0
    self.minDamage = 0
    self.maxDamage = None


class EngineSetup:
  def __init__(self, technologyContext, nr, multiplier, msp):
    self.technologyContext = technologyContext
    self.nr = nr
    self.multiplier = multiplier
    self.msp = msp

    self.ep = self.technologyContext.getEPPerMsp()*self.msp*self.multiplier
    fuelConsumptionBaseModifier = self.technologyContext.fuelConsumption
    fuelConsumptionSizeModifier = 1.0/((self.msp/5.0)**0.683)
    fuelConsumptionMultiplierModifier = self.multiplier**2.5
    self.fuelPerEPH = 5.0*fuelConsumptionBaseModifier*fuelConsumptionSizeModifier*fuelConsumptionMultiplierModifier

  def getFuelPerHour(self):
    return self.fuelPerEPH*self.ep

  def getTotalFuelPerSecond(self):
    return self.getFuelPerHour()*self.nr/3600.0

  def __repr__(self):
    return "{} x [{} EP ({} MSP) missile engine with multiplier {}, Fuel/EPH={}, Fuel/Hour={}]".format(self.nr, self.ep, self.msp, self.multiplier, self.fuelPerEPH, self.getFuelPerHour())
    
  def getTotalEngineMsp(self):
    return self.msp*self.nr

  def getSpeed(self, totalMsp):
    return 1000*self.ep*self.nr*20.0/totalMsp

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

  def __repr__(self):
    return "Size={} (WH={}, Fuel={}, Agility={}, Engine={}, Excess={}), Speed={}, Damage={}, Range={} mkm, 10000km/s Cth={}, Engine={}".format(
      self.getSize(), round(self.warheadMsp,2), round(self.fuelMsp,2), round(self.agilityMsp,2), round(self.engineSetup.getTotalEngineMsp(),2), self.excessMsp, round(self.getSpeed()), self.getDamage(), round(self.getRange()/1000000), self.getCth(10000), self.engineSetup)
    
  def getSize(self):
    size = self.warheadMsp + self.engineSetup.getTotalEngineMsp() + self.fuelMsp + self.agilityMsp + self.excessMsp
    return round(size,6)

  def getSpeed(self):
    speed = self.engineSetup.getSpeed(self.getSize())
    return round(speed,6)
  
  def getDamage(self):
    damage = math.floor(self.technologyContext.damagePerMsp*self.warheadMsp)
    return damage

  def getFuel(self):
    fuel = self.fuelMsp*2500
    return round(fuel,6)

  def getRange(self):
    range = self.getFuel()*self.getSpeed()*1.0/self.engineSetup.getTotalFuelPerSecond()
    return round(range,6)

  def getMr(self):
    mr = round(self.technologyContext.agilityPerMsp*self.agilityMsp/self.getSize())
    return mr

  def getCth(self, its):
    cth = self.getSpeed()/its*(10+self.getMr())
    return round(cth,6)


class MissileOptimization:
  def __init__(self, auroraData, technologyContext, calculationContext):
    self.auroraData = auroraData
    self.technologyContext = technologyContext
    self.calculationContext = calculationContext
    self._auroraData = AuroraData()
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
    print("Engine candidates: {}".format(len(self._allEngines)))
    print("Warhead candidates: {}".format(len(self._allWarhead)))
    print("MR candidates: {0}".format(len(self._allMr)))

  def _getAllEngineSetup(self):
    maxMsp = self.calculationContext.size - self.calculationContext.minExcessSize - self._minWarheadMsp
    engineSetups = []
    for msp in auroraData.engineMsps:
      for multiplier in auroraData.engineMultipliers:
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
    if not (self.technologyContext.MinPowerFactor is None or multiplier >= self.technologyContext.MinPowerFactor):
      return False
    if not (self.technologyContext.MaxPowerFactor is None or multiplier <= self.technologyContext.MaxPowerFactor*2.0):
      return False
    return True

  def _checkEngine(self, engineSetup):
    speed = engineSetup.getSpeed(self.calculationContext.size)
    if not (self.calculationContext.minSpeed is None or speed>=self.calculationContext.minSpeed):
      return False
    if not (self.calculationContext.maxSpeed is None or speed<=self.calculationContext.maxSpeed):
      return False
    return True
    
  def _getAllWarheadMsp(self):
    minDmg = self.calculationContext.minDamage
    maxMsp = self.calculationContext.size - self.calculationContext.minExcessSize
    damagePerMsp = self.technologyContext.damagePerMsp
    mspPerDamage = math.ceil(1.0/damagePerMsp*10000)/10000.0
    damageSteps = math.floor(maxMsp / mspPerDamage)
    if not self.calculationContext.maxDamage is None:
      maxDmg = min(damageSteps, self.calculationContext.maxDamage)
    else:
      maxDamage = damageSteps
    
    warheadMsps = [dmg*mspPerDamage for dmg in range(minDmg, maxDmg+1)]
    return warheadMsps

  def _getAllMr(self):
    maxMsp = self.calculationContext.size - self.calculationContext.minExcessSize - self._minWarheadMsp - self._minEngineMsp
    agilityPerMsp = self.technologyContext.agilityPerMsp
    mrPerMsp = agilityPerMsp*1.0/self.calculationContext.size
    initialMspForMr = 0.5*self.calculationContext.size/agilityPerMsp
    mspPerMr = math.ceil(1.0/mrPerMsp*10000)/10000.0
    remainingMsp = maxMsp-initialMspForMr
    mrSteps = math.floor(remainingMsp / mspPerMr)
    agilityMsps = [0] + [initialMspForMr + k*mspPerMr for k in range(0, mrSteps+1)]
    return agilityMsps

  def getAllMissiles(self):
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
    return missiles

  def _checkMissile(self, missile):
    size = missile.getSize()
    calcCtx = self.calculationContext
    if size > calcCtx.size:
      raise Exception("Size = {} > {}".format(size, calcCtx.size))
    if missile.excessMsp < calcCtx.minExcessSize:
      raise Exception("ExcessMsp = {} < {}".format(missile.excessMsp, calcCtx.minExcessSize))
    speed = missile.getSpeed()
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
  

auroraData = AuroraData()
techContext = TechnologyContext()
techContext.damagePerMsp = 20
techContext.agilityPerMsp = 160
techContext.EPPerHs = 50
techContext.fuelConsumption = 0.2
#techContext.MinPowerFactor = 0.1
#techContext.MaxPowerFactor = 6

calcContext = CalculationContext()
#calcContext.size = 1
#calcContext.minDamage = 1
#calcContext.maxDamage = 1
#calcContext.minSpeed = 50000
#calcContext.maxSpeed = 1000000
#calcContext.minRange = 20000000
#calcContext.minCth = 1000
calcContext.size = 12
calcContext.minExcessSize = 1.0
calcContext.minDamage = 80
calcContext.maxDamage = 100
calcContext.minSpeed = 50000
calcContext.maxSpeed = 1000000
calcContext.minRange = 2000000000
calcContext.minCth = 100

missileOpt = MissileOptimization(auroraData, techContext, calcContext)
allMissiles = missileOpt.getAllMissiles()
#sortedMissiles=sorted(allMissiles, key=lambda m:m.getCth(10000), reverse=True)
sortedMissiles=sorted(allMissiles, key=lambda m:m.getDamage(), reverse=True)
print("Final candidates: {}".format(len(sortedMissiles)))
print(sortedMissiles[0])
print(sortedMissiles[1])
print(sortedMissiles[2])
print(sortedMissiles[3])
print(sortedMissiles[4])
print(sortedMissiles[5])
