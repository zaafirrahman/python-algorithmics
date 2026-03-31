'''A module for calculating the Ruffier test result.


Ideally, the sum of pulse rate shall be measured in three attempts (before the physical exertion, immediately after it, and after a short rest)
should not exceed 200 beats per minute.
We suggest the children measure their pulse for 15 seconds
and bring the result to beats per minute, multiplying it by 4:
   S = 4 * (P1 + P2 + P3)
The further this result from the ideal 200 beats is, the worse.
Traditionally, tables are given for a value divided by 10.


Ruffier Index  
   IR = (S - 200) / 10
is estimated by the table according to one's age:
       7-8             9-10                11-12               13-14               15+ (for teenagers only!)
exl.    6.4 and less    4.9  and less       3.4  and less         1.9  and less               0.4  and less
good    6.5 - 11.9     5 - 10.4          3.5 - 8.9           2 - 7.4                   0.5 - 5.9
sat.  12 - 16.9      10.5 - 15.4       9 - 13.9            7.5 - 12.4                6 - 10.9
weak  17 - 20.9      15.5 - 19.4       14 - 17.9           12.5 - 16.4               11 - 14.9
unsat.   21 and more     19.5 and more      18 and more          16.5 and more              15 and more


for all ages, the difference between the unsatisfactory and weak results is 4,
the difference between the weak and satisfactory results is 5, and the difference between the good and satisfactory results is 5.5


therefore, let's code the ruffier_result(r_index, level) function that would receive
the calculated Ruffier index and the "unsatisfactory" level for the tested person's age, and return the result


'''
# here you can specify the strings representing the result:
txt_index = "Your Ruffier Index: "
txt_workheart = "Cardiac performance: "
txt_nodata = '''no data for this age'''
txt_res = []
txt_res.append('''low.
Urgently consult the doctor!''')
txt_res.append('''satisfactory.
Consult the doctor!''')
txt_res.append('''average.
It may be worth an additional consultation of the doctor.''')
txt_res.append('''
above average''')
txt_res.append('''
high''')


def ruffier_index(P1, P2, P3):
   '''returns the index value by three pulse rate indicators for making reconciliation with the table'''
   return (4 * (P1+P2+P3) - 200) / 10


def neud_level(age):
   '''options with an age less than 7 and age of adults should be processed separately;
   here we shall select the "unsatisfactory" level only inside the table:
   for children aged 7, "unsatisfactory" is the index of 21; then, it decreases by 1.5 every 2 years to the value of 15 for children aged 15-16 '''
   norm_age = (min(age, 15) - 7) // 2  # for the age up to 15, every 2 years of the difference between the age and 7 years should be taken as 1
   result = 21 - norm_age * 1.5 # every 2 years of the difference should be multiplied by 1.5; this way the levels in the table are distributed
   return result
  
def ruffier_result(r_index, level):
   '''the function gets the Ruffier index and interprets it
   returning the fitness level: a number from 0 to 4
   (the higher the level is, the better).  '''
   if r_index >= level:
       return 0
   level = level - 4 # this will not be executed if we have already returned the "unsatisfactory" response
   if r_index >= level:
       return 1
   level = level - 5 # similarly, we get here if the level is at least "satisfactory"
   if r_index >= level:
       return 2
   level = level - 5.5 # next level
   if r_index >= level:
       return 3
   return 4 # we are here if the index is less than all the intermediate levels; i.e. the tested person has great results.


def test(P1, P2, P3, age):
   ''' this function may be used outside the module for calculating the Ruffier index.
   It returns the finished texts that shall be drawn in the right place
   For the texts, it uses the constants specified at the beginning of this module. '''
   if age < 7:
       return (txt_index + "0", txt_nodata) # the enigma not intended for this test
   else:
       ruff_index = ruffier_index(P1, P2, P3) # calculation
       result = txt_res[ruffier_result(ruff_index, neud_level(age))] # the interpretation; conversion the numeric value of the fitness level into a text
       res = txt_index + str(ruff_index) + '\n' + txt_workheart + result
       return res
