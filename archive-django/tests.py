import unittest, datetime

class TestAggregator(unittest.TestCase):
    def setUp(self):
        try:
            import aggregator
        except:
            print('aggregator.py not found')
        self.ag = aggregator.Aggregator()
    def test_zip_validity(self):
        zip_code = 1
        result = self.ag.valid_zip(zip_code)
        expected = False
        self.assertEqual(result, expected)
        zip_code = 22201
        result = self.ag.valid_zip(zip_code)
        expected = False
        self.assertEqual(result, expected)
        zip_code = '1'
        result = self.ag.valid_zip(zip_code)
        expected = False
        self.assertEqual(result, expected)
        zip_code = '22201'
        result = self.ag.valid_zip(zip_code)
        expected = True
        self.assertEqual(result, expected)
    def test_pollen(self):
        result = self.ag.pollen_api(11111)
        expected = 'Invalid zip code'
        self.assertEqual(result, expected)
        result = self.ag.pollen_api('22201')
        expected = {'zip code': '22201',
					'pollen rating': 0,
					'access date': 0}
        self.assertEqual(len(result), len(expected))
        self.assertEqual(result.keys(), expected.keys())
        #print(type(result['access date']))
        #self.assertIsInstance(result['pollen rating'], datetime.datetime)
    def test_walkability(self):
        result = self.ag.walkability_api(11111)
        expected = 'Invalid zip code'
        self.assertEqual(result, expected)
        result = self.ag.walkability_api('22201')
        expected = {'zip code': '22201',
					'walkability rating': 0,
					'access date': 0}
        self.assertEqual(len(result), len(expected))
        self.assertEqual(result.keys(), expected.keys())
    def test_zip_to_county(self):
        result = self.ag.get_zip_to_county(11111)
        expected = 'Invalid zip code'
        self.assertEqual(result, expected)
        result = self.ag.get_zip_to_county('22201')
        expected = 'Arlington County, VA'
        self.assertEqual(result, expected)

if __name__ == '__main__':
	unittest.main()
