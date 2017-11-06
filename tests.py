import os
import unittest
from flask import json
from app import app, db, Potion

headers = {"Authorization": "admin"}


class TestCase(unittest.TestCase):
    ############################
        # setup and teardown
    ############################
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ##########################
        # test credentials
    ##########################
    def test_invalid_credentials(self):
        response = self.app.post("/api/v1/potions")
        self.assertEqual(response.status_code, 401)

    ###########################
        # test get and post
    ###########################
    def test_get_all_potions(self):
        potion_1 = Potion("potion_1", "passive", "life")
        potion_2 = Potion("potion_2", "active", "fire")
        potion_3 = Potion("potion_3", "passive", "mana")
        db.session.add(potion_1)
        db.session.add(potion_2)
        db.session.add(potion_3)
        db.session.commit()
        response = self.app.get("/api/v1/potions")
        self.assertEqual(response.status_code, 200)
        for potion in json.loads(response.data):
            self.assertIsNotNone(potion["potion_class"])
            self.assertIsNotNone(potion["potion_name"])
            self.assertIsNotNone(potion["potion_type"])
            self.assertIsNotNone(potion["location"])

    def test_get_potion(self):
        potion_1 = Potion("potion_1", "passive", "life")
        db.session.add(potion_1)
        db.session.commit()
        response = self.app.get("/api/v1/potions/potion_1")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["potion_class"], "life")
        self.assertEqual(data["potion_name"], "potion_1")
        self.assertEqual(data["potion_type"], "passive")
        self.assertEqual(data["location"], "/api/v1/potions/potion_1")

    def test_get_non_existing_potion(self):
        response = self.app.get("/api/v1/potions/1")
        self.assertEqual(response.status_code, 404)

    def test_filter_by_type(self):
        potion_1 = Potion("potion_1", "passive", "mana")
        potion_2 = Potion("potion_2", "passive", "life")
        potion_3 = Potion("potion_3", "active", "poison")
        db.session.add(potion_1)
        db.session.add(potion_2)
        db.session.add(potion_3)
        db.session.commit()
        response = self.app.get("/api/v1/potions?potion_type=passive")
        self.assertEqual(response.status_code, 200)
        for potion in json.loads(response.data):
            self.assertEqual(potion["potion_type"], "passive")

    def test_filter_by_class(self):
        potion_1 = Potion("potion_1", "active", "poison")
        potion_2 = Potion("potion_2", "active", "fire")
        potion_3 = Potion("potion_3", "passive", "mana")
        db.session.add(potion_1)
        db.session.add(potion_2)
        db.session.add(potion_3)
        db.session.commit()
        response = self.app.get("/api/v1/potions?potion_class=fire")
        self.assertEqual(response.status_code, 200)
        for potion in json.loads(response.data):
            self.assertEqual(potion["potion_class"], "fire")

    def test_post_valid_potion(self):
        params = json.dumps(dict(potion_name="potion_1",
                                 potion_type="passive",
                                 potion_class="life"))
        response = self.app.post("/api/v1/potions",
                                 headers=headers,
                                 data=params)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data["potion_class"], "life")
        self.assertEqual(data["potion_name"], "potion_1")
        self.assertEqual(data["potion_type"], "passive")
        self.assertEqual(data["location"], "/api/v1/potions/potion_1")

    ##########################
        # test validations
    ##########################
    def test_post_missing_potion_name(self):
        params = json.dumps(dict(potion_type="passive", potion_class="mana"))
        response = self.app.post("/api/v1/potions",
                                 headers=headers,
                                 data=params)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "potion_name can't be empty")

    def test_post_potion_name_starts_with_underscore(self):
        params = json.dumps(dict(potion_name="_potion_1",
                                 potion_type="passive",
                                 potion_class="life"))
        response = self.app.post("/api/v1/potions",
                                 headers=headers,
                                 data=params)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"],
                         "potion_name cannot start with underscore or dash")

    def test_post_potion_name_starts_with_dash(self):
        params = json.dumps(dict(potion_name="-potion_1",
                                 potion_type="active",
                                 potion_class="fire"))
        response = self.app.post("/api/v1/potions",
                                 headers=headers,
                                 data=params)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"],
                         "potion_name cannot start with underscore or dash")

    def test_post_potion_name_length(self):
        params = json.dumps(dict(potion_name="pot",
                                 potion_type="passive",
                                 potion_class="life"))
        response = self.app.post("/api/v1/potions",
                                 headers=headers,
                                 data=params)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"],
                         "potion_name must be between 4 and 64 characters")

    def test_post_potion_name_ascii(self):
        params = json.dumps(dict(potion_name="po$$ti*n",
                                 potion_type="active",
                                 potion_class="fire"))
        response = self.app.post("/api/v1/potions",
                                 headers=headers,
                                 data=params)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"],
                         "potion_name can only contain alphanumeric " +
                         "ascii characters, underscores, or dashes")

    def test_post_potion_name_unique(self):
        potion_1 = Potion("potion_1", "passive", "mana")
        db.session.add(potion_1)
        db.session.commit()
        params = json.dumps(dict(potion_name="potion_1",
                                 potion_type="passive",
                                 potion_class="mana"))
        response = self.app.post("/api/v1/potions",
                                 headers=headers,
                                 data=params)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "potion_name must be unique")

    def test_post_missing_potion_type(self):
        params = json.dumps(dict(potion_name="potion_1",
                                 potion_class="poison"))
        response = self.app.post("/api/v1/potions",
                                 headers=headers,
                                 data=params)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "potion_type can't be empty")

    def test_post_invalid_potion_type(self):
        params = json.dumps(dict(potion_name="potion_1",
                                 potion_type="hybrid",
                                 potion_class="fire"))
        response = self.app.post("/api/v1/potions",
                                 headers=headers,
                                 data=params)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"],
                         "potion_type must either be 'passive' or 'active', " +
                         "both lowercase")

    def test_post_missing_potion_class(self):
        params = json.dumps(dict(potion_name="potion_1",
                                 potion_type="passive"))
        response = self.app.post("/api/v1/potions",
                                 headers=headers,
                                 data=params)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"], "potion_class can't be empty")

    def test_post_potion_class_based_on_type_passive(self):
        params = json.dumps(dict(potion_name="potion_1",
                                 potion_type="passive",
                                 potion_class="fire"))
        response = self.app.post("/api/v1/potions",
                                 headers=headers,
                                 data=params)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"],
                         "potion_class must either be 'life' or 'mana', " +
                         "both lowercase")

    def test_post_potion_class_based_on_type_active(self):
        params = json.dumps(dict(potion_name="potion_1",
                                 potion_type="active",
                                 potion_class="life"))
        response = self.app.post("/api/v1/potions",
                                 headers=headers,
                                 data=params)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["error"],
                         "potion_class must either be 'fire' or 'poison', " +
                         "both lowercase")


if __name__ == "__main__":
    unittest.main()
