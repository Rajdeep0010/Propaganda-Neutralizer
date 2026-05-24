#imports 
from detector import detect
from neutralizer import neutralizer

def run_pipeline(context, snippet):
    print("="*60)
    print((f"Original"))
    print(f"Context : {context}")
    print(f"Snippet" : {snippet})
    print("="*60)
    
    #Detection
    detection = detect(context, snippet)
    
    if not detection:
        print("\nNo propanda technique detected.")
        print("="*60)
        return{
            "original" : context,
            "snippet" : snippet,
            "technique" : [],
            "neutralized": context
        }
    print(f"\n Detected techniques")
    for d in detections:
        print(f" {d['technique']:<40} confidence: {d['confidence']:.4f}")
        
    #Neutralize
    top_technique = detections[0]["technique"]
    print(f"\nNeutralizing using top technique: {top_technique}")
    print("Rewriting...\n")
    neutralized = neutralize(context, snippet, top_technique)
    
    #Output
    print("BEFORE")
    print(f"  {context}")
    print("\nAFTER")
    print(f"  {neutralized}")
    print("=" * 60)

    return {
        "original"   : context,
        "snippet"    : snippet,
        "techniques" : detections,
        "neutralized": neutralized
    }
    
#Test
if __name__ == "__main__":

    run_pipeline(
        context="The radical left is destroying everything our ancestors built.",
        snippet="radical left is destroying everything"
    )
    run_pipeline(
        context="Everyone is joining the movement. You should too before it's too late.",
        snippet="Everyone is joining the movement"
    )

    run_pipeline(
        context="The minister announced a new education policy for rural schools.",
        snippet="new education policy for rural schools"
    )
