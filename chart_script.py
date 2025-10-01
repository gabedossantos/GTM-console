# Create a comprehensive technical architecture diagram for JourneyLens
diagram_code = """
flowchart TD
    subgraph "Frontend Layer"
        A[Next.js React App]
        B[Role Views<br/>CSM/AE/Support]
        C[Dashboard UI]
    end
    
    subgraph "Backend Layer"
        D[FastAPI Backend]
        E[Auth Service]
        F[API Routes]
    end
    
    subgraph "AI/ML Pipeline"
        G[LLM Service<br/>OpenAI/Local]
        H[RAG Pipeline]
        I[Embeddings<br/>Transformers]
        J[Intent Analysis]
    end
    
    subgraph "Data Layer"
        K[(PostgreSQL<br/>Accounts/Contacts)]
        L[(Vector DB<br/>Embeddings)]
    end
    
    subgraph "External"
        M[File Upload<br/>txt/md files]
        N[CRM Integration]
    end
    
    %% Data Flow 1: Upload → Process → Store
    M --> D
    D --> H
    H --> I
    I --> L
    L --> K
    
    %% Data Flow 2: Query → Retrieve → Generate
    A --> D
    D --> H
    H --> L
    L --> G
    G --> A
    
    %% Data Flow 3: Feedback → Evaluate → Improve
    A --> E
    E --> K
    K --> J
    J --> G
    
    %% Component connections
    A --> B
    B --> C
    D --> E
    E --> F
    N --> D
"""

# Create the mermaid diagram
png_path, svg_path = create_mermaid_diagram(
    diagram_code, 
    'journeylens_architecture.png',
    'journeylens_architecture.svg'
)

print(f"Architecture diagram saved to {png_path} and {svg_path}")