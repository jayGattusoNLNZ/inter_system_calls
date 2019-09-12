from bs4 import BeautifulSoup as bs
from pydnz import Dnz
from credentials import API_KEY
dnz = Dnz(API_KEY)

ies = []

def get_ies(mms_id, i):
	ies = []
	results = dnz.search(mms_id)
	if results.result_count == 1:
		print (f"{i}/{len(refs)} {mms_id} - Hit")
		for identifier in results.records[0]['dc_identifier']:
			if identifier.startswith("ndha"):
				ies.append(identifier.replace("ndha:", ""))

	elif results.result_count == 0:
		print (f"{i}/{len(refs)} {mms_id} - Miss")

	else:
		print (f"{i}/{len(refs)} {mms_id} - Hits ({results.result_count})")
		for record in results.records:
			for identifier in record['dc_identifier']:
				if identifier.startswith("ndha"):
					ies.append(identifier.replace("ndha:", ""))
	return ies

# file path to ead xml file
ead_doc = ""

with open(ead_doc, encoding="utf8") as data:
	ead = bs(data.read(), "lxml") 

refs = ead.find_all("unitid", {"label":"Reference Number"})

for i, ref in enumerate(refs, 1):
	new_ies = get_ies(ref.text, i)
	# print (new_ies)
	for ie in new_ies:
		if ie not in ies:
			ies.append(ie)

	print (f"Caught: {len(ies)} IEs")

for ie in ies:
	print (ie)

with open("ies.txt", "w") as data:
	data.write("\n".join(ies))