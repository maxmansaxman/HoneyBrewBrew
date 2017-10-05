
'''Program to read, write, and calculate data and aspects of the
brewing process'''

import math
import cPickle

class HopAdditions:
  "A class for a hop addition during the boil"
  def __init__(self,name,AA):
    self.name=name
    self.AA=AA


class Brew:
  "A class for all the attributes of the beer you're making"

  def __init__(self, name):
        self.name=name

  og = 0

  fg = 0

  ibu = 0

  abv = 0

  hopsAAs={}

  hops=[]

  grains={}




def brew_reader(filePath):
  '''A method to read brew data from a file using cPickle'''
  file = open(filePath, 'r+')
  beer=cPickle.load(file)
  print 'The beer %s was read from the file \n%s' % (beer.name, filePath)
  file.close()
  return beer


def brew_writer(filePath,beer):
  '''A method for writing brew data to a file'''
  file=open(filePath,'w')
  cPickle.dump(beer,file)
  print 'The beer %s was saved to the file \n%s' % (beer.name, filePath)
  file.close()
  



def abv_calculator(og,fg):
  '''A function to calculate the abv of a beer'''
  alc=(76.08*(og-fg)/(1.775-og))*(fg/0.794)
  return alc

def mash_vol_calculator(lbs):
  '''a function to calculate the recommended mash volume, in gallons'''
  mashVol=lbs*1.125/4
  return mashVol

def sparge_vol_calculator(lbs):
  '''a function to calculate the recommended sparge volume, in gallons'''
  spargeVol=lbs*0.5
  return spargeVol



print('Welcome to Honey Brew Brew version 0.2')
while True:
    choice=raw_input(
    'Would you like to start a (n)ew brew or (m)odify an existing one? ')
    if choice.lower() == 'm':
      filePath=raw_input('Enter the name of the recipe file: ')
      beer=brew_reader(filePath)
      break
    if choice.lower() == 'n':
      print('New brew it is!')
      name=raw_input('What would you like to call your beer? \n')
      beer=Brew(name)
      break
    if choice.lower() not in ['n', 'm']:
      print('Not a valid response, please try again')



while True:
  print('What would you like to do with %s? '%beer.name)
  choice=raw_input(
  '(A)BV, (I)BUs, (M)ash grains, (E)fficiency calcutaion, (S)ave your brew, or (Q)uit ')
  if choice.upper() =='A':
    og=raw_input('What is your original gravity? ')
    beer.og=float(og)
    fg=raw_input('What is your final gravity? ')
    beer.fg=float(fg)
    beer.abv= abv_calculator(beer.og,beer.fg)
    print('Your alcohol content is %.2f percent' %beer.abv)

  if choice.upper()=='I':
    hops={}
    print("Let's calculate some expected IBUs")
    print("Go grab your hops schedule")
    print("First let's find all the types of hops you'll be using")
    while True:
      hopName=raw_input('Type the name of a hop, or press RETURN to stop \n')
      if len(hopName)==0:
        break
      AA=raw_input('What is the Alpha Acid (AA) content listed? \n')
      AA=float(AA)
      hops[hopName]= AA

    print("Now we'll go through your hop additions in the boil")
    bg=raw_input("What's your estimated boil gravity? (or go with default) \n")
    if len(bg)==0:
      bg=float(1.050)
    else :
      bg=float(bg)
    vol=raw_input("What's your batch volume (in gal)? (or go with default) \n")
    if len(vol)==0:
      vol=float(5)
    else :
      vol=float(vol)
    additions=[]
    IBUs=[]
    for h in hops.keys():
      while True:
        time=raw_input(
        "What's the boil time of an addition of %s? \n" %h)
        if len(time)==0:
          break
        time=float(time)
        weight=raw_input(
        "What's the weight, in oz, of the %s addition at %d minutes? \n" %(h,time))
        weight=float(weight)
        utilization = 1.65*(0.000125**(bg-1))*(1-math.exp(-0.04*time))/4.15
        IBU = weight*hops[h]*utilization*74.89/vol
        print('This adds %.2f IBUs' %int(IBU))
        additions.append([time, h, weight])
        IBUs.append(IBU)
    IBU_total=sum(IBUs)
    print('Total IBUs are %d' %IBU_total)
    # adding new information to brew
    beer.ibu=IBU_total
    beer.hops=additions
    beer.hopAAs=hops

  if choice.upper()=='M':
    # if len(grains)>0:
    #   print 'There is already a grain bill for this brew:\n'
    #   print grains
    #   overwrite=raw_input('Would you like to overwrite this? (y/n)\n')
    #   if overwrite.lower=='n':
    #     break
    #   elif overwrite.upper=='y':
    #     continue
    grains={}
    print 'Mash calculations'
    print 'First let\'s find your grain bill'
    while True:
      grainName=raw_input('Type the name of a grain, or press RETURN to stop \n')
      if len(grainName)==0:
        break
      lbs=raw_input('How many lbs of grain are you using (rounded down)? \n')
      oz=raw_input('and additional ounces? \n')
      lbs=float(lbs)+float(oz)/16
      grains[grainName]= lbs

    lbs_total=sum(grains.values())
    print('%.2f lbs of grain in your grain bill \n' %lbs_total)
    mashVol=mash_vol_calculator(lbs_total)
    print('Use %.2f gallons of water for your mash \n' %mashVol)
    spargeVol=sparge_vol_calculator(lbs_total)
    print('Use %.2f gallons of water for your sparge \n' %spargeVol)

    #adding info to brew
    beer.grains=grains






  if choice.upper()=='S':
    print 'Saving your brew'
    filePath=raw_input('Name of the file to save your brew as: ')
    brew_writer(filePath,beer)
    print('Goodbye!')
    break





  if choice.upper() =='Q':
    print('Quitting the program')
    print('Happy brewing!')
    break

  elif choice.upper() not in ['A', 'I', 'E', 'S', 'Q']:
    print('Invalid selection, please try again')
