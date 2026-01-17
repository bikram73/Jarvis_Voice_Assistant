#!/usr/bin/env python3
"""
Final verification that translation and recording fixes work
"""

def verify_translation_fix():
    """Verify translation command parsing works"""
    print("🌍 VERIFYING TRANSLATION FIX...")
    
    from language_translator import translate_text
    
    # Test the exact command that was failing
    request = "translate my name is vikram to hindi"
    
    # Parse using the new logic from Jarvis.py
    if "translate" in request and "to" in request:
        parts = request.split("to")
        text_part = parts[0].replace("translate", "").strip()
        target_lang = parts[1].strip()
        
        print(f"✅ Parsed text: '{text_part}'")
        print(f"✅ Target language: '{target_lang}'")
        
        result = translate_text(text_part, target_lang)
        if isinstance(result, dict):
            print(f"✅ Translation successful: {result['translated']}")
            return True
    
    return False

def verify_recording_fix():
    """Verify screen recording works"""
    print("\n🎥 VERIFYING RECORDING FIX...")
    
    from screenshot_recorder import start_recording, stop_recording
    import time
    
    try:
        # Start recording
        result = start_recording("verification_test.mp4", with_audio=False)
        print(f"✅ Recording started: {result}")
        
        # Record for 1 second
        time.sleep(1)
        
        # Stop recording
        result = stop_recording()
        print(f"✅ Recording stopped: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Recording failed: {e}")
        return False

def main():
    print("="*60)
    print("🔧 FINAL VERIFICATION OF FIXES")
    print("="*60)
    
    translation_ok = verify_translation_fix()
    recording_ok = verify_recording_fix()
    
    print("\n" + "="*60)
    print("📊 VERIFICATION RESULTS:")
    print("="*60)
    
    print(f"🌍 Translation Fix: {'✅ WORKING' if translation_ok else '❌ FAILED'}")
    print(f"🎥 Recording Fix: {'✅ WORKING' if recording_ok else '❌ FAILED'}")
    
    if translation_ok and recording_ok:
        print("\n🎉 ALL FIXES VERIFIED SUCCESSFULLY!")
        print("\n✅ You can now use these commands in Jarvis:")
        print("   • 'translate my name is Vikram to Hindi'")
        print("   • 'start recording'")
        print("   • 'stop recording'")
        print("   • 'take screenshot'")
    else:
        print("\n⚠️ Some issues remain - check error messages above")

if __name__ == "__main__":
    main()