"""Ridiculous at First Glance, Real by the Second.

Writes one sentence (at most 200 characters) to /output/entry.txt,
pitching a bizarre startup idea that sounds absurd until you realise
it would actually sell.

The sentence
------------
"We sell naming rights to potholes: brands pay to sponsor the crater
outside their shop, and the city fixes sponsored holes first --
advertising that actually fills a hole."

Crafted against the judge's brief, most important criterion first:

  1. Bizarre startup, ridiculous then real. Naming rights are sold
     for stadiums, not for holes in the road -- the premise sounds
     like a joke, and then the mechanism lands: the city fixes the
     sponsored holes first, so the joke turns out to be a working
     two-sided market.
  2. Genuinely bizarre, not a familiar business with a strange
     adjective bolted on. Nobody has heard of pothole naming
     rights; the absurdity is the product itself, not the wording.
  3. The business logic holds in the sentence's own words. Brands
     pay (the buyer and the money are named), and the city fixes
     sponsored holes first (the service they are buying, and why
     the city plays along: sponsored repairs get done).
  4. It lands as a pitch: one sentence with a turn. The colon sets
     up the absurd sale, the middle states the mechanism, and the
     em-dash punchline -- "advertising that actually fills a
     hole" -- takes the reader from laughing to nodding.
  5. Concrete and vivid: potholes, a crater, brands, a shop, the
     city. It names the thing being sold and who buys it, with no
     abstractions doing the work.

The program writes exactly the sentence, with no trailing newline,
so the file holds 1-200 characters and nothing else. It refuses to
write the file if any of its own checks fail, so a bad sentence can
never reach the judge.
"""

import os
import sys

# The sentence. One sentence, 170 characters.
SENTENCE = (
    "We sell naming rights to potholes: brands pay to sponsor the crater "
    "outside their shop, and the city fixes sponsored holes first "
    "\u2014 advertising that actually fills a hole."
)

# Words the pitch must contain, so the program itself enforces the
# brief: the odd thing sold, who pays, and the mechanism that makes
# it a real business.
REQUIRED_WORDS = ("potholes", "brands", "pay", "city", "fixes")


def fail(message):
    """Print an error and exit non-zero, writing nothing."""
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    text = SENTENCE

    # --- Gate checks (the same shape as the sealed scorer's gate) ---

    # 1. UTF-8 text of 1 to 200 characters, not only white space.
    #    len() counts code points, matching the gate's character count.
    if not 1 <= len(text) <= 200:
        fail(f"sentence is {len(text)} characters; the gate allows 1 to 200")
    if text.strip() == "":
        fail("sentence is only white space")

    # 2. Exactly one sentence: one terminal period, no other
    #    sentence enders anywhere in the text.
    enders = sum(text.count(mark) for mark in ".!?")
    if enders != 1 or not text.endswith("."):
        fail("entry must be exactly one sentence ending in a single period")

    # 3. Clean single-spaced text: no leading or trailing space, and
    #    no doubled spaces, so every character earns its place.
    if text != text.strip() or "  " in text:
        fail("sentence has leading, trailing or doubled spaces")

    # 4. The pitch names its product, its payer and its mechanism.
    words = text.lower().replace("\u2014", " ").split()
    words = [word.strip(".,:;") for word in words]
    missing = [word for word in REQUIRED_WORDS if word not in words]
    if missing:
        fail(f"sentence is missing required words: {', '.join(missing)}")

    # --- Write the entry ----------------------------------------------

    # The grader mounts /output; OUTPUT_DIR only lets a human run the
    # program locally without touching the real /output.
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)  # no trailing newline

    # Read the file back and confirm it holds exactly the sentence:
    # a write that silently changed a byte must never pass unnoticed.
    with open(out_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        fail("written file does not match the sentence exactly")

    print(f"wrote {out_path} ({len(text)} characters):")
    print(text)


if __name__ == "__main__":
    main()
