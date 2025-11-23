import logging
import requests
import time
import hashlib
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import exc as sa_exc
import os
import sys

logger = logging.getLogger(__name__)

# 🔑 API credentials

from dotenv import load_dotenv
load_dotenv()

import os

API_KEY = os.getenv("GOOGLE_API_KEY")
CSE_ID = os.getenv("GOOGLE_CSE_ID")




# 🔁 Cache threshold
CACHE_MINIMUM_COUNT = 10  # Increased to ensure we have enough items

# 🎨 Color palettes for undertones
warm_palette = ["#FFD500", "#5A0F0A", "#F1A27E", "#F6A12A", "#FFC75F"]
cool_palette = ["#FFFFFF", "#CFCFD3", "#8B8B94", "#D65A82", "#B9AAD3"]
neutral_palette = ["#D1C8C1", "#146751", "#193C64", "#D59399", "#C27A86"]

# ✅ IMPORT OUTFIT MODEL - Add this crucial import
try:
    # Add parent directory to path to import models
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    
    from models import Outfit
    logger.info("✅ SUCCESS: Outfit model imported successfully")
except ImportError as e:
    logger.error(f"❌ FAILED to import Outfit model: {e}")
    # Fallback mock class
    class Outfit:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)

# 🎯 Map hex → color name
def hex_to_color_name(hex_code: str) -> str:
    color_map = {
        "#FFD500": "yellow", "#5A0F0A": "burgundy", "#F1A27E": "coral",
        "#F6A12A": "orange", "#FFC75F": "gold", "#88B04B": "olive",
        "#FFFFFF": "white", "#CFCFD3": "gray", "#8B8B94": "charcoal",
        "#D65A82": "pink", "#B9AAD3": "lavender", "#D1C8C1": "beige",
        "#146751": "green", "#193C64": "blue", "#D59399": "pink",
    }
    return color_map.get(hex_code, "neutral")

# 🔍 Generate unique ID for items
def generate_item_id(link: str, title: str) -> str:
    unique_string = f"{link}_{title}"
    return hashlib.sha256(unique_string.encode()).hexdigest()

# 🛍️ Google Custom Search API for fashion items
def search_fashion_items(query: str, max_results: int = 3) -> List[Dict]:
    """Fetch fashion images from Google Custom Search API."""
    try:
        logger.info(f"🔍 Searching for: {query}")
        
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "cx": CSE_ID,
            "key": API_KEY,
            "searchType": "image",
            "num": max_results
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code != 200:
            logger.error(f"❌ API Error {response.status_code}: {response.text}")
            return []
            
        data = response.json()
        items = []
        
        for item in data.get("items", []):
            title = item.get("title", "Unknown Title")
            link = item.get("link", "")
            image_url = item.get("image", {}).get("thumbnailLink", "") or link
            
            if title and link and image_url:
                api_item_id = generate_item_id(link, title)
                display_title = title[:80] + "..." if len(title) > 80 else title
                
                items.append({
                    "api_item_id": api_item_id,
                    "title": display_title,
                    "link": link,
                    "image": image_url
                })

        logger.info(f"✅ Found {len(items)} items for: {query}")
        return items

    except Exception as e:
        logger.error(f"❌ Search error: {str(e)}")
        return []

# 🧩 Fetch and format outfits for a given undertone
def fetch_and_structure_outfits(undertone: str) -> List[Dict[str, Any]]:
    """Fetch new outfits from Google API based on undertone."""
    logger.info(f"🎨 Starting outfit fetch for {undertone}...")

    palette = {
        "Warm Undertone": warm_palette,
        "Cool Undertone": cool_palette,
    }.get(undertone, neutral_palette)

    top_colors = [hex_to_color_name(color) for color in palette][:5]
    all_fashion_items = []
    
    logger.info(f"🎯 Targeting 5 colors: {top_colors}")

    for color in top_colors:
        # Try multiple queries to get enough results
        queries = [
            f"{color} dress fashion",
            f"{color} dress women",
            f"{color} outfit fashion",
            f"{color} clothing women"
        ]
        
        color_items = []
        
        for query in queries:
            if len(color_items) >= 2:  # We need exactly 2 per color
                break
                
            items = search_fashion_items(query, max_results=3)
            
            for item in items:
                if len(color_items) < 2:  # Take only 2 per color
                    item["color"] = color
                    item["undertone_match"] = undertone
                    color_items.append(item)
            
            time.sleep(1)  # Rate limiting
        
        logger.info(f"🎨 Color '{color}': Found {len(color_items)} items")
        all_fashion_items.extend(color_items)

    logger.info(f"📊 Total items fetched: {len(all_fashion_items)}")
    
    # If we don't have enough items, try to fill with additional searches
    if len(all_fashion_items) < 10:
        logger.warning(f"⚠️ Only got {len(all_fashion_items)} items, trying to get more...")
        additional_items_needed = 10 - len(all_fashion_items)
        
        # Try some generic searches
        generic_queries = [
            "fashion dress women",
            "women clothing fashion",
            "outfit dress trendy"
        ]
        
        for query in generic_queries:
            if additional_items_needed <= 0:
                break
                
            items = search_fashion_items(query, max_results=additional_items_needed)
            for item in items:
                if additional_items_needed > 0:
                    item["color"] = "multi"  # Generic color
                    item["undertone_match"] = undertone
                    all_fashion_items.append(item)
                    additional_items_needed -= 1
            
            time.sleep(1)
    
    logger.info(f"🎯 Final count: {len(all_fashion_items)} items")
    return all_fashion_items[:10]  # Ensure we return exactly 10 items

