import os

try:
    from dotenv import load_dotenv
    load_dotenv()

    MODEL_NAME = os.environ.get("GOOGLE_GENAI_MODEL", "gemini-2.0-flash")
except ImportError:
    print("Warning: python-dotenv not installed. Ensure API key is set")
    MODEL_NAME = "gemini-2.0-flash"

from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools import google_search
from typing import List

from multi_agent.instructions import (
   STOCK_DATA_COLLECTOR_INSTRUCTION,
   TECHNICAL_ANALYSIS_INSTRUCTION,
   INVESTMENT_THESIS_GENERATOR_INSTRUCTION,
   LINKEDIN_CONTENT_CREATOR_INSTRUCTION,
   INSTAGRAM_CONTENT_CREATOR_INSTRUCTION,
   SOCIAL_MEDIA_COORDINATOR_INSTRUCTION,
   FINAL_REPORT_GENERATOR_INSTRUCTION,
   STOCK_SOCIAL_ORCHESTRATOR_INSTRUCTION
)

stock_data_collector = LlmAgent(
     name="StockDataCollector",
    model=MODEL_NAME,
    instruction=STOCK_DATA_COLLECTOR_INSTRUCTION,
    tools=[google_search],  
     output_key="stock_data_summary"
)
    
technical_analyst = LlmAgent(
    name="TechnicalAnalyst", 
    model=MODEL_NAME,
    instruction=TECHNICAL_ANALYSIS_INSTRUCTION,
    output_key="technical_analysis"
)
    
investment_thesis_generator = LlmAgent(
    name="InvestmentThesisGenerator",
    model=MODEL_NAME,
    instruction=INVESTMENT_THESIS_GENERATOR_INSTRUCTION,
    output_key="investment_thesis"
)
    
linkedin_creator = LlmAgent(
    name="LinkedInContentCreator",
    model=MODEL_NAME,
    instruction=LINKEDIN_CONTENT_CREATOR_INSTRUCTION,
    output_key="linkedin_content"
)
    
instagram_creator = LlmAgent(
    name="InstagramContentCreator", 
    model=MODEL_NAME,
    instruction=INSTAGRAM_CONTENT_CREATOR_INSTRUCTION,
    output_key="instagram_content"
)
    
social_media_coordinator = LlmAgent(
    name="SocialMediaCoordinator",
    model=MODEL_NAME,
    instruction=SOCIAL_MEDIA_COORDINATOR_INSTRUCTION,
    output_key="social_media_package"
)
    
report_generator = LlmAgent(
    name="FinalReportGenerator",
    model=MODEL_NAME,
    instruction=FINAL_REPORT_GENERATOR_INSTRUCTION,
    output_key="final_report"
)

social_media_parallel_agent = ParallelAgent(
    name="SocialMediaContentCreators",
    sub_agents=[linkedin_creator, instagram_creator]
)
    
stock_social_orchestrator = SequentialAgent(
    name="StockAnalysisAndSocialMediaAssistant",
    description=STOCK_SOCIAL_ORCHESTRATOR_INSTRUCTION,
    sub_agents=[
            stock_data_collector,           # Sequential: Collect data
            technical_analyst,              # Sequential: Analyze trends  
            investment_thesis_generator,    # Sequential: Generate thesis
            social_media_parallel_agent,    # Parallel: Create LinkedIn + Instagram content
            social_media_coordinator,       # Sequential: Coordinate content
            report_generator               # Sequential: Generate final report
        ]
)
    
root_agent = stock_social_orchestrator