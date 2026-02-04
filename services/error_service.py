from datetime import datetime
from ai.graph import analyze_error_node, generate_solution_node
from db.repositories.error_repo import save_error, save_error_analysis, save_error_solution
from db.session import SessionLocal

def ingest_error(error_data):
        if error_data["severity"] == "error":
            error_data["severity"] = "high"
        elif error_data["severity"] == "warning":
            error_data["severity"] = "medium"
        else:
            error_data["severity"] = "low"
        
        db = SessionLocal()
        
        err = save_error(db, error_data)
        db.commit()
        db.refresh(err)
        
        result = analyze_error_node(error_data)
        # Add receipt timestamp
        error_data['received_at'] = datetime.now().isoformat()
        
        if result["urgency"] == "error":
            result["urgency"] = "high"
        elif result["urgency"] == "warning":
            result["urgency"] = "medium"
        else:
            result["urgency"] = "low"
            
        if result:
            save_error_analysis(db, err.id, result)
        
        
        print("-"*20)
        print("AI ANALYSIS")
        print("-"*20)
        print()
        print("-"*20)
        print("ERROR NAME:")
        print("-"*20)
        print(result["error_name"])
        print()
        print("-"*20)
        print("PROBABLE ROOT CAUSE:")
        print("-"*20)
        print(result["probable_root_cause"])
        print()
        print("-"*20)
        print("IMPACT ASSESMENT:")
        print("-"*20)
        print(result["impact_assesment"])
        print()
        print("-"*20)
        print("URGENCY:")
        print("-"*20)
        print(result["urgency"])
        print()
        print("-"*20)
        print("CONFIDENCE:")
        print("-"*20)
        print(result["confidence"])
        print()
        print("-"*20)
        print("SIGNALS USED:")
        print("-"*20)
        for a in result["signals_used"]:
            print(a)
        print()
        print("-"*20)
        print("IMMEDIATE ACTIONS:")
        print("-"*20)
        for a in result["immediate_actions"]:
            print(a)
        print()
        print("-"*20)
        print("DEEPER INVESTIGATION:")
        print("-"*20)
        for a in result["deeper_investigation"]:
            print(a)
        print()
        print("-"*20)
        print("ASSUMPTIONS:")
        print("-"*20)
        for a in result["assumptions"]:
            print(a)
        print()
        
        solution = generate_solution_node(result)
        
        if solution:
            save_error_solution(db, err.id, solution)
        
        if result or solution:
            db.commit()
        
        print("-"*20)
        print("SOLUTION")
        print("-"*20)
        print()
        print("-"*20)
        print("CODE FIXES:")
        print("-"*20)
        for code_fix in solution["code_fixes"]:
            print("FILE:", code_fix["file"])
            print("DESCRIPTION:", code_fix["description"])
            print("CODE:")
            print(code_fix["code"])
            print()
        
        print("-"*20)
        print("CONFIGURATION CHANGES:")
        print("-"*20)
        for config_change in solution["configuration_changes"]:
            print("KEY:", config_change["key"])
            print("VALUE:", config_change["value"])
            print("REASON:", config_change["reason"])
            print()
        
        print("-"*20)
        print("DEPLOYMENT STEPS:")
        print("-"*20)
        for step in solution["deployment_steps"]:
            print(step)
        
        print()
        print("-"*20)
        print("ROLLBACK PLAN:")
        print("-"*20)
        print("SIGNALS TO MONITOR:")
        
        for signal in solution["rollback_plan"]["signals_to_monitor"]:
            print(signal)
            
        print()
        print("STEPS:")
        for step in solution["rollback_plan"]["steps"]:
            print(step)
            
        print()
        
        return err.id