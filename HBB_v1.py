
'''Program to read, write, and calculate data and aspects of the
brewing process'''

import math

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

  IBU = 0

  abv = 0


print('Welcome to Honey Brew Brew version 0.1')
while True:
    choice=raw_input(
    'Would you like to start a (n)ew brew or (m)odify an existing one? ')
    if choice.lower() == 'm':
      print('Still working on this')
    if choice.lower() == 'n':
      print('New brew it is!')
      break
    if choice.lower() not in ['n', 'm']:
      print('Not a valid response, please try again')

def abv(og,fg):
  '''A function to calculate the abv of a beer'''
  alc=(76.08*(og-fg)/(1.775-og))*(fg/0.794)
  return alc

hops={}

name=raw_input('What would you like to call your beer? \n')



while True:
  print('What would you like to do with %s? '%name)
  choice=raw_input(
  '(A)BV, (I)BUs, (E)fficiency calcutaion, (S)ave your brew, or (Q)uit ')
  if choice.upper() =='A':
    og=raw_input('What is your original gravity? ')
    og=float(og)
    fg=raw_input('What is your final gravity? ')
    fg=float(fg)
    alc= abv(og,fg)
    print('Your alcohol content is %d percent' %alc)

  if choice.upper()=='I':
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
        print('This adds %d IBUs' %int(IBU))
        additions.append([time, h, weight])
        IBUs.append(IBU)
    IBU_total=sum(IBUs)
    print('Total IBUs are %d' %IBU_total)









  if choice.upper() =='Q':
    print('Quitting the program')
    print('Happy brewing!')
    break

  if choice.upper() not in ['A', 'I', 'E', 'S', 'Q']:
    print('Invalid selection, please try again')
