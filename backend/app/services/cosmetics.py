"""The cosmetics catalog: avatar items by slot, profile frames, titles, page background effects and pet gear.

game.SHOP is built from this plus the older items (accents, themes). The browser draws every item from its
value (website/src/theme.js for avatars and frames, effects.js for backgrounds, pets.js for pet gear), so a new
item needs its art there too. Rarity is shown in the locker and sets the price band.
"""

# value: (name, price, rarity, about). A price of 0 means it's free for everyone.
RARITY = ("common", "rare", "epic", "legendary")

AVATAR = {
    "hat": [
        ("beanie", "Beanie", 0, "common", "Warm, red, and free."),
        ("cap", "Backward cap", 90, "common", "Brim to the back, like you mean it."),
        ("pencil", "Pencil behind the ear", 60, "common", "Ready for the next question."),
        ("headphones", "Headphones", 100, "common", "Focus music on."),
        ("gradcap", "Graduation cap", 150, "rare", "Dress for the score you want."),
        ("catears", "Cat ears", 220, "rare", "Curious about every problem."),
        ("flowers", "Flower crown", 260, "rare", "Fresh from the study garden."),
        ("tophat", "Top hat", 320, "rare", "Very formal. Very fancy."),
        ("pirate", "Pirate hat", 340, "rare", "Arr, x marks the solution."),
        ("propeller", "Propeller cap", 420, "epic", "It spins when you think hard."),
        ("viking", "Viking helmet", 480, "epic", "For storming hard Module 2s."),
        ("wizard", "Wizard hat", 650, "epic", "For Desmos sorcery."),
        ("halo", "Glowing halo", 750, "epic", "Never missed a streak day. Probably."),
        ("astronaut", "Astronaut helmet", 1100, "legendary", "One small step for your score."),
        ("crown", "Crown", 1400, "legendary", "Rule the leaderboard."),
    ],
    "face": [
        ("glasses", "Round glasses", 0, "common", "Classic and free."),
        ("sunglasses", "Sunglasses", 80, "common", "Too cool for careless mistakes."),
        ("monocle", "Monocle", 240, "rare", "Inspect every answer choice."),
        ("starshades", "Star shades", 300, "rare", "You're the star of this study session."),
        ("mask", "Hero mask", 380, "epic", "Secret identity: top scorer."),
        ("visor", "Glow visor", 800, "epic", "Sees the graph before you draw it."),
        ("scanner", "Scanner visor", 1300, "legendary", "A red light sweeps for mistakes."),
    ],
    "outfit": [
        ("tee", "T-shirt", 0, "common", "The basics, in your shirt color."),
        ("hoodie", "Hoodie", 120, "common", "Comfy for long sessions."),
        ("vest", "Sweater vest", 160, "common", "Tidy and studious."),
        ("jersey", "Number 1 jersey", 220, "rare", "Your name on the leaderboard, your number on your chest."),
        ("varsity", "Varsity jacket", 300, "rare", "Letter in Math."),
        ("labcoat", "Lab coat", 280, "rare", "For experiments with x."),
        ("suit", "Suit and tie", 380, "epic", "Interview-ready."),
        ("cape", "Hero cape", 700, "epic", "It flutters a little."),
        ("spacesuit", "Space suit", 1000, "legendary", "Matches the helmet."),
        ("armor", "Knight armor", 1500, "legendary", "Shines when the light hits it."),
    ],
    "backdrop": [
        ("solid", "Solid color", 0, "common", "Your background color, plain."),
        ("graph", "Graph paper", 100, "common", "A grid behind you."),
        ("confetti", "Confetti", 200, "rare", "Every day is a celebration."),
        ("chalkboard", "Chalkboard", 180, "rare", "Equations in chalk."),
        ("waves", "Ocean waves", 250, "rare", "Calm water."),
        ("sunset", "Sunset", 320, "rare", "Bands of evening color."),
        ("stars", "Night sky", 420, "epic", "Twinkling stars."),
        ("circuit", "Circuit board", 520, "epic", "Wired for math."),
        ("galaxy", "Galaxy", 950, "epic", "A ringed planet and far-off stars."),
        ("fire", "Flames", 1500, "legendary", "Your streak, on fire."),
    ],
}
FREE_AVATAR = {slot: {v for v, _, p, _, _ in items if p == 0} for slot, items in AVATAR.items()}
DEFAULT_AVATAR = {"hat": "none", "face": "none", "outfit": "tee", "backdrop": "solid"}

