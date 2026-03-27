"""
PITCHIQ LEAD SCORING ENGINE
=============================
Adapted from Smart Lead Hunter scoring system.
Works for BOTH new opening hotels AND existing hotels.

SCORING BREAKDOWN:
- Brand Tier:        25 pts — quality + uniform variety
- Location:          15 pts — US/Caribbean priority markets  
- Urgency:           25 pts — new opening date OR hiring/renovation signals
- Staff/Room Size:   15 pts — order size potential
- Contact Authority: 12 pts — decision maker level
- Outreach Angle:     8 pts — strength of personalization hook

TOTAL: 100 pts

SCORE TIERS:
- HOT:  80-100 — contact immediately
- WARM: 60-79  — strong lead, prioritize
- COOL: 40-59  — worth pursuing
- COLD: 0-39   — low priority
"""

import re
from typing import Tuple

# ═══════════════════════════════════════════════
# BRAND TIER LISTS (adapted from Smart Lead Hunter)
# ═══════════════════════════════════════════════

TIER1_ULTRA_LUXURY = [
    "aman", "rosewood", "four seasons", "mandarin oriental",
    "peninsula", "raffles", "bulgari", "bvlgari", "capella",
    "one&only", "one and only", "belmond", "oberoi", "six senses",
    "banyan tree", "como hotels", "faena", "setai", "the carlyle",
    "the breakers", "montage", "auberge", "baccarat hotel",
    "dorchester collection", "oetker collection", "viceroy",
    "small luxury hotels", "leading hotels of the world",
]

TIER2_LUXURY = [
    "ritz-carlton", "ritz carlton", "st. regis", "st regis",
    "waldorf astoria", "waldorf-astoria", "conrad", "park hyatt",
    "w hotel", "w hotels", "edition", "luxury collection",
    "the luxury collection", "loews", "kimpton", "thompson",
    "1 hotel", "1hotels", "equinox hotel", "soho house",
    "fontainebleau", "acqualina", "eden roc", "boca raton resort",
    "the biltmore", "wynn", "bellagio", "mgm grand", "caesars palace",
    "grand hyatt", "andaz", "aloft", "intercontinental",
    "regent", "langham", "nobu hotel", "nomad",
]

TIER3_UPSCALE = [
    "marriott", "hilton", "hyatt", "westin", "sheraton",
    "renaissance", "le meridien", "autograph collection",
    "tribute portfolio", "delta hotels", "curio collection",
    "tapestry collection", "doubletree", "embassy suites",
    "omni", "loews", "kimpton", "ac hotels", "moxy",
    "hotel indigo", "crowne plaza", "even hotels",
    "joie de vivre", "thompson hotels", "sage hospitality",
    "dream hotel", "sls hotel", "standard hotel", "the standard",
    "ace hotel", "proper hotel", "graduate hotels",
]

TIER4_MIDSCALE = [
    "courtyard", "springhill suites", "fairfield", "residence inn",
    "towneplace suites", "four points", "aloft", "element",
    "hampton inn", "hilton garden inn", "homewood suites",
    "home2 suites", "hyatt place", "hyatt house",
    "holiday inn", "holiday inn express", "staybridge",
    "candlewood", "avid hotels", "even hotels",
]

TIER5_BUDGET = [
    "motel 6", "super 8", "days inn", "travelodge",
    "red roof", "econo lodge", "americas best value",
    "microtel", "knights inn", "howard johnson",
    "quality inn", "comfort inn", "sleep inn", "rodeway",
]

# ═══════════════════════════════════════════════
# PRIORITY MARKETS (adapted from Smart Lead Hunter)
# ═══════════════════════════════════════════════

TIER1_MARKETS = [
    "miami", "miami beach", "south beach", "brickell",
    "new york", "manhattan", "brooklyn",
    "los angeles", "beverly hills", "santa monica",
    "las vegas", "orlando", "chicago",
    "san francisco", "napa", "sonoma",
    "honolulu", "maui", "waikiki",
    # Caribbean
    "bahamas", "nassau", "paradise island",
    "turks and caicos", "providenciales",
    "st. barthelemy", "st barts",
    "anguilla", "antigua", "barbados",
    "jamaica", "montego bay", "negril",
    "dominican republic", "punta cana", "cap cana",
    "puerto rico", "san juan", "dorado",
    "st. lucia", "st lucia",
    "cayman islands", "grand cayman",
    "aruba", "curacao", "bonaire",
    "usvi", "st. thomas", "st. john",
    "bvi", "tortola", "virgin gorda",
]

