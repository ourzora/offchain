# flake8: noqa: E501

import pytest


@pytest.fixture
def raw_crypto_coven_metadata():  # type: ignore[no-untyped-def]
    return {
        "description": "You are a WITCH of the highest order. You are borne of chaos that gives the night shape. Your magic spawns from primordial darkness. You are called oracle by those wise enough to listen. ALL THEOLOGY STEMS FROM THE TERROR OF THE FIRMAMENT!",
        "external_url": "https://www.cryptocoven.xyz/witches/1",
        "image": "https://cryptocoven.s3.amazonaws.com/nyx.png",
        "name": "nyx",
        "background_color": "",
        "attributes": [
            {"trait_type": "Background", "value": "Sepia"},
            {"trait_type": "Skin Tone", "value": "Dawn"},
            {"trait_type": "Body Shape", "value": "Lithe"},
            {"trait_type": "Top", "value": "Sheer Top (Black)"},
            {"trait_type": "Eyebrows", "value": "Medium Flat (Black)"},
            {"trait_type": "Eye Style", "value": "Nyx"},
            {"trait_type": "Eye Color", "value": "Cloud"},
            {"trait_type": "Mouth", "value": "Nyx (Mocha)"},
            {"trait_type": "Hair (Front)", "value": "Nyx"},
            {"trait_type": "Hair (Back)", "value": "Nyx Long"},
            {"trait_type": "Hair Color", "value": "Steel"},
            {"trait_type": "Hat", "value": "Witch (Black)"},
            {"trait_type": "Necklace", "value": "Moon Necklace (Silver)"},
            {"trait_type": "Archetype of Power", "value": "Witch of Woe"},
            {"trait_type": "Sun Sign", "value": "Taurus"},
            {"trait_type": "Moon Sign", "value": "Aquarius"},
            {"trait_type": "Rising Sign", "value": "Capricorn"},
            {"display_type": "number", "trait_type": "Will", "value": 9},
            {"display_type": "number", "trait_type": "Wisdom", "value": 9},
            {"display_type": "number", "trait_type": "Wonder", "value": 9},
            {"display_type": "number", "trait_type": "Woe", "value": 10},
            {"display_type": "number", "trait_type": "Wit", "value": 9},
            {"display_type": "number", "trait_type": "Wiles", "value": 9},
        ],
        "coven": {
            "id": 1,
            "name": "nyx",
            "type": "Witch of Woe",
            "description": {
                "intro": "You are a WITCH of the highest order.",
                "hobby": "You are borne of chaos that gives the night shape.",
                "magic": "Your magic spawns from primordial darkness.",
                "typeSpecific": "You are called oracle by those wise enough to listen.",
                "exclamation": "ALL THEOLOGY STEMS FROM THE TERROR OF THE FIRMAMENT!",
            },
            "skills": {
                "will": 9,
                "wisdom": 9,
                "wonder": 9,
                "woe": 10,
                "wit": 9,
                "wiles": 9,
            },
            "birthChart": {
                "sun": "taurus",
                "moon": "aquarius",
                "rising": "capricorn",
            },
            "styles": [
                {
                    "attribute": "background",
                    "name": "solid",
                    "color": "sepia",
                    "fullName": "background_solid_sepia",
                },
                {
                    "attribute": "base",
                    "name": "lithe",
                    "color": "dawn",
                    "fullName": "base_lithe_dawn",
                },
                {
                    "attribute": "body-under",
                    "name": "sheer-top",
                    "color": "black",
                    "fullName": "body-under_sheer-top_black",
                },
                {
                    "attribute": "eyebrows",
                    "name": "medium-flat",
                    "color": "black",
                    "fullName": "eyebrows_medium-flat_black",
                },
                {
                    "attribute": "eyes",
                    "name": "nyx",
                    "color": "cloud",
                    "fullName": "eyes_nyx_cloud",
                },
                {
                    "attribute": "mouth",
                    "name": "nyx",
                    "color": "mocha",
                    "fullName": "mouth_nyx_mocha",
                },
                {
                    "attribute": "hair-back",
                    "name": "nyx",
                    "color": "steel",
                    "fullName": "hair-back_nyx_steel",
                },
                {
                    "attribute": "hair-bangs",
                    "name": "nyx",
                    "color": "steel",
                    "fullName": "hair-bangs_nyx_steel",
                },
                {
                    "attribute": "hat-back",
                    "name": "witch",
                    "color": "black",
                    "fullName": "hat-back_witch_black",
                },
                {
                    "attribute": "hat-front",
                    "name": "witch",
                    "color": "black",
                    "fullName": "hat-front_witch_black",
                },
                {
                    "attribute": "necklace",
                    "name": "moon-necklace",
                    "color": "silver",
                    "fullName": "necklace_moon-necklace_silver",
                },
            ],
            "hash": "nyx",
        },
    }
