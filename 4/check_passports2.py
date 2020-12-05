import re

#    byr (Birth Year)
#    iyr (Issue Year)
#    eyr (Expiration Year)
#    hgt (Height)
#    hcl (Hair Color)
#    ecl (Eye Color)
#    pid (Passport ID)
#    cid (Country ID)


def check_fields(data):
	#required_fields = {"byr","iyr","eyr","hgt","hcl","ecl","pid","cid"}
	required_fields = {"byr","iyr","eyr","hgt","hcl","ecl","pid"}
	pattern = re.compile("\s(\w+):")
	m = re.findall(pattern,data)
	passport_fields = set(m)
	if len(required_fields.difference(passport_fields)) == 0:
		return True
	else:
		return False

def check_values(data):
	print(data)
	valid = True
	pattern = re.compile("byr:(\d+)")
	m = pattern.search(data)
	if m == None or int(m.group(1)) < 1920 or int(m.group(1)) > 2002: 	
		print("invalid byr")
		valid = False
	pattern = re.compile("iyr:(\d+)")
	m = pattern.search(data)
	if m == None or int(m.group(1)) < 2010 or int(m.group(1)) > 2020: 	
		print("invalid iyr")
		valid = False
	pattern = re.compile("eyr:(\d+)")
	m = pattern.search(data)
	if m == None or int(m.group(1)) < 2020 or int(m.group(1)) > 2030: 	
		print("invalid eyr")
		valid = False
	pattern1 = re.compile("hgt:(\d+)cm")
	pattern2 = re.compile("hgt:(\d+)in")
	m1 = pattern1.search(data)
	m2 = pattern2.search(data)
	if (m1 == None or int(m1.group(1)) < 150 or int(m1.group(1)) > 193) and \
      (m2 == None or int(m2.group(1)) < 59 or int(m2.group(1)) > 76): 	
		print("invalid hgt")
		valid = False
	pattern = re.compile("hcl:#([0-9a-f]){6}")
	m = pattern.search(data)
	if m == None:
		print("invalid hcl")
		valid = False
	pattern = re.compile("ecl:(\w+)")
	m = pattern.search(data)
	if m == None or (m.group(1) not in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]):
		print("invalid ecl")
		valid = False
	pattern1 = re.compile("pid:(\d+){9}")
	pattern2 = re.compile("pid:(\d+){10}")
	m1 = pattern1.search(data)
	m2 = pattern2.search(data)
	if m1 == None or (m1 != None and m2 != None):
		print("invalid pid")
		valid = False

	return valid

### main ###
#infile = 'input1_test'
infile = 'input1'
#infile = 'input1_valid'
#infile = 'input1_invalid'
f = open(infile,'r')

count_valid = 0
passport = ""
for line in f:
	if line.rstrip() == "":
		# end of passport info
		valid = (check_fields(passport) and check_values(passport))
		if valid:
			count_valid += 1
		passport = ""
	else:
		passport += " " + line.rstrip()
if len(passport) != 0:
	valid = (check_fields(passport) and check_values(passport))
	if valid:
		count_valid += 1
  

print("Number of valid passports: " + str(count_valid))
