# Create a more detailed and readable wireframe mockup for JourneyLens UI
diagram_code = """
flowchart TD
    subgraph TOP ["Top Navigation Bar"]
        NAV1["🔄 Role: CSM | AE | Support"]
        NAV2["👤 User Profile"]
        NAV3["⚙️ Settings"]
    end
    
    subgraph SIDE ["Left Sidebar"]
        SIDE1["📊 My Accounts Today<br/>• Account A - High Risk<br/>• Account B - Medium Risk"]
        SIDE2["💡 Insights Feedback Needed<br/>• 3 Pending Reviews"]
        SIDE3["🤖 AI Performance Snapshot<br/>• 89% Accuracy<br/>• 156 Predictions"]
    end
    
    subgraph CSM ["CSM Dashboard View"]
        CSM1["⚠️ Accounts at Risk Today<br/>━━━━━━━━━━━━━━━━━━━<br/>• TechCorp - Contract Risk<br/>• DataFlow - Usage Drop<br/>• CloudSync - Support Issues"]
        CSM2["📈 Last 7 Days Interaction Deltas<br/>━━━━━━━━━━━━━━━━━━━<br/>[Chart: Line graph showing<br/>engagement trends]"]
        CSM3["🎯 Next Best Actions<br/>━━━━━━━━━━━━━━━━━━━<br/>• Schedule check-in call<br/>• Send usage report<br/>• Escalate to manager"]
    end
    
    subgraph AE ["AE Dashboard View"]
        AE1["💼 Open Opportunities<br/>━━━━━━━━━━━━━━━━━━━<br/>• Enterprise Deal - 🔴 Intent ↓<br/>• Growth Account - 🟢 Intent ↑<br/>• New Prospect - 🟡 Intent →"]
        AE2["❓ Key Objections Extracted<br/>━━━━━━━━━━━━━━━━━━━<br/>• Budget concerns: 45%<br/>• Feature gaps: 30%<br/>• Timeline issues: 25%"]
        AE3["💰 Revenue Pipeline Status<br/>━━━━━━━━━━━━━━━━━━━<br/>[Chart: Progress bars showing<br/>pipeline stages]"]
    end
    
    subgraph SUP ["Support Dashboard View"]
        SUP1["🎫 Tickets with Repeated Themes<br/>━━━━━━━━━━━━━━━━━━━<br/>• Login Issues: 12 tickets<br/>• API Errors: 8 tickets<br/>• Billing Questions: 6 tickets"]
        SUP2["😟 Sentiment Regression Detector<br/>━━━━━━━━━━━━━━━━━━━<br/>🔴 3 Alerts:<br/>• Account X - Negative trend<br/>• Account Y - Escalating tone"]
        SUP3["⏱️ Resolution Time Trends<br/>━━━━━━━━━━━━━━━━━━━<br/>[Chart: Trend line showing<br/>avg resolution times]"]
    end
    
    subgraph MODAL ["Account Detail Modal"]
        MOD1["🧠 RAG-Powered Recent Intent<br/>━━━━━━━━━━━━━━━━━━━<br/>• Expansion interest detected<br/>• Feature request patterns<br/>• Renewal likelihood: 78%"]
        MOD2["📅 Account Timeline<br/>━━━━━━━━━━━━━━━━━━━<br/>• Last contact: 2 days ago<br/>• Contract renewal: 45 days<br/>• Support ticket: Resolved"]
        MOD3["📝 Feedback Widget<br/>━━━━━━━━━━━━━━━━━━━<br/>⭐ Rate this insight<br/>💬 Add comments<br/>✅ Mark as helpful"]
    end
    
    TOP --> SIDE
    TOP --> CSM
    TOP --> AE  
    TOP --> SUP
    SIDE --> MODAL
    CSM --> MODAL
    AE --> MODAL
    SUP --> MODAL
"""

# Create the enhanced wireframe diagram
png_path, svg_path = create_mermaid_diagram(diagram_code, 'journeylens_wireframe.png', 'journeylens_wireframe.svg', width=1400, height=1200)

print(f"Enhanced JourneyLens UI wireframe saved as: {png_path} and {svg_path}")