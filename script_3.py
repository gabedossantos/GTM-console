# Create sample data generation for JourneyLens demo
import json
import csv
from datetime import datetime, timedelta
import random

# Sample data for Jobber-like small business scenarios
sample_data = {
    "accounts": [
        {"id": 1, "name": "Sunshine Landscaping", "industry": "landscaping", "status": "active"},
        {"id": 2, "name": "QuickFix Plumbing", "industry": "plumbing", "status": "active"}, 
        {"id": 3, "name": "Elite House Cleaning", "industry": "cleaning", "status": "active"},
        {"id": 4, "name": "PowerWash Pro", "industry": "pressure_washing", "status": "active"},
        {"id": 5, "name": "City HVAC Solutions", "industry": "hvac", "status": "active"}
    ],
    
    "contacts": [
        {"id": 1, "account_id": 1, "name": "Maria Rodriguez", "email": "maria@sunshinelandscaping.com", "role": "Owner"},
        {"id": 2, "account_id": 1, "name": "James Thompson", "email": "james@sunshinelandscaping.com", "role": "Operations Manager"},
        {"id": 3, "account_id": 2, "name": "Mike Chen", "email": "mike@quickfixplumbing.com", "role": "Owner"},
        {"id": 4, "account_id": 3, "name": "Sarah Williams", "email": "sarah@elitecleaning.com", "role": "Owner"},
        {"id": 5, "account_id": 4, "name": "Robert Davis", "email": "rob@powerwashpro.com", "role": "Owner"},
        {"id": 6, "account_id": 5, "name": "Lisa Johnson", "email": "lisa@cityhvac.com", "role": "General Manager"}
    ]
}

# Generate sample conversations for different scenarios
sample_conversations = [
    {
        "account_id": 1,
        "contact_id": 1,
        "channel": "email",
        "content": """Hi Support Team,

I hope you're doing well. I wanted to reach out because we're having some challenges with the new invoicing feature that was rolled out last month. 

Our team has been trying to customize the invoice templates to match our branding, but we're running into issues with the logo placement and color schemes. The current options don't seem to support our specific requirements.

Additionally, we've noticed that the automatic tax calculations aren't working correctly for our service area. We operate across multiple tax jurisdictions, and it seems like the system is applying the wrong rates in some cases.

This is becoming urgent because we have several large commercial projects completing next week, and we need to get accurate invoices out to our clients. Our cash flow depends on prompt billing.

Could someone from your technical team give me a call today or tomorrow? We really need to get this sorted out quickly.

Thanks for your help,
Maria Rodriguez
Sunshine Landscaping
(555) 123-4567""",
        "intent": "support_request",
        "sentiment": "negative",
        "risk_score": 0.7
    },
    
    {
        "account_id": 2,
        "contact_id": 3,
        "channel": "call",
        "content": """Call transcript - Mike Chen, QuickFix Plumbing

Mike: Hey, thanks for taking my call. I've been using Jobber for about 8 months now, and overall it's been great for our business. We've seen a real improvement in our scheduling efficiency and customer communication.

Support: That's wonderful to hear, Mike. What can I help you with today?

Mike: Well, I'm actually looking at expanding my subscription. We're growing pretty fast - added three new trucks and five employees in the last quarter. I'm interested in the advanced features, particularly the GPS tracking and the advanced reporting.

Support: Congratulations on the growth! That's exactly the kind of success story we love to hear. Let me walk you through our Professional plan features...

Mike: Yeah, the GPS tracking would be huge for us. Right now I'm manually checking where my guys are, and it's eating up a lot of my time. And I heard you have some new features coming for inventory management?

Support: Absolutely! Our inventory management module just entered beta, and it integrates directly with your job scheduling. You can track parts usage, set reorder points, and even generate purchase orders automatically.

Mike: That sounds perfect. We're losing money on inefficient inventory right now. What would the upgrade cost, and when could we get started?

Support: For your size operation, you'd be looking at the Professional plan at $129 per month, up from your current $79. The inventory module would be an additional $39 per month. I can get you set up today if you'd like.

Mike: Let's do it. This is exactly what we need to scale properly.""",
        "intent": "upgrade_inquiry",
        "sentiment": "positive", 
        "risk_score": 0.1
    },
    
    {
        "account_id": 3,
        "contact_id": 4,
        "channel": "email",
        "content": """Subject: Pricing Question - Multiple Location Discount?

Hi,

I run Elite House Cleaning, and we've been really happy with Jobber over the past year. It's made a huge difference in how we manage our operations.

I'm writing because we're about to expand into two new cities, and I wanted to understand if there are any volume discounts available for multiple locations. We're projecting that we'll need to add about 15-20 more team members across the new locations.

Currently we're on the Growing Business plan, but with the expansion, we'd probably need the Professional plan features for better territory management and advanced reporting.

Also, I saw that you have a new customer portal feature. Could you tell me more about how that works? Our clients are always asking for better ways to track their service history and make changes to their recurring cleanings.

I'd love to schedule a call to discuss our expansion plans and see how Jobber can support our growth. We're planning to launch the new locations in the next 3 months.

Best regards,
Sarah Williams
Elite House Cleaning
sarah@elitecleaning.com
(555) 987-6543""",
        "intent": "expansion_inquiry",
        "sentiment": "positive",
        "risk_score": 0.2
    },
    
    {
        "account_id": 4,
        "contact_id": 5,
        "channel": "email", 
        "content": """Subject: Considering Other Options

Hi,

I've been a Jobber customer for about 6 months now, but I'm starting to have some concerns about whether this is still the right fit for my business.

Don't get me wrong - the software does what it says it will do. But I'm finding that the cost is adding up, and I'm not sure I'm getting enough value for what I'm paying. Between the monthly subscription, the payment processing fees, and some of the add-on features, it's becoming a significant expense.

I've been looking at some other options like ServiceTitan and Housecall Pro, and they seem to offer similar features at different price points. ServiceTitan in particular has some advanced features for route optimization that could save me fuel costs.

I'm also frustrated with the mobile app performance. My crew is constantly complaining that it's slow and sometimes crashes when they're trying to update job statuses or take photos. This is causing issues with our customer communication because updates aren't getting through in real-time.

Before I make any decisions, I wanted to give you guys a chance to address these concerns. Is there anything you can do about the pricing? And are there any plans to improve the mobile app performance?

I really don't want to switch systems because I know how disruptive that can be, but I need to do what's best for my business.

Let me know if we can discuss this.

Robert Davis
PowerWash Pro
rob@powerwashpro.com""",
        "intent": "churn_risk",
        "sentiment": "negative",
        "risk_score": 0.9
    },
    
    {
        "account_id": 5,
        "contact_id": 6,
        "channel": "email",
        "content": """Subject: Feature Request - Integration with QuickBooks Enterprise

Hello Jobber Team,

I hope this message finds you well. We've been using Jobber for our HVAC business for over two years now, and it's been instrumental in helping us grow from a 5-person operation to a 25-person company.

I wanted to reach out with a feature request that would be extremely valuable for our business. We use QuickBooks Enterprise for our accounting, and while the standard QuickBooks integration works well, we need some additional functionality that's specific to the Enterprise version.

Specifically, we need:
1. Support for job costing with multiple cost centers
2. Integration with QB Enterprise's advanced inventory tracking
3. Support for progress billing on large commercial projects

Our commercial HVAC projects often run 3-6 months, and we need to be able to bill milestone payments while tracking costs against specific job phases. The current integration doesn't handle this level of complexity.

I know you're always working on new features, and I wanted to see if this might be something on your roadmap. We'd be happy to participate in a beta program if you decide to develop this functionality.

Also, I wanted to mention that we're probably going to need to add 5-8 more user licenses in the next quarter as we continue to grow. The return on investment with Jobber has been fantastic.

Thanks for all the great work you do!

Lisa Johnson
General Manager
City HVAC Solutions
lisa@cityhvac.com
(555) 555-0123""",
        "intent": "feature_request",
        "sentiment": "positive",
        "risk_score": 0.3
    }
]

