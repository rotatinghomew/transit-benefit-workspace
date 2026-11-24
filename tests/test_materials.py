"""检查资料交接的结构及可追踪性。"""
import unittest
from materials import read_bundle,validate

class MaterialIntegrity(unittest.TestCase):
    def test_protocol_and_references(self):
        counts=validate()
        self.assertTrue(counts)
        self.assertTrue(all(n>0 for n in counts.values()))
    def test_field_explanations(self):
        schema,tables=read_bundle()
        self.assertEqual(set(schema["tables"]),set(tables))
        for table in schema["tables"].values():
            self.assertTrue(table["description"])
            for field in table["fields"].values():self.assertTrue(field["description"])

if __name__=="__main__":unittest.main()
