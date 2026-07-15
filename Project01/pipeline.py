from Prompts.user_query import query_prompt
from Prompts.direct_answer import answer_prompt
from Prompts.support_ticket import support_ticket_prompt

from langchain_core.chat_history import InMemoryChatMessageHistory

from LLM.brain import llm

from Pydantic.layer01 import QueryAnalysis
from Pydantic.support_ticket import SupportTicket

from tools.helper_functions import (
    get_order_status,
    delivery_charge_calculator,
    estimate_delivery_time
)



# 1. HISTORY


history = InMemoryChatMessageHistory()



# 2. QUERY ANALYSIS CHAIN


structured_llm = llm.with_structured_output(QueryAnalysis)

query_chain = query_prompt | structured_llm


# ==================================================
# 3. DIRECT ANSWER CHAIN
# ==================================================

answer_chain = answer_prompt | llm


# ==================================================
# 4. SUPPORT TICKET CHAIN
# ==================================================

ticket_chain = (
    support_ticket_prompt
    | llm.with_structured_output(SupportTicket)
)


# ==================================================
# 5. TOOLS
# ==================================================

tools = [
    get_order_status,
    delivery_charge_calculator,
    estimate_delivery_time
]

llm_with_tools = llm.bind_tools(tools)


tools_by_name = {
    tool.name: tool
    for tool in tools
}


# ==================================================
# 6. CUSTOMER INFORMATION
# ==================================================

customer_name = input(
    "Enter customer name: "
).strip()

customer_type = input(
    "Enter customer type (Premium/Standard): "
).strip()


# ==================================================
# 7. CONVERSATION LOOP
# ==================================================

while True:

    user_query = input("\nYou: ").strip()

    # Exit conversation
    if user_query.lower() in ["exit", "quit"]:
        print("SmartKart: Thank you for contacting SmartKart.")
        break


    # ==================================================
    # 8. ANALYZE QUERY WITH PREVIOUS HISTORY
    # ==================================================

    analysis_result = query_chain.invoke({
        "customer_name": customer_name,
        "customer_type": customer_type,
        "history": history.messages,
        "user_query": user_query
    })


    # Debugging only
    print("\n[DEBUG] Analysis:", analysis_result)


    # ==================================================
    # 9. ROUTING
    # ==================================================

    if analysis_result.required_action == "direct_answer":

        answer_result = answer_chain.invoke({
            "problem_details": analysis_result.problem_details,
            "intent": analysis_result.intent
        })

        final_answer = answer_result.content


    elif analysis_result.required_action == "tool_required":

        tool_response = llm_with_tools.invoke(
            f"""
Customer Name: {customer_name}
Customer Type: {customer_type}

Original Customer Query:
{user_query}

Resolved Problem Details:
{analysis_result.problem_details}

Customer Intent:
{analysis_result.intent}

Select and call the appropriate tool required
to handle the customer's request.
"""
        )


        if tool_response.tool_calls:

            tool_results = []

            for tool_call in tool_response.tool_calls:

                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                selected_tool = tools_by_name[tool_name]

                actual_tool_result = selected_tool.invoke(
                    tool_args
                )

                # Debugging only
                print(
                    f"[DEBUG] Tool: {tool_name}"
                )

                print(
                    f"[DEBUG] Arguments: {tool_args}"
                )

                print(
                    f"[DEBUG] Result: {actual_tool_result}"
                )

                tool_results.append(
                    str(actual_tool_result)
                )


            final_answer = " ".join(tool_results)

        else:

            final_answer = (
                "I could not determine the appropriate "
                "tool for your request."
            )


    elif analysis_result.required_action == "support_issue":

        ticket_result = ticket_chain.invoke({
            "customer_issue": user_query
        })


        # Debugging only
        print(
            "[DEBUG] Support Ticket:",
            ticket_result
        )


        final_answer = (
            f"Your issue has been forwarded to the "
            f"{ticket_result.recommended_team}. "
            f"Priority: {ticket_result.priority}."
        )


    # ==================================================
    # 10. DISPLAY FINAL ANSWER
    # ==================================================

    print(
        f"\nSmartKart: {final_answer}"
    )


    # ==================================================
    # 11. SAVE COMPLETED CONVERSATION TO MEMORY
    # ==================================================

    history.add_user_message(
        user_query
    )

    history.add_ai_message(
        final_answer
    )