# Generate CSV files for demo
def create_demo_data():
    # Accounts CSV
    with open('demo_accounts.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'industry', 'status', 'created_at'])
        writer.writeheader()
        for account in sample_data['accounts']:
            account['created_at'] = (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat()
            writer.writerow(account)
    
    # Contacts CSV  
    with open('demo_contacts.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'account_id', 'name', 'email', 'role', 'created_at'])
        writer.writeheader()
        for contact in sample_data['contacts']:
            contact['created_at'] = (datetime.now() - timedelta(days=random.randint(15, 200))).isoformat()
            writer.writerow(contact)
    
    # Interactions CSV
    with open('demo_interactions.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'account_id', 'contact_id', 'channel', 'content', 'timestamp'])
        writer.writeheader()
        for i, conv in enumerate(sample_conversations, 1):
            interaction = {
                'id': i,
                'account_id': conv['account_id'],
                'contact_id': conv.get('contact_id'),
                'channel': conv['channel'],
                'content': conv['content'].strip(),
                'timestamp': (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat()
            }
            writer.writerow(interaction)
    
    # Expected insights CSV (for evaluation)
    with open('demo_expected_insights.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['interaction_id', 'expected_intent', 'expected_sentiment', 'expected_risk_score'])
        writer.writeheader()
        for i, conv in enumerate(sample_conversations, 1):
            writer.writerow({
                'interaction_id': i,
                'expected_intent': conv['intent'],
                'expected_sentiment': conv['sentiment'],
                'expected_risk_score': conv['risk_score']
            })

create_demo_data()

# Also create individual conversation files for upload testing
for i, conv in enumerate(sample_conversations, 1):
    filename = f"conversation_{i}_{conv['intent']}.txt"
    with open(filename, 'w') as f:
        f.write(f"Account: {conv['account_id']}\n")
        f.write(f"Channel: {conv['channel']}\n")
        f.write(f"Expected Intent: {conv['intent']}\n")
        f.write(f"Expected Sentiment: {conv['sentiment']}\n")
        f.write(f"Expected Risk Score: {conv['risk_score']}\n")
        f.write("="*50 + "\n\n")
        f.write(conv['content'])

print("✅ Demo data generated successfully!")
print("\nFiles created:")
print("- demo_accounts.csv (5 sample service businesses)")
print("- demo_contacts.csv (6 business contacts)")  
print("- demo_interactions.csv (5 realistic conversations)")
print("- demo_expected_insights.csv (evaluation ground truth)")
print("- conversation_1_support_request.txt")
print("- conversation_2_upgrade_inquiry.txt")
print("- conversation_3_expansion_inquiry.txt")
print("- conversation_4_churn_risk.txt")
print("- conversation_5_feature_request.txt")

print("\nDemo Scenarios Cover:")
print("- 📞 Support requests with technical issues")
print("- 💰 Upgrade and expansion inquiries")
print("- ⚠️ Churn risk situations")
print("- 💡 Feature requests and feedback")
print("- 🎯 Different sentiment levels and risk scores")
print("- 🏢 Various small business industries (landscaping, plumbing, cleaning, etc.)")