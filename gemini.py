import os
import google.genai as genai


def get_client():
    """Get or create Gemini client"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    return genai.Client(api_key=api_key)



# AI CHAT FUNCTION — Home Tech Solution
def chat_with_knowledge_base(user_question: str, knowledge_base: str, chat_history: list = None) -> str:
    """
    Chat with AI using the Home Tech Solution knowledge base as context.
    """
    system_prompt = f"""You are an expert AI assistant for Home Tech Solution — a smart apartment monitoring system that integrates IoT sensor data, maintenance logs, and energy efficiency insights.

YOUR ROLE:
- Answer questions ONLY using the knowledge base and dataset provided below
- Provide clear, specific, and data-driven responses
- Use exact numbers and metrics from the data (e.g., energy use, temperature, maintenance counts)
- Format your answers in a professional, easy-to-read manner
- If a question is outside the knowledge base, politely explain that you can only answer questions about Home Tech Solution data

RESPONSE GUIDELINES:
1. Start with a direct, factual answer to the user’s question
2. Support your response with metrics or numbers from the knowledge base
3. Use bullet points (hyphens "-") for clarity when listing insights
4. Add short explanations or implications when relevant
5. Keep responses concise but informative
6. Do NOT use asterisks or markdown symbols for emphasis
7. Use proper numeric formatting with commas and decimals where needed
8. Mention time periods or unit IDs if available (e.g., "Unit U493", "January–April period")
9. Keep tone professional and analytical
10. Write in plain, readable English suitable for business reporting

EXAMPLE INTERACTIONS:

User: "When do apartments consume the most energy?"
Good Response: "Apartments consume the most energy during the evening, accounting for 25.63% of total usage. This aligns with higher occupancy levels after work hours."

User: "Which unit has the highest maintenance activity?"
Good Response: "Unit U493 recorded the highest number of maintenance issues. The majority were HVAC-related, indicating possible strain on the cooling system."

User: "What’s the average indoor temperature?"
Good Response: "The average indoor temperature across all monitored units is 69.79°F, suggesting balanced HVAC regulation and optimal comfort."

User: "What’s the most common maintenance issue?"
Good Response: "HVAC failures are the most common issue, with 153 cases representing 44% of total maintenance logs."

KNOWLEDGE BASE:
{knowledge_base}

Remember: Be accurate, concise, and use only information from the knowledge base.
"""

    try:
        client = get_client()
        if chat_history is None:
            chat_history = []

        messages = [system_prompt]
        for msg in chat_history[-10:]:
            messages.append(msg)
        messages.append(f"User Question: {user_question}")

        full_prompt = "\n\n".join(messages)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
            config={
                "temperature": 0.3,
                "top_p": 0.9,
                "max_output_tokens": 1024,
            },
        )

        return response.text or "I couldn't generate a response. Please try again."

    except Exception as e:
        return f"Error: {str(e)}"



# COMPREHENSIVE INSIGHTS REPORT GENERATOR

def generate_comprehensive_report(knowledge_base: str) -> str:
    """
    Generate a detailed, professional Home Tech Solution system insights report.
    """
    prompt = f"""You are Francis Afful Gyan, a Business Intelligence Specialist for Home Tech Solution. 
Generate a comprehensive technical insights report based on the knowledge base below. 
The report should provide meaningful business and operational intelligence related to IoT monitoring, energy management, and maintenance performance.

KNOWLEDGE BASE:
{knowledge_base}

Create a structured report with the following sections:

---
# HOME TECH SOLUTION BUSINESS INSIGHTS REPORT

Date: 26 October 2025
Prepared by: Francis Afful Gyan, Business Intelligence Specialist 

---

## 1. Executive Summary
- Overview of system performance and operational highlights
- Major insights from IoT energy and maintenance dashboards
- Overall energy efficiency and comfort trends

## 2. Energy Performance Analysis
- Total energy consumption across all apartments
- HVAC settings distribution and correlation with energy usage
- Time-of-day and seasonal consumption patterns
- Energy optimization insights and saving potential

## 3. Occupancy and Behavior Insights
- Occupancy vs energy usage analysis
- Energy preferences (warmer, cooler, neutral)
- Behavioral trends affecting consumption

## 4. HVAC Efficiency Assessment
- Average HVAC setting and temperature balance
- Energy usage across high, normal, and low HVAC levels
- Recommendations for optimal HVAC operation

## 5. Maintenance Performance Analysis
- Total maintenance events and issue distribution
- Common failures and seasonal maintenance spikes
- Correlation between energy use and maintenance frequency

## 6. Cross-Domain Insights
- Relationships between energy peaks and maintenance loads
- Impact of occupancy patterns on maintenance activities
- Identification of high-risk or high-load units (e.g., U493)

## 7. Key Operational Challenges
- Identify recurring or high-cost maintenance types
- Detect potential inefficiencies in HVAC systems
- Highlight patterns that may signal predictive maintenance needs

## 8. Strategic Recommendations
- Propose 5–7 actionable recommendations to improve system performance
- Include data-driven reasoning for each recommendation
- Focus on predictive maintenance, smart automation, and tenant comfort

## 9. Conclusion
- Summarize findings and emphasize opportunities for sustainability and efficiency

FORMAT REQUIREMENTS:
- Use # and ## for headings (markdown format)
- Include exact numbers and percentages
- Use plain text (no asterisks or markdown styling)
- Format all numeric values clearly with commas or decimals
- Write professionally, clearly, and concisely
"""

    try:
        client = get_client()
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
            config={
                "temperature": 0.4,
                "top_p": 0.9,
                "max_output_tokens": 8192,
            },
        )

        return response.text or "Unable to generate report."

    except Exception as e:
        return f"Error generating report: {str(e)}"
