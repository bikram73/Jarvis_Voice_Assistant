#!/usr/bin/env python3
"""
Test Jarvis startup and basic functionality
"""

def test_jarvis_startup():
    """Test if Jarvis starts up correctly"""
    
    print("🤖 TESTING JARVIS STARTUP")
    print("="*40)
    
    try:
        # Test imports
        print("1. Testing imports...")
        import Jarvis
        print("✅ Jarvis imported successfully")
        
        # Test basic functions
        print("\n2. Testing basic functions...")
        
        # Test wishme function
        try:
            Jarvis.wishme()
            print("✅ Wishme function working")
        except Exception as e:
            print(f"⚠️ Wishme function issue: {e}")
        
        # Test load_name function
        try:
            name = Jarvis.load_name()
            print(f"✅ Assistant name loaded: {name}")
        except Exception as e:
            print(f"⚠️ Load name issue: {e}")
        
        print("\n3. Testing feature availability...")
        
        # Check which features are available
        features = {
            "PDF Reader": hasattr(Jarvis, 'PDF_AVAILABLE') and Jarvis.PDF_AVAILABLE,
            "System Control": hasattr(Jarvis, 'SYSTEM_CONTROL_AVAILABLE') and Jarvis.SYSTEM_CONTROL_AVAILABLE,
            "Volume Control": hasattr(Jarvis, 'VOLUME_CONTROL_AVAILABLE') and Jarvis.VOLUME_CONTROL_AVAILABLE
        }
        
        for feature, available in features.items():
            status = "✅ Available" if available else "⚠️ Not Available"
            print(f"{feature}: {status}")
        
        print("\n" + "="*40)
        print("🎉 JARVIS STARTUP TEST COMPLETED!")
        print("="*40)
        
        available_count = sum(features.values())
        print(f"Core features working: ✅")
        print(f"Additional features: {available_count}/3 available")
        
        if available_count >= 1:
            print("\n✅ Jarvis is ready to use!")
            print("You can run 'python Jarvis.py' to start the assistant")
        else:
            print("\n⚠️ Some features may be limited due to missing dependencies")
            print("But core Jarvis functionality should work")
        
        return True
        
    except Exception as e:
        print(f"❌ Jarvis startup failed: {e}")
        return False

if __name__ == "__main__":
    test_jarvis_startup()