# 💾 Save outfits to database
def save_outfits_to_db(outfits: List[Dict], db: Session, undertone: str) -> int:
    """Save outfits to database with detailed logging."""
    saved_count = 0
    skipped_count = 0
    error_count = 0
    
    logger.info(f"💾 Attempting to save {len(outfits)} items to database...")
    
    for i, item in enumerate(outfits):
        try:
            # Check if item already exists
            exists = db.query(Outfit).filter(Outfit.api_item_id == item["api_item_id"]).first()
            if exists:
                logger.debug(f"⏭️ Item {i+1}: Already exists in DB - {item['title'][:30]}...")
                skipped_count += 1
                continue
                
            # Create new outfit record - matching your model structure
            db_outfit = Outfit(
                api_item_id=item["api_item_id"],
                category="Dress",  # Default category
                base_color=item["color"],
                undertone_match=item["undertone_match"],
                image_url=item["image"],
                details_url=item["link"],
                price=None  # Price not available from Google API
            )
            db.add(db_outfit)
            saved_count += 1
            logger.info(f"💾 Item {i+1}: Saving - {item['title'][:40]}...")
            
        except Exception as e:
            error_count += 1
            logger.error(f"❌ Item {i+1}: Save failed - {e}")

    try:
        db.commit()
        logger.info(f"✅ DATABASE COMMIT SUCCESSFUL!")
        logger.info(f"📊 SAVE SUMMARY - Saved: {saved_count}, Skipped: {skipped_count}, Errors: {error_count}")
        return saved_count
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ DATABASE COMMIT FAILED: {e}")
        return 0

# 💾 Main function to get fashion recommendations
def get_fashion_recommendations(undertone: str, db: Session) -> List[Dict[str, Any]]:
    """
    Main function that:
    1. Checks if database has enough items
    2. If not, fetches from Google API
    3. Saves new items to database
    4. Returns results
    """
    logger.info(f"🚀 STARTING FASHION RECOMMENDATIONS FOR: {undertone}")
    
    # Step 1: Check current database
    try:
        outfit_count = db.query(Outfit).filter(Outfit.undertone_match == undertone).count()
        logger.info(f"📊 Database has {outfit_count} items for {undertone}")
        
        if outfit_count >= CACHE_MINIMUM_COUNT:
            logger.info("✅ Using existing database items")
            outfits = db.query(Outfit).filter(Outfit.undertone_match == undertone).limit(10).all()
            result = format_outfit_response(outfits)
            logger.info(f"🎯 Returning {len(result)} items from database")
            return result
            
    except Exception as e:
        logger.error(f"❌ Database check failed: {e}")
        outfit_count = 0

    # Step 2: Fetch from API if database is empty
    logger.warning(f"❌ Database empty or insufficient. Fetching from Google API...")
    new_outfits = fetch_and_structure_outfits(undertone)

    if not new_outfits:
        logger.error("❌ Google API returned no data")
        return get_mock_fashion_items(undertone)

    # Step 3: Save to database
    saved_count = save_outfits_to_db(new_outfits, db, undertone)
    
    if saved_count > 0:
        logger.info(f"✅ Successfully saved {saved_count} new items to database")
    else:
        logger.warning("⚠️ No new items saved (may be duplicates)")

    # Step 4: Return results (either from DB or directly from API)
    try:
        # Try to get from database first
        db_outfits = db.query(Outfit).filter(Outfit.undertone_match == undertone).limit(10).all()
        if db_outfits:
            result = format_outfit_response(db_outfits)
            logger.info(f"🎯 Returning {len(result)} items from database")
            return result
        else:
            # Fallback to API results
            result = format_outfit_response(new_outfits[:10])
            logger.info(f"🎯 Returning {len(result)} items from API")
            return result
    except Exception as e:
        logger.error(f"❌ Error getting final outfits: {e}")
        result = format_outfit_response(new_outfits[:10])
        logger.info(f"🎯 Returning {len(result)} items as fallback")
        return result

