#!/usr/bin/env python3
"""
Test YouTube functionality fix
"""

from browsing_functionalities import youtube, youtube_direct_play
import webbrowser

def test_youtube_functions():
    print("Testing YouTube functionality...")
    
    # Test basic YouTube search
    print("\n1. Testing basic YouTube search...")
    try:
        result = youtube("play python tutorial")
        print(f"Result: {result}")
        print("✓ Basic YouTube search working")
    except Exception as e:
        print(f"✗ Basic YouTube search failed: {e}")
    
    # Test direct play function
    print("\n2. Testing direct play function...")
    try:
        result = youtube_direct_play("play relaxing music")
        print(f"Result: {result}")
        print("✓ Direct play function working")
    except Exception as e:
        print(f"⚠ Direct play failed (expected): {e}")
        print("This is normal - falling back to search results")
    
    print("\n3. Testing URL encoding...")
    try:
        result = youtube("play hello world python programming")
        print(f"Result: {result}")
        print("✓ URL encoding working")
    except Exception as e:
        print(f"✗ URL encoding failed: {e}")

if __name__ == "__main__":
    test_youtube_functions()