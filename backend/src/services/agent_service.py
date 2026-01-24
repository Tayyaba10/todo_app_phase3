import openai
from typing import Dict, Any, Optional, List
from uuid import UUID
from datetime import datetime
from ..models.conversation import Conversation
from ..models.message import Message, SenderType
from ..services.task_service import TaskService
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from sqlmodel import Session


class AgentService:
    def __init__(self, db_session: Session, openai_api_key: str):
        self.db_session = db_session
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.task_service = TaskService(db_session)
        self.conversation_service = ConversationService(db_session)
        self.message_service = MessageService(db_session)

    def process_user_message(
        self,
        user_id: UUID,
        message_content: str,
        conversation_id: Optional[UUID] = None
    ) -> Dict[str, Any]:
        """
        Process a user message through the AI agent and return the response.
        """
        # Get or create conversation
        if conversation_id:
            conversation = self.conversation_service.get_conversation_by_id_with_messages(conversation_id)
        else:
            # Create new conversation
            from ..models.conversation import ConversationCreate
            conversation_data = ConversationCreate(user_id=user_id, title=message_content[:50])
            conversation = self.conversation_service.create_conversation(conversation_data)

        if not conversation:
            raise ValueError("Could not create or retrieve conversation")

        # Save user message using conversation service
        self.conversation_service.save_user_message(
            conversation_id=conversation.id,
            content=message_content
        )

        # Retrieve conversation history for context
        conversation_history = self.conversation_service.get_conversation_history(conversation.id)

        # Prepare the conversation history for the agent
        messages_for_agent = []
        # Add system message
        messages_for_agent.append({
            "role": "system",
            "content": "You are a helpful AI assistant that manages todos for users. "
                      "Use the available tools to create, list, update, and delete tasks. "
                      "Always respond in a friendly and helpful manner."
        })

        # Add conversation history
        for msg in conversation_history:
            role = "user" if msg.sender_type == SenderType.user else "assistant"
            messages_for_agent.append({
                "role": role,
                "content": msg.content
            })

        # Call the OpenAI API with function calling
        response = self.openai_client.chat.completions.create(
            model="gpt-4-turbo",  # Using a capable model
            messages=messages_for_agent,
            tools=self._get_available_tools(),
            tool_choice="auto"
        )

        # Process the response
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # If the agent wants to use tools
        if tool_calls:
            # Execute the tools and get results
            tool_results = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                try:
                    # Safely evaluate function arguments
                    function_args = eval(tool_call.function.arguments)
                except Exception:
                    # If eval fails, try to parse as JSON
                    import json
                    try:
                        import ast
                        function_args = ast.literal_eval(tool_call.function.arguments)
                    except:
                        function_args = {}

                # Execute tool with retry logic
                result = self._execute_tool_with_retry(function_name, function_args, user_id)
                tool_results.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": self._handle_tool_execution_errors(result)
                })

            # Get final response from the model with tool results
            final_messages = messages_for_agent + [
                response_message,
            ] + tool_results

            try:
                final_response = self.openai_client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=final_messages
                )

                agent_reply = final_response.choices[0].message.content
            except Exception as e:
                # Handle error in final response generation
                agent_reply = f"I encountered an error processing your request: {str(e)}. Could you please rephrase your request?"
        else:
            # No tools needed, just return the model's response
            agent_reply = response_message.content

        # Save agent response using conversation service
        self.conversation_service.save_agent_message(
            conversation_id=conversation.id,
            content=agent_reply
        )

        return {
            "response": agent_reply,
            "conversation_id": conversation.id,
            "tool_calls": [call.model_dump() for call in tool_calls] if tool_calls else []
        }

    def _get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Define the available tools that the agent can use.
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "create_todo",
                    "description": "Create a new todo item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The title of the todo"},
                            "description": {"type": "string", "description": "The description of the todo"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_todos",
                    "description": "List all todo items for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_todo",
                    "description": "Update a todo item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {"type": "string", "description": "The ID of the todo to update"},
                            "title": {"type": "string", "description": "The new title of the todo"},
                            "description": {"type": "string", "description": "The new description of the todo"},
                            "completed": {"type": "boolean", "description": "Whether the todo is completed"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_todo",
                    "description": "Delete a todo item",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {"type": "string", "description": "The ID of the todo to delete"}
                        },
                        "required": ["todo_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "request_clarification",
                    "description": "Request clarification from the user when the request is ambiguous",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string", "description": "The question to ask the user for clarification"}
                        },
                        "required": ["question"]
                    }
                }
            }
        ]

    def _execute_tool(self, function_name: str, function_args: Dict[str, Any], user_id: UUID) -> Any:
        """
        Execute the specified tool with the given arguments.
        """
        try:
            if function_name == "create_todo":
                return self.task_service.create_task(user_id, **function_args)
            elif function_name == "list_todos":
                return self.task_service.get_tasks_by_user(user_id)
            elif function_name == "update_todo":
                if "todo_id" in function_args:
                    todo_id = function_args.pop("todo_id")
                    return self.task_service.update_task(todo_id, **function_args)
                else:
                    return {"error": "todo_id is required for update_todo"}
            elif function_name == "delete_todo":
                return self.task_service.delete_task(function_args.get("todo_id"))
            elif function_name == "request_clarification":
                # Return the question to ask the user for clarification
                return {"clarification_needed": function_args.get("question", "I need more information to help you")}
            else:
                return {"error": f"Unknown function: {function_name}"}
        except Exception as e:
            return {"error": f"Error executing {function_name}: {str(e)}"}

    def _handle_tool_execution_errors(self, tool_call_result: Any) -> str:
        """
        Handle errors from tool execution and format appropriate responses.
        """
        if isinstance(tool_call_result, dict) and "error" in tool_call_result:
            return tool_call_result["error"]
        return str(tool_call_result)

    def _execute_tool_with_retry(self, function_name: str, function_args: Dict[str, Any], user_id: UUID, max_retries: int = 3) -> Any:
        """
        Execute a tool with retry logic for failed calls.
        """
        last_exception = None

        for attempt in range(max_retries):
            try:
                result = self._execute_tool(function_name, function_args, user_id)
                # If successful, return the result
                if not (isinstance(result, dict) and "error" in result):
                    return result
                # If it's a known error that shouldn't be retried, return it
                if "clarification_needed" in result:
                    return result
            except Exception as e:
                last_exception = e
                # Wait briefly before retrying (could implement exponential backoff)
                import time
                time.sleep(0.5)

        # If all retries failed, return the error
        if last_exception:
            return {"error": f"Error executing {function_name} after {max_retries} attempts: {str(last_exception)}"}
        else:
            return {"error": f"Error executing {function_name} after {max_retries} attempts"}