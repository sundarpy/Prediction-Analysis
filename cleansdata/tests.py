from django.test import TestCase

# Create your tests here.
import json

with open('dummy.json') as f:
	data = json.load(f)
	print(data)
with open('dummy_one.json', 'w') as f:
	json.dump(data, f, indent=2)