TIER2_MARKETS = [
    "fort lauderdale", "palm beach", "naples", "sarasota",
    "key west", "florida keys", "tampa", "st. pete",
    "scottsdale", "sedona", "phoenix",
    "nashville", "austin", "dallas", "houston",
    "atlanta", "charlotte", "raleigh",
    "washington dc", "baltimore", "philadelphia",
    "boston", "portland", "seattle",
    "denver", "aspen", "vail", "telluride",
    "new orleans", "savannah", "charleston",
    "san diego", "monterey", "carmel",
    "greenwich", "hamptons",
]

# ═══════════════════════════════════════════════
# HELPER: BRAND MATCHING (word-boundary aware)
# Inspired by Smart Lead Hunter M-07 fix
# ═══════════════════════════════════════════════

_SHORT_BRAND_THRESHOLD = 4
_brand_patterns = {}

def _brand_matches(brand: str, text: str) -> bool:
    """Match brand name with word-boundary awareness for short names"""
    stripped = brand.strip()
    if len(stripped) <= _SHORT_BRAND_THRESHOLD:
        if stripped not in _brand_patterns:
            escaped = re.escape(stripped)
            _brand_patterns[stripped] = re.compile(
                r"\b" + escaped + r"\b", re.IGNORECASE
            )
        return bool(_brand_patterns[stripped].search(text))
    else:
        return stripped.lower() in text.lower()


# ═══════════════════════════════════════════════
# 1. BRAND TIER SCORING (25 pts max)
# ═══════════════════════════════════════════════

def get_brand_score(hotel_name: str) -> Tuple[int, str, int]:
    """
    Returns (tier_number, tier_name, points)
    """
    name_lower = hotel_name.lower()

    for brand in TIER1_ULTRA_LUXURY:
        if _brand_matches(brand, name_lower):
            return (1, "Ultra Luxury", 25)

    for brand in TIER2_LUXURY:
        if _brand_matches(brand, name_lower):
            return (2, "Luxury", 20)

    for brand in TIER3_UPSCALE:
        if _brand_matches(brand, name_lower):
            return (3, "Upscale", 14)

    for brand in TIER4_MIDSCALE:
        if _brand_matches(brand, name_lower):
            return (4, "Midscale", 7)

    for brand in TIER5_BUDGET:
        if _brand_matches(brand, name_lower):
            return (5, "Budget", 0)

    # Independent / boutique hotel — still valuable
    return (3, "Independent/Boutique", 12)


def should_skip_brand(hotel_name: str) -> bool:
    """Skip budget brands — not worth pursuing"""
    tier_num, _, _ = get_brand_score(hotel_name)
    return tier_num == 5


# ═══════════════════════════════════════════════
# 2. LOCATION SCORING (15 pts max)
# ═══════════════════════════════════════════════

def get_location_score(hotel_location: str) -> Tuple[int, str]:
    """
    Returns (points, tier_name)
    """
    if not hotel_location:
        return (8, "Unknown Location")

    location_lower = hotel_location.lower()

    for market in TIER1_MARKETS:
        if market.lower() in location_lower:
            return (15, f"Tier 1 Market — {market}")

    for market in TIER2_MARKETS:
        if market.lower() in location_lower:
            return (10, f"Tier 2 Market — {market}")

    # US but not a priority market
    us_indicators = ["fl", "ny", "ca", "tx", "nv", "il", "ga", "nc",
                     "florida", "new york", "california", "texas",
                     "nevada", "illinois", "georgia", "usa", "united states"]
    if any(indicator in location_lower for indicator in us_indicators):
        return (6, "US — Non-Priority Market")

    # Caribbean not in tier 1
    caribbean_indicators = ["caribbean", "island", "resort"]
    if any(indicator in location_lower for indicator in caribbean_indicators):
        return (8, "Caribbean")

    return (3, "International/Unknown")

# ═══════════════════════════════════════════════
# 3. URGENCY SCORING (25 pts max)
# Works for BOTH new openings AND existing hotels
# ═══════════════════════════════════════════════

