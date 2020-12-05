import re

#    byr (Birth Year)
#    iyr (Issue Year)
#    eyr (Expiration Year)
#    hgt (Height)
#    hcl (Hair Color)
#    ecl (Eye Color)
#    pid (Passport ID)
#    cid (Country ID)


# create grid
def check_fields(data):
	#required_fields = {"byr","iyr","eyr","hgt","hcl","ecl","pid","cid"}
	required_fields = {"byr","iyr","eyr","hgt","hcl","ecl","pid"}
	pattern = re.compile("\s(\w+):")
	m = re.findall(pattern,data)
	print(data)
	print(m)	
	passport_fields = set(m)
	print(required_fields.difference(passport_fields))
	if len(required_fields.difference(passport_fields)) == 0:
		print("len is 0")
		return True
	else:
		return False

### main ###
infile = 'input1_test'
#infile = 'input1'
f = open(infile,'r')

count_valid = 0
passport = ""
for line in f:
	if line.rstrip() == "":
		# end of passport info
		valid = check_fields(passport)
		if valid:
			count_valid += 1
		passport = ""
	else:
		passport += " " + line.rstrip()
if len(passport) != 0:
	valid = check_fields(passport)
	if valid:
		count_valid += 1
  

print("Number of valid passports: " + str(count_valid))
