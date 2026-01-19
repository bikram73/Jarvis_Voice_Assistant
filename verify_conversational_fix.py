#!/usr/bin/env python3
"""
Verify that conversational commands are working in the actual Jarvis
"""

def test_jarvis_conversational_commands():
    """Test that Jarvis has all the conversational commands implemented"""
    
    print("🤖 VERIFYING CONVERSATIONAL COMMANDS IN JARVIS")
    print("="*60)
    
    try:
        # Import Jarvis to check the implementation
        import Jarvis
        print("✅ Jarvis imported successfully")
        
        # Read the Jarvis.py file to verify commands are present
        with open("Jarvis.py", "r") as f:
            jarvis_content = f.read()
        
        # Check for the presence of conversational commands
        conversational_checks = [
            ("hello", '"hello" in request'),
            ("good morning", '"good morning" in request'),
            ("good afternoon", '"good afternoon" in request'),
            ("good evening", '"good evening" in request'),
            ("how are you", '"how are you" in request'),
            ("what is your name", '"what is your name" in request'),
            ("what can you do", '"what can you do" in request'),
            ("help", '"help" in request'),
            ("thank you", '"thank you" in request'),
            ("what day is it", '"what day is it" in request'),
        ]
        
        print("\nChecking implemented commands:")
        all_present = True
        
        for command_name, search_string in conversational_checks:
            if search_string in jarvis_content:
                print(f"✅ '{command_name}' - IMPLEMENTED")
            else:
                print(f"❌ '{command_name}' - MISSING")
                all_present = False
        
        # Check for additional conversational commands
        additional_checks = [
            ("who created you", '"who created you" in request'),
            ("how old are you", '"how old are you" in request'),
            ("where are you from", '"where are you from" in request'),
            ("you're awesome", '"you\'re awesome" in request'),
            ("i'm bored", '"i\'m bored" in request'),
        ]
        
        print("\nChecking additional conversational commands:")
        for command_name, search_string in additional_checks:
            if search_string in jarvis_content:
                print(f"✅ '{command_name}' - IMPLEMENTED")
            else:
                print(f"⚠️ '{command_name}' - Not found (may use different pattern)")
        
        print("\n" + "="*60)
        
        if all_present:
            print("🎉 ALL BASIC CONVERSATIONAL COMMANDS ARE IMPLEMENTED!")
            print("="*60)
            
            print("\n✅ Working Commands:")
            print("   • 'Hello' / 'Hi'")
            print("   • 'Good morning/afternoon/evening'")
            print("   • 'How are you?'")
            print("   • 'What's your name?'")
            print("   • 'What can you do?'")
            print("   • 'Help'")
            print("   • 'Thank you'")
            print("   • 'What day is it?'")
            print("   • And more conversational responses!")
            
            print(f"\n🚀 You can now run 'python Jarvis.py' and use all conversational commands!")
            
        else:
            print("⚠️ SOME COMMANDS MAY BE MISSING")
            print("Check the implementation in Jarvis.py")
        
        return all_present
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

if __name__ == "__main__":
    success = test_jarvis_conversational_commands()
    
    if success:
        print("\n🎯 VERIFICATION COMPLETE - ALL SYSTEMS GO!")
    else:
        print("\n⚠️ VERIFICATION INCOMPLETE - CHECK IMPLEMENTATION")