def get_urgency_score(
    outreach_angle: str,
    hiring_signals: list,
    opening_date: str = None,
) -> Tuple[int, str]:
    """
    Returns (points, tier_name)
    New opening → score by opening date proximity
    Existing hotel → score by hiring/renovation/expansion signals
    """
    angle_lower = (outreach_angle or "").lower()
    hiring_str = " ".join(hiring_signals or []).lower()

    # ── NEW OPENING PATH ──
    if opening_date:
        try:
            from datetime import datetime
            open_dt = datetime.strptime(opening_date, "%Y-%m-%d")
            days_until = (open_dt - datetime.now()).days

            if days_until <= 90:
                return (25, "Opening within 90 days — URGENT")
            elif days_until <= 180:
                return (20, "Opening within 6 months — HOT")
            elif days_until <= 365:
                return (14, "Opening within 1 year — WARM")
            elif days_until <= 730:
                return (8, "Opening within 2 years — COOL")
            else:
                return (4, "Opening 2+ years out — COLD")
        except Exception:
            pass

    # ── EXISTING HOTEL PATH ──
    # Renovation signals (highest urgency — need new uniforms now)
    if any(word in angle_lower for word in ["renovation", "rebrand", "remodel", "refresh"]):
        return (25, "Renovation — Uniform refresh needed NOW")

    # Expansion signals
    if any(word in angle_lower for word in ["expansion", "new wing", "new tower", "opening"]):
        return (22, "Expansion — Additional uniforms needed")

    # Major hiring surge
    if hiring_signals:
        if any(num in hiring_str for num in ["100+", "200+", "300+", "400+", "500+"]):
            return (22, "Major hiring surge — 100+ positions")
        elif any(num in hiring_str for num in ["50+", "60+", "70+", "80+", "90+"]):
            return (18, "Strong hiring — 50+ positions")
        elif any(num in hiring_str for num in ["20+", "30+", "40+"]):
            return (12, "Moderate hiring — 20+ positions")
        elif len(hiring_signals) > 0:
            return (8, "Active hiring detected")

    # Award recognition (good moment to reach out)
    if any(word in angle_lower for word in ["award", "recognition", "best hotel", "ranked"]):
        return (10, "Award recognition — premium image focus")

    # Staff challenges
    if any(word in angle_lower for word in ["turnover", "challenge", "staff shortage"]):
        return (14, "Staff challenges — uniform solution needed")

    return (5, "No strong urgency signal")


# ═══════════════════════════════════════════════
# 4. STAFF/ROOM SIZE SCORING (15 pts max)
# ═══════════════════════════════════════════════

def get_size_score(
    staff_estimate: str,
    hiring_signals: list
) -> Tuple[int, str]:
    """
    Returns (points, tier_name)
    Estimates staff size from available data
    """
    hiring_str = " ".join(hiring_signals or []).lower()

    # Try to extract staff estimate
    try:
        staff = int(str(staff_estimate).replace(",", "").strip())
        if staff >= 500:
            return (15, f"Large property — {staff}+ staff")
        elif staff >= 200:
            return (12, f"Mid-large property — {staff}+ staff")
        elif staff >= 100:
            return (8, f"Mid property — {staff}+ staff")
        elif staff >= 50:
            return (5, f"Small-mid property — {staff}+ staff")
        else:
            return (3, f"Small property — {staff}+ staff")
    except Exception:
        pass

    # Estimate from hiring signals
    for num in ["500+", "400+", "300+", "200+"]:
        if num in hiring_str:
            return (15, f"Large property — {num} hiring")
    for num in ["100+", "150+"]:
        if num in hiring_str:
            return (12, f"Mid-large property — {num} hiring")
    for num in ["50+", "60+", "70+", "80+", "90+"]:
        if num in hiring_str:
            return (8, f"Mid property — {num} hiring")

    return (6, "Size unknown — estimated mid")


# ═══════════════════════════════════════════════
# 5. CONTACT AUTHORITY SCORING (12 pts max)
# ═══════════════════════════════════════════════

def get_contact_score(
    contact_title: str,
    contact_email: str = None,
    decision_authority: str = None
) -> Tuple[int, str]:
    """
    Returns (points, tier_name)
    """
    title_lower = (contact_title or "").lower()
    points = 0
    tier = ""

    # Title scoring (8 pts max)
    if any(word in title_lower for word in [
        "owner", "ceo", "president", "chief executive"
    ]):
        points += 8
        tier = "Owner/C-Suite"
    elif any(word in title_lower for word in [
        "general manager", "gm", "managing director",
        "vp", "vice president", "director of operations"
    ]):
        points += 7
        tier = "General Manager/VP"
    elif any(word in title_lower for word in [
        "director", "head of", "chief"
    ]):
        points += 5
        tier = "Director Level"
    elif any(word in title_lower for word in [
        "manager", "supervisor", "coordinator"
    ]):
        points += 3
        tier = "Manager Level"
    else:
        points += 1
        tier = "Staff Level"

    # Email bonus (4 pts)
    if contact_email:
        points += 4
        tier += " + Email"

    return (min(points, 12), tier)


# ═══════════════════════════════════════════════
# 6. OUTREACH ANGLE SCORING (8 pts max)
# ═══════════════════════════════════════════════