def format_outfit_response(outfits: List[Any]) -> List[Dict[str, Any]]:
    """Format outfits for API response."""
    formatted = []
    for outfit in outfits:
        if hasattr(outfit, 'category') and hasattr(outfit, 'base_color'):
            # Database outfit object
            formatted.append({
                "title": f"{outfit.category} in {outfit.base_color}",
                "color": outfit.base_color,
                "link": outfit.details_url or "#",
                "image": outfit.image_url,
                "source": "database"
            })
        else:
            # Dictionary outfit (from API)
            formatted.append({
                "title": outfit.get("title", "Fashion Item"),
                "color": outfit.get("color", "unknown"),
                "link": outfit.get("link", ""),
                "image": outfit.get("image", ""),
                "source": "api"
            })
    
    # Ensure we return exactly 10 items
    if len(formatted) < 10:
        logger.warning(f"⚠️ Only {len(formatted)} items available, filling with mock data")
        # Fill remaining slots with mock data
        while len(formatted) < 10:
            formatted.append({
                "title": "Fashion Item",
                "color": "multi",
                "link": "#",
                "image": "https://via.placeholder.com/300x400/cccccc/666666?text=Fashion+Item",
                "source": "mock"
            })
    
    return formatted[:10]

# 🧠 Mock fallback if API fails
def get_mock_fashion_items(undertone: str) -> List[Dict]:
    """Provide sample items when API fails."""
    logger.info(f"🔄 Using mock data for {undertone}")
    
    color_map = {
        "Warm Undertone": ["amber", "orange", "olive", "brown", "black"],
        "Cool Undertone": ["white", "gray", "pink", "light blue", "lavender"],
        "Neutral Undertone": ["beige", "green", "blue", "red", "black"],
    }

    colors = color_map.get(undertone, color_map["Neutral Undertone"])
    
    # Create exactly 10 items: 5 colors × 2 outfits
    mock_items = []
    for color in colors[:5]:  # Take first 5 colors
        for i in range(2):  # 2 outfits per color
            mock_items.append({
                "title": f"Beautiful {color} dress {i+1}",
                "link": f"https://example.com/{color}-dress-{i+1}",
                "image": f"https://via.placeholder.com/300x400/cccccc/666666?text={color}+dress+{i+1}",
                "color": color,
                "source": "mock"
            })
    
    return mock_items[:10]  # Ensure exactly 10 items

# 🆕 FUNCTION TO FORCE REFRESH DATA (even if database has items)
def refresh_fashion_data(undertone: str, db: Session) -> List[Dict[str, Any]]:
    """
    Force refresh data from Google API regardless of what's in database.
    Useful for populating empty database.
    """
    logger.info(f"🔄 FORCE REFRESHING data for {undertone} from Google API")
    
    # Fetch new data
    new_outfits = fetch_and_structure_outfits(undertone)
    
    if not new_outfits:
        logger.error("❌ Google API returned no data")
        return get_mock_fashion_items(undertone)
    
    # Save to database
    saved_count = save_outfits_to_db(new_outfits, db, undertone)
    logger.info(f"✅ Refresh completed: {saved_count} new items saved")
    
    return format_outfit_response(new_outfits[:10])

# 🔧 Database utility functions
def get_database_stats(db: Session) -> Dict[str, Any]:
    """Get database statistics."""
    try:
        total_outfits = db.query(Outfit).count()
        
        undertone_counts = {}
        outfits = db.query(Outfit).all()
        for outfit in outfits:
            undertone = outfit.undertone_match or "Unknown"
            undertone_counts[undertone] = undertone_counts.get(undertone, 0) + 1
        
        return {
            "total_outfits": total_outfits,
            "undertone_distribution": undertone_counts,
            "database_status": "healthy"
        }
    except Exception as e:
        return {"database_status": "error", "error": str(e)}

# Alias for backward compatibility
get_fashion_recommendations_with_db = get_fashion_recommendations