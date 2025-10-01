# Create a cleaner, more readable database schema diagram for JourneyLens
diagram_code = """
erDiagram
    ACCOUNTS {
        int id PK
        varchar name
        varchar industry
        timestamp created_at
        varchar status
    }
    
    USERS {
        int id PK
        varchar email
        varchar role
        varchar name
        timestamp created_at
    }
    
    CONTACTS {
        int id PK
        int account_id FK
        varchar name
        varchar email
        varchar role
        timestamp created_at
    }
    
    INTERACTIONS {
        int id PK
        int account_id FK
        int contact_id FK
        varchar channel
        timestamp timestamp
        text content
        varchar file_path
    }
    
    INSIGHTS {
        int id PK
        int interaction_id FK
        varchar intent
        varchar sentiment
        decimal risk_score
        text summary
        decimal confidence
        timestamp created_at
    }
    
    FEEDBACK {
        int id PK
        int insight_id FK
        int user_id FK
        varchar rating
        varchar reason_code
        text comments
        timestamp created_at
    }
    
    EVALSAMPLES {
        int id PK
        int interaction_id FK
        varchar expected_intent
        varchar expected_sentiment
        decimal expected_risk
        timestamp created_at
    }
    
    ACCOUNTS ||--o{ CONTACTS : ""
    ACCOUNTS ||--o{ INTERACTIONS : ""
    CONTACTS ||--o{ INTERACTIONS : ""
    INTERACTIONS ||--|| INSIGHTS : ""
    INSIGHTS ||--o{ FEEDBACK : ""
    INTERACTIONS ||--|| EVALSAMPLES : ""
    USERS ||--o{ FEEDBACK : ""
"""

# Create the diagram with maximum dimensions for better readability
png_path, svg_path = create_mermaid_diagram(
    diagram_code, 
    png_filepath='journeylens_schema_final.png',
    svg_filepath='journeylens_schema_final.svg',
    width=2000,
    height=1400
)

print(f"Final schema diagram saved to: {png_path} and {svg_path}")