def get_angle_score(
    outreach_angle: str,
    personalization_hook: str
) -> Tuple[int, str]:
    """
    Returns (points, tier_name)
    Stronger angle = higher score
    """
    angle_lower = (outreach_angle or "").lower()
    hook_lower = (personalization_hook or "").lower()

    # Specific dollar amount or number = very strong hook
    if any(char.isdigit() for char in hook_lower) and len(hook_lower) > 20:
        return (8, "Highly specific hook with numbers")

    if any(word in angle_lower for word in [
        "renovation", "expansion", "rebranding", "new opening"
    ]):
        return (7, "Strong event-based angle")

    if any(word in angle_lower for word in [
        "hiring", "award", "recognition"
    ]):
        return (5, "Good signal-based angle")

    if outreach_angle and len(outreach_angle) > 5:
        return (3, "Generic angle")

    return (1, "No clear angle")

# ═══════════════════════════════════════════════
# SCORE RESULT CLASS
# ═══════════════════════════════════════════════

class ScoreResult:
    """Complete scoring result with breakdown"""

    def __init__(
        self,
        total: int,
        score_tier: str,
        should_pursue: bool,
        skip_reason: str,
        breakdown: dict
    ):
        self.total = total
        self.score_tier = score_tier
        self.should_pursue = should_pursue
        self.skip_reason = skip_reason
        self.breakdown = breakdown

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "score_tier": self.score_tier,
            "should_pursue": self.should_pursue,
            "skip_reason": self.skip_reason,
            "breakdown": self.breakdown
        }

    def format_breakdown(self) -> str:
        lines = []
        lines.append("=" * 50)
        lines.append(f"TOTAL SCORE: {self.total}/100 [{self.score_tier}]")
        lines.append("=" * 50)
        if not self.should_pursue:
            lines.append(f"!! SKIP: {self.skip_reason}")
            return "\n".join(lines)
        for category, data in self.breakdown.items():
            lines.append(
                f"{category:<20} {data['points']:>2} pts — {data['reason']}"
            )
        return "\n".join(lines)


# ═══════════════════════════════════════════════
# MAIN SCORING FUNCTION
# ═══════════════════════════════════════════════

def calculate_pitchiq_score(
    hotel_name: str,
    hotel_location: str = "",
    hotel_tier: str = "",
    contact_title: str = "",
    contact_email: str = "",
    decision_authority: str = "",
    outreach_angle: str = "",
    personalization_hook: str = "",
    hiring_signals: list = None,
    staff_estimate: str = "",
    opening_date: str = None,
) -> ScoreResult:
    """
    Master scoring function for PitchIQ.
    Works for both new opening and existing hotels.
    """
    hiring_signals = hiring_signals or []
    breakdown = {}
    total = 0

    # ── 1. BRAND TIER (25 pts) ──
    tier_num, tier_name, brand_pts = get_brand_score(hotel_name)

    if tier_num == 5:
        return ScoreResult(
            total=0,
            score_tier="SKIP",
            should_pursue=False,
            skip_reason=f"Budget brand — {hotel_name} not worth pursuing",
            breakdown={}
        )

    breakdown["Brand Tier"] = {"points": brand_pts, "reason": tier_name}
    total += brand_pts

    # ── 2. LOCATION (15 pts) ──
    loc_pts, loc_tier = get_location_score(hotel_location)
    breakdown["Location"] = {"points": loc_pts, "reason": loc_tier}
    total += loc_pts

    # ── 3. URGENCY (25 pts) ──
    urg_pts, urg_tier = get_urgency_score(
        outreach_angle, hiring_signals, opening_date
    )
    breakdown["Urgency"] = {"points": urg_pts, "reason": urg_tier}
    total += urg_pts

    # ── 4. STAFF/ROOM SIZE (15 pts) ──
    size_pts, size_tier = get_size_score(staff_estimate, hiring_signals)
    breakdown["Staff Size"] = {"points": size_pts, "reason": size_tier}
    total += size_pts

    # ── 5. CONTACT AUTHORITY (12 pts) ──
    contact_pts, contact_tier = get_contact_score(
        contact_title, contact_email, decision_authority
    )
    breakdown["Contact Authority"] = {"points": contact_pts, "reason": contact_tier}
    total += contact_pts

    # ── 6. OUTREACH ANGLE (8 pts) ──
    angle_pts, angle_tier = get_angle_score(outreach_angle, personalization_hook)
    breakdown["Outreach Angle"] = {"points": angle_pts, "reason": angle_tier}
    total += angle_pts

    # ── SCORE TIER ──
    if total >= 80:
        score_tier = "HOT 🔥"
    elif total >= 60:
        score_tier = "WARM ♨️"
    elif total >= 40:
        score_tier = "COOL 🌤️"
    else:
        score_tier = "COLD ❄️"

    return ScoreResult(
        total=total,
        score_tier=score_tier,
        should_pursue=True,
        skip_reason=None,
        breakdown=breakdown
    )