
import sys

class Variants(object):
	def __init__(self):
		pass

	def __del__(self):
		pass

	def createVariantsFile(self, target):
		print("create variants.yml")
		f = open("variants.yml", "w")
		f.write("variants:\n")
		match target: 
			case "aurora":
				f.write(f"  - \"-s board.product=aurora\"\n")
			case "kp6tab":
				f.write(f"  - \"-s board.product=kp6000 -s emv=True\"\n")
			case "taipan":
				f.write(f"  - \"-s board.product=adept -s emv=True\"\n")
				f.write(f"  - \"-s board.product=adept\"\n")
				f.write(f"  - \"-s board.product=rugged -s emv=True\"\n")
				f.write(f"  - \"-s board.product=rugged\"\n")
			case "viper2":
				f.write(f"  - \"-s board.product=tp5700\"\n")
				f.write(f"  - \"-s board.product=tp5800\"\n")
				f.write(f"  - \"-s board.product=cp6500 -s emv=True\"\n")
				f.write(f"  - \"-s board.product=cp6500\"\n")
			case "cobra2":
				f.write(f"  - \"-s board.product=cr6000\"\n")
			case _:
				f.write(f"  - \"\"\n")
		f.close()
