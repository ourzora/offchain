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


@pytest.fixture
def mock_video_rawdata():  # type: ignore[no-untyped-def]
    return {
        "name": "🤑👉😍👑💍",
        "description": "Yats 🖖 are emoji usernames that become your universal Internet identity 🗿, website URL 💻, payment address 🤑, and more. By owning a Yat – let’s say 🤑👉😍👑💍 – it’s yours forever. Get inspired and join our amazingly creative Yat Community at Y.at.",
        "image": "https://y.at/viz/money-mouth/money-mouth.point.heart-eyes.crown.ring-2ba3b7.png",
        "thumbnail_image": "https://y.at/viz/money-mouth/money-mouth.point.heart-eyes.crown.ring-2ba3b7.png",
        "animation_url": "https://y.at/viz/money-mouth/money-mouth.point.heart-eyes.crown.ring-2ba3b7.mp4",
        "icon_url": "",
        "token_id": "",
        "owner_name": "",
        "external_link": "https://y.at/%F0%9F%A4%91%F0%9F%91%89%F0%9F%98%8D%F0%9F%91%91%F0%9F%92%8D",
        "attributes": [
            {"trait_type": "Length", "value": "Five-Emoji"},
            {"trait_type": "Rhythm Score", "value": "0-25"},
            {"trait_type": "Generation", "value": "Gen One"},
            {"trait_type": "Visualizer Theme", "value": "ribbons"},
        ],
    }


@pytest.fixture
def mock_image_rawdata():  # type: ignore[no-untyped-def]
    return {
        "description": "The tax man came, and old gregson was left with nothing. They took it all, his house, his possessions, every ounce of savings in his bank account..and most of all, his beloved farm with the many animals he cherished and adored…”. Gregson wanted to end it all, instead by some miracle he ended up on the mysterious continent of crypto befriending hammond the punk, michelangelo the ape & kafka the cat changing their lives forever. James di martino turns reality into fiction in this Orwellian journey of trust, betrayal and the limitless power of ethereum.",
        "external_url": "",
        "image": "https://ipfs.io/ipfs/QmQaYaf3Q2oCBaUfUvV6mBP58EjbUTbMk6dC1o4YGjeWCo",
        "name": "CryptoFarm",
    }