FRAMES = [
    ("pixel", "Pixel frame", 180, "rare", "Stepped like an old game."),
    ("neon", "Neon ring", 420, "epic", "A soft glow in your accent color."),
    ("laurel", "Laurel ring", 520, "epic", "For champions."),
    ("prism", "Prism ring", 650, "epic", "Six bright segments."),
    ("orbit", "Orbit", 1000, "legendary", "A little moon circles your picture."),
    ("blaze", "Blaze", 1600, "legendary", "A ring that flickers like fire."),
]

TITLES = [
    ("Desmos Wizard", 150, "common"), ("Comeback Kid", 150, "common"), ("Graph Goblin", 180, "rare"),
    ("Sine Language", 200, "rare"), ("Ratio Royalty", 220, "rare"), ("Night Owl Scholar", 220, "rare"),
    ("Streak Machine", 350, "epic"), ("Module 2 Menace", 400, "epic"), ("Perfect 800 Energy", 900, "legendary"),
]

# Page background effects (Settings > Appearance > Background). Free ones need no purchase.
EFFECTS = [
    ("none", "None", 0, "common", "A plain background."),
    ("ripple", "Ripples", 0, "common", "Dots that ripple out wherever you click."),
    ("dots", "Still dots", 0, "common", "A quiet dot grid that doesn't move."),
    ("snow", "Snowfall", 200, "rare", "Slow, gentle snow."),
    ("constellation", "Constellation", 260, "rare", "Drifting stars that link up near your cursor."),
    ("symbols", "Floating symbols", 320, "rare", "π, Σ and √ drift slowly upward."),
    ("waves", "Sine waves", 450, "epic", "Layered waves rolling across the page."),
    ("fireflies", "Fireflies", 520, "epic", "Warm lights that wander and blink."),
    ("warp", "Star warp", 900, "legendary", "Stars rushing past, very slowly."),
    # Interactive: these follow your pointer (or finger) and react when you click or tap.
    ("springy", "Springy dots", 300, "rare", "Interactive. Dots bend away from your cursor and spring back. Click to push them."),
    ("pencil", "Pencil trail", 340, "rare", "Interactive. Your cursor leaves a graphite line that slowly fades."),
    ("magnet", "Iron filings", 380, "rare", "Interactive. Little lines turn to point at your cursor. Click to send a pulse."),
    ("graphpaper", "Graph paper", 480, "epic", "Interactive. The grid lights up around your cursor and shows its coordinates. Click to plot a point."),
    ("bubbles", "Number bubbles", 560, "epic", "Interactive. Click to blow bubbles. Move over one to pop it."),
    ("gravity", "Gravity well", 950, "legendary", "Interactive. Specks fall toward your cursor and swing around it. Click to fling them away."),
]
FREE_EFFECTS = {v for v, _, p, _, _ in EFFECTS if p == 0}

PETGEAR = [
    ("bow", "Bow", 80, "common", "A neat little bow."),
    ("party", "Party hat", 120, "common", "Every level-up is a party."),
    ("scarf", "Scarf", 160, "rare", "Cozy."),
    ("shades", "Tiny shades", 200, "rare", "Pets can be cool too."),
    ("tinycrown", "Tiny crown", 600, "epic", "Royalty."),
    ("wings", "Sparkle wings", 1200, "legendary", "Flutters when your pet is happy."),
]


def shop_items():
    """The new items as shop rows (free avatar items aren't sold)."""
    out = []
    for slot, items in AVATAR.items():
        for v, name, price, rarity, about in items:
            if price:
                out.append({"key": f"avatar:{v}", "kind": "avatar", "slot": slot, "value": v, "name": name, "price": price,
                            "rarity": rarity, "about": about})
    for v, name, price, rarity, about in FRAMES:
        out.append({"key": f"frame:{v}", "kind": "frame", "value": v, "name": name, "price": price, "rarity": rarity, "about": about})
    for t, price, rarity in TITLES:
        key = "title:" + t.lower().replace(" ", "-")
        out.append({"key": key, "kind": "title", "value": t, "name": t, "price": price, "rarity": rarity, "about": "A title under your name."})
    for v, name, price, rarity, about in EFFECTS:
        if price:
            out.append({"key": f"effect:{v}", "kind": "effect", "value": v, "name": name, "price": price, "rarity": rarity, "about": about})
    for v, name, price, rarity, about in PETGEAR:
        out.append({"key": f"petgear:{v}", "kind": "petgear", "value": v, "name": name, "price": price, "rarity": rarity, "about": about})
    return out


def rarity_for(price):
    return "common" if price < 150 else "rare" if price < 400 else "epic" if price < 1000 else "legendary"


def slot_of(value):
    return next((slot for slot, items in AVATAR.items() if any(v == value for v, *_ in items)), None)
